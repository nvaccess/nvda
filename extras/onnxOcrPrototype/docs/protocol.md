# Worker protocol and integration API

Transport is UTF-8 newline-delimited JSON over the worker's stdin/stdout. Protocol version `1` processes one request
at a time. Logs and tracebacks go to stderr so they cannot corrupt responses.

## Recognize request

```json
{
  "protocolVersion": 1,
  "type": "recognize",
  "requestId": "unique opaque string",
  "image": {
    "path": "absolute path to a temporary BGRA8 file",
    "width": 960,
    "height": 320,
    "stride": 3840
  },
  "manifestPath": "absolute path to a validated JSON manifest",
  "modelDirectory": "absolute path to the user model cache"
}
```

The frame size must equal `stride * height`; `stride` must hold at least four bytes per pixel. The alpha byte is
ignored. The client owns and deletes the frame after every terminal path.

## Success response

```json
{
  "protocolVersion": 1,
  "requestId": "same opaque string",
  "result": {
    "lines": [[{"x": 10, "y": 20, "width": 80, "height": 24, "text": "Example"}]],
    "metrics": {
      "preparationSeconds": 0.1,
      "totalSeconds": 0.2,
      "detectionSeconds": 0.1,
      "recognitionSeconds": 0.08,
      "detectedRegions": 1,
      "recognizedRegions": 1,
      "deskewedRegions": 0,
      "provider": "CPUExecutionProvider",
      "sessionCacheHit": false,
      "workerArchitecture": "AMD64",
      "workerProcessId": 1234
    }
  }
}
```

Coordinates are relative to the submitted frame. NVDA's `LinesWordsResult` converts them back to screen coordinates
for review and routing. A detected text region is currently represented as one word-like item; regions are grouped
into visual lines and sorted left-to-right.

The add-on may enlarge a capture whose width or height is below 100 pixels before sending it. The scale factor is at
most 4 and is also limited so the longest submitted side is at most 1280 pixels. Normal-size captures retain their
original pixels. The result's scale factor maps Worker coordinates back to the original screen object.

## Error response

```json
{
  "protocolVersion": 1,
  "requestId": "same opaque string or null",
  "error": {"type": "ValueError", "message": "safe diagnostic text"}
}
```

Malformed JSON, wrong versions, mismatched IDs, invalid frame metadata, unsafe manifests, failed integrity checks,
download errors, malformed result geometry, non-finite metrics, and inference errors are terminal. The client
discards the Worker after protocol or process errors.

## Lifecycle and cancellation

Successful requests reuse the process and cached inference sessions. A settings/model change creates a new client.
Cancellation clears the active request first, then terminates the process; this suppresses stale callbacks even if
native inference cannot cooperatively cancel. The next request starts a clean process. Add-on termination and idle
expiry use the same cleanup path. A request that produces no terminal response within 180 seconds is reported as an
error and the process is restarted for the next request. A packaged worker also accepts a versioned `shutdown`
request for diagnostics, although the production client uses process termination for bounded cleanup.
