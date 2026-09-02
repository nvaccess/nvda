# On-device OCR for NVDA

This directory contains a buildable NVDA add-on and a direct ONNX Runtime worker for offline OCR. It is the
functional prototype for OSPP project `25d3e0489` and follows the constraints discussed in NVDA issues
[#18662](https://github.com/nvaccess/nvda/issues/18662),
[#18663](https://github.com/nvaccess/nvda/issues/18663), and
[#17406](https://github.com/nvaccess/nvda/issues/17406).

## User experience

* Press `NVDA+Alt+O` to recognize the current navigator object.
* NVDA presents the result through its standard content-recognition document, including speech, braille,
  cursor-key review, Escape to dismiss, and routing/clicking through OCR coordinates.
* Choose the tiny or small PP-OCRv6 model under **NVDA Settings > On-device OCR**.
* The selected detector and recognizer download on first use, are checked by exact size and SHA-256, and remain in
  `%LOCALAPPDATA%\nvda\onDeviceOcr\models`.
* After the initial download, image recognition is offline. Temporary BGRA captures are user-local and removed
  after success, failure, or cancellation.

The new command deliberately does not claim `NVDA+R`. Issue #17406 proposes a shared engine selector for that core
gesture. It also avoids `NVDA+Shift+R`, which conflicts with NVDA's Excel row-header command.

## Architecture

```text
NVDA main process
  contentRecog capture -> thin global plugin -> background JSON-lines client
                                                |
                                                v
                                 isolated onnxOcrWorker.exe
                                   verified model manager
                                   direct ONNX Runtime sessions
                                   DB detector postprocessing
                                   CTC recognition and reading order
                                                |
                                                v
                              NVDA LinesWordsResult (speech + braille)
```

The NVDA process never imports NumPy, ONNX Runtime, RapidOCR, PaddleOCR, or PaddlePaddle. The worker imports only
NumPy and ONNX Runtime. A warm worker retains model sessions for responsive repeated recognition; cancellation,
failure, model changes, add-on termination, and the idle timeout all dispose of it safely.

The worker protocol is versioned, request IDs prevent stale results, stderr stays outside the JSON response stream,
and only one request can be active. Models are not committed to Git or bundled into the add-on. The schema records
source, license, supported languages, byte size, and SHA-256 for every external file.

## Included model profiles

The manifests point to RapidOCR's separately distributed Apache-2.0 PP-OCRv6 ONNX assets. RapidOCR is the model
source and reference implementation, not a runtime dependency.

| Profile | Download | Intended use |
| --- | ---: | --- |
| PP-OCRv6 tiny | 6.0 MiB | Fast Chinese, English, Traditional Chinese, and common Latin-script UI text |
| PP-OCRv6 small | 29.7 MiB | Higher accuracy and Japanese support where memory is less constrained |

See [docs/model-selection-report.md](docs/model-selection-report.md) for the selection rationale and license/runtime
boundary.

## Build on Windows

The release artifact uses a Python 3.12 worker frozen as a separate executable. This avoids depending on NVDA's
embedded Python environment and keeps native libraries out of `nvda.exe`.

The Microsoft Visual C++ 2015–2022 x64 Redistributable must be installed. The build deliberately excludes Python's
older private MSVC DLL copies because they shadow the current system runtime and prevent ONNX Runtime from loading.

```powershell
cd extras\onnxOcrPrototype
powershell -ExecutionPolicy Bypass -File .\scripts\buildAddon.ps1
```

The script creates `dist\onDeviceOcr-0.2.0.nvda-addon`. Double-click it, accept the add-on installation prompt, and
restart NVDA. The model is intentionally not in that package; the first recognition downloads and verifies it.

For a development checkout, set `NVDA_ONNX_OCR_WORKER_PYTHON` to a Python environment containing
`requirements-worker.txt`. `NVDA_ONNX_OCR_WORKER_EXE`, `NVDA_ONNX_OCR_MANIFEST`, and
`NVDA_ONNX_OCR_MODEL_DIR` are optional development overrides. `NVDA_ONNX_OCR_TEST_DOUBLE=1` enables the deterministic
wiring test without native dependencies or model downloads.

## Tests

Cross-platform protocol, cache, cancellation, and geometry tests:

```text
python -W error::ResourceWarning -m unittest discover -s extras/onnxOcrPrototype/tests -p "test_*.py" -v
```

Windows release validation must additionally cover:

1. installation and settings-panel loading in the latest stable NVDA;
2. first-use model download, exact hashes, and no model files inside the add-on or repository;
3. Chinese/English recognition delivered to speech and braille through the result document;
4. warm repeated recognition, cancellation, dismissal, NVDA restart, and Worker cleanup;
5. timing and private-working-set measurements against the OSPP 3–5 second interaction target.

The manual matrix and evidence fields are in [docs/windows-test-plan.md](docs/windows-test-plan.md). The completed
Windows 10 / NVDA 2026.1.1 acceptance evidence is in
[docs/windows-validation-report.md](docs/windows-validation-report.md).

## Current scope

The included postprocessor is designed for horizontal desktop UI text. It uses DB thresholding, dilation,
run-length connected components, rectangular unclip expansion, CTC decoding, and line ordering. It does not yet
perform polygon contour extraction, perspective rectification, an angle classifier, handwriting recognition, or
vertical-text layout. Those are documented follow-ups rather than hidden dependencies.

The add-on command is an integration seam while #17406 remains unresolved. If NVDA core gains a content-recognizer
registry and preferred-engine setting, `OnDeviceOcrRecognizer` can be registered there without changing the worker,
model manager, or protocol.
