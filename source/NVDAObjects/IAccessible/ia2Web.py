#NVDAObjects/IAccessible/ia2Web.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2015 NV Access Limited

"""Base classes with common support for browsers exposing IAccessible2.
"""

import oleacc
import IAccessibleHandler
import controlTypes
from NVDAObjects.behaviors import Dialog
from . import IAccessible
from .ia2TextMozilla import MozillaCompoundTextInfo

class Ia2Web(IAccessible):
	IAccessibleTableUsesTableCellIndexAttrib=True

	def _get_positionInfo(self):
		info=super(Ia2Web,self).positionInfo
		level=info.get('level',None)
		if not level:
			level=self.IA2Attributes.get('level',None)
			if level:
				info['level']=level
		return info

class Document(Ia2Web):
	value = None

	def _get_shouldCreateTreeInterceptor(self):
		return controlTypes.STATE_READONLY in self.states

class Application(Document):
	shouldCreateTreeInterceptor = False

class BlockQuote(Ia2Web):
	role = controlTypes.ROLE_BLOCKQUOTE

class Editor(Ia2Web):
	TextInfo = MozillaCompoundTextInfo

def findExtraOverlayClasses(obj, clsList, baseClass=Ia2Web, documentClass=None):
	"""Determine the most appropriate class if this is an IA2 web object.
	This should be called after finding any classes for the specific web implementation.
	@param baseClass: The base class for all web objects.
	@param documentClass: The class to use for document roots, including ARIA applications.
	"""
	if not documentClass:
		raise ValueError("documentClass cannot be None")
	if not isinstance(obj.IAccessibleObject, IAccessibleHandler.IAccessible2):
		return

	iaRole = obj.IAccessibleRole
	if iaRole == IAccessibleHandler.IA2_ROLE_SECTION and obj.IA2Attributes.get("tag", None) == "blockquote":
		clsList.append(BlockQuote)
	elif iaRole == oleacc.ROLE_SYSTEM_ALERT:
		clsList.append(Dialog)

	isApp = iaRole in (oleacc.ROLE_SYSTEM_APPLICATION, oleacc.ROLE_SYSTEM_DIALOG)
	if isApp:
		clsList.append(Application)
	if isApp or iaRole == oleacc.ROLE_SYSTEM_DOCUMENT:
		clsList.append(documentClass)

	if obj.IA2States & IAccessibleHandler.IA2_STATE_EDITABLE and obj.IAccessibleStates & oleacc.STATE_SYSTEM_FOCUSABLE:
		clsList.append(Editor)

	if iaRole in (oleacc.ROLE_SYSTEM_DIALOG,oleacc.ROLE_SYSTEM_PROPERTYPAGE):
		xmlRoles = obj.IA2Attributes.get("xml-roles", "").split(" ")
		if "dialog" in xmlRoles or "tabpanel" in xmlRoles:
			# #2390: Don't try to calculate text for ARIA dialogs.
			# #4638: Don't try to calculate text for ARIA tab panels.
			try:
				clsList.remove(Dialog)
			except ValueError:
				pass

	clsList.append(baseClass)
