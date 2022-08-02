#appModules/poedit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012-2013 Mesar Hameed, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Poedit.
"""

import api
import appModuleHandler
import controlTypes
import displayModel
import textInfos
import tones
import ui
from NVDAObjects.IAccessible import sysListView32
import windowUtils
import NVDAObjects.IAccessible
import winUser


def fetchObject(obj, path):
	"""Fetch the child object  described by path.
	@returns: requested object if found, or None
	@rtype: L{NVDAObjects.NVDAObject}
	"""
	path.reverse()
	p = obj
	while len(path) and p.firstChild:
		p = p.firstChild
		steps = path.pop()
		i=0
		while i<steps and p.next: 
			p = p.next
			i += 1
		# the path requests us to look for further siblings, but none found.
		if i<steps: return None
	# the path requests us to look for further children, but none found.
	if len(path): return None
	return p


class AppModule(appModuleHandler.AppModule):

	def script_reportAutoCommentsWindow(self,gesture):
		obj = fetchObject(api.getForegroundObject(), [2, 0, 1, 0, 1, 0, 1])
		if obj and obj.windowControlID != 101:
			try:
				obj = obj.next.firstChild
			except AttributeError:
				obj = None
		elif obj:
			obj = obj.firstChild
		if obj:
			try:
				ui.message(obj.name + " " + obj.value)
			except:
				# Translators: this message is reported when there are no 
				# notes for translators to be presented to the user in Poedit.
				ui.message(_("No notes for translators."))
		else:
			# Translators: this message is reported when NVDA is unable to find 
			# the 'Notes for translators' window in poedit.
			ui.message(_("Could not find Notes for translators window."))
	# Translators: The description of an NVDA command for Poedit.
	script_reportAutoCommentsWindow.__doc__ = _("Reports any notes for translators")

	def script_reportCommentsWindow(self,gesture):
		try:
			obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(api.getForegroundObject().windowHandle, visible=True, controlID=104),
				winUser.OBJID_CLIENT, 0)
		except LookupError:
			# Translators: this message is reported when NVDA is unable to find
			# the 'comments' window in poedit.
			ui.message(_("Could not find comment window."))
			return None
		try:
			ui.message(obj.name + " " + obj.value)
		except:
			# Translators: this message is reported when there are no
			# comments to be presented to the user in the translator
			# comments window in poedit.
			ui.message(_("No comment."))
	# Translators: The description of an NVDA command for Poedit.
	script_reportCommentsWindow.__doc__ = _("Reports any comments in the comments window")

	__gestures = {
		"kb:control+shift+c": "reportCommentsWindow",
		"kb:control+shift+a": "reportAutoCommentsWindow",
	}

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if "SysListView32" in obj.windowClassName and obj.role==controlTypes.Role.LISTITEM:
			clsList.insert(0,PoeditListItem)

	def event_NVDAObject_init(self, obj):
		if obj.role == controlTypes.Role.EDITABLETEXT and controlTypes.State.MULTILINE in obj.states and obj.isInForeground:
			# Oleacc often gets the name wrong.
			# The label object is positioned just above the field on the screen.
			l, t, w, h = obj.location
			try:
				obj.name = NVDAObjects.NVDAObject.objectFromPoint(l + 10, t - 10).name
			except AttributeError:
				pass
			return

class PoeditListItem(sysListView32.ListItem):

	def _get_isBold(self):
		info=displayModel.DisplayModelTextInfo(self,position=textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_CHARACTER)
		fields=info.getTextWithFields()
		try:
			return fields[0].field['bold']
		except:
			return False

	def _get_name(self):
		# If this item is untranslated or fuzzy, then it will be bold.
		# Other info on the web says that the background color of 
		# the item changes, but this doesn't seem to be true while testing.
		name = super(PoeditListItem,self).name
		return "* " + name if self.isBold else name

	def event_gainFocus(self):
		super(sysListView32.ListItem, self).event_gainFocus()
		if self.isBold:
			tones.beep(550, 50)
