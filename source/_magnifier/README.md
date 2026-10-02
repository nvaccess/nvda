# NVDA Magnifier (`source/_magnifier/`): handover document

This document is for whoever takes over development of NVDA's built-in magnifier.
It explains how the module is built, why it is built that way, which pitfalls have already been hit, and what is left to do.

It describes the magnifier as shipped in NVDA 2026.2. Work done after that release is out of scope here, so check the code before relying on any detail below.

Throughout this document, native means the Windows Magnification API (`magnification.dll`) reached through `winBindings`. A "native call" is a call into that DLL, and a "native error" is the `OSError` it raises on failure. It never means anything else, such as C++ code in NVDA's own binaries.

---

## 1. Summary

* The magnifier is built on the Windows Magnification API (`magnification.dll`), through the bindings in `source/winBindings/magnification.py`.
* Only one view is actually implemented: full-screen (`FullScreenMagnifier`).
* The Fixed, Docked and Lens views (`FixedMagnifier`, `DockedMagnifier`, `LensMagnifier`) are empty shells. They exist so that view cycling and configuration are already wired up. Section 8 describes the recommended way to build them and what was learned while prototyping the Fixed view.
* Full-screen features: zoom from 100% to 5000% in steps of 50, three color filters, two tracking modes (center, relative), tracking of four sources (mouse, system focus, review cursor, navigator object), manual panning, animated screen overview ("spotlight"), automatic error recovery, coexistence with Screen Curtain, touch support.

---

## 2. Module map

| File | Responsibility |
| --- | --- |
| `__init__.py` | Entry point: the `_magnifier` singleton, `initialize`/`terminate`, `start`/`stop`, and the view factory |
| `magnifier.py` | `Magnifier` base class: lifecycle, update loop, zoom, pan, bounds, errors, Screen Curtain |
| `fullscreenMagnifier.py` | `FullScreenMagnifier`: everything that calls the full-screen Magnification API |
| `fixedMagnifier.py` | Empty shell |
| `dockedMagnifier.py` | Empty shell |
| `lensMagnifier.py` | Empty shell |
| `config.py` | The only access point to `config.conf["magnifier"]` (getters and setters, `ZoomLevel`, `_isDebug`) |
| `commands.py` | Keyboard command logic (called from `globalCommands.py`) and spoken messages |
| `utils/types.py` | Shared enums and NamedTuples (`Coordinates`, `Size`, `MagnifiedView`, `Filter`, `FullScreenMode`...) |
| `utils/focusManager.py` | Computes the position to track (mouse, focus, review, navigator) and the priorities between them |
| `utils/mouseHook.py` | `WH_MOUSE_LL` hook in a dedicated thread |
| `utils/spotlightManager.py` | Screen overview animation (zoom out, then back) |
| `utils/filterHandler.py` | 5x5 color matrices (`MAGCOLOREFFECT`) for the filters |
| `utils/errorHandling.py` | `MagnifierStartError` and the `trackNativeMagnifierErrors` decorator |

Unit tests live in `tests/unit/test_magnifier/`, with shared fixtures in `test_magnifier.py` and focused tests for the implemented magnifier, full-screen API, commands, spotlight, mouse hook, and focus manager.

### Integration points outside the module

The magnifier is not isolated. Any change to its internal API must be reflected here:

| File | Role |
| --- | --- |
| `source/core.py` | Calls `_magnifier.initialize()` on startup and `terminate()` on exit, including when NVDA restarts. |
| `source/globalCommands.py` | Declares scripts and gestures. Contains no logic: it delegates to `_magnifier.commands`. |
| `source/gui/settingsDialogs.py` | `MagnifierPanel`. Writes both to config and to the active instance (`magnifier._panStep`, `magnifier._fullscreenMode`). |
| `source/screenCurtain/_screenCurtain.py` | Calls `onScreenCurtainEnabled()` / `onScreenCurtainDisabled()` on the instance. |
| `source/config/configSpec.py` | `[magnifier]` section and the `debugLog.magnifier` key. |
| `source/config/profileUpgradeSteps.py` | `upgradeConfigFrom_23_to_24`: removes the "true center" key and the `border` tracking mode from older profiles, since both were postponed (section 7.1). |
| `source/winBindings/magnification.py` | ctypes bindings. Each function has an `errcheck` that raises `OSError` (via `WinError()`) when the API returns `FALSE`. |
| `source/winAPI/_displayTracking.py` | `displayChanged` extension point, created for the magnifier. |

