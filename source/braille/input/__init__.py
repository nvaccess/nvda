# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2026 NV Access Limited, Rui Batista, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Framework for handling braille input from the user.
All braille input is represented by a :class:`braille.input.gesture.BrailleInputGesture`.
Normally, all that is required is to create and execute a :class:`braille.input.gesture.BrailleInputGesture`,
as there are built-in gesture bindings for braille input.
"""

from __future__ import annotations

import inputCore
from logHandler import log

from . import gesture as _gesture
from . import inputHandler as _inputHandler

inputCore.registerGestureSource("bk", _gesture.BrailleInputGesture)

handler: _inputHandler.BrailleInputHandler | None = None
"""The singleton BrailleInputHandler instance."""


def initialize():
	global handler
	handler = _inputHandler.BrailleInputHandler()
	log.info("Braille input initialized")


def terminate():
	global handler
	handler = None
