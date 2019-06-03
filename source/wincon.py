# NVDAObjects/wincon.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

import warnings
from winconLegacy import *

warnings.warn("wincon is deprecated. Use winconLegacy instead, and consider switching to the UIA console implementation.",
	DeprecationWarning, stacklevel=3)
