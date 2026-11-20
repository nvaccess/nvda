# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Screen curtain implementation based on the windows magnification API."""

from logHandler import log
from winBindings.magnification import MAGNIFICATION_AVAILABLE, MAGNIFICATION_LOAD_ERROR

from ._screenCurtain import ScreenCurtain

__all__ = (
	"initialize",
	"screenCurtain",
	"terminate",
)


screenCurtain: ScreenCurtain | None = None
"""Global Screen Curtain controller."""


def initialize():
	"""Initialize theScreen Curtain."""
	global screenCurtain
	if not MAGNIFICATION_AVAILABLE:
		log.warning(
			"Screen Curtain unavailable because the Windows Magnification API is unavailable.",
			exc_info=MAGNIFICATION_LOAD_ERROR,
		)
		return
	if screenCurtain is None:
		screenCurtain = ScreenCurtain()


def terminate():
	"""Terminate the Screen Curtain."""
	global screenCurtain
	if screenCurtain is not None:
		screenCurtain.disable(persist=False)
		screenCurtain = None