---

## 3. Runtime behavior

### 3.1 Lifecycle

On startup, `core.py` calls `_magnifier.initialize()`, which:

1. calls `createMagnifier()` with the view read from config, and stores the result as the single `_magnifier` instance;
2. calls `start()` when the magnifier is enabled in config, which calls `_startMagnifier()` on that instance.

`_startMagnifier()` runs in two stages, base class first:

1. `Magnifier._startMagnifier()` checks Screen Curtain, sets `_isActive` to `True`, and starts the mouse hook;
2. `FullScreenMagnifier._startMagnifier()` then initializes the native API, applies the current filter, and starts the timer.

Afterwards, a keyboard command or the settings panel calls `commands.toggleMagnifier()`, which calls `start()` or `stop()`. On exit, `core.py` calls `_magnifier.terminate()`, which calls `stop(persist=False)`.

Rules to follow:

* There is a single instance, stored in `_magnifier` (`__init__.py`). Access it through `getMagnifier()`. Changing view destroys the instance and creates a new one (`_setMagnifiedView`).
* `start()` always syncs config with the real state through a `try/finally` (`setEnabled(isActive())`). The settings panel checkbox must never lie, even when the start fails.
* `terminate()` calls `stop(persist=False)`: exiting NVDA must not disable the magnifier for the next startup.
* Each subclass calls `super()._startMagnifier()` first, then checks `self._isActive`. If the base class refused to start (Screen Curtain), the subclass must not touch anything, especially not the native API.

### 3.2 The update loop

`Magnifier._updateMagnifier()` is called by a `wx.Timer` in one-shot mode, every 12 ms (`_TIMER_INTERVAL_MS`). It re-arms itself at the end of every pass, including after an error.

On each pass:

1. `_managePanning()`: if the user panned manually and the focus moves, manual panning mode ends.
2. If not in manual panning mode, `currentCoordinates` receives the position computed by the `FocusManager`.
3. `_doUpdate()` (implemented by the subclass) applies the transform.
4. On `OSError` or `COMError`: consecutive error counter. At 3, `_attemptRecovery()`.

Why only these two exception types are caught: they are the two failures that are expected here and that recovery can do something about. `OSError` is what the `winBindings` `errcheck` raises when a Magnification call returns `FALSE`, typically because another process took the API over. `COMError` is what the accessibility layer raises while the `FocusManager` queries the caret or the navigator object, for example `RPC_E_DISCONNECTED` when the application being read goes away. Anything else is a bug in the module: it must reach the log as an unhandled error instead of being counted, retried, and hidden behind a recovery that cannot fix it.

The timer runs on the wx main thread. All Magnification API calls happen on that thread, including those triggered by the mouse (see 3.4).

### 3.3 The coordinate pipeline (full-screen)

Each update turns the position of whatever is being tracked into one call to the native API, in four steps:

1. `FocusManager.getCurrentFocusCoordinates()` returns the raw position, the top-left corner of the tracked object.
2. The `Magnifier.currentCoordinates` setter clamps it through `_clampCoordinates()`, within bounds that depend on the tracking mode.
3. `_getCoordinatesForMode()` adjusts it for the mode: center mode leaves it unchanged, relative mode passes it through `_relativePos()`.
4. `_getMagnifierParameters()` turns it into the top-left corner of the source area, plus the size of that area.

The result is passed to `MagSetFullscreenTransform(zoom, left, top)`, followed by `MagSetInputTransform` when UIAccess is available.

Key points:

* The `currentCoordinates` setter always clamps the coordinates, so the view can never drift off screen whatever the code path. Never write `_currentCoordinates` directly in production code. Tests do it on purpose.
* We track the top-left corner of objects, not their center. Tracking the center of a large object (a list, a text area) pushed its beginning out of view.
* RTL support: in a `WS_EX_LAYOUTRTL` window, the right edge of the object is used (`_isWindowRTL` in `focusManager.py`).
* Clamping currently depends on the tracking mode, not on a setting. In center mode, the view is clamped to the screen edges. In relative mode, it is not, so the Windows 11 taskbar can be reached. A separate "true center" setting was postponed (section 7.1).

### 3.4 Mouse tracking: two paths

The mouse is tracked by two complementary mechanisms:

