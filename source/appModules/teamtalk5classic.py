# appModules/tt_classic.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2019 NVDA Contributors, Doug Lee, Tyler Spivey, Bill Dengler
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
# The names, in order, of the toolbar items.
# The count must match exactly or this module will not function.
# The name "sep" is a placeholder for separators in the toolbar.
# These are name sets per client version.
# Stored in reverse so current clients find the right list faster.
_msgNames = {
	"4.5": [
		_("Connected"),
		"sep",
		_("Push To Talk"),
		_("Voice Activation"),
		_("Video"),
		_("Desktop"),
		_("Stream To Channel"),
		"sep",
		_("Mute All"),
		_("Store Audio"),
		"sep",
		_("Show Channel Messages"),
	],
	"4.3": [
		_("Connected"),
		"sep",
		_("Push To Talk"),
		_("Voice Activation"),
		_("Video"),
		_("Desktop"),
		_("Mute All"),
		_("Store Audio"),
		"sep",
		_("Show Channel Messages"),
	],
	"4.2": [
		_("Connected"),
		"sep",
		_("Push To Talk"),
		_("Voice Activation"),
		"sep",
		_("Mute All"),
		_("Store Audio"),
		"sep",
		_("Show Channel Messages"),
	],
	"4.1": [
		_("Connected"),
		"sep",
		_("Push To Talk"),
		_("Voice Activation"),
		"sep",
		_("Mute All"),
		"sep",
		_("Show Channel Messages"),
	],
}

# How checkboxes on the toolbar are announced when activated (checked) or deactivated.
# %1 is a name from the above list of item names.
_msgActive = _("%s active")
_msgInactive = _("%s disabled")
_msgConnected = _("Connected")
_msgDisconnected = _("Disconnected")


class TTToolBarInfo(object):
	"""Info about one TeamTalk toolbar and its items.
	"""

	def __init__(self, NVDAObj=None):
		if not NVDAObj:
			# Use the IAccessible for the active TeamTalk instance's toolbar.
			NVDAObj = self.getToolBar()
			if not NVDAObj:
				ui.message(_("Toolbar not found"))
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

	@property
	def name(self):
		return self.parent.info.name(self.IAccessibleChildID)


class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj):
		# The richedit control displaying incoming chat does not return correct _isWindowUnicode flag.
		if obj.windowClassName == "RichEdit20A":
			obj._isWindowUnicode = False
		# Label channel chat in/out controls.
		if obj.windowControlID == 1204:
			obj.name = _("Channel messages")
		elif obj.windowControlID == 1206:
			obj.name = _("Type a message to the channel")
		# Better name Add/Remove buttons where they occur.
		# Example: Banned Users dialog from the Server menu.
		elif obj.role == controlTypes.ROLE_BUTTON:
			if obj.name == ">":
				obj.name = _("Add to unban list")
			elif obj.name == "<":
				obj.name = _("Remove from unban list")
		# Name the lists in the Banned Users dialog.
		elif obj.role == controlTypes.ROLE_LIST:
			if obj.windowControlID == 1326:
				obj.name = _("Banned")
			elif obj.windowControlID == 1327:
				obj.name = _("Unbanned")

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# There is a VU meter progress bar in the main window which we don't want to get anounced as all the other progress bars.
		if obj.windowClassName == "msctls_progress32" and obj.name == _("VU"):
			try:
				clsList.remove(ProgressBar)
			except ValueError:
				pass
		# Name toolbar icons.
		elif obj.windowControlID == 59392:
			# Applies to toolbar and its items.
			if obj.role == controlTypes.ROLE_TOOLBAR:
				clsList.insert(0, TTToolBar)
			elif obj.parent and obj.parent.role == controlTypes.ROLE_TOOLBAR:
				clsList.insert(0, TTToolBarItem)

	def script_sayToolbarInfo(self, gesture):
		"""Say various on/off states from the toolbar. Depending
		on TeamTalk version, these can include connection status,
		status of voice activation, push-to-talk, and video
		features, whether channel audio is being saved to files,
		and whether the channel message window is showing.
		On one press, just says which are checked (in effect).
		On two presses, says all states.
		"""
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

	__gestures = {"kb:control+shift+s": "sayToolbarInfo"}
