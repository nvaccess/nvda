# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2023 NV Access Limited, Babbage B.V., Mozilla Corporation, Accessolutions, Julien Cochuyt

from dataclasses import dataclass
from typing import (
	Iterable,
	Optional,
)
import typing
import weakref
from ctypes import byref
from . import VirtualBuffer, VirtualBufferTextInfo, VBufStorage_findMatch_word, VBufStorage_findMatch_notEmpty
import treeInterceptorHandler
import controlTypes
import NVDAObjects.IAccessible.mozilla
import NVDAObjects.behaviors
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos
from comtypes.gen.IAccessible2Lib import IAccessible2
from comInterfaces import IAccessible2Lib as IA2
from comInterfaces.IAccessible2Lib import IAccessibleTextSelectionContainer, IA2TextSelection, IAccessibleText
from comtypes import COMError
import aria
import config
from NVDAObjects.IAccessible import normalizeIA2TextFormatField, IA2TextTextInfo
import documentBase


def _getNormalizedCurrentAttrs(attrs: textInfos.ControlField) -> typing.Dict[str, typing.Any]:
	valForCurrent = attrs.get("IAccessible2::attribute_current", "false")
	try:
		isCurrent = controlTypes.IsCurrent(valForCurrent)
	except ValueError:
		log.debugWarning(f"Unknown isCurrent value: {valForCurrent}")
		isCurrent = controlTypes.IsCurrent.NO
	if isCurrent != controlTypes.IsCurrent.NO:
		return {
			'current': isCurrent
		}
	return {}


