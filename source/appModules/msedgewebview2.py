# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Support for apps employing Edge WebView2 runtime interface."""

from typing import Any  # noqa: I001
import appModuleHandler


def getAppNameFromHost(processId: int) -> str:
	# #16705: some apps have launcher executables which launch msedgewebview2.exe to display the interface.
	# In this case, the parent process will usually be the launcher.
	try:
		proc = appModuleHandler.getWmiProcessInfo(processId)
		parent = getattr(proc, "ParentProcessId", None) or getattr(proc, "parentProcessId", None)
		if not parent:
			raise LookupError
		return appModuleHandler.getAppNameFromProcessID(parent)
	except Exception:
		raise LookupError


def __getattr__(attrName: str) -> Any:
	if attrName == "AppModule":
		return appModuleHandler.AppModule
	raise AttributeError(f"module {__name__!r} has no attribute {attrName!r}")
