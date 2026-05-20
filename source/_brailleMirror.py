# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Pneuma Solutions
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""BrailleMirror and DirectBrailleWindow public APIs, and their supporting infrastructure.

Kept in a separate module to avoid further growth of braille.py (see #12772).
Imported into braille at the bottom of that module so callers continue to access
everything as ``braille.BrailleMirror`` etc.
"""

from __future__ import annotations

import inputCore
import winUser
import wx

# Imported at module level for runtime isinstance checks and attribute access.
# All references to braille.X names are inside function/method bodies so the
# circular import (braille -> _brailleMirror -> braille) is safe.
import braille


class BrailleMirror:
	"""Abstract base class for a braille mirror.

	A mirror intercepts every braille display update and can optionally influence the negotiated display width.
	Both the physical display and all registered mirrors receive the same cells simultaneously; the mirror does **not** suppress the local display.
	Register an instance with :func:`registerMirror` and remove it with :func:`unregisterMirror`.  To inject a gesture back into NVDA (e.g. a routing key received over a remote channel) use :func:`injectGesture`.
	"""

	def display(self, cells: list[int]) -> None:
		"""Called with the full cell array on every display update.

		:param cells: The braille cells written to the display.
		"""

	def numCells(self) -> int:
		"""Return the number of cells this mirror can show.

		Return 0 (the default) to have no effect on the negotiated display
		width.  A positive value caps the display width used by
		:data:`braille.filter_displayDimensions` to the smallest value across all registered mirrors and the physical display.
		"""
		return 0


_registeredMirrors: list[BrailleMirror] = []


def _mirrorPreWriteCells(cells: list[int], **kwargs) -> None:
	for mirror in _registeredMirrors:
		mirror.display(cells)


def _mirrorFilterDisplayDimensions(value: braille.DisplayDimensions) -> braille.DisplayDimensions:
	sizes = [m.numCells() for m in _registeredMirrors if m.numCells() > 0]
	if not sizes:
		return value
	cap = min(sizes)
	if cap >= value.numCols:
		return value
	return value._replace(numCols=cap)


def registerMirror(mirror: BrailleMirror) -> None:
	"""Register *mirror* to receive braille display updates.

	:meth:`BrailleMirror.display` will be called on the main thread for every subsequent :meth:`braille.BrailleHandler._writeCells` call.  If *mirror* returns a positive value from :meth:`BrailleMirror.numCells`, it will also participate in display-width negotiation via :data:`braille.filter_displayDimensions`.
	"""
	if not _registeredMirrors:
		braille.pre_writeCells.register(_mirrorPreWriteCells)
		braille.filter_displayDimensions.register(_mirrorFilterDisplayDimensions)
	_registeredMirrors.append(mirror)
	if braille.handler:
		braille.handler._refreshEnabled(block=True)


def unregisterMirror(mirror: BrailleMirror) -> None:
	"""Remove a previously registered mirror.

	Safe to call even if *mirror* is not currently registered.
	"""
	try:
		_registeredMirrors.remove(mirror)
	except ValueError:
		return
	if not _registeredMirrors:
		braille.pre_writeCells.unregister(_mirrorPreWriteCells)
		braille.filter_displayDimensions.unregister(_mirrorFilterDisplayDimensions)
	if braille.handler:
		braille.handler._refreshEnabled(block=True)


def injectGesture(gesture: braille.BrailleDisplayGesture) -> None:
	"""Inject *gesture* into NVDA's input pipeline.

	This is a thin wrapper around :func:`inputCore.manager.executeGesture` that silently swallows :class:`inputCore.NoInputGestureAction` so callers do not need to handle the common case where no script is bound.

	Thread safety: must be called on the main thread, or scheduled via ``wx.CallAfter`` from a background thread.
	"""
	try:
		inputCore.manager.executeGesture(gesture)
	except inputCore.NoInputGestureAction:
		pass


class DirectBrailleWindow:
	"""Take over braille output and input while a specific window has focus.

	When the window identified by *hwnd* is the foreground window, NVDA's own braille rendering is suspended.  The application drives what appears on the physical display by calling :meth:`display`, and all braille gestures are forwarded to :meth:`onGesture` instead of being processed by NVDA.
	When the window loses focus, normal NVDA rendering resumes automatically.

	:param hwnd: The HWND of the window that triggers direct braille mode.
	:param numCells: Advertised display width; 0 means use whatever NVDA provides.  A positive value caps the negotiated display width via :data:`braille.filter_displayDimensions`.
	"""

	def __init__(self, hwnd: int, numCells: int = 0) -> None:
		self._hwnd = hwnd
		self._numCells = numCells
		self._active = False

	def _isForeground(self) -> bool:
		"""Return True if our registered window is currently in the foreground."""
		fg = winUser.getForegroundWindow()
		return fg == self._hwnd or winUser.isDescendantWindow(self._hwnd, fg)

	def display(self, cells: list[int]) -> None:
		"""Push *cells* to the physical braille display.

		Has no effect if the registered window is not currently foreground or if no braille display is connected.

		Thread safety: safe to call from any thread; the actual write is dispatched to the main thread via ``wx.CallAfter``.
		"""
		if braille.handler and self._isForeground():
			wx.CallAfter(braille.handler._writeCells, cells)

	def onGesture(self, gesture: braille.BrailleDisplayGesture) -> None:
		"""Called when a braille gesture arrives while this window is active.

		The default implementation does nothing, so gestures are suppressed. Subclass and override to handle them.

		:param gesture: The braille gesture that was intercepted.
		"""

	def _handleDecideEnabled(self) -> bool:
		return not self._isForeground()

	def _handleDecideExecuteGesture(self, gesture: inputCore.InputGesture) -> bool:
		if not self._isForeground():
			return True
		if isinstance(gesture, braille.BrailleDisplayGesture):
			self.onGesture(gesture)
			return False
		return True

	def _handleFilterDisplayDimensions(self, value: braille.DisplayDimensions) -> braille.DisplayDimensions:
		if self._numCells <= 0 or not self._isForeground():
			return value
		if self._numCells >= value.numCols:
			return value
		return value._replace(numCols=self._numCells)

	def activate(self) -> None:
		"""Start intercepting braille output and input for the registered window.

		Safe to call even if already active (subsequent calls are no-ops).
		"""
		if self._active:
			return
		self._active = True
		braille.decide_enabled.register(self._handleDecideEnabled)
		inputCore.decide_executeGesture.register(self._handleDecideExecuteGesture)
		if self._numCells > 0:
			braille.filter_displayDimensions.register(self._handleFilterDisplayDimensions)
		if braille.handler:
			braille.handler._refreshEnabled(block=True)

	def deactivate(self) -> None:
		"""Stop intercepting braille, restoring NVDA's normal rendering.

		Safe to call even if not currently active.
		"""
		if not self._active:
			return
		self._active = False
		braille.decide_enabled.unregister(self._handleDecideEnabled)
		inputCore.decide_executeGesture.unregister(self._handleDecideExecuteGesture)
		if self._numCells > 0:
			braille.filter_displayDimensions.unregister(self._handleFilterDisplayDimensions)
		if braille.handler:
			braille.handler._refreshEnabled(block=True)
