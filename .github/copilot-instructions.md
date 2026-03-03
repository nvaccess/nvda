# Copilot instructions for GitHub code reviews (NVDA)

Use these instructions when reviewing pull requests in this repository.

## Review goals

* Prioritize correctness, regressions, accessibility impact, API compatibility, and security.
* Keep feedback specific and actionable; prefer concrete code suggestions over generic comments.
* Classify issues by severity:
  * **Blocking**: likely bug, regression risk, security concern, API break, missing required tests/docs.
  * **Non-blocking**: style consistency, readability, minor refactors.
* Avoid requesting unrelated refactors or broad redesigns outside PR scope.

## NVDA Python style checks

When reviewing Python changes, verify alignment with `projectDocs/dev/codingStandards.md`:

* Follow PEP 8 unless NVDA guidance differs.
* **Indentation must use tabs**, not spaces.
* New/changed code should include **PEP 484 type hints** (prefer `X | Y` and `T | None`).
* Naming conventions:
  * functions/variables: `lowerCamelCase`
  * classes: `UpperCamelCase`
  * constants: `UPPER_SNAKE_CASE`
  * scripts: `script_*`
  * events: `event_*`
* User-visible strings must be translatable via `_()` and include an appropriate translators comment.
* Public APIs should have Sphinx-style docstrings (without type declarations in docstrings).
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

For code that can expose sensitive information or run in privileged contexts:

* Check lock-screen object handling safeguards (for example, secure object filtering).
* Check secure-mode behavior (`globalVars.appArgs.secure`) and that blocked actions fail gracefully.
* Ensure changes do not leak information on secure screens.
* Check writable behavior (`NVDAState.shouldWriteToDisk`) and do not write to disk if running securely or if running from the launcher.

## Comment style for Copilot reviews

* Focus comments on changed lines and clear user/developer impact.
* Explain **why** something is a problem and **what** acceptable fix looks like.
* If uncertain, ask a precise question instead of making a weak assertion.
* Acknowledge valid trade-offs; do not insist on preferences when standards are satisfied.
