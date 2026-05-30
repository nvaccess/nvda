# braille.py Package Split — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split `source/braille.py` (~4256 lines) into a `source/braille/` package of focused submodules while preserving the exact `braille.X` public API.

**Architecture:** Convert the module to a package, then extract cohesive blocks one submodule at a time, each guarded by a regression test and the existing `tests/unit/test_braille/` suite. `__init__.py` becomes a facade that re-exports every public symbol (explicit `__all__`, controlTypes precedent) plus the handful of private symbols external code already uses, and keeps the mutable `handler` global and the `initialize`/`pumpAll`/`terminate` lifecycle functions.

**Tech Stack:** Python 3.11, NVDA build via `uv`/SCons, unittest (`rununittests.bat`), ruff + pyright (`runlint.bat`).

**Spec:** `docs/superpowers/specs/2026-05-30-braille-package-split-design.md`

**Branch:** `splitBraillePackage` (already created).

---

## Background the implementer must know

- **Tabs, not spaces.** One tab per indent level. UTF-8, LF line endings. Match the existing file exactly.
- **`_()` is a builtin** injected by NVDA's gettext setup; label dicts call it at import time. This already works in the unit-test harness — do not import it.
- **Unit tests run in a harness** (`rununittests.bat`) that initialises enough of NVDA that `import braille` works. The existing tests in `tests/unit/test_braille/` import `braille` and exercise it; they are the primary safety net. Keep them green at every step.
- **`from __future__ import annotations`** goes at the top of each *new submodule* (after the license header, before other imports). It makes annotations lazy strings so class-body annotations that name sibling modules (e.g. `bdDetect.DeviceMatch`) never evaluate at import time. Dataclasses / `NamedTuple` subclasses in these modules continue to work with stringised annotations.
- **Facade access rules (from the spec, enforce strictly):**
  - A submodule may reference a **public** symbol via the facade (`braille.handler`) or via relative import — your choice for readability.
  - A submodule must reference a **private** symbol (`_x`) **only** by relative import from the defining submodule (`from .display import _getDisplayDriver`) — never `braille._x`.
- **The mutable `handler` global lives in `__init__.py`.** Submodules that need it do `import braille` and read `braille.handler` at runtime (never `from braille import handler`, which would capture a stale `None`).
- **Move code verbatim.** Each extraction moves existing definitions unchanged except for the import wiring this plan specifies. Do not refactor logic, rename symbols, or rewrite docstrings in this work.
- **Line numbers in this plan are hints from the pre-split file and shift after each extraction.** Locate blocks by symbol name, not by line number.

### Verification commands (used throughout)

- New surface test only: `rununittests.bat tests.unit.test_braille.test_publicSurface`
- Whole braille suite: `rununittests.bat tests.unit.test_braille`
- Lint + format + pyright: `runlint.bat`
- Build the source tree (proves the package is picked up): `scons source`

---

## File structure

Created:
- `source/braille/__init__.py` — facade (from the renamed `braille.py`); explicit re-exports, `__all__`, `handler` global, `initialize`/`pumpAll`/`terminate`.
- `source/braille/labels.py` — labels, shapes, indicators, port constants, formatting-marker types.
- `source/braille/regions.py` — Region hierarchy, braille field/property helpers, the two speak-on-navigation helpers.
- `source/braille/buffer.py` — `BrailleBuffer`, focus-region functions, `DisplayDimensions`, `formatCellsForLog`.
- `source/braille/display.py` — `BrailleDisplayDriver`, `BrailleDisplayGesture`, driver discovery, `RENAMED_DRIVERS`.
- `source/braille/_handler.py` — `BrailleHandler` class, extension points, `FALLBACK_TABLE`.
- `tests/unit/test_braille/test_publicSurface.py` — public-surface regression test.

Modified:
- Nothing outside the package and the new test. External consumers (`bdDetect.py`, `gui/settingsDialogs.py`, `_remoteClient/localMachine.py`, `brailleDisplayDrivers/*`, add-ons) keep working through the preserved surface.
- `user_docs/en/changes.md` — developer note (final task).

Unchanged / out of scope: `brailleInput`, `brailleTables`, `louisHelper`, `bdDetect` stay top-level; `brailleDisplayDrivers/` stays top-level.

---

## Task 1: Public-surface regression test (the anchor)

This characterization test captures the current `braille.X` surface so later extractions cannot silently drop or hide a symbol. It must pass against the unmodified `braille.py` and keep passing through every later task.

