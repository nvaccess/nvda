# App module for Windows 10 Settings app
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

""" AppModule for the Windows System Settings app.
"""

import appModuleHandler
import controlTypes
from NVDAObjects.UIA import UIA
from NVDAObjects.behaviors import ProgressBar


class VolumeMeter(UIA):
	role = controlTypes.ROLE_METER


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, UIA):
			if obj.UIAElement.CurrentAutomationId == "SystemSettings_Audio_Output_VolumeValue_ProgressBar":
				# Volume meters have a role of progressBar
				# which causes their value to be reported via beeps and speech inappropriately.
				# Therefore force the role to something other than progressBar.
				clsList.remove(ProgressBar)
				clsList.insert(0, VolumeMeter)
