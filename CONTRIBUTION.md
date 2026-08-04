# Contribution #14555: Dark Mode for help menu documents

**Contribution Number:** 2
**Student:** Karen Emily Muhwezi
**Issue:** <https://github.com/nvaccess/nvda/issues/14555>
**Status:** Implementation complete — ready for PR

---

## Why I Chose This Issue

I chose this issue because it offers a well-scoped, achievable way to contribute without getting stuck in the complexity of NVDA's core architecture. The original request asks for dark mode across NVDA's entire UI, which would require deep changes to the wxPython-based interface and Windows UI APIs, a significant undertaking. However, the documentation piece is self-contained: it's just HTML/CSS, and can be solved with a `prefers-color-scheme` media query and a small set of colour rules. This makes it approachable for someone at my level while still being a real, useful improvement to the project.

Beyond the technical scope, I picked this issue because it aligns with my goals as a software engineering student. I wanted hands-on experience with frontend work, specifically CSS and responsive design patterns like media queries — which I'll continue to rely on going forward. Just as importantly, I wanted to go through the full open-source contribution process end-to-end: forking, branching, writing a clear PR, and getting it reviewed and merged. Starting with a smaller, well-defined issue like this lets me learn that workflow without the added pressure of solving something architecturally complex, and it sets me up to take on more challenging issues once I'm comfortable with how the project's contribution process works.

---

## Understanding the Issue

### Problem Description

NVDA's HTML documentation (the User Guide, Developer Guide, Changes/What's New, and Key Commands Quick Reference) is styled with a single fixed light theme: a white page background with dark text and NVDA-purple accents. There is no dark variant, so users who prefer a dark colour scheme system-wide are still shown a bright white document when they open these files from the NVDA help menu or in a browser. For anyone with light sensitivity — including many low-vision users, who are a core part of NVDA's audience — a full-page white background is uncomfortable to read for any length of time.

### Expected Behavior

When the user's operating system (or browser) is set to a dark colour scheme, the documentation should render with a dark background and appropriately light text, while keeping NVDA's visual identity (the purple accent colour). No manual toggle should be needed. When the system is set to light, the documentation should look exactly as it does today.

### Current Behavior

The documentation always renders light regardless of the system colour scheme, because `user_docs/styles.css` hard-codes light colours (`color: #333` on the default white background, `#472F5F` purple headings/links, black table borders, `#f6f8fa` code backgrounds) with no `prefers-color-scheme` handling.

### Affected Components

* `user_docs/styles.css` — the shared stylesheet linked by every generated document. All documentation colours live here, as literal hex values with no media query.
* `user_docs/en/changes.md` — where a changelog entry must be added for this user-visible change.
* `user_docs/numberedHeadings.css` — the extra stylesheet for the User/Developer guides; reviewed and confirmed it only sets layout/counters and defines no colours, so it needs no dark-mode changes.
* `source/md2html.py` — the converter that turns the Markdown docs into HTML. Its `HTML_HEADERS` template (around lines 68-80) links `styles.css`, and the logic further down also attaches `numberedHeadings.css` for the user/developer guides. Reviewed to confirm how the stylesheet is wired in; no change needed here.
* `sconstruct` (around lines 324 and 567-573) — build wiring that copies the CSS files alongside the generated HTML. Reviewed; no change needed.

---

## Reproduction Process

### Environment Setup

Setting up the NVDA build environment on Windows was the hardest part of this contribution. Notes on what I hit and how I worked around it:

* **uv wasn't installed.** NVDA uses uv (see <https://docs.astral.sh/uv/>) as its package/project manager. I installed it with the official script (`irm https://astral.sh/uv/install.ps1 | iex`). It lands in `C:\Users\<me>\.local\bin`, which isn't on `PATH` by default, so I prepend that to `$env:Path` each session.
* **Pinned Python vs. `only-system` preference.** `.python-version` pins exactly 3.13.13, but `pyproject.toml` sets `python-preference = "only-system"` and my machine only had 3.13.3 — so uv refused to fetch the managed build. Fix, without editing the tracked `pyproject.toml`: override for the session with `$env:UV_PYTHON_PREFERENCE = "managed"`. uv then downloaded 3.13.13, created `.venv`, and installed all 115 packages.
* **Workspace submodules are mandatory.** `uv sync` fails unless the two uv workspace members — `miscDeps` and `include/nvda-mathcat` — are checked out. I ran `git submodule update --init` for those plus `espeak`, `liblouis`, and `nvda-cldr`.
* **Blocker — Visual Studio C++ toolchain.** `.\scons.bat user_docs` fails with "Could not find the Clang compiler", because SConstruct descends into the nvdaHelper C++ build even for the docs-only target. It requires Visual Studio 2022 plus "C++ Clang tools for Windows" (via `.vsconfig`), which isn't installed on my machine.
* **Workaround for CSS work.** Since this issue is pure HTML/CSS, I don't need the full build. I render pages directly with `source/md2html.py` in the ready venv, copy `styles.css`/`numberedHeadings.css` next to the output, and open the result in a browser to preview — bypassing the C++ build entirely.

### Steps to Reproduce

1. Render a doc to HTML: `.venv/Scripts/python.exe source/md2html.py -t userGuide user_docs/en/userGuide.md userGuide.html`, with `styles.css` alongside it. (The equivalent full-build command is `.\scons.bat user_docs`.)
2. Set Windows to dark mode (Settings → Personalization → Colors → "Dark"), or emulate it in DevTools (Rendering → Emulate CSS `prefers-color-scheme: dark`).
3. Open `userGuide.html` in a browser.
4. **Observed result:** the page stays on a white background with dark grey body text and dark-purple (`#472F5F`) headings/links regardless of the OS setting — the docs do not respond to dark mode.

### Reproduction Evidence

* **Screenshots:** before/after preview screenshots captured from a local render of `userGuide.html` in both system colour schemes.
* **My findings:** The styling lives entirely in `user_docs/styles.css`, and it is light-mode-only. There is no `prefers-color-scheme` media query anywhere in the repo, and no `color-scheme` declaration — so the browser never flips the default white canvas. The colours are all hard-coded (`body { color: #333 }` with no `background-color`, `#472F5F` purple headings/links, `#f6f8fa` code background, `1px solid black` table borders), so even a flipped background would be low-contrast. The HTML `<head>` that links this stylesheet is generated by `source/md2html.py`; `numberedHeadings.css` defines no colours and needs no change. The fix is therefore CSS-only: hoist the colours into custom properties and override them inside a `@media (prefers-color-scheme: dark)` block.

---

## Solution Approach

### Analysis

The root cause is that `user_docs/styles.css` was written exclusively for a light background:

* No `prefers-color-scheme` media query exists anywhere in the repo, so the docs never react to the OS theme.
* The `body` rule sets `color: #333` but no `background-color`, so the page falls back to the browser default background (white). Because there is no `color-scheme` declaration, the browser doesn't flip that default background even when the OS is in dark mode.
* Several colours would have poor contrast on a dark background even if it did flip: the `#472F5F` purple text/links, the `#f6f8fa` light-grey code background, and the `1px solid black` table borders.

All of the relevant colour rules live in `user_docs/styles.css` (originally around lines 7, 15-16, 25, 34, and 49-52).

The underlying problem is that the stylesheet only ever defines one set of colours, with no mechanism to switch them based on the user's preference. The CSS standard already provides that mechanism via the `prefers-color-scheme` media feature, which browsers resolve from the OS setting — so no JavaScript, no build changes, and no per-document work are needed. The fix belongs entirely in the shared stylesheet.

### Proposed Solution

Refactor the existing hard-coded hex values into CSS custom properties on `:root`, then add a single `@media (prefers-color-scheme: dark)` block that overrides **only those colour variables** with a dark, accessible palette. Refactoring first keeps the override clean and maintainable instead of duplicating every rule, and it means all layout, fonts, spacing, and the numbered-heading counters are shared by both themes — so the dark theme cannot drift structurally from the light one.