**Files:**
- Test: `tests/unit/test_braille/test_publicSurface.py` (create)

- [ ] **Step 1: Write the test**

Create `tests/unit/test_braille/test_publicSurface.py` with exactly this content (tabs for indentation):

```python
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Regression tests guarding the public attribute surface of the braille package.

Splitting braille.py into a package must not drop or hide any symbol that external
code (add-ons, drivers, other NVDA modules, tests) reaches as ``braille.X``.
"""

import unittest

import braille


#: Public symbols that must remain reachable as ``braille.<name>``.
EXPECTED_PUBLIC = frozenset(
	{
		# Classes
		"Region",
		"TextRegion",
		"NVDAObjectRegion",
		"ReviewNVDAObjectRegion",
		"TextInfoRegion",
		"CursorManagerRegion",
		"ReviewTextInfoRegion",
		"ReviewCursorManagerRegion",
		"BrailleBuffer",
		"DisplayDimensions",
		"BrailleHandler",
		"BrailleDisplayDriver",
		"BrailleDisplayGesture",
		"FormatTagDelimiter",
		"FormattingMarker",
		# Functions
		"NVDAObjectHasUsefulText",
		"getDisplayList",
		"getPropertiesBraille",
		"getControlFieldBraille",
		"getFormatFieldBraille",
		"getParagraphStartMarker",
		"invalidateCachedFocusAncestors",
		"getFocusContextRegions",
		"getFocusRegions",
		"formatCellsForLog",
		"initialize",
		"pumpAll",
		"terminate",
		"getSerialPorts",
		"getDisplayDrivers",
		"rindex",
		# Constants and module-level state
		"FALLBACK_TABLE",
		"roleLabels",
		"positiveStateLabels",
		"negativeStateLabels",
		"landmarkLabels",
		"CURSOR_SHAPES",
		"SELECTION_SHAPE",
		"CONTINUATION_SHAPE",
		"END_OF_BRAILLE_OUTPUT_SHAPE",
		"INPUT_START_IND",
		"INPUT_END_IND",
		"TEXT_SEPARATOR",
		"CONTEXTPRES_CHANGEDCONTEXT",
		"CONTEXTPRES_FILL",
		"CONTEXTPRES_SCROLL",
		"focusContextPresentations",
		"RegionWithPositions",
		"AUTOMATIC_PORT",
		"AUTO_DISPLAY_NAME",
		"NO_BRAILLE_DISPLAY_NAME",
		"USB_PORT",
		"BLUETOOTH_PORT",
		"fontAttributeFormattingMarkers",
		"RENAMED_DRIVERS",
		"handler",
		# Extension points
		"pre_writeCells",
		"filter_displaySize",
		"filter_displayDimensions",
		"displaySizeChanged",
		"displayChanged",
		"decide_enabled",
	}
)

#: Private symbols with known external consumers (bdDetect, gui, _remoteClient, tests).
#: They must remain reachable as ``braille._<name>`` but must NOT appear in ``braille.__all__``.
EXPECTED_BOUND_PRIVATE = frozenset(
	{
		"_getDisplayDriver",
		"_WindowRowPositions",
		"_pre_showBrailleMessage",
		"_post_dismissBrailleMessage",
		"_decide_disabledIncludesMessages",
	}
)


class TestBraillePublicSurface(unittest.TestCase):
	def test_publicSymbolsPresent(self):
		missing = sorted(name for name in EXPECTED_PUBLIC if not hasattr(braille, name))
		self.assertEqual(missing, [], f"public braille symbols missing: {missing}")

	def test_boundPrivatesPresent(self):
		missing = sorted(name for name in EXPECTED_BOUND_PRIVATE if not hasattr(braille, name))
		self.assertEqual(missing, [], f"externally-used private braille symbols missing: {missing}")
```

- [ ] **Step 2: Run the test against the current `braille.py`**

