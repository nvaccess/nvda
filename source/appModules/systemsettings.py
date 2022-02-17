# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019-2022 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Settings app on Windows 10 and later (aka Immersive Control Panel)."""

import appModuleHandler
from NVDAObjects.UIA import UIA, ProgressBar


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, UIA):
			# #10411: In build 17035, Settings/System/Sound has been added, but has an anoying volume meter.
			if obj.UIAElement.cachedClassName == "ProgressBar" and isinstance(obj.next, UIA):
				# Due to Storage Sense UI redesign in build 18277,
				# the progress bar's sibling might not be a UIA object at all.
				try:
					if (
						obj.next.UIAAutomationId.startswith(
							"SystemSettings_Audio_Output_VolumeValue_"
						)
						or obj.simplePrevious.UIAAutomationId.startswith(
							"SystemSettings_Audio_Input_VolumeValue_"
						)
					):
						try:
							clsList.remove(ProgressBar)
						except ValueError:
							pass
				except AttributeError:
					pass