1. The timer: `FocusManager` reads `winUser.getCursorPos()` every 12 ms, like the other sources.
2. The hook: `MagnifierMouseHook` (`utils/mouseHook.py`) installs a `WH_MOUSE_LL` hook in its own thread with its own message pump. On each `WM_MOUSEMOVE`, `Magnifier._onMouseMove(x, y)` only records the position and posts a `wx.CallAfter(_applyPendingMousePosition)`. Only one `CallAfter` is pending at a time (`_mouseUpdatePending`).

Why: at high Windows scale factors (225%), the wx thread is saturated and the timer no longer keeps its 12 ms pace, so the view lagged behind the cursor. The hook reacts immediately.

Hard rule: `_onMouseMove` must not do anything expensive. `WH_MOUSE_LL` is a global hook. Windows waits for the whole hook chain to return before delivering the real mouse move to the window under the cursor, for the entire system. Calling the Magnification API from this callback would slow down the mouse for all of Windows, even though the API itself is thread-safe.

Other hook details: the ctypes function is kept in `self._cCallback` so it is not garbage collected, the hook is installed and removed in the same thread (a Windows requirement), and `PeekMessage(PM_NOREMOVE)` creates the thread's message queue so that `PostThreadMessage(WM_QUIT)` works on stop.

### 3.5 Focus source priority

`FocusManager.getCurrentFocusCoordinates()` queries all four sources on every pass and only reacts to a change. Priority order, each source being considered only when its "follow" setting is enabled:

1. Mouse, if it moved or if the left button is held down (drag and drop).
2. Table special case: if the system focus and the navigator object change at the same time while the review cursor does not (numpad navigation in a table), the navigator object wins.
3. System focus (system caret position, including in browse mode; falls back to the focus object location).
4. Review cursor.
5. Navigator object.

If nothing changed: we stay on the last active source as long as it is enabled. If it has been disabled, the view freezes at `_lastReportedCoordinates`. It does not jump to another source. This is what makes "disable all / restore" (`toggleAllFollowStates`) usable.

Each source keeps a "last valid position": a `(0, 0)` position is treated as invalid and replaced by the previous one.

---

## 4. How to develop in this module

### 4.1 NVDA conventions used here

* Tab indentation, `camelCase` for functions and variables, `PascalCase` for classes. No `snake_case`.
* License header at the top of every file (copy it from a neighboring file, add your name to the authors).
* Sphinx-style docstrings (`:param x:`, `:return:`, `:raises X:`).
* Every user-visible string goes through `pgettext("magnifier", "...")`, preceded by a `# Translators:` comment that explains the context to translators. No compound strings like `"{edge} edge"`: some languages do not inflect the word the same way depending on usage. Write one complete string per case.
* `# noqa: I001` on the first import line: automatic import sorting is not treated as a safe fix in the repository. Keep the existing order.
* `@override` (from `typing`) on methods overridden in subclasses.
* Shared types go in `utils/types.py`. Enums shown to the user inherit from `DisplayStringEnum` or `DisplayStringStrEnum` and define `_displayStringLabels`.
* Coordinates: always `Coordinates` (NamedTuple). Switching to `locationHelper.Point` was tried and reverted: `Coordinates` is simpler to compare, to unpack (`x, y = coords`) and to handle in tests.
* Vocabulary follows the user guide: *view* (full-screen, fixed...), *tracking* (what is followed), *tracking mode* (center, relative). Use these terms in code and messages, not "type", "focus mode" or "follow mode".

### 4.2 Configuration

* Never read `config.conf["magnifier"]` outside `config.py`. Add a getter/setter in `config.py`, then use it everywhere (commands, panel, classes). This is a magnifier convention, not an NVDA-wide rule: most of NVDA reads `config.conf` directly, which is fine. Here the indirection earns its place because nearly every value needs work on the way in or out: strings become enums (`Filter(...)`, `FullScreenMode(...)`), the zoom is validated against its range and its step of 50 before being written, and several settings are read on every pass of a loop that runs every 12 ms. It also keeps a single place to update when a key is renamed or removed, which has already happened twice.
* Adding a key: `configSpec.py` (`[magnifier]` section), `config.py`, `MagnifierPanel`, the user guide.
* Removing or renaming a key: add a step in `profileUpgradeSteps.py` and bump the schema version. See `upgradeConfigFrom_23_to_24`. Without a migration, existing profiles keep an invalid key.
* Any setting changed by a gesture must be persisted (`setZoomLevel`, `setFilter`...), otherwise it is lost on restart.