Run: `rununittests.bat tests.unit.test_braille.test_publicSurface`
Expected: PASS (2 tests). This is the baseline. If any symbol is reported missing, the `EXPECTED_PUBLIC` list is wrong for this codebase — reconcile it with the actual current `braille` module before continuing.

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_braille/test_publicSurface.py
git commit -m "test(braille): characterize public surface before package split"
```

---

## Task 2: Convert `braille.py` to a package and add `__all__`

Turn the single module into a package without splitting content yet, and make the public contract explicit with `__all__`. This is the safe structural pivot.

**Files:**
- Rename: `source/braille.py` → `source/braille/__init__.py`
- Modify: `source/braille/__init__.py` (add `__all__`)
- Modify: `tests/unit/test_braille/test_publicSurface.py` (add `__all__` checks)

- [ ] **Step 1: Rename the module into a package (preserve history)**

```bash
git mv source/braille.py source/braille/__init__.py
```

- [ ] **Step 2: Run the braille suite to confirm the package imports identically**

Run: `rununittests.bat tests.unit.test_braille`
Expected: PASS (all existing tests + the 2 surface tests). The content is unchanged, only its location.

- [ ] **Step 3: Add an explicit `__all__` at the end of `source/braille/__init__.py`**

Append this block at the very end of `source/braille/__init__.py` (tabs for indentation). The list mirrors `EXPECTED_PUBLIC`; the five externally-used privates are deliberately **excluded**:

```python
#: Public API of the braille package.
#: Keep in sync with tests/unit/test_braille/test_publicSurface.py::EXPECTED_PUBLIC.
__all__ = [
	"AUTOMATIC_PORT",
	"AUTO_DISPLAY_NAME",
	"BLUETOOTH_PORT",
	"BrailleBuffer",
	"BrailleDisplayDriver",
	"BrailleDisplayGesture",
	"BrailleHandler",
	"CONTEXTPRES_CHANGEDCONTEXT",
	"CONTEXTPRES_FILL",
	"CONTEXTPRES_SCROLL",
	"CONTINUATION_SHAPE",
	"CURSOR_SHAPES",
	"CursorManagerRegion",
	"DisplayDimensions",
	"END_OF_BRAILLE_OUTPUT_SHAPE",
	"FALLBACK_TABLE",
	"FormatTagDelimiter",
	"FormattingMarker",
	"INPUT_END_IND",
	"INPUT_START_IND",
	"NO_BRAILLE_DISPLAY_NAME",
	"NVDAObjectHasUsefulText",
	"NVDAObjectRegion",
	"Region",
	"RegionWithPositions",
	"RENAMED_DRIVERS",
	"ReviewCursorManagerRegion",
	"ReviewNVDAObjectRegion",
	"ReviewTextInfoRegion",
	"SELECTION_SHAPE",
	"TEXT_SEPARATOR",
	"TextInfoRegion",
	"TextRegion",
	"USB_PORT",
	"decide_enabled",
	"displayChanged",
	"displaySizeChanged",
	"filter_displayDimensions",
	"filter_displaySize",
	"focusContextPresentations",
	"fontAttributeFormattingMarkers",
	"formatCellsForLog",
	"getControlFieldBraille",
	"getDisplayDrivers",
	"getDisplayList",
	"getFocusContextRegions",
	"getFocusRegions",
	"getFormatFieldBraille",
	"getParagraphStartMarker",
	"getPropertiesBraille",
	"getSerialPorts",
	"handler",
	"initialize",
	"invalidateCachedFocusAncestors",
	"landmarkLabels",
	"negativeStateLabels",
	"positiveStateLabels",
	"pre_writeCells",
	"pumpAll",
	"rindex",
	"roleLabels",
	"terminate",
]
```

- [ ] **Step 4: Extend the surface test with `__all__` checks**

In `tests/unit/test_braille/test_publicSurface.py`, add these two methods to `TestBraillePublicSurface` (tabs):

```python
	def test_publicSymbolsExported(self):
		notExported = sorted(EXPECTED_PUBLIC - set(braille.__all__))
		self.assertEqual(notExported, [], f"public symbols not in braille.__all__: {notExported}")
		unresolved = sorted(name for name in braille.__all__ if not hasattr(braille, name))
		self.assertEqual(unresolved, [], f"names in braille.__all__ that don't resolve: {unresolved}")

	def test_privatesNotExported(self):
		leaked = sorted(EXPECTED_BOUND_PRIVATE & set(braille.__all__))
		self.assertEqual(leaked, [], f"private symbols leaked into braille.__all__: {leaked}")
