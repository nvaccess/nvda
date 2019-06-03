# NVDAObjects/winConsoleHandler.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

import warnings
from winConsoleHandlerLegacy import *

warnings.warn("winConsoleHandler is deprecated. Use winConsoleHandlerLegacy instead, and consider switching to the UIA console implementation.",
	DeprecationWarning, stacklevel=3)
