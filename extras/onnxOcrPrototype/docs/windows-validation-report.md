# Windows and NVDA validation report

## Environment

* Date: 2026-08-29
* Host: `DESKTOP-09H5AA7`
* Operating system: Windows 10 build 19045
* NVDA: 2026.1.1 portable
* Worker Python: 3.12
* Model profile: PP-OCRv6 tiny, CPUExecutionProvider
* Source: `feature/ospp-on-device-ocr` at this report's revision

## Outcome

The packaged add-on loaded in an isolated NVDA configuration and completed real-model recognition through the
`NVDA+Alt+O` gesture. A 1400x500 Chinese/English image produced these ordered result lines:

```text
NVDA on-device OCR
离线识别：你好，世界2026
Privacy first - fast and local
```

NVDA automatically read the result, and the same `LinesWordsResult` was rendered by NVDA's Braille Viewer. The
standard content-recognition result document remained navigable and dismissible. No ONNX Runtime or NumPy module
was loaded into `nvda.exe`.

## Defects found by the Windows run

1. PyInstaller initially copied private, older MSVC runtime DLLs beside the Worker. They shadowed the current system
   redistributable and caused ONNX Runtime DLL initialization to fail. The build now excludes those exact runtime
   names and checks for the current x64 VC++ 2015-2022 runtime before packaging.
2. The settings panel used the obsolete top-level `guiHelper` import. It now imports `guiHelper` from NVDA's `gui`
   package and loads as the twentieth settings category in NVDA 2026.1.1.
3. A frozen Worker inherited the Windows system code page. Chinese JSON was therefore not valid UTF-8 when read by
   NVDA's explicitly UTF-8 client. The Worker now reconfigures stdin, stdout, and stderr at startup; a regression
   test starts it with `PYTHONIOENCODING=cp1252` and verifies a Chinese request ID round-trips as UTF-8.

## Functional evidence

| Check | Observation | Result |
| --- | --- | --- |
| Build | Reproducible PyInstaller build and `.nvda-addon` packaging completed | Pass |
| Frozen protocol | Test-double request exited 0 with version and request ID intact | Pass |
| Real frozen inference | Three Chinese/English lines, CPUExecutionProvider | Pass |
| NVDA add-on load | `onDeviceOcr 0.2.0` added to `globalPlugins` | Pass |
| Settings | `On-device OCR`, category 20 of 20, controls created without error | Pass |
| Gesture | Windows key events invoked `kb(desktop):NVDA+alt+o` | Pass |
| Speech | NVDA log contains all three ordered result lines | Pass |
| Braille | NVDA Braille Viewer rendered the standard recognition result | Pass |
| Warm reuse | Same Worker PID, `sessionCacheHit=True` | Pass |
| Idle release | Worker exited after the configured 120 seconds | Pass |
| Main-process isolation | `nvda.exe` loaded ML module count: 0 | Pass |
| Automated regression | 16 tests passed on Windows with `ResourceWarning` as error | Pass |

## Timing and memory

The large Chinese/English NVDA run took 0.3566 seconds inside the Worker on a cold session. Its warm cached rerun took
0.2639 seconds and reused Worker PID 16740. An earlier 960x320 cached run took 0.2989 seconds cold and 0.2557 seconds
warm. These are comfortably below the three-second target and five-second OSPP outer bound.

The observed warm Worker working set was 75,476,992 bytes. At the isolation check, NVDA's working set was 185,499,648
bytes and its loaded-module list contained no `onnxruntime` or `numpy` module. The Worker was absent after idle expiry.

## Final artifact

* File: `onDeviceOcr-0.2.0.nvda-addon`
* Size: 33,079,716 bytes
* SHA-256: `cf2cc5d1515a838ace5e2e912360d36289454a3c2d0fea96c77d4bc1605c6bd7`
* Embedded Worker size: 33,342,428 bytes
* Embedded Worker SHA-256: `9594f9ed7c71ea7a587fb84db780482ba3e93bd6dc1c0a75dc091b7bda9bb599`

The test used an isolated portable NVDA configuration. Optional `ftd2xx` and remote-console accessibility warnings
in the log were unrelated to this add-on. Small default-size Notepad text was less reliable than the large image;
this is an OCR quality limitation to retain in future corpus testing, not a protocol or NVDA integration failure.
