#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2012 NV Access Limited
import appModuleHandler
import controlTypes
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import DisplayModelEditableText
import winUser
import api
import virtualBuffers.lotusNotes

#IRIS.tedit editable text controls are accessibl with displayModel, but they have no suitable labels
#There are usually fake IAccessibles at the same screen coordinates containing a better label
class IrisTedit(IAccessible):

	def _get_name(self):
		label=api.getDesktopObject().objectFromPoint(*self.location.center)
		if label:
			return label.name

#Some NotesrichText controls are accessible with displayModel.
#However, there are many added purely as fake IAccessibles to provide extra info such as a label.
#These controls do not contain the caret, yet fire focus events.
#These must be ignored as focus was already correct.
class NotesRichText(IAccessible):

	def _get_shouldAllowIAccessibleFocusEvent(self):
		if not isinstance(self,DisplayModelEditableText) and self.role==controlTypes.Role.EDITABLETEXT:
			return False
		return super(NotesRichText,self).shouldAllowIAccessibleFocusEvent

	def _get_treeInterceptorClass(self):
		if controlTypes.State.READONLY in self.states:
			return virtualBuffers.lotusNotes.LotusNotesRichText
		raise NotImplementedError

class NotesSubprog(IAccessible):
	shouldAllowIAccessibleFocusEvent=False
	presentationType=IAccessible.presType_layout

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		windowClassName=obj.windowClassName
		role=obj.role
		states=obj.states
		if windowClassName=="NotesSubprog" and role==controlTypes.Role.DOCUMENT:
			clsList.insert(0,NotesSubprog)
		elif windowClassName=="NotesRichText" and role in (controlTypes.Role.DOCUMENT,controlTypes.Role.EDITABLETEXT):
			clsList.insert(0,NotesRichText)
		elif windowClassName=="IRIS.tedit" and isinstance(obj,IAccessible) and obj.event_objectID==winUser.OBJID_CLIENT: 
			clsList.insert(0,IrisTedit)
