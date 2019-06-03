# NVDAObjects/window/winConsole.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

import warnings
from ..IAccessible.winConsoleLegacy import WinConsoleLegacy as WinConsole

warnings.warn("NVDAObjects.window.winConsole is deprecated. Use NVDAObjects.IAccessible.WinConsoleLegacy or NVDAObjects.UIA.winConsoleUIA instead",
	DeprecationWarning, stacklevel=3)