```

- [ ] **Step 5: Run the surface test**

Run: `rununittests.bat tests.unit.test_braille.test_publicSurface`
Expected: PASS (4 tests). If `test_publicSymbolsExported` reports names "not in `__all__`", a public symbol is missing from the `__all__` list — add it.

- [ ] **Step 6: Build the source tree**

Run: `scons source`
Expected: completes without error (the package is picked up).

- [ ] **Step 7: Commit**

```bash
git add source/braille/__init__.py tests/unit/test_braille/test_publicSurface.py
git commit -m "refactor(braille): convert braille module to a package with explicit __all__"
```

---

## Task 3: Extract `labels.py`

Move the labels, shapes, indicators, port constants, and formatting-marker types — the base layer with no dependencies on other braille submodules.

**Files:**
- Create: `source/braille/labels.py`
- Modify: `source/braille/__init__.py`

**Symbols to move** (originally ~lines 96–453 in `braille.py`): `roleLabels`, `positiveStateLabels`, `negativeStateLabels`, `landmarkLabels`, `CURSOR_SHAPES`, `SELECTION_SHAPE`, `CONTINUATION_SHAPE`, `END_OF_BRAILLE_OUTPUT_SHAPE`, `INPUT_START_IND`, `INPUT_END_IND`, `FormatTagDelimiter`, `TEXT_SEPARATOR`, `CONTEXTPRES_CHANGEDCONTEXT`, `CONTEXTPRES_FILL`, `CONTEXTPRES_SCROLL`, `focusContextPresentations`, `AUTOMATIC_PORT`, `AUTO_DISPLAY_NAME`, `NO_BRAILLE_DISPLAY_NAME`, `USB_PORT`, `BLUETOOTH_PORT`, `FormattingMarker`, `fontAttributeFormattingMarkers`.

> Note: `FALLBACK_TABLE` (line 93) is **not** a label — it depends on `config` and belongs with the handler. Leave it in `__init__.py` for now; it moves in Task 7.

- [ ] **Step 1: Create `source/braille/labels.py`**

Start the file with the license header (copy the 5 comment lines from the top of `__init__.py`), then:

```python
from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple

import controlTypes
```

Then paste the moved symbol definitions verbatim (tabs preserved) below the imports.

- [ ] **Step 2: Replace the moved block in `__init__.py` with a re-export**

Delete the moved definitions from `__init__.py`. In their place (keep them roughly where they were so surrounding code still reads top-to-bottom) add:

```python
from .labels import (
	roleLabels,
	positiveStateLabels,
	negativeStateLabels,
	landmarkLabels,
	CURSOR_SHAPES,
	SELECTION_SHAPE,
	CONTINUATION_SHAPE,
	END_OF_BRAILLE_OUTPUT_SHAPE,
	INPUT_START_IND,
	INPUT_END_IND,
	FormatTagDelimiter,
	TEXT_SEPARATOR,
	CONTEXTPRES_CHANGEDCONTEXT,
	CONTEXTPRES_FILL,
	CONTEXTPRES_SCROLL,
	focusContextPresentations,
	AUTOMATIC_PORT,
	AUTO_DISPLAY_NAME,
	NO_BRAILLE_DISPLAY_NAME,
	USB_PORT,
	BLUETOOTH_PORT,
	FormattingMarker,
	fontAttributeFormattingMarkers,
)
```

These re-exports both expose the names as `braille.X` and keep the still-in-`__init__` code (which references e.g. `roleLabels`, `TEXT_SEPARATOR`) resolving.

- [ ] **Step 3: Run lint to prune now-unused imports in `__init__.py`**

Run: `runlint.bat`
Expected: PASS. ruff removes imports in `__init__.py` that were only used by the moved code (e.g. `from enum import StrEnum` if nothing else uses it). Fix any reported error. If pyright reports an undefined name in `labels.py`, add the missing import there.

- [ ] **Step 4: Run the braille suite**

Run: `rununittests.bat tests.unit.test_braille`
Expected: PASS (all tests, including the 4 surface tests).

- [ ] **Step 5: Commit**

```bash
git add source/braille/labels.py source/braille/__init__.py
git commit -m "refactor(braille): extract labels and constants into braille.labels"
```

---

## Task 4: Extract `regions.py`

Move the Region class hierarchy, the braille field/property helpers, and the two speak-on-navigation helpers (their only callers are in `TextInfoRegion`).

**Files:**
- Create: `source/braille/regions.py`
- Modify: `source/braille/__init__.py`

**Symbols to move** (originally ~lines 489–1838 plus 4226–4257): `NVDAObjectHasUsefulText`, `RegionWithPositions`, `Region`, `TextRegion`, `_getAnnotationProperty`, `getPropertiesBraille`, `NVDAObjectRegion`, `ReviewNVDAObjectRegion`, `getControlFieldBraille`, `_getControlFieldForLayoutPresentation`, `_getControlFieldForTableCell`, `_getControlFieldForReportStart`, `getFormatFieldBraille`, `getParagraphStartMarker`, `_getFormattingTags`, `_appendFormattingMarker`, `TextInfoRegion`, `CursorManagerRegion`, `ReviewTextInfoRegion`, `ReviewCursorManagerRegion`, `_routingShouldMoveSystemCaret`, `rindex`, `_speakOnRouting`, `_speakOnNavigatingByUnit`.

> `RegionWithPositions` (a `namedtuple`) lives at line ~392 in the original; move it here. `_speakOnRouting`/`_speakOnNavigatingByUnit` live at the end of the original file (~4226–4257); move them here too — `TextInfoRegion` is their sole caller.

- [ ] **Step 1: Create `source/braille/regions.py`**

License header, then:

```python
from __future__ import annotations
```

Then copy the **entire top-of-file import block** from `__init__.py` (the `import …` / `from … import …` lines and the `if TYPE_CHECKING:` block) into `regions.py` below the future import. Then add the sibling import:

```python
from .labels import (
	roleLabels,
	positiveStateLabels,
	negativeStateLabels,
	landmarkLabels,
	SELECTION_SHAPE,
	INPUT_START_IND,
	INPUT_END_IND,
	TEXT_SEPARATOR,
	FormatTagDelimiter,
	fontAttributeFormattingMarkers,
)

