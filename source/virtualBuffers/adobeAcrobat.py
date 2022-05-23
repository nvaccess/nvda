#virtualBuffers/adobeAcrobat.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2012 NV Access Limited, Aleksey Sadovoy

from . import VirtualBuffer, VirtualBufferTextInfo
import browseMode
import controlTypes
import NVDAObjects.IAccessible
from NVDAObjects.IAccessible.adobeAcrobat import normalizeStdName, AcrobatNode
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos
import languageHandler

class AdobeAcrobat_TextInfo(VirtualBufferTextInfo):

	def _getBoundingRectFromOffset(self,offset):
		formatFieldStart, formatFieldEnd = self._getUnitOffsets(textInfos.UNIT_FORMATFIELD, offset)
		# The format field starts at the first character.
		for field in reversed(self._getFieldsInRange(formatFieldStart, formatFieldStart+1)):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "formatChange"):
				# This is no format field.
				continue
			attrs = field.field
			indexInParent = attrs.get("_indexInParent")
			if indexInParent is None:
				continue
			try:
				obj = self._getNVDAObjectFromOffset(offset).getChild(indexInParent)
			except IndexError:
				obj = None
			if not obj:
				continue
			if not obj.location:
				# Older versions of Adobe Reader have per word objects, but they don't expose a location
				break
			return obj.location
		return super(AdobeAcrobat_TextInfo, self)._getBoundingRectFromOffset(offset)

	def _normalizeControlField(self,attrs):
		stdName = attrs.get("acrobat::stdname", "")
		try:
			role, level = normalizeStdName(stdName)
		except LookupError:
			role, level = None, None

		if not role:
			role = IAccessibleHandler.NVDARoleFromAttr(attrs['IAccessible::role'])
		states = IAccessibleHandler.getStatesSetFromIAccessibleAttrs(attrs)
		role, states = controlTypes.transformRoleStates(role, states)

		if (
			role == controlTypes.Role.EDITABLETEXT
			and states.issuperset({
				controlTypes.State.READONLY,
				controlTypes.State.FOCUSABLE,
				controlTypes.State.LINKED
			})
		):
			# HACK: Acrobat sets focus states on text nodes beneath links,
			# making them appear as read only editable text fields.
			states.difference_update({controlTypes.State.FOCUSABLE, controlTypes.State.FOCUSED})

		attrs['role']=role
		attrs['states']=states
		if level:
			attrs["level"] = level
		return super(AdobeAcrobat_TextInfo, self)._normalizeControlField(attrs)

	def _normalizeFormatField(self, attrs):
		try:
			attrs["language"] = languageHandler.normalizeLanguage(attrs["language"])
		except KeyError:
			pass
		try:
			attrs["_indexInParent"] = int(attrs["_indexInParent"])
		except KeyError:
			pass
		return attrs

class AdobeAcrobat(VirtualBuffer):
	TextInfo = AdobeAcrobat_TextInfo
	programmaticScrollMayFireEvent = True

	def __init__(self,rootNVDAObject):
		super(AdobeAcrobat,self).__init__(rootNVDAObject,backendName="adobeAcrobat")

	def __contains__(self,obj):
		return winUser.isDescendantWindow(self.rootNVDAObject.windowHandle, obj.windowHandle)

	def _get_isAlive(self):
		if self.isLoading:
			return True
		root=self.rootNVDAObject
		if not root:
			return False
		if not winUser.isWindow(root.windowHandle) or root.role == controlTypes.Role.UNKNOWN:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		return NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle, winUser.OBJID_CLIENT, ID)

	def getIdentifierFromNVDAObject(self,obj):
		if not isinstance(obj,AcrobatNode):
			raise LookupError
		return obj.windowHandle, obj.accID

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType in ("link", "unvisitedLink"):
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK]}
		elif nodeType=="table":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TABLE]}
		elif nodeType.startswith("heading") and nodeType[7:].isdigit():
			attrs = {"acrobat::stdname": ["H%s" % nodeType[7:]]}
		elif nodeType == "heading":
			attrs = {"acrobat::stdname": ["H", "H1", "H2", "H3", "H4", "H5", "H6"]}
		elif nodeType == "formField":
			attrs = {"IAccessible::role": [oleacc.ROLE_SYSTEM_PUSHBUTTON, oleacc.ROLE_SYSTEM_RADIOBUTTON, oleacc.ROLE_SYSTEM_CHECKBUTTON, oleacc.ROLE_SYSTEM_COMBOBOX, oleacc.ROLE_SYSTEM_LIST, oleacc.ROLE_SYSTEM_OUTLINE, oleacc.ROLE_SYSTEM_TEXT], "IAccessible::state_%s" % oleacc.STATE_SYSTEM_READONLY: [None]}
		elif nodeType == "list":
			attrs = {"acrobat::stdname": ["L"]}
		elif nodeType == "listItem":
			attrs = {"acrobat::stdname": ["LI"]}
		elif nodeType=="button":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_READONLY:[None]}
		elif nodeType=="radioButton":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_RADIOBUTTON]}
		elif nodeType=="checkBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_CHECKBUTTON]}
		elif nodeType == "blockQuote":
			attrs = {"acrobat::stdname": ["BlockQuote"]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="graphic":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_GRAPHIC]}
		elif nodeType=="comboBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_COMBOBOX]}
		else:
			return None
		return attrs

	def event_valueChange(self, obj, nextHandler):
		if obj.event_childID == 0:
			return nextHandler()
		if not self._handleScrollTo(obj):
			return nextHandler()

	def _get_ElementsListDialog(self):
		return ElementsListDialog

class ElementsListDialog(browseMode.ElementsListDialog):

	ELEMENT_TYPES=browseMode.ElementsListDialog.ELEMENT_TYPES[0:2]
