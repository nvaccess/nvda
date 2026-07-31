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

<<<<<<< HEAD
NVDA's HTML documentation (the User Guide, Developer Guide, Changes/What's New, and Key Commands Quick Reference) is styled with a single fixed light theme: a white page background with dark text and NVDA-purple accents. There is no dark variant, so users who prefer a dark colour scheme system-wide — including many low-vision users who find bright white pages uncomfortable — are still shown a bright white document when they open these files from the NVDA help menu or in a browser.

### Expected Behavior

When the user's operating system (or browser) is set to a dark colour scheme, the documentation should render with a dark background and appropriately light text, while keeping NVDA's visual identity (the purple accent colour). When the system is set to light, the documentation should look exactly as it does today.

### Current Behavior

The documentation always renders light regardless of the system colour scheme, because `user_docs/styles.css` hard-codes light colours (`color: #333` on the default white background, `#472F5F` purple headings/links, black table borders, `#f6f8fa` code backgrounds) with no `prefers-color-scheme` handling.

### Affected Components

* `user_docs/styles.css` — the shared stylesheet linked by every generated document.
* `source/md2html.py` — the converter that turns the Markdown docs into HTML and links `styles.css` in the `<head>`. (Reviewed to confirm how the stylesheet is wired in; no change needed here.)
* `user_docs/numberedHeadings.css` — the extra stylesheet for the User/Developer guides; reviewed and confirmed it only sets layout/counters, no colours, so it needs no dark-mode changes.
=======
NVDA's help documentation (the User Guide, "What's New"/changelog, key commands reference, etc.) is rendered as HTML, but the stylesheet that controls its appearance only defines colors for a light background. Users whose operating system is set to dark mode still see a bright white documentation page, which can be uncomfortable or even painful to read, especially for anyone with light sensitivity.

### Expected Behavior

When a user has their OS set to dark mode, NVDA's help documentation should automatically switch to a dark background with light, sufficiently high-contrast text, without needing any manual toggle. When the OS is in light mode, the docs should look exactly as they do today.

### Current Behavior