### 4.3 Logging

* Detailed logs go behind `if _isDebug():` (the "magnifier" category in advanced settings). The loop runs every 12 ms: an unguarded `log.debug` floods the log and costs performance.
* `log.error` / `log.warning` / `log.exception` stay unguarded: they report real anomalies.

### 4.4 Error handling

Three tools, each for a specific case:

| Situation | Tool |
| --- | --- |
| Native call whose failure can be ignored (reset, uninitialize, filter) | `@trackNativeMagnifierErrors` decorator: catches `OSError` and nothing else, logs at debug level, returns `None`. Other exceptions (code bugs) propagate. |
| Native call whose failure must be counted | Let the `OSError` propagate up to `_updateMagnifier`, which counts it and triggers recovery. This is the case for `MagSetFullscreenTransform` in `_fullscreenMagnifier()`. |
| Startup failure to present to the user | Raise `MagnifierStartError(translated message)`. Business code does not speak. The caller chooses the channel: speech for a keyboard gesture (`_speakStartError`), a message box for the settings panel (`onStartError=self._showMagnifierStartError`). |

Memory retention pitfall. Never store an exception in a local variable to try fallbacks once the `except` block has been left. If a fallback raises in turn, the original exception is chained into the traceback, its frames keep `TextInfo` objects alive, which keep NVDA dialogs alive. Real symptom: the speech dictionary dialog could not be reopened while the magnifier was running. Run the fallbacks inside the `except` block, as in `FocusManager._getPointAtStart`. Python releases the exception when leaving the block.

### 4.5 Threads and timers

* Everything touching the Magnification API or wx runs on the main thread. From another thread: `wx.CallAfter`.
* `_startTimer()` always stops the previous timer before creating a new one. Do not create a `wx.Timer` by hand.
* The spotlight pauses the main timer (`_stopTimer`) during its animation, then restarts it (`_stopSpotlight`). Any new animation must do the same, otherwise tracking and animation fight each other.
* For animated zoom changes, use `_setZoomRawValue()` (no validation against the step of 50). The `zoomLevel` setter rejects intermediate values and made the animation stutter.
* To read a mouse button state, use `winUser.getAsyncKeyState`, never `getKeyState`. `getKeyState` reads the state of the wx thread's message queue, which can lag behind: the transform moved between the physical press and the processing of the click, and clicks landed in the wrong place in apps such as Discord or Teams.

### 4.6 Where to put code

* Anything that does not depend on the full-screen API goes into `Magnifier` (base class), right away, even if only full-screen uses it today. Examples already there: Screen Curtain handling, mouse hook, clamping, panning, error counter. Future views inherit them for free.
* Anything that depends on `MagSetFullscreenTransform` and related calls stays in `FullScreenMagnifier` (`_clearStaleApiState`, `MagSetInputTransform`, native recovery).
* `commands.py` holds the logic and messages. `globalCommands.py` only declares gestures.

### 4.7 Unit tests

* Shared base: `_TestMagnifier` in `test_magnifier.py`. It patches `winBindings.magnification`, `_magnifier.fullscreenMagnifier.magnification`, `MagnifierMouseHook` and `screenCurtain`. No test may call the real DLL or install a real hook. Reuse this base for any new test file.
* Patch where the name is imported, not where it is defined (e.g. `_magnifier.fullscreenMagnifier.magnification`, not `winBindings.magnification` alone).
* Unit tests do not see the rendering. Any visual change (position, zoom, filter, touch) must be checked by hand on a real machine, ideally at several scale factors (100%, 150%, 225%).

### 4.8 Checking your work visually

The magnifier is invisible to screenshots and screen recorders. Magnification is applied by the Windows compositor, downstream of what capture APIs read. To show a bug or make a demo: film the screen with a phone or use an HDMI capture device.

---

## 5. Windows Magnification API pitfalls

These are the behaviors that cost the most time. They are all handled in the current code. Do not "simplify" these parts without rereading this section.

1. `MagInitialize()` succeeds even when another process already holds the API (Windows Magnifier running). Only `MagSetFullscreenTransform()` fails afterwards. Hence: `_initializeNativeMagnification()` performs a real first transform call as a probe, and raises if it fails. Recovery reuses the same method; a recovery that only checked `MagInitialize` reported a false success and looped forever.

