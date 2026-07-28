# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

from typing import TYPE_CHECKING

from logHandler import log

from .config import getMagnifiedView, getEnabled, setEnabled
from .utils.types import MagnifiedView
from .utils.errorHandling import MagnifierStartError

if TYPE_CHECKING:
	from .magnifier import Magnifier

_magnifier: "Magnifier | None" = None


def createMagnifier(magnifiedView: MagnifiedView) -> "Magnifier":
	"""
	Create a magnifier instance based on the specified view.

	:param magnifiedView: The magnifier view to create
	:return: The created magnifier instance
	:raises ValueError: If the magnifier view is not supported
	"""

	match magnifiedView:
		case MagnifiedView.FULLSCREEN:
			from .fullscreenMagnifier import FullScreenMagnifier

			return FullScreenMagnifier()

		case MagnifiedView.FIXED:
			from .fixedMagnifier import FixedMagnifier

			return FixedMagnifier()

		case MagnifiedView.DOCKED:
			from .dockedMagnifier import DockedMagnifier

			return DockedMagnifier()

		case MagnifiedView.LENS:
			from .lensMagnifier import LensMagnifier

			return LensMagnifier()

		case _:
			raise ValueError(f"Unsupported magnifier view: {MagnifiedView}")


def _setMagnifiedView(magnifiedView: MagnifiedView) -> None:
	"""
	Set the magnifier view, stopping the current one if active and creating a new instance.

	:param magnifiedView: The magnifier view to set
	"""
	global _magnifier

	# Stop current magnifier if active
	if _magnifier and _magnifier._isActive:
		_magnifier._stopMagnifier()

	# Create and set new magnifier instance
	_magnifier = createMagnifier(magnifiedView)


def initialize() -> None:
	"""
	Initialize the magnifier module with the default magnifier view from config.
	"""
	log.debug("Initializing magnifier")
	magnifiedView = getMagnifiedView()
	_setMagnifiedView(magnifiedView)
	if getEnabled():
		try:
			start()
		except MagnifierStartError:
			# The magnifier was enabled in config but cannot start now (e.g. another magnifier
			# application is already running). start() has updated config to reflect the real
			# state; there is no GUI at startup, so just log it.
			log.warning("Magnifier is enabled in config but failed to start.", exc_info=True)


def terminate() -> None:
	"""
	Terminate the magnifier module.
	Called when NVDA shuts down.
	"""
	global _magnifier

	log.debug("Terminating magnifier")
	stop(persist=False)
	_magnifier = None


def start() -> None:
	"""Start the magnifier.

	Config is always updated to reflect the real active state, whether or not the start succeeds.

	:raises MagnifierStartError: If the magnifier cannot be started (e.g. another magnifier
		application is already running, or screen curtain is active). The exception carries a
		user-facing message so the caller can present it (spoken or in a message box).
	"""
	if _magnifier is None:
		log.error("Attempted to start magnifier, but it is not initialized.")
		return
	try:
		_magnifier._startMagnifier()
	finally:
		setEnabled(isActive())


def stop(persist: bool = True) -> None:
	"""Stop the magnifier if it is active.

	:param persist: Whether to persist the magnifier state
	"""
	if isActive():
		_magnifier._stopMagnifier()
		if persist:
			setEnabled(isActive())
	else:
		log.debug("Attempted to stop magnifier, but it is not active.")


def isActive() -> bool:
	"""
	Check if magnifier is currently active.

	:return: True if magnifier is active, False otherwise
	"""
	global _magnifier
	return _magnifier is not None and _magnifier._isActive


def changeMagnifiedView(magnifiedView: MagnifiedView) -> None:
	"""
	Change the magnifier view at runtime.
	Stops the current magnifier and starts a new one of the specified view.

	:param magnifiedView: The new magnifier view to use
	:raises RuntimeError: If no magnifier is currently active
	"""
	global _magnifier
	if not _magnifier or not _magnifier._isActive:
		raise RuntimeError("Cannot change magnifier view: magnifier is not active")

	_setMagnifiedView(magnifiedView)
	_magnifier._startMagnifier()


def getMagnifier() -> "Magnifier | None":
	"""
	Get the current magnifier instance.

	:return: The current magnifier instance, or None if not initialized
	"""
	global _magnifier
	return _magnifier
