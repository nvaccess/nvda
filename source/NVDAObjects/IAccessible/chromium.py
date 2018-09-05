#NVDAObjects/IAccessible/chromium.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
# Copyright (C) 2010-2013 NV Access Limited

"""NVDAObjects for the Chromium browser project
"""

from comtypes import COMError
import oleacc
import controlTypes
import IAccessibleHandler
from NVDAObjects.IAccessible import IAccessible
from virtualBuffers.gecko_ia2 import Gecko_ia2 as GeckoVBuf
from . import ia2Web

class ChromeVBuf(GeckoVBuf):

	def __contains__(self, obj):
		if obj.windowHandle != self.rootNVDAObject.windowHandle:
			return False
		if not isinstance(obj,ia2Web.Ia2Web):
			# #4080: Input composition NVDAObjects are the same window but not IAccessible2!
			return False
		accId = obj.IA2UniqueID
		if accId == self.rootID:
			return True
		try:
			self.rootNVDAObject.IAccessibleObject.accChild(accId)
		except COMError:
			return False
		return not self._isNVDAObjectInApplication(obj)

class Document(ia2Web.Document):

	def _get_treeInterceptorClass(self):
		states = self.states
		if controlTypes.STATE_EDITABLE not in states and controlTypes.STATE_BUSY not in states:
			return ChromeVBuf
		return super(Document, self).treeInterceptorClass

class ComboboxListItem(IAccessible):
	"""
	Represents a list item inside a combo box.
	"""

	def _get_focusRedirect(self):
		# Chrome 68 and below fires focus on the active list item of combo boxes even when the combo box is collapsed.
		# We get around this by redirecting focus back up to the combo box itself if the list inside is invisible (I.e. the combo box is collapsed).
		if self.parent and controlTypes.STATE_INVISIBLE in self.parent.states:
			return self.parent.parent

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for Chromium objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	if obj.role==controlTypes.ROLE_LISTITEM and obj.parent and obj.parent.parent and obj.parent.parent.role==controlTypes.ROLE_COMBOBOX:
		clsList.append(ComboboxListItem)
	ia2Web.findExtraOverlayClasses(obj, clsList,
		documentClass=Document)