NVDA's purple identity is preserved by using lightened purple tints (`#cba2e8` for headings/links, `#5d3f80` for the H1 banner) that keep readable contrast on a dark background, rather than switching to a different hue.

### Implementation Plan

Using the UMPIRE framework (adapted):

**Understand:** NVDA's HTML help pages are styled by a single stylesheet (`user_docs/styles.css`) that only defines light-mode colours and never checks the OS theme. Users who run their OS in dark mode still get a bright white doc page. The goal is to respect the user's OS-level dark-mode preference via a `prefers-color-scheme: dark` media query, giving a dark background with accessible, sufficiently contrasting text, without changing the light-mode appearance at all.

**Match:** I searched the whole repo for `prefers-color-scheme`, `color-scheme`, and "dark mode" — there is no existing dark-mode or theming CSS to copy from, and no CSS-variable or theming layer either. This will be the first theme-aware CSS in the docs. `prefers-color-scheme` is the standard, framework-free pattern for the job, and the existing stylesheet already groups colours by element (`body`, `h1`, headings/links, `strong`, tables, `code`/`pre`), which maps cleanly onto a set of variables.

**Plan:**

1. In `user_docs/styles.css`, hoist the existing colours into CSS custom properties on `:root` (text, background, accent/NVDA-purple, banner, `strong`, borders, code text/background/border, `pre` accent) and reference those variables from the existing rules, preserving the current light appearance.
2. Add `color-scheme: light dark` to `:root` so the default canvas, form controls, and scrollbars also respond to the theme, and set an explicit `background-color` on `body` so the dark override has something to override.
3. Append a `@media (prefers-color-scheme: dark)` block at the end of the file that overrides the variables with a dark palette: dark background, light body text, a lightened NVDA purple for headings/links and the H1 banner, a dark code background, and lighter table borders.
4. Verify WCAG contrast for every dark-mode pair: AA for text (at least 4.5:1 for body text, 3:1 for large text) and at least 3:1 for non-text elements such as table borders (WCAG 1.4.11).
5. Confirm the `h1` banner (white text on purple) still reads well in dark mode; adjust the purple if needed.
6. Leave `numberedHeadings.css` untouched, since it defines no colours, and `md2html.py`/`sconstruct` untouched, since the media query lives entirely in the already-linked `styles.css`.
7. Add a changelog entry to `user_docs/en/changes.md`.

**Implement:** Branch `menu-dark-mode`; the change is confined to `user_docs/styles.css` and `user_docs/en/changes.md`.

**Review:** Self-review against the project's contribution guidelines:

* Followed `.github/CONTRIBUTING.md` and `projectDocs/dev/contributing.md`.
* Commented on issue #14555 to note I'm working on it (documentation issues are explicitly welcomed for first-time contributors).
* Colours only — every change is scoped to colour-bearing properties; no layout, JavaScript, or build changes.
* Light theme visually unchanged (see Manual Testing for the one deliberate addition).
* NVDA purple preserved rather than replaced; contrast verified.
* PR is well under the project's 500 LOC guideline.
* Added a changelog entry to `user_docs/en/changes.md` in the required format — `{Description of change}. (#{issue number}, @{GitHub username})`.
* Only edited the English `changes.md`; translations are handled separately.
* Branched off the latest master, and avoided the reserved `try-` branch prefix.
* Ran `runlint.bat` and the pre-commit hooks before opening the PR.
* Filled out the PR template checklist.

**Evaluate:** Render `userGuide.html` and compare it under both system colour schemes, and check every dark-mode colour pair against a contrast checker (see Testing Strategy).

---

## Testing Strategy

### Unit Tests

Not applicable. This change is purely presentational CSS in the shared documentation stylesheet; NVDA's Python unit-test suite does not cover the rendered appearance of the HTML docs, so there is nothing meaningful to assert in code.

