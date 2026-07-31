# Contribution #14555: Dark Mode for help menu documents

**Contribution Number:** [2]
**Student:** Karen Emily Muhwezi
**Issue:** <https://github.com/nvaccess/nvda/issues/14555>
**Status:** Implementation complete — ready for PR

---

## Why I Chose This Issue

I chose this issue because it offers a well-scoped, achievable way to contribute without getting stuck in the complexity of NVDA's core architecture. The original request asks for dark mode across NVDA's entire UI, which would require deep changes to the wxPython-based interface and Windows UI APIs, a significant undertaking. However, the documentation piece is self-contained: it's just HTML/CSS, and can be solved with a prefers-color-scheme media query and a small set of color rules. This makes it approachable for someone at my level while still being a real, useful improvement to the project.
Beyond the technical scope, I picked this issue because it aligns with my goals as a software engineering student. I wanted hands-on experience with frontend work, specifically CSS and responsive design patterns like media queries — which I'll continue to rely on going forward. Just as importantly, I wanted to go through the full open-source contribution process end-to-end: forking, branching, writing a clear PR, and getting it reviewed and merged. Starting with a smaller, well-defined issue like this lets me learn that workflow without the added pressure of solving something architecturally complex, and it sets me up to take on more challenging issues once I'm comfortable with how the project's contribution process works.

---

## Understanding the Issue

### Problem Description

NVDA's HTML documentation (the User Guide, Developer Guide, Changes/What's New, and Key Commands Quick Reference) is styled with a single fixed light theme: a white page background with dark text and NVDA-purple accents. There is no dark variant, so users who prefer a dark colour scheme system-wide — including many low-vision users who find bright white pages uncomfortable — are still shown a bright white document when they open these files from the NVDA help menu or in a browser.

### Expected Behavior

When the user's operating system (or browser) is set to a dark colour scheme, the documentation should render with a dark background and appropriately light text, while keeping NVDA's visual identity (the purple accent colour). When the system is set to light, the documentation should look exactly as it does today.

### Current Behavior

The documentation always renders light regardless of the system colour scheme, because `user_docs/styles.css` hard-codes light colours (`color: #333` on the default white background, `#472F5F` purple headings/links, black table borders, `#f6f8fa` code backgrounds) with no `prefers-color-scheme` handling.

### Affected Components

* `user_docs/styles.css` — the shared stylesheet linked by every generated document.
* `source/md2html.py` — the converter that turns the Markdown docs into HTML and links `styles.css` in the `<head>`. (Reviewed to confirm how the stylesheet is wired in; no change needed here.)
* `user_docs/numberedHeadings.css` — the extra stylesheet for the User/Developer guides; reviewed and confirmed it only sets layout/counters, no colours, so it needs no dark-mode changes.

---

## Reproduction Process

### Environment Setup

Setting up the NVDA build environment on Windows was the hardest part. Notes on what I hit and how I worked around it:

* NVDA uses **uv** to manage Python and a `.venv` with ~115 dependencies (SCons, markdown, wxPython, etc.). uv wasn't on my PATH by default and `pyproject.toml` pins `python-preference = "only-system"`, so I had to set `UV_PYTHON_PREFERENCE=managed` in the session for uv to accept the managed Python 3.13.
* The full `scons` build fails on my machine because the nvdaHelper C++ build needs Visual Studio 2022 with the "C++ Clang tools" component, which I don't have installed.
* **Workaround:** since this issue is pure HTML/CSS, I don't need the full build. I run `source/md2html.py` directly in the venv to convert a Markdown doc to HTML, copy `styles.css`/`numberedHeadings.css` next to it, and open the result in a browser to preview.

### Steps to Reproduce

1. Generate a doc: `.venv/Scripts/python.exe source/md2html.py -t userGuide user_docs/en/userGuide.md userGuide.html` (with `styles.css` alongside it).
2. Set Windows to dark mode (Settings → Personalization → Colors → "Dark").
3. Open `userGuide.html` in a browser.
4. **Observed result:** the page is still bright white with dark text — it ignores the dark system setting.

