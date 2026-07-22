# Contribution #14555: Dark Mode for help menu documents

**Contribution Number:** [2]  
**Student:** Karen Emily Muhwezi 
**Issue:** https://github.com/nvaccess/nvda/issues/14555 
**Status:** Phase I Complete

---

## Why I Chose This Issue

I chose this issue because it offers a well-scoped, achievable way to contribute without getting stuck in the complexity of NVDA's core architecture. The original request asks for dark mode across NVDA's entire UI, which would require deep changes to the wxPython-based interface and Windows UI APIs, a significant undertaking. However, the documentation piece is self-contained: it's just HTML/CSS, and can be solved with a prefers-color-scheme media query and a small set of color rules. This makes it approachable for someone at my level while still being a real, useful improvement to the project.
Beyond the technical scope, I picked this issue because it aligns with my goals as a software engineering student. I wanted hands-on experience with frontend work, specifically CSS and responsive design patterns like media queries — which I'll continue to rely on going forward. Just as importantly, I wanted to go through the full open-source contribution process end-to-end: forking, branching, writing a clear PR, and getting it reviewed and merged. Starting with a smaller, well-defined issue like this lets me learn that workflow without the added pressure of solving something architecturally complex, and it sets me up to take on more challenging issues once I'm comfortable with how the project's contribution process works.

---

## Understanding the Issue

### Problem Description

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

---

## Reproduction Process

### Environment Setup

Setting up NVDA's dev environment to build the docs had two snags worth recording:

- uv wasn't installed. NVDA uses uv (https://docs.astral.sh/uv/) as its package/project manager. Installed it with the official script (irm https://astral.sh/uv/install.ps1 | iex). It lands in C:\Users\<me>\.local\bin, which isn't on PATH by default, so I prepend that to $env:Path each session.
- Pinned Python vs. only-system preference. .python-version pins exactly 3.13.13, but pyproject.toml sets python-preference = "only-system" and my machine only had 3.13.3 — so uv refused to fetch the managed build. Fix (without editing the tracked pyproject.toml): override for the session with $env:UV_PYTHON_PREFERENCE = "managed". uv then downloaded 3.13.13, created .venv, and installed all 115 packages.
- Workspace submodules are mandatory. uv sync fails unless the two uv workspace members — miscDeps and include/nvda-mathcat — are checked out. Ran git submodule update --init for those plus espeak, liblouis, and nvda-cldr.
- Blocker — Visual Studio C++ toolchain. .\scons.bat user_docs fails with Could not find the Clang compiler, because SConstruct descends into the nvdaHelper C++ build even for the docs-only target. It requires Visual Studio 2022 + "C++ Clang tools for Windows" (via .vsconfig), which isn't installed yet. Workaround for CSS work: render pages directly with source/md2html.py in the ready venv, bypassing the C++ build.

Steps to Reproduce

1. Build (or render) the user docs to HTML — e.g. .\scons.bat user_docs, or run source/md2html.py on user_docs/en/userGuide.md to produce userGuide.html alongside user_docs/styles.css.
2. Open the generated userGuide.html in a browser, then enable OS-level dark mode (Windows: Settings → Personalization → Colors → Dark) — or emulate it in DevTools (Rendering → Emulate CSS prefers-color-scheme: dark).
3. Observed result: the page stays on a white background with dark-purple (#472F5F) headings/links regardless of the OS setting — the docs do not respond to dark mode.

Reproduction Evidence

- Commit showing reproduction: [add link to a commit/branch in your fork once pushed]
- Screenshots/logs: [attach a before screenshot of the doc in OS dark mode showing the white background]
- My findings: The styling lives entirely in user_docs/styles.css, and it's light-mode-only. There is no prefers-color-scheme media query anywhere in the repo, and no color-scheme declaration — so the browser never flips the default white canvas. Colors are hardcoded (body { color: #333 } with no background, #472F5F purple headings/links, #f6f8fa code background, 1px solid black table borders), so even a flipped background would be low-contrast. The HTML <head> that links this stylesheet is generated by source/md2html.py (HTML_HEADERS, lines 68–80); numberedHeadings.css defines no colors and needs no change. Fix is CSS-only: hoist colors into custom properties and override them inside a @media (prefers-color-scheme: dark) block.

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


### Proposed Solution

Add a @media (prefers-color-scheme: dark) block to user_docs/styles.css that overrides the existing colors with a dark, accessible palette, refactoring the current hardcoded hex values into CSS custom properties first so the override stays clean and maintainable rather than duplicating every rule.

### Implementation Plan

Using UMPIRE framework (adapted):

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

**Implement:** [Link to your branch/commits as you work]

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

---

## Testing Strategy

### Unit Tests

-No unit tests apply directly, since this is a pure CSS change with no Python logic involved

### Integration Tests
CI docs build (.github/workflows/testAndPublish.yml) will catch any build-breaking errors in the CSS or template.
runlint.bat will catch code style issues

### Manual Testing

[What you tested manually and results]

---

## Implementation Notes

### Week [X] Progress

[What you built this week, challenges faced, decisions made]

### Week [Y] Progress

[Continue documenting as you work]

### Code Changes

- **Files modified:** [List]
- **Key commits:** [Links to important commits]
- **Approach decisions:** [Why you chose certain approaches]

---

## Pull Request

**PR Link:** [GitHub PR URL when submitted]

**PR Description:** [Draft or final PR description - much of the content above can be adapted]

**Maintainer Feedback:**
- [Date]: [Summary of feedback received]
- [Date]: [How you addressed it]

**Status:** [Awaiting review / Iterating / Approved / Merged]

---

## Learnings & Reflections

### Technical Skills Gained

[What you learned technically]

### Challenges Overcome

[What was hard and how you solved it]

### What I'd Do Differently Next Time

[Reflection on your process]

---

## Resources Used

- [Link to helpful documentation]
- [Tutorial or Stack Overflow post that helped]
- [GitHub issues or discussions that helped]