2. Calling `MagInitialize`, then `MagUninitialize`, then `MagInitialize` again in the same process leaves a corrupted internal state: the next `MagSetFullscreenTransform` returns `FALSE` with error code 0 (`OSError: [WinError 0]`). Same thing after Screen Curtain has set its black matrix. Current solution: `_clearStaleApiState()` runs a dummy cycle (`MagInitialize`, reset to the neutral filter, `MagUninitialize`) before every real `MagInitialize`.
   Keeping the API initialized for the whole NVDA session and only uninitializing on exit was tried first. It was dropped because it conflicted with Screen Curtain.

3. Screen Curtain uses the same API. If the magnifier calls `MagUninitialize()` while Screen Curtain is active, the screen is exposed: this is a privacy issue. Therefore: the magnifier refuses to start while Screen Curtain is active (`_isBlockedByScreenCurtain`). During NVDA startup it silently defers and restarts once Screen Curtain is disabled. Enabling Screen Curtain stops the magnifier, disabling it restarts the magnifier.

   Note that both features share a single global color matrix: `MagSetFullscreenColorEffect` has one slot for the whole session, not one per feature. Today the handover between them goes through the neutral state, so a user with the inverted filter on sees a brief flash of normal colors when Screen Curtain switches on, and again when it switches off. Removing that flash means ordering the two transitions so the screen never returns to neutral in between: set the black matrix before the magnifier resets its own, and restore the filter before the zoom on the way back. It is worth doing, but it has to be designed together with `screenCurtain`, since the sequence starts there: it notifies the magnifier first, then applies its own matrix.

4. A clean stop requires restoring the neutral state before uninitializing: zoom 1.0 at (0, 0), identity filter, input transform disabled (`_resetMagnification`), then `MagUninitialize`. Otherwise the screen stays zoomed or tinted after stopping.

5. `MagSetInputTransform` requires UIAccess, so an installed copy of NVDA. On a portable copy or when running from source, the call fails with `WinError 5` (access denied). The code checks `systemUtils.hasUiAccess()` up front, then on `WinError 5` sets `_inputTransformSupported` to `False` and continues without it. Consequence: touch cannot be properly tested from source. You need an installed build.

6. Native errors arrive as `OSError`, thanks to the bindings' `errcheck`. COM/UIA errors coming from focus tracking arrive as `COMError` (for example `RPC_E_DISCONNECTED` in recent Notepad). The loop catches both.

---

## 6. Problems encountered and chosen solutions

Grouped by theme. Each row gives the symptom, the cause and what was done.

### Robustness and startup

| Symptom | Cause | Solution |
| --- | --- | --- |
| The magnifier freezes while the user keeps navigating | An uncaught `COMError` in focus tracking stopped the loop, which never re-armed | Protected loop, timer always re-armed, recovery after 3 errors, clean stop with a message if recovery fails |
| Infinite recovery loop while Windows Magnifier runs | See pitfall 1 in section 5 | Probe with `MagSetFullscreenTransform`, recovery capped at 3 attempts (`_MAX_RECOVERY_ATTEMPTS`) |
| Stopping and restarting the magnifier fails with `WinError 0` | See pitfall 2 | `_clearStaleApiState()` dummy cycle |
| Screen briefly exposed on restart with Screen Curtain active | See pitfall 3 | Startup blocked by Screen Curtain, transitions handled in the base class |
| NVDA announces "magnifier enabled" when it did not start, checkbox wrongly checked | Startup spoke by itself and did not report the failure | `MagnifierStartError`, `start()` with `try/finally`, `onStartError` callback |
| Speech dictionary dialog cannot be reopened | Objects retained by a chained traceback (section 4.4) | Fallbacks moved inside the `except` block |

### Tracking and positioning

| Symptom | Cause | Solution |
| --- | --- | --- |
| The magnifier did not follow the focus correctly | Wrong position sources | `FocusManager`: focus object, navigator object, system caret, review cursor |
| Caret at end of text not tracked (Notepad, Python console) | `pointAtStart` fails on a collapsed caret at the end offset | Fall back to the right edge of the previous character, local to the magnifier (`TextInfo` is not changed globally) |
| Beginning of a large object out of view | The center of the object was tracked | The top-left corner is tracked |
| The view drifts off screen | Coordinates not clamped on every path | Clamping centralized in the `currentCoordinates` setter |
| Disabling a tracking source still moves the view | Automatic fallback to another source | Freeze on the last position, two-step "disable all / restore" toggle |
| Clicks have no effect in Discord, Teams... in center mode | Transform changed between the press and the processing of the click, button state read late | No movement during a click, state read with `getAsyncKeyState` |
| Mouse tracking lag at high scale factors | wx timer late because the main thread is saturated | Dedicated mouse hook (section 3.4) |