import braille
```

Then paste the moved definitions verbatim below.

- [ ] **Step 2: Qualify the `handler` global references in `regions.py`**

The moved code reads the module-global `handler` in four places (originally lines 594, 631, 1745, 1749). Change each bare `handler` to `braille.handler`. Concretely:
- `louisHelper.getTableLanguage(handler.table.fileName)` → `louisHelper.getTableLanguage(braille.handler.table.fileName)`
- `[handler.table.fileName, "braille-patterns.cti"]` → `[braille.handler.table.fileName, "braille-patterns.cti"]`
- both `handler.autoScroll(enable=False)` → `braille.handler.autoScroll(enable=False)`

Leave `brailleInput.handler` references untouched (different object — that is `brailleInput`'s own handler), and keep the existing late `import brailleInput` statements inside methods as-is.

- [ ] **Step 3: Replace the moved block in `__init__.py` with re-exports**

Remove the moved definitions from `__init__.py` and add:

```python
from .regions import (
	NVDAObjectHasUsefulText,
	RegionWithPositions,
	Region,
	TextRegion,
	getPropertiesBraille,
	NVDAObjectRegion,
	ReviewNVDAObjectRegion,
	getControlFieldBraille,
	getFormatFieldBraille,
	getParagraphStartMarker,
	TextInfoRegion,
	CursorManagerRegion,
	ReviewTextInfoRegion,
	ReviewCursorManagerRegion,
	rindex,
)
```

(The underscore helpers in `regions.py` — `_getAnnotationProperty`, the `_getControlField*` helpers, `_getFormattingTags`, `_appendFormattingMarker`, `_routingShouldMoveSystemCaret`, `_speakOnRouting`, `_speakOnNavigatingByUnit` — have no external consumers, so they are not re-exported.)

- [ ] **Step 4: Run lint**

Run: `runlint.bat`
Expected: PASS. ruff prunes the now-unused imports left behind in `__init__.py`. If pyright flags an undefined name in `regions.py`, it is a symbol the moved code uses that is defined elsewhere in `braille` — resolve it: if public, `braille.<name>` (or add it to the `from .labels import` list); if it is a name still living in `__init__` that has not been extracted yet, import it with `from braille import <name>` at runtime usage or leave the reference as `braille.<name>`.

- [ ] **Step 5: Run the braille suite**

Run: `rununittests.bat tests.unit.test_braille`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add source/braille/regions.py source/braille/__init__.py
git commit -m "refactor(braille): extract Region classes and helpers into braille.regions"
```

---

## Task 5: Extract `buffer.py`

Move the buffer and focus/window machinery.

**Files:**
- Create: `source/braille/buffer.py`
- Modify: `source/braille/__init__.py`