### Reproduction Evidence

* **Screenshots/logs:** Before/after preview screenshots captured from a local render of `userGuide.html`.
* **My findings:** The `<head>` links `styles.css`, and that file has no `@media (prefers-color-scheme: dark)` rule anywhere — confirming the docs simply never respond to the system colour scheme.

---

## Solution Approach

### Analysis

The root cause is straightforward: `styles.css` only ever defines one set of colours and there is no mechanism to switch them based on the user's preference. The CSS standard already provides that mechanism via the `prefers-color-scheme` media feature, which browsers resolve from the OS setting — so no JavaScript, no build changes, and no per-document work are needed. The fix belongs entirely in the shared stylesheet.

### Proposed Solution

Add a single `@media (prefers-color-scheme: dark)` block to `user_docs/styles.css` that overrides **only the colour-bearing properties** (backgrounds, text, headings/links, table borders, code blocks). All layout, fonts, spacing, and the numbered-heading counters are left untouched so the dark theme is guaranteed to match the light theme structurally. NVDA's purple identity is preserved by using lightened purple tints (`#cba2e8` for headings/links, `#5d3f80` for the H1 banner) that keep readable contrast on a dark background rather than switching to a different hue.

### Implementation Plan

Using UMPIRE framework (adapted):

**Understand:** The docs never adapt to a dark system theme because `styles.css` hard-codes light colours.

**Match:** `prefers-color-scheme` is the standard, framework-free pattern for this. The existing stylesheet already groups colours by element (body, `h1`, headings/links, `strong`, tables, code/pre), which maps cleanly onto a set of dark overrides.

**Plan:**

1. Append a `@media (prefers-color-scheme: dark)` block at the end of `user_docs/styles.css`.
2. Override background/text on `body`; lighten the `h1` banner; recolour headings/links/`th` to a lighter purple; fix `strong`, table borders, and code/pre colours for the dark background.
3. Add a user-facing entry to `user_docs/en/changes.md`.
4. No unit tests apply (pure presentational CSS); verify by rendering in both themes.

**Implement:** Branch `menu-dark-mode`; the CSS change is in `user_docs/styles.css`.

**Review:** Colours only, scoped inside the media query; light theme byte-for-byte unchanged; NVDA purple preserved; contrast checked to AA.

**Evaluate:** Render `userGuide.html` in both light and dark system settings and compare (see Testing Strategy).

---

## Testing Strategy

### Unit Tests

Not applicable. This change is purely presentational CSS in the shared documentation stylesheet; NVDA's Python unit-test suite does not cover the rendered appearance of the HTML docs, so there is nothing meaningful to assert in code.

### Integration Tests

* [x] The docs still generate without error after the CSS change — verified by running `md2html.py` on `userGuide.md`.
* [x] Both `styles.css` and `numberedHeadings.css` are still linked and applied correctly in the generated HTML.

### Manual Testing

Rendered `userGuide.html` locally (via `md2html.py`) and viewed it in Chrome under both system colour schemes:

* **Light mode:** Confirmed the page is byte-for-byte visually identical to before the change — dark NVDA-purple headings, black table borders, dark text on white, light code chips. No regression.
* **Dark mode:** Confirmed the page now renders with a dark (`#1a1a1a`) background, light (`#e8e8e8`) body text, lightened-purple headings/links/table headers (`#cba2e8`), a lifted-purple H1 banner (`#5d3f80`) with white text, `#555` table borders, and dark (`#262626`) code/pre blocks with light text.
* Checked headings, links, tables, and inline `code`/`pre` blocks specifically, since those are the elements that carry colour. All remained legible with comfortable contrast (targeting WCAG AA).

---

## Implementation Notes

### Progress

