#appModules/nvda.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import api
import controlTypes
import versionInfo
from NVDAObjects.IAccessible import IAccessible
import gui
import config

nvdaMenuIaIdentity = None

class NvdaDialog(IAccessible):
	"""Fix to ensure NVDA message dialogs get reported when they pop up.
	"""

	def _get_presentationType(self):
		presType = super(NvdaDialog, self).presentationType
		# Sometimes, NVDA message dialogs briefly report the invisible state
		# after they're focused.
		# This causes them to be treated as unavailable and they are thus not reported.
		# If this dialog is in the foreground, treat it as content.
		if presType == self.presType_unavailable and self == api.getForegroundObject():
			return self.presType_content
		return presType

class AppModule(appModuleHandler.AppModule):

	def isNvdaMenu(self, obj):
		global nvdaMenuIaIdentity
		if not isinstance(obj, IAccessible):
			return False
		if nvdaMenuIaIdentity and obj.IAccessibleIdentity == nvdaMenuIaIdentity:
			return True
		if nvdaMenuIaIdentity is not True:
			return False
		# nvdaMenuIaIdentity is True, so the next menu we encounter is the NVDA menu.
		if obj.role == controlTypes.ROLE_POPUPMENU:
			nvdaMenuIaIdentity = obj.IAccessibleIdentity
			return True
		return False

	def event_NVDAObject_init(self, obj):
		# It seems that context menus always get the name "context" and this cannot be overridden.
		# Fudge the name of the NVDA system tray menu to make it more friendly.
		if self.isNvdaMenu(obj):
			obj.name=versionInfo.name

	def event_gainFocus(self, obj, nextHandler):
		if obj.role == controlTypes.ROLE_UNKNOWN and controlTypes.STATE_INVISIBLE in obj.states:
			return
		nextHandler()

	# Silence invisible unknowns for stateChange as well.
	event_stateChange = event_gainFocus

	def event_foreground         (self, obj, nextHandler):
		if not gui.shouldConfigProfileTriggersBeSuspended():
			config.conf.resumeProfileTriggers()
		nextHandler()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "#32770" and obj.role == controlTypes.ROLE_DIALOG:
			clsList.insert(0, NvdaDialog)