**Symbols to move** (originally ~lines 1845–2509 and the focus-cache globals at ~2296): `_WindowRowPositions`, the focus-ancestor cache globals (`_cachedFocusAncestors`, `_cachedFocusAncestorsEnd`), `BrailleBuffer`, `invalidateCachedFocusAncestors`, `getFocusContextRegions`, `getFocusRegions`, `formatCellsForLog`, `DisplayDimensions`.

- [ ] **Step 1: Create `source/braille/buffer.py`**

License header, then:

```python
from __future__ import annotations
```

Copy the top-of-file import block from `__init__.py` (as in Task 4), then add the sibling imports:

```python
from .labels import (
	TEXT_SEPARATOR,
	CONTINUATION_SHAPE,
	CONTEXTPRES_CHANGEDCONTEXT,
	CONTEXTPRES_SCROLL,
)
from .regions import (
	Region,
	RegionWithPositions,
	NVDAObjectRegion,
	TextInfoRegion,
)
```

Then paste the moved definitions verbatim. `buffer.py` does **not** use the `handler` global, so no `import braille` is required here.

- [ ] **Step 2: Replace the moved block in `__init__.py` with re-exports**

```python
from .buffer import (
	BrailleBuffer,
	invalidateCachedFocusAncestors,
	getFocusContextRegions,
	getFocusRegions,
	formatCellsForLog,
	DisplayDimensions,
	_WindowRowPositions,
)
```

(`_WindowRowPositions` is re-exported because unit tests reference `braille._WindowRowPositions`; it stays out of `__all__`.)

- [ ] **Step 3: Run lint**

Run: `runlint.bat`
Expected: PASS. Resolve any undefined-name as in Task 4, Step 4.

- [ ] **Step 4: Run the braille suite**

Run: `rununittests.bat tests.unit.test_braille`
Expected: PASS (includes `test_calculateWindowRowBufferOffsets`, `test_windowBrailleCells`, `test_focusContextPresentation`, which exercise this code).

- [ ] **Step 5: Commit**

```bash
git add source/braille/buffer.py source/braille/__init__.py
git commit -m "refactor(braille): extract BrailleBuffer and focus handling into braille.buffer"
```

---

## Task 6: Extract `display.py`

Move the driver base classes and discovery.

**Files:**
- Create: `source/braille/display.py`
- Modify: `source/braille/__init__.py`

**Symbols to move** (originally ~lines 507–551, 3570–3577, 3602–4224): `_getDisplayDriver`, `getDisplayList`, `RENAMED_DRIVERS`, `BrailleDisplayDriver`, `BrailleDisplayGesture`, `getSerialPorts`, `getDisplayDrivers`.

- [ ] **Step 1: Create `source/braille/display.py`**

License header, then:

```python
from __future__ import annotations
```

Copy the top-of-file import block from `__init__.py`, then add:

```python
from .labels import (
	AUTOMATIC_PORT,
	AUTO_DISPLAY_NAME,
	NO_BRAILLE_DISPLAY_NAME,
	USB_PORT,
	BLUETOOTH_PORT,
)

import braille
```

Then paste the moved definitions verbatim.

- [ ] **Step 2: Qualify the `handler` global references in `display.py`**

The moved code reads the module-global `handler` (originally lines 3900, 3903, 4056, 4098, 4156, 4157). Change each bare `handler` to `braille.handler`:
- `winBindings.kernel32.CancelWaitableTimer(handler.ackTimerHandle)` → `…(braille.handler.ackTimerHandle)`
- `handler._writeCellsInBackground()` → `braille.handler._writeCellsInBackground()`
- `display = handler.display` → `display = braille.handler.display`
- `[inputCore.manager.userGestureMap, handler.display.gestureMap]` → `[inputCore.manager.userGestureMap, braille.handler.display.gestureMap]`
- `handler.display.name.lower()` → `braille.handler.display.name.lower()`
- `description = handler.display.description` → `description = braille.handler.display.description`

Keep existing late `import brailleInput` statements inside methods as-is.

- [ ] **Step 3: Replace the moved block in `__init__.py` with re-exports**

```python
from .display import (
	getDisplayList,
	RENAMED_DRIVERS,
	BrailleDisplayDriver,
	BrailleDisplayGesture,
	getSerialPorts,
	getDisplayDrivers,
	_getDisplayDriver,
)
```

(`_getDisplayDriver` is re-exported because `bdDetect`, `gui/settingsDialogs.py`, and tests reference `braille._getDisplayDriver`; it stays out of `__all__`.)

- [ ] **Step 4: Run lint**

