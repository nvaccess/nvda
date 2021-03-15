# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2020 NV Access Limited, Joseph Lee

"""App module host for Windows 8.x and 10 apps hosted by wwahost.exe.
In Windows 8, apps written in Javascript are executed inside WWAHost, including some WinRT apps.
In Windows 10, progressive web apps (PWA) and friends are hosted inside this process.
App modules wishing to support apps hosted inside this process must subclass the AppModule class.
"""

import ctypes
import appModuleHandler
import winKernel


def getAppNameFromHost(processId):
	# Some apps that come with Windows 8 and 8.1 are hosted by wwahost.exe.
	# App modules for these are named after the hosted app name.
	processHandle = winKernel.openProcess(
		winKernel.SYNCHRONIZE | winKernel.PROCESS_QUERY_INFORMATION, False, processId
	)
	length = ctypes.c_uint()
	winKernel.kernel32.GetApplicationUserModelId(processHandle, ctypes.byref(length), None)
	appModel = ctypes.create_unicode_buffer(length.value)
	winKernel.kernel32.GetApplicationUserModelId(processHandle, ctypes.byref(length), appModel)
	winKernel.closeHandle(processHandle)
	# Sometimes app model might be empty, so raise errors and fall back to wwahost.
	if not appModel.value:
		raise LookupError
	# App model is shown as familyName!appName,
	# and importing files with the exclamation point in the middle of the name isn't supported.
	# Therefore return only the app name portion.
	# Convert this into lowercase to make the file name consistent with other NVDA app modules.
	return appModel.value.split("!")[-1].lower()

class AppModule(appModuleHandler.AppModule):

	# WWAHost app content is treated as part of an app, not a browse mode document.
	disableBrowseModeByDefault = True
