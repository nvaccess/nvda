# OSPP 25d3e0489 implementation report

## Outcome

The prototype provides offline, multilingual OCR for the current NVDA navigator object while isolating all native ML
code and model memory in a cancellable external process. Results use NVDA's existing content-recognition document,
so speech, braille, review navigation, dismissal, and coordinate routing require no parallel accessibility UI.

## Requirement traceability

| OSPP requirement | Implementation and evidence |
| --- | --- |
| Model/library research and selection | `model-selection-report.md`; two licensed/hash-pinned PP-OCRv6 profiles; no RapidOCR/Paddle runtime dependency |
| Modular design and trigger/result APIs | `protocol.md`; `OcrWorkerClient`; versioned JSON-lines boundary; `ContentRecognizer` adapter |
| Functional NVDA branch prototype | global plugin command `NVDA+Alt+O`; navigator-object capture; offline inference; `LinesWordsResult` for speech/braille |
| Performance optimization and tests | persistent sessions, two-thread CPU cap, disabled ORT arena, run-length components, dynamic recognizer width; unit/integration and Windows plans |
| Final report and user/developer docs | this report, root readme, English/Chinese add-on help, build scripts, model report, protocol, and test plan |

## Important design changes from the earlier RapidOCR PR

1. ONNX Runtime and NumPy are no longer imported into NVDA.
2. RapidOCR is not a runtime dependency; only its separately distributed PP-OCRv6 ONNX files are referenced.
3. Models are downloaded on demand to a user cache and verified by exact byte size and SHA-256.
4. Native inference runs in a process that can be terminated on cancellation or failure.
5. A warm Worker removes repeated model/session startup cost while an idle timeout bounds retained memory.
6. The earlier `NVDA+Shift+R` gesture is not reused because it conflicts with Excel row-header behavior.
7. The code does not preempt the unresolved core engine-choice UX in issue #17406; the worker API can plug into that
   registry later.

## Implementation details

The client copies NVDA's captured BGRA8 buffer to a restricted temporary file, starts or reuses the frozen Worker,
sends a request with a unique ID, validates the version and ID in the response, and deletes the frame in `finally`.
Cancellation marks the request stale before killing the process, so a late line can never take focus.

The model manager accepts HTTPS (and `file:` for developer tests), rejects unsafe filenames, limits every declared
file to 1 GiB, streams downloads, checks length/hash, and atomically replaces the cache. Existing corrupt files are
not trusted and self-heal on the next use.

The direct adapter performs PP-OCR normalization on BGR data, detector resizing in multiples of 32, thresholding,
optional dilation, run-length/union-find connected components, score filtering, rectangular unclip expansion,
dynamic-width recognizer preprocessing, softmax normalization where needed, CTC decoding, confidence filtering, and
visual line ordering. ONNX character metadata removes a redundant dictionary download for the selected models.

The Windows build pins its direct Python dependencies and filters Python 3.12's older private MSVC runtime copies
from the frozen executable. Those copies otherwise shadow the current VC++ 2015–2022 system Redistributable and make
ONNX Runtime fail during DLL initialization. The build performs an explicit system-runtime preflight.

## Verification to date

* 15 automated tests pass with `ResourceWarning` promoted to an error.
* The suite covers protocol validation, invalid frames, async callback, Worker reuse, cancellation suppression,
  restart after cancellation, path traversal, missing sizes, bad hashes, corrupt-cache repair, schema-v2 embedded
  dictionaries, connected components, and reading order.
* Direct real-model inference on a 960×320 mixed Chinese/English synthetic image returned the expected three lines.
* Model-only CPU time on the development host was 0.082 seconds. The cached cold external-worker run was 0.220
  seconds end to end; four warm runs were 0.068–0.071 seconds and reused one PID. This proves compatibility, not
  Windows acceptance.
* The earlier Windows test-double run already validated NVDA capture, result presentation, cancellation, dismissal,
  and temporary-file cleanup. The current build still requires a fresh packaged-worker and real-model Windows run.

## Challenges and decisions

External-process isolation does not reduce total system memory by itself. It prevents model memory from becoming a
persistent part of NVDA and permits reliable release after cancellation/idle. The warm/cold trade-off is explicit in
settings and metrics.

Full Paddle DB polygon reconstruction normally relies on OpenCV/Shapely-style geometry. Adding those packages would
substantially enlarge the frozen Worker. The current rectangular UI-text postprocessor is intentionally implemented
in NumPy only. Rotated/perspective text is declared out of scope until evaluation shows that an angle model and more
geometry justify their costs.

Model downloads introduce a network operation on first use. This is kept out of NVDA's UI thread, integrity checked,
and unnecessary afterward. A future core model manager could add progress, mirrors, removal, policy controls, and a
shared cache UI without changing inference.

## Next upstream steps

1. Complete and attach Windows timing/memory evidence from `windows-test-plan.md`.
2. Decide with NV Access whether the first contribution should land as an add-on, an experimental core engine, or
   the process/model-manager foundation from #18662.
3. Implement the engine registry/preferred-engine UX proposed in #17406 before assigning `NVDA+R` to an alternative
   OCR backend.
4. Split reviewable changes: protocol/process manager, model manager, adapter/tests, then UI registration.
5. Expand the corpus and only then consider polygon/angle/language-specific model profiles.