### Interface and translation

| Symptom | Cause | Solution |
| --- | --- | --- |
| No message when a command is used while the magnifier is off | `pgettext` context argument in the wrong position | Fixed, and messages aligned with the rest of NVDA |
| Wrong translations for "left", "right"... | The same string used as an adverb and as an adjective | One complete string per case |
| Settings changed with the keyboard lost on restart | No persistence | Config setters called from the commands |
| Debug log unusable | Too many `log.debug` calls in the loop | `_isDebug()` |

---

## 7. Removed features and approaches

Some things were removed to be able to ship the magnifier in 2026.2, because their remaining problems would have delayed the release too much. They are meant to come back. Others were abandoned for good.

### 7.1 Postponed to ship 2026.2: to bring back later

| Feature | Why it was postponed | What bringing it back involves |
| --- | --- | --- |
| "Border" tracking mode | The view only moved when the tracked item reached the edge of the view. On Windows 11, with clamping the taskbar could not be reached, and without clamping it could not be used. | Add the mode back to `FullScreenMode`, handle it in `_getCoordinatesForMode()`, and solve the taskbar problem for both clamping cases. |
| "True center" option | Keeps the tracked item exactly at the center of the screen, with no clamping at the edges. It only worked properly in relative mode, and removing the clamping broke the taskbar in the other modes. | `config.isTrueCentered()` is kept as the plug-in point: today it only returns `getFullscreenMode() == RELATIVE`, and the comment above it lists the issues to solve before the option can be exposed again. Clamping is decided in `_getScreenLimits()` and `_getMagnifierParameters()`. |
| Fixed, Docked and Lens views | Not ready for 2026.2. The empty shells were kept so that view cycling and configuration are already in place. | See section 8.1. |

When bringing back an option whose config key was removed, remember that `upgradeConfigFrom_23_to_24` deleted the old `isTrueCentered` key and the `border` value from existing profiles. Add the key again in `configSpec.py` with a sensible default: old user values are gone.

### 7.2 Abandoned for good: do not redo them

Each of these was tried, sometimes shipped, then removed. The reasons still hold.

| Approach | Why it was removed |
| --- | --- |
| "Keep mouse centered" option | More nuisance than benefit: upward drift of the cursor, conflicts with panning and with clicks. Replaced by a one-shot "move mouse to the center of the view" command. |
| Blocking touch input while the magnifier runs (flag in `touchHandler`, alert sound, warning dialog) | Degraded the feature and coupled a core NVDA module to the magnifier. Replaced by `MagSetInputTransform`, the primitive Windows provides for exactly this case. Lesson: before adding a mechanism to NVDA's core, exhaust the Magnification API. |
| Repeating 8 ms timer with `timeBeginPeriod(1)` | `timeBeginPeriod` changes the clock resolution for the whole system and costs power. A repeating timer does not re-arm cleanly after an error. The smoothness problem was solved by the mouse hook. |
| Calling the Magnification API from the mouse hook | Slows down the mouse for the whole system (section 3.4). |
| API initialized once per session | Conflicted with Screen Curtain. Replaced by the dummy cycle (section 5, pitfall 2). |
| `locationHelper.Point` instead of `Coordinates` | No benefit, many tests to rewrite. |
| Tracking the center of objects | Large objects started out of view. |

---

## 8. What is left to do

### 8.1 The Fixed, Docked and Lens views

They are declared everywhere (`MagnifiedView`, `createMagnifier`, `cycleMagnifiedView`, `magnifiedView` config) but their `_doUpdate()` does nothing. Warning: the change-view gesture currently lets the user switch to an empty view.

To implement a view:

1. Inherit from `Magnifier`, define `_MAGNIFIED_VIEW`.
2. Implement `_doUpdate()`, `_getMagnifierParameters()`, `_computeMagnifiedViewCenter()`, and `_attemptRecovery()` if the view uses a native resource.
3. Call `super()._startMagnifier()` first and check `self._isActive` (Screen Curtain).
4. Move anything that could serve another view up into `Magnifier`.
5. Review the full-screen-only commands (`magnifierIsFullscreenVerify`: tracking mode, screen overview).