class Gecko_ia2_TextInfo(VirtualBufferTextInfo):

	def _setSelectionOffsets(self, start: int, end: int):
		super()._setSelectionOffsets(start, end)
		if self.obj._nativeAppSelectionMode:
			if start != end:
				self.obj.updateAppSelection()
			else:
				self.obj.clearAppSelection()

	def _getBoundingRectFromOffset(self,offset):
		formatFieldStart, formatFieldEnd = self._getUnitOffsets(textInfos.UNIT_FORMATFIELD, offset)
		# The format field starts at the first character.
		for field in reversed(self._getFieldsInRange(formatFieldStart, formatFieldStart+1)):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "formatChange"):
				# This is no format field.
				continue
			attrs = field.field
			ia2TextStartOffset = attrs.get("ia2TextStartOffset")
			if ia2TextStartOffset is None:
				# No ia2TextStartOffset specified, most likely a format field that doesn't originate from IA2Text.
				continue
			ia2TextStartOffset += attrs.get("strippedCharsFromStart", 0)
			relOffset = offset - formatFieldStart + ia2TextStartOffset
			obj = self._getNVDAObjectFromOffset(offset)
			if not hasattr(obj, "IAccessibleTextObject"):
				raise LookupError("Object doesn't have an IAccessibleTextObject")
			return IA2TextTextInfo._getBoundingRectFromOffsetInObject(obj, relOffset)
		return super(Gecko_ia2_TextInfo, self)._getBoundingRectFromOffset(offset)

	def _calculateDescriptionFrom(self, attrs: textInfos.ControlField) -> controlTypes.DescriptionFrom:
		"""Overridable calculation of DescriptionFrom
		Match behaviour of NVDAObjects.IAccessible.mozilla.Mozilla._get_descriptionFrom
		@param attrs: source attributes for the TextInfo
		@return: the origin for accDescription.
		@remarks: Firefox does not yet have a 'IAccessible2::attribute_description-from'
			(IA2 attribute "description-from").
			We can infer that the origin of accDescription is 'aria-description' because Firefox will include
			a 'IAccessible2::attribute_description' (IA2 attribute "description") when the aria-description
			HTML attribute is used.
			If 'IAccessible2::attribute_description' matches the accDescription value, we can infer that
			aria-description was the original source.
		"""
		IA2Attr_desc = attrs.get("IAccessible2::attribute_description")
		accDesc = attrs.get("description")
		if not IA2Attr_desc or accDesc != IA2Attr_desc:
			return controlTypes.DescriptionFrom.UNKNOWN
		else:
			return controlTypes.DescriptionFrom.ARIA_DESCRIPTION

	# C901 '_normalizeControlField' is too complex
	# Note: when working on _normalizeControlField, look for opportunities to simplify
	# and move logic out into smaller helper functions.
	def _normalizeControlField(self, attrs):  # noqa: C901
		# convert some IAccessible2 text values to integers
		for name in (
			"ia2TextWindowHandle",
			"ia2TextUniqueID",
			"ia2TextStartOffset",
		):
			val = attrs.get(name, None)
			if val is not None:
				attrs[name] = int(val)
		for attr in (
			"table-rownumber-presentational",
			"table-columnnumber-presentational",
			"table-rowcount-presentational",
			"table-columncount-presentational"
		):
			attrVal = attrs.get(attr)
			if attrVal is not None and attrVal.lstrip('-').isdigit():
				attrs[attr] = int(attrVal)
			else:
				attrs[attr] = None

		attrs["_description-from"] = self._calculateDescriptionFrom(attrs)
		attrs.update(_getNormalizedCurrentAttrs(attrs))

		placeholder = self._getPlaceholderAttribute(attrs, "IAccessible2::attribute_placeholder")
		if placeholder is not None:
			attrs['placeholder']= placeholder

		role = IAccessibleHandler.NVDARoleFromAttr(attrs['IAccessible::role'])
		if attrs.get('IAccessible2::attribute_tag',"").lower()=="blockquote":
			role=controlTypes.Role.BLOCKQUOTE

		states = IAccessibleHandler.getStatesSetFromIAccessibleAttrs(attrs)
		states |= IAccessibleHandler.getStatesSetFromIAccessible2Attrs(attrs)
		role, states = controlTypes.transformRoleStates(role, states)

		if role == controlTypes.Role.EDITABLETEXT and not (controlTypes.State.FOCUSABLE in states or controlTypes.State.UNAVAILABLE in states or controlTypes.State.EDITABLE in states):
			# This is a text leaf.
			# See NVDAObjects.Iaccessible.mozilla.findOverlayClasses for an explanation of these checks.
			role = controlTypes.Role.STATICTEXT
		if attrs.get("IAccessibleAction_showlongdesc") is not None:
			states.add(controlTypes.State.HASLONGDESC)
		if "IAccessibleAction_click" in attrs:
			states.add(controlTypes.State.CLICKABLE)
		grabbed = attrs.get("IAccessible2::attribute_grabbed")
		if grabbed == "false":
			states.add(controlTypes.State.DRAGGABLE)
		elif grabbed == "true":
			states.add(controlTypes.State.DRAGGING)
		sorted = attrs.get("IAccessible2::attribute_sort")
		if sorted=="ascending":
			states.add(controlTypes.State.SORTED_ASCENDING)
		elif sorted=="descending":
			states.add(controlTypes.State.SORTED_DESCENDING)
		elif sorted=="other":
			states.add(controlTypes.State.SORTED)
		roleText=attrs.get("IAccessible2::attribute_roledescription")
		if roleText:
			attrs['roleText']=roleText
		roleTextBraille = attrs.get("IAccessible2::attribute_brailleroledescription")
		if roleTextBraille:
			attrs['roleTextBraille'] = roleTextBraille
		if attrs.get("IAccessible2::attribute_dropeffect", "none") != "none":
			states.add(controlTypes.State.DROPTARGET)
		if role==controlTypes.Role.LINK and controlTypes.State.LINKED not in states:
			# This is a named link destination, not a link which can be activated. The user doesn't care about these.
			role=controlTypes.Role.TEXTFRAME
		level=attrs.get('IAccessible2::attribute_level',"")
		xmlRoles = attrs.get("IAccessible2::attribute_xml-roles", "").split(" ")
		landmark = next((xr for xr in xmlRoles if xr in aria.landmarkRoles), None)
		if landmark and role != controlTypes.Role.LANDMARK and landmark != xmlRoles[0]:
			# Ignore the landmark role
			landmark = None
		if role == controlTypes.Role.DOCUMENT and xmlRoles[0] == "article":
			role = controlTypes.Role.ARTICLE
		elif role == controlTypes.Role.GROUPING and xmlRoles[0] == "figure":
			role = controlTypes.Role.FIGURE
		elif role in (controlTypes.Role.LANDMARK, controlTypes.Role.SECTION) and xmlRoles[0] == "region":
			role = controlTypes.Role.REGION
		elif xmlRoles[0] == "switch":
			# role="switch" gets mapped to IA2_ROLE_TOGGLE_BUTTON, but it uses the
			# checked state instead of pressed.
			# We want to map this to our own Switch role and On state.
			role = controlTypes.Role.SWITCH
			states.discard(controlTypes.State.PRESSED)
			states.discard(controlTypes.State.CHECKABLE)
			if controlTypes.State.CHECKED in states:
				states.discard(controlTypes.State.CHECKED)
				states.add(controlTypes.State.ON)
		popupState = aria.ariaHaspopupValuesToNVDAStates.get(
			attrs.get("IAccessible2::attribute_haspopup")
		)
		if popupState:
			states.discard(controlTypes.State.HASPOPUP)
			states.add(popupState)
		attrs['role']=role
		attrs['states']=states
		if level != "" and level is not None:
			attrs['level']=level
		if landmark:
			attrs["landmark"]=landmark

		detailsRoles = attrs.get('detailsRoles')
		if detailsRoles is not None:
			attrs['detailsRoles'] = set(self._normalizeDetailsRole(detailsRoles))
			if config.conf["debugLog"]["annotations"]:
				log.debug(f"detailsRoles: {attrs['detailsRoles']}")
		return super()._normalizeControlField(attrs)

	def _normalizeDetailsRole(self, detailsRoles: str) -> Iterable[Optional[controlTypes.Role]]:
		"""
		The attribute has been added directly to the buffer as a string, containing a comma separated list
		of values, each value is either:
		- role string
		- role integer
		Ensures the returned role is a fully supported by the details-roles attribute.
		Braille and speech needs consistent normalization for translation and reporting.
		"""
		# Can't import at module level as chromium imports from this module
		from NVDAObjects.IAccessible.chromium import supportedAriaDetailsRoles
		if config.conf["debugLog"]["annotations"]:
			log.debug(f"detailsRoles: {repr(detailsRoles)}")
		detailsRolesValues = detailsRoles.split(',')
		for detailsRole in detailsRolesValues:
			if detailsRole.isdigit():
				detailsRoleInt = int(detailsRole)
				# get a role, but it may be unsupported
				detailsRole = IAccessibleHandler.IAccessibleRolesToNVDARoles.get(detailsRoleInt)
				# return a supported details role
				if detailsRole in supportedAriaDetailsRoles.values():
					yield detailsRole
				else:
					yield None
			else:
				# return a supported details role
				# Note, "unknown" is used when the target has no role.
				if detailsRole == "unknown" and config.conf["debugLog"]["annotations"]:
					log.debug("Found unknown aria details role")
				detailsRole = supportedAriaDetailsRoles.get(detailsRole)
				yield detailsRole

	def _normalizeFormatField(self, attrs):
		normalizeIA2TextFormatField(attrs)
		# convert some IAccessible2 values to integers
		for name in (
			"ia2TextWindowHandle",
			"ia2TextUniqueID",
			"ia2TextStartOffset",
		):
			val = attrs.get(name, None)
			if val is not None:
				attrs[name] = int(val)
		return super(Gecko_ia2_TextInfo,self)._normalizeFormatField(attrs)


