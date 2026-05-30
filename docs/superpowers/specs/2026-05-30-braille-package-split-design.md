# Design: Split `braille.py` into a `braille/` package

- **Date:** 2026-05-30
- **Issue:** [#12772 — Consider splitting braille.py into smaller files](https://github.com/nvaccess/nvda/issues/12772)
- **Status:** Approved (ready for implementation planning)

## Problem

`source/braille.py` is ~4256 lines (>100 KB). Its size makes the module hard to
navigate, hard to reason about, and hard to review. Issue #12772 asks to split it
into smaller modules, *"something similar to what we did with controlTypes"*, while
not breaking add-ons. This refactor is also a stepping stone for #12971 (making all
docstrings Sphinx-parseable): smaller, focused modules are easier to document.

## Goals

- Split `braille.py` into a `braille/` package with focused submodules.
- Preserve the public API exactly: every symbol currently reachable as `braille.X`
  stays reachable as `braille.X`, with identical behaviour. No add-on or in-tree
  consumer needs to change.
- Follow the established `controlTypes` package precedent (public submodules,
  explicit re-exports from `__init__.py`, hand-maintained `__all__`).
- Keep each submodule cohesive and independently understandable.

## Non-goals (out of scope — deferred to a follow-up)

- Relocating sibling modules into the package
  (`brailleInput` → `braille.input`, `brailleTables` → `braille.tables`,
  `louisHelper` → `braille.louisHelper`, `bdDetect` → `braille.bdDetect`) and the
  back-compat shims that would require. These stay top-level and are imported by the
  `braille` package exactly as today. A separate spec/issue will cover them.
- `brailleDisplayDrivers/` stays top-level (always was; unchanged).
- A full docstring rewrite for #12971. Existing docstrings are preserved during the
  move and kept Sphinx-parseable where trivial, but rewriting them is a separate
  effort.

## Precedent: `controlTypes`

`controlTypes.py` was previously refactored into a `controlTypes/` package. The
pattern this design follows:

- Submodules are **public** names (`role.py`, `state.py`, `formatFields.py`, …).
- `__init__.py` does **explicit** re-exports (`from .role import Role, …`) and
  defines an explicit, hand-maintained `__all__`.
- A dedicated `deprecatedAliases.py` holds back-compat aliases for *renamed*
  symbols. (Not needed here — this split renames nothing; see below.)

## Target layout

```
source/braille/
  __init__.py   # facade: explicit re-exports + __all__; the mutable `handler` global;
                #   initialize / pumpAll / terminate
  labels.py     # labels, shapes, indicators, port constants, formatting marker types
  regions.py    # the Region class hierarchy + braille field/property helpers
  buffer.py     # BrailleBuffer, focus-region functions, display-dimension helpers
  _handler.py   # the BrailleHandler class, extension points, FALLBACK_TABLE,
                #   speech-on-routing helpers  (private name: see Invariant 1)
  display.py    # BrailleDisplayDriver, BrailleDisplayGesture, driver discovery
```

`brailleDisplayDrivers/`, `brailleInput`, `brailleTables`, `louisHelper`, and
`bdDetect` remain exactly where they are.

### Content mapping (from current `braille.py`)

**`labels.py`** — constants and label/type definitions (depends only on
`controlTypes`, config flags, `_()`):
`roleLabels`, `positiveStateLabels`, `negativeStateLabels`, `landmarkLabels`,
`CURSOR_SHAPES`, `SELECTION_SHAPE`, `CONTINUATION_SHAPE`,
`END_OF_BRAILLE_OUTPUT_SHAPE`, `INPUT_START_IND`, `INPUT_END_IND`,
`TEXT_SEPARATOR`, `CONTEXTPRES_CHANGEDCONTEXT`, `CONTEXTPRES_FILL`,
`CONTEXTPRES_SCROLL`, `focusContextPresentations`, `AUTOMATIC_PORT`,
`AUTO_DISPLAY_NAME`, `NO_BRAILLE_DISPLAY_NAME`, `USB_PORT`, `BLUETOOTH_PORT`,
`FormatTagDelimiter`, `FormattingMarker`, `fontAttributeFormattingMarkers`.