#### Recommended route: the Windows magnifier control (not tried yet)

The NV Access developers suggested building the Fixed, Docked and Lens views on the magnifier control of the Windows Magnification API, the same API family already used for full-screen. This route has not been tried. What follows comes from the Windows documentation and has to be checked in practice.

How it works:

* The application creates its own host window, then a child window of class `WC_MAGNIFIER` inside it (`CreateWindowEx` after `MagInitialize`).
* `MagSetWindowSource(hwndMag, rect)` chooses which screen area is shown. `MagSetWindowTransform(hwndMag, MAGTRANSFORM)` sets the zoom factor (3x3 matrix).
* `MagSetColorEffect(hwndMag, MAGCOLOREFFECT)` applies a color matrix to that window only. The matrices in `filterHandler.py` can be reused as they are.
* The `MS_SHOWMAGNIFIEDCURSOR` style draws the cursor in the magnified image. `MS_INVERTCOLORS` inverts colors.
* The control does not follow anything by itself: on every update, call `MagSetWindowSource` with the new area, then `InvalidateRect` on the control. This fits directly into `_doUpdate()` and the existing update loop.

Why it is attractive: magnification, filtering and cursor drawing are done by Windows, not in Python. It avoids the GDI capture, the manual cursor drawing and the bitmap filtering of the prototype described below.

Things to check before committing to it:

* Bindings: `winBindings/magnification.py` only exposes the full-screen functions and `MagSetInputTransform` today. `MagSetWindowSource`, `MagSetWindowTransform`, `MagSetColorEffect`, `MAGTRANSFORM` and possibly `MagSetWindowFilterList` have to be added there, with the same `errcheck`. As everywhere in NVDA, every Win32 function goes through `winBindings` (`user32`, `gdi32`...): no `ctypes.windll` declarations inside the magnifier module.
* The host window must not magnify itself. The documentation offers `MagSetWindowFilterList`, but it has restrictions on recent Windows versions. `SetWindowDisplayAffinity(WDA_EXCLUDEFROMCAPTURE)` on the host window, already validated in the prototype, is probably the way to go. It has to be added to `winBindings/user32.py` first.
* Full-screen and windowed magnification in the same process: switching views must leave the full-screen transform neutral (`_resetMagnification`) before creating the control, and the pitfalls of section 5 (initialize/uninitialize cycles, Screen Curtain) still apply.
* Docked view: the window must reserve its part of the screen so that other windows do not go under it. This is what an application desktop toolbar (`SHAppBarMessage`) does.
* Lens view: the host window follows the mouse, so it must be click-through and must be moved from the main thread, never from the mouse hook (section 3.4).

#### What was learned while prototyping the Fixed view

A first prototype of the Fixed view did not use the magnifier control. It drew the magnified image itself in an overlay window. The requirements found for that window still apply to the host window of the magnifier control.

NVDA already has a window that meets them: `HighlightWindow` in `visionEnhancementProviders/NVDAHighlighter.py`. It subclasses `windowUtils.CustomWindow` with the same styles. Use it as the model rather than inventing a new pattern. The window must be:

* a native Win32 window through `windowUtils.CustomWindow`, not a wx window: wx windows were visible to NVDA and hard to make click-through;
* invisible to NVDA and accessibility APIs: `WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW`;
* excluded from screen capture: `SetWindowDisplayAffinity(WDA_EXCLUDEFROMCAPTURE)`, otherwise the window captures itself and creates an infinite mirror effect;
* click-through: `WS_DISABLED | WS_EX_TRANSPARENT`, plus `WS_EX_NOACTIVATE` and `WS_EX_TOPMOST`.

The prototype captured the screen with GDI (`StretchBlt` in `HALFTONE` mode), applied the filters to the bitmap, and drew the cursor itself with `DrawIconEx`, because the cursor does not appear in a GDI capture. It worked, but it does in Python what the magnifier control does natively. It also declared its Win32 functions locally with `ctypes.windll`, which does not follow NVDA's `winBindings` convention.

A generic animation manager (zoom and movement interpolation shared by all views) was also prototyped. The spotlight animation in `spotlightManager.py` would be a good candidate to move into the base class that way.

### 8.2 Known touch limitations

