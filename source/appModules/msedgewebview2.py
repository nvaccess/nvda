# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Support for apps employing Edge WebView2 runtime interface."""

from typing import Any
import appModuleHandler


def getAppNameFromHost(processId: int) -> str:
	# #16705: some apps have launcher executables which launch msedgewebview2.exe to display the interface.
	# In this case, the parent process will usually be the launcher.
	proc = appModuleHandler.getWmiProcessInfo(processId)
	# Unlikely but react to undefined parent process ID.
	if not (parent := proc.parentProcessId):
		raise LookupError
	return appModuleHandler.getAppNameFromProcessID(parent)


def __getattr__(attrName: str) -> Any:
	if attrName == "AppModule":
		return appModuleHandler.AppModule
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