Run: `runlint.bat`
Expected: PASS. Resolve undefined names as before.

- [ ] **Step 5: Run the braille suite**

Run: `rununittests.bat tests.unit.test_braille`
Expected: PASS (includes `test_brailleDisplayDrivers`, `test_displayTextForGestureIdentifier`).

- [ ] **Step 6: Commit**

```bash
git add source/braille/display.py source/braille/__init__.py
git commit -m "refactor(braille): extract display driver classes into braille.display"
```

---

## Task 7: Extract `_handler.py`

Move the handler class, extension points, and `FALLBACK_TABLE`. The submodule is private (`_handler`) because a public `handler.py` would clash with the `braille.handler` global. The `handler` global itself and the lifecycle functions stay in `__init__.py`.

**Files:**
- Create: `source/braille/_handler.py`
- Modify: `source/braille/__init__.py`

**Symbols to move** (originally lines 93, 2446–2542, 2547–3568): `FALLBACK_TABLE`, the extension points (`pre_writeCells`, `filter_displaySize`, `filter_displayDimensions`, `displaySizeChanged`, `displayChanged`, `decide_enabled`, `_decide_disabledIncludesMessages`, `_pre_showBrailleMessage`, `_post_dismissBrailleMessage`), and `BrailleHandler`.

**Symbols that STAY in `__init__.py`:** the `handler` global (`handler: Optional[BrailleHandler] = None`) and `initialize`, `pumpAll`, `terminate` (originally lines 3577–3601).

- [ ] **Step 1: Create `source/braille/_handler.py`**

License header, then:

```python
from __future__ import annotations
```

Copy the top-of-file import block from `__init__.py`, then add the sibling imports:

```python
from .labels import (
	AUTO_DISPLAY_NAME,
	NO_BRAILLE_DISPLAY_NAME,
	CONTEXTPRES_CHANGEDCONTEXT,
	TEXT_SEPARATOR,
)
from .regions import (
	Region,
	NVDAObjectRegion,
	TextInfoRegion,
)
from .buffer import (
	BrailleBuffer,
	DisplayDimensions,
	getFocusContextRegions,
	getFocusRegions,
)
from .display import (
	BrailleDisplayDriver,
	_getDisplayDriver,
)

import braille
```

Then paste `FALLBACK_TABLE`, the extension points, and `BrailleHandler` verbatim. (`getFocusContextRegions`/`getFocusRegions` live in `buffer.py` from Task 5, hence the `.buffer` import group.)

- [ ] **Step 2: Qualify the `handler` global references in `_handler.py`**

`BrailleHandler` methods read the module-global `handler` (originally lines 2720, 2721, 2722). Change each bare `handler` to `braille.handler`:
- `handler.mainBuffer.focus(_showSpeechInBrailleRegions[0])` → `braille.handler.mainBuffer.focus(_showSpeechInBrailleRegions[0])`
- `handler.mainBuffer.update()` → `braille.handler.mainBuffer.update()`
- `handler.update()` → `braille.handler.update()`

- [ ] **Step 3: Update `__init__.py` — keep the lifecycle, re-export the rest**

Remove the moved definitions. Ensure `__init__.py` still contains, in this order near the end:

1. The re-export from `_handler`:

```python
from ._handler import (
	FALLBACK_TABLE,
	BrailleHandler,
	pre_writeCells,
	filter_displaySize,
	filter_displayDimensions,
	displaySizeChanged,
	displayChanged,
	decide_enabled,
	_decide_disabledIncludesMessages,
	_pre_showBrailleMessage,
	_post_dismissBrailleMessage,
)
```

2. The `handler` global and lifecycle functions (these were already in `braille.py` at the end; leave them in `__init__.py` unchanged):

```python
handler: Optional[BrailleHandler] = None


def initialize():
	...  # existing body, unchanged


def pumpAll():
	...  # existing body, unchanged


def terminate():
	...  # existing body, unchanged
```

`initialize`/`terminate` already use `global handler`; because `handler` now lives in `__init__`, those statements work without change. `Optional` must be importable in `__init__` — it is part of the copied `typing` import; if ruff pruned it earlier, re-add `from typing import Optional`.

- [ ] **Step 4: Run lint**

Run: `runlint.bat`
Expected: PASS. This is the largest extraction; resolve any undefined-name reports per Task 4, Step 4. Pay attention to pyright reports in `_handler.py` for names that were module globals in the original (e.g. label names, region/buffer/display classes) — add them to the relevant `from .<module> import` group.

