# Windows and NVDA acceptance plan

Record NVDA version, Windows build, CPU, RAM, display scale, model profile, worker dependency versions, and commit for
every run. Retain the NVDA log and a machine-readable timing summary.

## Installation and isolation

* Build `onDeviceOcr-0.2.0.nvda-addon` with the provided PowerShell script.
* Install into a current NVDA portable or user profile and restart NVDA.
* Confirm **NVDA Settings > On-device OCR** opens without an error.
* Confirm the Simplified Chinese manifest, settings, status, and error strings load from the compiled catalog.
* Confirm `nvda.exe` has not loaded `onnxruntime.dll`, NumPy, PaddleOCR, PaddlePaddle, RapidOCR, or the model files.
* Confirm `onnxOcrWorker.exe` is a child process only after recognition begins.
* Confirm the packaged Worker PE machine is AMD64 and the archive contains no models, source catalogs, Python
  caches, partial downloads, duplicate paths, or unsafe paths.

## Functional matrix

| Case | Expected result |
| --- | --- |
| First `NVDA+Alt+O` on Chinese/English window | Says “Recognizing”; downloads two files; focuses readable result document |
| Speech and braille | Same ordered text is available to both through standard NVDA review |
| Escape | Dismisses result and returns to the prior object |
| Second warm recognition | Same Worker PID; `sessionCacheHit=true`; no model download |
| Invoke while another recognition runs | First request is cancelled; only the newest result appears |
| Change model profile | Old Worker exits; selected model downloads/loads; result uses new session |
| Idle timeout | Worker exits after configured interval; NVDA continues normally |
| Corrupt cached model | Hash/size status is invalid; next use replaces it only after verified download |
| Network unavailable with empty cache | NVDA reports recognition failure and remains responsive |
| Network unavailable with valid cache | Recognition succeeds offline |
| Screen Curtain | Uses NVDA's existing content-recognition capture policy and messages |
| Excel focused | Existing row-header gesture remains unchanged; OCR is `NVDA+Alt+O` |
| NVDA secure desktop | Command is blocked before capture, model download, or worker startup |
| Windows locked with a below-lock-screen navigator object | Object validation refuses capture |
| Small navigator object | Capture is enlarged by a bounded factor; ordinary captures remain at 1x |
| Oversized/malformed capture | Localized error is reported before allocation or Worker launch |
| NVDA compatibility | Current stable and the next declared release candidate load and complete a real gesture |

## Sample corpus

At minimum test: Notepad English, Notepad Simplified Chinese, mixed Chinese/English/digits, Windows Settings at 100%
and 150% scaling, a browser image with no accessibility text, low-contrast UI, dense two-column text, an empty image,
an 8-degree skew case, and a 90-degree/strong-perspective negative case. Record exact output and mark expected
limitations rather than silently passing.

## Performance acceptance

* First use is reported separately because it includes network download.
* Cold cached run includes worker startup and ONNX session creation.
* Warm runs: at least 10; report median and p95 end-to-end time.
* The target for a typical window/object is below 3 seconds, with 5 seconds as the outer OSPP interaction bound.
* Record peak Worker private working set and verify NVDA's private working set does not retain the model allocation.
* Cancel a deliberately overlapping run and verify Worker exit within 2 seconds.

## Evidence template

```text
Commit:
NVDA / Windows / CPU / RAM / scaling:
Model and hashes:
Cold cached end-to-end:
Warm median / p95:
Worker peak private working set:
NVDA memory before / after:
Functional cases passed / failed:
Known limitations observed:
Log and artifact paths:
```
