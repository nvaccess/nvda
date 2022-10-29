# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" This module provides the WindowsLib Robot Framework Library which allows interacting with Windows GUI
features.
"""
# imported methods start with underscore (_) so they don't get imported into robot files as keywords

from robot.libraries.BuiltIn import BuiltIn as _BuiltInLib

from SystemTestSpy.windows import (
	GetForegroundWindowTitle as _getForegroundWindowTitle,
	GetForegroundHwnd as _getForegroundHwnd,
	Window as _Window,
)

builtIn: _BuiltInLib = _BuiltInLib()

# This library doesn't rely on state, so it is not a class.
# However, if converting to a class note that in Robot libraries, the class name must match the name
# of the module.
# Use caps for both.


def isWindowInForeground(window: _Window) -> bool:
	return window.hwndVal == _getForegroundHwnd()


def logForegroundWindowTitle():
	"""Debugging helper, log the current foreground window title to the robot framework log.
	See log.html.
	"""
	windowTitle = _getForegroundWindowTitle()
	builtIn.log(f"Foreground window title: {windowTitle}")
