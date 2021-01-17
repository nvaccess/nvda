# appModules/systemsettings.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 10 Settings app (aka Immersive Control Panel)."""

import appModuleHandler
from NVDAObjects.UIA import UIA
from NVDAObjects.behaviors import ProgressBar


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, UIA):
			# #10411: In build 17035, Settings/System/Sound has been added, but has an anoying volume meter.
			if obj.UIAElement.cachedClassName == "ProgressBar" and isinstance(obj.next, UIA):
				# Due to Storage Sense UI redesign in build 18277,
				# the progress bar's sibling might not be a UIA object at all.
				try:
					if (
						obj.next.UIAElement.cachedAutomationID.startswith(
							"SystemSettings_Audio_Output_VolumeValue_"
						)
						or obj.simplePrevious.UIAElement.cachedAutomationID.startswith(
							"SystemSettings_Audio_Input_VolumeValue_"
						)
					):
						try:
							clsList.remove(ProgressBar)
						except ValueError:
							pass
				except AttributeError:
					pass
