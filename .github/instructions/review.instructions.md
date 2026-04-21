---
description: 'Code review instructions'
applyTo: '**'
excludeAgent: coding-agent
---

# Copilot instructions for GitHub code reviews

Use these instructions when reviewing pull requests in this repository.

## Review goals

* Prioritize correctness, positive accessibility impact, API compatibility, security and avoiding regressions.
* Keep feedback specific and actionable; prefer concrete code suggestions over generic comments.
* Classify issues by severity:
  * **Blocking**: likely bug, regression risk, security concern, API break, missing required tests/docs.
  * **Non-blocking**: style consistency, readability, minor refactors.
* Avoid requesting unrelated refactors or broad redesigns outside PR scope.

## PR checklist expectations

Ensure the PR content supports NVDA’s review checklist:

* Documentation impact considered:
  * changelog entry when required
  * user/developer docs updates where needed
  * context-sensitive help for GUI options
* Testing strategy is clear and reproducible:
  * unit/system/manual coverage discussed
  * manual steps are concrete
* UX impact considered for:
  * speech, braille, low vision
  * browser differences where applicable
  * localization implications
* API compatibility with add-ons is preserved, unless breaking API compatibility is explicitly intended and documented.

## Comment style for Copilot reviews

* Focus comments on changed lines and clear user/developer impact.
* Explain **why** something is a problem and **what** an acceptable fix looks like.
* If uncertain, ask a precise question instead of making a weak assertion.
* Acknowledge valid trade-offs; do not insist on preferences when standards are satisfied.