class Gecko_ia2(VirtualBuffer):

	TextInfo=Gecko_ia2_TextInfo
	#: Maps NVDAObjects to a list of iframes/frames in that object's ancestry,
	#: ordered from deepest to shallowest. The key is held as a weak reference so
	#: that the cache for an object is cleaned up when that object dies. Each
	#: frame/iframe in the lists is a tuple of (IAccessible2_2, uniqueId). This
	#: cache is used across instances.
	_framesCache = weakref.WeakKeyDictionary()
	_nativeAppSelectionModeSupported = True

	def __init__(self,rootNVDAObject):
		super(Gecko_ia2,self).__init__(rootNVDAObject,backendName="gecko_ia2")
		self._initialScrollObj = None

	@staticmethod
	def _getEmbedderFrame(acc):
		"""Get the iframe/frame (if any) which contains the given object.
		For example, if acc is a button inside an iframe, this will return the iframe.
		"""
		try:
			# 1. Get the containing document.
			if not isinstance(acc, IA2.IAccessible2_2):
				# IAccessible NVDAObjects currently fetch IA2, but we need IA2_2 for relationTargetsOfType.
				# (Out-of-process, for a single relation, this is cheaper than IA2::relations.)
				acc = acc.QueryInterface(IA2.IAccessible2_2)
			targets, count = acc.relationTargetsOfType(
				IAccessibleHandler.RelationType.CONTAINING_DOCUMENT,
				1  # max relations to fetch
			)
			if count == 0:
				return None
			doc = targets[0].QueryInterface(IA2.IAccessible2_2)
			# 2. Get its parent (the embedder); e.g. iframe.
			embedder = doc.accParent
			if not embedder:
				return None
			embedder = embedder.QueryInterface(IA2.IAccessible2_2)
			# 3. Make sure this is an iframe/frame.
			attribs = embedder.attributes
			if "tag:browser;" in attribs:
				# This is a top level browser, not an iframe/frame.
				return None
			return embedder
		except COMError:
			return None

	@classmethod
	def _iterIdsToTryWithAccChild(cls, obj):
		"""Return the child ids we should try with accChild in order to determine
		whether this object is a descendant of a particular document.
		"""
		# 1. Try the object itself.
		acc = obj.IAccessibleObject
		accId = obj.IA2UniqueID
		yield accId
		# 2. If this fails, this might be because the object is in an
		# out-of-process frame, in which case the embedder document won't know
		# about it. Try embedder frames.
		# 2.1. Try cached frames. We cache because walking frames is expensive,
		# and when trying to work out what TreeInterceptor this object belongs to,
		# we'll need to query these frames for each TreeInterceptor.
		cache = cls._framesCache.setdefault(obj, [])
		for acc, accId in cache:
			if not acc:
				# All frames were cached in a previous run. There are no more.
				return
			yield accId
		# 2.2. Walk remaining ancestor embedder frames, filling the cache as we go.
		while True:
			acc = cls._getEmbedderFrame(acc)
			if not acc:
				# No more. Signal this in the cache.
				cache.append((None, None))
				return
			try:
				accId = acc.uniqueID
			except COMError:
				# Dead object.
				cache.append((None, None))
				return
			cache.append((acc, accId))
			yield accId

	def __contains__(self,obj):
		if (
			not (
				isinstance(obj, NVDAObjects.IAccessible.IAccessible)
				and isinstance(obj.IAccessibleObject, IA2.IAccessible2)
			)
			or not obj.windowClassName.startswith('Mozilla')
			or not winUser.isDescendantWindow(self.rootNVDAObject.windowHandle, obj.windowHandle)
		):
			return False
		for accId in self._iterIdsToTryWithAccChild(obj):
			if accId == self.rootID:
				return True
			try:
				self.rootNVDAObject.IAccessibleObject.accChild(accId)
				# The object is definitely a descendant of the document.
				break
			except COMError:
				pass
		else:
			# The object is definitely not a descendant of the document.
			return False

		return not self._isNVDAObjectInApplication(obj)

	def _get_isAlive(self):
		if self.isLoading:
			return True
		root=self.rootNVDAObject
		if not root:
			return False
		if not winUser.isWindow(root.windowHandle):
			return False
		if not root.isInForeground:
			# #7818: Subsequent checks make COM calls.
			# The chances of a buffer dying while the window is in the background are
			# low, so don't make COM calls in this case; just treat it as alive.
			# This prevents freezes on every focus change if the browser process
			# stops responding; e.g. it froze, crashed or is being debugged.
			return True
		try:
			isDefunct = bool(root.IAccessibleObject.states & IA2.IA2_STATE_DEFUNCT)
		except COMError:
			# If IAccessible2 states can not be fetched at all, defunct should be assumed as the object has clearly been disconnected or is dead
			isDefunct=True
		return not isDefunct

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		return NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle, winUser.OBJID_CLIENT, ID)

	def getIdentifierFromNVDAObject(self,obj):
		docHandle=obj.windowHandle
		ID=obj.IA2UniqueID
		return docHandle,ID

	def _shouldIgnoreFocus(self, obj):
		if obj.role == controlTypes.Role.DOCUMENT and controlTypes.State.EDITABLE not in obj.states:
			return True
		return super(Gecko_ia2, self)._shouldIgnoreFocus(obj)

	def _postGainFocus(self, obj):
		if isinstance(obj, NVDAObjects.behaviors.EditableText):
			# We aren't passing this event to the NVDAObject, so we need to do this ourselves.
			obj.initAutoSelectDetection()
		super(Gecko_ia2, self)._postGainFocus(obj)

	def _shouldSetFocusToObj(self, obj):
		if obj.role == controlTypes.Role.GRAPHIC and controlTypes.State.LINKED in obj.states:
			return True
		return super(Gecko_ia2,self)._shouldSetFocusToObj(obj)

	def _activateLongDesc(self,controlField):
		index=int(controlField['IAccessibleAction_showlongdesc'])
		docHandle=int(controlField['controlIdentifier_docHandle'])
		ID=int(controlField['controlIdentifier_ID'])
		obj=self.getNVDAObjectFromIdentifier(docHandle,ID)
		obj.doAction(index)

	def _searchableTagValues(self, values):
		return values

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType.startswith('heading') and nodeType[7:].isdigit():
			attrs = {"IAccessible::role": [IA2.IA2_ROLE_HEADING], "IAccessible2::attribute_level": [nodeType[7:]]}
		elif nodeType == "annotation":
			attrs = {
				"IAccessible::role": [IA2.IA2_ROLE_CONTENT_DELETION, IA2.IA2_ROLE_CONTENT_INSERTION]
			}
		elif nodeType=="heading":
			attrs = {"IAccessible::role": [IA2.IA2_ROLE_HEADING]}
		elif nodeType=="table":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TABLE]}
			if not config.conf["documentFormatting"]["includeLayoutTables"]:
				attrs["table-layout"]=[None]
		elif nodeType=="link":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_LINKED:[1]}
		elif nodeType=="visitedLink":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_TRAVERSED:[1]}
		elif nodeType=="unvisitedLink":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_LINKED:[1],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_TRAVERSED:[None]}
		elif nodeType=="formField":
			attrs=[
				{
					"IAccessible::role": [
						oleacc.ROLE_SYSTEM_BUTTONMENU,
						oleacc.ROLE_SYSTEM_CHECKBUTTON,
						oleacc.ROLE_SYSTEM_COMBOBOX,
						oleacc.ROLE_SYSTEM_LIST,
						oleacc.ROLE_SYSTEM_OUTLINE,
						oleacc.ROLE_SYSTEM_PUSHBUTTON,
						oleacc.ROLE_SYSTEM_RADIOBUTTON,
						oleacc.ROLE_SYSTEM_PAGETAB,
						IA2.IA2_ROLE_TOGGLE_BUTTON,
					],
					f"IAccessible::state_{oleacc.STATE_SYSTEM_READONLY}": [None],
				},
				{
					"IAccessible::role": [
						oleacc.ROLE_SYSTEM_COMBOBOX,
						oleacc.ROLE_SYSTEM_TEXT
					],
					f"IAccessible2::state_{IA2.IA2_STATE_EDITABLE}": [1],
				},
				{
					f"IAccessible2::state_{IA2.IA2_STATE_EDITABLE}": [1],
					f"parent::IAccessible2::state_{IA2.IA2_STATE_EDITABLE}": [None],
				},
			]
		elif nodeType=="list":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LIST]}
		elif nodeType=="listItem":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LISTITEM]}
		elif nodeType=="button":
			attrs = {
				"IAccessible::role": [
					oleacc.ROLE_SYSTEM_PUSHBUTTON,
					oleacc.ROLE_SYSTEM_BUTTONMENU,
					IA2.IA2_ROLE_TOGGLE_BUTTON
				]
			}
		elif nodeType=="edit":
			attrs=[
				{
					"IAccessible::role": [oleacc.ROLE_SYSTEM_TEXT],
					f"IAccessible2::state_{IA2.IA2_STATE_EDITABLE}":[1]
				},
				{
					f"IAccessible2::state_{IA2.IA2_STATE_EDITABLE}": [1],
					f"parent::IAccessible2::state_{IA2.IA2_STATE_EDITABLE}":[None]
				},
			]
		elif nodeType=="frame":
			attrs = {"IAccessible::role": [IA2.IA2_ROLE_INTERNAL_FRAME]}
		elif nodeType=="separator":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_SEPARATOR]}
		elif nodeType=="radioButton":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_RADIOBUTTON]}
		elif nodeType=="comboBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_COMBOBOX]}
		elif nodeType=="checkBox":
			attrs = [
				{"IAccessible::role": [oleacc.ROLE_SYSTEM_CHECKBUTTON]},
				{"IAccessible2::attribute_xml-roles": [VBufStorage_findMatch_word("switch")]},
			]
		elif nodeType=="graphic":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_GRAPHIC]}
		elif nodeType=="blockQuote":
			attrs=[
				# Search for a tag of blockquote for older implementations before the blockquote IAccessible2 role existed.
				{"IAccessible2::attribute_tag":self._searchableTagValues(["blockquote"])},
				# Also support the new blockquote IAccessible2 role
				{"IAccessible::role": [IA2.IA2_ROLE_BLOCK_QUOTE]},
			]
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="landmark":
			attrs = [
				{"IAccessible::role": [IA2.IA2_ROLE_LANDMARK]},
				{"IAccessible2::attribute_xml-roles": [VBufStorage_findMatch_word(lr) for lr in aria.landmarkRoles]},
				{"IAccessible2::attribute_xml-roles": [VBufStorage_findMatch_word("region")],
					"name": [VBufStorage_findMatch_notEmpty]}
				]
		elif nodeType == "article":
			attrs = [
				{"IAccessible2::attribute_xml-roles": [VBufStorage_findMatch_word("article")]}
			]
		elif nodeType == "grouping":
			attrs = [
				{
					"IAccessible2::attribute_xml-roles": [
						VBufStorage_findMatch_word(r) for r in ("group", "radiogroup")
					],
					"name": [VBufStorage_findMatch_notEmpty]
				},
				{
					"IAccessible2::attribute_tag": self._searchableTagValues(["fieldset"]),
					"name": [VBufStorage_findMatch_notEmpty]
				},
			]
		elif nodeType=="embeddedObject":
			attrs=[
				{
					"IAccessible2::attribute_tag":
					self._searchableTagValues(["embed", "object", "applet", "audio", "video", "figure"])
				},
				{"IAccessible::role":[oleacc.ROLE_SYSTEM_APPLICATION,oleacc.ROLE_SYSTEM_DIALOG]},
			]
		elif nodeType == "tab":
			attrs = [
				{"IAccessible::role": [oleacc.ROLE_SYSTEM_PAGETAB]}
			]
		else:
			return None
		return attrs

	def event_stateChange(self,obj,nextHandler):
		if not self.isAlive:
			return treeInterceptorHandler.killTreeInterceptor(self)
		return nextHandler()

	def event_scrollingStart(self, obj, nextHandler):
		if not self.isReady:
			self._initialScrollObj = obj
			return nextHandler()
		if not self._handleScrollTo(obj):
			return nextHandler()
	event_scrollingStart.ignoreIsReady = True

	def _getTableCellAt(self,tableID,startPos,destRow,destCol):
		docHandle = self.rootDocHandle
		table = self.getNVDAObjectFromIdentifier(docHandle, tableID)
		try:
			try:
				cell = table.IAccessibleTable2Object.cellAt(destRow - 1, destCol - 1).QueryInterface(IAccessible2)
			except AttributeError:
				cell = table.IAccessibleTableObject.accessibleAt(destRow - 1, destCol - 1).QueryInterface(IAccessible2)
			cell = NVDAObjects.IAccessible.IAccessible(IAccessibleObject=cell, IAccessibleChildID=0)
			if cell.IA2Attributes.get('hidden'):
				raise LookupError("Found hidden cell") 
			return self.makeTextInfo(cell)
		except (COMError, RuntimeError):
			raise LookupError

	def _getNearestTableCell(
			self,
			startPos: textInfos.TextInfo,
			cell: documentBase._TableCell,
			movement: documentBase._Movement,
			axis: documentBase._Axis,
	) -> textInfos.TextInfo:
		# Skip the VirtualBuffer implementation as the base BrowseMode implementation is good enough for us here.
		return super(VirtualBuffer, self)._getNearestTableCell(startPos, cell, movement, axis)

	def _get_documentConstantIdentifier(self):
		try:
			return self.rootNVDAObject.IAccessibleObject.accValue(0)
		except COMError:
			return None

	def _getInitialCaretPos(self):
		initialPos = super(Gecko_ia2,self)._getInitialCaretPos()
		if initialPos:
			return initialPos
		return self._initialScrollObj
	
	def _getStartSelection(self, ia2Sel: "_Ia2Selection", selFields: TextInfo.TextWithFieldsT):
		"""Get the start of the selection.

		:param ia2Sel: Selection object to update.
		:param selFields: List of fields in the selection.
		:raises NotImplementedError: If the start of the selection could not be found.
		AssertionError: If the start object query interface failed.
		"""
		# Locate the start of the selection by walking through the fields.
		# Until we find the deepest field with IAccessibleText information.
		# It may be on a formatChange which represents a text attribute run,
		# or on a controlStart which represents an embeded object within text,
		# Where we have not included its inner text attribute run
		# as the content was overridden by an ARIA label or similar.
		for field in selFields:
			if isinstance(field, textInfos.FieldCommand):
				if field.command in ("controlStart", "formatChange"):
					hwnd = field.field.get('ia2TextWindowHandle')
					if hwnd is not None:
						ia2Sel.startWindow = hwnd
						ia2Sel.startID = field.field['ia2TextUniqueID']
						ia2Sel.startOffset = field.field['ia2TextStartOffset']
						if field.command == "formatChange":
							ia2Sel.startOffset += field.field.get('strippedCharsFromStart', 0)
							ia2Sel.startOffset += field.field['_offsetFromStartOfNode']
					if field.command == "controlStart":
						continue
			break
		if ia2Sel.startOffset is None:
			raise NotImplementedError("No ia2TextStartOffset in any field")
		log.debug(f"ia2 start window: {ia2Sel.startWindow}")
		log.debug(f"ia2 start ID: {ia2Sel.startID}")
		log.debug(f"ia2 start offset: {ia2Sel.startOffset}")
		ia2Sel.startObj, childID = IAccessibleHandler.accessibleObjectFromEvent(
			ia2Sel.startWindow, winUser.OBJID_CLIENT, ia2Sel.startID
		)
		assert (childID == 0), "childID should be 0"
		ia2Sel.startObj = ia2Sel.startObj.QueryInterface(IAccessibleText)
		log.debug(f"ia2 start obj: {ia2Sel.startObj}")

	def _getEndSelection(self, ia2Sel: "_Ia2Selection", selFields: TextInfo.TextWithFieldsT):
		"""Get the end of the selection.

		:param ia2Sel: Selection object to update.
		:param selFields: List of fields in the selection.
		:raises NotImplementedError: If the end of the selection could not be found.
		AssertionError: If the end object query interface failed.
		"""
		textLen = 0
		# Locate the end of the selection by walking through the fields in reverse,
		# similar to how we located the start of the selection.
		for field in reversed(selFields):
			if isinstance(field, str):
				textLen = len(field)
				continue
			elif isinstance(field, textInfos.FieldCommand):
				if field.command in ("controlEnd", "formatChange"):
					hwnd = field.field.get('ia2TextWindowHandle')
					if hwnd is not None:
						ia2Sel.endWindow = hwnd
						ia2Sel.endID = field.field['ia2TextUniqueID']
						ia2Sel.endOffset = field.field['ia2TextStartOffset']
						if field.command == "controlEnd":
							ia2Sel.endOffset += 1
						elif field.command == "formatChange":
							ia2Sel.endOffset += field.field.get('strippedCharsFromStart', 0)
							ia2Sel.endOffset += field.field['_offsetFromStartOfNode']
							ia2Sel.endOffset += textLen
				if field.command == "controlEnd":
					continue
			break
		if ia2Sel.endOffset is None:
			raise NotImplementedError("No ia2TextEndOffset in any field")
		log.debug(f"ia2 end window: {repr(ia2Sel.endWindow)}")
		log.debug(f"ia2 end ID: {repr(ia2Sel.endID)}")
		log.debug(f"ia2 end offset: {ia2Sel.endOffset}")
		if ia2Sel.endID == ia2Sel.startID:
			ia2Sel.endObj = ia2Sel.startObj
			log.debug("Reusing ia2Sel.startObj for ia2Sel.endObj")
		else:
			ia2Sel.endObj, childID = IAccessibleHandler.accessibleObjectFromEvent(
				ia2Sel.endWindow, winUser.OBJID_CLIENT, ia2Sel.endID
			)
			assert (childID == 0), "childID should be 0"
			ia2Sel.endObj = ia2Sel.endObj.QueryInterface(IAccessibleText)
			log.debug(f"ia2 end obj {ia2Sel.endObj}")

	def updateAppSelection(self):
		"""Update the native selection in the application to match the browse mode selection in NVDA."""
		try:
			paccTextSelectionContainer = self.rootNVDAObject.IAccessibleObject.QueryInterface(
				IAccessibleTextSelectionContainer
			)
		except COMError as e:
			raise NotImplementedError from e
		selInfo = self.makeTextInfo(textInfos.POSITION_SELECTION)
		selFields = selInfo.getTextWithFields()
		ia2Sel = _Ia2Selection()

		log.debug("checking fields...")
		self._getStartSelection(ia2Sel, selFields)
		self._getEndSelection(ia2Sel, selFields)

		log.debug("setting selection...")
		r = IA2TextSelection(
			ia2Sel.startObj,
			ia2Sel.startOffset,
			ia2Sel.endObj,
			ia2Sel.endOffset,
			False
		)
		paccTextSelectionContainer.SetSelections(1, byref(r))

	def clearAppSelection(self):
		"""Clear the native selection in the application."""
		try:
			paccTextSelectionContainer = self.rootNVDAObject.IAccessibleObject.QueryInterface(
				IAccessibleTextSelectionContainer
			)
		except COMError as e:
			raise NotImplementedError from e
		r = IA2TextSelection(None, 0, None, 0, False)
		paccTextSelectionContainer.SetSelections(0, byref(r))


@dataclass
class _Ia2Selection:
	startObj: IA2.IAccessible2 | None = None
	startWindow: int | None = None
	startID: int | None = None
	startOffset: int | None = None
	endObj: IA2.IAccessible2 | None = None
	endWindow: int | None = None
	endID: int | None = None
	endOffset: int | None = None