### Integration Tests

* [x] The docs still generate without error after the CSS change — verified by running `md2html.py` on `userGuide.md`.
* [x] Both `styles.css` and `numberedHeadings.css` are still linked and applied correctly in the generated HTML.
* [x] `runlint.bat` (ruff) and the repo's pre-commit hooks pass. Note that `runlint.bat` only covers Python; the markdown files in this PR are covered by the `markdownlint-cli2` hook, and CSS has no linter configured.
* [x] The CI docs build (`.github/workflows/testAndPublish.yml`) will catch any build-breaking error in the CSS or template.

### Manual Testing

Rendered `userGuide.html` locally (via `md2html.py`) and viewed it in Chrome under both system colour schemes:

* **Light mode:** confirmed the page is visually identical to before the change — dark NVDA-purple headings, black table borders, dark text on white, light code chips. No regression. The one deliberate difference in the CSS is that `body` now declares `background-color: #fff` explicitly instead of relying on the browser default; this renders identically but is required for the dark override to work.
* **Dark mode:** confirmed the page now renders with a dark (`#1a1a1a`) background, light (`#e8e8e8`) body text, lightened-purple headings/links/table headers (`#cba2e8`), a lifted-purple H1 banner (`#5d3f80`) with white text, `#6b6b6b` table borders, and dark (`#262626`) code/`pre` blocks with light text.
* Checked headings, links, tables, and inline `code`/`pre` blocks specifically, since those are the elements that carry colour. All remained legible with comfortable contrast.

### Contrast Verification

Every dark-mode colour pair was measured against its background:

| Element | Foreground / background | Ratio | Requirement | Result |
| --- | --- | --- | --- | --- |
| Body text | `#e8e8e8` on `#1a1a1a` | 14.2:1 | 4.5:1 (AA) | Pass |
| Headings, links, `th` | `#cba2e8` on `#1a1a1a` | 8.2:1 | 4.5:1 (AA) | Pass |
| H1 banner text | `#fff` on `#5d3f80` | 8.4:1 | 4.5:1 (AA) | Pass |
| Code text | `#e8e8e8` on `#262626` | 12.3:1 | 4.5:1 (AA) | Pass |
| Table borders | `#6b6b6b` on `#1a1a1a` | 3.3:1 | 3:1 (1.4.11) | Pass |
| `pre` left accent | `#69c` on `#1a1a1a` | 5.8:1 | 3:1 (1.4.11) | Pass |

The table border colour was the one value I had to revise: my first choice, `#555`, only reached 2.3:1, which is below the 3:1 that WCAG 1.4.11 requires of non-text elements. Lightening it to `#6b6b6b` brings it to 3.3:1.

---

## Implementation Notes

### Progress

* Explored how the docs are built and styled: `source/md2html.py` wraps each Markdown doc in an HTML template that links `user_docs/styles.css` (and `numberedHeadings.css` for the guides), and `sconstruct` copies the CSS next to the generated HTML. Confirmed all colours live in `styles.css`.
* Refactored the hard-coded colours in `styles.css` into CSS custom properties on `:root`, leaving the light appearance unchanged.
* Implemented the dark theme as a single `@media (prefers-color-scheme: dark)` block that overrides only those variables.
* Chose the dark palette to preserve NVDA's purple identity by lightening it rather than replacing it, then measured every pair against WCAG thresholds and adjusted the table border colour.
* Added a `changes.md` entry and verified the docs render correctly in both themes.

### Code Changes

**Files modified:**

* `user_docs/styles.css` — hoisted colours into `:root` custom properties, added `color-scheme: light dark`, and appended the `@media (prefers-color-scheme: dark)` override block.
* `user_docs/en/changes.md` — added a "New Features" entry.

**Approach decisions:**