- [ ] **Step 5: Run the braille suite**

Run: `rununittests.bat tests.unit.test_braille`
Expected: PASS (includes `test_handlerExtensionPoints`, `test_routing`, `test_regionLanguageIndexes`, `test_normalizeCellArraySize`).

- [ ] **Step 6: Commit**

```bash
git add source/braille/_handler.py source/braille/__init__.py
git commit -m "refactor(braille): extract BrailleHandler into braille._handler"
```

---

## Task 8: Finalize the facade, lint, build, and document

Tidy `__init__.py` so it is a clean facade, then run the full verification battery.

**Files:**
- Modify: `source/braille/__init__.py`
- Modify: `user_docs/en/changes.md`

- [ ] **Step 1: Tidy `__init__.py`**

Confirm `__init__.py` now contains only: the license header and module docstring; the `from __future__ import annotations` line (add it if missing); the re-export blocks from `.labels`, `.regions`, `.buffer`, `.display`, `._handler` (ordered to respect `labels → regions → buffer → display → _handler`); any imports the lifecycle functions still need (`config`, `typing.Optional`, etc.); the `handler` global; `initialize`/`pumpAll`/`terminate`; and the `__all__` block at the end. Remove any leftover dead code or stray imports.

- [ ] **Step 2: Run the full lint pass**

Run: `runlint.bat`
Expected: PASS (ruff + format + pyright clean across the new package).

- [ ] **Step 3: Run the full braille unit suite**

Run: `rununittests.bat tests.unit.test_braille`
Expected: PASS (all tests, including the 4 surface tests).

- [ ] **Step 4: Run the broader unit suite to catch external importers**

Run: `rununittests.bat`
Expected: PASS. This exercises modules that import `braille` (e.g. anything pulling in `bdDetect`, gui dialogs via tests). If a test fails on an unresolved `braille.X` / `braille._x`, add the missing re-export to `__init__.py` and re-run.

- [ ] **Step 5: Build the source tree and smoke-check imports of external consumers**

Run: `scons source`
Expected: completes without error.

Then verify the known external private consumers still resolve by grepping (these must all map to a re-exported name): `braille._getDisplayDriver` (bdDetect, gui/settingsDialogs), `braille._WindowRowPositions` (tests), `braille._pre_showBrailleMessage` / `braille._post_dismissBrailleMessage` / `braille._decide_disabledIncludesMessages` (_remoteClient/localMachine). The surface test already asserts these; this is a final cross-check.

- [ ] **Step 6: Manual smoke test (checkpoint — requires a machine with NVDA)**

Launch NVDA from source (`runnvda.bat`) and confirm: NVDA starts without errors in the log; if a braille display (real or the NVDA Remote / emulated display) is available, it connects (auto-detection via `bdDetect` works); braille input produces text; switching the output braille table in Braille Settings works. Record the result. If NVDA cannot be launched in this environment, note that this checkpoint is deferred to a reviewer.

- [ ] **Step 7: Add a developer changelog entry**

In `user_docs/en/changes.md`, under the "Changes for Developers" section of the in-development release, add an item (match the file's existing bullet style and add a `#12772` reference):

```markdown
* The `braille` module is now a package (`braille/`), split into focused submodules (`braille.labels`, `braille.regions`, `braille.buffer`, `braille.display`).
  The public API is unchanged: every symbol previously accessed as `braille.X` remains available. (#12772)
```

- [ ] **Step 8: Final commit**

```bash
git add source/braille/__init__.py user_docs/en/changes.md
git commit -m "refactor(braille): finalize package facade and document the split (#12772)"
```

---

## Done criteria

- `source/braille/` is a package of `__init__.py`, `labels.py`, `regions.py`, `buffer.py`, `display.py`, `_handler.py`; no `source/braille.py` remains.
- `rununittests.bat` passes, including `tests.unit.test_braille.test_publicSurface` (4 tests) and the full existing `tests/unit/test_braille/` suite.
- `runlint.bat` passes.
- `scons source` succeeds.
- Every `braille.X` public symbol and the five externally-used `braille._x` privates resolve unchanged.
- `user_docs/en/changes.md` has the developer note referencing #12772.
- Sibling modules (`brailleInput`, `brailleTables`, `louisHelper`, `bdDetect`) and `brailleDisplayDrivers/` are untouched (deferred follow-up).
```
