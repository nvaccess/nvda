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
import speech
import braille
import config
from logHandler import log

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

class NvdaSettingsCategoryPanel(IAccessible):
	# The configuration profile that has been previously edited.
	# This ought to be a class property.
	oldProfile = None

	def event_nameChange(self):
		if self in api.getFocusAncestors():
			speech.speakObjectProperties(self, name=True, reason=controlTypes.REASON_CHANGE)
		braille.handler.handleUpdate(self)
		self.handlePossibleProfileSwitch()

	@classmethod
	def handlePossibleProfileSwitch(cls):
		from gui.settingsDialogs import NvdaSettingsDialogActiveConfigProfile as newProfile
		if (cls.oldProfile and newProfile and newProfile != cls.oldProfile):
			# Translators: A message announcing what configuration profile is currently being edited.
			speech.speakMessage(_("Editing profile {profile}").format(profile=newProfile))
		cls.oldProfile = newProfile

class AppModule(appModuleHandler.AppModule):

	def event_appModule_loseFocus(self):
		NvdaSettingsCategoryPanel.oldProfile = None

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

	def isNvdaSettingsCategoryPanel(self, obj):
		controlId = obj.windowControlID
		from gui.settingsDialogs import NvdaSettingsCategoryPanelId
		if not isinstance(obj, IAccessible):
			return False
		if controlId == NvdaSettingsCategoryPanelId:
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
		else:
			NvdaSettingsCategoryPanel.handlePossibleProfileSwitch()
		nextHandler()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "#32770" and obj.role == controlTypes.ROLE_DIALOG:
			clsList.insert(0, NvdaDialog)
		if self.isNvdaSettingsCategoryPanel(obj):
			clsList.insert(0, NvdaSettingsCategoryPanel)