The documentation always renders with a white background, dark grey body text (#333), and NVDA-purple headings/links (#472F5F), regardless of the OS-level theme setting, because no prefers-color-scheme media query (or any dark-mode-aware CSS at all) exists in the project.

### Affected Components

user_docs/styles.css — the single stylesheet defining all documentation colors (no media query, all hardcoded hex values)
user_docs/numberedHeadings.css — heading/TOC numbering only; no colors, so no changes needed here
source/md2html.py — the Markdown→HTML build script; contains the HTML <head> template (HTML_HEADERS, lines 68–80) that links styles.css, and the logic (line 199) that also attaches numberedHeadings.css for the user/developer guides
sconstruct (lines ~324, 567–573) — build wiring that copies the CSS files alongside the generated HTML
user_docs/en/changes.md — where a changelog entry must be added for this user-visible change
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

---

## Reproduction Process

### Environment Setup

<<<<<<< HEAD
Setting up the NVDA build environment on Windows was the hardest part. Notes on what I hit and how I worked around it:

* NVDA uses **uv** to manage Python and a `.venv` with ~115 dependencies (SCons, markdown, wxPython, etc.). uv wasn't on my PATH by default and `pyproject.toml` pins `python-preference = "only-system"`, so I had to set `UV_PYTHON_PREFERENCE=managed` in the session for uv to accept the managed Python 3.13.
* The full `scons` build fails on my machine because the nvdaHelper C++ build needs Visual Studio 2022 with the "C++ Clang tools" component, which I don't have installed.
* **Workaround:** since this issue is pure HTML/CSS, I don't need the full build. I run `source/md2html.py` directly in the venv to convert a Markdown doc to HTML, copy `styles.css`/`numberedHeadings.css` next to it, and open the result in a browser to preview.
=======
Setting up NVDA's dev environment to build the docs had two snags worth recording:
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

- uv wasn't installed. NVDA uses uv (https://docs.astral.sh/uv/) as its package/project manager. Installed it with the official script (irm https://astral.sh/uv/install.ps1 | iex). It lands in C:\Users\<me>\.local\bin, which isn't on PATH by default, so I prepend that to $env:Path each session.
- Pinned Python vs. only-system preference. .python-version pins exactly 3.13.13, but pyproject.toml sets python-preference = "only-system" and my machine only had 3.13.3 — so uv refused to fetch the managed build. Fix (without editing the tracked pyproject.toml): override for the session with $env:UV_PYTHON_PREFERENCE = "managed". uv then downloaded 3.13.13, created .venv, and installed all 115 packages.
- Workspace submodules are mandatory. uv sync fails unless the two uv workspace members — miscDeps and include/nvda-mathcat — are checked out. Ran git submodule update --init for those plus espeak, liblouis, and nvda-cldr.
- Blocker — Visual Studio C++ toolchain. .\scons.bat user_docs fails with Could not find the Clang compiler, because SConstruct descends into the nvdaHelper C++ build even for the docs-only target. It requires Visual Studio 2022 + "C++ Clang tools for Windows" (via .vsconfig), which isn't installed yet. Workaround for CSS work: render pages directly with source/md2html.py in the ready venv, bypassing the C++ build.

<<<<<<< HEAD
1. Generate a doc: `.venv/Scripts/python.exe source/md2html.py -t userGuide user_docs/en/userGuide.md userGuide.html` (with `styles.css` alongside it).
2. Set Windows to dark mode (Settings → Personalization → Colors → "Dark").
3. Open `userGuide.html` in a browser.
4. **Observed result:** the page is still bright white with dark text — it ignores the dark system setting.
=======
Steps to Reproduce
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

1. Build (or render) the user docs to HTML — e.g. .\scons.bat user_docs, or run source/md2html.py on user_docs/en/userGuide.md to produce userGuide.html alongside user_docs/styles.css.
2. Open the generated userGuide.html in a browser, then enable OS-level dark mode (Windows: Settings → Personalization → Colors → Dark) — or emulate it in DevTools (Rendering → Emulate CSS prefers-color-scheme: dark).
3. Observed result: the page stays on a white background with dark-purple (#472F5F) headings/links regardless of the OS setting — the docs do not respond to dark mode.

<<<<<<< HEAD
* **Screenshots/logs:** Before/after preview screenshots captured from a local render of `userGuide.html`.
* **My findings:** The `<head>` links `styles.css`, and that file has no `@media (prefers-color-scheme: dark)` rule anywhere — confirming the docs simply never respond to the system colour scheme.
=======
Reproduction Evidence

- Commit showing reproduction: [add link to a commit/branch in your fork once pushed]
- Screenshots/logs: [attach a before screenshot of the doc in OS dark mode showing the white background]
- My findings: The styling lives entirely in user_docs/styles.css, and it's light-mode-only. There is no prefers-color-scheme media query anywhere in the repo, and no color-scheme declaration — so the browser never flips the default white canvas. Colors are hardcoded (body { color: #333 } with no background, #472F5F purple headings/links, #f6f8fa code background, 1px solid black table borders), so even a flipped background would be low-contrast. The HTML <head> that links this stylesheet is generated by source/md2html.py (HTML_HEADERS, lines 68–80); numberedHeadings.css defines no colors and needs no change. Fix is CSS-only: hoist colors into custom properties and override them inside a @media (prefers-color-scheme: dark) block.
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

---

## Solution Approach

### Analysis
The root cause is that user_docs/styles.css was written exclusively for a light background:

No prefers-color-scheme media query exists anywhere in the repo, so the docs never react to the OS theme.
The body rule sets color: #333 but no background-color, so the page falls back to the browser default background (white). Because there's no color-scheme declaration, the browser doesn't flip that default background even when the OS is in dark mode.
Several colors would have poor contrast on a dark background even if it did flip: the 
#472F5F purple text/links, the 
#f6f8fa light-grey code background, and 1px solid black table borders.

All of the relevant color rules live in user_docs/styles.css (roughly lines 7, 15–16, 25, and 34, 49–52).

<<<<<<< HEAD
The root cause is straightforward: `styles.css` only ever defines one set of colours and there is no mechanism to switch them based on the user's preference. The CSS standard already provides that mechanism via the `prefers-color-scheme` media feature, which browsers resolve from the OS setting — so no JavaScript, no build changes, and no per-document work are needed. The fix belongs entirely in the shared stylesheet.

### Proposed Solution

Add a single `@media (prefers-color-scheme: dark)` block to `user_docs/styles.css` that overrides **only the colour-bearing properties** (backgrounds, text, headings/links, table borders, code blocks). All layout, fonts, spacing, and the numbered-heading counters are left untouched so the dark theme is guaranteed to match the light theme structurally. NVDA's purple identity is preserved by using lightened purple tints (`#cba2e8` for headings/links, `#5d3f80` for the H1 banner) that keep readable contrast on a dark background rather than switching to a different hue.
=======

### Proposed Solution

Add a @media (prefers-color-scheme: dark) block to user_docs/styles.css that overrides the existing colors with a dark, accessible palette, refactoring the current hardcoded hex values into CSS custom properties first so the override stays clean and maintainable rather than duplicating every rule.
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

### Implementation Plan

Using UMPIRE framework (adapted):

<<<<<<< HEAD
**Understand:** The docs never adapt to a dark system theme because `styles.css` hard-codes light colours.

**Match:** `prefers-color-scheme` is the standard, framework-free pattern for this. The existing stylesheet already groups colours by element (body, `h1`, headings/links, `strong`, tables, code/pre), which maps cleanly onto a set of dark overrides.

**Plan:**
=======
**Understand:** NVDA's HTML help pages are styled by a single stylesheet (user_docs/styles.css) that only defines light-mode colors and never checks the OS theme. Users who run their OS in dark mode still get a bright white doc page. The goal is to respect the user's OS-level dark-mode preference via a prefers-color-scheme: dark CSS media query, giving a dark background with accessible, sufficiently contrasting text, without changing the light-mode appearance at all.

**Match:** I searched the whole repo for prefers-color-scheme, color-scheme, and "dark mode" — there is no existing dark-mode or theming CSS to copy from, and no CSS-variable/theming layer either (colors are all literal hex values). This will be the first theme-aware CSS in the docs. The chosen approach is to hoist the literal colors into CSS custom properties on :root and override them inside the media query, rather than duplicating every rule.

**Plan:** 
In user_docs/styles.css, hoist the existing colors into CSS variables on :root (text, background, accent/NVDA-purple, code background, code text, borders) and reference those variables in the existing rules — this preserves the current light appearance exactly.
Add color-scheme: light dark; to :root (or html) so form controls, scrollbars, and the default canvas background respond to the theme.
Add a @media (prefers-color-scheme: dark) { :root { … } } block overriding the variables with a dark palette: a dark background (e.g. 
#1e1e1e), light body text (e.g. 
#e0e0e0), a lightened NVDA purple for headings/links so it stays on-brand but readable (a pale lavender/lilac rather than 
#472F5F), a dark code background, and lighter table borders.
Verify WCAG AA contrast (≥4.5:1 for body text, ≥3:1 for large text) for every dark-mode color pair.
Confirm the h1 banner (white text on purple) still reads well in dark mode; adjust the purple if needed.
numberedHeadings.css needs no changes, since it defines no colors.
No change is strictly required in md2html.py, since the media query lives entirely in the already-linked styles.css.
Add a changelog entry to user_docs/en/changes.md (see Review, below).
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

1. Append a `@media (prefers-color-scheme: dark)` block at the end of `user_docs/styles.css`.
2. Override background/text on `body`; lighten the `h1` banner; recolour headings/links/`th` to a lighter purple; fix `strong`, table borders, and code/pre colours for the dark background.
3. Add a user-facing entry to `user_docs/en/changes.md`.
4. No unit tests apply (pure presentational CSS); verify by rendering in both themes.

<<<<<<< HEAD
**Implement:** Branch `menu-dark-mode`; the CSS change is in `user_docs/styles.css`.

**Review:** Colours only, scoped inside the media query; light theme byte-for-byte unchanged; NVDA purple preserved; contrast checked to AA.

**Evaluate:** Render `userGuide.html` in both light and dark system settings and compare (see Testing Strategy).
=======
**Review:** [Self-review checklist - does it follow the project's contribution guidelines?]
Followed .github/CONTRIBUTING.md and projectDocs/dev/contributing.md
 Commented on issue #14555 to note I'm working on it (documentation issues are explicitly welcomed for first-time contributors)
 PR is well under the project's 500 LOC guideline
 Added a changelog entry to user_docs/en/changes.md in the required format: {Description of change}. (#{issue number}, @{GitHub username}) — e.g. NVDA's documentation now follows the operating system's dark mode setting. (#14555, @karenemily)
 Only edited the English changes.md (translations are handled separately)
 Branched off the latest master; avoided the reserved try- branch prefix
 Ran runlint.bat before opening the PR
 Filled out the PR template checklist

**Evaluate:** 
Build the docs locally (scons user_docs or scons source user_docs) — output HTML and the copied styles.css land in the build output directory.
Open the generated userGuide.html in a browser.
Toggle OS dark mode (or emulate via devtools) and confirm the page automatically flips background/text.
Run the dark palette through a WCAG contrast checker; verify headings, links, body text, code blocks, and the h1 banner all pass AA.
Confirm light mode looks pixel-identical to before the change (diff the rendered light page).
No automated CSS test exists for the docs, so verification is manual/visual — but runlint.bat still runs on the PR, and CI builds the docs (the docs targets in .github/workflows/testAndPublish.yml), so a build break would be caught automatically.
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

---

## Testing Strategy

### Unit Tests

<<<<<<< HEAD
Not applicable. This change is purely presentational CSS in the shared documentation stylesheet; NVDA's Python unit-test suite does not cover the rendered appearance of the HTML docs, so there is nothing meaningful to assert in code.

### Integration Tests

* [x] The docs still generate without error after the CSS change — verified by running `md2html.py` on `userGuide.md`.
* [x] Both `styles.css` and `numberedHeadings.css` are still linked and applied correctly in the generated HTML.
=======
-No unit tests apply directly, since this is a pure CSS change with no Python logic involved

### Integration Tests
CI docs build (.github/workflows/testAndPublish.yml) will catch any build-breaking errors in the CSS or template.
runlint.bat will catch code style issues
>>>>>>> fdfab5a8f82251fe50e68376881aa28e6b3be392

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