**`regions.py`** — the Region hierarchy and the braille-generation helpers:
`NVDAObjectHasUsefulText`, `RegionWithPositions`, `Region`, `TextRegion`,
`_getAnnotationProperty`, `getPropertiesBraille`, `NVDAObjectRegion`,
`ReviewNVDAObjectRegion`, `getControlFieldBraille`,
`_getControlFieldForLayoutPresentation`, `_getControlFieldForTableCell`,
`_getControlFieldForReportStart`, `getFormatFieldBraille`,
`getParagraphStartMarker`, `_getFormattingTags`, `_appendFormattingMarker`,
`TextInfoRegion`, `CursorManagerRegion`, `ReviewTextInfoRegion`,
`ReviewCursorManagerRegion`, `_routingShouldMoveSystemCaret`, `rindex`.

**`buffer.py`** — the buffer and focus/window machinery:
`_WindowRowPositions`, `BrailleBuffer`, the focus-ancestor cache globals,
`invalidateCachedFocusAncestors`, `getFocusContextRegions`, `getFocusRegions`,
`formatCellsForLog`, `DisplayDimensions`.

**`_handler.py`** — the handler and its surrounding state:
`FALLBACK_TABLE`, the extension points (`pre_writeCells`, `filter_displaySize`,
`filter_displayDimensions`, `displaySizeChanged`, `displayChanged`,
`decide_enabled`, `_decide_disabledIncludesMessages`, `_pre_showBrailleMessage`,
`_post_dismissBrailleMessage`), `BrailleHandler`, `_speakOnRouting`,
`_speakOnNavigatingByUnit`.

**`display.py`** — driver base classes and discovery:
`_getDisplayDriver`, `getDisplayList`, `RENAMED_DRIVERS`, `BrailleDisplayDriver`,
`BrailleDisplayGesture`, `getSerialPorts`, `getDisplayDrivers`.

**`__init__.py`** — the public facade (see below):
the `handler` global, `initialize`, `pumpAll`, `terminate`, plus all re-exports.

Exact line-by-line placement is finalised during implementation; the grouping above
is the contract.

## Public API preservation

`__init__.py` reconstructs the exact attribute surface that `braille.py` exposes
today:

- **Public symbols** are re-exported explicitly and listed in a hand-maintained
  `__all__` (controlTypes style). Example: `from .display import BrailleDisplayDriver`
  so `braille.BrailleDisplayDriver` resolves even though the class lives in
  `braille.display`.
- **Private symbols with external consumers** are bound in `__init__.py` but
  **excluded from `__all__`**, so `braille._x` keeps resolving for code outside the
  package without advertising them in `from braille import *`. The known external
  private consumers are:
  - `_getDisplayDriver` — used by `bdDetect.py`, `gui/settingsDialogs.py`, and unit
    tests. (Lives in `display.py`.)
  - `_WindowRowPositions` — used by unit tests. (Lives in `buffer.py`.)
  - `_pre_showBrailleMessage`, `_post_dismissBrailleMessage`,
    `_decide_disabledIncludesMessages` — used by `_remoteClient/localMachine.py`.
    (Live in `_handler.py`.)
- This split **renames nothing**, so a `braille/deprecatedAliases.py` is **not**
  needed. The controlTypes-style alias module is reserved for any future symbol
  rename/removal.

## Invariants

These are the rules the implementation must hold to.

### Invariant 1 — the mutable `handler` global stays in `__init__.py`

`braille.handler` is a module-level global, reassigned at runtime (`initialize()`
sets it to a `BrailleHandler` instance; `terminate()` clears it) and read across the
codebase as `braille.handler`. It must live in `__init__.py`:

- If it were re-exported from a submodule (`from ._handler import handler`), the name
  in the package namespace would be bound once at import and would **not** track later
  reassignment — `braille.handler` would stay stale.
- So the `handler` global and the lifecycle functions that reassign it
  (`initialize`, `pumpAll`, `terminate`) live in `__init__.py`; the `BrailleHandler`
  **class** lives in `_handler.py`.
- This also forces the handler submodule's name: a public `handler.py` would collide
  with the `braille.handler` global attribute. The submodule is therefore named
  `_handler.py` (private). It is the only submodule whose name clashes with an
  existing global, so it is the only private submodule.

### Invariant 2 — facade access rules

- **Internal submodules may use the facade for public symbols.** Referencing
  `braille.BrailleDisplayDriver` (or any public `braille.X`) from inside a submodule
  is allowed, as is a relative import — implementer's choice for readability.
