# Copilot instructions for GitHub code reviews (NVDA)

Use these instructions when reviewing pull requests in this repository.

## Review goals

* Prioritize correctness, avoiding regressions, positive accessibility impact, API compatibility, and security.
* Keep feedback specific and actionable; prefer concrete code suggestions over generic comments.
* Classify issues by severity:
  * **Blocking**: likely bug, regression risk, security concern, API break, missing required tests/docs.
  * **Non-blocking**: style consistency, readability, minor refactors.
* Avoid requesting unrelated refactors or broad redesigns outside PR scope.

## NVDA Python style checks

When reviewing Python changes, verify alignment with `projectDocs/dev/codingStandards.md`:

* Follow PEP 8 unless NVDA guidance differs.
* **Indentation must use tabs**, not spaces.
* New/changed code must include **PEP 484 type hints** (prefer `X | Y` and `T | None`).
* Naming conventions:
  * functions/variables: `lowerCamelCase`
  * classes: `UpperCamelCase`
  * constants: `UPPER_SNAKE_CASE`
  * scripts: `script_*`
  * events: `event_*`
* User-visible strings must be translatable via gettext (`_()`, `pgettext()`, `ngettext()` or `npgettext()`) and include an appropriate translators comment.
* All public functions, classes, and methods must have Sphinx-style docstrings (without type declarations in docstrings).
Most internal functions, classes, and methods should also have docstrings, except where their purpose is clear from their name or code.
* Flag unnecessary import-time side effects and new module-level globals where avoidable.
* Prefer inclusive language and avoid terms disallowed by NVDA guidelines.

## PR checklist expectations

Ensure the PR content supports NVDA’s review checklist (`.github/PULL_REQUEST_TEMPLATE.md`):

* Documentation impact considered:
  * changelog entry when required (`user_docs/en/changes.md`)
  * user/developer docs updates where needed
  * context-sensitive help for GUI options
* Testing strategy is clear and reproducible:
  * unit/system/manual coverage discussed
  * manual steps are concrete
* UX impact considered for:
  * speech, braille, low vision
  * browser differences where applicable
  * localization implications
* API compatibility with add-ons is preserved unless explicitly intended and documented.

## Security-specific review checks

NVDA operates with `UIAccess` privileges, injects code into other processes and handles untrusted data.
Scrutinize code for privilege escalation and data leaks.

* Secure mode, lock screens & installer limitations:
  * Check lock-screen object handling safeguards (e.g., secure object filtering).
  * Ensure `globalVars.appArgs.secure` is respected and blocked actions fail gracefully.
  * Check `NVDAState.shouldWriteToDisk`; do not write to disk/config if running securely or from the launcher.
  * Ensure no system or personal information is unintentionally exposed in secure screens or the lock screen.
* Subprocesses & file execution:
  * Flag any use of `subprocess`, `os.system`, or `os.startfile`.
  Because NVDA has UIAccess, these must use strictly sanitied arguments and absolute paths to prevent path/binary hijacking.
* Sensitive Data Logging:
  * Ensure new logging statements that are INFO level or higher do not capture sensitive user data, particularly from `protected` or password text fields, API keys, or secure desktop states.
  DEBUG level logging may include sensitive information such as a speech passed to a synthesizer.
* Untrusted input & web parsing:
  * Validate that parsing of external structures (HTML, ARIA attributes, UIA/IA2 properties) handles malformed, excessively long or deeply nested inputs safely without causing infinite loops or memory crashes.
  * Check for XSS e.g. from translators via translatable strings
* IPC and injected C++ code (`NVDAHelper`):
  * Ensure data sent via RPC or IPC from injected processes to the main NVDA process is strictly validated for length and type.
  * In C++ code, flag unsafe string handling, missing bounds checks or improper buffer allocations.
* Network / Updates:
  * Any new HTTP/network requests must enforce secure connections (HTTPS) and validate server certificates except when updating certificates.

## Architecture / performance checks

* Verify thread safety.
GUI changes, core state mutations and most COM/UI interactions must happen on the main thread.
Ensure `wx.CallLater`, `wx.CallAfter`, `utils.schedule`, `core.callLater` or `queueHandler` are used when passing execution from background threads.
* Flag expensive operations (such as heavy computations, blocking I/O, complex loops) inside performance-critical hot paths like focus changes, key presses, or text iteration. 
Watch for excessive COM calls (e.g. fetching properties individually inside a large loop instead of caching) and deep UIA tree walks on the main thread.
* For `ctypes` and COM interactions, ensure memory buffers, handles, and variants are safely freed to prevent memory leaks (e.g. using `ole32.CoTaskMemFree` or `kernel32.CloseHandle`).
* If an API change breaks compatibility, ensure it follows NVDA’s deprecation cycle (using `utils._deprecate`) and is noted in the API changelog as per `projectDocs/dev/deprecations.md`.
* For C++ changes, prioritise RAII, smart pointers for COM objects and lightweight execution inside injected hooks to prevent crashing target apps.
## Comment style for Copilot reviews

* Focus comments on changed lines and clear user/developer impact.
* Explain **why** something is a problem and **what** an acceptable fix looks like.
* If uncertain, ask a precise question instead of making a weak assertion.
* Acknowledge valid trade-offs; do not insist on preferences when standards are satisfied.
