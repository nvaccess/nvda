# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2026 NV Access Limited, Rui Batista, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Framework for handling braille input from the user.
All braille input is represented by a {BrailleInputGesture}.
Normally, all that is required is to create and execute a L{BrailleInputGesture},
as there are built-in gesture bindings for braille input.
"""

from typing import Optional

import inputCore
from logHandler import log

from . import gesture as _gesture
from . import inputHandler as _inputHandler

inputCore.registerGestureSource("bk", _gesture.BrailleInputGesture)

#: The singleton BrailleInputHandler instance.
handler: Optional[_inputHandler.BrailleInputHandler] = None


def initialize():
	global handler
	handler = _inputHandler.BrailleInputHandler()
	log.info("Braille input initialized")


def terminate():
	global handler
	handler = None
