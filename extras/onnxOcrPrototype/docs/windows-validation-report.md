# Windows and NVDA validation report

## Environment and scope

* Date: 2026-08-29
* Host: Windows 10 Home Chinese, build 19045, 64-bit
* NVDA: 2026.1.1 stable and 2026.2rc2, isolated portable configurations
* Worker: frozen Python 3.12 AMD64 executable, CPUExecutionProvider
* Profiles: PP-OCRv6 tiny and small
* Source: uncommitted local development on `feature/ospp-on-device-ocr`

This is local development/acceptance evidence, not a release claim. The declared manifest range is minimum NVDA
2026.1 and last-tested NVDA 2026.2. The candidate was not committed, pushed, submitted, or installed over the user's
normal NVDA configuration.

## Outcome

The final candidate passed its complete Windows validation helper. The packaged add-on loaded in both tested NVDA
versions and completed a real `NVDA+Alt+O` gesture. The worker returned these ordered lines exactly:

```text
NVDA on-device OCR
离线识别：你好，世界2026
Privacy first · fast and local
```

NVDA announced the result through its standard content-recognition result flow. Inspection of `nvda.exe` found no
NumPy or ONNX Runtime module. A repeated gesture while a delayed request was active cancelled/replaced the first
request and produced exactly one completion. All isolated NVDA and Worker processes were absent after cleanup.

## Final artifact audit

| Field | Value |
| --- | --- |
| Candidate | `onDeviceOcr-0.2.0-fully-adapted-localtest.nvda-addon` |
| Size | 33,087,794 bytes |
| SHA-256 | `bafa1f94b42c40fdc1e5a023ecea8a2648435ab674c9e2b9ca3a2e5f6c355193` |
| Archive | 17 entries; required paths present; no duplicates or unsafe paths |
| Exclusions | no ONNX model, `.po`, `.pyc`, `.pyo`, `__pycache__`, or `.part` entry |
| Source match | every packaged source/config/help/catalog entry matched the audited Windows source |
| Localization | compiled `zh_CN` catalog loaded successfully |
| Embedded Worker | 33,345,445 bytes; SHA-256 `48a7c548a4427e60ead409c1b6d70792942bc35bc151346ae57afa4697fcb768` |
| PE machine | `0x8664` (AMD64) |
| Manifest | minimum 2026.1; last tested 2026.2 |

The source archive transferred for this run had SHA-256
`36ede5962fb7649ff26576b553ce137fedf69676bd75533ec97d10c2ac8e86d0`.

## Functional and compatibility evidence

| Check | Observation | Result |
| --- | --- | --- |
| Automated regression | 42 tests passed in 2.950 seconds with `ResourceWarning` as error | Pass |
| Build | frozen Worker PE validation and add-on packaging completed | Pass |
| Stable NVDA | 2026.1.1 AMD64; 175 modules; real gesture returned three lines/regions | Pass |
| Next NVDA line | 2026.2rc2 AMD64; 183 modules; real gesture returned three lines/regions | Pass |
| Main-process isolation | forbidden NumPy/ONNX Runtime modules: none in both NVDA runs | Pass |
| NVDA errors | add-on-specific errors: none in all four NVDA scenarios | Pass |
| Cancellation/replacement | two gestures 0.2 seconds apart against a two-second request; one completion | Pass |
| Small capture | approximately 287×39 focused capture submitted as 1148×156; bounded below 1280 | Pass |
| Normal capture | remains at 1x; deskew fallback remains inactive on normal horizontal text | Pass |
| Localization | zh_CN manifest/catalog and translated settings/status/error strings packaged | Pass |
| Cleanup | NVDA and Worker process lists empty before and after the isolated suite | Pass |

Two processes with the Worker executable path are visible during each PyInstaller one-file run: its bootloader parent
and extracted child. This is expected one-file behavior; neither remained after the test. PowerShell also labels
native stderr from verbose `unittest` and PyInstaller progress as `NativeCommandError` / `RemoteException`; the same
build log ends with the test `OK`, both artifact creation messages, and `FULL_ADAPT_BUILD_PASSED`.

## Real-model timing

| Profile/case | End-to-end | Worker inference | Session cache | Result |
| --- | ---: | ---: | --- | --- |
| Tiny, 8-degree sample, cold | 1.3121 s | 0.2120 s | no | exact; one deskewed region |
| Tiny, mixed sample, warm | 0.0986 s | 0.0977 s | yes | exact three lines |
| Small, mixed sample, cold | 4.8466 s | 0.3790 s | no | exact three lines |
| Small, mixed sample, warm | 0.3307 s | 0.3298 s | yes | exact three lines |

The small profile's cold start is within the OSPP five-second outer interaction bound but close to its edge. Tiny is
the appropriate default for a lightweight experience; small remains an explicit higher-accuracy choice.

## Defects found and closed during Windows testing

1. Private older MSVC DLLs shadowed the current system redistributable; exact runtime names are excluded and the x64
   VC++ 2015–2022 runtime is checked before packaging.
2. The settings panel used an obsolete top-level `guiHelper` import; it now uses NVDA's supported `gui` package.
3. Frozen Worker streams inherited the Windows code page; stdin/stdout/stderr are now explicitly UTF-8.
4. The archiver admitted stale Python caches; it now walks a sorted filtered list and validates the package.
5. The add-on claimed an untested future NVDA version; `lastTestedNVDAVersion` now truthfully declares 2026.2 after
   validation on 2026.2rc2.
6. Very small navigator objects lost text detail; only small captures now receive bounded nearest-neighbour scaling.
7. Corrupt settings/profile values and unexpected capture/plugin exceptions could escape the command boundary;
   fallback, localized reporting, and lifecycle cleanup now cover those paths.

## Honest residual boundaries

* The 17-case small-text corpus is 15/17 exact; 8 px and 10 px samples remain below reliable OCR quality. The new
  scaling fixes small capture surfaces, but it cannot recreate source glyph detail that is absent.
* Vertical text, handwriting, strong perspective, 90-degree/arbitrary rotation, and complex multi-column layout are
  outside this lightweight horizontal desktop-UI postprocessor.
* Windows 11 ARM64 and native ARM64 packaging were not tested. The supplied Worker is deliberately verified AMD64.
* NVDA 2026.2 final was not available for this run; 2026.2rc2 was tested. The manifest does not claim 2026.3.
* The command stays on `NVDA+Alt+O`; taking over core `NVDA+R` awaits the engine-selection design in issue #17406.

Within the declared Windows x64, NVDA 2026.1–2026.2, horizontal desktop-text scope, no known integration, isolation,
localization, cancellation, packaging, or process-cleanup defect remained after this run.
