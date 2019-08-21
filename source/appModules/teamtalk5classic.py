# appModules/teamtalk5classic.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2019 NV Access Limited, Doug Lee, Tyler Spivey, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import api
import appModuleHandler
import controlTypes
import scriptHandler
import speech
import ui

from NVDAObjects.behaviors import ProgressBar
from NVDAObjects.IAccessible import IAccessible

# Constants
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_CONNECTED = _("Connected")
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_PTT = _("Push To Talk")
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_VOX = _("Voice Activation")
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_VIDEO = _("Video")
# Translators: Status text in the TeamTalk voice conferencing client.
# Note: this string is slightly different from the actual toolbar text
# to avoid a translatable string conflict.
LBL_DESKTOP = _("Share desktop")
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_STREAM = _("Stream To Channel")
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_MUTE = _("Mute All")
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_RECORD = _("Store Audio")
# Translators: Status text in the TeamTalk voice conferencing client.
LBL_MSG = _("Show Channel Messages")

#: The names, in order, of the toolbar items.
#: The count must match exactly or this module will not function.
#: The name "sep" is a placeholder for separators in the toolbar.
#: These are name sets per client version.
#: Stored in reverse so current clients find the right list faster.
_msgNames = {
	"4.5": [
		LBL_CONNECTED,
		"sep",
		LBL_PTT,
		LBL_VOX,
		LBL_VIDEO,
		LBL_DESKTOP,
		LBL_STREAM,
		"sep",
		LBL_MUTE,
		LBL_RECORD,
		"sep",
		LBL_MSG,
	],
	"4.3": [
		LBL_CONNECTED,
		"sep",
		LBL_PTT,
		LBL_VOX,
		LBL_VIDEO,
		LBL_DESKTOP,
		LBL_MUTE,
		LBL_RECORD,
		"sep",
		LBL_MSG,
	],
	"4.2": [
		LBL_CONNECTED,
		"sep",
		LBL_PTT,
		LBL_VOX,
		"sep",
		LBL_MUTE,
		LBL_RECORD,
		"sep",
		LBL_MSG,
	],
	"4.1": [
		LBL_CONNECTED,
		"sep",
		LBL_PTT,
		LBL_VOX,
		"sep",
		LBL_MUTE,
		"sep",
		LBL_MSG,
	],
}

# window control IDs
ID_CHATOUT = 1204
ID_CHATIN = 1206
ID_BANNEDLIST = 1326
ID_UNBANNEDLIST = 1327
ID_TOOLBAR = 59392
ID_VU = 1004


class TTToolBarInfo(object):
	"""Info about one TeamTalk toolbar and its items.
	"""

	def __init__(self, NVDAObj=None):
		if not NVDAObj:
			# Use the IAccessible for the active TeamTalk instance's toolbar.
			NVDAObj = self.getToolBar()
			if not NVDAObj:
				# Translators: Reported when status information is unavailable
				# in the TeamTalk voice conferencing client.
				ui.message(_("Status unavailable"))
				return
		self.NVDAObj = NVDAObj
		n = NVDAObj.childCount
		# TeamTalk version-specific toolbar item names by toolbar item count.
		self.names = []
		for lst in _msgNames.values():
			if len(lst) == n:
				self.names = lst
				break

	def getToolBar(self):
		# First lastChild is a Window object, then the client toolbar object.
		try:
			tb = api.getForegroundObject().lastChild.lastChild
		except AttributeError:
			tb = None
		return tb

	def name(self, itemID):
		"""The name of one item.
		"""
		if itemID <= 0:
			return ""
		# ChildIDs are 1-based, but Python arrays are 0-based.
		try:
			name = self.names[itemID - 1]
		except IndexError:
			return ""
		if name == "sep":
			return ""
		return name


class TTToolBar(IAccessible):
	def initOverlayClass(self):
		self.info = TTToolBarInfo(self)


class TTToolBarItem(IAccessible):
	def event_valueChange(self):
		speech.speakObject(self)

	def _get_name(self):
		return self.parent.info.name(self.IAccessibleChildID)


class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj):
		# For some TeamTalk versions, the incoming chat control does not
		# return the correct _isWindowUnicode flag.
		if obj.windowClassName == "RichEdit20A":
			obj._isWindowUnicode = False
		# Label channel chat in/out controls.
		if obj.windowControlID == ID_CHATOUT:
			# Translators: a label for a read only edit control
			# in the TeamTalk voice conferencing client where incoming chat
			# messages are displayed.
			obj.name = _("Channel messages")
		elif obj.windowControlID == ID_CHATIN:
			# Translators: a label for the TeamTalk chat entry field
			obj.name = _("Type a message to the channel")
		# Better name Add/Remove buttons where they occur.
		# Example: Banned Users dialog from the Server menu.
		elif obj.role == controlTypes.ROLE_BUTTON:
			if obj.name == ">":
				# Translators: A TeamTalk button label.
				obj.name = _("Add to unban list")
			elif obj.name == "<":
				# Translators: A TeamTalk button label.
				obj.name = _("Remove from unban list")
		# Name the lists in the Banned Users dialog.
		elif obj.role == controlTypes.ROLE_LIST:
			if obj.windowControlID == ID_BANNEDLIST:
				# Translators: Label for a list of banned users in TeamTalk
				obj.name = _("Banned")
			elif obj.windowControlID == ID_UNBANNEDLIST:
				# Translators: Label for a list of unbanned users in TeamTalk
				obj.name = _("Unbanned")

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# There is a VU meter progress bar in the main window
		# that shouldn't be monitored (it presents many spurious updates).
		if obj.windowClassName == "msctls_progress32" and (
			obj.name == "VU"
			or obj.windowControlID == ID_VU
		):
			try:
				clsList.remove(ProgressBar)
			except ValueError:
				from logHandler import log
				log.exception("Couldn't remove VU meter progress bar")
		# Name toolbar icons.
		elif obj.windowControlID == ID_TOOLBAR:
			# Applies to toolbar and its items.
			if obj.role == controlTypes.ROLE_TOOLBAR:
				clsList.insert(0, TTToolBar)
			elif obj.parent and obj.parent.role == controlTypes.ROLE_TOOLBAR:
				clsList.insert(0, TTToolBarItem)

	@scriptHandler.script(
		gesture="kb:control+shift+s",
		description="""Says various on/off states from the toolbar. Depending
on TeamTalk version, these can include connection status,
status of voice activation, push-to-talk, and video
features, whether channel audio is being saved to files,
and whether the channel message window is showing.
On one press, just says which are checked (in effect).
On two presses, says all states.
		"""
	)
	def script_sayToolbarInfo(self, gesture):
		info = TTToolBarInfo()
		if not info:
			return
		scnt = scriptHandler.getLastScriptRepeatCount()
		if scnt > 0:
			[
				speech.speakObject(o)
				for o in info.NVDAObj.children
				if o.role == controlTypes.ROLE_CHECKBOX
				and not (controlTypes.STATE_UNAVAILABLE in o.states)
			]
			return
		for o in info.NVDAObj.children:
			if o.role != controlTypes.ROLE_CHECKBOX:
				continue
			if controlTypes.STATE_UNAVAILABLE in o.states:
				continue
			if controlTypes.STATE_CHECKED not in o.states:
				continue
			speech.speakText(o.name)