* Explored how the docs are built and styled: `source/md2html.py` wraps each Markdown doc in an HTML template that links `user_docs/styles.css` (and `numberedHeadings.css` for the guides). Confirmed all colours live in `styles.css`.
* Implemented the dark theme as a single `@media (prefers-color-scheme: dark)` block appended to `styles.css`, overriding only colour properties.
* Chose the dark palette to preserve NVDA's purple identity by lightening it rather than replacing it, and checked contrast.
* Added a `changes.md` entry and verified the docs render correctly in both themes.

### Code Changes

* **Files modified:**
  * `user_docs/styles.css` — added the `@media (prefers-color-scheme: dark)` block.
  * `user_docs/en/changes.md` — added a "New Features" entry.
* **Approach decisions:**
  * **CSS-only, no JS and no build changes** — `prefers-color-scheme` lets the browser resolve the OS preference natively, which is the simplest and most robust option and touches the fewest files.
  * **Override colours only, inherit everything else** — guarantees the dark theme can't drift structurally from the light theme and keeps the diff small and reviewable.
  * **Lighten the purple instead of changing hue** — keeps NVDA's brand identity recognisable in dark mode while restoring readable contrast on a dark background.

---

## Pull Request

**PR Link:** [GitHub PR URL when submitted]

**PR Description (draft):**

> **Link to issue number:** Closes #14555
>
> **Summary of the issue:** NVDA's HTML documentation is styled with a fixed light theme and does not respond to the user's system colour scheme, so users who prefer dark mode are shown a bright white page.
>
> **Description of user facing changes:** The documentation (User Guide, Developer Guide, What's New, Key Commands) now automatically switches to a dark colour scheme when the operating system requests one, while preserving NVDA's purple accent identity. When the system is set to light, the docs look exactly as before.
>
> **Description of development approach:** Added a single `@media (prefers-color-scheme: dark)` block to `user_docs/styles.css` that overrides only colour-bearing properties (backgrounds, text, headings/links, table borders, code blocks). No layout, JavaScript, or build changes. Verified by rendering the User Guide in both light and dark system settings.

**Maintainer Feedback:**

* [Date]: [Summary of feedback received]
* [Date]: [How you addressed it]

**Status:** Ready to open PR

---

<!-- The sections below are personal reflections — draft content, adjust to your own voice. -->

## Learnings & Reflections

### Technical Skills Gained

* Using the `prefers-color-scheme` media feature to build theme-aware CSS that responds to the OS setting with no JavaScript.
* Reading an unfamiliar codebase well enough to trace how a rendered artifact is produced (Markdown → `md2html.py` → HTML linking `styles.css`) and to locate exactly where a change belongs.
* Scoping a change to be minimal and low-risk — overriding only colour properties inside a media query so the existing light theme is provably unaffected.
* Thinking about colour contrast and accessibility (WCAG AA) rather than just picking colours that "look dark".

### Challenges Overcome

* The biggest hurdle was the development environment: the full `scons` build fails on my machine without Visual Studio's C++ Clang tools. Instead of getting blocked, I found that this issue only needs the HTML/CSS output, so I could run `md2html.py` directly in the venv to preview docs without the full build.
* Getting uv to use the managed Python (`UV_PYTHON_PREFERENCE=managed`) and onto my PATH before the venv would work.
* Previewing dark mode reliably — I forced the theme on/off in local copies of the stylesheet so I could compare both without repeatedly toggling the Windows setting.

### What I'd Do Differently Next Time

* Sort out the build environment (or confirm which parts I actually need) before starting, to avoid losing time to the C++ toolchain blocker.
* Verify my colour choices against a contrast checker earlier in the process rather than at the end.

---

## Resources Used

* MDN — [`prefers-color-scheme`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
* NVDA issue [#14555](https://github.com/nvaccess/nvda/issues/14555) (the original request)
* NVDA's own `user_docs/styles.css` and `source/md2html.py` for understanding the existing structure