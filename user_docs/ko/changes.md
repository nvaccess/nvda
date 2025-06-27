# NVDA 변경사항

## 2025.1

이번 릴리스에서는 NVDA 원격 접근(Remote Access) 기능이 도입되었습니다. 이 기능을 통해 NVDA가 실행 중인 다른 기기에서 NVDA가 실행 중인 원격 컴퓨터를 제어할 수 있습니다.

음성 관련 기능이 많이 개선되었으며, 특히 SAPI 4, SAPI 5, OneCore 음성의 응답성이 향상되었습니다.
이제 SAPI 5에서 음성 속도 증폭(Rate boost) 및 자동 언어 전환 기능이 지원됩니다.
SAPI 4 음성에서 오디오 더킹(audio ducking), 앞부분 묵음 제거(leading silence trimming), 오디오 장치 활성 상태 유지(keeping the audio device awake) 기능이 지원됩니다.

추가 기능 스토어(Add-on Store)의 자동 업데이트 시스템이 개선되어, 자동 업데이트 채널 선택 및 백그라운드 자동 업데이트 실행이 가능해졌습니다.

수동 OCR 결과 갱신 또는 자동 갱신 여부를 전환하는 새로운 단축키가 추가되었습니다.

이제 Chrome 및 Edge 브라우저에서 네이티브 선택(Native selection) 기능을 사용할 수 있습니다.

Microsoft Office 및 LibreOffice 지원 기능이 향상되었으며, 특히 더 많은 단축키를 음성으로 안내하게 되었습니다.

이제 설정된 NVDA 언어에 따라 기본 입력 및 출력 점자표를 결정할 수 있습니다.
닷 잉크(Dot Inc.)의 촉각 그래픽 장치인 닷 패드(Dot Pad)가 다중 라인 점자 디스플레이로서 기본 지원(Native support) 목록에 추가되었습니다.
점자 디스플레이와 관련하여 사소한 수정 사항들이 있었으며, 특히 연결성 문제가 개선되었습니다.

LibLouis 점자 변환기, eSpeak-NG, Unicode CLDR이 업데이트되었습니다.
새로운 콥트어, 축약형 쐐기 문자, 포르투갈어 6점 컴퓨터 점자 테이블을 사용할 수 있습니다.

### 중요 참고 사항

* 이번 릴리스는 기존 부가 기능과 호환되지 않습니다.

### 보안 수정 사항

보안 문제는 NVDA의 [보안 정책](https://github.com/nvaccess/nvda/blob/master/security.md)에 따라 책임감 있게 신고해 주시기 바랍니다.

* 기기가 잠겨 있을 때 점자 디스플레이에 민감할 수 있는 정보가 표시되지 않도록 수정했습니다.
([GHSA-8f8q-2jc3-6rf4](https://github.com/nvaccess/nvda/security/advisories/GHSA-8f8q-2jc3-6rf4))
* 설치 프로그램이 디렉토리에서 원치 않는 DLL을 로드하지 못하도록 합니다.
([GHSA-qf5h-qw92-rx2f](https://github.com/nvaccess/nvda/security/advisories/GHSA-qf5h-qw92-rx2f))

### 새로운 기능

* 추가 기능 스토어:
  * 자동 업데이트 (#3208):
    * 추가 기능의 자동 업데이트 채널을 이제 수정할 수 있습니다.
      * 업데이트 채널 하위 메뉴를 통해 추가기능 업데이트 채널을 선택할 수 있습니다.
      * NVDA 설정의 추가 기능 스토어 패널에서 기본 자동 업데이트 채널을 설정할 수 있습니다.
    * 이제 백그라운드에서 자동 업데이트가 진행될 수 있습니다.
      * NVDA 설정의 부가 기능 스토어 패널에서 "자동 업데이트" 설정을 "자동으로 업데이트"로 변경하여 이 기능을 활성화할 수 있습니다.
    * 호환되지 않는 부가 기능도 최신 버전(여전히 호환되지 않을 수 있음)으로 자동 업데이트할 수 있습니다.
      * NVDA 설정의 추가 기능 스토어 패널에서 이 기능을 활성화할 수 있습니다.
  * 추가 기능 설치를 취소하는 작업이 추가되었습니다. (#15578, @hwf1324)
  * 추가 기능 다운로드/설치 실패 시 재시도하는 작업이 추가되었습니다. (#17090, @hwf1324)
  * 이제 추가 기능 목록을 게시 날짜 등을 포함한 열 기준으로 오름차순 또는 내림차순 정렬할 수 있습니다. (#15277, #16681, @nvdaes)
* 말하기:
  * Microsoft Speech API version 5 (SAPI5) 및 Microsoft Speech 플랫폼 음성 사용 시 자동 언어 전환을 지원합니다. (#17146, @gexgd0419)
  * Microsoft Speech API Version 5 (SAPI5) 및 Microsoft Speech 플랫폼 음성 사용 시 음성 속도 부스트를 지원하며 6배속을 지원합니다. (#17606, @gexgd0419)
* 웹 브라우저:
  * 이제 Google Chrome, Edge 및 Chromium 134 이상 기반의 다른 애플리케이션에서 NVDA 탐색 모드의 네이티브 선택 모드(`NVDA+Shift+F10`)가 지원됩니다. (#17838)
  * Mozilla Firefox에서 텍스트 조각(text fragment)이 포함된 URL을 방문하면, NVDA가 URL에 의해 강조된 텍스트를 읽어줍니다. (#16910, @jcsteh)
  * 이제 NVDA는 대상이 현재 페이지를 가리키는 링크를 알립니다. (#141, @LeonarddeR, @nvdaes)
* Microsoft Office:
  * Microsoft PowerPoint에서 텍스트 상자를 편집할 때 `alt+upArrow와`alt+downArrow` 키를 통해 문장 단위로 이동할 수 있습니다. (#17015, @LeonarddeR)
  * Microsoft Word에서 이제 Word 명령(`f8` or `shift+f8`)을 사용하여 선택을 확장하거나 줄일 때 선택 업데이트가 보고됩니다. (#3293, @CyrilleB79)
  * 워드 버전 16.0.18226 이상 또는 워드 객체 모델 사용 시, 제목이 축소되었는지 여부를 NVDA가 음성과 점자로 알려줍니다. (#17499)
  * UIA를 사용하는 워드에서 기본 확장 표 탐색 명령(Alt+Home, Alt+End, Alt+PageUp, Alt+PageDown) 사용 시, 이제 캐럿 이동이 보고됩니다. (#17867, @CyrilleB79)
  * 워드에서 "포커스 보고" 명령 사용 시, 이 정보가 사용 가능하고 객체 설명 보고가 활성화된 경우 문서 레이아웃이 안내됩니다. (#15088, @nvdaes)
  *  Word 및 Outlook에서 더 많은 단축키의 결과가 이제 보고됩니다:
    * 글꼴 서식 단축키 (#10271, @CyrilleB79)
    * 제목 축소 또는 확장 (#17545, @CyrilleB79)
* LibreOffice:
  * Writer에서 단축키를 통해 글자 크기를 키우거나 줄일 때 변경된 글자 크기를 알립니다. (#6915, @michaelweghorn)
  * Writer 25.2 이상에서 "본문 텍스트" 또는 제목 문단 스타일을 적용할 때, NVDA가 새로 적용된 문단 스타일을 알립니다. (#6915, @michaelweghorn)
  * Writer에서 단축키를 통해 이중 밑줄로 전환할 때, NVDA가 새로운 상태("이중 밑줄 켬"/"이중 밑줄 끔")을 알립니다. (#6915, @michaelweghorn)
  * LibreOffice 25.8 이상에서 NVVDA가 첫줄 들여쓰기을 알릴 수 있습니다. (#13052, @michaelweghorn)
* OCR:
  * 인식 결과 내에서 `NVDA+f5` 키 사용 시 수동으로 인식된 텍스트를 갱신합니다. (#17715, @CyrilleB79)
  * OCR 결과의 주기적 갱신을 위한 새로운 제스처(단축키 지정 안 됨)가 추가됩니다. (#16897)
* NVDA 원격(Remote) 추가 기능에 기반한 원격 접근 기능이 NVDA에 통합되었습니다. (#4390, @ctoth, @tspivey, @daiverd, NVDA Remote  기여자 및 후원자)
* 이제 NVDA 업데이트와 추가 기능 스토어에 사용할 미러 URL을 지정할 수 있습니다. (#14974, #17151, #17310, @christopherpross)
* PDF 내 수학 콘텐츠 지원이 추가되었습니다. (#9288, @NSoiffer)
  * 이것은 최신 버전의 TeX/LaTeX에서 생성된 일부 파일과 같은 MathML과 관련된 공식에서 작동합니다.
  * 현재 이 기능은 Foxit Reader 및 Foxit Editor에서만 지원됩니다.
* 이제 점자 탐색 키로 이동할 때 현재 줄이나 단락을 음성으로 출력하도록 NVDA를 설정할 수 있습니다. (#17053, @nvdaes)
* 이제 예를 들어 Visual Studio Code 등에서 Alt+위쪽 화살표 또는 Alt+아래쪽 화살표 제스처를 누를 때 NVDA가 캐럿 변경 사항을 보고할 수 있습니다. (#17652, @LeonarddeR)
* 선택된 텍스트의 첫 문자와 마지막 문자로 리뷰 커서를 이동하는 명령이 추가되었으며, 각각 NVDA+Alt+Home 및 NVDA+Alt+End 키에 할당되었습니다. (#17299, @nvdaes)
* 전체 읽기 또는 점자 읽기 중 디스플레이가 꺼지는 것을 방지하는 일반 설정이 추가되었습니다.
이 옵션은 기본적으로 활성화되어 있지만, 배터리 소모가 증가할 수 있습니다. (#17649, @LeonarddeR)
* 이제 NVDA가 보스니아어를 지원합니다. (#17953)
* Microsoft Word로 생성된 PDF 문서 내 수학 방정식을 Adobe Acrobat 사용 시 NVDA로 읽고 상호작용할 수 있습니다. (#18056)

### 변경사항

* 구성요소 업데이트:
  * LibLouis 점자 변환기가 3.33.0 버전으로 업데이트되었습니다. (#17469, #17768, @LeonarddeR, @codeofdusk)
    * 새로운 콥트어, 축약형 쐐기 문자, 포르투갈어 6점 컴퓨터 점자 테이블이 추가되었습니다.
  * CLDR이 46.0 버전으로 업데이트되었습니다. (#17484, @OzancanKaratas)
  * eSpeak NG가 1.52.0 버전으로 업데이트되었습니다. (#17056)
* NVDA 인터페이스 변경사항:
  * NVDA 설치파일 실행 시 더 이상 소리를 재생하지 않습니다. (#14068)
  * 사용자 편의를 위해 링크 주소 알림, 글자 서식 정보 및 선택 내용 말하기 대화상자에 "닫기" 및 "복사" 버튼이 추가되었습니다. (#17018, @XLTechie)
  * NVDA 종료 대화상자에 새로운 옵션이 추가됩니다: 추가 기능을 비활성화하고 디버그 로그 활성화하여 재시작 (#11538, @CyrilleB79)
  * 오디오 출력을 위해 WASAPI를 사용하지 않도록 선택하는 기능이 제거되었습니다. (#16080)
  * 브라우즈 모드 설정의 "자동으로 초점 이동 가능한 요소에 시스템 초점 이동"이 제거되었습니다, 이 동작은 비활성화됩니다. (#17598)
  * 이제 NVDA는 현재 버전과 추가기능 API가 호환되지 않는 새 버전으로 업데이트할 때만 추가기능 호환성 경고를 표시합니다. (#17071, #17506)
  * "기여자 목록" 파일이 NVDA 메뉴에서 삭제됩니다. (#16922)
  * 가독성을 위해 NVDA 라이선스를 이제 HTML로 제공합니다. (#17600)
  * 자주 사용하는 명령줄 옵션의 단축 옵션이 추가되었습니다: `-d` 명령은 `--disable-addons`의 단축 명령이며 `-n` 명령은 `--lang`의 단축 명령입니다.
  명령줄 플래그의 접두사 일치(예를들어 `--disable-addons`를 사용하기 위해 `--di`를 사용)을 더이상 지원하지 않습니다. (#11644, @CyrilleB79)
  * COM Registration 문제 해결 도구 변경사항(재설정 도구에서 문제 해결 도구로 명칭 변경됨): (#12355, @XLTechie)
    * 이제 경고 대신 사용자 친화적인 목적 설명으로 시작합니다. (#12351)
    * 초기 창은 이제 Esc 또는 Alt+F4 키로 종료할 수 있습니다. (#10799)
    * COM 재등록 시도 중 드물게 윈도우 오류가 발생하는 경우, 이제 오류를 포함한 메시지를 사용자에게 표시합니다.
* 음성:
  * 마이크로소프트 스피치 API 버전 5 및 마이크로소프트 스피치 플랫폼 음성은 이제 오디오 출력에 WASAPI를 사용하며, 이로 인해 해당 음성의 반응성이 향상될 수 있습니다. (#13284, @gexgd0419)
  * OneCore 음성, SAPI5 음성 및 일부 타사 음성 애드온 사용 시, 반응성 개선을 위해 음성 시작 부분의 침묵이 이제 제거됩니다. (#17614, @gexgd0419)
  * 마이크로소프트 스피치 API 버전 4 음성은 이제 오디오 출력에 WASAPI를 사용하므로, 오디오 더킹, 시작 침묵 제거, 오디오 장치 깨우기 유지와 같은 기능과 함께 작동할 수 있습니다.
  만약 사용하는 SAPI 4 음성에서 이 기능이 작동하지 않는다면, 고급 설정에서 SAPI 4용 WASAPI를 비활성화할 수 있습니다. (#17718, #17801, @gexgd0419)
  * 이제 음성 출력에 유니코드 정규화가 기본적으로 활성화됩니다. (#17017, @LeonarddeR).
    * NVDA 설정 대화 상자의 음성 카테고리에서 이 기능을 비활성화할 수 있습니다.
* "입력 문자 읽기" 및 "입력 단어 읽기" 키보드 설정에는 이제 꺼짐, 편집창에서만, 항상의 세 가지 옵션이 있습니다. (#17505, @Cary-rowen)
  * 기본적으로 "입력 문자 읽기"는 이제 "편집창에서만"으로 설정됩니다.
* 이제 NVDA 언어를 기반으로 기본 입출력 점자 테이블을 결정할 수 있습니다. (#17306, #16390, #290, @nvdaes)

### 버그 수정

* 음성:
  * 일부 SAPI5 음성엔진 사용 시, 연속 읽기(모두 읽기)가 첫 문장 끝에서 멈추던 문제를 수정했습니다. (#16691, @gexgd0419)
  * SAPI5 및 SAPI4 음성 합성기에서 음성 설정 링을 사용해 음성을 전환할 때, 음성 속도 및 볼륨과 같은 음성 매개변수가 기본값으로 초기화되지 않도록 수정했습니다. (#17693, #2320, @gexgd0419)
  * 일부 SAPI4 음성(예: IBM TTS 중국어)을 불러올 수 없던 문제를 수정했습니다. (#17726, @gexgd0419)
* 점자:
  * Dot Inc의 다중 라인 점자 디스플레이인 Dot Pad 촉각 그래픽 장치를 네이티브로 지원합니다. (#17007)
  * Seika 노트테이커를 사용할 때, 스페이스 및 스페이스 + 점 조합 제스처가 입력 제스처 대화상자에 올바르게 표시됩니다. (#17047, @school510587)
  * 점자 디스플레이가 연결되지 않은 상태에서 음성 출력 점자 모드를 사용할 때, 더 이상 오류음을 재생하거나 로그 파일에 과도한 메시지를 기록하지 않습니다. (#17092, @Emil-18)
  * 표준 HID 점자 디스플레이 드라이버가 점자 디스플레이 드라이버로 명시적으로 선택된 경우, 점자 디스플레이 목록을 열면 NVDA가 HID 드라이버를 올바르게 선택된 드라이버로 인식합니다. (#17537, @LeonarddeR)
  * Humanware Brailliant 드라이버가 올바른 연결 지점을 보다 안정적으로 선택할 수 있게 개선되어, 연결 안정성이 향상되고 오류가 줄어듭니다. (#17537, @LeonarddeR)
  * 개발자 스크래치패드에 있는 사용자 지정 점자표는 추가기능을 비활성화한 상태에서 무시되도록 수정되었습니다. (#17565, @LeonarddeR)
  * NVDA에서 일부 USB 점자 디스플레이가 적절하게 감지되지 않던 문제가 해결되었습니다. (#18114, @christiancomaschi)
* Microsoft Office:
  * 링크의 대상 URL을 보고하는 명령이 이제 Word, Outlook, Excel 및 PowerPoint의 레거시 객체 모델 사용 시 정상적으로 작동합니다. (#17292, #17362, #17435, @CyrilleB79)
  * Excel에서 요소 목록 대화상자(`NVDA+f7`)가 일부 비영어 시스템에서 주석이나 수식을 나열하지 못하던 문제를 수정했습니다. (#11366, @CyrilleB79)
  * PowerPoint 개선 사항:
    * 텍스트에 이모지 같은 넓은 문자가 포함되어 있을 때, 캐럿 보고가 중단되던 문제를 수정했습니다. (#17006, @LeonarddeR)
    * 문자 위치 알림이 정확해졌습니다 (`NVDA+Delete` 키를 눌렀을 때 등). (#9941, @LeonarddeR)
    * 슬라이드 쇼를 시작할 때, 그리고 탐색 모드 설정 "페이지 로드 시 자동 모두 읽기"가 비활성화된 경우, NVDA가 더 이상 모두 읽기를 시작하지 않습니다. (#17488, @LeonarddeR)
* LibreOffice:
  * 중국어용 마이크로소프트 병음 입력기를 사용하고 이전 버전을 사용하도록 병음 호환성 옵션을 활성화한 경우, IME 팝업이 표시되는 동안 Writer(및 잠재적으로 다른 응용 프로그램)에서 입력해도 더 이상 오류가 발생하지 않습니다. (#17198, @michaelweghorn)
  * 대화 상자 내 체크박스의 현재 상태(체크됨/체크 해제됨)가 이제 음성뿐만 아니라 점자로도 보고됩니다. (#17218, @michaelweghorn)
* 수학:
  * 일부 웹 요소에 대한 수식 읽기가 수정되었습니다.
  리치 탐색을 위한 MathML 없이 이미지와 대체 텍스트로만 표시되는 수학 방정식은 이제 내용 없는 수식이 아닌 일반 이미지처럼 처리되어 사용자가 g 키로 해당 위치로 이동하고 화살표 키를 사용하여 문자 단위로 대체 텍스트를 탐색할 수 있습니다. (#16007)
  * MathML 없이 이미지와 대체 텍스트만으로 표현된 수학 방정식은 이제 "내용이 없는 수학"이 아닌 일반 이미지로 처리되어, `g` 키로 탐색할 수 있고, 대체 텍스트를 문자 단위로 탐색할 수 있습니다. (#16007)
* IDE:
  * Android Studio 또는 IntelliJ Idea의 특정 소스 파일에서 전체 텍스트를 선택할 때 NVDA가 충돌하지 않도록 수정되었습니다. (#17418, @thgcode)
  * Visual Studio Code에서 문장 단위 탐색을 위한 `Alt+위/아래 화살표` 제스처를 NVDA가 가로채지 않도록 수정되었습니다. (#17082, @LeonarddeR)
  * Visual Studio Code에서 특정 section 요소를 편집 가능한 컨트롤로 올바르게 인식하도록 수정했습니다. (#17573, @Cary-rowen)
  * Notepad 및 기타 UIA 문서, Windows 11의 Notepad++ 문서에서 마지막 줄이 비어 있을 경우, "점자 다음 줄 명령"이 커서를 마지막 줄로 이동시킵니다.
  또한, 커서가 마지막 줄에 있을 경우 해당 명령을 사용하면 커서가 줄 끝으로 이동합니다. (#17251, #17430, @nvdaes)
* 설정 프로필:
  * "모두 읽기"를 설정 프로필에서 활성화했을 때 점자가 비정상적으로 동작하던 문제가 수정되었습니다. (#17163, @LeonarddeR)
  * 특정 설정값이 기본 구성과 동일하더라도, 활성 프로필에 명시적으로 저장되던 문제를 수정했습니다. (#17157, @LeonarddeR)
* 철자 읽기 시 유니코드 정규화 관련:
  * 정규화된 문자를 보고한 후, 이후 문자들이 잘못 정규화되어 보고되지 않도록 수정했습니다. (#17286, @LeonarddeR)
  * 합성 문자(é 등)가 올바르게 보고되도록 수정했습니다. (#17295, @LeonarddeR)
* Thunderbird 검색 결과 페이지의 하위 메뉴 항목을 NVDA가 읽을 수 있게 되었습니다. (#4708, @thgcode)
* COM 등록 복구 도구가 실패 시 성공으로 잘못 보고하지 않도록 수정되었습니다. (#12355, @XLTechie)
* Windows 11의 클립보드 기록 창을 닫을 때 항목이 남아 있는 경우, NVDA가 항목을 읽지 않도록 수정되었습니다. (#17308, @josephsl)
* 브라우저 가능한 메시지를 연 상태에서 플러그인을 다시 로드해도 NVDA가 이후 포커스 이동을 제대로 보고합니다. (#17323, @CyrilleB79)
* Skype, Discord, Signal, Phone Link 등 음성 통화용 응용 프로그램 사용 중, NVDA 음성 및 소리 볼륨이 줄어들지 않도록 수정되었습니다. (#17349, @jcsteh)
* NVDA Python 콘솔을 열 때 스냅샷 변수를 가져오는 중 오류가 발생하더라도 열리지 않는 문제가 발생하지 않도록 수정되었습니다. (#17391, @CyrilleB79)
* 웹 브라우저에서 편집 가능한 텍스트 컨트롤 내의 텍스트 선택 변경사항이 간혹 보고되지 않던 문제를 수정했습니다. (#17501, @jcsteh)
* 앵커 링크가 가상 캐럿 위치와 동일한 객체를 가리키는 경우, NVDA가 링크 대상으로 스크롤하지 못하는 문제를 수정했습니다. (#17669, @nvdaes)
* NVDA 강조 창 아이콘이 Explorer 재시작 후 작업 표시줄에 고정된 상태로 남지 않도록 수정되었습니다. (#17696, @hwf1324)

### Changes for Developers

Please refer to [the developer guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) for information on NVDA's API deprecation and removal process.

* 참고: 이것은 추가기능 API 호환성을 깨뜨리는 릴리즈입니다.
추가기능은 재테스트를 거쳐 매니페스트를 업데이트해야 합니다.
* 구성요소 업데이트:
  * Ruff가 0.8.1로 업데이트되었습니다. (#17102, #17260, #17473)
  * Comtypes가 1.4.6으로 업데이트되었습니다. (#17061, @LeonarddeR)
  * wxPython이 4.2.2로 업데이트되었습니다. (#17181, @dpy013)
  * SCons가 4.8.1로 업데이트되었습니다. (#17254)
  * sphinx가 8.1.2로, sphinx-rtd-theme이 3.0.1로 업데이트되었습니다. (#17284, @josephsl)
  * Robot Framework가 7.1.1로 업데이트되었습니다. (#17329, @josephsl)
  * configobj가 5.1.0 커밋 `8be5462`로 업데이트되었습니다. (#17328)
  * pre-commit이 4.0.1로 업데이트되었습니다. (#17260)
  * typing-extensions가 4.12.2로 업데이트되었습니다. (#17438, @josephsl)
  * licensecheck가 2024.3으로 업데이트되었습니다. (#17440, @josephsl)
  * markdown이 3.7로 업데이트되었습니다. (#17459, @josephsl)
  * nh3이 0.2.19로 업데이트되었습니다. (#17465, @josephsl)
  * nuitka가 2.5.4로 업데이트되었습니다. (#17458, @josephsl)
  * schedule이 1.2.2로 업데이트되었습니다. (#17455, @josephsl)
  * requests가 2.32.3으로 업데이트되었습니다. (#17456, @josephsl)
* 이제 `ui.browseableMessage`를 호출할 때 클립보드로 복사 버튼과/또는 창 닫기 버튼을 표시하는 옵션을 사용할 수 있습니다. (#17018, @XLTechie)
* 링크 유형을 식별하기 위한 여러 추가 사항이 포함되었습니다. (#16994, @LeonarddeR, @nvdaes)
  * 링크 유형을 결정하는 다양한 함수가 포함된 새로운 `utils.urlUtils` 모듈이 추가되었습니다.
  * `controlTypes.states.State`에 새로운 `INTERNAL_LINK` 상태가 추가되었습니다.
  * `NVDAObject`에 새로운 `linkType` 속성이 추가되었습니다.
  기본적으로 `treeInterceptor`가 있는 경우 이를 쿼리합니다.
  * `BrowseModeTreeInterceptor` 객체에 새로운 `documentUrl` 속성이 추가되었습니다.
  * `BrowseModeTreeInterceptor` 객체에 URL을 받아 객체의 링크 유형을 확인하는 `getLinkTypeInDocument` 메서드가 추가되었습니다.
  * `globalCommands`에 `toggleBooleanValue` 헬퍼 함수가 추가되었습니다.
  이 함수는 `config.conf`에서 불리언 값을 토글할 때 결과를 보고하는 데 사용할 수 있습니다.
* NVDA의 코딩 표준에서 함수 매개변수 목록을 두 탭으로 들여쓰기 해야 한다는 요구 사항이 제거되어, 최신 자동 린팅과 호환됩니다. (#17126, @XLTechie)
* [NVDA용 VS Code 워크스페이스 구성](https://nvaccess.org/nvaccess/vscode-nvda)이 Git 서브모듈로 추가되었습니다. (#17003)
* 새로운 함수 `gui.guiHelper.wxCallOnMain`이 추가되었습니다. 이 함수는 GUI 스레드가 아닌 곳에서 wx 함수를 안전하고 동기적으로 호출하고, 반환 값을 가져올 수 있도록 합니다. (#17304)
* 새로운 메시지 대화상자 API가 `gui.message`에 추가되었습니다. (#13007)
  * 추가된 클래스: `ReturnCode`, `EscapeCode`, `DialogType`, `Button`, `DefaultButton`, `DefaultButtonSet`, `MessageDialog`.
* `brailleTables` 모듈에 `getDefaultTableForCurrentLang` 함수가 추가되었습니다. (#17222, @nvdaes)
* NVDA 업데이트 메타데이터를 캡슐화하는 `updateCheck.UpdateInfo` 데이터 클래스가 추가되었습니다. (#17310, @christopherpross)
* 이제 다음의 경우 `labeledBy` 속성을 가져올 수 있습니다:
  * `labelled-by` IAccessible2 관계를 구현하는 응용프로그램의 객체. (#17436, @michaelweghorn)
  * 해당 `LabeledBy` UIA 속성을 지원하는 UIA 요소. (#17442, @michaelweghorn)
* `wx.ComboBox`와 `wx.StaticText` 레이블을 `gui.guiHelper.associateElements`를 사용하여 연결할 수 있는 기능이 추가되었습니다. (#17476)
* 다음 확장 포인트가 추가되었습니다. (#17428, @ctoth):
  * `inputCore.decide_handleRawKey`: 각 키 입력 시 호출됨
  * `speech.extensions.post_speechPaused`: 음성이 일시 중지되거나 다시 시작될 때 호출됨
* `bdDetect.DriverRegistrar`에서 점자 디스플레이 자동 감지 등록 변경 사항: (#17521, @LeonarddeR)
  * USB 장치를 하나씩 등록할 수 있는 `addUsbDevice` 메서드가 추가되었습니다.
  * `addUsbDevices`에 `matchFunc` 매개변수가 추가되었으며, 이는 `addUsbDevice`에서도 사용할 수 있습니다.
    * 이를 통해 VID/PID 조합이 여러 드라이버에 걸쳐 여러 장치에서 공유되거나, HID 장치가 여러 엔드포인트를 제공하는 경우와 같은 상황에서 장치 감지를 더 제한할 수 있습니다.
    * 자세한 내용은 메서드 문서와 albatross 및 brailliantB 드라이버의 예제를 참조하세요.
* 오디오 출력 장치를 열거하기 위한 새로운 함수 `utils.mmdevice.getOutputDevices`가 추가되었습니다. (#17678)
* `synthDriverHandler`에 새로운 확장 포인트 `pre_synthSpeak`가 추가되었으며, 이는 음성 관리자가 현재 음성 합성기의 `speak`를 호출하기 전에 호출됩니다. (#17648)
* NVDA는 `text-indent` IAccessible2 객체 속성을 지원합니다. (#13052, @michaelweghorn)
* `gesture.send`를 사용하는 스크립트가 `numLock`을 수정 키로 포함하는 제스처로 트리거될 때, Num Lock이 더 이상 꺼지지 않습니다. (#10827, @CyrilleB79)

#### #### API 호환성 변경사항

이 변경사항은 API 호환성을 깨뜨립니다.
새로운 API로 업데이트하는 데 문제가 있다면 GitHub 이슈를 열어주세요.

* `addonStore.network.BASE_URL` 상수가 제거되었습니다.
추가기능 스토어 기본 URL은 이제 NVDA 내에서 직접 구성할 수 있으므로 대체 항목은 계획되지 않았습니다. (#17099)
* `updateCheck.CHECK_URL` 상수가 제거되었습니다.
NVDA 업데이트 확인 URL은 이제 NVDA 내에서 직접 구성할 수 있으므로 대체 항목은 계획되지 않았습니다. (#17151)
* `NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA`가 공개 대체 항목 없이 제거되었습니다. (#14047, #16820, @codeofdusk)
* `NVDAObjects.IAccessible.ia2TextMozilla.FakeEmbeddingTextInfo`가 제거되었습니다. (#16768, @jcsteh)
* `appModules.soffice`의 다음 심볼이 이름이 변경되었습니다. (#6915, @michaelweghorn):
  * `SymphonyDocument.announceToolbarButtonToggle`이 `SymphonyDocument.announceFormattingGestureChange`로 변경되었습니다.
  * `SymphonyDocument.script_toggleTextAttribute`가 `SymphonyDocument.script_changeTextFormatting`으로 변경되었습니다.
* `brailleDisplayDrivers.seikantk.InputGesture`의 `space` 키워드 인자는 이제 `bool` 대신 `int`를 기대합니다. (#17047, @school510587)
* `[upgrade]` 구성 섹션과 `[upgrade][newLaptopKeyboardLayout]`이 제거되었습니다. (#17191)
* `updateCheck.checkForUpdate`는 이제 사전 대신 `UpdateInfo` 객체를 반환합니다. (#17310, @christopherpross)
* `updateCheck.UpdateResultDialog`와 `updateCheck.UpdateDownloader`의 생성자는 이제 메타데이터 사전 대신 `UpdateInfo` 객체를 받도록 업데이트되었습니다. (#17310, @christopherpross)
* NVDA의 winmm 지원이 중단됨에 따라 (#17496, #17532, #17678):
  * 다음 심볼이 `nvwave`에서 대체 항목 없이 제거되었습니다: `CALLBACK_EVENT`, `CALLBACK_FUNCTION`, `CALLBACK_NULL`, `HWAVEOUT`, `LPHWAVEOUT`, `LPWAVEFORMATEX`, `LPWAVEHDR`, `MAXPNAMELEN`, `MMSYSERR_NOERROR`, `usingWasapiWavePlayer`, `WAVEHDR`, `WAVEOUTCAPS`, `waveOutProc`, `WAVE_MAPPER`, `WHDR_DONE`, `WinmmWavePlayer`, 그리고 `winmm`.
  * 다음 심볼이 `nvwave`에서 제거되었습니다: `getOutputDeviceNames`, `outputDeviceIDToName`, `outputDeviceNameToID`.
  대신 `utils.mmdevice.getOutputDevices`를 사용하세요.
  * `nvwave.WasapiWavePlayer`가 `WavePlayer`로 이름이 변경되었습니다.
  또한, __init__ 메서드의 시그니처가 다음과 같이 변경되었습니다:
    * 이제 `outputDevice` 매개변수는 문자열로만 전달되어야 합니다.
    * 지원 종료 예정이었던 `closeWhenIdle`과 `buffered` 매개변수가 삭제되었습니다.
  * `gui.settingsDialogs.AdvancedPanelControls.wasapiComboBox`가 제거되었습니다.
  * 구성 사양의 `audio` 섹션에서 `WASAPI` 키가 제거되었습니다.
  * 구성 키 `config.conf["speech"]["outputDevice"]`가 제거되었습니다.
    이는 Windows 코어 오디오 엔드포인트 장치 ID를 저장하는 `config.conf["audio"]["outputDevice"]`로 대체되었습니다. (#17547)
* `NVDAObjects.window.scintilla.ScintillaTextInfo`에서 텍스트가 선택되지 않은 경우, `collapse` 메서드는 `end` 매개변수가 `True`로 설정되면 줄로 확장되도록 재정의됩니다. (#17431, @nvdaes)
* 다음 심볼이 대체 없이 제거되었습니다: `languageHandler.getLanguageCliArgs`, `__main__.quitGroup` 및 `__main__.installGroup`. (#17486, @CyrilleB79)
* 명령줄 플래그의 접두사 일치(예: `--disable-addons`를 사용하기 위해 `--di` 사용)는 더 이상 지원되지 않습니다. (#11644, @CyrilleB79)
* `bdDetect.DriverRegistrar`의 `useAsFallBack` 키워드 인자가 `useAsFallback`으로 이름이 변경되었습니다. (#17521, @LeonarddeR)
* `[addonStore][showWarning]` 구성 설정이 제거되었습니다.
대신 `addonStore.dataManager.addonDataManager.storeSettings.showWarning`을 사용하세요. (#17597)
* `ui.browseableMessage`는 이제 `sanitizeHtmlFunc` 매개변수를 받습니다.
이는 기본적으로 기본 인수와 함께 `nh3.clean`으로 설정됩니다.
즉, `isHtml=True`를 사용하여 `ui.browseableMessage`에 전달된 모든 HTML은 이제 기본적으로 정리됩니다.
태그나 속성을 허용 목록에 추가하는 등 정리 규칙을 변경하려면, 원하는 매개변수로 `nh3.clean`을 호출하는 함수를 생성하세요. (#16985)
* `updateCheck.UpdateAskInstallDialog`는 더 이상 업데이트 또는 연기 버튼이 눌렸을 때 자동으로 작업을 수행하지 않습니다.
대신, `callback` 속성이 추가되었으며, 대화상자의 반환 값을 사용하여 적절한 작업을 수행하는 함수를 반환합니다. (#17582)
* `gui.runScriptModalDialog`로 열리는 대화상자는 이제 NVDA에서 모달로 인식됩니다. (#17582)
* "자동으로 초점 이동 가능한 요소에 시스템 초점 설정" 설정과 관련된 다음 API 심볼이 대체 없이 제거되었습니다: (#17598)
  * `globalCommands.GlobalCommands.script_toggleAutoFocusFocusableElements`
  * `config.conf["virtualBuffers"]["autoFocusFocusableElements"]`
  * `gui.settingsDialogs.BrowseModePanel.autoFocusFocusableElementsCheckBox`
* 이제 SAPI5 음성은 `nvwave.WavePlayer`를 사용하여 오디오를 출력합니다: (#17592, @gexgd0419)
  * `synthDrivers.sapi5.SPAudioState`가 제거되었습니다.
  * `synthDrivers.sapi5.SynthDriver.ttsAudioStream`이 제거되었습니다.
* `autoSettingsUtils.driverSetting.DriverSetting`의 `id`가 밑줄(_)로 시작하는 인스턴스는 더 이상 NVDA 설정에 표시되지 않습니다. (#17599)
* 키보드 입력 에코 설정이 불리언에서 정수 값으로 변경되었습니다. (#17505, @Cary-rowen)
  * `config.conf["keyboard"]["speakTypedCharacters"]`와 `config.conf["keyboard"]["speakTypedWords"]`는 이제 정수 값을 사용합니다.
  * `config.configFlags`에 이러한 모드를 나타내는 `TypingEcho` 열거형이 추가되었습니다. 0=끔, 1=편집 컨트롤에서만, 2=항상.
  * `gui.settingsDialogs.KeyboardSettingsPanel.wordsCheckBox`와 `gui.settingsDialogs.KeyboardSettingsPanel.charsCheckBox`가 제거되었습니다.
* `winUser.paint`의 `painStruct`가 `paintStruct`로 이름이 변경되었으며, `PAINTSTRUCT`를 전달할 때 예외가 발생하던 버그가 수정되었습니다. (#17744)
* `documentationUtils.getDocFilePath`와 `installer.getDocFilePath`는 더 이상 로케일 문서 폴더에서 `.txt` 파일을 찾지 않습니다. (#17911, @CyrilleB79)
* `config.conf["documentFormatting"]["reportFontAttributes"]`가 제거되었습니다. 대신 `config.conf["documentFormatting"]["fontAttributeReporting"]`을 사용하세요. (#18066)
* config.conf["speech"]["includeCLDR"]가 제거되었습니다. 대신 config.conf["speech"]["symbolDictionaries"]에 "cldr"가 포함되어 있는지 확인하거나 수정하세요. (#18066)

#### #### 지원 종료 예정

* `braille.filter_displaySize` 확장 포인트는 지원 종료 예정입니다.
대신 `braille.filter_displayDimensions`를 사용하세요. (#17011)
* `gui.message.messageBox`와 `gui.runScriptModalDialog` 함수, 그리고 `gui.nvdaControls.MessageDialog` 클래스는 지원 종료 예정입니다.
대신 `gui.message.MessageDialog`를 사용하세요. (#17582)
* 다음 심볼들은 지원 종료 예정입니다 (#17486, @CyrilleB79):
  * `__main__`의 `NoConsoleOptionParser`, `stringToBool`, `stringToLang`; 대신 `argsParsing`의 동일한 심볼을 사용하세요.
  * `__main__.parser`; 대신 `argsParsing.getParser()`를 사용하세요.
* `bdDetect.DeviceType`은 지원 종료 예정이며, USB와 Bluetooth를 통해 HID와 Serial 통신이 모두 가능하다는 점을 고려하여 `bdDetect.ProtocolType`과 `bdDetect.CommunicationType`을 사용하세요. (#17537, @LeonarddeR)

## 2024.4.2

이 릴리즈는 점자 및 크롬 수식 읽기 관련 버그 수정 패치입니다.

### 버그 수정내역

* Chromium 브라우저(Chrome, Edge)의 수식 읽기 버그가 수정되었습니다. (#17421, @NSoiffer)
* 휴먼웨어 Brailliant BI 40X 디바이스 펌웨어 2.4 버전이 이제 정상 작동합니다. (#17518, @bramd)

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
* 구성요소 업데이트:
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

### 개발 변경사항

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* 구성요소 업데이트:
  * py2exe가 0.13.0.2로 업데이트되었습니다. (#16907, @dpy013)
  * setuptools가 72.0으로 업데이트되었습니다. (#16907, @dpy013)
  * Ruff가 0.5.6으로 업데이트되었습니다. (#16868, @LeonarddeR)
  * nh3이 0.2.18로 업데이트되었습니다. (#17020, @dpy013)
* NVDA의 저장소에 `.editorconfig` 파일이 추가되어 여러 IDE에서 기본 NVDA 코드 스타일 규칙을 자동으로 인식할 수 있습니다. (#16795, @LeonarddeR)
* 사용자 정의 음성 기호 사전을 지원합니다. (#16739, #16823, @LeonarddeR)
  * 사전은 추가 기능 패키지의 로케일별 폴더(e.g. `locale\en`)에 제공할 수 있습니다.
  * 사전 메타데이터는 추가 기능 매니페스트의 선택적 `symbolDictionaries` 섹션에 추가할 수 있습니다.
  * 자세한 내용은 [개발자 가이드의 사용자 정의 음성 기호 사전 섹션](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#AddonSymbolDictionaries)을 참조하십시오.
* 화면 좌표에서 가져온 객체를 리디렉션할 수 있는 `NVDAObject.objectFromPointRedirect` 메서드가 추가되었습니다. (#16788, @Emil-18)
* SCons를 `--all-cores` 매개변수와 함께 실행하면 사용 가능한 최대 CPU 코어 수를 자동으로 선택합니다. (#16943, #16868, @LeonarddeR)
* 개발자 정보에 내비게이터 객체의 응용 프로그램 아키텍처(예: AMD64)에 대한 정보가 포함됩니다. (#16488, @josephsl)

#### 지원 종료 예정

* `bool` 구성 키 `[documentFormatting][reportFontAttributes]`는 2025.1에서 제거될 예정입니다. 대신 `[fontAttributeReporting]`를 사용하십시오. (#16748)
  * 새로운 키는 `OutputMode` `enum`과 일치하는 `int` 값을 가지며, 음성, 점자, 음성과 점자, 비활성 옵션을 제공합니다.
  * API 소비자는 이전과 같이 `bool` 값을 사용할 수 있으며, 음성 또는 점자에 대해 특정 처리가 필요한 경우 `OutputMode`를 확인할 수 있습니다.
  * 이 키들은 2025.1까지 동기화 상태를 유지합니다.
* `NVDAObjects.UIA.InaccurateTextChangeEventEmittingEditableText`는 대체 없이 지원 종료 예정입니다. (#16817, @LeonarddeR)

## 2024.3.1

이 릴리즈는 자동 추가 기능 업데이트 알림과 관련된 버그를 수정하기 위한 패치 릴리즈입니다.

### 버그 수정내역

* 추가 기능 업데이트를 자동으로 확인할 때, NVDA가 연결 상태가 좋지 않은 경우 더 이상 멈추지 않습니다. (#17036)

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
* 특히 터미널 응용 프로그램에서 자동 텍스트 읽기 기능의 신뢰성이 향상되었습니다. (#15850, #16027, @Danstiv)
* 구성을 공장 기본값으로 안정적으로 재설정하는 것이 다시 한 번 가능합니다. (#16755, @Emil-18)
* Microsoft Excel에서 셀의 텍스트를 편집할 때 NVDA가 선택 변경 사항을 정확하게 발표합니다. (#15843)
* Java Access Bridge를 사용하는 응용 프로그램에서 NVDA는 이제 이전 줄을 반복하지 않고 마지막 빈 줄을 정확하게 읽습니다. (#9376, @dmitrii-drobotov)
* LibreOffice Writer(버전 24.8 이상)에서 텍스트 서식을 전환할 때(굵게, 이탤릭체, 밑줄, 아래첨자/위첨자, 정렬) 해당 키보드 단축키를 사용하면 NVDA가 새로운 서식 속성을 발표합니다(예: "굵게 켜짐", "굵게 꺼짐"). (#4248, @michaelweghorn)
* UI Automation을 사용하는 응용 프로그램의 텍스트 상자에서 커서 키로 탐색할 때 NVDA가 더 이상 잘못된 문자, 단어 등을 보고하지 않습니다. (#16711, @jcsteh)
* Windows 10/11 계산기에 붙여넣을 때 NVDA가 붙여넣은 전체 숫자를 정확하게 보고합니다. (#16573, @TristanBurchett)
* 원격 데스크탑 세션에서 연결을 끊고 다시 연결한 후 음성이 더 이상 침묵하지 않습니다. (#16722, @jcsteh)
* Visual Studio Code에서 개체 이름에 대한 텍스트 검토 명령에 대한 지원이 추가되었습니다. (#16248, @Cary-Rowen)
* 모노 오디오 장치에서 NVDA 소리 재생이 더 이상 실패하지 않습니다. (#16770, @jcsteh)
* outlook.com / 모던 아웃룩에서 To/CC/BCC 필드를 화살표 키로 탐색할 때 NVDA가 주소를 보고합니다. (#16856)
* NVDA가 추가 기능 설치 실패를 더 원활하게 처리합니다. (#16704)

### 개발 변경사항

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

* Adobe Reader에서 수학 속성이 잘못 읽히던 문제를 수정했습니다. 이로 인해 음성 출력이나 점자 출력이 부정확하거나 잘못되던 문제가 있었습니다. (#17980)
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

### 개발 변경사항

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* 10.0.22000 이상의 Windows 버전(예: 10.0.25398)에서 `winVersion.WinVersion` 객체를 생성할 때, 릴리스 이름으로 "Windows 10 unknown" 대신 "Windows 11 unknown"을 반환합니다. (#15992, @josephsl)
* AppVeyor 빌드 스크립트에서 NV Access 특정 부분을 비활성화하거나 수정할 수 있도록 appveyor.yml에 구성 가능한 변수를 추가하여 NVDA 포크의 AppVeyor 빌드 프로세스를 더 쉽게 만듭니다. (#16216, @XLTechie)
* NVDA 포크를 AppVeyor에서 빌드하는 과정을 설명하는 방법 문서를 추가했습니다. (#16293, @XLTechie)

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
* 구성요소 업데이트:
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
* NVDA는 WDAG(Windows Defender Application Guard) 내에서 실행되는 응용 프로그램의 초점을 다시 추적할 수 있습니다. (#15164)
* 마우스를 음성 출력 뷰어에서 움직일 때 음성 텍스트가 더 이상 업데이트되지 않습니다. (#15952, @hwf1324)
* NVDA가 Firefox나 Chrome에서 `escape` 또는 `alt+upArrow`로 콤보박스를 닫을 때 다시 탐색 모드로 전환합니다. (#15653)
* iTunes의 콤보 상자에서 위아래로 화살표 키를 누르면 더 이상 탐색 모드로 전환되지 않습니다. (#15653)

### 개발 변경사항

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* 참고: 이 릴리스는 추가 기능 API 호환성을 깨뜨리는 변경사항이 포함되어 있습니다.
추가 기능은 다시 테스트하고 매니페스트를 업데이트해야 합니다.
* 이제 NVDA를 빌드하려면 Visual Studio 2022가 필요합니다.
자세한 Visual Studio 구성 요소 목록은 [NVDA 문서](https://github.com/nvaccess/nvda/blob/release-2024.1/projectDocs/dev/createDevEnvironment.md)를 참조하세요. (#14313)
* 다음 확장 포인트가 추가되었습니다:
  * `treeInterceptorHandler.post_browseModeStateChange`. (#14969, @nvdaes)
  * `speech.speechCanceled`. (#15700, @LeonarddeR)
  * `_onErrorSoundRequested` (호출 시 `logHandler.getOnErrorSoundRequested()`를 사용하여 가져와야 함) (#15691, @CyrilleB79)
* 이제 추가 기능의 번역에서 복수형 형태를 사용할 수 있습니다. (#15661, @beqabeqa473)
* 외부 라이브러리가 [안정 ABI](https://docs.python.org/3.11/c-api/stable.html)를 사용하는 경우를 위해 추가 기능에서 사용할 수 있도록 바이너리 배포에 python3.dll이 포함되었습니다. (#15674, @mzanm)
* `BrailleDisplayDriver` 기본 클래스에 다중 줄 점자 디스플레이 정보를 제공하기 위한 `numRows` 및 `numCols` 속성이 추가되었습니다.
단일 줄 점자 디스플레이의 경우 여전히 `numCells` 설정이 지원되며, 다중 줄 점자 디스플레이의 경우 `numCells`는 전체 셀 수를 반환합니다. (#15386)
* BRLTTY용 BrlAPI가 버전 0.8.5로 업데이트되었으며, 해당 Python 모듈도 Python 3.11과 호환되는 빌드로 업데이트되었습니다. (#15652, @LeonarddeR)
* [SSML](https://www.w3.org/TR/speech-synthesis11/)을 사용하여 NVDA 음성 시퀀스를 작성할 수 있는 `speech.speakSsml` 함수가 추가되었습니다. (#15699, @LeonarddeR)
  * 현재 지원되는 태그는 다음과 같으며, 적절한 NVDA 음성 명령으로 변환됩니다:
    * `Prosody` (`pitch`, `rate`, `volume`). 곱셈(e.g. `200%`)만 지원됩니다.
    * `say-as`의 `interpret` 속성이 `characters`로 설정된 경우
    * `voice`의 `xml:lang` 속성이 XML 언어로 설정된 경우
    * `break`의 `time` 속성이 밀리초 값(e.g. `200ms`)으로 설정된 경우
    * `mark`의 `name` 속성이 마크 이름(e.g. `mark1`)으로 설정된 경우, 콜백 제공 필요
  * 예제: `speech.speakSsml('<speak><prosody pitch="200%">hello</prosody><break time="500ms" /><prosody rate="50%">John</prosody></speak>')`
  * SSML 구문 분석 기능은 `speechXml` 모듈의 `SsmlParser` 클래스를 기반으로 합니다.
* NVDA 컨트롤러 클라이언트 라이브러리 변경사항:
  * 라이브러리 파일 이름에서 아키텍처를 나타내는 접미사가 제거되었습니다. 즉, `nvdaControllerClient32/64.dll`은 이제 `nvdaControllerClient.dll`로 이름이 변경되었습니다. (#15718, #15717, @LeonarddeR)
  * Rust에서 nvdaControllerClient.dll을 사용하는 예제가 추가되었습니다. (#15771, @LeonarddeR)
  * 컨트롤러 클라이언트에 다음 함수가 추가되었습니다: (#15734, #11028, #5638, @LeonarddeR)
    * `nvdaController_getProcessId`: 컨트롤러 클라이언트가 사용하는 NVDA 인스턴스의 프로세스 ID(PID)를 가져옵니다.
    * `nvdaController_speakSsml`: 주어진 SSML에 따라 NVDA가 음성을 출력하도록 지시합니다. 이 함수는 다음을 지원합니다:
      * 기호 수준 제공.
      * 출력될 음성의 우선순위 제공.
      * 동기(차단) 및 비동기(즉시 반환) 모드에서 음성 출력.
    * `nvdaController_setOnSsmlMarkReachedCallback`: `nvdaController_speakSsml`에 제공된 SSML 시퀀스에서 `<mark />` 태그를 만날 때마다 동기 모드에서 호출되는 `onSsmlMarkReachedFuncType` 유형의 콜백을 등록합니다.
  * 참고: 컨트롤러 클라이언트의 새 함수는 NVDA 2024.1 이상에서만 지원됩니다.
* `include` 종속성이 업데이트되었습니다:
  * detours: `4b8c659f549b0ab21cf649377c7a84eb708f5e68`. (#15695)
  * ia2: `3d8c7f0b833453f761ded6b12d8be431507bfe0b`. (#15695)
  * sonic: `8694c596378c24e340c09ff2cd47c065494233f1`. (#15695)
  * w3c-aria-practices: `9a5e55ccbeb0f1bf92b6127c9865da8426d1c864`. (#15695)
  * wil: `5e9be7b2d2fe3834a7107f430f7d4c0631f69833`. (#15695)
* `hwPortUtils.listUsbDevices`에서 반환되는 장치 정보에 USB 장치의 버스 보고 설명(`busReportedDeviceDescription` 키)이 포함됩니다. (#15764, @LeonarddeR)
* USB 직렬 장치의 경우, `bdDetect.getConnectedUsbDevicesForDriver` 및 `bdDetect.getDriversForConnectedUsbDevices`는 이제 `busReportedDeviceDescription`과 같은 USB 장치에 대한 데이터로 풍부해진 `deviceInfo` 사전을 포함하는 장치 매치를 반환합니다. (#15764, @LeonarddeR)
* 구성 파일 `nvda.ini`가 손상된 경우, 재초기화 전에 백업 사본이 저장됩니다. (#15779, @CyrilleB79)
* 스크립트를 스크립트 데코레이터로 정의할 때, `speakOnDemand` 부울 인수를 지정하여 스크립트가 "요청 시" 음성 모드에서 음성을 출력할지 여부를 제어할 수 있습니다. (#481, @CyrilleB79)
  * 정보를 제공하는 스크립트(e.g. 창 제목 알림, 시간/날짜 알림)는 "요청 시" 모드에서 음성을 출력해야 합니다.
  * 작업을 수행하는 스크립트(e.g. 커서 이동, 매개변수 변경)는 "요청 시" 모드에서 음성을 출력하지 않아야 합니다.
* `scons -c` 중 git으로 추적된 파일을 삭제하면 다시 빌드 시 UIA COM 인터페이스가 누락되는 버그를 수정했습니다. (#7070, #10833, @hwf1324)
* 일부 코드 변경 사항이 `dist` 빌드 시 감지되지 않아 새 빌드가 트리거되지 않는 버그를 수정했습니다.
이제 `dist`는 항상 새로 빌드됩니다. (#13372, @hwf1324)
* 기본 유형이 표준인 `gui.nvdaControls.MessageDialog`가 더 이상 사운드가 할당되지 않아 발생하는 None 변환 예외를 발생시키지 않습니다. (#16223, @XLTechie)

#### API 호환성 변경사항

이 변경사항은 API 호환성을 깨뜨립니다.
새로운 API로 업데이트하는 데 문제가 있다면 GitHub 이슈를 열어주세요.

* NVDA는 이제 Python 3.11로 빌드됩니다. (#12064)
* pip 종속성이 업데이트되었습니다:
  * configobj가 5.1.0dev 커밋 `e2ba4457c4651fa54f8d59d8dcdd3da950e956b8`로 업데이트되었습니다. (#15544)
  * Comtypes가 1.2.0으로 업데이트되었습니다. (#15513, @codeofdusk)
  * Flake8이 4.0.1로 업데이트되었습니다. (#15636, @lukaszgo1)
  * py2exe가 0.13.0.1dev 커밋 `4e7b2b2c60face592e67cb1bc935172a20fa371d`로 업데이트되었습니다. (#15544)
  * robotframework가 6.1.1로 업데이트되었습니다. (#15544)
  * SCons가 4.5.2로 업데이트되었습니다. (#15529, @LeonarddeR)
  * sphinx가 7.2.6으로 업데이트되었습니다. (#15544)
  * wxPython이 4.2.2a 커밋 `0205c7c1b9022a5de3e3543f9304cfe53a32b488`로 업데이트되었습니다. (#12551, #16257)
* pip 종속성이 제거되었습니다:
  * typing_extensions는 이제 Python 3.11에서 기본적으로 지원됩니다. (#15544)
  * nose는 더 이상 사용되지 않으며, 대신 unittest-xml-reporting이 XML 리포트를 생성하는 데 사용됩니다. (#15544)
* `IAccessibleHandler.SecureDesktopNVDAObject`가 제거되었습니다.
대신 NVDA가 사용자 프로필에서 실행 중일 때, 확장 포인트 `winAPI.secureDesktop.post_secureDesktopStateChange`를 사용하여 보안 데스크탑의 존재를 추적하세요. (#14488)
* `braille.BrailleHandler.handlePendingCaretUpdate`가 제거되었으며, 대체할 공개 메서드는 없습니다. (#15163, @LeonarddeR)
* `bdDetect.addUsbDevices`와 `bdDetect.addBluetoothDevices`가 제거되었습니다.
점자 디스플레이 드라이버는 대신 `registerAutomaticDetection` 클래스 메서드를 구현해야 합니다.
이 메서드는 `addUsbDevices`와 `addBluetoothDevices` 메서드를 사용할 수 있는 `DriverRegistrar` 객체를 받습니다. (#15200, @LeonarddeR)
* `BrailleDisplayDriver`의 기본 `check` 메서드는 이제 `threadSafe`와 `supportsAutomaticDetection` 속성이 모두 `True`로 설정되어야 합니다. (#15200, @LeonarddeR)
* `hwIo.ioThread.IoThread.queueAsApc`에 람다 함수를 전달하는 것이 더 이상 불가능합니다. 함수는 약한 참조가 가능해야 합니다. (#14627, @LeonarddeR)
* `IoThread.autoDeleteApcReference`가 제거되었습니다. (#14924, @LeonarddeR)
* 대문자 음높이 변경을 지원하려면, 음성 합성기는 이제 `supportedCommands` 속성에서 `PitchCommand`에 대한 지원을 명시적으로 선언해야 합니다. (#15433, @LeonarddeR)
* `speechDictHandler.speechDictVars`가 제거되었습니다. `speechDictHandler.speechDictVars.speechDictsPath` 대신 `NVDAState.WritePaths.speechDictsDir`를 사용하세요. (#15614, @lukaszgo1)
* `languageHandler.makeNpgettext`와 `languageHandler.makePgettext`가 제거되었습니다.
이제 `npgettext`와 `pgettext`가 기본적으로 지원됩니다. (#15546)
* [Poedit](https://poedit.net)를 위한 앱 모듈이 크게 변경되었습니다. `fetchObject` 함수가 제거되었습니다. (#15313, #7303, @LeonarddeR)
* `hwPortUtils`에서 다음과 같은 중복 타입과 상수가 제거되었습니다: (#15764, @LeonarddeR)
  * `PCWSTR`
  * `HWND` (대체: `ctypes.wintypes.HWND`)
  * `ULONG_PTR`
  * `ULONGLONG`
  * `NULL`
  * `GUID` (대체: `comtypes.GUID`)
* `gui.addonGui.AddonsDialog`가 제거되었습니다. (#15834)
* `touchHandler.TouchInputGesture.multiFingerActionLabel`이 제거되었으며, 대체할 항목은 없습니다. (#15864, @CyrilleB79)
* `NVDAObjects.IAccessible.winword.WordDocument.script_reportCurrentHeaders`가 제거되었으며, 대체할 항목은 없습니다. (#15904, @CyrilleB79)
* 다음 앱 모듈이 제거되었습니다.
코드에서 이를 가져오는 경우, 대체 모듈을 대신 가져와야 합니다. (#15618, @lukaszgo1)

| | 제거된 모듈 이름 | 대체 모듈 ||
|---|---|
||`azardi-2.0` |`azardi20`||
||`azuredatastudio` |`code`||
||`azuredatastudio-insiders` |`code`||
||`calculatorapp` |`calculator`||
||`codeinsiders` |`code`||
||`commsapps` |`hxmail`||
||`dbeaver` |`eclipse`||
||`digitaleditionspreview` |`digitaleditions`||
||`esybraille` |`esysuite`||
||`hxoutlook` |`hxmail`||
||`miranda64` |`miranda32`||
||`mpc-hc` |`mplayerc`||
||`mpc-hc64` |`mplayerc`||
||`notepad++` |`notepadPlusPlus`||
||`searchapp` |`searchui`||
||`searchhost` |`searchui`||
||`springtoolsuite4` |`eclipse`||
||`sts` |`eclipse`||
||`teamtalk3` |`teamtalk4classic`||
||`textinputhost` |`windowsinternal_composableshell_experiences_textinput_inputapp`||
||`totalcmd64` |`totalcmd`||
||`win32calc` |`calc`||
||`winmail` |`msimn`||
||`zend-eclipse-php` |`eclipse`||
||`zendstudio` |`eclipse`||

#### 지원 종료 예정

* `watchdog.getFormattedStacksForAllThreads` 사용은 지원 종료 예정입니다대신 `logHandler.getFormattedStacksForAllThreads`를 사용하세요. (#15616, @lukaszgo1)
* `easeOfAccess.canConfigTerminateOnDesktopSwitch`는 지원 종료 예정입니다. Windows 7 지원이 중단되면서 더 이상 필요하지 않게 되었습니다. (#15644, @LeonarddeR)
* `winVersion.isFullScreenMagnificationAvailable`는 지원 종료 예정입니다대신 `visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart`를 사용하세요. (#15664, @josephsl)
* 다음 Windows 릴리스 상수는 winVersion 모듈에서 지원 종료 예정입니다. (#15647, @josephsl):
  * `winVersion.WIN7`
  * `winVersion.WIN7_SP1`
  * `winVersion.WIN8`
* `bdDetect.KEY_*` 상수는 지원 종료 예정입니다.
대신 `bdDetect.DeviceType.*`를 사용하세요. (#15772, @LeonarddeR)
* `bdDetect.DETECT_USB`와 `bdDetect.DETECT_BLUETOOTH` 상수는 지원 종료 예정이며, 공개 대체 항목은 없습니다. (#15772, @LeonarddeR)
* `gui.ExecAndPump` 사용은 지원 종료 예정입니다대신 `systemUtils.ExecAndPump`를 사용하세요. (#15852, @lukaszgo1)

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
    * NVDA를 업데이트할 때 이러한 추가 기능의 호환되지 않는 버전이 사용되지 않도록 설정됩니다:
    * Tony's Enhancements 1.15 이하 버전 (#15402)
* NVDA global commands extension 12.0.8 이하 버전 (#15443)
  * NVDA는 이제 광학 문자 인식(OCR) 기능 사용 시 지속적으로 결과를 업데이트하는 것이 가능합니다. 새로운 텍스트가 나타나면 말합니다. (#2797)
  * 이 기능을 활성화하려면, NVDA 설정 대화상자의 Windows OCR 카테고리에서 "인식된 콘텐츠를 주기적으로 새로고침"을 활성화하세요.
* 한번 활성화하면 `NVDA+5` 키(자동 변경 알림)를 눌러 전환하여 새로운 텍스트를 읽을 것인지 말 것인지 선택할 수 있습니다.
* 점자 디스플레이 자동 탐색을 사용할 때, 점자 디스플레이 선택 대화상자에서 특정 점자 디스플레이 장치를 탐색에서 제외할 수 있습니다.  (#15196)
* 문서 서식 알림 설정에 새 옵션인 "들여쓰기 빈줄 무시"이 추가되었습니다. (#13394)

### 변경사항

* 점자:
  * 점자:
  캐럿 업데이트를 동반하지 않고 텍스트가 변경되었을 때, 점자 디스플레이의 텍스트는 이제 변경된 줄에 위치할 때 적절하게 업데이트됩니다.
  * 여기에는 검토하기 위해 점자를 묶는 경우가 포함됩니다. (#15115)
    * 추가적인 BRLTTY 키 바인딩이 NVDA 명령에 매핑됨 (#6483):
    * `learn`: NVDA 입력도움말 토글
    * `prefmenu`: NVDA 메뉴 열기
    * `prefload`/`prefsave`: NVDA 환경 불러오기/저장하기
    * `time`: 시간 표시
    * `say_line`: 리뷰 커서의 현재 위치 줄 읽기
  * `say_below`: 리뷰커서로 모두 읽기
  * BRLTTY 드라이버는 오직 BrlAPI가 활성화BRLTTY 인스턴스 is running. (#15335)
  HID 점자 지원을 가능하게 하는 고급 설정은 새로운 옵션을 선호하여 삭제되었습니다. 이제 점자 표시 선택 대화상자에서 점자 표시 자동 감지를 위해 특정 드라이버를 비활성화할 수 있습니다. (#15196)
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

### 개발 변경사항

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* `braille.handler.handleUpdate`와 `braille.handler.handleReviewMove`가 즉시 업데이트되지 않도록 변경되었습니다.
이전에는 이 메서드들이 자주 호출될 경우 많은 리소스를 소모했습니다.
이제 이러한 메서드는 각 코어 사이클의 끝에서 업데이트를 큐에 추가합니다.
또한, 이 메서드들은 스레드 안전성을 가지며, 백그라운드 스레드에서 호출할 수 있습니다. (#15163)
* 자동 점자 디스플레이 탐지 프로세스에서 사용자 정의 점자 디스플레이 드라이버를 등록하는 공식 지원이 추가되었습니다.
자세한 내용은 `braille.BrailleDisplayDriver` 클래스 문서를 참조하십시오.
특히, `supportsAutomaticDetection` 속성을 `True`로 설정하고 `registerAutomaticDetection` 클래스 메서드를 구현해야 합니다. (#15196)

#### 지원 종료 예정

* `braille.BrailleHandler.handlePendingCaretUpdate`는 이제 지원 종료 예정이며, 대체할 공개 메서드는 없습니다.
이 메서드는 2024.1에서 제거될 예정입니다. (#15163)
* `NVDAObjects.window.excel`에서 `xlCenter`, `xlJustify`, `xlLeft`, `xlRight`, `xlDistributed`, `xlBottom`, `xlTop` 상수를 가져오는 것은 지원 종료 예정입니다.
대신 `XlHAlign` 또는 `XlVAlign` 열거형을 사용하십시오. (#15205)
* `NVDAObjects.window.excel.alignmentLabels` 매핑은 지원 종료 예정입니다.
대신 `XlHAlign` 또는 `XlVAlign` 열거형의 `displayString` 메서드를 사용하십시오. (#15205)
* `bdDetect.addUsbDevices`와 `bdDetect.addBluetoothDevices`는 지원 종료 예정입니다.
점자 디스플레이 드라이버는 대신 `registerAutomaticDetection` 클래스 메서드를 구현해야 합니다.
이 메서드는 `addUsbDevices`와 `addBluetoothDevices` 메서드를 사용할 수 있는 `DriverRegistrar` 객체를 받습니다. (#15200)
* `BrailleDisplayDriver`의 기본 `check` 메서드는 스레드 안전으로 표시된 장치에 대해 `bdDetect.driverHasPossibleDevices`를 사용합니다.
NVDA 2024.1부터 기본 메서드가 `bdDetect.driverHasPossibleDevices`를 사용하려면 `supportsAutomaticDetection` 속성도 `True`로 설정해야 합니다. (#15200)

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

* 구성요소 업데이트:
  * eSpeak NG가 1.52-dev commit `ed9a7bcf`으로 업데이트되었습니다. (#15036)
  * LibLouis 점역기가 [3.25.0](https://github.com/liblouis/liblouis/releases/tag/v3.25.0) 버전으로 업데이트되었습니다. (#14719)
  * 유니코드 CLDR이 43.0로 업데이트되었습니다. (#14918)
* 리브레Office 변경사항:
  * 이제 LibreOffice 버전용 LibreOffice Writer 7.6 버전 이하에서 리뷰 커서 위치를 보고할 때 현재 커서/캐럿 위치가 현재 페이지에 맞게 상대적으로 보고됩니다. 이는 Microsoft Word에 대해 적용된 것과 유사합니다. (#11696)
  * LibreOffice에서 상태 표시줄(예: "NVDA+end")의 알림이 작동합니다. (#11698)
  * LibreOffice Calc에서 다른 셀로 이동할 때 NVDA의 설정에서 셀 좌표 알림이 비활성화된 경우 NVDA는 더 이상 이전에 포커싱된 셀의 좌표를 알리지 않습니다. (#15098)
* 점자 변경사항:
  * 표준 HID 점자 드라이버로 점자 디스플레이를 사용할 때 dpad를 사용하여 화살표 키를 에뮬레이트하고 입력할 수 있습니다. 또한 스페이스+1점과 스페이스+4점이 이제 각각 위쪽 및 아래쪽 화살표에 매핑합니다. (#14713)
  동적 웹 콘텐츠 업데이트(ARIA 라이브 리전)가 이제 점자 디스플레이에 표시됩니다.
  * 고급 설정 패널에서 이 기능을 비활성화할 수 있습니다. (#7756)
  대시 및 앰 대시 기호가 항상 음성합성기로 전송됩니다. (#13830)
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
  그러나 이 수정 사항은 브라우즈 모드 설정에서 자동으로 포커스를 포커스 가능한 요소로 설정" 옵션이 해제된 경우에만 적용됩니다(기본값).
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
* 대신에 그 링크에 목적 사이트 주소가 없음을 알립니다. (#14723)
* NVDA는 이전에 완전히 중지된 응용 프로그램과 같은 더 많은 상황에서 다시 복구됩니다. (#14759)
* 특정 터미널 및 콘솔에서 UIA 지원을 강제로 실행할 때 프리징 및 로그 파일 스팸을 유발하는 버그가 수정됩니다. (#14689)
* 구성 재설정 후 NVDA가 더 이상 구성 저장을 거부하지 않습니다. (#13187)
* 런처에서 임시 버전을 실행할 때 NVDA는 사용자가 구성을 저장할 수 있다고 잘못 인식하지 않습니다. (#14914)
* 객체 알림 단축키가 개선되었습니다. (#10807)
* NVDA는 이제 일반적으로 명령과 초점 변경에 약간 더 빠르게 반응합니다. (#14928)
* 일부 시스템에서 OCR 설정을 표시하는 데 실패하지 않을 것입니다. (#15017)
* Synthesizer Swticher를 포함한 NVDA 구성을 저장하거나 불러올 때 버그를 수정합니다. (#14760)
* "위로 쓸기" 터치 제스처가 발생시키는 버그를 수정하여 이전 줄로 이동하는 대신 페이지를 이동합니다. (#15127)

### 개발 변경사항

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* 추가기능 매니페스트 사양에 권장 규칙이 추가되었습니다.
이 규칙들은 NVDA 호환성에는 선택 사항이지만, 추가기능 스토어에 제출하기 위해 권장되거나 필수입니다. (#14754)
  * `name` 필드에는 `lowerCamelCase`를 사용하십시오.
  * `version` 필드에는 `<major>.<minor>.<patch>` 형식을 사용하십시오 (추가기능 데이터스토어에 필수).
  * `url` 필드에는 `https://` 스키마를 사용하십시오 (추가기능 데이터스토어에 필수).
* 등록된 핸들러가 반환하는 반복 가능한 항목을 순회(iterate)할 수 있는 `Chain`이라는 새로운 확장 포인트 유형이 추가되었습니다. (#14531)
* `bdDetect.scanForDevices` 확장 포인트가 추가되었습니다.
핸들러는 USB나 블루투스 같은 기존 카테고리에 맞지 않는 `BrailleDisplayDriver/DeviceMatch` 쌍을 생성할 수 있습니다. (#14531)
* 확장 포인트 `synthDriverHandler.synthChanged`가 추가되었습니다. (#14618)
* NVDA 음성 설정 링이 이제 음성 합성기를 로드할 때가 아니라, 처음으로 설정 값이 필요할 때 사용 가능한 설정 값을 캐시합니다. (#14704)
* 이제 제스처 맵의 export 메서드를 호출하여 이를 사전(dictionary)으로 내보낼 수 있습니다.
이 사전은 `GlobalGestureMap`의 생성자에 전달하거나 기존 맵의 update 메서드에 전달하여 다른 제스처에서 가져올 수 있습니다. (#14582)
* `hwIo.base.IoBase`와 그 파생 클래스들은 이제 `hwIo.ioThread.IoThread`를 받을 수 있는 새로운 생성자 매개변수를 가집니다.
제공되지 않으면 기본 스레드가 사용됩니다. (#14627)
* `hwIo.ioThread.IoThread`는 이제 Python 함수를 사용하여 대기 가능한 타이머를 설정하는 `setWaitableTimer` 메서드를 제공합니다.
마찬가지로, 새로운 `getCompletionRoutine` 메서드는 Python 메서드를 안전하게 완료 루틴으로 변환할 수 있게 합니다. (#14627)
* `offsets.OffsetsTextInfo._get_boundingRects`는 이제 항상 `textInfos.TextInfo`의 서브클래스에 기대되는 대로 `List[locationHelper.rectLTWH]`를 반환해야 합니다. (#12424)
* `highlight-color`가 이제 형식 필드 속성으로 추가되었습니다. (#14610)
* NVDA는 이제 로그 메시지가 NVDA 코어에서 오는 것인지 더 정확히 판단해야 합니다. (#14812)
* NVDA는 더 이상 지원 종료 예정인 appModules에 대해 부정확한 경고나 오류를 로그하지 않습니다. (#14806)
* 모든 NVDA 확장 포인트가 이제 개발자 가이드의 새로운 전용 챕터에서 간략히 설명됩니다. (#14648)
* `scons checkpot`은 더 이상 `userConfig` 하위 폴더를 확인하지 않습니다. (#14820)
* 번역 가능한 문자열은 이제 `ngettext`와 `npgettext`를 사용하여 단수형과 복수형으로 정의할 수 있습니다. (#12445)

#### 지원 종료 예정

* `hwIo.ioThread.IoThread.queueAsApc`에 람다 함수를 전달하는 것은 지원 종료 예정입니다.
대신, 함수는 약한 참조가 가능해야 합니다. (#14627)
* `hwIo.base`에서 `LPOVERLAPPED_COMPLETION_ROUTINE`을 가져오는 것은 지원 종료 예정입니다.
대신, `hwIo.ioThread`에서 가져오십시오. (#14627)
* `IoThread.autoDeleteApcReference`는 지원 종료 예정입니다.
이 기능은 NVDA 2023.1에서 도입되었으나, 공개 API의 일부로 설계된 것이 아니었습니다.
제거될 때까지, 이 기능은 아무 작업도 수행하지 않는 컨텍스트 관리자로 동작합니다. (#14924)
* `gui.MainFrame.onAddonsManagerCommand`는 지원 종료 예정입니다. 대신 `gui.MainFrame.onAddonStoreCommand`를 사용하십시오. (#13985)
* `speechDictHandler.speechDictVars.speechDictsPath`는 지원 종료 예정입니다. 대신 `NVDAState.WritePaths.speechDictsDir`를 사용하십시오. (#15021)
* `speechDictHandler.dictFormatUpgrade`에서 `voiceDictsPath`와 `voiceDictsBackupPath`를 가져오는 것은 지원 종료 예정입니다.
대신, `NVDAState`의 `WritePaths.voiceDictsDir`와 `WritePaths.voiceDictsBackupDir`를 사용하십시오. (#15048)
* `config.CONFIG_IN_LOCAL_APPDATA_SUBKEY`는 지원 종료 예정입니다.
대신, `config.RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY`를 사용하십시오. (#15049)

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
  * 이는 현재 UIA에서 지원하지 않는 스크린리더를 통해 이름이 정의된 범위의 헤더를 얘기하는 것이 아닙니다.
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

### 개발 변경사항

참고: 이것은 추가 기능 API 호환성이 께지는 릴리즈입니다.
추가기능은 재테스트를 거쳐 매니페스트를 업데이트해야 합니다.
NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* 시스템 테스트가 이제 비영어권 시스템에서도 로컬에서 실행될 때 통과해야 합니다. (#13362)
* 시스템 테스트가 이제 비영어권 시스템에서 로컬로 실행될 때 통과합니다. (#13362)
* Windows 11 ARM 환경에서 x64 응용 프로그램이 더 이상 ARM64 응용 프로그램으로 식별되지 않습니다. (#14403)
새로운 UI 자동화 시나리오에서 `SearchField`와 `SuggestionListItem` `UIA` `NVDAObjects`를 사용하는 것이 더 이상 필요하지 않습니다. 이제 검색 제안 자동 알림과 `controllerFor` 패턴을 통해 UI 자동화로 노출된 입력 기능은 각각 `behaviours.EditableText`와 기본 `NVDAObject`를 통해 일반적으로 사용할 수 있습니다. (#14222)
* UIA 디버그 로깅 카테고리가 활성화되었을 때, 이제 UIA 이벤트 핸들러와 유틸리티에 대해 훨씬 더 많은 로깅을 생성합니다. (#14256)
* NVDAHelper 빌드 표준이 업데이트되었습니다. (#13072)
  * 이제 C++20 표준을 사용하며, 이전에는 C++17을 사용했습니다.
  * 이제 `/permissive-` 컴파일러 플래그를 사용하여 허용적 동작을 비활성화하고, 엄격한 준수를 위한 `/Zc` 컴파일러 옵션을 설정합니다.
* 일부 플러그인 객체(예: 드라이버 및 추가기능)가 이제 NVDA 파이썬 콘솔에서 더 유익한 설명을 제공합니다. (#14463)
* NVDA는 이제 Visual Studio 2022로 완전히 컴파일할 수 있으며, 더 이상 Visual Studio 2019 빌드 도구가 필요하지 않습니다. (#14326)
* NVDA 멈춤 현상을 디버깅하기 위한 더 자세한 로깅이 추가되었습니다. (#14309)
* 싱글톤 `braille._BgThread` 클래스가 `hwIo.ioThread.IoThread`로 대체되었습니다. (#14130)
  * 이 클래스의 단일 인스턴스 `hwIo.bgThread`(NVDA 코어 내)는 스레드 안전한 점자 디스플레이 드라이버를 위한 백그라운드 I/O를 제공합니다.
  * 이 새로운 클래스는 설계상 싱글톤이 아니며, 추가기능 개발자는 하드웨어 I/O를 수행할 때 자신의 인스턴스를 사용하는 것이 권장됩니다.
* 컴퓨터의 프로세서 아키텍처를 `winVersion.WinVersion.processorArchitecture` 속성을 통해 조회할 수 있습니다. (#14439)
* 새로운 확장 포인트가 추가되었습니다. (#14503)
  * `inputCore.decide_executeGesture`
  * `tones.decide_beep`
  * `nvwave.decide_playWaveFile`
  * `braille.pre_writeCells`
  * `braille.filter_displaySize`
  * `braille.decide_enabled`
  * `braille.displayChanged`
  * `braille.displaySizeChanged`
* 음성 합성기 드라이버에서 지원되는 설정에 대해 `useConfig`를 False로 설정할 수 있습니다. (#14601)

#### API 호환성 변경사항

이 변경사항은 API 호환성을 깨뜨립니다.
새로운 API로 업데이트하는 데 문제가 있다면 GitHub 이슈를 열어주세요.

* 설정 사양이 변경되었으며, 키가 제거되거나 수정되었습니다:
  * `[documentFormatting]` 섹션에서 (#14233):
    * `reportLineIndentation`은 이제 boolean 대신 int 값(0에서 3)을 저장합니다.
    * `reportLineIndentationWithTones`가 제거되었습니다.
    * `reportBorderStyle`과 `reportBorderColor`가 제거되었으며, `reportCellBorders`로 대체되었습니다.
  * `[braille]` 섹션에서 (#14233):
    * `noMessageTimeout`이 제거되었으며, `showMessages`의 값으로 대체되었습니다.
    * `messageTimeout`은 더 이상 값 0을 가질 수 없으며, `showMessages`의 값으로 대체되었습니다.
    * `autoTether`가 제거되었으며, 이제 `tetherTo`는 "auto" 값을 가질 수 있습니다.
  * `[keyboard]` 섹션에서 (#14528):
    * `useCapsLockAsNVDAModifierKey`, `useNumpadInsertAsNVDAModifierKey`, `useExtendedInsertAsNVDAModifierKey`가 제거되었습니다.
    이들은 `NVDAModifierKeys`로 대체되었습니다.
* `NVDAHelper.RemoteLoader64` 클래스가 제거되었으며, 대체 항목은 없습니다. (#14449)
* `winAPI.sessionTracking`의 다음 함수가 제거되었으며, 대체 항목은 없습니다. (#14416, #14490)
  * `isWindowsLocked`
  * `handleSessionChange`
  * `unregister`
  * `register`
  * `isLockStateSuccessfullyTracked`
* `braille.handler.enabled`를 설정하여 점자 핸들러를 활성화/비활성화하는 것이 더 이상 불가능합니다.
점자 핸들러를 프로그래밍 방식으로 비활성화하려면 `braille.handler.decide_enabled`에 핸들러를 등록하세요. (#14503)
* `braille.handler.displaySize`를 설정하여 핸들러의 디스플레이 크기를 업데이트하는 것이 더 이상 불가능합니다.
디스플레이 크기를 프로그래밍 방식으로 업데이트하려면 `braille.handler.filter_displaySize`에 핸들러를 등록하세요.
이를 수행하는 방법에 대한 예시는 `brailleViewer`를 참조하세요. (#14503)
* `addonHandler.Addon.loadModule` 사용 방식에 변경사항이 있습니다. (#14481)
  * `loadModule`은 이제 백슬래시 대신 점을 구분자로 기대합니다.
  예: "lib\example" 대신 "lib.example".
  * `loadModule`은 이제 모듈을 로드할 수 없거나 오류가 있는 경우 예외를 발생시키며, 원인을 알리지 않고 `None`을 반환하지 않습니다.
* `appModules.foobar2000`에서 다음 심볼이 제거되었으며, 대체 항목은 없습니다. (#14570)
  * `statusBarTimes`
  * `parseIntervalToTimestamp`
  * `getOutputFormat`
  * `getParsingFormat`
* 다음 항목은 더 이상 싱글톤이 아니며, get 메서드가 제거되었습니다.
`Example.get()` 대신 `Example()`을 사용하세요. (#14248)
  * `UIAHandler.customAnnotations.CustomAnnotationTypesCommon`
  * `UIAHandler.customProps.CustomPropertiesCommon`
  * `NVDAObjects.UIA.excel.ExcelCustomProperties`
  * `NVDAObjects.UIA.excel.ExcelCustomAnnotationTypes`

#### 지원 종료 예정

* `NVDAObjects.UIA.winConsoleUIA.WinTerminalUIA`는 지원 종료 예정이며, 사용이 권장되지 않습니다. (#14047)
* `config.addConfigDirsToPythonPackagePath`는 이동되었습니다.
대신 `addonHandler.packaging.addDirsToPythonPackagePath`를 사용하세요. (#14350)
* `braille.BrailleHandler.TETHER_*`는 지원 종료 예정입니다.
대신 `configFlags.TetherTo.*.value`를 사용하세요. (#14233)
* `utils.security.postSessionLockStateChanged`는 지원 종료 예정입니다.
대신 `utils.security.post_sessionLockStateChanged`를 사용하세요. (#14486)
* `NVDAObject.hasDetails`, `NVDAObject.detailsSummary`, `NVDAObject.detailsRole`는 지원 종료 예정입니다.
대신 `NVDAObject.annotations`를 사용하세요. (#14507)
* `keyboardHandler.SUPPORTED_NVDA_MODIFIER_KEYS`는 지원 종료 예정이며, 직접적인 대체 항목은 없습니다.
대신 `config.configFlags.NVDAKey` 클래스를 사용하는 것을 고려하세요. (#14528)
* `gui.MainFrame.evaluateUpdatePendingUpdateMenuItemCommand`는 지원 종료 예정입니다.
대신 `gui.MainFrame.SysTrayIcon.evaluateUpdatePendingUpdateMenuItemCommand`를 사용하세요. (#14523)

## 2022.4

이번 릴리즈는 표 전체 읽기 명령을 포함한 여러 개의 새로운 단축키가 포함되어 있습니다.
빠른 시작 가이드 섹션이 사용자 가이드에 추가되었습니다.
또한, 여러 버그가 포함되어 있습니다.

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
이러한 수정 사항이 제대로 작동하려면 NVDA가 상호 작용하는 응용 프로그램도 DPI를 인식해야 합니다.
Chrome 및 Edge에는 여전히 알려진 문제가 있습니다. (#13254)
  * 이제 시각적 강조 표시 프레임이 대부분의 응용 프로그램에 올바르게 배치되어야 합니다. (#13370, #3875, #12070)
  * 이제 터치 스크린 상호 작용이 대부분의 응용 프로그램에서 정확해야 합니다. (#7083)
  * 마우스 추적은 이제 대부분의 응용 프로그램에서 작동합니다. (#6722)
* 방향 상태(가로/세로 방향) 변경은 이제 변경 사항이 없을 때(예: 모니터 변경) 올바르게 무시됩니다. (#14035)
* NVDA는 Windows 10 시작 메뉴 타일과 Windows 11의 가상 데스크탑을 재배치하는 것과 같은 위치에 드래그 항목을 화면에 표시합니다. (#12271, #14081)
* 고급 설정에서 "기본값 복원" 단추를 누르면 "로그된 오류에 대해 사운드 재생" 옵션이 기본값으로 올바르게 복원됩니다. (#14149)
* NVDA는 이제 Java 응용 프로그램에서 `NVDA+f10` 바로 가기 키를 사용하여 텍스트를 선택할 수 있습니다. (#14163)
* Microsoft Teams에서 스레드 대화를 위 아래 화살표 키로 탐색할 때 NVDA가 더 이상 메뉴에 갇히지 않습니다. (#14355)

### 개발 변경사항

NVDA의 지원 종료 예정 API 및 제거 프로세스에 대한 내용은 [개발자 가이드](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#API) 를 참조하시기 바랍니다.

* [NVDA API 공지 메일링 리스트](https://groups.google.com/a/nvaccess.org/g/nvda-api/about)가 생성되었습니다. (#13999)
* 대부분의 UI 자동화 응용 프로그램에서 `textChange` 이벤트를 처리하지 않도록 변경되었습니다. 이는 성능에 극도로 부정적인 영향을 미치기 때문입니다. (#11002, #14067)

#### 지원 종료 예정

* `core.post_windowMessageReceipt`는 지원 종료 예정입니다. 대신 `winAPI.messageWindow.pre_handleWindowMessage`를 사용하세요.
* `winKernel.SYSTEM_POWER_STATUS`는 지원 종료 예정이며, 사용이 권장되지 않습니다. 이는 `winAPI._powerTracking.SystemPowerStatus`로 이동되었습니다.
* `winUser.SM_*` 상수는 지원 종료 예정입니다. 대신 `winAPI.winUser.constants.SystemMetrics`를 사용하세요.

## 2022.3.3

이 릴리스는 2022.3.2, 2022.3.1 및 2022.3에서 발생한 문제를 수정하기 위한 마이너 릴리스입니다.
또한 보안 문제를 해결합니다.

### 보안 수정사항

* 인증되지 않은 사용자가 시스템에 접근(예: NVDA 파이썬 콘솔)할 가능성을 방지합니다.
([GHSA-fpwc-2gxx-j9v7](https://github.com/nvaccess/nvda/security/advisories/GHSA-fpwc-2gxx-j9v7))

### 버그 수정내역

* NVDA가 잠금 상태에서 멈출 경우, Windows 잠금 화면에서 사용자의 데스크탑에 접근할 수 있는 버그를 수정했습니다. (#14416)
* NVDA가 잠금 상태에서 멈출 경우, 장치가 여전히 잠겨 있는 것처럼 NVDA가 올바르게 동작하지 않는 버그를 수정했습니다. (#14416)
* Windows "PIN 잊어버림" 프로세스와 Windows 업데이트/설치 환경에서의 접근성 문제를 수정했습니다. (#14368)
* 일부 Windows 환경(예: Windows Server)에서 NVDA를 설치하려고 할 때 발생하는 버그를 수정했습니다. (#14379)

### 개발 변경사항

#### 지원 종료 예정

* `utils.security.isObjectAboveLockScreen(obj)`는 지원 종료 예정이며, 대신 `obj.isBelowLockScreen`을 사용하세요. (#14416)
* `winAPI.sessionTracking`의 다음 함수들은 2023.1에서 제거될 예정으로 지원 종료 예정입니다. (#14416)
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
  * `control+f`를 눌러 텍스트를 찾을 때, 리뷰커서의 위치가 찾은 용어 위치로 업데이트됩니다. (#11172)
  * 입력한 글자가 나타나지 않는 상황(예: 암호 입력)에서 입력 글자 알림이 기본으로 비활성화됩니다.
이 기능은 NVDA 설정의 고급 패널에서 다시 활성화할 수 있습니다.. (#11554)
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
* UI 자동화를 사용하여 Microsoft Excel 스프레드시트 컨트롤에 접근할 때, NVDA는 이제 셀이 병합되었는지 보고할 수 있습니다. (#12843)
* "상세 정보 있음"을 보고하는 대신, 가능한 경우 상세 정보의 목적을 포함하여 예를 들어 "코멘트 있음"과 같이 보고합니다. (#13649)
* NVDA의 설치 크기가 이제 Windows 프로그램 및 기능 섹션에 표시됩니다. (#13909)

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

### 개발 변경사항

* Comtypes가 버전 1.1.11로 업데이트되었습니다. (#12953)
* Windows Console(`conhost.exe`)의 NVDA API 레벨이 2(`FORMATTED`) 이상인 빌드(예: Windows 11 버전 22H2(Sun Valley 2)에 포함된 빌드)에서 UI Automation이 기본적으로 사용됩니다. (#10964)
  * 이는 NVDA의 고급 설정 패널에서 "Windows Console 지원" 설정을 변경하여 재정의할 수 있습니다.
  * Windows Console의 NVDA API 레벨을 확인하려면 "Windows Console 지원"을 "사용 가능한 경우 UIA"로 설정한 다음, 실행 중인 Windows Console 인스턴스에서 NVDA+F1 로그를 확인하세요.
* Chromium 가상 버퍼는 문서 객체가 IA2를 통해 MSAA `STATE_SYSTEM_BUSY` 상태를 노출하더라도 이제 로드됩니다. (#13306)
* NVDA의 실험적 기능에 사용할 수 있도록 `featureFlag`라는 설정 사양 타입이 생성되었습니다. 자세한 내용은 `devDocs/featureFlag.md`를 참조하세요. (#13859)

#### 지원 종료 예정

2022.3에서는 지원 종료 예정 항목이 제안되지 않았습니다.

## 2022.2.4

보안 문제를 해결하기 위한 패치 릴리스입니다.

### 버그 수정내역

* 잠금 화면의 로그 뷰어를 통해 NVDA 파이썬 콘솔을 열 수 있는 익스플로잇을 수정했습니다.
([GHSA-585m-rpvvv-93qg](https://github.com/nvaccess/nvda/security/advisories/GHSA-585m-rpvv-93qg))

## 2022.2.3

이번 릴리즈는 2022.2.1에 도입된 실수로 인한 API 손상을 수정하기 위한 패치입니다.

### 버그 수정내역

* NVDA가 보안 데스크탑에 들어갈 때 "보안 데스크탑"을 표시하지 않는 버그를 수정했습니다.
이로 인해 NVDA Remote가 보안 데스크탑을 인식하지 못했습니다. (#14094)

## 2022.2.2

이것은 2022.2.1에서 입력 제스처 도입으로 인해 생긴 버그를 수정하기 위한 패치 릴리즈입니다.

### 버그 수정내역

* 입력 제스처가 항상 작동하지 않는 버그를 수정했습니다. (#14065)

## 2022.2.1

이것은 보안 문제를 해결하기 위한 사소한 릴리스입니다.
보안 문제를 `<info@nvaccess.org>`에 책임감 있게 공개해 주세요.

### 보안 수정사항

* 잠금 화면에서 파이썬 콘솔을 실행할 수 있었던 고정 익스플로잇. (GHSA-rmq3-vvhq-gp32)
* 객체 탐색을 사용하여 잠금 화면을 피할 수 있었던 고정 익스플로잇. (GHSA-rmq3-vvhq-gp32)

### 개발 변경사항

#### 지원 종료 예정

이 지원 종료 예정 항목들은 현재 제거 일정이 잡혀 있지 않습니다.
지원 종료 예정된 별칭은 추후 공지가 있을 때까지 유지됩니다.
새로운 API를 테스트하고 피드백을 제공해 주세요.
추가기능 개발자는 이러한 변경 사항이 필요를 충족하지 못할 경우 GitHub 이슈를 열어주세요.

* `appModules.lockapp.LockAppObject`는 `NVDAObjects.lockscreen.LockScreenObject`로 대체해야 합니다. (GHSA-rmq3-vvhq-gp32)
* `appModules.lockapp.AppModule.SAFE_SCRIPTS`는 `utils.security.getSafeScripts()`로 대체해야 합니다. (GHSA-rmq3-vvhq-gp32)

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
워드패드와 다른 `richText` 컨트롤에서 숨겨진 텍스트를 더 이상 알리지 않습니다. (#13618)
* Windows 11 메모장에서 상태표시줄 내용을 읽을 것입니다. (#13688)
* 이제 탐색 객체 표시 기능을 활성화하면 강조 표시가 즉시 나타납니다. (#13641)
* 단일 열로 된 목록보기 항목의 읽기 문제을 수정합니다. (#13659, #13735)
* 영어 및 프랑스어를 영국 영어와 프랑스어(프랑스)로 되돌리는 경우에 대한 eSpeak 자동 언어 전환을 수정합니다. (#13727)
* 이전에 설치된 언어로 전환하려고 할 경우에 대한 OneCore의 자동 언어 전환을 수정합니다. (#13732)

### 개발 변경사항

* NVDA 종속성을 Visual Studio 2022 (17.0)로 컴파일하는 것이 이제 지원됩니다.
개발 및 릴리스 빌드에서는 여전히 Visual Studio 2019가 사용됩니다. (#13033)
* `IAccessible::get_accSelection`을 통해 선택된 자식의 개수를 가져올 때,
음수 자식 ID 또는 IDispatch가 반환되는 경우를 이제 적절히 처리합니다. (#13277)
* `appModuleHandler` 모듈에 새로운 편의 함수 `registerExecutableWithAppModule`과 `unregisterExecutable`이 추가되었습니다.
이 함수들은 여러 실행 파일에서 단일 앱 모듈을 사용할 수 있도록 지원합니다. (#13366)

#### 지원 종료 예정

이 변경사항들은 API 호환성을 깨뜨릴 수 있는 제안된 변경사항들입니다.
API의 지원 종료 예정 부분은 명시된 릴리스까지 계속 사용할 수 있습니다.
릴리스가 명시되지 않은 경우, 제거 계획은 아직 결정되지 않았습니다.
제거 로드맵은 '최선의 노력'에 기반하며 변경될 수 있습니다.
새로운 API를 테스트하고 피드백을 제공해 주세요.
추가기능 개발자는 이러한 변경사항이 API가 요구사항을 충족하지 못하게 만드는 경우 GitHub 이슈를 열어주세요.

* `appModuleHandler.NVDAProcessID`는 지원 종료 예정이며, 대신 `globalVars.appPid`를 사용하세요. (#13646)
* `gui.quit`는 지원 종료 예정이며, 대신 `wx.CallAfter(mainFrame.onExitCommand, None)`를 사용하세요. (#13498)
  -
* 일부 별칭 앱 모듈이 지원 종료 예정으로 표시되었습니다.
이 모듈들에서 가져오는 코드는 대신 대체 모듈에서 가져와야 합니다. (#13366)

| | 제거된 모듈 이름 | 대체 모듈 ||
|---|---|
||azuredatastudio |code||
||azuredatastudio-insiders |code||
||calculatorapp |calculator||
||codeinsiders |code||
||commsapps |hxmail||
||dbeaver |eclipse||
||digitaleditionspreview |digitaleditions||
||esybraille |esysuite||
||hxoutlook |hxmail||
||miranda64 |miranda32||
||mpc-hc |mplayerc||
||mpc-hc64 |mplayerc||
||notepad++ |notepadPlusPlus||
||searchapp |searchui||
||searchhost |searchui||
||springtoolsuite4 |eclipse||
||sts |eclipse||
||teamtalk3 |teamtalk4classic||
||textinputhost |windowsinternal_composableshell_experiences_textinput_inputapp||
||totalcmd64 |totalcmd||
||win32calc |calc||
||winmail |msimn||
||zend-eclipse-php |eclipse||
||zendstudio |eclipse||

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

### 개발 변경사항

* 참고: 이것은 추가기능 API 호환성을 깨뜨리는 릴리즈입니다. 추가기능은 재테스트를 거쳐 매니페스트를 업데이트해야 합니다.
* NVDA는 여전히 Visual Studio 2019를 요구하지만, Visual Studio의 최신 버전(예: 2022)이 2019와 함께 설치된 경우 빌드가 실패하지 않습니다. (#13033, #13387)
* SCons가 버전 4.3.0으로 업데이트되었습니다. (#13033)
* py2exe가 버전 0.11.1.0으로 업데이트되었습니다. (#13510)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable`가 제거되었습니다. 대신 `apiLevel`을 사용하세요. (#12955, #12660)
* `sysTreeView32`에서 `TVItemStruct`가 제거되었습니다. (#12935)
* Outlook appModule에서 `MessageItem`이 제거되었습니다. (#12935)
* `audioDucking.AUDIODUCKINGMODE_*` 상수는 이제 `DisplayStringIntEnum`입니다. (#12926)
  * 사용 사례는 `AudioDuckingMode.*`로 대체해야 합니다.
  * `audioDucking.audioDuckingModes` 사용 사례는 `AudioDuckingMode.*.displayString`으로 대체해야 합니다.
* `audioDucking.ANRUS_ducking_*` 상수 사용 사례는 `ANRUSDucking.*`로 대체해야 합니다. (#12926)
* `synthDrivers.sapi5` 변경사항 (#12927):
  * `SPAS_*` 사용 사례는 `SPAudioState.*`로 대체해야 합니다.
  * `constants.SVSF*` 사용 사례는 `SpeechVoiceSpeakFlags.*`로 대체해야 합니다.
    * 참고: `SVSFlagsAsync`는 `SpeechVoiceSpeakFlags.Async`로 대체해야 하며, `SpeechVoiceSpeakFlags.lagsAsync`가 아닙니다.
  * `constants.SVE*` 사용 사례는 `SpeechVoiceEvents.*`로 대체해야 합니다.
* `soffice` appModule에서 다음 클래스와 함수가 제거되었습니다: `JAB_OOTableCell`, `JAB_OOTable`, `gridCoordStringToNumbers`. (#12849)
* `core.CallCancelled`는 이제 `exceptions.CallCancelled`입니다. (#12940)
* `core`와 `logHandler`에서 RPC로 시작하는 모든 상수는 `RPCConstants.RPC` 열거형으로 이동되었습니다. (#12940)
* 마우스를 클릭하여 논리적 작업(예: 활성화(기본) 또는 컨텍스트 메뉴 표시(보조))를 수행하려면 `mouseHandler.doPrimaryClick` 및 `mouseHandler.doSecondaryClick` 함수를 사용하는 것이 좋습니다.
`executeMouseEvent`를 사용하여 왼쪽 또는 오른쪽 마우스 버튼을 지정하는 대신 이를 사용하세요.
이렇게 하면 Windows 사용자 설정에서 기본 마우스 버튼을 교체하는 옵션을 준수할 수 있습니다. (#12642)
* `config.getSystemConfigPath`가 제거되었습니다. 대체 항목은 없습니다. (#12943)
* `shlobj.SHGetFolderPath`가 제거되었습니다. 대신 `shlobj.SHGetKnownFolderPath`를 사용하세요. (#12943)
* `shlobj` 상수가 제거되었습니다. `SHGetKnownFolderPath`와 함께 사용할 새 열거형 `shlobj.FolderId`가 생성되었습니다. (#12943)
* `diffHandler.get_dmp_algo`와 `diffHandler.get_difflib_algo`는 각각 `diffHandler.prefer_dmp`와 `diffHandler.prefer_difflib`로 대체되었습니다. (#12974)
* `languageHandler.curLang`가 제거되었습니다. 현재 NVDA 언어를 가져오려면 `languageHandler.getLanguage()`를 사용하세요. (#13082)
* NVDA가 상태 표시줄에서 텍스트를 가져오는 방식을 사용자 정의하려면 appModule에 `getStatusBarText` 메서드를 구현할 수 있습니다. (#12845)
* `globalVars.appArgsExtra`가 제거되었습니다. (#13087)
  * 추가 명령줄 인수를 처리해야 하는 추가기능의 경우 `addonHandler.isCLIParamKnown` 및 개발자 가이드의 세부 정보를 참조하세요.
* UIA 핸들러 모듈 및 기타 UIA 지원 모듈은 이제 UIAHandler 패키지의 일부입니다. (#10916)
  * `UIAUtils`는 이제 `UIAHandler.utils`입니다.
  * `UIABrowseMode`는 이제 `UIAHandler.browseMode`입니다.
  * `_UIAConstants`는 이제 `UIAHandler.constants`입니다.
  * `_UIACustomProps`는 이제 `UIAHandler.customProps`입니다.
  * `_UIACustomAnnotations`는 이제 `UIAHandler.customAnnotations`입니다.
* `IAccessibleHandler`의 `IA2_RELATION_*` 상수는 `IAccessibleHandler.RelationType` 열거형으로 대체되었습니다. (#13096)
  * 제거된 항목: `IA2_RELATION_FLOWS_FROM`
  * 제거된 항목: `IA2_RELATION_FLOWS_TO`
  * 제거된 항목: `IA2_RELATION_CONTAINING_DOCUMENT`
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST`, `LOCALE_SLANGDISPLAYNAME`는 `languageHandler`에서 제거되었습니다. 대신 `languageHandler.LOCALE`의 멤버를 사용하십시오. (#12753)
* NVDA의 후킹 라이브러리를 Minhook에서 Microsoft Detours로 변경했습니다. 이 라이브러리는 주로 디스플레이 모델을 지원하기 위해 사용됩니다. (#12964)
* `winVersion.WIN10_RELEASE_NAME_TO_BUILDS`가 제거되었습니다. (#13211)
* SCons는 이제 시스템의 논리 프로세서 수와 동일한 작업 수로 빌드하도록 경고합니다.
이 설정은 멀티코어 시스템에서 빌드 시간을 크게 단축할 수 있습니다. (#13226, #13371)
* `characterProcessing.SYMLVL_*` 상수는 제거되었습니다. 대신 `characterProcessing.SymbolLevel.*`을 사용하십시오. (#13248)
* `addonHandler`에서 `loadState`와 `saveState` 함수가 제거되었습니다. 대신 `addonHandler.state.load`와 `addonHandler.state.save`를 사용하십시오. (#13245)
* NVDAHelper의 UWP/OneCore 상호작용 계층을 [C++/CX에서 C++/Winrt로](https://docs.microsoft.com/en-us/windows/uwp/cpp-and-winrt-apis/move-to-winrt-from-cx) 이전했습니다. (#10662)
* 이제 `DictionaryDialog`를 사용하려면 반드시 서브클래스를 생성해야 합니다. (#13268)
* `config.RUN_REGKEY`, `config.NVDA_REGKEY`는 지원 종료 예정입니다. 대신 `config.RegistryKey.RUN`, `config.RegistryKey.NVDA`를 사용하세요. 이 항목들은 2023년에 제거될 예정입니다. (#13242)
* `easeOfAccess.ROOT_KEY`, `easeOfAccess.APP_KEY_PATH`는 지원 종료 예정입니다. 대신 `easeOfAccess.RegistryKey.ROOT`, `easeOfAccess.RegistryKey.APP`를 사용하세요. 이 항목들은 2023년에 제거될 예정입니다. (#13242)
* `easeOfAccess.APP_KEY_NAME`은 지원 종료 예정이며, 2023년에 제거될 예정입니다. (#13242)
* `DictionaryDialog`와 `DictionaryEntryDialog`는 `gui.settingsDialogs`에서 `gui.speechDict`로 이동되었습니다. (#13294)
* IAccessible2 관계가 이제 IAccessible2 객체의 개발자 정보에 표시됩니다. (#13315)
* `languageHandler.windowsPrimaryLCIDsToLocaleNames`가 제거되었습니다. 대신 `languageHandler.windowsLCIDToLocaleName` 또는 `winKernel.LCIDToLocaleName`을 사용하세요. (#13342)
* UIA 객체의 `UIAAutomationId` 속성을 `cachedAutomationId`보다 우선적으로 사용하세요. (#13125, #11447)
  * `cachedAutomationId`는 요소에서 직접 가져온 경우에만 사용할 수 있습니다.
* `NVDAObjects.window.scintilla.CharacterRangeStruct`는 `NVDAObjects.window.scintilla.Scintilla.CharacterRangeStruct`로 이동되었습니다. (#13364)
* Boolean `gui.isInMessageBox`가 제거되었습니다. 대신 함수 `gui.message.isModalMessageBoxActive`를 사용하세요. (#12984, #13376)
* `controlTypes`가 여러 하위 모듈로 분리되었습니다. (#12510, #13588)
  * `ROLE_*`와 `STATE_*`는 `Role.*`와 `State.*`로 대체되었습니다.
  * 여전히 사용할 수 있지만, 다음 항목들은 지원 종료 예정으로 간주해야 합니다:
    * `ROLE_*`와 `STATE_*`, 대신 `Role.*`와 `State.*`를 사용하세요.
    * `roleLabels`, `stateLabels` 및 `negativeStateLabels`, `roleLabels[ROLE_*]`와 같은 사용 사례는 `Role.*.displayString` 또는 `State.*.negativeDisplayString`으로 대체해야 합니다.
    * `processPositiveStates`와 `processNegativeStates`는 대신 `processAndLabelStates`를 사용해야 합니다.
* Excel 셀 상태 상수(`NVSTATE_*`)는 이제 `NvCellState` 열거형의 값으로, `NVDAObjects/window/excel.py`의 `NvCellState` 열거형에 반영되며 `_nvCellStatesToStates`를 통해 `controlTypes.State`에 매핑됩니다. (#13465)
* `EXCEL_CELLINFO` 구조체 멤버 `state`는 이제 `nvCellStates`로 변경되었습니다.
* `mathPres.ensureInit`가 제거되었으며, MathPlayer는 이제 NVDA가 시작될 때 초기화됩니다. (#13486)

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
* Microsoft Word에서 TaiwanMicrosoft Quick과 같은 중국어 입력 방법을 사용할 때 점자 디스플레이를 앞뒤로 잘못 스크롤해도 더 이상 원래 캐럿 위치로 계속 이동하지 않습니다. (#12855)
* UIA로 Microsoft Word 문서에 접근하고 있을 때, 문장 단위로 탐색하기(Alt + 아래 화살표 키 / Alt + 위 화살표 키)가 다시 가능합니다. (#9254)
* UIA가 활성화된 MS Word 문서를 탐색할 때 단락 들여쓰기를 알립니다. (#12899)
* UIA로 Microsoft Word에 액세스할 때 변경 추적 명령과 일부 다른 지역화된 명령이 Word에 보고됩니다. (#12904)
* name이나 content가 description과 일치 할 때의 중복된 점자 및 음성 출력을 수정됐습니다. (#12888)
* UIA가 활성화된 MS Word에서는 입력할 때 철자 오류 소리가 더 정확하게 들립니다. (#12161)
* Windows 11에서 NVDA는 Alt+Tab을 눌러 프로그램 간 전환할 때 더 이상 "창"을 알리지 않습니다. (#12648)
* UIA를 통해 문서에 액세스하지 않을 때 MS Word에서 새로운 Modern Comments 사이드 트랙 창이 지원됩니다. 사이드 트랙 창과 문서 사이를 이동하려면 Alt+f12를 누르십시오. (#12982)

### 개발 변경사항

* 이제 NVDA를 빌드하려면 Visual Studio 2019 16.10.4 이상이 필요합니다.
프로덕션 빌드 환경과 일치시키기 위해, Visual Studio를 [AppVeyor에서 사용하는 현재 버전](https://www.appveyor.com/docs/windows-images-software/#visual-studio-2019)과 동기화하여 업데이트하세요. (#12728)
* `NVDAObjects.UIA.winConsoleUIA.WinConsoleUIA.isImprovedTextRangeAvailable`는 2022.1에서 제거될 예정으로 지원 종료 예정입니다. (#12660)
  * 대신 `apiLevel`을 사용하세요. (`_UIAConstants.WinConsoleAPILevel`에 있는 주석을 참조하세요.)
* GDI 응용 프로그램(디스플레이 모델을 통해)에서 가져온 텍스트 배경색의 투명도가 이제 추가기능이나 appModule에서 노출됩니다. (#12658)
* `LOCALE_SLANGUAGE`, `LOCALE_SLIST`, `LOCALE_SLANGDISPLAYNAME`은 `languageHandler`의 `LOCALE` 열거형으로 이동되었습니다.
이 항목들은 여전히 모듈 수준에서 사용할 수 있지만 지원 종료 예정이며 NVDA 2022.1에서 제거될 예정입니다. (#12753)
* `addonHandler.loadState`와 `addonHandler.saveState` 함수의 사용은 각각 `addonHandler.state.save`와 `addonHandler.state.load`로 대체되어야 하며, 2022.1 이전에 변경해야 합니다. (#12792)
* 이제 시스템 테스트에서 점자 출력 확인이 가능합니다. (#12917)

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

### 개발 변경사항

* `characterProcessing.SYMLVL_*` 상수는 2022.1 이전에 해당하는 `SymbolLevel.*`로 대체해야 합니다. (#11856, #12636)
* `controlTypes`가 여러 하위 모듈로 분리되었으며, 지원 종료 예정으로 표시된 심볼은 2022.1 이전에 대체해야 합니다. (#12510)
  * `ROLE_*` 및 `STATE_*` 상수는 각각 해당하는 `Role.*` 및 `State.*`로 대체해야 합니다.
  * `roleLabels`, `stateLabels` 및 `negativeStateLabels`는 지원 종료 예정이며, `roleLabels[ROLE_*]`와 같은 사용 사례는 해당하는 `Role.*.displayString` 또는 `State.*.negativeDisplayString`으로 대체해야 합니다.
  * `processPositiveStates`와 `processNegativeStates`는 제거 예정입니다.
* Windows 10 버전 1511 이상(Insider Preview 빌드를 포함)에서 현재 Windows 기능 업데이트 릴리스 이름은 Windows 레지스트리에서 가져옵니다. (#12509)
* 지원 종료 예정: `winVersion.WIN10_RELEASE_NAME_TO_BUILDS`는 2022.1에서 제거될 예정이며, 직접적인 대체 항목은 없습니다. (#12544)

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
* 사용 설명서, 변경 이력, Nvda 기능키 목록(Nvda 간편 기능키 참고서)가 새로 개편되었습니다. (#12027)ㅁ
* 이제 Microsoft Word 같이 화면 레이아웃을 지원하지 않는 프로그램에서 화면 레이아웃 기능을 전환을 시도하면 "지원 안 됨"을 알립니다. (#7297)
* 고급설정에 있는 '포커스 이벤트가 만료되면 발화를 중단합니다' 옵션은 이제 활성화(예)가 기본값으로 설정됩니다. (#10885)
  * 이 기능은 설정에서 "아니오"를 선택하여 비활성화할 수 있습니다.
  * 웹 응용 프로그램 (E.G. Gmail) 포커스를 빠르게 이동할 때 더 이상 오래된 정보를 말하지 않습니다..
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

### 개발 변경사항

* 참고: 이것은 추가기능 API 호환성을 깨뜨리는 릴리스입니다. 추가기능은 다시 테스트되어야 하며, 매니페스트를 업데이트해야 합니다.
* NVDA의 빌드 시스템은 이제 모든 Python 종속성을 pip으로 가져와 Python 가상 환경에 저장합니다. 이 모든 과정은 투명하게 처리됩니다.
  * NVDA를 빌드하려면 기존 방식대로 SCons를 계속 사용해야 합니다. 예: 저장소의 루트에서 scons.bat을 실행합니다. `py -m SCons` 실행은 더 이상 지원되지 않으며, `scons.py`도 제거되었습니다.
  * 소스에서 NVDA를 실행하려면 `source/nvda.pyw`를 직접 실행하는 대신, 이제 개발자는 저장소 루트에 있는 `runnvda.bat`을 사용해야 합니다. 만약 `source/nvda.pyw`를 실행하려고 하면, 더 이상 지원되지 않는다는 메시지 상자가 표시됩니다.
  * 단위 테스트를 수행하려면 `rununittests.bat [<추가 unittest discover 옵션>]`을 실행하세요.
  * 시스템 테스트를 수행하려면 `runsystemtests.bat [<추가 robot 옵션>]`을 실행하세요.
  * 린팅을 수행하려면 `runlint.bat <기준 브랜치>`를 실행하세요.
  * 자세한 내용은 readme.md를 참조하세요.
* 다음 Python 종속성도 업그레이드되었습니다:
  * comtypes가 1.1.8로 업데이트되었습니다.
  * pySerial이 3.5로 업데이트되었습니다.
  * wxPython이 4.1.1로 업데이트되었습니다.
  * Py2exe가 0.10.1.0으로 업데이트되었습니다.
* `LiveText._getTextLines`가 제거되었습니다. (#11639)
  * 대신, 객체의 모든 텍스트를 문자열로 반환하는 `_getText`를 재정의하세요.
* `LiveText` 객체는 이제 문자 단위로 차이를 계산할 수 있습니다. (#11639)
  * 특정 객체에 대해 차이 계산 동작을 변경하려면 `diffAlgo` 속성을 재정의하세요(자세한 내용은 docstring을 참조하세요).
* `script` 데코레이터로 스크립트를 정의할 때, 'allowInSleepMode'라는 불리언 인수를 지정하여 스크립트가 슬립 모드에서 사용 가능한지 여부를 제어할 수 있습니다. (#11979)
* 다음 함수들이 config 모듈에서 제거되었습니다. (#11935)
  * `canStartOnSecureScreens`대신 `config.isInstalledCopy`를 사용하세요.
  * `hasUiAccess`와 `execElevated`대신 systemUtils 모듈에서 사용하세요.
  * `getConfigDirs`대신 `globalVars.appArgs.configPath`를 사용하세요.
* controlTypes 모듈의 REASON_상수들이 제거되었습니다대신 `controlTypes.OutputReason`을 사용하세요. (#11969)
* `REASON_QUICKNAV`가 browseMode에서 제거되었습니다대신 `controlTypes.OutputReason.QUICKNAV`를 사용하세요. (#11969)
* `NVDAObject` (및 파생 객체)의 `isCurrent` 속성은 이제 Enum 클래스 `controlTypes.IsCurrent`를 엄격히 반환합니다. (#11782)
  * `isCurrent`는 더 이상 Optional이 아니며, None을 반환하지 않습니다.
    * 객체가 현재 상태가 아닐 경우 `controlTypes.IsCurrent.NO`가 반환됩니다.
* `controlTypes.isCurrentLabels` 매핑이 제거되었습니다. (#11782)
  * 대신 `controlTypes.IsCurrent` 열거형 값의 `displayString` 속성을 사용하세요.
    * 예: `controlTypes.IsCurrent.YES.displayString`.
* `winKernel.GetTimeFormat`이 제거되었습니다대신 `winKernel.GetTimeFormatEx`를 사용하세요. (#12139)
* `winKernel.GetDateFormat`이 제거되었습니다대신 `winKernel.GetDateFormatEx`를 사용하세요. (#12139)
* `gui.DriverSettingsMixin`이 제거되었습니다대신 `gui.AutoSettingsMixin`을 사용하세요. (#12144)
* `speech.getSpeechForSpelling`이 제거되었습니다대신 `speech.getSpellingSpeech`를 사용하세요. (#12145)
* `speech` 모듈에서 명령을 직접 가져올 수 없습니다. 예: `import speech; speech.ExampleCommand()` 또는 `import speech.manager; speech.manager.ExampleCommand()` 대신 `from speech.commands import ExampleCommand`를 사용하세요. (#12126)
* `speakTextInfo`는 이제 reason이 `SAYALL`일 경우 `speakWithoutPauses`를 통해 음성을 전달하지 않습니다. 이는 `SayAllHandler`가 수동으로 처리하기 때문입니다. (#12150)
* `synthDriverHandler` 모듈은 더 이상 `globalCommands`와 `gui.settingsDialogs`에서 별표(*)로 가져오지 않습니다. 대신 `from synthDriverHandler import synthFunctionExample`을 사용하세요. (#12172)
* `controlTypes`에서 `ROLE_EQUATION`이 제거되었습니다. 대신 `ROLE_MATH`를 사용하세요. (#12164)
* `autoSettingsUtils.driverSetting` 클래스는 `driverHandler`에서 제거되었습니다. 대신 `autoSettingsUtils.driverSetting`에서 사용하세요. (#12168)
* `autoSettingsUtils.utils` 클래스는 `driverHandler`에서 제거되었습니다. 대신 `autoSettingsUtils.utils`에서 사용하세요. (#12168)
* `contentRecog.BaseContentRecogTextInfo`를 상속하지 않는 `TextInfo`에 대한 지원이 제거되었습니다. (#12157)
* `speech.speakWithoutPauses`가 제거되었습니다. 대신 `speech.speechWithoutPauses.SpeechWithoutPauses(speakFunc=speech.speak).speakWithoutPauses`를 사용하세요. (#12195, #12251)
* `speech.re_last_pause`가 제거되었습니다. 대신 `speech.speechWithoutPauses.SpeechWithoutPauses.re_last_pause`를 사용하세요. (#12195, #12251)
* `WelcomeDialog`, `LauncherDialog`, `AskAllowUsageStatsDialog`는 `gui.startupDialogs`로 이동되었습니다. (#12105)
* `getDocFilePath`가 `gui`에서 `documentationUtils` 모듈로 이동되었습니다. (#12105)
* `gui.accPropServer` 모듈과 `gui.nvdaControls` 모듈의 `AccPropertyOverride` 및 `ListCtrlAccPropServer` 클래스가 제거되었습니다. 이는 WX의 기본 접근성 속성 재정의 지원을 사용하기 위함입니다. WX 컨트롤의 접근성을 개선하려면 `wx.Accessible`을 구현하세요. (#12215)
* `source/comInterfaces/`의 파일들이 이제 IDE와 같은 개발자 도구에서 더 쉽게 사용할 수 있습니다. (#12201)
* Windows 버전을 가져오고 비교하기 위한 편의 메서드와 타입이 `winVersion` 모듈에 추가되었습니다. (#11909)
  * `winVersion` 모듈의 `isWin10` 함수가 제거되었습니다.
  * `winVersion.WinVersion` 클래스는 Windows 버전 정보를 캡슐화하는 비교 가능하고 정렬 가능한 타입입니다.
  * 현재 실행 중인 OS를 나타내는 `winVersion.WinVersion`을 가져오기 위해 `winVersion.getWinVer` 함수를 사용하세요.
  * 알려진 Windows 릴리스에 대한 편의 상수가 추가되었습니다. `winVersion.WIN*` 상수를 참조하세요.
* `IAccessibleHandler`는 더 이상 `IAccessible` 및 `IA2 COM` 인터페이스에서 모든 것을 별표(*)로 가져오지 않습니다. 대신 직접 사용하세요. (#12232)
* `TextInfo` 객체는 이제 시작과 끝 속성을 가지며, `<`, `<=`, `==`, `!=`, `>=`, `>`와 같은 연산자를 사용하여 수학적으로 비교할 수 있습니다. (#11613)
  * 예: `ti1.start <= ti2.end`
  * 이는 이제 `ti1.compareEndPoints(ti2,"startToEnd") <= 0` 대신 선호되는 사용법입니다.
* TextInfo의 start와 end 속성은 서로 설정할 수도 있습니다. (#11613)
  * 예: ti1.start = ti2.end
  * 이 사용법은 ti1.SetEndPoint(ti2, "startToEnd") 대신 선호됩니다.
* `wx.CENTRE_ON_SCREEN`과 `wx.CENTER_ON_SCREEN`은 제거되었습니다. 대신 `self.CentreOnScreen()`을 사용하세요. (#12309)
* `easeOfAccess.isSupported`가 제거되었습니다. NVDA는 이 값이 `True`로 평가되는 Windows 버전만 지원합니다. (#12222)
* `sayAllHandler`는 `speech.sayAll`로 이동되었습니다. (#12251)
  * `speech.sayAll.SayAllHandler`는 `stop`, `isRunning`, `readObjects`, `readText`, `lastSayAllMode` 함수를 제공합니다.
  * `SayAllHandler.stop`은 `SayAllHandler`의 `SpeechWithoutPauses` 인스턴스도 초기화합니다.
  * `CURSOR_REVIEW`와 `CURSOR_CARET`은 `CURSOR.REVIEW`와 `CURSOR.CARET`으로 대체되었습니다.
* `speech.SpeechWithoutPauses`는 `speech.speechWithoutPauses.SpeechWithoutPauses`로 이동되었습니다. (#12251)
* `speech.curWordChars`는 `speech._curWordChars`로 이름이 변경되었습니다. (#12395)
* 다음 항목들은 `speech`에서 제거되었으며, 이제 `speech.getState()`를 통해 접근할 수 있습니다. 이 값들은 이제 읽기 전용입니다. (#12395)
  * `speechMode`
  * `speechMode_beeps_ms`
  * `beenCanceled`
  * `isPaused`
* `speech.speechMode`를 업데이트하려면 `speech.setSpeechMode`를 사용하세요. (#12395)
* 다음 항목들은 `speech.SpeechMode`로 이동되었습니다. (#12395)
  * `speech.speechMode_off`는 `speech.SpeechMode.off`로 변경되었습니다.
  * `speech.speechMode_beeps`는 `speech.SpeechMode.beeps`로 변경되었습니다.
  * `speech.speechMode_talk`는 `speech.SpeechMode.talk`로 변경되었습니다.
* `IAccessibleHandler.IAccessibleObjectIdentifierType`은 이제 `IAccessibleHandler.types.IAccessibleObjectIdentifierType`입니다. (#12367)
* `NVDAObjects.UIA.WinConsoleUIA`의 다음 항목들이 변경되었습니다. (#12094)
  * `NVDAObjects.UIA.winConsoleUIA.is21H1Plus`는 `NVDAObjects.UIA.winConsoleUIA.isImprovedTextRangeAvailable`로 이름이 변경되었습니다.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfo`는 클래스 이름의 첫 글자가 대문자로 시작하도록 변경되었습니다.
  * `NVDAObjects.UIA.winConsoleUIA.consoleUIATextInfoPre21H1`는 `NVDAObjects.UIA.winConsoleUIA.ConsoleUIATextInfoWorkaroundEndInclusive`로 이름이 변경되었습니다.
    * 이 구현은 [microsoft/terminal PR 4018](https://github.com/microsoft/terminal/pull/4018) 이전에 텍스트 범위에서 양쪽 끝점이 포함되는 문제를 해결합니다.
    * `expand`, `collapse`, `compareEndPoints`, `setEndPoint` 등의 작업에 대한 해결책이 포함됩니다.

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

* Fast Log Entry 응용 프로그램을 사용할 때 편집 영역에서 NVDA가 제대로 동작하도록 수정됐습니다. (#8996)
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

### 개발 변경사항

* 시스템 테스트에서 이제 `spy.emulateKeyPress`를 사용하여 키를 보낼 수 있습니다. 이 함수는 NVDA의 키 이름 규칙을 따르는 키 식별자를 받고, 기본적으로 동작이 실행될 때까지 차단합니다. (#11581)
* NVDA는 이제 현재 디렉터리가 NVDA 응용 프로그램 디렉터리일 필요 없이 동작합니다. (#6491)
* 라이브 영역의 aria live politeness 설정은 이제 NVDA 객체에서 `liveRegionPoliteness` 속성을 통해 확인할 수 있습니다. (#11596)
* Outlook과 Word 문서에 대해 별도의 제스처를 정의할 수 있습니다. (#11196)

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

### 개발 변경사항

* GUI Helper의 BoxSizerHelper.addDialogDismissButtons 메서드에 "separated"라는 새로운 키워드 인수가 추가되어, 메시지 및 단일 입력 대화상자를 제외한 다른 대화상자에 표준 가로 구분선을 추가할 수 있습니다. (#6468)
* 응용 프로그램 모듈에 실행 파일 경로(appPath), Windows 스토어 응용 프로그램 여부(isWindowsStoreApp), 응용 프로그램의 머신 아키텍처(appArchitecture)와 같은 추가 속성이 추가되었습니다. (#7894)
* Windows 8 이상에서 wwahost.exe 내부에 호스팅된 응용 프로그램에 대한 응용 프로그램 모듈을 생성할 수 있습니다. (#4569)
* 로그의 일부를 구분한 후 NVDA+Control+Shift+F1을 사용하여 클립보드에 복사할 수 있습니다. (#9280)
* Python의 순환 가비지 수집기에 의해 삭제되는 NVDA 전용 객체가 이제 로그에 기록되어 참조 순환 제거를 돕습니다. (#11499)
  * NVDA의 대부분의 클래스가 추적되며, 여기에는 NVDAObjects, appModules, GlobalPlugins, SynthDrivers, TreeInterceptors가 포함됩니다.
  * 추적이 필요한 클래스는 garbageHandler.TrackedObject를 상속받아야 합니다.
* MSAA 이벤트에 대한 중요한 디버그 로깅을 NVDA의 고급 설정에서 활성화할 수 있습니다. (#11521)
* 현재 포커스된 객체에 대한 MSAA winEvent는 특정 스레드의 이벤트 수가 초과되더라도 다른 이벤트와 함께 필터링되지 않습니다. (#11520)

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
* DevExpress text controls 를 열 때 NVDA 오류 효과음이 들리는 버그가 수정됐습니다. (#10918)시스템 트레이에서 아이콘의 이름과 툴팁 내용이 같을 경우, 이름을 두 번 알리지 않기 위해서 이제 툴팁을 읽지 않습니다. (#6656)
* 시스템 트레이에 있는 아이콘의 텍스트가 아이콘의 이름과 같으면 키보드 탐색 시 중복 알림을 피하기 위해 툴팁이 더 이상 보고되지 않습니다. (#6656)
* 브라우즈 모드에서 자동으로 시스템 포커스 이동 옵션이 비활성화되어 있을 경우, NVDA+Space 키를 눌러 포커스 모드로 바꾸면 캐럿 아래에 있는 요소를 포커스합니다. (#11206)
* 일부 시스템에서 NVDA 업데이트를 다시 확인할 수 있게 됐습니다. (예: 초기 설치된 윈도우즈) (#11253)
* 자바 어플리케이션의 포커스되지 않은 트리, 테이블, 목록 등에서 선택항목이 바뀔 때 포커스가 바뀌는 문제가 수정됐습니다. (#5989)

### 개발 변경사항

* `execElevated`와 `hasUiAccess`가 `config` 모듈에서 `systemUtils` 모듈로 이동되었습니다. `config` 모듈을 통한 사용은 지원 종료 예정입니다. (#10493)
* `configobj`가 5.1.0dev commit f9a265c4로 업데이트되었습니다. (#10939)
* 이제 Chrome과 HTML 샘플을 사용하여 NVDA의 자동화된 테스트가 가능합니다. (#10553)
* `IAccessibleHandler`가 패키지로 변환되었으며, `OrderedWinEventLimiter`가 별도의 모듈로 분리되고 단위 테스트가 추가되었습니다. (#10934)
* `BrlApi`가 0.8 버전(BRLTTY 6.1)으로 업데이트되었습니다. (#11065)
* 상태 표시줄의 텍스트를 가져오는 방식이 이제 `AppModule`에서 사용자 정의될 수 있습니다. (#2125, #4640)
* NVDA는 더 이상 `IAccessible EVENT_OBJECT_REORDER` 이벤트를 수신하지 않습니다. (#11076)
* 잘못된 `ScriptableObject`(예: 기본 클래스의 `init` 메서드 호출이 누락된 `GlobalPlugin`)가 NVDA의 스크립트 처리를 중단시키지 않습니다. (#5446)

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

### 개발 변경사항

* 개발자 문서는 이제 Sphinx를 사용하여 빌드됩니다. (#9840)
* 여러 음성 함수가 두 개로 분리되었습니다. (#10593)
  speakX 버전은 유지되지만, 이제 음성 시퀀스를 반환하는 getXSpeech 함수에 의존합니다.
  * speakObjectProperties는 이제 getObjectPropertiesSpeech에 의존합니다.
  * speakObject는 이제 getObjectSpeech에 의존합니다.
  * speakTextInfo는 이제 getTextInfoSpeech에 의존합니다.
  * speakWithoutPauses는 클래스 형태로 변환되고 리팩토링되었지만, 호환성에는 영향을 주지 않습니다.
  * getSpeechForSpelling은 지원 종료 예정이며, 대신 getSpellingSpeech를 사용하세요.
  내부적으로 변경된 사항으로 추가기능 개발자에게 영향을 주지 않습니다:
  * _speakPlaceholderIfEmpty는 이제 _getPlaceholderSpeechIfTextEmpty로 변경되었습니다.
  * _speakTextInfo_addMath는 이제 _extendSpeechSequence_addMathForTextInfo로 변경되었습니다.
* 음성 'reason'은 Enum으로 변환되었습니다. controlTypes.OutputReason 클래스를 참조하세요. (#10703)
  * 모듈 수준의 'REASON_*' 상수는 지원 종료 예정입니다.
* NVDA 종속성을 컴파일하려면 이제 Visual Studio 2019 (16.2 이상)가 필요합니다. (#10169)
* SCons가 버전 3.1.1로 업데이트되었습니다. (#10169)
* behaviors._FakeTableCell이 위치를 정의하지 않아도 다시 허용됩니다. (#10864)

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

### 개발 변경사항

* Python을 3.7 버전으로 업데이트했습니다. (#7105)
* pySerial을 3.4 버전으로 업데이트했습니다. (#8815)
* wxPython을 4.0.3 버전으로 업데이트하여 Python 3.5 이상을 지원합니다. (#9630)
* six를 1.12.0 버전으로 업데이트했습니다. (#9630)
* py2exe를 0.9.3.2 버전(개발 중, albertosottile/py2exe#13의 commit b372a8e)으로 업데이트했습니다. (#9856)
* UIAutomationCore.dll comtypes 모듈을 10.0.18362 버전으로 업데이트했습니다. (#9829)
* Python 콘솔의 탭 자동 완성 기능은 이제 밑줄로 시작하는 속성을 제안하려면 밑줄을 먼저 입력해야 합니다. (#9918)
* Flake8 린팅 도구가 SCons에 통합되어 Pull Request의 코드 요구 사항을 반영합니다. (#5918)
* NVDA가 더 이상 pyWin32에 의존하지 않으므로, 추가기능에서 win32api 및 win32con 모듈을 사용할 수 없습니다. (#9639)
  * win32api 호출은 ctypes를 사용하여 win32 DLL 함수에 직접 호출로 대체할 수 있습니다.
  * win32con 상수는 파일 내에서 정의해야 합니다.
* nvwave.playWaveFile의 "async" 인수가 "asynchronous"로 이름이 변경되었습니다. (#8607)
* synthDriver 객체의 speakText 및 speakCharacter 메서드는 더 이상 지원되지 않습니다.
  * 이 기능은 SynthDriver.speak에서 처리됩니다.
* synthDriverHandler의 SynthSetting 클래스가 제거되었습니다. 이제 driverHandler.DriverSetting 클래스를 사용하세요.
* SynthDriver 클래스는 더 이상 lastIndex 속성을 통해 인덱스를 노출하지 않아야 합니다.
  * 대신, 모든 이전 오디오가 해당 인덱스 이전에 재생을 완료한 후 synthDriverHandler.synthIndexReached 작업에 인덱스를 알리세요.
* SynthDriver 클래스는 SynthDriver.speak 호출에서 모든 오디오가 재생을 완료한 후 synthDriverHandler.synthDoneSpeaking 작업을 지원해야 합니다.
* SynthDriver 클래스는 speak 메서드에서 speech.PitchCommand를 지원해야 하며, 이제 철자 읽기에서 음조 변경은 이 기능에 의존합니다.
* speech 함수 getSpeechTextForProperties가 getPropertiesSpeech로 이름이 변경되었습니다. (#10098)
* braille 함수 getBrailleTextForProperties가 getPropertiesBraille로 이름이 변경되었습니다. (#10469)
* 여러 speech 함수가 이제 음성 시퀀스를 반환하도록 변경되었습니다. (#10098)
  * getControlFieldSpeech
  * getFormatFieldSpeech
  * getSpeechTextForProperties (이제 getPropertiesSpeech로 이름 변경)
  * getIndentationSpeech
  * getTableInfoSpeech
* Python 3 문자열과 Windows 유니코드 문자열 간의 차이를 단순화하기 위해 textUtils 모듈을 추가했습니다. (#9545)
  * 모듈 문서와 textInfos.offsets 모듈에서 구현 예제를 참조하세요.
* 지원 종료 예정 기능이 제거되었습니다. (#9548)
  * 제거된 AppModules:
    * Windows XP 사운드 레코더.
    * Klango Player, 더 이상 유지보수되지 않는 소프트웨어.
  * configobj.validate 래퍼가 제거되었습니다.
    * 새로운 코드는 import validate 대신 from configobj import validate를 사용해야 합니다.
  * textInfos.Point와 textInfos.Rect는 각각 locationHelper.Point와 locationHelper.RectLTRB로 대체되었습니다.
  * braille.BrailleHandler._get_tether와 braille.BrailleHandler.set_tether가 제거되었습니다.
  * config.getConfigDirs가 제거되었습니다.
  * config.ConfigManager.getConfigValidationParameter는 getConfigValidation으로 대체되었습니다.
  * inputCore.InputGesture.logIdentifier 속성이 제거되었습니다.
    * 대신 inputCore.InputGesture의 _get_identifiers를 사용하세요.
  * synthDriverHandler.SynthDriver.speakText/speakCharacter가 제거되었습니다.
  * 여러 synthDriverHandler.SynthSetting 클래스가 제거되었습니다.
    * 이전에는 하위 호환성을 위해 유지되었으나 (#8214), 이제는 더 이상 필요하지 않음으로 간주됩니다.
    * SynthSetting 클래스를 사용하던 드라이버는 DriverSetting 클래스를 사용하도록 업데이트해야 합니다.
  * 일부 레거시 코드가 제거되었습니다. 특히:
    * Outlook 2003 이전 메시지 목록에 대한 지원.
    * Windows Vista 및 이전 버전에서만 사용 가능한 클래식 시작 메뉴에 대한 오버레이 클래스.
    * Skype 7에 대한 지원이 중단되었습니다. 더 이상 작동하지 않기 때문입니다.
* 화면 콘텐츠를 변경할 수 있는 비전 향상 제공자를 생성하기 위한 프레임워크가 추가되었습니다. (#9064)
  * 추가기능은 visionEnhancementProviders 폴더에 자체 제공자를 포함할 수 있습니다.
  * 프레임워크와 예제 구현에 대한 자세한 내용은 vision 및 visionEnhancementProviders 모듈을 참조하세요.
  * 비전 향상 제공자는 NVDA 설정 대화상자의 '비전' 카테고리에서 활성화 및 구성할 수 있습니다.
* 추상 클래스 속성이 이제 baseObject.AutoPropertyObject를 상속받는 객체(NVDAObjects 및 TextInfos 등)에서 지원됩니다. (#10102)
* displayModel.UNIT_DISPLAYCHUNK이 DisplayModelTextInfo에 특정한 textInfos 단위 상수로 도입되었습니다. (#10165)
  * 이 새로운 상수는 DisplayModelTextInfo에서 텍스트를 기본 모델에 저장된 텍스트 청크와 더 유사하게 탐색할 수 있도록 합니다.
* displayModel.getCaretRect는 이제 locationHelper.RectLTRB의 인스턴스를 반환합니다. (#10233)
* UNIT_CONTROLFIELD와 UNIT_FORMATFIELD 상수는 virtualBuffers.VirtualBufferTextInfo에서 textInfos 패키지로 이동되었습니다. (#10396)
* NVDA 로그의 모든 항목에 대해, 해당 항목이 생성된 스레드에 대한 정보가 이제 포함됩니다. (#10259)
* UIA TextInfo 객체는 이제 페이지, 이야기(story), 그리고 formatField 텍스트 단위로 이동/확장할 수 있습니다. (#10396)
* 외부 모듈(appModules 및 globalPlugins)이 NVDAObjects의 생성을 방해할 가능성이 줄어들었습니다.
  * "chooseNVDAObjectOverlayClasses" 및 "event_NVDAObject_init" 메서드로 인해 발생한 예외가 이제 적절히 포착되고 로그에 기록됩니다.
* aria.htmlNodeNameToAriaLandmarkRoles 사전이 aria.htmlNodeNameToAriaRoles로 이름이 변경되었습니다. 이제 랜드마크가 아닌 역할도 포함합니다.
* scriptHandler.isCurrentScript는 사용 사례 부족으로 제거되었습니다. 대체 항목은 없습니다. (#8677)

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

### 개발 변경사항

* 이제 애플리케이션 모듈에서 "disableBrowseModeByDefault" 속성을 설정하여 기본적으로 브라우즈 모드를 비활성화할 수 있습니다. (#8846)
* 창의 확장된 창 스타일이 이제 Window 객체 및 그 파생 객체의 `extendedWindowStyle` 속성을 통해 노출됩니다. (#9136)
* comtypes 패키지가 1.1.7로 업데이트되었습니다. (#9440, #8522)
* 모듈 정보 알림 명령을 사용할 때, 정보의 순서가 변경되어 모듈이 먼저 표시됩니다. (#7338)
* C#에서 nvdaControllerClient.dll을 사용하는 예제가 추가되었습니다. (#9600)
* winVersion 모듈에 새로운 isWin10 함수가 추가되어 NVDA가 실행 중인 Windows 10의 릴리스 버전(예: 1903) 이상인지 여부를 반환합니다. (#9761)
* NVDA Python 콘솔에 이제 더 유용한 모듈들(예: appModules, globalPlugins, config, textInfos)이 네임스페이스에 포함됩니다. (#9789)
* NVDA Python 콘솔에서 마지막으로 실행된 명령의 결과를 이제 _ (라인) 변수에서 접근할 수 있습니다. (#9782)
  * 이 변수는 gettext 번역 함수 "_"와 이름이 겹칩니다. 번역 함수에 접근하려면: del _

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
  * 개발중인 코드를 테스트해야하는 개발자의 경우 NVDA 설정의 고급 카테고리에서 NVDA의 개발자 스크래치 패드 디렉토리 옵션을 활성화해야 합니다. 이 옵션이 활성화되면 NVDA 사용자 환경 설정 디렉토리에 있는 '스크래치 패드'디렉토리에 개발 중인 코드를 복사해야 합니다.

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

### 개발 변경사항

* 이제 Microsoft Visual Studio 2017의 모든 에디션(Community 에디션뿐만 아니라)으로 NVDA를 빌드할 수 있습니다. (#8939)
* NVDA 설정의 debugLogging 섹션에서 louis 플래그를 활성화하여 liblouis의 로그 출력을 NVDA 로그에 포함할 수 있습니다. (#4554)
* 추가기능 제작자는 이제 추가기능 매니페스트에 NVDA 버전 호환성 정보를 제공할 수 있습니다. (#6275, #9055)
  * minimumNVDAVersion: 추가기능이 제대로 작동하기 위해 필요한 NVDA의 최소 버전.
  * lastTestedNVDAVersion: 추가기능이 테스트된 NVDA의 마지막 버전.
* OffsetsTextInfo 객체는 이제 _getBoundingRectFromOffset 메서드를 구현하여 문자 단위로 경계 사각형을 검색할 수 있습니다. (#8572)
* TextInfo 객체에 boundingRect 속성이 추가되어 텍스트 범위의 경계 사각형을 검색할 수 있습니다. (#8371)
* 클래스 내 속성과 메서드는 이제 NVDA에서 추상으로 표시할 수 있습니다. 이러한 클래스는 인스턴스화될 경우 오류를 발생시킵니다. (#8294, #8652, #8658)
* NVDA는 텍스트가 발화될 때 입력 이후 경과 시간을 로그에 기록할 수 있습니다. 이는 인식된 응답성을 측정하는 데 도움이 됩니다. NVDA 설정의 debugLog 섹션에서 timeSinceInput 설정을 True로 설정하여 활성화할 수 있습니다. (#9167)

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
* 키보드 설정에서 NVDA 보조 키 체크박스들을 하나의 목록으로 통합함.
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

### 개발 변경사항

* gui.nvdaControls에는 이제 체크박스가 있는 접근 가능한 리스트를 생성하기 위한 두 개의 클래스가 포함되어 있습니다. (#7325)
  * CustomCheckListBox는 wx.CheckListBox의 접근 가능한 서브클래스입니다.
  * AutoWidthColumnCheckListCtrl은 wx.ListCtrl을 기반으로 한 AutoWidthColumnListCtrl에 접근 가능한 체크박스를 추가합니다.
* 이미 접근 가능하지 않은 wx 위젯을 접근 가능하게 만들어야 하는 경우, gui.accPropServer.IAccPropServer_impl 인스턴스를 사용하여 이를 수행할 수 있습니다. (#7491)
  * 자세한 내용은 gui.nvdaControls.ListCtrlAccPropServer의 구현을 참조하세요.
* configobj가 5.1.0dev commit 5b5de48a로 업데이트되었습니다. (#4470)
* config.post_configProfileSwitch 작업은 이제 선택적인 prevConf 키워드 인수를 받아, 프로파일 전환 전후의 설정 차이에 따라 작업을 수행할 수 있도록 합니다. (#8758)

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

### 개발 변경사항

* scriptHandler.script가 추가되었으며, 이는 스크립트 가능한 객체에서 스크립트에 데코레이터로 사용할 수 있습니다. (#6266)
* NVDA를 위한 시스템 테스트 프레임워크가 도입되었습니다. (#708)
* hwPortUtils 모듈에 몇 가지 변경 사항이 추가되었습니다: (#1271)
  * listUsbDevices는 이제 hardwareID와 devicePath를 포함한 장치 정보를 담은 사전을 반환합니다.
  * listComPorts에서 반환되는 사전은 이제 USB VID/PID 정보가 hardware ID에 포함된 COM 포트에 대해 usbID 항목도 포함합니다.
* wxPython이 4.0.3으로 업데이트되었습니다. (#7077)
* NVDA가 이제 Windows 7 SP1 이상만 지원하므로, 특정 Windows 릴리스에서 UIA를 활성화할지 확인하는 데 사용되던 "minWindowsVersion" 키가 제거되었습니다. (#8422)
* 설정 저장/초기화 작업에 대해 알림을 받을 수 있도록 새로운 config.pre_configSave, config.post_configSave, config.pre_configReset, config.post_configReset 작업이 추가되었습니다. (#7598)
  * config.pre_configSave는 NVDA의 설정이 저장되기 직전에 알림을 받을 때 사용되며, config.post_configSave는 설정이 저장된 후 호출됩니다.
  * config.pre_configReset과 config.post_configReset은 설정이 디스크에서 다시 로드되는지(false) 또는 기본값으로 재설정되는지(true)를 지정하는 factory defaults 플래그를 포함합니다.
* config.configProfileSwitch가 config.post_configProfileSwitch로 이름이 변경되어 프로파일 전환이 완료된 후 호출된다는 점을 반영합니다. (#7598)
* UI Automation 인터페이스가 Windows 10 October 2018 Update 및 Server 2019(IUIAutomation6 / IUIAutomationElement9)로 업데이트되었습니다. (#8473)

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

### 개발 변경사항

* UIA 객체의 개발자 정보에 이제 사용 가능한 UIA 패턴 목록이 포함됩니다. (#5712)
* 응용 프로그램 모듈에서 isGoodUIAWindow 메서드를 구현하여 특정 창이 항상 UIA를 사용하도록 강제할 수 있습니다. (#7961)
* 설정의 점자 섹션에 있던 숨겨진 불리언 플래그 "outputPass1Only"가 다시 제거되었습니다. Liblouis는 더 이상 1단계 출력만을 지원하지 않습니다. (#7839)

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

### 개발 변경사항

* 점자 설정 섹션에 숨겨진 불리언 플래그 "outputPass1Only"가 추가되었습니다. (#7301, #7693, #7702)
  * 이 플래그는 기본값으로 true로 설정됩니다. false로 설정하면 liblouis 다중 패스 규칙이 점자 출력에 사용됩니다.
* 사용자가 기존 드라이버에서 새로운 드라이버로 원활히 전환할 수 있도록 돕는 사전(braille.RENAMED_DRIVERS)이 추가되었습니다. (#7459)
* comtypes 패키지가 1.1.3 버전으로 업데이트되었습니다. (#7831)
* 점자 디스플레이가 확인/승인 패킷을 전송하는 경우를 처리하기 위한 일반적인 시스템이 braille.BrailleDisplayDriver에 구현되었습니다. handyTech 점자 디스플레이 드라이버를 예제로 참조하세요. (#7590, #7721)
* NVDA가 Windows Desktop Bridge Store 앱으로 실행 중인지 감지할 수 있는 새로운 "isAppX" 변수가 config 모듈에 추가되었습니다. (#7851)
* NVDAObjects나 browseMode와 같이 textInfo를 가진 문서 구현을 위해, 표 탐색 스크립트를 표준적으로 제공하는 새로운 documentBase.documentWithTableNavigation 클래스가 추가되었습니다. 표 탐색이 작동하려면 이 클래스에서 제공해야 하는 헬퍼 메서드를 참조하세요. (#7849)
* scons 배치 파일이 Python 3이 설치된 경우를 더 잘 처리하며, Python 2.7 32비트 버전을 명시적으로 실행하기 위해 런처를 사용합니다. (#7541)
* hwIo.Hid는 이제 기본값이 True인 추가 매개변수 exclusive를 받습니다. False로 설정하면 NVDA와 연결된 동안 다른 응용 프로그램도 장치와 통신할 수 있습니다. (#7859)

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

### 개발 변경사항

* "scons tests" 명령은 이제 번역 가능한 문자열에 번역자 주석이 있는지 확인합니다. 이 작업만 별도로 실행하려면 "scons checkPot" 명령을 사용할 수 있습니다. (#7492)
* 새로운 extensionPoints 모듈이 추가되어 코드의 특정 지점에서 확장성을 제공하는 일반적인 프레임워크를 제공합니다. 이를 통해 관심 있는 사용자가 특정 작업이 발생할 때 알림을 받을 수 있도록 등록(extensionPoints.Action)하거나, 특정 유형의 데이터를 수정(extensionPoints.Filter)하거나, 어떤 작업이 수행될지 결정하는 데 참여(extensionPoints.Decider)할 수 있습니다. (#3393)
* config.configProfileSwitched Action을 통해 설정 프로파일 전환에 대한 알림을 받을 수 있도록 등록할 수 있습니다. (#3393)
* 시스템 키보드의 특수 키(예: control 및 alt)를 에뮬레이션하는 점자 디스플레이 제스처는 이제 명시적으로 정의하지 않아도 다른 에뮬레이션 키와 조합할 수 있습니다. (#6213)
  * 예를 들어, 디스플레이의 한 키가 alt 키에 매핑되고 다른 키가 아래쪽 화살표 키에 매핑된 경우, 이 두 키를 조합하면 alt+아래쪽 화살표 키를 에뮬레이션할 수 있습니다.
* braille.BrailleDisplayGesture 클래스에 새로운 model 속성이 추가되었습니다. 이 속성이 제공되면, 키를 누를 때 모델별로 특정한 추가 제스처 식별자가 생성됩니다. 이를 통해 특정 점자 디스플레이 모델에 제한된 제스처를 사용자 정의할 수 있습니다.
  * 이 새로운 기능에 대한 예시는 baum 드라이버를 참조하세요.
* NVDA는 이제 Visual Studio 2017과 Windows 10 SDK를 사용하여 컴파일됩니다. (#7568)

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

### 개발 변경사항

* 로그의 타임스탬프에 밀리초가 포함되도록 변경되었습니다. (#7163)
* 이제 NVDA는 Visual Studio Community 2015로 빌드해야 합니다. Visual Studio Express는 더 이상 지원되지 않습니다. (#7110)
  * Windows 10 도구 및 SDK가 이제 필요하며, Visual Studio 설치 시 활성화할 수 있습니다.
  * 추가 세부 정보는 readme 파일의 설치된 종속성 섹션을 참조하세요.
* OCR 및 이미지 설명 도구와 같은 콘텐츠 인식 도구에 대한 지원이 contentRecog 패키지를 사용하여 쉽게 구현될 수 있습니다. (#7361)
* Python json 패키지가 이제 NVDA 바이너리 빌드에 포함됩니다. (#3050)

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
* 모질라 FireFox와 같은 Gecko 기반 프로그램에서 멀티프로세스 기능 사용 시 NVDA가 다운되던 문제 수정. (#6885)
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

### 개발 변경사항

* 명령줄 인수가 이제 Python의 argparse 모듈로 처리됩니다. optparse 대신 argparse를 사용하여 -r 및 -q와 같은 특정 옵션을 독점적으로 처리할 수 있습니다. (#6865)
* core.callLater는 이제 지정된 지연 시간 후에 콜백을 NVDA의 메인 큐에 대기시킵니다. 이전에는 콜백을 직접 실행했으나, 이제는 메시지 박스 표시와 같은 모달 호출 중간에 core가 실수로 대기 상태로 전환되는 것을 방지하여 잠재적인 멈춤 현상을 방지합니다. (#6797)
* InputGesture.identifiers 속성은 더 이상 정규화되지 않습니다. (#6945)
  * 서브클래스는 이 속성에서 반환하기 전에 식별자를 정규화할 필요가 없습니다.
  * 정규화된 식별자가 필요한 경우, identifiers 속성에서 반환된 식별자를 정규화하는 InputGesture.normalizedIdentifiers 속성을 사용할 수 있습니다.
* InputGesture.logIdentifier 속성은 이제 지원 종료 예정입니다. 호출자는 InputGesture.identifiers[0]을 대신 사용해야 합니다. (#6945)
* 일부 지원 종료 예정 코드를 제거했습니다:
  * `speech.REASON_*` 상수: 대신 `controlTypes.REASON_*`을 사용해야 합니다. (#6846)
  * 음성 엔진 설정의 `i18nName`: 대신 `displayName` 및 `displayNameWithAccelerator`을 사용해야 합니다. (#6846, #5185)
  * `config.validateConfig`. (#6846, #667)
  * `config.save`: 대신 `config.conf.save`를 사용해야 합니다. (#6846, #667)
* Python 콘솔의 자동 완성 컨텍스트 메뉴에 있는 완성 목록에서 더 이상 최종 심볼까지의 객체 경로가 표시되지 않습니다. (#7023)
* NVDA에 대한 단위 테스트 프레임워크가 추가되었습니다. (#7026)
  * 단위 테스트와 관련 인프라는 tests/unit 디렉터리에 있습니다. 자세한 내용은 tests\unit\init.py 파일의 docstring을 참조하세요.
  * "scons tests" 명령을 사용하여 테스트를 실행할 수 있습니다. 자세한 내용은 readme.md의 "테스트 실행" 섹션을 참조하세요.
  * NVDA에 대한 풀 리퀘스트를 제출하기 전에 테스트를 실행하고 통과했는지 확인해야 합니다.

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

### 개발 변경사항

* 프로필 및 설정 파일이 스키마 수정 요구 사항을 충족하도록 자동으로 업그레이드됩니다. 업그레이드 중 오류가 발생하면 알림이 표시되고, 설정이 초기화되며, 이전 설정 파일은 NVDA 로그의 '정보' 수준에서 확인할 수 있습니다. (#6470)

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

### 개발 변경사항

* 이제 이름에 점(.)이 포함된 실행 파일에 대한 응용 프로그램 모듈을 제공할 수 있습니다. 점은 밑줄(_)로 대체됩니다. (#5323)
* 새로운 gui.guiHelper 모듈에는 wxPython GUI 생성을 단순화하기 위한 유틸리티가 포함되어 있습니다. 여기에는 간격 관리를 자동화하는 기능이 포함됩니다. 이를 통해 시각적 외형과 일관성이 개선되고, 시각장애인 개발자가 새로운 GUI를 더 쉽게 생성할 수 있습니다. (#6287)

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

### 개발 변경사항

* 속성에서 직접 로그 정보를 기록할 때, 더 이상 해당 속성이 재귀적으로 계속 호출되지 않습니다. (#6122)

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

### 개발 변경사항

* NVDA의 C++ 구성 요소는 이제 Microsoft Visual Studio 2015로 빌드됩니다. (#5592)
* ui.browseableMessage를 사용하여 브라우즈 모드에서 사용자에게 텍스트 또는 HTML 메시지를 표시할 수 있습니다. (#4908)
* 사용자 설명서에서 <!-KC:setting 명령이 모든 키보드 레이아웃에 공통된 키를 가진 설정에 사용될 때, 키는 일반 콜론(:)뿐만 아니라 전각 콜론(：) 뒤에 배치될 수 있습니다. (#5739) -->

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

### 개발 변경사항

* 새로운 `audioDucking.AudioDucker` 클래스는 오디오를 출력하는 코드가 배경 오디오를 낮춰야 할 때 이를 알릴 수 있도록 합니다. (#3830)
* `nvwave.WavePlayer`의 생성자에 `wantDucking`이라는 키워드 인수가 추가되었습니다. 이 인수는 오디오가 재생되는 동안 배경 오디오를 낮출지 여부를 지정합니다. (#3830)
  * 이 기능이 활성화된 경우(기본값), 적절한 시점에 `WavePlayer.idle`을 호출하는 것이 필수적입니다.
* 점자 디스플레이를 위한 향상된 I/O: (#5609)
  * 스레드 안전한 점자 디스플레이 드라이버는 `BrailleDisplayDriver.isThreadSafe` 속성을 사용하여 자신을 스레드 안전하다고 선언할 수 있습니다. 드라이버가 아래의 기능을 활용하려면 스레드 안전해야 합니다.
  * 스레드 안전한 점자 디스플레이 드라이버에 데이터가 백그라운드에서 쓰여 성능이 향상됩니다.
  * `hwIo.Serial`은 드라이버가 폴링하지 않고 데이터가 수신될 때 호출 가능한 객체를 호출하도록 pyserial을 확장합니다.
  * `hwIo.Hid`는 USB HID를 통해 통신하는 점자 디스플레이를 지원합니다.
  * `hwPortUtils`와 `hwIo`는 발견된 장치와 전송 및 수신된 모든 데이터를 포함한 자세한 디버그 로깅을 선택적으로 제공합니다.
* 터치스크린 제스처에서 접근 가능한 몇 가지 새로운 속성이 추가되었습니다: (#5652)
  * `MultitouchTracker` 객체는 이제 `childTrackers` 속성을 포함하며, 이는 해당 트래커를 구성한 `MultiTouchTrackers`를 포함합니다. 예를 들어, 두 손가락 더블 탭은 두 개의 두 손가락 탭에 대한 하위 트래커를 가집니다. 두 손가락 탭 자체는 두 개의 탭에 대한 하위 트래커를 가집니다.
  * `MultiTouchTracker` 객체는 이제 `rawSingleTouchTracker` 속성도 포함하며, 이 속성은 하나의 손가락으로 탭, 플릭 또는 호버를 수행한 결과인 경우에 해당합니다. `SingleTouchTracker`는 운영 체제에서 손가락에 할당된 기본 ID와 현재 손가락이 여전히 접촉 중인지 여부에 접근할 수 있도록 합니다.
  * `TouchInputGestures`는 이제 `x`와 `y` 속성을 가지며, 간단한 경우에 트래커에 접근할 필요를 제거합니다.
  * `TouchInputGestures`는 이제 `preheldTracker` 속성을 포함하며, 이는 이 동작이 수행되는 동안 유지된 다른 손가락을 나타내는 `MultitouchTracker` 객체입니다.
* 두 가지 새로운 터치스크린 제스처가 추가되었습니다: (#5652)
  * 복수 탭 및 홀드(예: 두 손가락 탭 및 홀드)
  * 홀드에 대한 손가락 수가 제거된 일반화된 식별자(예: `1finger_hold+hover` 대신 `hold+hover`).

## 2015.4

이번 버전의 주 기능들: 윈도우 10 지원 향상; 윈도우 8 이상 접근성 센터내 NVDA 추가; 엑셀 지원 향상(sheet 목록 및 이름 변경과 잠겨진 셀로 이동 가능); 모질라 FireFox, 구글 Chrome 및 모질라 썬더버드에서의 rich text 편집 지원 향상 등입니다.

### 새로운 기능

* 윈도우 8이상 사용 시 NVDA가 접근성 센터에 표시되도록 함. (#308)
* Microsoft Excel에서 셀을 옮길때 문서 서식 설정에서 활성화된 서식 정보가 출력되도록 함. (#4878)
* 문서 서식 설정에 "강조 텍스트 알림" 설정(기본적으로 선택되어 있음)을 추가하여 문서내 강조된 텍스트를 자동으로 출력하도록 함(현재인터넷 익스플로러와 같은 MSHTML 컨트롤에서 브라우즈 모드 사용 시 em 또는 strong 텍스트에서만 적용됨). (#4920)
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
    1. 1. 일반 설정을 호출합니다.
    1. 1. 윈도우 로그인 후 NvDA 자동 시작 설정을 해제합니다.
    1. 1. 확인 버튼을 선택합니다.
    1. 1. 일반 설정을 다시 호출합니다.
    1. 1. 윈도우 로그인 후 NvDA 자동 시작 설정을 선택합니다.
    1. 1. 확인 버튼을 선택합니다.
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

### 개발 변경사항

* 이제 Windows에서 기본적으로 처리되지 않는 시스템 키보드(예: 점자 디스플레이의 QWERTY 키보드)에서 원시 입력을 주입할 수 있는 새로운 keyboardHandler.injectRawKeyboardInput 함수가 추가되었습니다. (#4576)
* eventHandler.requestEvents가 추가되어 기본적으로 차단된 특정 이벤트를 요청할 수 있습니다. 예를 들어, 특정 컨트롤에서의 표시 이벤트나 백그라운드 상태에서도 특정 이벤트를 요청할 수 있습니다. (#3831)
* synthDriverHandler.SynthSetting에 단일 i18nName 속성 대신 displayNameWithAccelerator와 displayName 속성이 분리되어 추가되었습니다. 이를 통해 일부 언어에서 음성 설정 링에서 단축키가 알림되지 않도록 할 수 있습니다.
  * 이전 버전과의 호환성을 위해 생성자에서 displayName은 선택 사항이며, 제공되지 않을 경우 displayNameWithAccelerator에서 파생됩니다. 그러나 설정에 단축키를 포함하려는 경우 두 속성을 모두 제공해야 합니다.
  * i18nName 속성은 지원 종료 예정이며, 향후 릴리스에서 제거될 수 있습니다.

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

### 개발 변경사항

* brailleInput.handler.sendChars(mychar)는 이전 문자와 동일한 문자가 입력될 경우 이를 필터링하지 않도록 수정되었습니다. 이제 키가 올바르게 해제되었는지 확인합니다. (#4139)
* 터치 모드를 변경하는 스크립트는 touchHandler.touchModeLabels에 새로 추가된 레이블을 준수하도록 수정되었습니다. (#4699)
* 추가기능은 자체적인 수학 표현 구현을 제공할 수 있습니다. 자세한 내용은 mathPres 패키지를 참조하세요. (#4509)
* 음성 명령이 구현되어 단어 사이에 휴지(break)를 삽입하거나 음높이, 볼륨, 속도를 변경할 수 있습니다. 자세한 내용은 speech 모듈의 BreakCommand, PitchCommand, VolumeCommand, RateCommand를 참조하세요. (#4674)
  * 또한 speech.PhonemeCommand를 사용하여 특정 발음을 삽입할 수 있지만, 현재 구현은 매우 제한된 수의 음소만 지원합니다.

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

### 개발 변경사항

* wxPython을 3.0.2.0 버전으로 업데이트했습니다. (#3763)
* Python을 2.7.9 버전으로 업데이트했습니다. (#4715)
* 추가기능의 installTasks 모듈에서 speechDictHandler를 가져오는 경우, 해당 추가기능을 제거하거나 업데이트한 후 NVDA를 재시작할 때 더 이상 NVDA가 충돌하지 않습니다. (#4496)

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

### 개발 변경사항

* 여러 응용 프로그램을 호스팅하는 실행 파일(e.g. javaw.exe)의 경우, 이제 모든 호스팅된 응용 프로그램에 동일한 앱 모듈을 로드하는 대신 각 응용 프로그램에 대해 특정 앱 모듈을 로드할 수 있는 코드를 제공할 수 있습니다. (#4360)
  * 자세한 내용은 appModuleHandler.AppModule의 코드 문서를 참조하세요.
  * javaw.exe에 대한 지원이 구현되었습니다.

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
 표의 첫 머릿말 셀에서 열 머릿말(NVDA+Shift+C)과 행 머릿말(NVDA+Shift+R) 지정 명령을 사용하여 행 및 열 머릿말을 지정했을때 본 값이  문서에 저장되어 후에 문서를 불러올때 적용됨. 또한 타 스크린 리더가 워드 책갈피 기능 지원시 이를 사용할 수 있음.
* Microsoft Word에서 탭을 누를때 페이지 좌측 가장자리로부터의 간격을 알리도록 함. (#1353)
* Microsoft Word 사용 시 여러 서식(굵게 쓰기, 이태릭, 밑줄, 표시, outline 레벨 등) 변환 명령이 음성과 점자로 출력되도록 함. (#1353)
* Microsoft Excel에서 현재 셀에 주석이 존재하는 경우 NvDA+Alt+C를 눌러 주석을 확인할 수 ㅣㅇㅆ음. (#2920)
* Microsoft Excel에서 Shift+F2를 눌러 주석 편    모드를 선택한 후 NVDA가 제공하는 주석 편집 대화상자를 통해 포커스된 셀에 주석을 삽입할 수 있음. (#2920)
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

### 개발 변경사항

* NVDA는 이제 추가기능 문서를 통합적으로 지원합니다. 자세한 내용은 개발자 가이드의 추가기능 문서 섹션을 참조하세요. (#2694)
* ScriptableObject에서 __gestures를 통해 제스처 바인딩을 제공할 때, 이제 None 키워드를 스크립트로 제공할 수 있습니다. 이를 통해 상위 클래스에서 제스처를 바인딩 해제할 수 있습니다. (#4240)
* 특정 로케일에서 NVDA 시작에 사용하는 바로 가기 키가 문제를 일으킬 경우, 이를 변경할 수 있습니다. (#2209)
  * 이는 gettext를 통해 이루어집니다.
  * NVDA 설치 대화상자의 "바탕 화면 바로 가기 만들기" 옵션 텍스트와 사용자 설명서의 바로 가기 키도 업데이트되어야 합니다.

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

### 개발 변경사항

* AppModules에는 이제 productName 및 productVersion 속성이 포함됩니다. 이 정보는 이제 개발자 정보(NVDA+f1)에도 포함됩니다. (#1625)
* Python 콘솔에서 이제 Tab 키를 눌러 현재 식별자를 자동 완성할 수 있습니다. (#433)
  * 가능한 항목이 여러 개인 경우, Tab 키를 한 번 더 눌러 목록에서 선택할 수 있습니다.

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
* 키보드 설정에서 NVDA 보조 키 설정이 모두 해제된 경우 이에 대한 오류 메시지가 뜨도록 함 (기능키를 최소한 하나 이상 설정 바람). (#2871)
* Microsoft Excel에서 다중 선택된 셀과 통합된 셀이 다르게 출력되도록 함. (#3567)
* 브라우즈 모드 사용 시 웹사이트에 표시된 대화상자나 앱에서 빠져나갈때 커서 위치가 다른 곳에 위치하던 문제 수정. (#3145)
* 특정 시스템에서 휴멍웨어 Brailliant B/BI 디스플레이가 USB로 연결되었음에도 NVDA가 인식하지 않던 문제 수정.
* 탐색 객체가 화면(위치)에 존재하지 않을때 화면 탐색 모드로 전환되지 못하는 문제 수정 (이때 리뷰 커서는 화면 상단에 ㅜ이치하게 됨). (#3454)
* 특정 시스템에서 Freedom Scientific 디스플레이가 USB로 연결되었음에도 NVDA가 인식하지 않던 문제 수정. (#3509, #3662)
* Freedom Scientific 디스플레이 사용 시 여러 키들이 동작하지 않던 문제 수정. (#3401, #3662)

### 개발 변경사항

* AppModules에는 이제 productName 및 productVersion 속성이 포함됩니다. 이 정보는 이제 개발자 정보(NVDA+f1)에도 포함됩니다. (#1625)
* Python 콘솔에서 이제 Tab 키를 눌러 현재 식별자를 자동 완성할 수 있습니다. (#433)
* 가능한 항목이 여러 개인 경우, Tab 키를 한 번 더 눌러 목록에서 선택할 수 있습니다.

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

### 개발 변경사항

* `windowUtils.findDescendantWindow` 함수가 추가되어 지정된 가시성, 컨트롤 ID 및/또는 클래스 이름과 일치하는 하위 창(HWND)을 검색할 수 있습니다.
* 원격 Python 콘솔이 입력을 기다리는 동안 10초 후에 더 이상 시간 초과되지 않습니다. (#3126)
* 바이너리 빌드에서 `bisect` 모듈의 포함은 지원 종료 예정이며, 향후 릴리스에서 제거될 수 있습니다. (#3368)
  * `bisect` 모듈에 의존하는 추가기능(예: `urllib2` 모듈 포함)은 이 모듈을 포함하도록 업데이트해야 합니다.

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

| | 이름 |키||
|---|---|
||모두 읽기 |NVDA+a||
||현재 줄 읽기 |NVDA+l||
||현재 선택된 텍스트 읽기 |NVDA+shift+s||
||상태 표시줄 읽기 |NVDA+shift+end||

이 외 객체 탐색, 리뷰 커서, 마우스 조작 및 음성 설정 명령들이 변경되었습니다.
자세한 사항은 [간편 단축키 참고서](keyCommands.html) 문서를 참조하십시오.

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
* 사용자 경로에 다중 글자가 사용된 경우 NVDA가 설치되지 않던 문제 수정. (#2729)
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

### 개발 변경사항

* 점자 디스플레이 드라이버에서 수동 포트 선택을 지원할 수 있습니다. (#426)
  * 이는 레거시 시리얼 포트를 통해 연결을 지원하는 점자 디스플레이에 가장 유용합니다.
  * 이는 BrailleDisplayDriver 클래스의 getPossiblePorts 클래스 메서드를 사용하여 수행됩니다.
* 점자 키보드를 통한 점자 입력이 이제 지원됩니다. (#808)
  * 점자 입력은 brailleInput.BrailleInputGesture 클래스 또는 이를 상속받은 하위 클래스에 의해 처리됩니다.
  * braille.BrailleDisplayGesture의 하위 클래스(braille 디스플레이 드라이버에서 구현됨)도 brailleInput.BrailleInputGesture를 상속받을 수 있습니다. 이를 통해 디스플레이 명령과 점자 입력을 동일한 제스처 클래스에서 처리할 수 있습니다.
* NVDA가 UIAccess 권한으로 실행 중일 때, comHelper.getActiveObject를 사용하여 일반 프로세스에서 활성 COM 객체를 가져올 수 있습니다. (#2483)

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

### 변경사항

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

### 개발 변경사항

* 이전 로그 파일은 NVDA 초기화 시 nvda-old.log로 복사됩니다. 따라서 NVDA가 충돌하거나 재시작된 경우, 해당 세션의 로그 정보를 여전히 확인할 수 있습니다. (#916)
* chooseNVDAObjectOverlayClasses에서 role 속성을 가져오는 작업이 더 이상 특정 객체(예: Windows 명령 콘솔 및 Scintilla 컨트롤)에서 role이 잘못되거나 포커스 시 알리지 않는 문제를 발생시키지 않습니다. (#2569)
* NVDA 환경 설정, 도구 및 도움말 메뉴는 이제 gui.mainFrame.sysTrayIcon의 속성으로 각각 preferencesMenu, toolsMenu 및 helpMenu로 접근할 수 있습니다. 이를 통해 플러그인이 이러한 메뉴에 항목을 더 쉽게 추가할 수 있습니다.
* globalCommands의 navigatorObject_doDefaultAction 스크립트는 review_activate로 이름이 변경되었습니다.
* Gettext 메시지 컨텍스트가 이제 지원됩니다. 이를 통해 컨텍스트에 따라 단일 영어 메시지에 대해 여러 번역을 정의할 수 있습니다. (#1524)
  * 이는 pgettext(context, message) 함수를 사용하여 수행됩니다.
  * NVDA 자체와 추가기능 모두에서 지원됩니다.
  * PO 및 MO 파일을 생성하려면 GNU gettext의 xgettext 및 msgfmt를 사용해야 합니다. Python 도구는 메시지 컨텍스트를 지원하지 않습니다.
  * xgettext의 경우, --keyword=pgettext:1c,2 명령줄 인수를 전달하여 메시지 컨텍스트 포함을 활성화하십시오.
  * 자세한 내용은 http://www.gnu.org/software/gettext/manual/html_node/Contexts.html#Contexts 를 참조하십시오.
* 서드파티 모듈에 의해 재정의된 내장 NVDA 모듈에 접근할 수 있는 기능이 추가되었습니다. 자세한 내용은 nvdaBuiltin 모듈을 참조하십시오.
* 추가기능 번역 지원은 이제 추가기능의 installTasks 모듈 내에서도 사용할 수 있습니다. (#2715)

## 2012.2.1

이 릴리스는 몇 가지 잠재적인 보안 문제를 해결합니다(Python 버전 2.7.3 업데이트).

## 2012.2

이 릴리스의 주요 특징은 내장된 설치 및 휴대용 버전 생성 기능, 자동 업데이트, 새로운 NVDA 추가 기능의 간편한 관리, Microsoft Word에서 그래픽 알림, Windows 8 메트로 스타일 응용 프로그램 지원, 그리고 몇 가지 중요한 버그 수정입니다.

### 새로운 기능

* NVDA가 이제 자동으로 업데이트를 확인하고, 다운로드하며 설치할 수 있습니다. (#73)
* NVDA의 기능 확장이 더 쉬워졌습니다. NVDA 메뉴의 도구 항목 아래에 추가된 추가 기능 관리자(Add-ons Manager)를 통해 새로운 NVDA 추가 기능 패키지(.nvda-addon 파일)를 설치 및 제거할 수 있습니다. 이 추가 기능 관리자는 구성 디렉터리에 수동으로 복사된 이전의 사용자 정의 플러그인 및 드라이버는 표시하지 않습니다. (#213)
* NVDA의 많은 일반적인 기능들이 Windows 8 메트로 스타일 응용 프로그램에서도 작동합니다. 설치된 NVDA 릴리스를 사용할 경우, 입력한 문자 읽기 및 웹 문서에 대한 브라우즈 모드(메트로 버전의 Internet Explorer 10 포함)와 같은 기능을 사용할 수 있습니다. 그러나 휴대용 버전의 NVDA는 메트로 스타일 응용 프로그램에 접근할 수 없습니다. (#1801)
* 브라우즈 모드 문서(Internet Explorer, Firefox 등)에서 특정 포함 요소(예: 목록 및 표)의 시작 지점으로 이동하거나 끝을 넘어 이동할 수 있습니다. Shift+, 및 , 키를 각각 사용합니다. (#123)
* 새로운 언어: 그리스어.
* Microsoft Word 문서에서 그래픽과 대체 텍스트가 이제 알림됩니다. (#2282, #1541)

### 변경사항

* Microsoft Excel에서 셀 좌표 알림은 이제 내용 뒤에 위치하며, 문서 서식 설정 대화 상자에서 표 알림 및 표 셀 좌표 알림 설정이 활성화된 경우에만 포함됩니다. (#320)
* NVDA는 이제 하나의 패키지로 배포됩니다. 휴대용 및 설치 버전이 별도로 제공되지 않으며, 실행 시 임시 NVDA 복사본을 시작하고 설치하거나 휴대용 배포본을 생성할 수 있는 단일 파일로 제공됩니다. (#1715)
* NVDA는 이제 모든 시스템에서 항상 Program Files에 설치됩니다. 이전 설치를 업데이트하는 경우, 이전에 다른 위치에 설치되었더라도 자동으로 이동됩니다.

### 버그 수정내역

* 자동 언어 전환이 활성화된 경우, Mozilla Gecko(예: Firefox)에서 그래픽의 대체 텍스트 및 특정 컨트롤의 레이블과 같은 콘텐츠가 적절히 마크업되어 있다면 올바른 언어로 알립니다.
* BibleSeeker(및 기타 TRxRichEdit 컨트롤)에서 모두 읽기 명령을 사용할 때 더 이상 구절 중간에서 멈추지 않습니다.
* Windows 8 탐색기의 파일 속성(권한 탭) 및 Windows 8 Windows Update에서 발견된 목록이 이제 올바르게 읽힙니다.
* MS Word에서 문서에서 텍스트를 가져오는 데 2초 이상 걸릴 때(매우 긴 줄 또는 목차) 발생할 수 있는 멈춤 현상이 수정되었습니다. (#2191)
* 공백 뒤에 특정 구두점이 오는 경우 단어 경계 감지가 이제 올바르게 작동합니다. (#1656)
* Adobe Reader의 브라우즈 모드에서 빠른 탐색 및 요소 목록을 사용하여 레벨이 없는 제목으로 이동할 수 있습니다. (#2181)
* Winamp에서 재생 목록 편집기에서 다른 항목으로 이동할 때 점자가 이제 올바르게 업데이트됩니다. (#1912)
* 브라우즈 모드 문서에서 사용할 수 있는 요소 목록의 트리가 이제 각 요소의 텍스트를 표시하도록 적절히 크기가 조정됩니다. (#2276)
* Java Access Bridge를 사용하는 응용 프로그램에서 편집 가능한 텍스트 필드가 이제 점자로 올바르게 표시됩니다. (#2284)
* Java Access Bridge를 사용하는 응용 프로그램에서 특정 상황에서 편집 가능한 텍스트 필드가 이상한 문자를 보고하지 않습니다. (#1892)
* Java Access Bridge를 사용하는 응용 프로그램에서 편집 가능한 텍스트 필드의 끝에 있을 때 현재 줄이 이제 올바르게 알립니다. (#1892)
* Mozilla Gecko 14 이상(예: Firefox 14)을 사용하는 응용 프로그램의 브라우즈 모드에서 빠른 탐색이 이제 인용 블록 및 임베디드 객체에 대해 작동합니다. (#2287)
* Internet Explorer 9에서 특정 랜드마크나 포커스 가능한 요소(특히 포커스 가능한 div 요소 또는 ARIA 랜드마크 역할이 있는 요소) 내부로 포커스가 이동할 때 NVDA가 원치 않는 콘텐츠를 더 이상 읽지 않습니다.
* NVDA 데스크탑 및 시작 메뉴 바로 가기의 NVDA 아이콘이 이제 64비트 Windows 에디션에서 올바르게 표시됩니다. (#354)

### 개발 변경사항

* 이전 NSIS 설치 관리자가 Python으로 작성된 내장 설치 관리자로 대체됨에 따라, 번역자가 설치 관리자용 langstrings.txt 파일을 유지할 필요가 없어졌습니다. 모든 로컬라이제이션 문자열은 이제 gettext po 파일로 관리됩니다.

## 2012.1

이 릴리스의 주요 내용으로는 점자를 더 유창하게 읽을 수 있는 기능, 점자에서 문서 서식 알림, Microsoft Word에서 훨씬 더 많은 서식 정보 접근 및 성능 향상, 그리고 iTunes Store 지원이 포함됩니다.

### 새로운 기능

* NVDA는 현재 줄의 들여쓰기 탭 및 공백 수를 입력된 순서대로 알릴 수 있습니다. 이는 문서 서식 대화 상자에서 줄 들여쓰기 알림을 선택하여 활성화할 수 있습니다. (#373)
* NVDA는 이제 화면 키보드나 음성 인식 소프트웨어와 같은 대체 키보드 입력 에뮬레이션에서 생성된 키 입력을 감지할 수 있습니다.
* NVDA는 이제 Windows 명령 콘솔에서 색상을 감지할 수 있습니다.
* 굵게, 기울임꼴 및 밑줄은 이제 설정된 번역 테이블에 적합한 기호를 사용하여 점자로 표시됩니다. (#538)
* Microsoft Word 문서에서 훨씬 더 많은 정보가 알림됩니다. 여기에는 다음이 포함됩니다:
  * 각주 및 미주 번호, 제목 수준, 주석 존재 여부, 표 중첩 수준, 링크 및 텍스트 색상과 같은 인라인 정보;
  * 주석, 각주 및 미주, 머리글 및 바닥글 섹션에 진입할 때 알림.
* 점자는 이제 선택된 텍스트를 점 7과 8을 사용하여 표시합니다. (#889)
* 점자는 이제 문서 내의 링크, 버튼 및 제목과 같은 컨트롤에 대한 정보를 알립니다. (#202)
* hedo ProfiLine 및 MobilLine USB 점자 디스플레이에 대한 지원이 추가되었습니다. (#1863, #1897)
* NVDA는 이제 기본적으로 점자에서 단어를 분리하지 않도록 설정되어 있습니다. 이는 점자 설정 대화 상자에서 비활성화할 수 있습니다. (#1890, #1946)
* 이제 점자를 줄 대신 단락 단위로 표시할 수 있습니다. 이는 많은 양의 텍스트를 더 유창하게 읽을 수 있도록 도와줍니다. 점자 설정 대화 상자의 단락 단위 읽기 옵션을 사용하여 구성할 수 있습니다. (#1891)
* 브라우즈 모드에서 점자 디스플레이를 사용하여 커서 아래의 객체를 활성화할 수 있습니다. 이는 커서가 이미 위치하지 않은 경우 커서 라우팅 키를 두 번 눌러 수행됩니다. (#1893)
* iTunes의 스토어와 같은 웹 영역에 대한 기본 지원이 추가되었습니다. WebKit 1을 사용하는 다른 응용 프로그램도 지원될 수 있습니다. (#734)
* Adobe Digital Editions 1.8.1 이상 버전의 책에서 모두 읽기를 사용할 때 페이지가 자동으로 넘어갑니다. (#1978)
* 새로운 점자 번역 테이블: 포르투갈어 2단계 점자, 아이슬란드어 8점 컴퓨터 점자, 타밀어 1단계 점자, 스페인어 8점 컴퓨터 점자, 페르시아어 1단계 점자. (#2014)
* 문서 서식 환경 설정 대화 상자에서 문서 내 프레임 알림 여부를 구성할 수 있습니다. (#1900)
* OpenBook을 사용할 때 잠자기 모드가 자동으로 활성화됩니다. (#1209)
* Poedit에서 번역자는 이제 번역자가 추가한 주석과 자동으로 추출된 주석을 읽을 수 있습니다. 번역되지 않았거나 불확실한 메시지는 별표로 표시되며, 해당 메시지로 이동할 때 비프음이 들립니다. (#1811)
* HumanWare Brailliant BI 및 B 시리즈 디스플레이에 대한 지원이 추가되었습니다. (#1990)
* 새로운 언어: 노르웨이어 보크몰, 번체 중국어(홍콩).

### 변경사항

* 현재 문자 설명 또는 현재 단어/줄 철자 명령은 이제 자동 언어 전환이 활성화되고 적절한 언어 정보가 제공되는 경우, 텍스트에 따라 적절한 언어로 철자합니다.
* eSpeak 음성 합성기를 1.46.02로 업데이트했습니다.
* NVDA는 이제 그래픽 및 링크 URL에서 추정된 매우 긴 이름(30자 이상)을 잘라냅니다. 이는 대부분 읽기에 방해가 되는 불필요한 정보일 가능성이 높습니다. (#1989)
* 점자에 표시되는 일부 정보가 축약되었습니다. (#1955, #2043)
* 캐럿 또는 리뷰 커서가 이동할 때, 점자가 수동으로 스크롤될 때와 동일한 방식으로 스크롤됩니다. 이는 점자가 단락 단위로 읽도록 설정되었거나 단어 분할을 피하도록 설정된 경우 더 적합합니다. (#1996)
* 새로운 스페인어 1단계 점자 번역 테이블로 업데이트되었습니다.
* liblouis 점자 변환기를 2.4.1로 업데이트했습니다.

### 버그 수정내역

* Windows 8에서 NVDA가 Windows 탐색기의 검색 필드에서 포커스를 잘못 이동시키는 문제가 해결되어 이제 NVDA가 해당 필드와 상호작용할 수 있습니다.
* Microsoft Word 문서를 읽거나 탐색할 때 서식 자동 알림이 활성화된 경우 성능이 크게 개선되어 서식 검토 등이 훨씬 편리해졌습니다. 일부 사용자에게는 전반적인 성능도 향상될 수 있습니다.
* 전체 화면 Adobe Flash 콘텐츠에 대해 이제 브라우즈 모드가 사용됩니다.
* Microsoft Speech API 버전 5 음성을 사용할 때 오디오 출력 장치가 기본값(Microsoft Sound Mapper)이 아닌 경우 발생하던 오디오 품질 저하 문제가 해결되었습니다. (#749)
* NVDA를 "음성 출력 끔" 음성 엔진과 함께 다시 사용할 수 있게 되어, 점자나 음성 뷰어만으로도 NVDA를 사용할 수 있습니다. (#1963)
* 객체 탐색 명령이 더 이상 "자식 없음" 및 "부모 없음"을 알리지 않고, 대신 문서와 일치하는 메시지를 알립니다.
* NVDA가 영어가 아닌 다른 언어로 설정된 경우, Tab 키의 이름이 이제 올바른 언어로 알립니다.
* Mozilla Gecko(예: Firefox)에서 문서 내 메뉴를 탐색할 때 NVDA가 간헐적으로 브라우즈 모드로 전환되는 문제가 해결되었습니다. (#2025)
* 계산기에서 백스페이스 키를 누를 때 이제 아무것도 알리지 않던 문제 대신 업데이트된 결과를 알립니다. (#2030)
* 브라우즈 모드에서 현재 탐색 커서 객체로 마우스를 이동하는 명령이 이제 객체의 왼쪽 상단이 아닌 중심으로 이동하여 더 정확해졌습니다. (#2029)
* 브라우즈 모드에서 포커스 변경 시 자동 포커스 모드가 활성화된 경우, 툴바에 포커스가 이동하면 이제 포커스 모드로 전환됩니다. (#1339)
* Adobe Reader에서 보고 제목 명령이 다시 제대로 작동합니다.
* 포커스 변경에 대한 자동 포커스 모드가 활성화된 경우, 포커스된 테이블 셀(예: ARIA 그리드)에서 포커스 모드가 올바르게 사용됩니다. (#1763)
* iTunes에서 특정 목록의 위치 정보가 이제 올바르게 알립니다.
* Adobe Reader에서 일부 링크가 더 이상 읽기 전용 편집 가능한 텍스트 필드를 포함하는 것으로 처리되지 않습니다.
* 일부 편집 가능한 텍스트 필드의 레이블이 대화 상자의 텍스트를 알릴 때 잘못 포함되지 않습니다. (#1960)
* 객체 설명 알림이 활성화된 경우, 그룹화된 항목의 설명이 다시 알립니다.
* Windows 탐색기의 드라이브 속성 대화 상자 텍스트에 사람이 읽을 수 있는 크기가 이제 포함됩니다.
* 일부 경우 속성 페이지 텍스트의 중복 알림이 억제되었습니다. (#218)
* 화면에 쓰여진 텍스트를 사용하는 편집 가능한 텍스트 필드에서 캐럿 추적이 개선되었습니다. 특히, Microsoft Excel 셀 편집기와 Eudora 메시지 편집기에서 편집이 개선되었습니다. (#1658)
* Firefox 11에서 포함된 객체(예: Flash 콘텐츠)를 벗어나기 위해 포함된 가상 버퍼로 이동 명령(NVDA+control+space)이 이제 제대로 작동합니다.
* NVDA가 비ASCII 문자가 포함된 디렉터리에 위치한 경우(예: 구성된 언어를 변경한 후) NVDA가 올바르게 다시 시작됩니다. (#2079)
* 점자는 객체 단축키, 위치 정보 및 설명 알림 설정을 올바르게 따릅니다.
* Mozilla 응용 프로그램에서 점자가 활성화된 상태로 브라우즈 모드와 포커스 모드 간 전환이 더 이상 느리지 않습니다. (#2095)
* 일부 편집 가능한 텍스트 필드에서 점자 커서 라우팅 키를 사용하여 줄/문단 끝의 공백으로 커서를 이동하는 것이 이제 텍스트 시작으로 이동하지 않고 올바르게 작동합니다. (#2096)
* NVDA가 Audiologic Tts3 음성 합성기와 다시 올바르게 작동합니다. (#2109)
* Microsoft Word 문서가 이제 다중 줄로 올바르게 처리됩니다. 이는 문서가 포커스될 때 점자가 더 적절하게 동작하도록 만듭니다.
* Microsoft Internet Explorer에서 특정 드문 컨트롤에 포커스할 때 더 이상 오류가 발생하지 않습니다. (#2121)
* 사용자가 구두점/기호의 발음을 변경하면 NVDA를 다시 시작하거나 자동 언어 전환을 비활성화하지 않아도 즉시 적용됩니다.
* eSpeak를 사용할 때, NVDA 로그 뷰어의 "다른 이름으로 저장" 대화 상자에서 일부 경우 음성이 사라지지 않습니다. (#2145)

### 개발 변경사항

* 원격 디버깅이 유용한 상황에서 사용할 수 있는 원격 Python 콘솔이 추가되었습니다. 자세한 내용은 개발자 가이드를 참조하십시오.
* 로그에서 추적 정보의 가독성을 높이기 위해 NVDA 코드의 기본 경로가 제거되었습니다. (#1880)
* TextInfo 객체에 activate() 메서드가 추가되어 TextInfo가 나타내는 위치를 활성화할 수 있습니다.
  * 이는 점자 디스플레이의 커서 라우팅 키를 사용하여 위치를 활성화하는 데 사용됩니다. 그러나 향후 다른 호출자가 있을 수 있습니다.
* TreeInterceptor와 한 번에 한 페이지의 텍스트만 노출하는 NVDA 객체는 textInfos.DocumentWithPageTurns 믹스인을 사용하여 모두 읽기 중 자동 페이지 넘김을 지원할 수 있습니다. (#1978)
* 여러 제어 및 출력 상수가 이름이 변경되거나 이동되었습니다. (#228)
  * speech.REASON_상수는 controlTypes로 이동되었습니다.
  * controlTypes에서 speechRoleLabels와 speechStateLabels는 각각 roleLabels와 stateLabels로 이름이 변경되었습니다.
* 점자 출력이 이제 입력/출력 수준에서 로그에 기록됩니다. 먼저 모든 영역의 번역되지 않은 텍스트가 기록되고, 이후 표시되는 창의 점자 셀이 기록됩니다. (#2102)
* sapi5 synthDriver의 하위 클래스는 이제 _getVoiceTokens를 재정의하고 sapi.spObjectTokenCategory와 같은 사용자 지정 레지스트리 위치에서 토큰을 가져오기 위해 init을 확장할 수 있습니다.

## 2011.3

이번 릴리스의 주요 내용으로는 적절한 언어 정보가 포함된 문서를 읽을 때 음성 언어를 자동으로 전환하는 기능, 64비트 Java Runtime Environment 지원, Mozilla 응용 프로그램의 브라우즈 모드에서 텍스트 서식 알림, 응용 프로그램 충돌 및 멈춤 현상에 대한 개선된 처리, 그리고 Windows 8에 대한 초기 수정 사항이 포함됩니다.

### 새로운 기능

* NVDA는 이제 적절한 언어 정보가 포함된 특정 웹/PDF 문서를 읽을 때 eSpeak 음성 합성기의 언어를 실시간으로 변경할 수 있습니다. 음성 설정 대화 상자에서 자동 언어/방언 전환을 켜거나 끌 수 있습니다. (#845)
* Java Access Bridge 2.0.2가 이제 지원되며, 64비트 Java Runtime Environment도 포함됩니다.
* Mozilla Gecko(예: Firefox)에서 객체 탐색을 사용할 때 제목 수준이 이제 알립니다.
* Mozilla Gecko(예: Firefox 및 Thunderbird)에서 브라우즈 모드를 사용할 때 텍스트 서식을 알릴 수 있습니다. (#394)
* Mozilla 응용 프로그램과 같은 표준 IAccessible2 텍스트 컨트롤에서 밑줄 및/또는 취소선이 있는 텍스트를 감지하고 알릴 수 있습니다.
* Adobe Reader의 브라우즈 모드에서 테이블 행 및 열 수가 이제 알립니다.
* Microsoft Speech Platform 음성 합성기가 추가로 지원됩니다. (#1735)
* IBM Lotus Symphony에서 캐럿의 페이지 및 줄 번호가 이제 알립니다. (#1632)
* 대문자를 말할 때 음높이가 얼마나 변하는지를 백분율로 설정할 수 있으며, 이는 음성 설정 대화 상자에서 구성할 수 있습니다. 그러나 이는 이전의 대문자 음높이 상승 체크박스를 대체합니다(따라서 이 기능을 끄려면 백분율을 0으로 설정하십시오). (#255)
* Microsoft Excel의 셀 서식 알림에 텍스트 및 배경 색상이 포함됩니다. (#1655)
* Java Access Bridge를 사용하는 응용 프로그램에서, 현재 탐색 객체 활성화 명령이 적절한 경우 컨트롤에서 작동합니다. (#1744)
* 새로운 언어: 타밀어.
* Design Science MathPlayer에 대한 기본 지원이 추가되었습니다.

### 변경사항

* NVDA가 충돌할 경우 자동으로 다시 시작됩니다.
* 점자에 표시되는 일부 정보가 축약되었습니다. (#1288)
* 활성 창 읽기 스크립트(NVDA+b)가 불필요한 컨트롤을 필터링하도록 개선되었으며, 이제 훨씬 더 쉽게 중단할 수 있습니다. (#1499)
* 브라우즈 모드 문서가 로드될 때 자동으로 모두 읽기를 실행하는 기능이 이제 브라우즈 모드 설정 대화 상자의 옵션으로 제공됩니다. (#414)
* 상태 표시줄 읽기(데스크탑 NVDA+end)를 시도할 때, 실제 상태 표시줄 객체를 찾을 수 없는 경우 NVDA는 대신 활성 응용 프로그램의 화면에 쓰여진 마지막 줄의 텍스트를 사용합니다. (#649)
* 브라우즈 모드 문서에서 모두 읽기를 사용할 때, NVDA는 이제 제목 및 기타 블록 수준 요소의 끝에서 일시 정지하며, 다음 텍스트와 함께 긴 문장으로 읽지 않습니다.
* 브라우즈 모드에서 탭에서 Enter 또는 스페이스를 누르면 포커스 모드로 전환되지 않고 탭이 활성화됩니다. (#1760)
* eSpeak 음성 합성기가 1.45.47로 업데이트되었습니다.

### 버그 수정내역

* NVDA는 이제 Internet Explorer 및 기타 MSHTML 컨트롤에서 작성자가 목록 스타일을 "none"으로 설정하여 표시하지 않도록 지정한 경우, 목록의 글머리 기호나 번호를 더 이상 표시하지 않습니다. (#1671)
* NVDA가 멈춘 경우(예: control+alt+n을 눌러 재시작) 이전 복사본을 종료하지 않고 새 복사본을 시작하지 않는 문제가 해결되었습니다.
* Windows 명령 콘솔에서 백스페이스나 화살표 키를 누를 때 이상한 결과가 발생하던 문제가 해결되었습니다. (#1612)
* 텍스트 편집이 허용되지 않는 WPF 콤보 박스(및 UI 자동화를 사용하는 일부 다른 콤보 박스)에서 선택된 항목이 이제 올바르게 알립니다.
* Adobe Reader의 브라우즈 모드에서, 헤더 행과 다음 행 간에 이동하거나 그 반대로 이동하는 명령을 항상 사용할 수 있습니다. 또한, 헤더 행이 더 이상 행 0으로 알리지 않습니다. (#1731)
* Adobe Reader의 브라우즈 모드에서, 테이블의 빈 셀로 이동(따라서 빈 셀을 지나 이동)할 수 있습니다.
* 점자에서 무의미한 위치 정보(예: 0 중 0 레벨 0)가 더 이상 알리지 않습니다.
* 점자가 리뷰에 연결된 경우, 이제 평면 리뷰의 내용을 표시할 수 있습니다. (#1711)
* 텍스트 컨트롤의 텍스트가 일부 경우(예: WordPad 문서의 시작 부분에서 뒤로 스크롤) 점자 디스플레이에 두 번 표시되지 않습니다.
* Internet Explorer의 브라우즈 모드에서 파일 업로드 버튼에서 Enter를 누르면 포커스 모드로 전환되지 않고 파일 선택 대화 상자가 올바르게 표시됩니다. (#1720)
* Dos 콘솔과 같은 동적 콘텐츠 변경 사항이 해당 응용 프로그램에 대해 수면 모드가 활성화된 경우 더 이상 알리지 않습니다. (#1662)
* 브라우즈 모드에서 alt+위쪽 화살표 및 alt+아래쪽 화살표를 사용하여 콤보 박스를 축소 및 확장하는 동작이 개선되었습니다. (#1630)
* NVDA는 이제 이전에 완전히 멈추게 했던 응용 프로그램이 응답을 중지하는 상황에서 더 잘 복구됩니다. (#1408)
* Mozilla Gecko(Firefox 등) 브라우즈 모드 문서에서, display:table로 스타일 지정된 요소가 있는 특정 상황에서 텍스트 렌더링에 실패하지 않습니다. (#1373)
* NVDA는 포커스가 컨트롤 내부로 이동할 때 레이블 컨트롤을 알리지 않습니다. 이는 Firefox(Gecko) 및 Internet Explorer(MSHTML)의 일부 폼 필드에서 레이블이 두 번 알리는 문제를 방지합니다. (#1650)
* Microsoft Excel에서 control+v로 셀에 붙여넣은 후 셀을 읽지 못하는 문제가 해결되었습니다. (#1781)
* Adobe Reader에서 포커스 모드로 다른 페이지의 컨트롤로 이동할 때 문서에 대한 불필요한 정보가 더 이상 알리지 않습니다. (#1659)
* Mozilla Gecko 응용 프로그램(e.g. Firefox)의 브라우즈 모드에서 토글 버튼이 이제 올바르게 감지되고 알립니다. (#1757)
* NVDA는 이제 Windows 8 개발자 미리보기에서 Windows 탐색기의 주소 표시줄을 올바르게 읽을 수 있습니다.
* NVDA는 Windows 8 개발자 미리보기에서 잘못된 글리프 변환으로 인해 winver 및 WordPad와 같은 응용 프로그램을 더 이상 충돌시키지 않습니다.
* Mozilla Gecko 10 이상(Firefox 10 등)을 사용하는 응용 프로그램의 브라우즈 모드에서, 대상 앵커가 있는 페이지를 로드할 때 커서가 더 자주 올바르게 위치합니다. (#360)
* Mozilla Gecko 응용 프로그램(e.g. Firefox)의 브라우즈 모드에서 이미지 맵의 레이블이 이제 렌더링됩니다.
* 마우스 추적이 활성화된 경우, 특정 편집 가능한 텍스트 필드(Synaptics Pointing Device Settings 및 SpeechLab SpeakText 등) 위로 마우스를 이동해도 응용 프로그램이 더 이상 충돌하지 않습니다. (#672)
* NVDA는 이제 Windows XP에 포함된 응용 프로그램의 여러 정보 대화 상자에서 올바르게 작동합니다. 예: 메모장의 정보 대화 상자 및 Windows 정보 대화 상자. (#1853, #1855)
* Windows Edit 컨트롤에서 단어 단위 리뷰가 수정되었습니다. (#1877)
* 포커스 모드에서 왼쪽 화살표, 위쪽 화살표 또는 pageUp으로 편집 가능한 텍스트 필드를 벗어나면, 캐럿 이동에 대한 자동 포커스 모드가 활성화된 경우 브라우즈 모드로 올바르게 전환됩니다. (#1733)

### 개발 변경사항

* NVDA는 이제 특정 발화 섹션에 대해 음성 합성기에 언어를 전환하도록 지시할 수 있습니다.
  * 이를 지원하기 위해 드라이버는 SynthDriver.speak()에 전달된 시퀀스에서 speech.LangChangeCommand를 처리해야 합니다.
  * SynthDriver 객체는 VoiceInfo 객체에 언어 인수를 제공해야 하며(또는 현재 언어를 검색하기 위해 language 속성을 재정의해야 합니다), 그렇지 않으면 NVDA의 사용자 인터페이스 언어가 사용됩니다.

## 2011.2

이번 릴리스의 주요 내용으로는 구두점 및 기호와 관련된 주요 개선 사항이 포함됩니다. 여기에는 구성 가능한 수준, 사용자 정의 라벨링 및 문자 설명이 포함됩니다. 또한, 모두 읽기 명령 사용 시 줄 끝에서의 멈춤이 제거되었으며, Internet Explorer에서 ARIA 지원이 개선되었습니다. Adobe Reader에서 XFA/LiveCycle PDF 문서에 대한 지원이 향상되었고, 더 많은 응용 프로그램에서 화면에 쓰여진 텍스트에 접근할 수 있게 되었습니다. 마지막으로, 화면에 쓰여진 텍스트의 서식 및 색상 정보에 접근할 수 있는 기능이 추가되었습니다.

### 새로운 기능

* 이제 현재 문자의 설명을 들을 수 있습니다. 현재 문자 읽기 스크립트를 빠르게 두 번 누르면 됩니다. 영어 문자의 경우 표준 영어 음성 알파벳이 사용됩니다. 전통 중국어와 같은 그림 문자 언어의 경우, 주어진 기호를 사용하는 하나 이상의 예문이 제공됩니다. 또한, 현재 단어 읽기 또는 현재 줄 읽기를 세 번 누르면 해당 단어/줄을 첫 번째 설명을 사용하여 철자합니다. (#55)
* Mozilla Thunderbird와 같이 텍스트를 화면에 직접 글리프로 쓰는 응용 프로그램에서 평면 리뷰로 더 많은 텍스트를 볼 수 있습니다.
* 이제 여러 수준의 구두점 및 기호 알림을 선택할 수 있습니다. (#332)
* 구두점이나 기타 기호가 네 번 이상 반복될 경우, 반복된 기호를 말하는 대신 반복 횟수를 알립니다. (#43)
* 새로운 점자 번역 테이블: 노르웨이어 8점 컴퓨터 점자, 에디오피아어 1단계 점자, 슬로베니아어 1단계 점자, 세르비아어 1단계 점자. (#1456)
* 모두 읽기 명령을 사용할 때 음성이 각 줄 끝에서 부자연스럽게 멈추지 않습니다. (#149)
* NVDA는 이제 웹 브라우저에서 aria-sort 속성에 따라 정렬 여부를 알립니다. (#1500)
* 유니코드 점자 패턴이 점자 디스플레이에 올바르게 표시됩니다. (#1505)
* Internet Explorer 및 기타 MSHTML 컨트롤에서 포커스가 컨트롤 그룹(필드셋으로 둘러싸인) 내부로 이동하면 NVDA가 그룹 이름(전설)을 알립니다. (#535)
* Internet Explorer 및 기타 MSHTML 컨트롤에서 aria-labelledBy 및 aria-describedBy 속성이 이제 준수됩니다.
* Internet Explorer 및 기타 MSHTML 컨트롤에서 ARIA 리스트, 그리드셀, 슬라이더 및 진행률 표시줄 컨트롤에 대한 지원이 개선되었습니다.
* 사용자는 이제 구두점 및 기타 기호의 발음과 기호가 말해지는 수준을 변경할 수 있습니다. (#271, #1516)
* Microsoft Excel에서 control+pageUp 또는 control+pageDown으로 시트를 전환할 때 활성 시트의 이름이 알림됩니다. (#760)
* Microsoft Word에서 Tab 키로 테이블을 탐색할 때 NVDA가 현재 셀을 알립니다. (#159)
* 문서 서식 환경 설정 대화 상자에서 테이블 셀 좌표를 알릴지 여부를 구성할 수 있습니다. (#719)
* NVDA는 이제 화면에 쓰여진 텍스트의 서식과 색상을 감지할 수 있습니다.
* Outlook Express/Windows Mail/Windows Live Mail 메시지 목록에서, NVDA는 이제 메시지가 읽지 않은 상태인지, 그리고 대화 스레드의 경우 확장되었는지 축소되었는지를 알립니다. (#868)
* eSpeak에 이제 말하기 속도를 세 배로 증가시키는 속도 부스트 설정이 추가되었습니다.
* Windows 7 시계에서 접근할 수 있는 날짜 및 시간 정보 대화 상자에 있는 캘린더 컨트롤에 대한 지원이 추가되었습니다. (#1637)
* MDV Lilli 점자 디스플레이에 대한 추가 키 바인딩이 추가되었습니다. (#241)
* 새로운 언어: 불가리아어, 알바니아어.

### 변경사항

* 리뷰 커서로 캐럿을 이동하려면, 이제 탐색 객체로 포커스 이동 스크립트(데스크탑 NVDA+shift+numpadMinus, 랩톱 NVDA+shift+backspace)를 빠르게 두 번 누르십시오. 이는 키보드에서 더 많은 키를 사용할 수 있도록 합니다. (#837)
* 리뷰 커서 아래의 문자의 10진수 및 16진수 표현을 들으려면, 이제 현재 문자 읽기를 세 번 눌러야 합니다. 두 번 누르면 이제 문자 설명을 알립니다.
* eSpeak 음성 합성기를 1.45.03으로 업데이트했습니다. (#1465)
* Mozilla Gecko 응용 프로그램에서 포커스 모드이거나 문서 외부에 있을 때 레이아웃 테이블이 더 이상 알리지 않습니다.
* Internet Explorer 및 기타 MSHTML 컨트롤에서, ARIA 응용 프로그램 내부의 문서에 대해 브라우즈 모드가 이제 작동합니다. (#1452)
* liblouis 점자 변환기를 2.3.0으로 업데이트했습니다.
* 브라우즈 모드에서 빠른 탐색 또는 포커스를 사용하여 컨트롤로 이동할 때, 컨트롤에 설명이 있는 경우 이를 알립니다.
* 브라우즈 모드에서 진행률 표시줄이 이제 알립니다.
* Internet Explorer 및 기타 MSHTML 컨트롤에서 ARIA 역할이 presentation으로 표시된 노드는 간단 리뷰 및 포커스 계층에서 필터링됩니다.
* NVDA의 사용자 인터페이스와 문서에서 이제 가상 버퍼를 브라우즈 모드로 지칭합니다. "가상 버퍼"라는 용어는 대부분의 사용자에게 의미가 없기 때문입니다. (#1509)
* 사용자가 로그인 화면 등에서 사용할 사용자 설정을 시스템 프로필로 복사하려고 할 때, 설정에 사용자 정의 플러그인이 포함된 경우 보안 위험이 있을 수 있음을 경고합니다. (#1426)
* NVDA 서비스는 더 이상 사용자 입력 데스크탑에서 NVDA를 시작하거나 중지하지 않습니다.
* Windows XP 및 Windows Vista에서 NVDA는 플랫폼 업데이트를 통해 UI 자동화가 제공되더라도 이를 더 이상 사용하지 않습니다. UI 자동화를 사용하면 일부 최신 응용 프로그램의 접근성이 향상될 수 있지만, XP 및 Vista에서는 이를 사용할 때 너무 많은 멈춤, 충돌 및 전반적인 성능 저하가 발생했습니다. (#1437)
* Mozilla Gecko 2 이상(예: Firefox 4 이상)을 사용하는 응용 프로그램에서 문서를 브라우즈 모드로 완전히 로드되기 전에 읽을 수 있습니다.
* NVDA는 포커스가 컨트롤 내부로 이동할 때 컨테이너의 상태를 알립니다(예: 포커스가 로드 중인 문서 내부로 이동하면 "사용 중"으로 알림).
* NVDA의 사용자 인터페이스와 문서에서 객체 탐색과 관련하여 "첫 번째 자식" 및 "부모"라는 용어를 더 이상 사용하지 않습니다. 이러한 용어는 많은 사용자에게 혼란을 줄 수 있기 때문입니다.
* 하위 메뉴가 있는 일부 메뉴 항목에 대해 더 이상 "축소됨"이 알리지 않습니다.
* 현재 서식 알림 스크립트(NVDA+f)는 이제 시스템 캐럿/포커스 대신 리뷰 커서 위치의 서식을 알립니다. 기본적으로 리뷰 커서는 캐럿을 따르기 때문에 대부분의 사용자는 차이를 느끼지 못할 것입니다. 그러나 이제 리뷰 커서를 이동할 때(예: 평면 리뷰에서) 서식을 확인할 수 있습니다.

### 버그 수정내역

* 브라우즈 모드 문서에서 NVDA+스페이스로 포커스 모드를 강제로 전환한 후 콤보 박스를 축소해도 자동으로 브라우즈 모드로 전환되지 않음. (#1386)
* Gecko(예: Firefox) 및 MSHTML(예: Internet Explorer) 문서에서, 이전에 별도의 줄로 렌더링되던 특정 텍스트가 이제 동일한 줄에 올바르게 렌더링됨. (#1378)
* 점자가 리뷰에 연결된 상태에서 탐색 객체가 브라우즈 모드 문서로 이동되면(수동으로 또는 포커스 변경으로 인해), 점자가 브라우즈 모드 콘텐츠를 적절히 표시함. (#1406, #1407)
* 구두점 읽기가 비활성화된 경우, 일부 음성 합성기를 사용할 때 특정 구두점이 잘못 읽히는 문제가 더 이상 발생하지 않음. (#332)
* 음성 설정을 지원하지 않는 Audiologic Tts3와 같은 음성 합성기의 설정을 로드할 때 문제가 더 이상 발생하지 않음. (#1347)
* Skype Extras 메뉴가 이제 올바르게 읽힘. (#648)
* 마우스 설정 대화 상자에서 "밝기 조절이 볼륨을 제어" 옵션을 선택하면, Windows Vista/Windows 7에서 Aero가 활성화된 경우 마우스를 화면 주위로 이동할 때 비프음이 크게 지연되는 문제가 더 이상 발생하지 않음. (#1183)
* NVDA가 랩톱 키보드 레이아웃으로 설정된 경우, NVDA+Delete가 문서화된 대로 현재 탐색 객체의 크기를 알림. (#1498)
* NVDA가 Internet Explorer 문서에서 aria-selected 속성을 적절히 준수함.
* NVDA가 브라우즈 모드 문서에서 자동으로 포커스 모드로 전환될 때, 포커스의 컨텍스트에 대한 정보를 알림. 예를 들어, 리스트 박스 항목이 포커스를 받을 경우, 리스트 박스가 먼저 알림. (#1491)
* Internet Explorer 및 기타 MSHTML 컨트롤에서, ARIA 리스트박스 컨트롤이 이제 리스트 항목이 아닌 리스트로 처리됨.
* 읽기 전용 편집 가능한 텍스트 컨트롤이 포커스를 받을 때, NVDA가 이제 해당 컨트롤이 읽기 전용임을 알림. (#1436)
* 브라우즈 모드에서 NVDA가 읽기 전용 편집 가능한 텍스트 필드와 관련하여 올바르게 동작함.
* 브라우즈 모드 문서에서 aria-activedescendant가 설정될 때 NVDA가 잘못 포커스 모드에서 벗어나는 문제가 더 이상 발생하지 않음. 예: 일부 자동 완성 컨트롤에서 완료 리스트가 나타날 때.
* Adobe Reader에서 포커스를 이동하거나 브라우즈 모드에서 빠른 탐색을 사용할 때 컨트롤의 이름이 알림.
* Adobe Reader의 XFA PDF 문서에서 버튼, 링크 및 그래픽이 이제 올바르게 렌더링됨.
* Adobe Reader의 XFA PDF 문서에서 모든 요소가 별도의 줄에 렌더링됨. 이 변경은 이러한 문서에서 구조가 부족하여 큰 섹션(때로는 문서 전체)이 구분 없이 렌더링되던 문제를 해결하기 위해 이루어짐.
* Adobe Reader의 XFA PDF 문서에서 편집 가능한 텍스트 필드로 포커스를 이동하거나 벗어날 때 발생하던 문제가 수정됨.
* Adobe Reader의 XFA PDF 문서에서 포커스를 받은 콤보 박스의 값 변경 사항이 이제 알림.
* Outlook Express에서 색상을 선택하는 콤보 박스와 같은 소유자 그리기 콤보 박스가 이제 NVDA로 접근 가능함. (#1340)
* 프랑스어 및 독일어와 같이 공백을 숫자 그룹/천 단위 구분자로 사용하는 언어에서, 별도의 텍스트 청크에서 가져온 숫자가 단일 숫자로 잘못 발음되지 않음. 이는 특히 숫자가 포함된 테이블 셀에서 문제가 되었음. (#555)
* Internet Explorer 및 기타 MSHTML 컨트롤에서 ARIA 역할이 description인 노드가 이제 편집 필드가 아닌 정적 텍스트로 분류됨.
* 브라우즈 모드 문서에서 포커스가 있는 상태에서 Tab 키를 누를 때 발생하던 다양한 문제가 수정됨(예: Internet Explorer에서 Tab 키가 부적절하게 주소 표시줄로 이동). (#720, #1367)
* 텍스트를 읽는 동안 리스트에 들어갈 때, NVDA가 이제 "5개의 항목이 있는 리스트"와 같이 알림. (#1515)
* 입력 도움말 모드에서, 제스처가 입력 도움말을 우회하는 스크립트에 바인딩된 경우에도 제스처가 로그에 기록됨. 예: 점자 디스플레이 앞으로/뒤로 스크롤 명령.
* 입력 도움말 모드에서, 키보드에서 특수 키를 누르고 있을 때 NVDA가 더 이상 해당 키가 자신을 수정하는 것처럼 알리지 않음. 예: NVDA+NVDA.
* Adobe Reader 문서에서 c 또는 shift+c를 눌러 콤보 박스로 이동하는 기능이 이제 작동함.
* 선택 가능한 테이블 행의 선택 상태가 이제 리스트 및 트리 뷰 항목과 동일한 방식으로 알림.
* Firefox 및 기타 Gecko 응용 프로그램에서, 콘텐츠가 화면 밖으로 플로팅된 경우에도 브라우즈 모드에서 컨트롤을 활성화할 수 있음. (#801)
* 메시지 대화 상자가 표시되는 동안 NVDA 설정 대화 상자를 표시할 수 없게 됨. 이 경우 설정 대화 상자가 동결되었음. (#1451)
* Microsoft Excel에서 셀 간 이동 또는 선택을 위해 키를 누르고 있거나 빠르게 누를 때 지연이 발생하지 않음.
* NVDA 서비스가 간헐적으로 충돌하여 보안 Windows 화면에서 NVDA가 실행되지 않던 문제가 수정됨.
* 텍스트가 사라지는 변경 사항이 발생했을 때 점자 디스플레이에서 발생하던 문제가 수정됨. (#1377)
* Internet Explorer 9의 다운로드 창을 NVDA로 탐색하고 읽을 수 있음. (#1280)
* NVDA를 동시에 여러 복사본 실행하는 것이 불가능해짐. (#507)
* 느린 시스템에서 NVDA가 실행 중일 때 메인 창이 항상 표시되는 문제가 더 이상 발생하지 않음. (#726)
* Windows XP에서 WPF 응용 프로그램을 시작할 때 NVDA가 충돌하지 않음. (#1437)
* UI 자동화 텍스트 컨트롤에서 모든 필수 기능을 지원하는 경우, say all 및 리뷰로 say all이 작동함. 예: XPS Viewer 문서에서 say all을 사용할 수 있음.
* NVDA가 Outlook Express/Windows Live Mail 메시지 규칙 "지금 적용" 대화 상자에서 일부 리스트 항목을 체크박스로 잘못 분류하지 않음. (#576)
* 콤보 박스가 더 이상 하위 메뉴를 포함한다고 알리지 않음.
* NVDA가 Microsoft Outlook에서 받는 사람, 참조, 숨은 참조 필드의 내용을 읽을 수 있음. (#421)
* NVDA 음성 설정 대화 상자에서 슬라이더 값이 변경될 때 가끔 보고되지 않던 문제가 수정됨. (#1411)
* Excel 스프레드시트에서 잘라내기 및 붙여넣기 후 셀 간 이동 시 NVDA가 새 셀을 알리지 않던 문제가 수정됨. (#1567)
* NVDA가 색상 이름을 알릴수록 색상 이름 추측이 점점 더 나빠지던 문제가 수정됨.
* Internet Explorer 및 기타 MSHTML 컨트롤에서, ARIA 역할이 presentation인 iframe을 포함하는 드문 페이지의 일부를 읽을 수 없던 문제가 수정됨. (#1569)
* Internet Explorer 및 기타 MSHTML 컨트롤에서, 포커스 모드에서 다중 줄 편집 가능한 텍스트 필드와 문서 간 포커스가 무한히 튀던 드문 문제가 수정됨. (#1566)
* Microsoft Word 2010에서 NVDA가 확인 대화 상자를 자동으로 읽음. (#1538)
* Internet Explorer 및 기타 MSHTML 컨트롤의 다중 줄 편집 가능한 텍스트 필드에서 첫 번째 줄 이후의 선택이 올바르게 알림. (#1590)
* 브라우즈 모드 및 Windows 편집 컨트롤을 포함한 여러 경우에서 단어 단위 이동이 개선됨. (#1580)
* NVDA 설치 프로그램이 홍콩 버전의 Windows Vista 및 Windows 7에서 깨진 텍스트를 더 이상 표시하지 않음. (#1596)
* Microsoft Speech API 버전 5 음성 합성기의 설정이 포함된 구성에서 음성 설정이 누락된 경우에도 NVDA가 음성 합성기를 로드하지 못하던 문제가 수정됨. (#1599)
* Internet Explorer 및 기타 MSHTML 컨트롤의 편집 가능한 텍스트 필드에서 점자가 활성화된 경우 NVDA가 지연되거나 멈추지 않음.
* Firefox 브라우즈 모드에서, ARIA 역할이 presentation인 포커스 가능한 노드 내부의 콘텐츠를 포함하지 않던 문제가 수정됨.
* Microsoft Word에서 점자가 활성화된 경우 첫 번째 페이지 이후의 페이지에서 줄이 올바르게 알림. (#1603)
* Microsoft Word 2003에서, 오른쪽에서 왼쪽으로 쓰는 텍스트 줄이 점자가 활성화된 경우 다시 읽을 수 있음. (#627)
* Microsoft Word에서 문서가 문장 끝으로 끝나지 않을 때 say all이 올바르게 작동함.
* Windows Live Mail 2011에서 일반 텍스트 메시지를 열 때 NVDA가 메시지 문서에 올바르게 포커스를 맞추어 읽을 수 있음.
* Windows Live Mail의 이동/복사 대화 상자에서 NVDA가 일시적으로 멈추거나 말을 하지 않던 문제가 수정됨. (#574)
* Outlook 2010에서 NVDA가 메시지 리스트의 포커스를 올바르게 추적함. (#1285)
* MDV Lilli 점자 디스플레이에서 일부 USB 연결 문제가 해결됨. (#241)
* Internet Explorer 및 기타 MSHTML 컨트롤에서, 특정 경우(예: 링크 뒤) 브라우즈 모드에서 공백이 무시되지 않음.
* Internet Explorer 및 기타 MSHTML 컨트롤에서, 브라우즈 모드에서 불필요한 줄 바꿈이 제거됨. 특히, display 스타일이 None인 HTML 요소가 더 이상 줄 바꿈을 강제하지 않음. (#1685)
* NVDA가 시작할 수 없는 경우, Windows 중요 중지 소리를 재생하지 못해 로그 파일의 중요 오류 메시지가 덮어쓰이는 문제가 더 이상 발생하지 않음.

### 개발 변경사항

* 이제 SCons를 사용하여 개발자 문서를 생성할 수 있습니다. 관련 종속성을 포함한 자세한 내용은 소스 배포의 루트에 있는 readme.txt를 참조하십시오.
* 로케일에서 문자에 대한 설명을 제공할 수 있습니다. 자세한 내용은 개발자 가이드의 문자 설명 섹션을 참조하십시오. (#55)
* 로케일에서 특정 구두점 및 기타 기호의 발음 정보를 제공할 수 있습니다. 자세한 내용은 개발자 가이드의 기호 발음 섹션을 참조하십시오. (#332)
* nvdaHelper를 여러 디버깅 옵션으로 빌드할 수 있습니다. 자세한 내용은 소스 배포의 루트에 있는 readme.txt에서 nvdaHelperDebugFlags SCons 변수를 참조하십시오. (#1390)
* 음성 합성기 드라이버는 이제 텍스트와 인덱스만 전달받는 대신 텍스트와 음성 명령의 시퀀스를 전달받습니다.
  * 이를 통해 내장된 인덱스, 매개변수 변경 등을 지원할 수 있습니다.
  * 드라이버는 SynthDriver.speakText() 및 SynthDriver.speakCharacter() 대신 SynthDriver.speak()를 구현해야 합니다.
  * SynthDriver.speak()가 구현되지 않은 경우 이전 메서드가 사용되지만, 이는 지원 종료 예정이며 향후 릴리스에서 제거될 예정입니다.
* gui.execute()가 제거되었습니다. 대신 wx.CallAfter()를 사용해야 합니다.
* gui.scriptUI가 제거되었습니다.
  * 메시지 대화 상자의 경우 wx.CallAfter(gui.messageBox, ...)를 사용하십시오.
  * 기타 모든 대화 상자의 경우 실제 wx 대화 상자를 사용해야 합니다.
  * 새로운 gui.runScriptModalDialog() 함수는 스크립트에서 모달 대화 상자를 사용하는 작업을 단순화합니다.
* 음성 합성기 드라이버는 이제 불리언 설정을 지원할 수 있습니다. 자세한 내용은 SynthDriverHandler.BooleanSynthSetting을 참조하십시오.
* SCons는 이제 인증 코드 서명에 타임스탬프를 추가하기 위해 사용할 타임스탬프 서버의 URL을 지정하는 certTimestampServer 변수를 허용합니다. (#1644)

## 2011.1.1

이 릴리스는 NVDA 2011.1에서 발견된 여러 보안 및 기타 중요한 문제를 수정합니다.

### 버그 수정내역

* NVDA 메뉴의 후원 항목은 로그온, 잠금, UAC 및 기타 보안 Windows 화면에서 실행 중일 때 비활성화됩니다. 이는 보안 위험이기 때문입니다. (#1419)
* 보안 데스크탑(잠금 화면, UAC 화면 및 Windows 로그온)에서 NVDA의 사용자 인터페이스 내에서 복사하거나 붙여넣는 것이 불가능해졌습니다. 이는 보안 위험이기 때문입니다. (#1421)
* Firefox 4에서 포함된 객체(예: Flash 콘텐츠)를 벗어나기 위해 사용하는 포함된 가상 버퍼로 이동 명령(NVDA+control+space)이 이제 제대로 작동합니다. (#1429)
* 명령 키 알림이 활성화된 경우, Shift 키와 함께 입력된 문자가 더 이상 명령 키로 잘못 알림되지 않습니다. (#1422)
* 명령 키 알림이 활성화된 경우, Shift 이외의 특수 키(예: Control 및 Alt)와 함께 Space 키를 누르면 이제 명령 키로 알림됩니다. (#1424)
* 로그온, 잠금, UAC 및 기타 보안 Windows 화면에서 실행 중일 때 로깅이 완전히 비활성화됩니다. 이는 보안 위험이기 때문입니다. (#1435)
* 입력 도움말 모드에서, 제스처가 스크립트에 바인딩되지 않은 경우에도 로그에 기록됩니다(사용자 가이드에 따라). (#1425)

## 2011.1

이 릴리스의 주요 내용으로는 mIRC, PuTTY, Tera Term 및 SecureCRT에서 새 텍스트 출력 자동 알림; 글로벌 플러그인 지원; Microsoft Word에서 글머리 기호 및 번호 매기기 알림; 다음 줄 및 이전 줄로 이동하는 키를 포함한 점자 디스플레이에 대한 추가 키 바인딩; 여러 Baum, HumanWare 및 APH 점자 디스플레이 지원; IBM Lotus Symphony 텍스트 컨트롤을 포함한 일부 컨트롤에 대한 색상 알림이 포함됩니다.

### 새로운 기능

* 일부 컨트롤에 대해 색상을 보고할 수 있습니다. 자동 보고는 문서 서식 설정 대화 상자에서 구성할 수 있습니다. 또한 텍스트 서식 보고 명령(NVDA+f)을 사용하여 필요할 때 보고할 수도 있습니다.
  * 초기에는 표준 IAccessible2 편집 가능한 텍스트 컨트롤(예: Mozilla 응용 프로그램), RichEdit 컨트롤(예: Wordpad) 및 IBM Lotus Symphony 텍스트 컨트롤에서 지원됩니다.
* 가상 버퍼에서 페이지 단위(shift+pageDown 및 shift+pageUp) 및 단락 단위(shift+control+downArrow 및 shift+control+upArrow)로 선택할 수 있습니다. (#639)
* NVDA는 이제 mIRC, PuTTY, Tera Term 및 SecureCRT에서 새 텍스트 출력이 자동으로 보고됩니다. (#936)
* 사용자는 이제 단일 사용자 입력 제스처 맵을 제공하여 NVDA의 모든 스크립트에 대해 새로운 키 바인딩을 추가하거나 기존 키 바인딩을 재정의할 수 있습니다. (#194)
* 글로벌 플러그인 지원. 글로벌 플러그인은 모든 응용 프로그램에서 작동하는 NVDA에 새로운 기능을 추가할 수 있습니다. (#281)
* Caps Lock이 켜진 상태에서 shift 키를 사용하여 문자를 입력할 때 작은 비프음이 들립니다. 이는 키보드 설정 대화 상자의 관련 새 옵션을 선택 해제하여 끌 수 있습니다. (#663)
* Microsoft Word에서 줄 단위로 이동할 때 하드 페이지 구분이 보고됩니다. (#758)
* Microsoft Word에서 줄 단위로 이동할 때 글머리 기호 및 번호 매기기가 음성으로 보고됩니다. (#208)
* 현재 응용 프로그램에 대해 Sleep 모드를 전환하는 명령(NVDA+shift+s)이 새로 추가되었습니다. Sleep 모드(이전에는 자체 음성 모드로 알려짐)는 특정 응용 프로그램에 대해 NVDA의 모든 화면 읽기 기능을 비활성화합니다. 자체 음성 또는 화면 읽기 기능을 제공하는 응용 프로그램에 매우 유용합니다. 이 명령을 다시 누르면 Sleep 모드가 비활성화됩니다.
* 몇 가지 추가 점자 디스플레이 키 바인딩이 추가되었습니다. 자세한 내용은 사용자 가이드의 지원되는 점자 디스플레이 섹션을 참조하십시오. (#209)
* 타사 개발자의 편의를 위해 응용 프로그램 모듈뿐만 아니라 글로벌 플러그인도 NVDA를 다시 시작하지 않고 다시 로드할 수 있습니다. NVDA 메뉴에서 도구 -> 플러그인 다시 로드를 사용하거나 NVDA+control+f3을 누르십시오. (#544)
* NVDA는 이제 이전에 방문한 웹 페이지로 돌아갈 때 사용자가 위치했던 지점을 기억합니다. 이는 브라우저 또는 NVDA를 종료할 때까지 적용됩니다. (#132)
* Handy Tech 점자 디스플레이는 이제 Handy Tech 유니버설 드라이버를 설치하지 않고도 사용할 수 있습니다. (#854)
* 여러 Baum, HumanWare 및 APH 점자 디스플레이에 대한 지원이 추가되었습니다. (#937)
* Media Player Classic Home Cinema의 상태 표시줄이 이제 인식됩니다.
* Freedom Scientific Focus 40 Blue 점자 디스플레이는 이제 블루투스를 통해 연결된 경우 사용할 수 있습니다. (#1345)

### 변경사항

* 위치 정보가 더 이상 기본적으로 보고되지 않습니다. 이는 대부분의 메뉴, 실행 중인 응용 프로그램 바, 알림 영역 등에서 일반적으로 잘못된 경우가 많았기 때문입니다. 그러나 객체 표시 설정 대화 상자에서 추가된 옵션을 통해 다시 활성화할 수 있습니다.
* 키보드 도움말이 입력 도움말로 이름이 변경되었습니다. 이는 키보드 외의 입력 소스도 처리한다는 점을 반영한 것입니다.
* 입력 도움말은 더 이상 스크립트의 코드 위치를 음성 및 점자로 보고하지 않습니다. 이는 사용자에게 암호화되어 있으며 관련이 없기 때문입니다. 그러나 개발자와 고급 사용자를 위해 로그에 기록됩니다.
* NVDA가 멈췄다고 감지되면, NVDA 특수 키를 계속 가로채지만 다른 키는 시스템에 전달합니다. 이를 통해 사용자가 NVDA가 멈춘 것을 인지하지 못한 상태에서 NVDA 특수 키를 눌러 캡스 락 등을 의도치 않게 전환하는 것을 방지합니다. (#939)
* 다음 키 전달 명령을 사용한 후 키를 계속 누르고 있으면, 마지막 키가 해제될 때까지 모든 키(키 반복 포함)가 전달됩니다.
* NVDA 특수 키를 빠르게 두 번 눌러 전달하고 두 번째 누름을 계속 누르고 있으면, 모든 키 반복도 전달됩니다.
* 볼륨 증가, 감소 및 음소거 키가 이제 입력 도움말에서 보고됩니다. 이는 사용자가 이러한 키가 무엇인지 확신하지 못할 경우 유용할 수 있습니다.
* NVDA 환경 설정 메뉴의 검토 커서 항목에 대한 단축키가 r에서 c로 변경되었습니다. 이는 점자 설정 항목과의 충돌을 제거하기 위함입니다.

### 버그 수정내역

* 새 음성 사전 항목을 추가할 때, 대화 상자의 제목이 이제 "사전 항목 추가"로 표시되며, 이전에는 "사전 항목 편집"으로 표시되었습니다. (#924)
* 음성 사전 대화 상자에서, 사전 항목 목록의 정규 표현식 및 대소문자 구분 열의 내용이 항상 영어로 표시되던 문제가 수정되어 이제 NVDA에서 설정된 언어로 표시됩니다.
* AIM에서 트리 뷰의 위치 정보가 이제 발표됩니다.
* 음성 설정 대화 상자의 슬라이더에서, 위쪽 화살표/페이지 업/홈 키는 설정을 증가시키고, 아래쪽 화살표/페이지 다운/엔드 키는 설정을 감소시킵니다. 이전에는 반대로 작동했으며, 이는 논리적이지 않고 음성 설정 링과 일관성이 없었습니다. (#221)
* 화면 레이아웃이 비활성화된 가상 버퍼에서, 일부 불필요한 빈 줄이 더 이상 나타나지 않습니다.
* NVDA 특수 키를 빠르게 두 번 눌렀을 때 중간에 다른 키 입력이 있는 경우, 두 번째 누름에서 NVDA 특수 키가 더 이상 전달되지 않습니다.
* 구두점 읽기가 비활성화된 경우에도 입력 도움말에서 구두점 키가 발표됩니다. (#977)
* 키보드 설정 대화 상자에서, 키보드 레이아웃 이름이 항상 영어로 표시되던 문제가 수정되어 이제 NVDA에서 설정된 언어로 표시됩니다. (#558)
* Adobe Reader 문서에서 일부 항목이 빈 항목으로 렌더링되던 문제가 수정되었습니다. 예: Apple iPhone IOS 4.1 사용자 가이드의 목차 링크.
* NVDA 일반 설정 대화 상자의 "현재 저장된 설정을 로그인 및 기타 보안 화면에서 사용" 버튼이 NVDA를 새로 설치한 직후 보안 화면이 나타나기 전에 사용된 경우에도 이제 제대로 작동합니다. 이전에는 NVDA가 복사가 성공했다고 보고했지만 실제로는 아무 효과가 없었습니다. (#1194)
* 두 개의 NVDA 설정 대화 상자를 동시에 열 수 없게 되었습니다. 이는 하나의 열린 대화 상자가 다른 열린 대화 상자에 의존하는 경우 발생하는 문제를 해결합니다. 예: 음성 설정 대화 상자가 열려 있는 동안 음성 합성기를 변경하는 경우. (#603)
* UAC가 활성화된 시스템에서, NVDA 일반 설정 대화 상자의 "현재 저장된 설정을 로그인 및 기타 보안 화면에서 사용" 버튼이 사용자의 계정 이름에 공백이 포함된 경우에도 더 이상 실패하지 않습니다. (#918)
* Internet Explorer 및 기타 MSHTML 컨트롤에서, NVDA가 링크 이름을 결정하기 위해 URL을 최후의 수단으로 사용하는 대신 빈 링크를 표시하던 문제가 수정되었습니다. (#633)
* AOL Instant Messenger 7 메뉴에서 포커스를 무시하던 문제가 수정되었습니다. (#655)
* Microsoft Word 맞춤법 검사 대화 상자에서 오류에 대한 올바른 레이블이 발표됩니다. 예: 사전에 없음, 문법 오류, 구두점. 이전에는 모두 문법 오류로 발표되었습니다. (#883)
* Microsoft Word에서 점자 디스플레이를 사용하는 동안 입력된 텍스트가 깨지거나 점자 라우팅 키를 누를 때 발생하던 드문 멈춤 문제가 수정되었습니다. (#1212) 그러나 제한 사항으로, Word 2003 이하에서 아랍어 텍스트를 점자 디스플레이로 읽을 수 없습니다. (#627)
* 편집 필드에서 삭제 키를 누를 때, 점자 디스플레이의 텍스트/커서가 변경 사항을 반영하도록 항상 적절히 업데이트됩니다. (#947)
* Gecko2 문서(예: Firefox 4)에서 여러 탭이 열려 있는 동안 동적 페이지의 변경 사항이 이제 NVDA에 의해 제대로 반영됩니다. 이전에는 첫 번째 탭의 변경 사항만 반영되었습니다. (Mozilla 버그 610985)
* Microsoft Word 맞춤법 검사 대화 상자에서 문법 및 구두점 오류에 대한 제안 사항이 이제 NVDA에 의해 제대로 발표됩니다. (#704)
* Internet Explorer 및 기타 MSHTML 컨트롤에서, NVDA가 가상 버퍼에서 대상 앵커를 빈 링크로 표시하던 문제가 수정되었습니다. 대신 이러한 앵커는 숨겨집니다. (#1326)
* 표준 그룹 상자 창 주위 및 내부에서 객체 탐색이 더 이상 깨지거나 비대칭적이지 않습니다.
* Firefox 및 기타 Gecko 기반 컨트롤에서, 외부 문서가 로드되기 전에 하위 프레임이 로드를 완료하면 NVDA가 더 이상 하위 프레임에 갇히지 않습니다.
* numpadDelete로 문자를 삭제할 때 NVDA가 다음 문자를 적절히 발표합니다. (#286)
* Windows XP 로그인 화면에서, 선택된 사용자가 변경될 때 사용자 이름이 다시 발표됩니다.
* 줄 번호 보고가 활성화된 Windows 명령 콘솔에서 텍스트를 읽을 때 발생하던 문제가 수정되었습니다.
* 가상 버퍼의 요소 목록 대화 상자가 이제 시각 장애인이 아닌 사용자도 사용할 수 있습니다. 모든 컨트롤이 화면에 표시됩니다. (#1321)
* 음성 사전 대화 상자의 항목 목록이 이제 시각 장애인이 아닌 사용자에게 더 읽기 쉽게 표시됩니다. 목록이 이제 모든 열을 화면에 표시할 수 있을 만큼 충분히 큽니다. (#90)
* ALVA BC640/BC680 점자 디스플레이에서, 다른 키가 해제된 후에도 여전히 눌려 있는 디스플레이 키가 NVDA에 의해 무시되지 않습니다.
* Adobe Reader X에서 태그가 없는 문서 옵션을 떠난 후 처리 대화 상자가 나타나기 전에 더 이상 충돌하지 않습니다. (#1218)
* NVDA가 저장된 구성으로 복원될 때 적절한 점자 디스플레이 드라이버로 전환됩니다. (#1346)
* Visual Studio 2008 프로젝트 마법사가 다시 올바르게 읽힙니다. (#974)
* 실행 파일 이름에 비ASCII 문자가 포함된 응용 프로그램에서 NVDA가 완전히 작동하지 않던 문제가 수정되었습니다. (#1352)
* AkelPad에서 줄 바꿈이 활성화된 상태로 줄 단위로 읽을 때, NVDA가 현재 줄 끝에서 다음 줄의 첫 번째 문자를 읽지 않습니다.
* Visual Studio 2005/2008 코드 편집기에서, NVDA가 입력된 문자마다 전체 텍스트를 읽지 않습니다. (#975)
* NVDA가 종료되거나 디스플레이가 변경될 때 일부 점자 디스플레이가 제대로 지워지지 않던 문제가 수정되었습니다.
* NVDA가 시작될 때 초기 포커스가 때때로 두 번 발표되던 문제가 수정되었습니다. (#1359)

### 개발 변경사항

* 이제 SCons를 사용하여 소스 트리를 준비하고 바이너리 빌드, 포터블 아카이브, 설치 프로그램 등을 생성합니다. 자세한 내용은 소스 배포의 루트에 있는 readme.txt를 참조하십시오.
* NVDA에서 사용되는 키 이름(키 매핑 포함)이 더 친숙하고 논리적으로 변경되었습니다. 예: extendedUp 대신 upArrow, prior 대신 numpadPageUp. 키 이름 목록은 vkCodes 모듈을 참조하십시오.
* 사용자의 모든 입력은 이제 inputCore.InputGesture 인스턴스로 표현됩니다. (#601)
  * 입력 소스마다 기본 InputGesture 클래스를 서브클래싱합니다.
  * 시스템 키보드의 키 입력은 keyboardHandler.KeyboardInputGesture 클래스로 처리됩니다.
  * 점자 디스플레이의 버튼, 휠 및 기타 컨트롤 입력은 braille.BrailleDisplayGesture 클래스의 서브클래스로 처리됩니다. 이러한 서브클래스는 각 점자 디스플레이 드라이버에서 제공합니다.
* 입력 제스처는 ScriptableObject의 ScriptableObject.bindGesture() 메서드를 사용하거나 클래스의 __gestures 딕셔너리를 통해 스크립트 이름에 매핑하여 바인딩할 수 있습니다. 자세한 내용은 baseObject.ScriptableObject를 참조하십시오.
* 응용 프로그램 모듈에는 더 이상 키 매핑 파일이 없습니다. 모든 입력 제스처 바인딩은 응용 프로그램 모듈 자체에서 처리해야 합니다.
* 모든 스크립트는 이제 키 입력 대신 InputGesture 인스턴스를 받습니다.
  * KeyboardInputGesture는 gesture의 send() 메서드를 사용하여 운영 체제로 전달할 수 있습니다.
* 임의의 키 입력을 보내려면 KeyboardInputGesture.fromName()을 사용하여 KeyboardInputGesture를 생성한 후 send() 메서드를 호출해야 합니다.
* 로케일은 이제 NVDA의 어디에서나 스크립트에 대한 새로운 바인딩을 추가하거나 기존 바인딩을 재정의하는 입력 제스처 맵 파일을 제공할 수 있습니다. (#810)
  * 로케일 제스처 맵은 locale\LANG\gestures.ini에 배치해야 하며, LANG는 언어 코드를 나타냅니다.
  * 파일 형식에 대한 자세한 내용은 inputCore.GlobalGestureMap을 참조하십시오.
* 새로운 LiveText 및 Terminal NVDAObject 동작은 새로운 텍스트를 자동으로 알리는 기능을 제공합니다. 자세한 내용은 NVDAObjects.behaviors의 해당 클래스를 참조하십시오. (#936)
  * NVDAObjects.window.DisplayModelLiveText 오버레이 클래스는 화면에 쓰여진 텍스트를 검색해야 하는 객체에 사용할 수 있습니다.
  * 사용 예시는 mirc 및 putty 응용 프로그램 모듈을 참조하십시오.
* 더 이상 _default 응용 프로그램 모듈이 없습니다. 응용 프로그램 모듈은 appModuleHandler.AppModule(기본 AppModule 클래스)을 서브클래싱해야 합니다.
* 전역 플러그인을 지원하여 전역적으로 스크립트를 바인딩하거나 NVDAObject 이벤트를 처리하고 NVDAObject 오버레이 클래스를 선택할 수 있습니다. (#281) 자세한 내용은 globalPluginHandler.GlobalPlugin을 참조하십시오.
* SynthDriver 객체에서 문자열 설정(e.g. availableVoices 및 availableVariants)에 대한 available속성은 이제 ID를 키로 사용하는 OrderedDict로 제공됩니다.
* synthDriverHandler.VoiceInfo는 이제 음성의 언어를 지정하는 선택적 language 인수를 받습니다.
* SynthDriver 객체는 현재 음성의 언어를 지정하는 language 속성을 제공합니다.
  * 기본 구현은 availableVoices의 VoiceInfo 객체에 지정된 언어를 사용합니다. 이는 음성당 하나의 언어를 지원하는 대부분의 음성 합성기에 적합합니다.
* 점자 디스플레이 드라이버는 버튼, 휠 및 기타 컨트롤을 NVDA 스크립트에 바인딩할 수 있도록 개선되었습니다:
  * 드라이버는 NVDA의 어디에서나 스크립트에 대한 바인딩을 추가하는 전역 입력 제스처 맵을 제공할 수 있습니다.
  * 디스플레이별 기능을 수행하는 자체 스크립트를 제공할 수도 있습니다.
  * 자세한 내용은 braille.BrailleDisplayDriver를 참조하고 기존 점자 디스플레이 드라이버를 예제로 확인하십시오.
* AppModule 클래스의 'selfVoicing' 속성 이름이 'sleepMode'로 변경되었습니다.
* 응용 프로그램 모듈 이벤트 event_appLoseFocus 및 event_appGainFocus는 각각 event_appModule_loseFocus 및 event_appModule_gainFocus로 이름이 변경되어 응용 프로그램 모듈 및 트리 인터셉터와의 명명 규칙을 일관되게 했습니다.
* 모든 점자 디스플레이 드라이버는 이제 braille.BrailleDisplayDriver를 사용해야 하며, braille.BrailleDisplayDriverWithCursor는 더 이상 사용되지 않습니다.
  * 커서는 이제 드라이버 외부에서 관리됩니다.
  * 기존 드라이버는 클래스 선언을 적절히 변경하고 _display 메서드 이름을 display로 변경하기만 하면 됩니다.

## 2010.2

이 릴리스의 주목할 만한 기능으로는 객체 탐색의 대폭 단순화, Adobe Flash 콘텐츠를 위한 가상 버퍼, 화면에 쓰여진 텍스트를 검색하여 이전에 접근할 수 없었던 많은 컨트롤에 접근, 화면 텍스트의 평면 검토, IBM Lotus Symphony 문서 지원, Mozilla Firefox에서 테이블 행 및 열 헤더 보고, 그리고 사용자 문서의 대폭 개선이 포함됩니다.

### 새로운 기능

* 객체 탐색이 크게 단순화되었습니다. 이제 검토 커서는 사용자에게 유용하지 않은 객체(예: 레이아웃 목적으로만 사용되거나 접근할 수 없는 객체)를 제외합니다.
* Java Access Bridge를 사용하는 응용 프로그램(OpenOffice.org 포함)에서 텍스트 컨트롤의 서식을 보고할 수 있습니다. (#358, #463)
* Microsoft Excel에서 마우스를 셀 위로 이동할 때 NVDA가 적절히 셀을 발표합니다.
* Java Access Bridge를 사용하는 응용 프로그램에서 대화 상자가 나타날 때 대화 상자의 텍스트를 발표합니다. (#554)
* Adobe Flash 콘텐츠를 탐색하기 위해 가상 버퍼를 사용할 수 있습니다. 객체 탐색 및 포커스 모드를 켜서 컨트롤과 직접 상호작용하는 것도 여전히 지원됩니다. (#453)
* Eclipse IDE의 편집 가능한 텍스트 컨트롤(코드 편집기 포함)이 이제 접근 가능합니다. Eclipse 3.6 이상을 사용해야 합니다. (#256, #641)
* NVDA는 이제 화면에 쓰여진 대부분의 텍스트를 검색할 수 있습니다. (#40, #643)
  * 이를 통해 더 직접적이고 신뢰할 수 있는 방법으로 정보를 노출하지 않는 컨트롤을 읽을 수 있습니다.
  * 이 기능으로 접근 가능한 컨트롤에는 다음이 포함됩니다: 아이콘을 표시하는 일부 메뉴 항목(예: Windows XP에서 파일의 "다음으로 열기" 메뉴) (#151), Windows Live 응용 프로그램의 편집 가능한 텍스트 필드 (#200), Outlook Express의 오류 목록 (#582), TextPad의 편집 가능한 텍스트 컨트롤 (#605), Eudora의 목록, Australian E-tax의 많은 컨트롤, Microsoft Excel의 수식 입력줄.
* Microsoft Visual Studio 2005 및 2008의 코드 편집기에 대한 지원. 최소한 Visual Studio Standard가 필요하며, Express 에디션에서는 작동하지 않습니다. (#457)
* IBM Lotus Symphony 문서에 대한 지원.
* Google Chrome에 대한 초기 실험적 지원. Chrome의 화면 판독기 지원은 아직 완전하지 않으며 NVDA에서도 추가 작업이 필요할 수 있습니다. 이를 시도하려면 최신 개발 빌드의 Chrome이 필요합니다.
* Caps Lock, Num Lock 및 Scroll Lock과 같은 토글 키의 상태가 눌릴 때 점자로 표시됩니다. (#620)
* 도움말 풍선이 나타날 때 점자로 표시됩니다. (#652)
* MDV Lilli 점자 디스플레이를 위한 드라이버가 추가되었습니다. (#241)
* Microsoft Excel에서 단축키 shift+space 및 control+space로 전체 행 또는 열을 선택할 때 새 선택 항목이 발표됩니다. (#759)
* 테이블 행 및 열 헤더를 발표할 수 있습니다. 이는 문서 서식 설정 대화 상자에서 구성할 수 있습니다.
  * 현재 Mozilla 응용 프로그램(Firefox 3.6.11 이상, Thunderbird 3.1.5 이상) 문서에서 지원됩니다. (#361)
* 평면 검토를 위한 명령이 도입되었습니다: (#58)
  * NVDA+numpad7은 평면 검토로 전환하여 검토 커서를 현재 객체의 위치에 배치하고, 텍스트 검토 명령을 사용하여 화면(또는 문서 내에서)을 검토할 수 있게 합니다.
  * NVDA+numpad1은 검토 커서 위치의 텍스트가 나타내는 객체로 검토 커서를 이동하여 해당 지점에서 객체를 탐색할 수 있게 합니다.
* 현재 NVDA 사용자 설정을 일반 설정 대화 상자의 버튼을 눌러 Windows 로그인 화면 및 UAC 화면과 같은 보안 Windows 화면에서 사용할 수 있도록 복사할 수 있습니다. (#730)
* Mozilla Firefox 4에 대한 지원.
* Microsoft Internet Explorer 9에 대한 지원.

### 변경사항

* 탐색자 객체로 전체 읽기(NVDA+numpadAdd), 탐색자 객체 다음 흐름(NVDA+shift+numpad6), 탐색자 객체 이전 흐름(NVDA+shift+numpad4) 명령이 일시적으로 제거되었습니다. 이는 버그 문제와 다른 기능을 위한 키 확보를 위해서입니다.
* NVDA 음성 합성기 대화 상자에서는 이제 합성기의 표시 이름만 나열됩니다. 이전에는 드라이버 이름이 접두사로 붙었으나, 이는 내부적으로만 관련이 있습니다.
* 포함된 응용 프로그램 또는 다른 가상 버퍼 안의 가상 버퍼(예: Flash)에서 nvda+control+space를 눌러 포함된 응용 프로그램 또는 가상 버퍼에서 상위 문서로 이동할 수 있습니다. 이전에는 nvda+space가 사용되었으나, 이제 nvda+space는 가상 버퍼에서 탐색/포커스 모드 전환에만 사용됩니다.
* 도구 메뉴에서 활성화할 수 있는 음성 뷰어가 포커스를 받으면(예: 클릭된 경우), 포커스가 이동하기 전까지 새 텍스트가 표시되지 않습니다. 이를 통해 텍스트를 선택(예: 복사)하기가 더 쉬워집니다.
* 로그 뷰어와 Python 콘솔이 활성화되면 최대화됩니다.
* Microsoft Excel에서 워크시트에 포커스가 맞춰지고 여러 셀이 선택된 경우, 활성 셀만 발표되는 대신 선택 범위가 발표됩니다. (#763)
* 로그인 화면, UAC 및 기타 보안 Windows 화면에서 실행 중일 때 구성 저장 및 특정 민감한 옵션 변경이 비활성화됩니다.
* eSpeak 음성 합성기가 1.44.03으로 업데이트되었습니다.
* NVDA가 이미 실행 중인 경우, 바탕 화면의 NVDA 바로 가기(또는 control+alt+n)를 활성화하면 NVDA가 다시 시작됩니다.
* 마우스 설정 대화 상자에서 "마우스 아래 텍스트 보고" 체크박스가 제거되고, "마우스 추적 활성화" 체크박스로 대체되었습니다. 이는 마우스 추적 전환 스크립트(NVDA+m)와 더 잘 일치합니다.
* 랩톱 키보드 레이아웃이 업데이트되어 데스크탑 레이아웃에서 사용 가능한 모든 명령을 포함하며, 비영어 키보드에서도 올바르게 작동합니다. (#798, #800)
* 사용자 문서에 대한 중요한 개선 및 업데이트가 이루어졌으며, 랩톱 키보드 명령 문서화와 키보드 명령 빠른 참조와 사용자 가이드의 동기화가 포함됩니다. (#455)
* liblouis 점자 번역기가 2.1.1로 업데이트되었습니다. 특히, 이는 중국어 점자 및 번역 테이블에 정의되지 않은 문자와 관련된 몇 가지 문제를 해결합니다. (#484, #499)

### 버그 수정내역

* µTorrent에서 토렌트 목록의 포커스된 항목이 메뉴가 열려 있을 때 반복적으로 보고되거나 포커스를 빼앗는 문제가 수정되었습니다.
* µTorrent에서 토렌트 콘텐츠 목록의 파일 이름이 이제 보고됩니다.
* Mozilla 응용 프로그램에서 빈 테이블이나 트리에 포커스가 도달했을 때 올바르게 감지됩니다.
* Mozilla 응용 프로그램에서 체크 가능한 테이블 셀과 같은 체크 가능한 컨트롤에 대해 "체크되지 않음"이 올바르게 보고됩니다. (#571)
* Mozilla 응용 프로그램에서 올바르게 구현된 ARIA 대화 상자의 텍스트가 더 이상 무시되지 않으며, 대화 상자가 나타날 때 보고됩니다. (#630)
* Internet Explorer 및 기타 MSHTML 컨트롤에서 ARIA level 속성이 올바르게 적용됩니다.
* Internet Explorer 및 기타 MSHTML 컨트롤에서 ARIA 역할이 다른 유형 정보보다 우선적으로 선택되어 더 정확하고 예측 가능한 ARIA 경험을 제공합니다.
* Internet Explorer에서 프레임 또는 iFrame을 탐색할 때 발생하는 드문 충돌이 중단되었습니다.
* Microsoft Word 문서에서 오른쪽에서 왼쪽으로 쓰는 줄(예: 아랍어 텍스트)을 다시 읽을 수 있습니다. (#627)
* 64비트 시스템의 Windows 명령 콘솔에서 대량의 텍스트가 표시될 때 지연이 크게 줄어들었습니다. (#622)
* NVDA가 시작될 때 Skype가 이미 실행 중인 경우, 접근성을 활성화하기 위해 Skype를 다시 시작할 필요가 없습니다. 이는 시스템 화면 판독기 플래그를 확인하는 다른 응용 프로그램에도 적용될 수 있습니다.
* Microsoft Office 응용 프로그램에서 NVDA가 전경 읽기(NVDA+b)를 실행하거나 도구 모음의 일부 객체를 탐색할 때 더 이상 충돌하지 않습니다. (#616)
* 0이 구분자 뒤에 포함된 숫자(예: 1,023)가 잘못 읽히는 문제가 수정되었습니다. (#593)
* Adobe Acrobat Pro 및 Reader 9에서 파일을 닫거나 특정 작업을 수행할 때 더 이상 충돌하지 않습니다. (#613)
* Microsoft Word와 같은 일부 편집 가능한 텍스트 컨트롤에서 control+a를 눌러 모든 텍스트를 선택할 때 선택 항목이 이제 발표됩니다. (#761)
* Scintilla 컨트롤(예: Notepad++)에서 NVDA가 캐럿을 이동할 때(예: 전체 읽기 중) 텍스트가 잘못 선택되지 않습니다. (#746)
* Microsoft Excel의 셀 내용을 검토 커서를 사용하여 다시 검토할 수 있습니다.
* Internet Explorer 8의 특정 문제 있는 textArea 필드에서 줄 단위로 다시 읽을 수 있습니다. (#467)
* NVDA가 실행 중일 때 Windows Live Messenger 2009가 시작 직후 종료되는 문제가 해결되었습니다. (#677)
* 웹 브라우저에서 포함된 객체(예: Flash 콘텐츠)와 상호작용하기 위해 객체에서 Enter를 누른 후 또는 다른 응용 프로그램에서 돌아온 후 Tab을 누를 필요가 없습니다. (#775)
* Scintilla 컨트롤(예: Notepad++)에서 긴 줄이 화면 밖으로 스크롤될 때 시작 부분이 잘리지 않습니다. 또한, 이러한 긴 줄이 선택되었을 때 점자에 올바르게 표시됩니다.
* Loudtalks에서 연락처 목록에 접근할 수 있습니다.
* Internet Explorer 및 기타 MSHTML 컨트롤에서 문서의 URL과 "MSAAHTML Registered Handler"가 가끔 잘못 보고되지 않습니다. (#811)
* Eclipse IDE의 트리 뷰에서 포커스가 새 항목으로 이동할 때 이전에 포커스된 항목이 잘못 발표되지 않습니다.
* 현재 작업 디렉터리가 DLL 검색 경로에서 제거된 시스템(CWDIllegalInDllSearch 레지스트리 항목을 0xFFFFFFFF로 설정)에서도 NVDA가 올바르게 작동합니다. 이는 대부분의 사용자와는 관련이 없습니다. (#907)
* Microsoft Word에서 테이블 탐색 명령이 테이블 외부에서 사용될 때 "테이블의 가장자리"가 "테이블에 없음" 뒤에 더 이상 발표되지 않습니다. (#921)
* Microsoft Word에서 테이블 탐색 명령이 테이블 가장자리로 인해 이동할 수 없을 때 "테이블의 가장자리"가 항상 영어로 발표되지 않고 NVDA에 설정된 언어로 발표됩니다. (#921)
* Outlook Express, Windows Mail 및 Windows Live Mail에서 메시지 규칙 목록의 체크박스 상태가 이제 보고됩니다. (#576)
* Windows Live Mail 2010에서 메시지 규칙의 설명을 읽을 수 있습니다.

## 2010.1

이 릴리스는 주로 버그 수정과 사용자 경험 개선에 중점을 두었으며, 몇 가지 중요한 안정성 수정이 포함되어 있습니다.

### 새로운 기능

* NVDA는 이제 오디오 출력 장치가 없는 시스템에서도 시작에 실패하지 않습니다. 이 경우 출력은 점자 디스플레이나 Speech Viewer와 함께 사용하는 Silence 음성 합성기를 통해 이루어져야 합니다. (#425)
* 문서 서식 설정 대화 상자에 랜드마크 보고 체크박스가 추가되어, NVDA가 웹 문서에서 랜드마크를 발표할지 여부를 구성할 수 있습니다. 이전 릴리스와의 호환성을 위해 이 옵션은 기본적으로 활성화되어 있습니다.
* 명령 키 읽기가 활성화된 경우, NVDA는 이제 많은 키보드에서 멀티미디어 키(예: 재생, 정지, 홈페이지 등)의 이름을 발표합니다. (#472)
* NVDA는 이제 control+backspace를 눌러 단어를 삭제할 때 삭제되는 단어를 발표합니다. (#491)
* 화살표 키를 사용하여 웹 포매터 창에서 텍스트를 탐색하고 읽을 수 있습니다. (#452)
* Microsoft Office Outlook 주소록의 항목 목록이 이제 지원됩니다.
* NVDA는 Internet Explorer에서 포함된 편집 가능한(디자인 모드) 문서를 더 잘 지원합니다. (#402)
* 새로운 스크립트(nvda+shift+numpadMinus)를 사용하여 시스템 포커스를 현재 내비게이터 객체로 이동할 수 있습니다.
* 드래그 앤 드롭 작업을 수행할 때 유용한 왼쪽 및 오른쪽 마우스 버튼 잠금/해제 스크립트가 추가되었습니다. shift+numpadDivide로 왼쪽 버튼 잠금/해제, shift+numpadMultiply로 오른쪽 버튼 잠금/해제.
* 새로운 점자 번역 테이블: 독일어 8점 컴퓨터 점자, 독일어 2단계, 핀란드어 8점 컴퓨터 점자, 중국어(홍콩, 광둥어), 중국어(대만, 만다린). (#344, #369, #415, #450)
* NVDA 설치 시 바탕 화면 바로 가기(및 바로 가기 키) 생성을 비활성화할 수 있는 옵션이 추가되었습니다. (#518)
* NVDA는 이제 64비트 응용 프로그램에서 IAccessible2를 사용할 수 있습니다. (#479)
* Mozilla 응용 프로그램에서 라이브 영역 지원이 개선되었습니다. (#246)
* NVDA 컨트롤러 클라이언트 API가 제공되어 응용 프로그램이 NVDA를 제어할 수 있습니다. 예: 텍스트 읽기, 음성 중지, 점자에 메시지 표시 등.
* Windows Vista 및 Windows 7의 로그인 화면에서 정보 및 오류 메시지가 읽힙니다. (#506)
* Adobe Reader에서 Adobe LiveCycle로 개발된 PDF 대화형 양식이 이제 지원됩니다. (#475)
* Miranda IM에서 동적 콘텐츠 변경 보고가 활성화된 경우, NVDA는 채팅 창에서 들어오는 메시지를 자동으로 읽습니다. 또한, 세 가지 최신 메시지를 보고하는 명령(NVDA+control+숫자)이 추가되었습니다. (#546)
* Adobe Flash 콘텐츠에서 입력 텍스트 필드가 이제 지원됩니다. (#461)

### 변경사항

* Windows 7 시작 메뉴에서 지나치게 자세한 키보드 도움말 메시지가 더 이상 보고되지 않습니다.
* Display synth가 새로운 Speech Viewer로 대체되었습니다. 이를 활성화하려면 도구 메뉴에서 Speech Viewer를 선택하십시오. Speech Viewer는 사용 중인 음성 합성기와 독립적으로 사용할 수 있습니다. (#44)
* 점자 디스플레이의 메시지는 포커스 이동과 같은 변경을 초래하는 키를 사용자가 누르면 자동으로 해제됩니다. 이전에는 메시지가 항상 설정된 시간 동안 유지되었습니다.
* 점자가 포커스 또는 검토 커서에 연결될지 여부(NVDA+control+t)는 이제 점자 설정 대화 상자에서도 설정할 수 있으며, 사용자의 구성에 저장됩니다.
* eSpeak 음성 합성기가 1.43으로 업데이트되었습니다.
* liblouis 점자 번역기가 1.8.0으로 업데이트되었습니다.
* 가상 버퍼에서 문자 또는 단어 단위로 이동할 때 요소 보고가 크게 개선되었습니다. 이전에는 많은 관련 없는 정보가 보고되었으며, 줄 단위로 이동할 때와 매우 다르게 보고되었습니다. (#490)
* Control 키는 이제 다른 키처럼 단순히 음성을 중지하며, 음성을 일시 중지하지 않습니다. 음성을 일시 중지/재개하려면 Shift 키를 사용하십시오.
* 테이블 행 및 열 수는 포커스 변경 사항을 보고할 때 더 이상 발표되지 않습니다. 이 발표는 지나치게 자세하고 일반적으로 유용하지 않습니다.

### 버그 수정내역

* NVDA는 UI Automation 지원이 사용 가능해 보이지만 초기화에 실패하는 경우에도 더 이상 시작에 실패하지 않습니다. (#483)
* Mozilla 응용 프로그램에서 셀 내부로 포커스를 이동할 때 테이블 행의 전체 내용이 가끔 잘못 발표되는 문제가 수정되었습니다. (#482)
* 매우 많은 하위 항목을 포함하는 트리 뷰 항목을 확장할 때 NVDA가 오랫동안 지연되지 않도록 수정되었습니다.
* SAPI 5 음성을 나열할 때, NVDA는 이제 결함이 있는 음성을 감지하고 이를 음성 설정 대화 상자와 음성 합성기 설정 링에서 제외합니다. 이전에는 문제가 있는 음성이 하나만 있어도 NVDA의 SAPI 5 드라이버가 가끔 시작에 실패하곤 했습니다.
* 가상 버퍼는 이제 객체 프레젠테이션 대화 상자에서 설정된 객체 바로 가기 키 보고 설정을 준수합니다. (#486)
* 가상 버퍼에서 테이블 보고가 비활성화된 경우, 행/열 헤더에 대해 잘못된 행/열 좌표가 읽히는 문제가 수정되었습니다.
* 가상 버퍼에서 테이블을 나갔다가 동일한 테이블 셀로 다시 들어갈 때, 다른 셀을 방문하지 않아도 행/열 좌표가 올바르게 읽히도록 수정되었습니다. 예: 테이블의 첫 번째 셀에서 위쪽 화살표를 누른 후 아래쪽 화살표를 누를 때. (#378)
* Microsoft Word 문서와 Microsoft HTML 편집 컨트롤에서 빈 줄이 점자 디스플레이에 적절히 표시됩니다. 이전에는 이러한 상황에서 현재 줄이 아닌 현재 문장이 디스플레이에 표시되었습니다. (#420)
* Windows 로그인 및 기타 보안 데스크탑에서 NVDA를 실행할 때 여러 보안 문제가 수정되었습니다. (#515)
* 표준 Windows 편집 필드와 Microsoft Word 문서에서 화면 하단을 넘어가는 Say All을 수행할 때 커서 위치(캐럿)가 올바르게 업데이트됩니다. (#418)
* 가상 버퍼에서 스크린 리더에 무관한 것으로 표시된 링크 및 클릭 가능한 이미지 내부의 텍스트가 잘못 포함되지 않도록 수정되었습니다. (#423)
* 랩톱 키보드 레이아웃과 관련된 문제가 수정되었습니다. (#517)
* 점자가 검토에 연결된 상태에서 Dos 콘솔 창에 포커스를 맞출 경우, 검토 커서가 콘솔의 텍스트를 제대로 탐색할 수 있습니다.
* TeamTalk3 또는 TeamTalk4 Classic을 사용할 때, 메인 창의 VU 미터 진행률 표시줄이 업데이트될 때 더 이상 발표되지 않습니다. 또한, 채팅 창에서 특수 문자가 올바르게 읽힙니다.
* Windows 7 시작 메뉴에서 항목이 두 번 발표되는 문제가 수정되었습니다. (#474)
* Firefox 3.6에서 동일 페이지 링크를 활성화하면 가상 버퍼의 커서가 페이지의 올바른 위치로 적절히 이동합니다.
* 특정 PDF 문서에서 Adobe Reader에서 일부 텍스트가 렌더링되지 않는 문제가 수정되었습니다.
* NVDA가 특정 숫자(예: 500-1000)를 잘못 읽는 문제가 수정되었습니다. (#547)
* Windows XP에서 Windows Update에서 체크박스를 전환할 때 Internet Explorer가 멈추는 문제가 수정되었습니다. (#477)
* 내장된 eSpeak 합성기를 사용할 때, 동시 음성과 비프음이 간헐적으로 일부 시스템에서 멈추는 문제가 수정되었습니다. 예: Windows 탐색기에서 대량의 데이터를 복사할 때.
* NVDA가 백그라운드에 있는 Firefox 문서가 바빠졌다고 잘못 발표하지 않도록 수정되었습니다. 이로 인해 포그라운드 응용 프로그램의 상태 표시줄이 잘못 발표되는 문제도 해결되었습니다.
* Windows 키보드 레이아웃을 전환할 때(control+shift 또는 alt+shift), 레이아웃의 전체 이름이 음성과 점자로 발표됩니다. 이전에는 음성으로만 발표되었으며, 대체 레이아웃(예: Dvorak)은 전혀 발표되지 않았습니다.
* 테이블 보고가 비활성화된 경우, 포커스가 변경될 때 테이블 정보가 발표되지 않도록 수정되었습니다.
* 64비트 응용 프로그램의 특정 표준 트리 뷰 컨트롤(예: Microsoft HTML 도움말의 콘텐츠 트리 뷰)이 이제 접근 가능합니다. (#473)
* 비ASCII 문자가 포함된 메시지 로깅과 관련된 몇 가지 문제가 수정되었습니다. 이는 비영어권 시스템에서 일부 경우에 오류를 유발할 수 있었습니다. (#581)
* NVDA 정보 대화 상자의 정보가 항상 영어로 표시되는 대신 사용자가 설정한 언어로 표시됩니다. (#586)
* 음성 합성기 설정 링을 사용할 때, 이전 음성보다 설정이 적은 음성으로 변경한 후 문제가 발생하지 않도록 수정되었습니다.
* Skype 4.2에서 연락처 목록의 연락처 이름이 두 번 발표되는 문제가 수정되었습니다.
* GUI와 가상 버퍼에서 잠재적인 주요 메모리 누수가 수정되었습니다. (#590, #591)
* 일부 SAPI 4 합성기의 심각한 버그를 우회하여 NVDA에서 빈번한 오류와 충돌을 유발하던 문제를 해결했습니다. (#597)

## 2009.1

이 릴리스의 주요 하이라이트는 64비트 Windows 에디션 지원, Microsoft Internet Explorer 및 Adobe Reader 문서에 대한 대폭 개선된 지원, Windows 7 지원, Windows 로그인 화면, control+alt+delete 및 사용자 계정 컨트롤(UAC) 화면 읽기, 그리고 웹 페이지에서 Adobe Flash 및 Sun Java 콘텐츠와 상호작용할 수 있는 기능을 포함합니다. 또한 몇 가지 중요한 안정성 수정과 일반 사용자 경험의 개선이 이루어졌습니다.

### 새로운 기능

* 공식적으로 64비트 Windows 에디션을 지원합니다! (#309)
* Newfon 음성 합성기를 위한 드라이버를 추가했습니다. 이 드라이버는 특별한 버전의 Newfon이 필요합니다. (#206)
* 가상 버퍼에서 포커스 모드와 탐색 모드를 음성 대신 소리로 보고할 수 있습니다. 이 기능은 기본적으로 활성화되어 있으며, 가상 버퍼 설정 대화 상자에서 구성할 수 있습니다. (#244)
* 키보드의 볼륨 조절 키를 눌렀을 때 NVDA가 음성을 취소하지 않도록 수정하여, 사용자가 볼륨을 변경하고 즉시 결과를 들을 수 있습니다. (#287)
* Microsoft Internet Explorer와 Adobe Reader 문서에 대한 지원을 완전히 새로 작성했습니다. 이 지원은 Mozilla Gecko에 사용된 핵심 지원과 통합되어, 빠른 페이지 렌더링, 광범위한 빠른 탐색, 링크 목록, 텍스트 선택, 자동 포커스 모드 및 점자 지원과 같은 기능이 이제 이러한 문서에서도 가능합니다.
* Windows Vista 날짜/시간 속성 대화 상자에 있는 날짜 선택 컨트롤에 대한 지원이 개선되었습니다.
* Modern XP/Vista 시작 메뉴(특히 모든 프로그램 및 장소 메뉴)에 대한 지원이 개선되었습니다. 적절한 수준 정보가 이제 발표됩니다.
* 마우스를 이동할 때 발표되는 텍스트의 양을 마우스 설정 대화 상자에서 구성할 수 있습니다. 문단, 줄, 단어 또는 문자 중에서 선택할 수 있습니다.
* Microsoft Word에서 커서 아래의 철자 오류를 발표합니다.
* Microsoft Word 2007 맞춤법 검사기를 지원합니다. 이전 Microsoft Word 버전에서도 일부 지원이 가능할 수 있습니다.
* Windows Live Mail에 대한 지원이 개선되었습니다. 일반 텍스트 메시지를 읽을 수 있으며, 일반 텍스트 및 HTML 메시지 작성기를 사용할 수 있습니다.
* Windows Vista에서 사용자가 보안 데스크탑으로 이동할 경우(UAC 제어 대화 상자가 나타나거나 control+alt+delete를 눌렀을 때), NVDA가 사용자가 보안 데스크탑에 있다는 사실을 발표합니다.
* NVDA는 DOS 콘솔 창 내에서 마우스 아래의 텍스트를 발표할 수 있습니다.
* Windows 7에서 제공되는 UI Automation 클라이언트 API를 통해 UI Automation을 지원하며, Windows 7에서 NVDA의 경험을 개선하기 위한 수정 사항이 포함되었습니다.
* NVDA를 Windows에 로그인한 후 자동으로 시작하도록 구성할 수 있습니다. 이 옵션은 일반 설정 대화 상자에 있습니다.
* NVDA는 Windows XP 이상에서 Windows 로그인 화면, control+alt+delete 및 사용자 계정 컨트롤(UAC) 화면과 같은 보안 Windows 화면을 읽을 수 있습니다. Windows 로그인 화면 읽기는 일반 설정 대화 상자에서 구성할 수 있습니다. (#97)
* Optelec ALVA BC6 시리즈 점자 디스플레이를 위한 드라이버를 추가했습니다.
* 웹 문서를 탐색할 때, n과 shift+n을 눌러 링크 블록을 앞으로 또는 뒤로 건너뛸 수 있습니다.
* 웹 문서를 탐색할 때, ARIA 랜드마크가 이제 발표되며, d와 shift+d를 사용하여 앞으로 또는 뒤로 이동할 수 있습니다. (#192)
* 웹 문서를 탐색할 때 사용할 수 있는 링크 목록 대화 상자가 이제 요소 목록 대화 상자가 되어, 링크, 제목 및 랜드마크를 나열할 수 있습니다. 제목과 랜드마크는 계층적으로 표시됩니다. (#363)
* 새로운 요소 목록 대화 상자에는 "필터 기준" 필드가 포함되어 있어 입력된 텍스트를 포함하는 항목만 목록에 표시되도록 필터링할 수 있습니다. (#173)
* NVDA의 휴대용 버전은 이제 NVDA 디렉터리 내의 'userConfig' 디렉터리에서 사용자 구성을 찾습니다. 설치 버전과 마찬가지로, 사용자의 구성을 NVDA 자체와 분리하여 유지합니다.
* 사용자 정의 앱 모듈, 점자 디스플레이 드라이버 및 음성 합성기 드라이버를 이제 사용자의 구성 디렉터리에 저장할 수 있습니다. (#337)
* 가상 버퍼는 이제 백그라운드에서 렌더링되며, 렌더링 프로세스 중에도 사용자가 시스템과 어느 정도 상호작용할 수 있습니다. 문서 렌더링에 1초 이상 걸리는 경우, 사용자에게 문서가 렌더링 중임을 알립니다.
* NVDA가 어떤 이유로 멈춘 것을 감지하면, 모든 키 입력을 자동으로 통과시켜 사용자가 시스템을 복구할 가능성을 높입니다.
* Mozilla Gecko에서 ARIA 드래그 앤 드롭을 지원합니다. (#239)
* 가상 버퍼 내에서 포커스를 이동할 때 문서 제목과 현재 줄 또는 선택 항목이 발표됩니다. 이를 통해 가상 버퍼로 포커스를 이동할 때의 동작이 일반 문서 객체와 일관성을 갖습니다. (#210)
* 가상 버퍼에서, 포함된 객체(예: Adobe Flash 및 Sun Java 콘텐츠)와 상호작용하려면 객체에서 Enter 키를 누릅니다. 접근 가능하다면, 다른 응용 프로그램처럼 Tab 키로 탐색할 수 있습니다. 문서로 포커스를 다시 이동하려면 NVDA+space를 누릅니다. (#431)
* 가상 버퍼에서, o와 shift+o를 사용하여 다음 및 이전 포함 객체로 이동할 수 있습니다.
* NVDA는 이제 Windows Vista 이상에서 관리자 권한으로 실행 중인 응용 프로그램에 완전히 접근할 수 있습니다. 이를 위해 NVDA의 공식 릴리스를 설치해야 합니다. 이 기능은 휴대용 버전 및 스냅샷에서는 작동하지 않습니다. (#397)

### 변경사항

* NVDA가 시작될 때 더 이상 "NVDA 시작됨"을 발표하지 않습니다.
* 시작 및 종료 사운드는 이제 Windows 기본 오디오 출력 장치 대신 NVDA에서 구성된 오디오 출력 장치를 사용하여 재생됩니다. (#164)
* 진행률 표시줄 보고가 개선되었습니다. 특히, 이제 NVDA가 음성과 비프음을 동시에 발표하도록 구성할 수 있습니다.
* 패널, 응용 프로그램, 프레임과 같은 일부 일반적인 역할은 컨트롤에 이름이 없는 경우를 제외하고는 초점에서 더 이상 발표되지 않습니다.
* 검토 복사 명령(NVDA+f10)은 시작 마커부터 현재 검토 위치까지의 텍스트를 포함하여 복사합니다. 이전에는 현재 위치를 제외하고 복사했기 때문에 줄의 마지막 문자를 복사할 수 없었습니다. (#430)
* navigatorObject_where 스크립트(ctrl+NVDA+numpad5)가 제거되었습니다. 이 키 조합은 일부 키보드에서 작동하지 않았으며, 스크립트가 유용하지 않은 것으로 판단되었습니다.
* navigatorObject_currentDimentions 스크립트가 NVDA+numpadDelete로 다시 매핑되었습니다. 이전 키 조합은 일부 키보드에서 작동하지 않았습니다. 이 스크립트는 이제 객체의 오른쪽/아래쪽 좌표 대신 너비와 높이를 보고합니다.
* 많은 비프음이 빠르게 연속적으로 발생할 때(예: 오디오 좌표가 활성화된 상태에서 빠른 마우스 이동) 성능이 개선되었습니다. 특히 넷북에서 효과적입니다. (#396)
* NVDA 오류 사운드는 이제 릴리스 후보 및 최종 릴리스에서 더 이상 재생되지 않습니다. 오류는 여전히 로그에 기록됩니다.

### 버그 수정내역

* NVDA가 8.3 도스 경로에서 실행되지만 관련 긴 경로(예: progra~1 대 program files)에 설치된 경우, NVDA는 설치된 복사본임을 올바르게 인식하고 사용자의 설정을 제대로 로드합니다.
* NVDA+t로 현재 전경 창의 제목을 읽는 기능이 메뉴 안에서도 올바르게 작동합니다.
* 점자 디스플레이에서 초점 컨텍스트에 불필요한 정보(예: 레이블이 없는 창)가 더 이상 표시되지 않습니다.
* Java 또는 Lotus 응용 프로그램에서 루트 창, 계층 창, 스크롤 창과 같은 초점 변경 시 불필요한 정보가 더 이상 발표되지 않습니다.
* Windows 도움말(CHM) 뷰어의 키워드 검색 필드를 훨씬 더 사용하기 쉽게 개선했습니다. 해당 컨트롤의 버그로 인해 현재 키워드를 읽을 수 없었으며, 키워드가 계속 변경되는 문제가 있었습니다.
* Microsoft Word에서 페이지 번호가 문서에서 특정 오프셋으로 설정된 경우 올바른 페이지 번호를 보고합니다.
* Microsoft Word 대화 상자(예: 글꼴 대화 상자)에서 발견되는 편집 필드에 대한 지원이 개선되었습니다. 이제 화살표 키로 이러한 컨트롤을 탐색할 수 있습니다.
* Dos 콘솔에 대한 지원이 개선되었습니다. 특히, NVDA가 항상 빈 것으로 간주했던 특정 콘솔의 내용을 읽을 수 있습니다. 또한 control+break를 눌러도 NVDA가 종료되지 않습니다.
* Windows Vista 이상에서 NVDA 설치 프로그램이 완료 화면에서 NVDA 실행을 요청받을 경우, NVDA를 일반 사용자 권한으로 시작합니다.
* 단어 입력 읽기 기능에서 백스페이스가 올바르게 처리됩니다. (#306)
* Windows 탐색기/Windows 셸의 특정 컨텍스트 메뉴에서 "시작 메뉴"를 잘못 보고하지 않습니다. (#257)
* NVDA는 이제 Mozilla Gecko에서 다른 유용한 콘텐츠가 없을 때 ARIA 레이블을 올바르게 처리합니다. (#156)
* NVDA는 더 이상 초점이 변경될 때 값이 업데이트되는 편집 가능한 텍스트 필드(예: http://tigerdirect.com/)에 대해 초점 모드를 자동으로 활성화하지 않습니다. (#220)
* NVDA는 이전에 완전히 멈췄을 상황에서 복구를 시도합니다. NVDA가 이러한 멈춤을 감지하고 복구하는 데 최대 10초가 걸릴 수 있습니다.
* NVDA 언어가 "사용자 기본값"으로 설정된 경우, Windows 로캘 설정 대신 사용자의 Windows 표시 언어 설정을 사용합니다. (#353)
* NVDA는 AIM 7에서 컨트롤의 존재를 인식합니다.
* 특수 키 전달 명령이 키가 눌린 상태로 유지될 경우 더 이상 멈추지 않습니다. 이전에는 NVDA가 명령을 수락하지 않게 되어 재시작해야 했습니다. (#413)
* 작업 표시줄이 초점을 받을 때 더 이상 무시되지 않습니다. 이는 응용 프로그램을 종료할 때 자주 발생합니다. 이전에는 NVDA가 초점이 전혀 변경되지 않은 것처럼 작동했습니다.
* Java Access Bridge를 사용하는 응용 프로그램(예: OpenOffice.org)에서 텍스트 필드를 읽을 때, 줄 번호 보고가 활성화된 경우에도 NVDA가 올바르게 작동합니다.
* 검토 복사 명령(NVDA+f10)은 시작 마커 이전 위치에서 사용될 경우에도 문제없이 처리합니다. 이전에는 Notepad++에서 충돌과 같은 문제가 발생할 수 있었습니다.
* 특정 제어 문자(0x1)가 텍스트에서 발견될 때 eSpeak의 이상한 동작(예: 볼륨 및 음높이 변경)을 더 이상 유발하지 않습니다. (#437)
* 텍스트 선택을 지원하지 않는 객체에서 텍스트 선택 보고 명령(NVDA+shift+upArrow)이 이제 선택 항목이 없음을 우아하게 보고합니다.
* 특정 Miranda-IM 버튼이나 링크에서 Enter 키를 누를 때 NVDA가 멈추는 문제를 수정했습니다. (#440)
* 현재 줄이나 선택 항목이 현재 내비게이터 객체를 철자하거나 복사할 때 올바르게 반영됩니다.
* Windows의 버그를 우회하여 Windows 탐색기 및 Internet Explorer 대화 상자에서 링크 컨트롤 이름 뒤에 쓰레기 값이 발표되는 문제를 해결했습니다. (#451)
* 날짜 및 시간 보고 명령(NVDA+f12)과 관련된 문제를 수정했습니다. 이전에는 일부 시스템에서 날짜 보고가 잘렸습니다. (#471)
* 보안 Windows 화면과 상호 작용한 후 시스템 화면 판독기 플래그가 부적절하게 해제되는 문제를 수정했습니다. 이는 Skype, Adobe Reader 및 Jart를 포함한 화면 판독기 플래그를 확인하는 응용 프로그램에서 문제를 일으킬 수 있었습니다. (#462)
* Internet Explorer 6 콤보 상자에서 활성 항목이 변경될 때 이를 보고합니다. (#342)

## 0.6p3

### 새로운 기능

* Microsoft Excel의 수식 입력줄이 NVDA에서 접근할 수 없으므로, 사용자가 셀에서 f2를 누를 때 NVDA 전용 편집 대화 상자를 제공합니다.
* IAccessible2 텍스트 컨트롤(예: Mozilla 응용 프로그램)에서 서식 지원.
* 가능한 경우 철자 오류를 보고할 수 있습니다. 이는 문서 서식 설정 대화 상자에서 구성할 수 있습니다.
* NVDA는 모든 진행률 표시줄 또는 보이는 진행률 표시줄에 대해 비프음을 울리도록 구성할 수 있습니다. 또는 진행률 표시줄 값을 10%마다 말하도록 구성할 수 있습니다.
* 리치에디트 컨트롤에서 링크를 식별할 수 있습니다.
* 대부분의 편집 가능한 텍스트 컨트롤에서 검토 커서 아래의 문자로 마우스를 이동할 수 있습니다. 이전에는 컨트롤의 중앙으로만 마우스를 이동할 수 있었습니다.
* 가상 버퍼에서 검토 커서는 이제 내비게이터 객체의 내부 텍스트(사용자에게 종종 유용하지 않음)가 아닌 버퍼의 텍스트를 검토합니다. 이를 통해 객체 탐색을 사용하여 가상 버퍼를 계층적으로 탐색할 수 있으며, 검토 커서가 해당 지점으로 이동합니다.
* Java 컨트롤에서 추가 상태를 처리합니다.
* 제목 명령(NVDA+t)을 두 번 누르면 제목을 철자합니다. 세 번 누르면 제목이 클립보드에 복사됩니다.
* 키보드 입력 도움말이  키를 단독으로 눌렀을 때 이름을 읽습니다.
* 키보드 입력 도움말에서 발표되는 키 이름은 이제 번역 가능합니다.
* SiRecognizer에서 인식된 텍스트 필드를 지원합니다. (#198)
* 점자 디스플레이 지원 추가!
* Windows 클립보드의 텍스트를 보고하는 명령(NVDA+c)을 추가했습니다. (#193)
* 가상 버퍼에서 NVDA가 자동으로 포커스 모드로 전환되면, Esc 키를 사용하여 탐색 모드로 다시 전환할 수 있습니다. NVDA+space도 여전히 사용할 수 있습니다.
* 가상 버퍼에서 포커스가 변경되거나 캐럿이 이동할 때, NVDA는 캐럿 아래 컨트롤에 적합하게 자동으로 포커스 모드 또는 탐색 모드로 전환할 수 있습니다. 이는 가상 버퍼 대화 상자에서 구성됩니다. (#157)
* SAPI4 음성 합성기 드라이버를 새로 작성하여 sapi4serotek 및 sapi4activeVoice 드라이버를 대체하며, 이 드라이버에서 발생한 문제를 해결합니다.
* NVDA 응용 프로그램에 매니페스트가 포함되어 이제 Windows Vista에서 호환 모드로 실행되지 않습니다.
* NVDA가 설치 프로그램을 사용하여 설치된 경우, 구성 파일과 음성 사전은 사용자의 응용 프로그램 데이터 디렉터리에 저장됩니다. 이는 Windows Vista에 필요하며, 여러 사용자가 개별 NVDA 구성을 가질 수 있도록 합니다.
* IAccessible2 컨트롤에 대한 위치 정보 지원 추가.
* 검토 커서를 사용하여 텍스트를 클립보드에 복사할 수 있는 기능을 추가했습니다. NVDA+f9는 검토 커서의 현재 위치에 시작 마커를 설정합니다. NVDA+f10은 시작 마커와 검토 커서의 현재 위치 사이의 텍스트를 가져와 클립보드에 복사합니다. (#240)
* 피나클 TV 소프트웨어의 일부 편집 컨트롤 지원 추가.
* 긴 선택 영역(512자 이상)에 대해 선택된 텍스트를 발표할 때, NVDA는 전체 선택 영역을 말하는 대신 선택된 문자 수를 말합니다. (#249)

### 변경사항

* 오디오 출력 장치가 Windows 기본 장치(Microsoft Sound Mapper)를 사용하도록 설정된 경우, 기본 장치가 변경되면 NVDA는 eSpeak 및 톤에 대해 새로운 기본 장치로 전환합니다. 예를 들어, USB 오디오 장치가 연결될 때 자동으로 기본 장치가 되면 NVDA는 해당 장치로 전환합니다.
* 일부 Windows Vista 오디오 드라이버에서 eSpeak의 성능을 개선했습니다.
* 링크, 제목, 표, 목록 및 블록 인용의 보고를 이제 문서 서식 설정 대화상자에서 구성할 수 있습니다. 이전에는 가상 버퍼 설정 대화상자를 사용하여 이러한 설정을 구성해야 했습니다. 이제 모든 문서가 이 구성을 공유합니다.
* 음성 합성기 설정 링에서 속도가 기본 설정이 되었습니다.
* 앱 모듈의 로드 및 언로드를 개선했습니다.
* 제목 명령(NVDA+t)은 이제 전체 객체 대신 제목만 보고합니다. 전경 객체에 이름이 없는 경우, 응용 프로그램의 프로세스 이름이 사용됩니다.
* 가상 버퍼 패스스루 켜기 및 끄기 대신, NVDA는 이제 포커스 모드(패스스루 켜짐)와 탐색 모드(패스스루 꺼짐)를 보고합니다.
* 음성은 이제 인덱스 대신 ID로 구성 파일에 저장됩니다. 이를 통해 시스템 및 구성 변경 간 음성 설정의 신뢰성이 향상됩니다. 음성 설정은 이전 구성에서 유지되지 않으며, 음성 합성기를 처음 사용할 때 오류가 기록될 수 있습니다. (#19)
* 모든 트리 뷰에서 이전에 포커스된 항목과 다른 수준의 트리 뷰 항목이 포커스될 경우, 해당 수준이 먼저 발표됩니다. 이전에는 Windows 기본(SysTreeView32) 트리 뷰에서만 이 기능이 작동했습니다.

### 버그 수정내역

* NVDA가 eSpeak를 사용하는 원격 데스크탑 서버에서 마지막 오디오 조각이 잘리는 문제가 해결되었습니다.
* 특정 음성에 대한 음성 사전을 저장하는 문제를 수정했습니다.
* Mozilla Gecko 가상 버퍼에서 큰 일반 텍스트 문서의 하단으로 단어, 줄 등 문자 이외의 단위로 이동할 때 발생하는 지연을 제거했습니다. (#155)
* 입력한 단어 읽기가 활성화된 경우, Enter 키를 누를 때 단어를 발표합니다.
* 리치에디트 문서에서 발생하는 일부 문자 집합 문제를 수정했습니다.
* NVDA 로그 뷰어가 로그를 표시하기 위해 단순 편집 대신 리치에디트를 사용하도록 변경되었습니다. 이를 통해 NVDA로 단어 단위로 읽기가 개선되었습니다.
* 리치에디트 컨트롤에 포함된 객체와 관련된 몇 가지 문제를 수정했습니다.
* NVDA가 Microsoft Word에서 페이지 번호를 읽도록 수정되었습니다. (#120)
* Mozilla Gecko 가상 버퍼에서 체크된 체크박스로 탭 이동 후 스페이스 키를 눌렀을 때 체크박스가 체크 해제되는 것을 발표하지 않는 문제를 수정했습니다.
* Mozilla 응용 프로그램에서 부분적으로 체크된 체크박스를 올바르게 보고합니다.
* 텍스트 선택이 양방향으로 확장되거나 축소될 경우, 선택 영역을 두 개가 아닌 하나의 덩어리로 읽습니다.
* 마우스로 읽을 때, Mozilla Gecko 편집 필드의 텍스트를 읽도록 수정되었습니다.
* Say all 기능이 특정 SAPI5 음성 합성기를 충돌시키지 않도록 수정되었습니다.
* NVDA가 시작된 후 첫 번째 포커스 변경 이전에 Windows 표준 편집 컨트롤에서 텍스트 선택 변경 사항이 읽히지 않는 문제를 수정했습니다.
* Java 객체에서 마우스 추적 문제를 수정했습니다. (#185)
* NVDA가 자식이 없는 Java 트리뷰 항목을 축소된 상태로 보고하지 않도록 수정되었습니다.
* Java 창이 전경으로 올 때 포커스된 객체를 발표합니다. 이전에는 최상위 Java 객체만 발표되었습니다.
* eSpeak 음성 합성기 드라이버가 단일 오류 후 완전히 멈추지 않도록 수정되었습니다.
* 음성 매개변수(속도, 음높이 등)가 업데이트된 후 음성이 합성기 설정 링에서 변경되었을 때 저장되지 않는 문제를 수정했습니다.
* 입력한 문자와 단어를 발표하는 기능을 개선했습니다.
* 이전에 텍스트 콘솔 응용 프로그램(예: 일부 텍스트 어드벤처 게임)에서 발표되지 않았던 새로운 텍스트가 이제 발표됩니다.
* NVDA가 백그라운드 창의 포커스 변경을 무시하도록 수정되었습니다. 이전에는 백그라운드 포커스 변경이 실제 포커스 변경으로 처리될 수 있었습니다.
* 컨텍스트 메뉴를 나갈 때 포커스를 감지하는 기능을 개선했습니다. 이전에는 컨텍스트 메뉴를 나갈 때 NVDA가 전혀 반응하지 않는 경우가 많았습니다.
* NVDA가 시작 메뉴에서 컨텍스트 메뉴가 활성화되었을 때 이를 발표합니다.
* 클래식 시작 메뉴를 응용 프로그램 메뉴 대신 시작 메뉴로 발표합니다.
* Mozilla Firefox에서 발생하는 경고와 같은 알림을 읽는 기능을 개선했습니다. 텍스트가 여러 번 읽히거나 불필요한 정보가 읽히지 않도록 수정되었습니다. (#248)
* 포커스 가능한 읽기 전용 편집 필드의 텍스트가 대화 상자의 텍스트를 가져올 때 포함되지 않도록 수정되었습니다. 이를 통해 설치 프로그램에서 전체 라이선스 계약이 자동으로 읽히는 문제를 해결했습니다.
* 일부 편집 컨트롤(예: Internet Explorer 주소 표시줄, Thunderbird 3 이메일 주소 필드)을 나갈 때 텍스트 선택 해제가 발표되지 않도록 수정되었습니다.
* Outlook Express 및 Windows Mail에서 일반 텍스트 이메일을 열 때 포커스가 메시지에 올바르게 배치되도록 수정되었습니다. 이전에는 사용자가 커서 키를 사용해 읽기 위해 탭을 누르거나 메시지를 클릭해야 했습니다.
* "명령 키 읽기" 기능과 관련된 여러 주요 문제를 수정했습니다.
* NVDA가 표준 편집 컨트롤에서 65535자를 초과하는 텍스트를 읽을 수 있도록 수정되었습니다(예: Notepad에서 큰 파일).
* MSHTML 편집 필드(Outlook Express 편집 가능한 메시지 및 Internet Explorer 텍스트 입력 필드)에서 줄 읽기 기능을 개선했습니다.
* OpenOffice에서 텍스트를 편집할 때 NVDA가 완전히 멈추는 문제가 수정되었습니다. (#148, #180)

## 0.6p2

* NVDA의 기본 ESpeak 음성을 개선했습니다.
* 노트북 키보드 레이아웃을 추가했습니다. 키보드 레이아웃은 NVDA의 키보드 설정 대화상자에서 구성할 수 있습니다. (#60)
* 주로 Windows Vista에서 발견되는 SysListView32 컨트롤에서 항목 그룹화를 지원합니다. (#27)
* SysTreeview32 컨트롤에서 트리뷰 항목의 체크 상태를 보고합니다.
* NVDA의 여러 설정 대화상자에 단축키를 추가했습니다.
* IAccessible2를 지원하는 응용 프로그램(예: Mozilla Firefox)을 NVDA를 휴대용 미디어에서 실행할 때, 특별한 DLL 파일을 등록하지 않고도 사용할 수 있습니다.
* Gecko 응용 프로그램에서 가상 버퍼 링크 목록과 관련된 충돌을 수정했습니다. (#48)
* NVDA가 Mozilla Gecko 응용 프로그램(예: Firefox 및 Thunderbird)보다 높은 권한으로 실행 중일 때 발생하는 충돌 문제를 해결했습니다. 예: NVDA가 관리자 권한으로 실행 중인 경우.
* 음성 사전(이전의 사용자 사전)은 이제 대소문자를 구분하거나 구분하지 않도록 설정할 수 있으며, 패턴을 정규 표현식으로 설정할 수도 있습니다. (#39)
* NVDA가 가상 버퍼 문서에 대해 '화면 레이아웃' 모드를 사용할지 여부를 설정 대화상자에서 구성할 수 있습니다.
* Gecko 문서에서 href가 없는 앵커 태그를 더 이상 링크로 보고하지 않습니다. (#47)
* NVDA 찾기 명령은 이제 모든 응용 프로그램에서 마지막으로 검색한 내용을 기억합니다. (#53)
* 가상 버퍼에서 일부 체크박스와 라디오 버튼의 체크 상태가 발표되지 않던 문제를 수정했습니다.
* 가상 버퍼 패스스루 모드는 이제 NVDA 전체가 아닌 각 문서에 대해 개별적으로 적용됩니다. (#33)
* 시스템이 대기 모드에서 복귀했거나 느린 경우 NVDA를 사용할 때 포커스 변경과 관련된 지연 및 잘못된 음성 중단 문제를 해결했습니다.
* Mozilla Firefox에서 콤보 박스 지원을 개선했습니다. 특히 화살표 키로 탐색할 때 텍스트가 반복되지 않으며, 콤보 박스를 벗어날 때 상위 컨트롤이 불필요하게 발표되지 않습니다. 또한 가상 버퍼 명령이 가상 버퍼 내에서 포커스된 경우에도 작동합니다.
* 많은 응용 프로그램에서 상태 표시줄을 찾는 정확도를 개선했습니다. (#8)
* NVDA의 내부를 실행 중에 살펴보고 조작할 수 있는 NVDA 대화형 Python 콘솔 도구를 추가했습니다.
* sayAll, reportSelection 및 reportCurrentLine 스크립트가 이제 가상 버퍼 패스스루 모드에서도 제대로 작동합니다. (#52)
* 속도 증가 및 감소 스크립트를 제거했습니다. 사용자는 synth 설정 링 스크립트(control+nvda+화살표) 또는 음성 설정 대화상자를 사용해야 합니다.
* 진행률 표시줄 비프음의 범위와 스케일을 개선했습니다.
* 새로운 가상 버퍼에 더 많은 빠른 키를 추가했습니다: l은 목록, i는 목록 항목, e는 편집 필드, b는 버튼, x는 체크박스, r은 라디오 버튼, g는 그래픽, q는 블록 인용, c는 콤보 박스, 1에서 6은 각각의 제목 수준, s는 구분선, m은 프레임. (#67, #102, #108)
* Mozilla Firefox에서 새 문서 로드를 취소하면 이전 문서의 가상 버퍼를 계속 사용할 수 있습니다. 단, 이전 문서가 아직 실제로 삭제되지 않은 경우에만 가능합니다. (#63)
* 가상 버퍼에서 단어 단위로 탐색할 때 단어가 여러 필드의 텍스트를 포함하지 않도록 정확도를 개선했습니다. (#70)
* Mozilla Gecko 가상 버퍼에서 탐색할 때 포커스 추적 및 포커스 업데이트의 정확도를 개선했습니다.
* 새로운 가상 버퍼에서 이전 찾기 스크립트(shift+NVDA+f3)를 추가했습니다.
* Mozilla Gecko 대화상자(Firefox 및 Thunderbird)에서 지연 현상을 개선했습니다. (#66)
* NVDA의 현재 로그 파일을 볼 수 있는 기능을 추가했습니다. NVDA 메뉴 -> 도구에서 찾을 수 있습니다.
* 시간 및 날짜 발표와 같은 스크립트가 현재 언어를 고려하도록 했습니다. 구두점 및 단어 순서가 언어를 반영합니다.
* NVDA의 일반 설정 대화상자에서 언어 콤보 박스가 사용 편의를 위해 전체 언어 이름을 표시합니다.
* 현재 내비게이터 객체에서 텍스트를 검토할 때 텍스트가 동적으로 변경되면 항상 최신 상태로 유지됩니다. 예: 작업 관리자에서 목록 항목의 텍스트를 검토할 때. (#15)
* 마우스로 이동할 때 마우스 아래 텍스트의 현재 단락이 발표됩니다. 특정 객체의 모든 텍스트나 현재 단어만 발표되는 대신입니다. 또한 오디오 좌표 및 객체 역할 발표는 선택 사항이며 기본적으로 꺼져 있습니다.
* Microsoft Word에서 마우스로 텍스트를 읽는 기능을 지원합니다.
* Wordpad와 같은 응용 프로그램에서 메뉴 표시줄을 벗어나면 텍스트 선택이 더 이상 발표되지 않던 버그를 수정했습니다.
* Winamp에서 트랙을 전환하거나 재생/일시 정지/중지할 때 트랙 제목이 반복적으로 발표되지 않습니다.
* Winamp에서 셔플 및 반복 컨트롤의 상태를 전환할 때 발표하는 기능을 추가했습니다. 메인 창과 재생 목록 편집기에서 작동합니다.
* Mozilla Gecko 가상 버퍼에서 특정 필드를 활성화하는 기능을 개선했습니다. 클릭 가능한 그래픽, 단락을 포함하는 링크 및 기타 특이한 구조를 포함할 수 있습니다.
* 일부 시스템에서 NVDA 대화상자를 열 때 초기 지연 현상을 수정했습니다. (#65)
* Total Commander 응용 프로그램에 대한 특정 지원을 추가했습니다.
* sapi4serotek 드라이버에서 피치가 특정 값에 고정될 수 있는 버그를 수정했습니다. 예: 대문자를 읽은 후 피치가 높은 상태로 유지됨. (#89)
* Mozilla Gecko 가상 버퍼에서 클릭 가능한 텍스트 및 기타 필드를 클릭 가능하다고 발표합니다. 예: onclick HTML 속성이 있는 필드. (#91)
* Mozilla Gecko 가상 버퍼에서 탐색할 때 현재 필드를 뷰로 스크롤합니다. 이는 시각적으로 동료가 사용자가 문서에서 어디에 있는지 알 수 있도록 유용합니다. (#57)
* IAccessible2를 지원하는 응용 프로그램에서 ARIA 라이브 영역 표시 이벤트에 대한 기본 지원을 추가했습니다. Chatzilla IRC 응용 프로그램에서 유용하며, 새 메시지가 자동으로 읽힙니다.
* ARIA 지원 웹 응용 프로그램 사용을 돕기 위한 약간의 개선 사항을 추가했습니다. 예: Google Docs.
* 가상 버퍼에서 텍스트를 복사할 때 추가 빈 줄을 추가하지 않습니다.
* 링크 목록에서 스페이스 키가 링크를 활성화하지 않도록 했습니다. 이제 다른 문자처럼 특정 링크 이름을 입력하는 데 사용할 수 있습니다.
* moveMouseToNavigator 스크립트(NVDA+numpadSlash)는 이제 내비게이터 객체의 왼쪽 상단이 아닌 중앙으로 마우스를 이동합니다.
* 왼쪽 및 오른쪽 마우스 버튼을 클릭하는 스크립트를 추가했습니다(numpadSlash 및 numpadStar 각각).
* Windows 시스템 트레이에 대한 접근성을 개선했습니다. 포커스가 특정 항목으로 계속 점프하는 것처럼 보이지 않아야 합니다. 참고: 시스템 트레이로 이동하려면 Windows 명령 WindowsKey+b를 사용하세요. (#10)
* 편집 필드에서 커서 키를 누르고 끝에 도달했을 때 성능을 개선하고 추가 텍스트 발표를 중지했습니다.
* 특정 메시지가 발표되는 동안 사용자가 기다려야 하는 문제를 방지했습니다. 특정 음성 합성기에서 발생하는 충돌/중단 문제를 해결했습니다. (#117)
* Audiologic Tts3 음성 합성기를 지원합니다. 기여: Gianluca Casalino. (#105)
* Microsoft Word 문서에서 탐색할 때 성능을 개선할 가능성이 있습니다.
* Mozilla Gecko 응용 프로그램에서 경고 텍스트를 읽을 때 정확도를 개선했습니다.
* Windows의 비영어 버전에서 구성 저장 시 발생할 수 있는 충돌을 방지했습니다. (#114)
* NVDA 환영 대화상자를 추가했습니다. 이 대화상자는 새로운 사용자에게 필수 정보를 제공하며 CapsLock을 NVDA 수정 키로 구성할 수 있습니다. 이 대화상자는 기본적으로 NVDA가 시작될 때 표시되며 비활성화될 때까지 계속 표시됩니다.
* Adobe Reader에 대한 기본 지원을 수정하여 버전 8 및 9에서 문서를 읽을 수 있도록 했습니다.
* NVDA가 제대로 초기화되기 전에 키를 누르고 있을 때 발생할 수 있는 일부 오류를 수정했습니다.
* 사용자가 NVDA를 종료 시 구성 저장으로 설정한 경우, Windows 종료 또는 로그아웃 시 구성이 제대로 저장되도록 했습니다.
* 설치 프로그램 시작 부분에 NVDA 로고 사운드를 추가했습니다. 기여: Victer Tsaran.
* 설치 프로그램에서 실행 중이든 그렇지 않든 NVDA는 종료 시 시스템 트레이 아이콘을 제대로 정리해야 합니다.
* NVDA 대화상자의 표준 컨트롤(예: 확인 및 취소 버튼)에 대한 레이블이 영어로만 유지되지 않고 NVDA가 설정된 언어로 표시됩니다.
* NVDA 아이콘이 시작 메뉴 및 데스크탑의 NVDA 바로 가기에 대해 기본 응용 프로그램 아이콘 대신 사용됩니다.
* MS Excel에서 탭 및 shift+탭으로 이동할 때 셀을 읽습니다. (#146)
* Skype의 특정 목록에서 이중 발표를 수정했습니다.
* IAccessible2 및 Java 응용 프로그램에서 캐럿 추적을 개선했습니다. 예: Open Office 및 Lotus Symphony에서 NVDA는 문서의 끝에서 잘못된 단어나 줄을 읽는 대신 캐럿이 이동할 때까지 제대로 기다립니다. (#119)
* Akelpad 4.0에서 발견된 AkelEdit 컨트롤을 지원합니다.
* Lotus Symphony에서 문서에서 메뉴 표시줄로 이동할 때 NVDA가 더 이상 멈추지 않습니다.
* Windows XP 프로그램 추가/제거 애플릿에서 제거 프로그램을 실행할 때 NVDA가 더 이상 멈추지 않습니다. (#30)
* Spybot Search and Destroy를 열 때 NVDA가 더 이상 멈추지 않습니다.

## 0.6p1

### 새로운 진행 중인 가상 버퍼를 통해 웹 콘텐츠에 액세스할 수 있습니다(Firefox3 및 Thunderbird3를 포함한 Mozilla Gecko 응용프로그램)

* 로드 시간이 거의 30배 개선되었습니다 (대부분의 웹 페이지가 버퍼에 로드될 때 기다릴 필요가 없습니다).
* 링크 목록이 추가되었습니다 (NVDA+f7).
* 찾기 대화상자 (control+nvda+f)가 대소문자를 구분하지 않는 검색을 수행하도록 개선되었으며, 해당 대화상자의 포커스 문제를 몇 가지 수정했습니다.
* 새로운 가상 버퍼에서 텍스트를 선택하고 복사할 수 있습니다.
* 기본적으로 새로운 가상 버퍼는 문서를 화면 레이아웃으로 나타냅니다 (링크와 컨트롤이 시각적으로 별도의 줄에 있지 않으면 별도의 줄로 표시되지 않습니다). 이 기능은 NVDA+v로 전환할 수 있습니다.
* control+upArrow와 control+downArrow로 단락 단위로 이동할 수 있습니다.
* 동적 콘텐츠에 대한 지원이 개선되었습니다.
* 위아래 화살표로 줄과 필드를 읽을 때 전반적인 정확도가 향상되었습니다.

### 국제화

* 이제 NVDA가 실행 중일 때 "죽은 문자"를 사용하는 악센트 문자를 입력할 수 있습니다.
* Alt+Shift를 눌러 키보드 레이아웃을 변경할 때 NVDA가 이를 발표합니다.
* 날짜와 시간 발표 기능이 시스템의 현재 지역 및 언어 옵션을 고려합니다.
* 체코어 번역 추가 (Tomas Valusek와 Jaromir Vit의 도움으로 작성됨)
* 베트남어 번역 추가 (Dang Hoai Phuc 작성)
* 아프리칸스어 (af_ZA) 번역 추가 (Willem van der Walt 작성)
* 러시아어 번역 추가 (Dmitry Kaslin 작성)
* 폴란드어 번역 추가 (DOROTA CZAJKA와 친구들 작성)
* 일본어 번역 추가 (Katsutoshi Tsuji 작성)
* 태국어 번역 추가 (Amorn Kiattikhunrat 작성)
* 크로아티아어 번역 추가 (Mario Percinic과 Hrvoje Katic 작성)
* 갈리시아어 번역 추가 (Juan C. buno 작성)
* 우크라이나어 번역 추가 (Aleksey Sadovoy 작성)

### 말하기

* NVDA는 이제 eSpeak 1.33과 함께 제공되며, 개선된 언어, 이름이 지정된 변형, 더 빠른 속도로 말할 수 있는 기능 등 많은 개선 사항이 포함되어 있습니다.
* 음성 설정 대화상자에서 음성 합성기가 변형을 지원하는 경우 변형을 변경할 수 있습니다. 변형은 일반적으로 현재 음성의 약간의 변화를 의미합니다. (eSpeak는 변형을 지원합니다).
* 현재 음성 합성기가 이를 지원하는 경우 음성 설정 대화상자에서 음성의 억양을 변경할 수 있는 기능이 추가되었습니다. (eSpeak는 억양을 지원합니다).
* 객체 위치 정보(예: 1/4)를 말하지 않도록 설정할 수 있는 기능이 추가되었습니다. 이 옵션은 객체 프레젠테이션 설정 대화상자에서 찾을 수 있습니다.
* NVDA는 이제 대문자를 말할 때 삐 소리를 낼 수 있습니다. 이는 음성 설정 대화상자의 체크박스를 통해 켜거나 끌 수 있습니다. 또한 NVDA가 대문자에 대해 일반적으로 수행하는 음높이 상승을 설정할 수 있는 "대문자 음높이 상승" 체크박스도 추가되었습니다. 이제 대문자에 대해 음높이 상승, "대문자"라고 말하기, 또는 삐 소리를 선택할 수 있습니다.
* NVDA에서 음성을 일시 정지할 수 있는 기능이 추가되었습니다(맥의 Voice Over에서 발견되는 것과 유사). NVDA가 무언가를 말하고 있을 때, 컨트롤 키나 쉬프트 키를 눌러 음성을 중단할 수 있으며, 다른 키를 누르지 않은 상태에서 쉬프트 키를 다시 누르면 음성이 중단된 바로 그 지점에서 계속됩니다.
* NVDA가 음성 합성기를 통해 말하는 대신 텍스트를 창에 출력하는 가상 synthDriver가 추가되었습니다. 이는 음성 합성에 익숙하지 않은 시각 개발자들에게 더 쾌적한 경험을 제공할 것입니다. 여전히 몇 가지 버그가 있을 수 있으니 피드백을 환영합니다.
* NVDA는 기본적으로 구두점을 말하지 않습니다. 구두점 읽기를 활성화하려면 NVDA+p를 누르세요.
* eSpeak는 이제 기본적으로 훨씬 느리게 말하며, NVDA를 처음 설치하거나 사용하기 시작하는 사람들에게 더 쉽게 사용할 수 있도록 했습니다.
* NVDA에 사용자 사전이 추가되었습니다. 이를 통해 NVDA가 특정 텍스트를 다르게 말하도록 설정할 수 있습니다. 사전은 기본, 음성, 임시의 세 가지가 있습니다. 기본 사전에 추가한 항목은 NVDA에서 항상 적용됩니다. 음성 사전은 현재 설정된 음성 합성기와 음성에 특정합니다. 임시 사전은 특정 작업을 수행하는 동안 빠르게 규칙을 설정하고 싶지만 영구적으로 유지하고 싶지 않을 때 유용합니다(NVDA를 닫으면 사라집니다). 현재로서는 규칙이 일반 텍스트가 아닌 정규 표현식입니다.
* 음성 합성기는 이제 음성 합성기 대화상자에서 음성 합성기를 선택하기 전에 출력 장치 콤보 상자를 설정하여 시스템의 모든 오디오 출력 장치를 사용할 수 있습니다.

### 성능

* NVDA는 이제 mshtml 편집 컨트롤에서 메시지를 편집할 때 시스템 메모리를 과도하게 사용하지 않습니다.
* 실제 커서가 없는 많은 컨트롤(예: MSN Messenger 기록 창, 트리뷰 항목, 리스트뷰 항목 등)에서 텍스트를 검토할 때 성능이 향상되었습니다.
* 리치 에디트 문서에서 성능이 개선되었습니다.
* NVDA는 이제 아무 이유 없이 시스템 메모리 크기가 점진적으로 증가하지 않습니다.
* 도스 콘솔 창에 세 번 이상 포커스를 맞추려고 할 때 발생하던 버그를 수정했습니다. NVDA가 완전히 충돌하는 경향이 있었습니다.

### 단축키

* NVDA+shift+numpad6 및 NVDA+shift+numpad4를 사용하여 각각 흐름에서 다음 객체 또는 이전 객체로 이동할 수 있습니다. 이를 통해 객체 계층 구조를 탐색할 때 상위 객체로 올라가거나 첫 번째 하위 객체로 내려가는 것을 걱정하지 않고도 이 두 키만으로 응용 프로그램을 탐색할 수 있습니다. 예를 들어, Firefox와 같은 웹 브라우저에서 이 두 키만 사용하여 문서를 객체 단위로 탐색할 수 있습니다. 흐름에서 다음 또는 이전으로 이동할 때 객체를 벗어나거나 객체 안으로 들어가면, 방향을 나타내는 순서 있는 비프음이 재생됩니다.
* 음성 설정 대화상자를 열지 않고도 음성 설정을 구성할 수 있는 Synth Settings Ring이 추가되었습니다. Synth Settings Ring은 음성 설정 그룹으로, control+NVDA+right 및 control+NVDA+left를 눌러 설정 간에 전환할 수 있습니다. 설정을 변경하려면 control+NVDA+up 및 control+NVDA+down을 사용하세요.
* 편집 필드에서 현재 선택된 내용을 보고하는 명령이 추가되었습니다 (NVDA+shift+upArrow).
* 텍스트를 읽는 여러 NVDA 명령(예: 현재 줄 보고 등)은 빠르게 두 번 누르면 텍스트를 철자 단위로 읽을 수 있습니다.
* capslock, numpad insert 및 extended insert 키를 NVDA 수정 키로 사용할 수 있습니다. 또한 이 키들 중 하나를 NVDA 수정 키로 사용할 경우, 다른 키를 누르지 않고 해당 키를 두 번 누르면 NVDA가 실행되지 않은 상태에서 키를 누른 것처럼 운영 체제로 키 입력이 전달됩니다. 이러한 키를 NVDA 수정 키로 설정하려면 키보드 설정 대화상자(이전에는 키보드 에코 대화상자라고 불림)에서 해당 키의 체크박스를 선택하세요.

### 응용프로그램 지원

* Firefox3 및 Thunderbird3 문서에 대한 지원이 개선되었습니다. 로드 시간이 거의 30배 빨라졌으며, 기본적으로 화면 레이아웃이 사용됩니다(NVDA+v를 눌러 화면 레이아웃과 비화면 레이아웃 간 전환 가능). 링크 목록(NVDA+f7)이 추가되었으며, 찾기 대화상자(Ctrl+NVDA+f)는 대소문자를 구분하지 않습니다. 동적 콘텐츠에 대한 지원이 크게 향상되었으며, 텍스트 선택 및 복사가 가능해졌습니다.
* MSN Messenger 및 Windows Live Messenger 기록 창에서 텍스트를 선택하고 복사할 수 있습니다.
* Audacity 응용 프로그램에 대한 지원이 개선되었습니다.
* Skype의 일부 편집/텍스트 컨트롤에 대한 지원이 추가되었습니다.
* Miranda 인스턴트 메신저 응용 프로그램에 대한 지원이 개선되었습니다.
* Outlook Express에서 HTML 및 일반 텍스트 메시지를 열 때 발생하던 포커스 문제를 수정했습니다.
* Outlook Express 뉴스그룹 메시지 필드가 이제 올바르게 레이블링됩니다.
* Outlook Express 메시지 필드(받는 사람/보낸 사람/참조 등)의 주소를 읽을 수 있습니다.
* Outlook Express 메시지 목록에서 메시지를 삭제할 때 NVDA가 다음 메시지를 더 정확하게 발표합니다.

### API 및 도구

* MSAA 개체에 대한 개체 탐색이 개선되었습니다. 이제 시스템 메뉴, 제목 표시줄 또는 스크롤 막대가 있는 창에서 이를 탐색할 수 있습니다.
* IAccessible2 접근성 API에 대한 지원이 추가되었습니다. 더 많은 컨트롤 유형을 발표할 수 있을 뿐만 아니라, Firefox 3 및 Thunderbird 3과 같은 응용 프로그램에서 커서를 액세스할 수 있어 텍스트를 탐색, 선택 또는 편집할 수 있습니다.
* Scintilla 편집 컨트롤에 대한 지원이 추가되었습니다(이러한 컨트롤은 Notepad++ 또는 Tortoise SVN에서 찾을 수 있습니다).
* Java 응용 프로그램에 대한 지원이 추가되었습니다(Java Access Bridge를 통해). 이는 Open Office(Java가 활성화된 경우) 및 기타 독립 실행형 Java 응용 프로그램에 대한 기본 지원을 제공합니다. 단, 웹 브라우저 내 Java 애플릿은 아직 작동하지 않을 수 있습니다.

### 마우스

* 마우스 포인터가 움직일 때 그 아래에 있는 내용을 읽는 기능의 지원이 향상되었습니다. 이제 훨씬 더 빠르며, 표준 편집 필드, Java 및 IAccessible2 컨트롤과 같은 일부 컨트롤에서는 현재 개체뿐 아니라 현재 단어도 읽을 수 있습니다. 이 기능은 마우스로 특정 텍스트만 읽고 싶은 시각 장애인에게 유용할 수 있습니다.
* 마우스 설정 대화 상자에 새로운 구성 옵션이 추가되었습니다. "마우스가 움직일 때 소리 재생" 옵션을 체크하면, 마우스가 움직일 때마다 40ms 길이의 삐 소리가 재생됩니다. 이 소리는 y축 위치에 따라 음높이(220~1760Hz)가 달라지며, x축 위치에 따라 좌우 음량이 달라집니다. 이를 통해 시각 장애인은 마우스가 화면에서 어느 위치에 있는지 대략적으로 파악할 수 있습니다. 이 기능은 또한 "마우스 아래 개체 보고" 기능이 켜져 있어야 작동합니다. 따라서 삐 소리와 개체 발표를 모두 빠르게 끄려면 NVDA+m을 누르면 됩니다. 삐 소리의 크기는 해당 지점의 화면 밝기에 따라 달라지기도 합니다.

### 객체 발표 및 상호작용

* 대부분의 일반적인 트리뷰 컨트롤에 대한 지원이 개선되었습니다. 이제 가지를 펼칠 때 그 안에 항목이 몇 개인지 알려줍니다. 가지를 드나들 때 레벨도 알려주며, 현재 항목 번호와 항목 수는 전체 트리뷰가 아닌 현재 가지 기준으로 알려줍니다.
* 응용 프로그램이나 운영 체제 내에서 이동할 때 포커스가 바뀌면 이제 무엇이 발표되는지도 개선되었습니다. 이제는 단지 도달한 컨트롤만 듣는 것이 아니라, 그 컨트롤이 포함된 다른 컨트롤의 정보도 들을 수 있습니다. 예를 들어 탭 키로 이동해서 그룹 상자 안에 있는 버튼에 도달하면, 그룹 상자도 함께 발표됩니다.
* NVDA는 이제 많은 대화 상자가 나타날 때 그 안의 메시지를 발표하려고 시도합니다. 대부분의 경우 정확하지만, 여전히 완벽하지 않은 대화 상자도 많습니다.
* 개체 프레젠테이션 설정 대화 상자에 "개체 설명 보고" 체크박스가 추가되었습니다. 고급 사용자는 Java 응용 프로그램과 같은 특정 컨트롤에서 너무 많은 설명을 들려주는 것을 방지하기 위해 이 옵션을 체크 해제할 수 있습니다.
* 편집 컨트롤로 포커스가 이동하면 NVDA는 자동으로 선택된 텍스트를 발표합니다. 선택된 텍스트가 없으면 일반적으로 현재 줄을 발표합니다.
* NVDA는 응용 프로그램에서 진행률 표시줄의 변경을 알리기 위해 삐 소리를 재생할 때 훨씬 더 신중해졌습니다. 이제는 Lotus Notes/Symphony와 같은 Eclipse 응용 프로그램이나 Accessibility Probe에서처럼 지나치게 삐 소리를 내지 않습니다.

### 사용자 인터페이스

* NVDA 인터페이스 창이 제거되고, 간단한 NVDA 팝업 메뉴로 대체되었습니다.
* NVDA의 사용자 인터페이스 설정 대화 상자는 이제 일반 설정이라고 불립니다. 여기에는 추가 설정 항목으로 로그 수준을 설정할 수 있는 콤보 상자가 포함되어 있습니다. 어떤 메시지를 NVDA 로그 파일에 기록할지 결정할 수 있습니다. 참고로 NVDA의 로그 파일 이름은 이제 debug.log가 아니라 nvda.log입니다.
* 개체 프레젠테이션 설정 대화 상자에서 "객체 그룹 이름 알림" 체크박스가 제거되었습니다. 그룹 이름 보고는 이제 다른 방식으로 처리됩니다.

## 0.5

* NVDA에는 이제 Jonathan Duddington이 개발한 eSpeak라는 내장 음성 엔진이 포함되어 있습니다. 매우 반응이 빠르고 가볍고, 다양한 언어를 지원합니다. SAPI 음성 엔진도 여전히 사용할 수 있지만, 기본적으로는 eSpeak가 사용됩니다.
  * eSpeak는 별도의 소프트웨어 설치가 필요하지 않기 때문에, USB 메모리나 어떤 컴퓨터에서도 NVDA와 함께 사용할 수 있습니다.
  * eSpeak에 대한 자세한 정보나 다른 버전을 찾으려면 http://espeak.sourceforge.net/ 를 방문하세요.
* Internet Explorer 및 Outlook Express의 편집 가능한 창에서 Delete 키를 눌렀을 때 잘못된 문자가 읽히던 버그를 수정했습니다.
* Skype의 더 많은 편집 필드에 대한 지원을 추가했습니다.
* 가상 버퍼는 해당 창에 포커스가 있을 때만 로드됩니다. 이는 Outlook Express에서 미리 보기 창이 켜져 있을 때 발생하는 문제를 해결합니다.
* NVDA에 다음과 같은 명령줄 인자를 추가했습니다:
  * `-m`, `--minimal`: 시작 및 종료 소리를 재생하지 않고, 설정되어 있다면 시작 시 인터페이스를 표시하지 않음
  * `-q`, `--quit`: 이미 실행 중인 NVDA 인스턴스를 종료한 후 종료
  * `-s`, `--stderr-file 파일이름`: 처리되지 않은 오류 및 예외를 기록할 파일 지정
  * `-d`, `--debug-file 파일이름`: 디버그 메시지를 기록할 파일 지정
  * `-c`, `--config-file`: 대체 구성 파일 지정
  * `-h`, `--help`: 명령줄 인자 목록이 담긴 도움말 메시지 표시
* 영어 이외의 언어를 사용할 때 입력한 문자가 해당 언어로 제대로 읽히지 않던 문제를 수정했습니다.
* Peter Vagner님의 기여로 슬로바키아어 언어 파일을 추가했습니다.
* 가상 버퍼 설정 대화상자와 문서 서식 설정 대화상자를 추가했습니다 (제공: Peter Vagner).
* Michel Such님의 기여로 프랑스어 번역을 추가했습니다.
* 진행률 표시줄의 삐 소리 토글 스크립트 (Insert+U)를 추가했습니다. (제공: Peter Vagner)
* NVDA에서 더 많은 메시지가 다른 언어로 번역 가능하도록 개선했습니다. 여기에는 키보드 입력 도움말 모드에서의 스크립트 설명도 포함됩니다.
* 가상 버퍼(Internet Explorer 및 Firefox)에 찾기 대화상자를 추가했습니다. 페이지에서 Ctrl+F를 누르면 검색 대화상자가 열리며, Enter를 누르면 해당 텍스트를 찾아 가상 커서가 그 줄로 이동합니다. F3을 누르면 다음 항목을 계속 검색합니다.
* '입력한 문자 읽기'가 켜져 있을 때 더 많은 문자를 읽을 수 있습니다. 이제 ASCII 32번부터 255번까지의 문자를 읽을 수 있습니다.
* 가독성을 위해 일부 컨트롤 유형의 명칭을 변경했습니다. 'Editable text'는 '편집', 'Outline'은 '트리 뷰', 'Push button'은 '버튼'으로 변경되었습니다.
* 목록 또는 트리 뷰에서 항목을 화살표 키로 탐색할 때, 컨트롤 유형(목록 항목, 트리 항목)을 더 이상 읽지 않아 탐색 속도가 향상되었습니다.
* 하위 메뉴가 있는 항목을 '팝업 있음' 대신 '하위 메뉴'라고 읽습니다.
* 일부 언어에서 Alt 또는 Ctrl과 같은 조합 키로 특수 문자를 입력하는 경우, '입력한 문자 읽기'가 켜져 있다면 해당 문자를 읽습니다.
* 정적 텍스트 컨트롤을 탐색할 때 발생하던 문제를 수정했습니다.
* Coscell Kao님의 기여로 번체 중국어 번역을 추가했습니다.
* NVDA 코드의 중요한 부분을 재구조화하여 설정 대화상자 등 사용자 인터페이스 관련 여러 문제를 해결했습니다.
* SAPI4 지원을 추가했습니다. 현재 두 개의 SAPI4 드라이버가 있으며, 하나는 Serotek이 기여한 코드 기반이고, 다른 하나는 ActiveVoice COM 인터페이스를 사용합니다. 두 드라이버 모두 문제점이 있으므로 사용자 환경에 맞는 것을 사용하세요.
* NVDA의 인스턴스를 두 개 이상 실행할 수 없게 했습니다. 이전에는 여러 인스턴스가 동시에 실행되면 시스템이 거의 사용할 수 없게 되는 문제가 있었습니다.
* NVDA 사용자 인터페이스의 제목을 ‘NVDA 인터페이스’에서 ‘NVDA’로 변경했습니다.
* Outlook Express에서 편집 가능한 메시지의 시작 부분에서 Backspace 키를 누르면 오류가 발생하던 문제를 수정했습니다.
* Rui Batista님의 패치로 현재 노트북 배터리 상태를 보고하는 스크립트 (Insert+Shift+B)를 추가했습니다.
* 아무 것도 읽지 않는 Silence 음성 드라이버를 추가했습니다. 이 드라이버는 향후 점자 지원 등에서 활용될 수 있습니다.
* J.J. Meddaugh님의 기여로 대문자 음높이 변화 설정을 추가했습니다.
* ‘마우스 아래 항목 읽기’ 토글 스크립트를 다른 토글 스크립트처럼 작동하도록 수정했습니다 (on/off 방식). (기여: J.J. Meddaugh)
* Juan C. Buo님의 스페인어 번역을 추가했습니다.
* Tamas Gczy님의 헝가리어 언어 파일을 추가했습니다.
* Rui Batista님의 포르투갈어 언어 파일을 추가했습니다.
* 음성 설정 대화상자에서 음성을 변경하면, 이제 선택한 음성의 기본 속도/음높이/볼륨 값이 슬라이더에 반영됩니다. Eloquence나 Viavoice처럼 속도가 다른 음성에서 발생하던 문제를 해결했습니다.
* 도스 콘솔 창에서 음성이 멈추거나 NVDA가 충돌하던 버그를 수정했습니다.
* Windows 언어 설정에 따라 NVDA의 인터페이스와 메시지가 자동으로 해당 언어로 표시되고 읽힙니다. 설정 대화상자에서 수동으로 언어를 변경할 수도 있습니다.
* 새로운 텍스트나 기타 동적 변경 사항을 자동으로 알릴지를 토글하는 스크립트 'toggleReportDynamicContentChanges' (Insert+5)를 추가했습니다. 현재는 도스 콘솔 창에서만 동작합니다.
* 시스템 캐럿 이동 시 검토 커서도 함께 이동할지를 토글하는 스크립트 'toggleCaretMovesReviewCursor' (Insert+6)를 추가했습니다. 도스 콘솔 창에서 유용합니다.
* 포커스 변경 시 내비게이터 객체도 함께 이동할지를 토글하는 스크립트 'toggleFocusMovesNavigatorObject' (Insert+7)를 추가했습니다.
* 여러 언어로 번역된 문서를 추가했습니다. 현재 프랑스어, 스페인어, 핀란드어가 제공됩니다.
* 개발자 문서를 바이너리 배포판에서 제거하고, 소스 버전에만 포함했습니다.
* Windows Live Messenger 및 MSN Messenger에서 연락처 목록을 화살표 키로 탐색하면 오류가 발생하던 문제를 수정했습니다.
* Windows Live Messenger 대화 중 새 메시지가 자동으로 읽히도록 했습니다 (현재 영어 버전에서만 동작).
* 대화창의 기록 창을 화살표 키로 탐색할 수 있게 했습니다 (현재 영어 버전에서만 동작).
* NVDA의 단축키와 충돌이 있을 경우 다음 키 입력을 Windows로 그대로 전달하는 스크립트 'passNextKeyThrough' (Insert+F2)를 추가했습니다.
* MS Word에서 매우 큰 문서를 열 때 NVDA가 1분 이상 멈추는 문제가 해결되었습니다.
* MS Word에서 표 밖으로 이동한 후 다시 같은 셀로 돌아오면 행/열 번호가 읽히지 않던 문제를 수정했습니다.
* 존재하지 않거나 작동하지 않는 음성 엔진으로 NVDA를 시작할 경우, SAPI5 엔진을 대신 로드하려 시도하며, 이마저도 실패할 경우 Silence로 설정됩니다.
* 속도 조절 스크립트는 이제 0~100 범위 밖으로 벗어나지 않습니다.
* 사용자 인터페이스 설정 대화 상자에서 언어를 선택할 때 오류가 발생하면, 메시지 상자가 이를 사용자에게 알립니다.
* 사용자 인터페이스 설정에서 언어를 변경했을 때, NVDA는 변경 사항을 저장하고 다시 시작할지를 묻습니다. 언어 변경은 재시작해야 적용됩니다.
* 음성 엔진을 선택했을 때 로드에 실패하면 메시지 상자가 표시되어 사용자에게 알려줍니다.
* 음성 엔진을 처음 로드할 때, 기본 속도/음높이/볼륨은 엔진이 적절히 설정하도록 했습니다. Eloquence나 Viavoice SAPI4 엔진이 너무 빠르게 말하는 문제를 해결했습니다.
