#NVDAObjects/IAccessible/ia2Web.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2017 NV Access Limited

"""Base classes with common support for browsers exposing IAccessible2.
"""

from ctypes import c_short
from comtypes import COMError, BSTR
import oleacc
import IAccessibleHandler
import controlTypes
from logHandler import log
from NVDAObjects.behaviors import Dialog, WebDialog 
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

	def _get_isCurrent(self):
		current = self.IA2Attributes.get("current", False)
		return current

	def _get_placeholder(self):
		placeholder = self.IA2Attributes.get('placeholder', None)
		return placeholder

	def _get_isPresentableFocusAncestor(self):
		if self.role==controlTypes.ROLE_TABLEROW:
			# It is not useful to present IAccessible2 table rows in the focus ancestry as  cells contain row and column information anyway.
			# Also presenting the rows would cause duplication of information
			return False
		return super(Ia2Web,self).isPresentableFocusAncestor

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

class EditorChunk(Ia2Web):
	beTransparentToMouse = True

class Math(Ia2Web):

	def _get_mathMl(self):
		from comtypes.gen.ISimpleDOM import ISimpleDOMNode
		try:
			node = self.IAccessibleObject.QueryInterface(ISimpleDOMNode)
			# Try the data-mathml attribute.
			attrNames = (BSTR * 1)("data-mathml")
			namespaceIds = (c_short * 1)(0)
			attr = node.attributesForNames(1, attrNames, namespaceIds)
			if attr:
				import mathPres
				if not mathPres.getLanguageFromMath(attr) and self.language:
					attr = mathPres.insertLanguageIntoMath(attr, self.language)
				return attr
			if self.IA2Attributes.get("tag") != "math":
				# This isn't MathML.
				raise LookupError
			if self.language:
				attrs = ' xml:lang="%s"' % self.language
			else:
				attrs = ""
			return "<math%s>%s</math>" % (attrs, node.innerHTML)
		except COMError:
			log.debugWarning("Error retrieving math. "
				"Not supported in this browser or ISimpleDOM COM proxy not registered.", exc_info=True)
			raise LookupError

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
	elif iaRole == oleacc.ROLE_SYSTEM_EQUATION:
		clsList.append(Math)

	if iaRole==oleacc.ROLE_SYSTEM_APPLICATION:
		clsList.append(Application)
	elif iaRole==oleacc.ROLE_SYSTEM_DIALOG:
		clsList.append(WebDialog)
	if iaRole in (oleacc.ROLE_SYSTEM_APPLICATION,oleacc.ROLE_SYSTEM_DIALOG,oleacc.ROLE_SYSTEM_DOCUMENT):
		clsList.append(documentClass)

	if obj.IA2States & IAccessibleHandler.IA2_STATE_EDITABLE:
		if obj.IAccessibleStates & oleacc.STATE_SYSTEM_FOCUSABLE:
			clsList.append(Editor)
		else:
			clsList.append(EditorChunk)

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
