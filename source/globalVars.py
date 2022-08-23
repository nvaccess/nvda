# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Łukasz Golonka, Leonard de Ruijter, Babbage B.V.,
# Aleksey Sadovoy, Peter Vágner
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""global variables module

This module is scheduled for deprecation.
Do not continue to add variables to this module.

To retain backwards compatibility, variables should not be removed
from globalVars.
Instead, encapsulate variables in setters and getters in
other modules.

When NVDA core is no longer dependent on globalVars,
a deprecation warning should be added to this module which
warns developers when importing anything from this module.

Once a warning is in place, after some time it may become appropriate to delete this module.
"""

import argparse
import os
import typing

if typing.TYPE_CHECKING:
	import NVDAObjects  # noqa: F401 used for type checking only


class DefaultAppArgs(argparse.Namespace):
	quit: bool = False
	check_running: bool = False
	logFileName: typing.Optional[os.PathLike] = ""
	logLevel: int = 0
	configPath: typing.Optional[os.PathLike] = None
	language: str = "en"
	minimal: bool = False
	secure: bool = False
	disableAddons: bool = False
	debugLogging: bool = False
	noLogging: bool = False
	changeScreenReaderFlag: bool = True
	install: bool = False
	installSilent: bool = False
	createPortable: bool = False
	createPortableSilent: bool = False
	portablePath: typing.Optional[os.PathLike] = None
	launcher: bool = False
	enableStartOnLogon: typing.Optional[bool] = None
	copyPortableConfig: bool = False
	easeOfAccess: bool = False


# Encapsulated by api module,
# refer to #14037 for removal strategy.
desktopObject: typing.Optional['NVDAObjects.NVDAObject'] = None
"""Deprecated, use `setDesktopObject|getDesktopObject` from `api` instead"""
foregroundObject: typing.Optional['NVDAObjects.NVDAObject'] = None
"""Deprecated, use `setForegroundObject|getForegroundObject` from `api` instead"""
focusObject: typing.Optional['NVDAObjects.NVDAObject'] = None
"""Deprecated, use `setFocusObject|getFocusObject` from `api` instead"""
focusAncestors: typing.List['NVDAObjects.NVDAObject'] = []
"""Deprecated, use `getFocusAncestors` from `api` instead"""
focusDifferenceLevel=None
"""Deprecated, use `getFocusDifferenceLevel` from `api` instead"""
mouseObject: typing.Optional['NVDAObjects.NVDAObject'] = None
"""Deprecated, use ``setMouseObject|getMouseObject`` from `api` instead"""
navigatorObject: typing.Optional['NVDAObjects.NVDAObject'] = None
"""Deprecated, use ``setNavigatorObject|getNavigatorObject`` from `api` instead"""
reviewPosition=None
"""Deprecated, use ``getReviewPosition|setReviewPosition`` from `api` instead"""
reviewPositionObj=None
"""Deprecated, use ``api.getReviewPosition().obj`` instead"""

# unused, should eventually get removed.
mouseOldX = None
"""Deprecated, this is unused and not set by NVDA core"""
mouseOldY = None
"""Deprecated, this is unused and not set by NVDA core"""
lastProgressValue = 0
"""Deprecated, this is unused and not set by NVDA core"""

# TODO: encapsulate in NVDAState
startTime: float = 0.0
"""Deprecated, use ``NVDAState.getStartTime`` instead"""
appArgs = DefaultAppArgs()
unknownAppArgs: typing.List[str] = []
exitCode=0
"""
Deprecated, this should not be used by add-on authors.
NVDA core should use `NVDAState._getExitCode|_setExitCode` instead.
"""
appPid: int = 0
"""The process ID of NVDA itself.
"""

# TODO: encapsulate in synthDriverHandler
settingsRing = None

# TODO: encapsulate in speechDict
speechDictionaryProcessing: bool = True
