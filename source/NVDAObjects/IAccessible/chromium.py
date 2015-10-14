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
from NVDAObjects.behaviors import Dialog
from .ia2TextMozilla import MozillaCompoundTextInfo

class ChromeVBuf(GeckoVBuf):

	def __contains__(self, obj):
		if obj.windowHandle != self.rootNVDAObject.windowHandle:
			return False
		accId = obj.IA2UniqueID
		if accId == self.rootID:
			return True
		try:
			self.rootNVDAObject.IAccessibleObject.accChild(accId)
		except COMError:
			return False
		return True

class Document(IAccessible):
	value = None

	def _get_treeInterceptorClass(self):
		states = self.states
		if controlTypes.STATE_READONLY in states and controlTypes.STATE_BUSY not in states:
			return ChromeVBuf
		return super(Document, self).treeInterceptorClass

class Editor(IAccessible):
	TextInfo = MozillaCompoundTextInfo

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for Chromium objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	if not isinstance(obj.IAccessibleObject, IAccessibleHandler.IAccessible2):
		return

	role = obj.role
	if role == controlTypes.ROLE_DOCUMENT:
		clsList.append(Document)

	if obj.IAccessibleStates & oleacc.STATE_SYSTEM_FOCUSABLE:
		try:
			ia2States = obj.IAccessibleObject.states
		except COMError:
			ia2States = 0
		if ia2States & IAccessibleHandler.IA2_STATE_EDITABLE:
			clsList.append(Editor)

	if role == controlTypes.ROLE_DIALOG:
		xmlRoles = obj.IA2Attributes.get("xml-roles", "").split(" ")
		if "dialog" in xmlRoles:
			# #2390: Don't try to calculate text for ARIA dialogs.
			try:
				clsList.remove(Dialog)
			except ValueError:
				pass
