# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Łukasz Golonka, Leonard de Ruijter, Babbage B.V.,
# Aleksey Sadovoy, Peter Vágner
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import argparse
import os
import sys
import typing

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


startTime=0
appArgs = DefaultAppArgs()
unknownAppArgs: typing.List[str] = []
settingsRing = None
speechDictionaryProcessing=True
exitCode=0

appPid: int = 0
"""The process ID of NVDA itself.
"""

_allowDeprecatedAPI: bool = True
"""
Used for marking code as deprecated.
This should never be False in released code.

Making this False may be useful for testing if code is compliant without using deprecated APIs.
Note that deprecated code may be imported at runtime,
and as such, this value cannot be changed at runtime to test compliance.
"""

runningAsSource: bool = getattr(sys, 'frozen', None) is None
"""
True if NVDA is running as a source copy.
When running as an installed copy, py2exe sets sys.frozen to 'windows_exe'.
"""