- **Internal submodules must never use the facade for private symbols.** A private
  symbol (`_x`) needed by another submodule is imported **directly from the defining
  submodule** via a relative import (`from .display import _getDisplayDriver`), never
  as `braille._x`.
- **External consumers** keep using `braille.X` (public) and `braille._x` (the bound
  privates listed above) unchanged.
- A public-surface snapshot test asserts the full `braille.X` set (public symbols
  *and* the externally-used privates) is unchanged before/after the refactor.

### Invariant 3 — deferred annotations / import ordering

Some class bodies use eagerly-evaluated annotations that reference sibling modules
(e.g. `BrailleHandler` has `_lastRequestedDeviceMatch: bdDetect.DeviceMatch | None`).
Two measures keep this safe:

- Add `from __future__ import annotations` to the new submodules so annotations are
  not evaluated at class-definition time. (Dataclasses and `NamedTuple` subclasses in
  these modules — `_WindowRowPositions`, `DisplayDimensions`, `FormattingMarker` —
  continue to work with stringised annotations.)
- Import siblings in dependency order in `__init__.py`:
  `labels` → `regions` → `buffer` → `display` → `_handler`. Cross-submodule
  references to other submodules use relative imports; `_handler` and `display`
  depend on the earlier modules, not vice versa.

### Invariant 4 — preserve existing import discipline

- `braille` → `brailleInput` stays a **late import** (inside functions/methods), as
  today, to avoid the `brailleInput` → `braille` top-level cycle.
- The existing `braille` ↔ `bdDetect` relationship is preserved: `bdDetect` keeps
  `import braille` and reads `braille.X` (incl. `braille._getDisplayDriver`,
  `braille.handler`) at **runtime**. Because `bdDetect` touches `braille` only at
  runtime, the package re-exports satisfy it with no import-time cycle.

## Implementation mechanics

1. Create the `braille/` package directory; move `braille.py`'s contents into the
   submodules per the content mapping, preserving code verbatim (no behaviour
   changes) other than the import rewiring the move requires.
2. Wire relative imports between submodules per Invariants 2–4.
3. Build `__init__.py`: explicit re-exports, the `handler` global, `initialize` /
   `pumpAll` / `terminate`, the hand-maintained `__all__`, and the bound (non-`__all__`)
   external privates.
4. Add `from __future__ import annotations` to submodules.
5. No changes to external consumers are required for this split. (`bdDetect`,
   `gui/settingsDialogs.py`, `_remoteClient/localMachine.py`, drivers, add-ons all
   keep working through the preserved surface.)

## Risks

- **Stale `handler` global** if mis-placed — mitigated by Invariant 1 and the
  snapshot test.
- **Import cycles / ordering** — mitigated by Invariants 3 and 4; verified by booting
  NVDA from source.
- **Dropped/renamed symbol slipping through** — mitigated by the public-surface
  snapshot test comparing the pre-refactor and post-refactor `braille.X` attribute
  set.
- **`from __future__ import annotations` interactions** — runtime annotation
  consumers (dataclasses, `NamedTuple`) are known-compatible; if any code calls
  `typing.get_type_hints()` on a braille class it must still resolve names, which the
  relative imports satisfy. Low risk; covered by the unit + smoke tests.
- **Build packaging** — the package and its submodules must be picked up by `scons
  dist` (auto-discovered; verify).

## Verification & testing

- `scons source` succeeds; NVDA boots from source.
- `import braille` works; every `braille.X` (public + the bound privates) resolves.
- New unit test: public-surface snapshot — assert the set of `braille` public
  attributes (and the externally-used privates) matches the expected list.
- Existing `tests/unit/test_braille/` package (already split into
  `test_brailleDisplayDrivers.py`, `test_calculateWindowRowBufferOffsets.py`,
  `test_windowBrailleCells.py`, …) passes unchanged.
- `scons dist` produces a build that includes the `braille` subpackage.
- Manual smoke test: a real or emulated braille display connects (incl. auto-detect
  via `bdDetect`), braille input works, and braille table switching works.
- Update `user_docs/en/changes.md` "Changes for Developers" with a note that
  `braille` is now a package (no public API change).

## Follow-up

A separate spec will cover relocating `brailleInput`, `brailleTables`, `louisHelper`,
and `bdDetect` into the `braille` package with mixed-per-module back-compat shims
(transparent `sys.modules` aliases for the heavy add-on surfaces; deprecation shims
via `utils._deprecate` for lighter ones), and updating bundled callers to the
canonical paths.