* Hovering with a finger can move the view, and therefore the focus, erratically. Tracking logic would need to improve.
* Gesture detection is not aware of the zoom: at 10x, a swipe must be 10 times longer (the 50 px threshold is applied to already transformed coordinates). Fixing this belongs to `touchHandler`, a core NVDA module used by everyone, not to the magnifier. It should not be patched with a magnifier-specific flag or special case (see the touch entry in section 7).

---

## 9. Technical debt

Structural limitations of the current design. None of them has a quick fix.

1. Primary display only. All size computations rely on `getPrimaryDisplayOrientation()`. Multiple monitors are not handled.
2. The settings panel writes private attributes of the active instance (`_panStep`, `_fullscreenMode`). The panel and the magnifier classes are coupled through internal names.
3. The spotlight animation cannot be cancelled. It chains `wx.CallLater` calls without keeping references to them. Only the mouse idle timer can be stopped.
4. Polling cost. Every 12 ms, the `FocusManager` queries the system caret, the review cursor and the navigator object, which triggers COM/UIA calls. This is the main lead if performance problems appear in slow applications. NVDA already notifies these changes through the extension points of `vision.visionHandler` (`post_focusChange`, `post_caretMove`, `post_browseModeMove`, `post_reviewMove`, `post_mouseMove`), which is how `NVDAHighlighter` follows the focus. Moving the `FocusManager` onto them would follow the way NVDA works, but it is a large change to the tracking priorities described in section 3.5.

---

## 10. What can be done right now

Small, self-contained fixes found while rereading the code for this document. None of them is applied yet.

1. Screen resolution or orientation changes are ignored. `Magnifier._onDisplayChanged` writes to `self.orientationState`, while all the code reads `self._displayOrientation`. In addition, `FullScreenMagnifier._displaySize` is computed only once. Assigning `self._displayOrientation = orientationState` is probably enough; then test by changing the resolution while the magnifier is active.
2. The `displayChanged` handler is registered in `__init__` but unregistered in `_stopMagnifier`. After stopping and restarting the same instance, it is no longer called. Move the registration to `_startMagnifier`.
3. `commands.toggleFilter` applies the filter twice: the `FullScreenMagnifier.filterType` setter already calls `_applyFilter()` when the magnifier is active. Remove the explicit call in `toggleFilter`. The second call sets the same colour matrix again, so nothing changes on screen, but it is one native call too many on every filter change.
4. Fix the docstring of `config.isTrueCentered()`. Keep the function: it is where the postponed "true center" option will plug back in (section 7.1). But its docstring still says it reads the setting from config, while it only returns `getFullscreenMode() == RELATIVE` today. Say so in the docstring.
5. Clean up what does not match the current code: `FullScreenMagnifier.event_gainFocus` is never called (the magnifier is not an event plugin); the `toggleFullscreenMode` docstring still lists "border" among the current modes. `Magnifier._MARGIN_BORDER` is unused today but belongs to the postponed border mode: keep it, or remove it and add it back with the mode.
6. Fix the error message of `createMagnifier`: it prints the `MagnifiedView` class instead of the received value.
7. Expose public properties for the pan step and the tracking mode, and use them from the settings panel (technical debt item 2).

---

## 11. Where the discussion happened

The reasoning behind the decisions above is written out in this document, so it can be read without leaving the repository. Two cases are the exception: options that were shipped and then taken out, and work that was attempted and never landed as such. For those, the argument lives in the pull request discussion, and the numbers below are the fastest way back to it.

Shipped, then removed or replaced:

| Decision | Introduced by | Removed or replaced by |
| --- | --- | --- |
| "True center" option (postponed, section 7.1) | #19593 | #20587 |
| "Border" tracking mode (postponed, section 7.1) | #19228 | #20587 |
| Blocking touch input while the magnifier runs | #20357 | #20612 |
| "Keep mouse centered" option | #19228 | #20268, replaced by the command added in #20238 |
| Magnification API initialized once per session | #20069 | #20342 |
| Tracking the center of objects rather than their top-left corner | #19228 | #20313 |
| Reading mouse button state with `getKeyState` | #19228 | #20052 |

Attempts at the Fixed, Docked and Lens views:

| Attempt | Outcome |
| --- | --- |
| #19473, then #19810: full implementation of the new views in one go | Too large to review as a whole, so they were not merged as such |
| #19882: types and naming needed by the new views | Split out of the above and merged on its own |
| #19915: view cycling and the empty shells | Split out of the above and merged on its own, which is why the shells exist today |