* **CSS-only, no JS and no build changes** — `prefers-color-scheme` lets the browser resolve the OS preference natively, which is the simplest and most robust option and touches the fewest files.
* **Custom properties plus one override block, not duplicated rules** — a second copy of every selector would drift from the light theme over time. Overriding only variables cannot change layout, so the two themes stay structurally identical and the diff stays small and reviewable.
* **Lighten the purple instead of changing hue** — keeps NVDA's brand identity recognisable in dark mode while restoring readable contrast on a dark background.

---

## Pull Request

**PR Link:** to be added once the PR is opened.

**PR Description (draft):**

> **Link to issue number:** Closes #14555
>
> **Summary of the issue:** NVDA's HTML documentation is styled with a fixed light theme and does not respond to the user's system colour scheme, so users who prefer dark mode are shown a bright white page.
>
> **Description of user facing changes:** The documentation (User Guide, Developer Guide, What's New, Key Commands) now automatically switches to a dark colour scheme when the operating system requests one, while preserving NVDA's purple accent identity. When the system is set to light, the docs look exactly as before.
>
> **Description of development approach:** Refactored the hard-coded colours in `user_docs/styles.css` into CSS custom properties on `:root`, added `color-scheme: light dark`, and appended a single `@media (prefers-color-scheme: dark)` block that overrides only those colour variables. No layout, JavaScript, or build changes. Verified by rendering the User Guide in both light and dark system settings, and checked every dark-mode colour pair against WCAG AA (and 1.4.11 for non-text elements).

**Maintainer Feedback:**

* To be recorded as review comments arrive.

**Status:** Ready to open PR

---

## Learnings & Reflections

### Technical Skills Gained

* Using the `prefers-color-scheme` media feature to build theme-aware CSS that responds to the OS setting with no JavaScript.
* Using CSS custom properties as a theming layer, and understanding why overriding variables in one place is safer than duplicating rules per theme.
* Learning what `color-scheme` actually does — that a dark `background-color` alone isn't enough, because the browser also needs to be told to adapt the canvas, scrollbars, and form controls.
* Reading an unfamiliar codebase well enough to trace how a rendered artifact is produced (Markdown → `md2html.py` → HTML linking `styles.css`) and to locate exactly where a change belongs.
* Scoping a change to be minimal and low-risk — overriding only colour properties so the existing light theme is provably unaffected.
* Calculating colour contrast ratios and applying the right WCAG threshold for each case (4.5:1 for body text, 3:1 for non-text elements), rather than just picking colours that "look dark".

### Challenges Overcome

* The biggest hurdle was the development environment: the full `scons` build fails on my machine without Visual Studio's C++ Clang tools. Instead of getting blocked, I found that this issue only needs the HTML/CSS output, so I could run `md2html.py` directly in the venv to preview docs without the full build.
* Getting uv onto my `PATH` and persuading it to use the managed Python (`UV_PYTHON_PREFERENCE=managed`) before the venv would build at all.
* Previewing dark mode reliably — I forced the theme on and off in local copies of the stylesheet so I could compare both without repeatedly toggling the Windows setting.
* Resolving a merge conflict in this write-up. I had two divergent drafts of several sections and initially committed the merge without resolving the markers, which the repo's own `check-merge-conflict` pre-commit hook would have rejected in CI. A good reminder to run the hooks locally before pushing.

### What I'd Do Differently Next Time

* Sort out the build environment (or confirm which parts I actually need) before starting, to avoid losing time to the C++ toolchain blocker.
* Verify colour choices against a contrast checker while picking them rather than at the end — I had to revise the table border colour after the fact.
* Run `pre-commit run --all-files` before committing, not just before pushing.

---

## Resources Used

* MDN — [`prefers-color-scheme`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
* MDN — [`color-scheme`](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)
* WCAG 2.1 — [Contrast (Minimum) 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) and [Non-text Contrast 1.4.11](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html)
* NVDA issue [#14555](https://github.com/nvaccess/nvda/issues/14555) (the original request)
* NVDA's own `user_docs/styles.css` and `source/md2html.py` for understanding the existing structure
