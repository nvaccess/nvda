# OSPP model and runtime selection report

## Decision

Use PP-OCRv6 detector and recognizer ONNX models, execute them with ONNX Runtime in a separate process, and keep
RapidOCR only as the upstream model source and behavioral reference. Ship no model binaries with NVDA or the add-on.

The default profile is PP-OCRv6 tiny (about 6.0 MiB total). PP-OCRv6 small (about 29.7 MiB) is optional for users who
prefer accuracy and Japanese support over the lowest memory footprint.

## Evaluation criteria

The OSPP task requires permissive licensing, offline operation, multilingual UI text, typical completion within
3–5 seconds, modest CPU/RAM use, and an integration that does not put native ML packages in NVDA's main process.
The NVDA issue discussion adds two especially important constraints: model downloads should be separate and managed,
and ONNX Runtime must not make NVDA startup, responsiveness, or steady-state memory materially worse.

| Candidate | License / platform | Strengths | Rejected or bounded because |
| --- | --- | --- | --- |
| PP-OCRv6 ONNX | Apache-2.0 model source and tooling | Small mobile models, Chinese/English/multilingual recognition, dynamic ONNX, CPU friendly | Needs a safe model manager and compatible DB/CTC pipeline; selected |
| RapidOCR Python runtime | Apache-2.0 | Mature ONNX reference pipeline and model catalog | Pulls a broader Python stack than the worker needs; used as reference only |
| PaddleOCR/PaddlePaddle runtime | Apache-2.0 | Full official pipeline and broad model coverage | Native runtime size and dependency surface are unsuitable for NVDA's main process |
| Tesseract | Apache-2.0 | Mature, offline, many languages | Language packs and classic segmentation are less attractive for small modern UI text; retained as a future benchmark baseline |
| Windows OCR | Windows component | Already integrated in NVDA and needs no add-on model manager | Windows-only, capability depends on installed language packs; remains the baseline engine, not the portable project output |
| Transformer OCR models | Varies | Strong on some document/handwriting tasks | Larger memory/compute cost and weaker fit for the baseline interaction budget |

## Exact selected artifacts

The committed manifests are authoritative. Each contains the ModelScope download URL, byte length, and SHA-256 from
RapidOCR release `v3.9.2`:

- `PP-OCRv6_det_tiny.onnx`: 1,829,618 bytes;
- `PP-OCRv6_rec_tiny.onnx`: 4,489,813 bytes;
- `PP-OCRv6_det_small.onnx`: 9,929,594 bytes;
- `PP-OCRv6_rec_small.onnx`: 21,234,383 bytes.

The ONNX recognizers carry their character list in model metadata, so schema version 2 does not require a separate
dictionary download. A custom schema version 1 manifest can still declare a dictionary file.

## Runtime boundary

Only the frozen worker contains NumPy and ONNX Runtime. NVDA communicates with it using newline-delimited JSON and a
temporary BGRA frame. This choice gives real process-level cancellation and ensures a native crash or leaked model
session cannot corrupt the screen reader process. A warm session avoids paying model-load cost on every command; an
idle timeout releases it.

ONNX Runtime's CPU memory arena is disabled for the included profiles and intra-op work is limited to two threads.
These are conservative defaults for a screen reader. They can be revisited only with baseline-hardware evidence.

## Measured development result

On the Apple-silicon development host, direct CPU inference on a synthetic 960×320 image containing English,
Simplified Chinese, punctuation, and digits recognized all three lines correctly. The measured model-only time was
0.082 seconds (0.049 detection and 0.025 recognition). Through the real external-worker client, the cached cold run
was 0.220 seconds end to end and four warm runs were 0.068–0.071 seconds with one stable Worker PID. This is a
compatibility check, not the required Windows baseline result; the Windows plan records NVDA latency and memory
separately.

## Remaining model work

- Add representative real Windows UI captures and low-contrast/scaled-text cases to the evaluation corpus.
- Compare tiny/small accuracy and resource use on baseline x64 hardware.
- Add specialized Arabic/Cyrillic profiles only after their model licenses, hashes, and memory costs are documented.
- Consider angle classification/polygon rectification only if measured failures justify the extra model and latency.

Primary references:

- [RapidOCR repository and license](https://github.com/RapidAI/RapidOCR)
- [RapidOCR default model catalog](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml)
- [PaddleOCR ONNX conversion documentation](https://github.com/PaddlePaddle/PaddleOCR/blob/main/deploy/paddle2onnx/readme.md)
- [NVDA ONNX Runtime issue #18662](https://github.com/nvaccess/nvda/issues/18662)
- [NVDA alternative OCR issue #18663](https://github.com/nvaccess/nvda/issues/18663)
