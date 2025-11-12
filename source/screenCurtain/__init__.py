# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Screen curtain implementation based on the windows magnification API."""

from ._screenCurtain import ScreenCurtain

__all__ = (
	"screenCurtain",
	"initialize",
	"terminate",
)


screenCurtain: ScreenCurtain | None = None
"""Global Screen Curtain controller."""


def initialize():
	"""Initialize theScreen Curtain."""
	global screenCurtain
	if screenCurtain is None:
		screenCurtain = ScreenCurtain()


def terminate():
	"""Terminate the Screen Curtain."""
	global screenCurtain
	if screenCurtain is not None:
		screenCurtain.disable(persist=False)
		screenCurtain = None
