#appModules/poedit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012 Mesar Hameed <mhameed@src.gnome.org>
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


def getPath(obj, ancestor):
	"""Gets the path of the object with respect to its ancestor.
	the ancestor is typically the forground object.

	@returns: A list of coordinates relative to the ansestor.
	@rtype: L{list}
	"""
	path = []
	cancel = 0
	if obj == stopObj: return []
	p = obj
	while p != stopObj:
		counter = 0
		while p.previous:
			p = p.previous
			counter += 1
			cancel += 1
			# Looks like we have an infinite ancestry, so get out
			if cancel == 50: return [-1]
		path.append(counter)
		p = p.parent
	path.reverse()
	return path

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
		obj = fetchObject(api.getForegroundObject(), [2, 0, 1, 0, 1, 0, 0, 0])
		# check the controlid, because in certain situations 
		# autoComments and comment windows change places.
		if obj and obj.windowControlID == 102:
			try:
				ui.message(obj.name + " " + obj.value)
			except:
				# Translators: this message is reported when there are no 
				# comments to be presented to the user in the automatic 
				# comments window in poedit.
				ui.message(_("No automatic comments."))
		else:
			# Translators: this message is reported when NVDA is unable to find 
			# the 'automatic comments' window in poedit.
			ui.message(_("Could not find automatic comments window."))

	def script_reportCommentsWindow(self,gesture):
		obj = fetchObject(api.getForegroundObject(), [2, 0, 1, 0, 1, 0, 1, 0])
		# if it isnt in the normal location, try to find it in the
		# location of the automatic window.
		if not obj: 
			obj = fetchObject(api.getForegroundObject(), [2, 0, 1, 0, 1, 0, 0, 0])
		if obj and obj.windowControlID == 105:
			try:
				ui.message(obj.name + " " + obj.value)
			except:
				# Translators: this message is reported when there are no
				# comments to be presented to the user in the translator
				# comments window in poedit.
				ui.message(_("No comment."))
		else:
			# Translators: this message is reported when NVDA is unable to find
			# the 'comments' window in poedit.
			ui.message(_("Could not find comment window."))

	__gestures = {
		"kb:control+shift+c": "reportCommentsWindow",
		"kb:control+shift+a": "reportAutoCommentsWindow",
	}

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if "SysListView32" in obj.windowClassName and obj.role==controlTypes.ROLE_LISTITEM:
			clsList.insert(0,PoeditListItem)
		if obj.role == controlTypes.ROLE_EDITABLETEXT:
			if obj.windowControlID == 102:
				# Translators: Automatic comments is the name of the poedit 
				# window that displays comments extracted from code.
				obj.name =  _("Automatic comments:")
			if obj.windowControlID == 104:
				# Translators: this is the label for the edit area in poedit 
				# that contains a translation.
				obj.name = _("Translation:")
			if obj.windowControlID == 105:
				# Translators: 'comments:' is the name of the poedit window 
				# that displays comments entered by the translator.
				obj.name = _("Comments:")

class PoeditListItem(sysListView32.ListItem):

	def _get_isBold(self):
		info=displayModel.DisplayModelTextInfo(self,position=textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_LINE)
		fields=info.getTextWithFields()
		try:
			return fields[1].field['bold']
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
