# -*- coding: UTF-8 -*-
#virtualBuffers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2012 NV Access Limited, Peter Vágner

import time
import threading
import ctypes
import collections
import itertools
import weakref
import wx
import review
import NVDAHelper
import XMLFormatting
import scriptHandler
from scriptHandler import isScriptWaiting, willSayAllResume
import speech
import NVDAObjects
import api
import sayAllHandler
import controlTypes
import textInfos.offsets
import config
import cursorManager
import gui
import eventHandler
import braille
import queueHandler
from logHandler import log
import ui
import aria
import nvwave
import treeInterceptorHandler
import watchdog

VBufStorage_findDirection_forward=0
VBufStorage_findDirection_back=1
VBufStorage_findDirection_up=2
VBufRemote_nodeHandle_t=ctypes.c_ulonglong


class VBufStorage_findMatch_word(unicode):
	pass

FINDBYATTRIBS_ESCAPE_TABLE = {
	# Symbols that are escaped in the attributes string.
	ord(u":"): ur"\\:",
	ord(u";"): ur"\\;",
	ord(u"\\"): u"\\\\\\\\",
}
# Symbols that must be escaped for a regular expression.
FINDBYATTRIBS_ESCAPE_TABLE.update({(ord(s), u"\\" + s) for s in u"^$.*+?()[]{}|"})
def _prepareForFindByAttributes(attribs):
	escape = lambda text: unicode(text).translate(FINDBYATTRIBS_ESCAPE_TABLE)
	reqAttrs = []
	regexp = []
	if isinstance(attribs, dict):
		# Single option.
		attribs = (attribs,)
	# All options will match against all requested attributes,
	# so first build the list of requested attributes.
	for option in attribs:
		for name in option:
			reqAttrs.append(unicode(name))
	# Now build the regular expression.
	for option in attribs:
		optRegexp = []
		for name in reqAttrs:
			optRegexp.append("%s:" % escape(name))
			values = option.get(name)
			if not values:
				# The value isn't tested for this attribute, so match any value.
				optRegexp.append(r"(?:\\;|[^;])+;")
			elif values[0] is None:
				# There must be no value for this attribute.
				optRegexp.append(r";")
			elif isinstance(values[0], VBufStorage_findMatch_word):
				# Assume all are word matches.
				optRegexp.append(r"(?:\\;|[^;])*\b(?:")
				optRegexp.append("|".join(escape(val) for val in values))
				optRegexp.append(r")\b(?:\\;|[^;])*;")
			else:
				# Assume all are exact matches.
				optRegexp.append("(?:")
				optRegexp.append("|".join(escape(val) for val in values))
				optRegexp.append(");")
		regexp.append("".join(optRegexp))
	return u" ".join(reqAttrs), u"|".join(regexp)

class VirtualBufferTextInfo(textInfos.offsets.OffsetsTextInfo):

	allowMoveToOffsetPastEnd=False #: no need for end insertion point as vbuf is not editable. 

	UNIT_CONTROLFIELD = "controlField"

	def _getFieldIdentifierFromOffset(self, offset):
		startOffset = ctypes.c_int()
		endOffset = ctypes.c_int()
		docHandle = ctypes.c_int()
		ID = ctypes.c_int()
		node=VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_locateControlFieldNodeAtOffset(self.obj.VBufHandle, offset, ctypes.byref(startOffset), ctypes.byref(endOffset), ctypes.byref(docHandle), ctypes.byref(ID),ctypes.byref(node))
		return docHandle.value, ID.value

	def _getOffsetsFromFieldIdentifier(self, docHandle, ID):
		node=VBufRemote_nodeHandle_t()
		NVDAHelper.localLib.VBuf_getControlFieldNodeWithIdentifier(self.obj.VBufHandle, docHandle, ID,ctypes.byref(node))
		if not node:
			raise LookupError
		start = ctypes.c_int()
		end = ctypes.c_int()
		NVDAHelper.localLib.VBuf_getFieldNodeOffsets(self.obj.VBufHandle, node, ctypes.byref(start), ctypes.byref(end))
		return start.value, end.value

	def _getPointFromOffset(self,offset):
		o = self._getNVDAObjectFromOffset(offset)
		left, top, width, height = o.location
		return textInfos.Point(left + width / 2, top + height / 2)

	def _getNVDAObjectFromOffset(self,offset):
		docHandle,ID=self._getFieldIdentifierFromOffset(offset)
		return self.obj.getNVDAObjectFromIdentifier(docHandle,ID)

	def _getOffsetsFromNVDAObjectInBuffer(self,obj):
		docHandle,ID=self.obj.getIdentifierFromNVDAObject(obj)
		return self._getOffsetsFromFieldIdentifier(docHandle,ID)

	def _getOffsetsFromNVDAObject(self, obj):
		while True:
			try:
				return self._getOffsetsFromNVDAObjectInBuffer(obj)
			except LookupError:
				pass
			# Interactive list/combo box/tree view descendants aren't rendered into the buffer, even though they are still considered part of it.
			# Use the container in this case.
			obj = obj.parent
			if not obj or obj.role not in (controlTypes.ROLE_LIST, controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_GROUPING, controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_TREEVIEWITEM):
				break
		raise LookupError

	def __init__(self,obj,position):
		self.obj=obj
		super(VirtualBufferTextInfo,self).__init__(obj,position)

	def _getSelectionOffsets(self):
		start=ctypes.c_int()
		end=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getSelectionOffsets(self.obj.VBufHandle,ctypes.byref(start),ctypes.byref(end))
		return start.value,end.value

	def _setSelectionOffsets(self,start,end):
		NVDAHelper.localLib.VBuf_setSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return NVDAHelper.localLib.VBuf_getTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		if start==end:
			return u""
		return NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle,start,end,False) or u""

	def getTextWithFields(self,formatConfig=None):
		start=self._startOffset
		end=self._endOffset
		if start==end:
			return ""
		text=NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle,start,end,True)
		if not text:
			return ""
		commandList=XMLFormatting.XMLTextParser().parse(text)
		for index in xrange(len(commandList)):
			if isinstance(commandList[index],textInfos.FieldCommand):
				field=commandList[index].field
				if isinstance(field,textInfos.ControlField):
					commandList[index].field=self._normalizeControlField(field)
				elif isinstance(field,textInfos.FormatField):
					commandList[index].field=self._normalizeFormatField(field)
		return commandList

	def _getWordOffsets(self,offset):
		#Use VBuf_getBufferLineOffsets with out screen layout to find out the range of the current field
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(self.obj.VBufHandle,offset,0,False,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		word_startOffset,word_endOffset=super(VirtualBufferTextInfo,self)._getWordOffsets(offset)
		return (max(lineStart.value,word_startOffset),min(lineEnd.value,word_endOffset))

	def _getLineOffsets(self,offset):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(self.obj.VBufHandle,offset,config.conf["virtualBuffers"]["maxLineLength"],config.conf["virtualBuffers"]["useScreenLayout"],ctypes.byref(lineStart),ctypes.byref(lineEnd))
		return lineStart.value,lineEnd.value
 
	def _getParagraphOffsets(self,offset):
		lineStart=ctypes.c_int()
		lineEnd=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getLineOffsets(self.obj.VBufHandle,offset,0,True,ctypes.byref(lineStart),ctypes.byref(lineEnd))
		return lineStart.value,lineEnd.value

	def _normalizeControlField(self,attrs):
		tableLayout=attrs.get('table-layout')
		if tableLayout:
			attrs['table-layout']=tableLayout=="1"

		isHidden=attrs.get('isHidden')
		if isHidden:
			attrs['isHidden']=isHidden=="1"

		# Handle table row and column headers.
		for axis in "row", "column":
			attr = attrs.pop("table-%sheadercells" % axis, None)
			if not attr:
				continue
			cellIdentifiers = [identifier.split(",") for identifier in attr.split(";") if identifier]
			# Get the text for the header cells.
			textList = []
			for docHandle, ID in cellIdentifiers:
				try:
					start, end = self._getOffsetsFromFieldIdentifier(int(docHandle), int(ID))
				except (LookupError, ValueError):
					continue
				textList.append(self.obj.makeTextInfo(textInfos.offsets.Offsets(start, end)).text)
			attrs["table-%sheadertext" % axis] = "\n".join(textList)

		if attrs.get("landmark") == "region" and not attrs.get("name"):
			# We only consider region to be a landmark if it has a name.
			del attrs["landmark"]

		return attrs

	def _normalizeFormatField(self, attrs):
		return attrs

	def _getLineNumFromOffset(self, offset):
		return None

	def _get_fieldIdentifierAtStart(self):
		return self._getFieldIdentifierFromOffset( self._startOffset)

	def _getUnitOffsets(self, unit, offset):
		if unit == self.UNIT_CONTROLFIELD:
			startOffset=ctypes.c_int()
			endOffset=ctypes.c_int()
			docHandle=ctypes.c_int()
			ID=ctypes.c_int()
			node=VBufRemote_nodeHandle_t()
			NVDAHelper.localLib.VBuf_locateControlFieldNodeAtOffset(self.obj.VBufHandle,offset,ctypes.byref(startOffset),ctypes.byref(endOffset),ctypes.byref(docHandle),ctypes.byref(ID),ctypes.byref(node))
			return startOffset.value,endOffset.value
		return super(VirtualBufferTextInfo, self)._getUnitOffsets(unit, offset)

	def _get_clipboardText(self):
		# Blocks should start on a new line, but they don't necessarily have an end of line indicator.
		# Therefore, get the text in block (paragraph) chunks and join the chunks with \r\n.
		blocks = (block.strip("\r\n") for block in self.getTextInChunks(textInfos.UNIT_PARAGRAPH))
		return "\r\n".join(blocks)

	def getControlFieldSpeech(self, attrs, ancestorAttrs, fieldType, formatConfig=None, extraDetail=False, reason=None):
		textList = []
		landmark = attrs.get("landmark")
		if formatConfig["reportLandmarks"] and fieldType == "start_addedToControlFieldStack" and landmark:
			try:
				textList.append(attrs["name"])
			except KeyError:
				pass
			if landmark == "region":
				# The word landmark is superfluous for regions.
				textList.append(aria.landmarkRoles[landmark])
			else:
				textList.append(_("%s landmark") % aria.landmarkRoles[landmark])
		textList.append(super(VirtualBufferTextInfo, self).getControlFieldSpeech(attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason))
		return " ".join(textList)

	def getControlFieldBraille(self, field, ancestors, reportStart, formatConfig):
		textList = []
		landmark = field.get("landmark")
		if formatConfig["reportLandmarks"] and reportStart and landmark and field.get("_startOfNode"):
			try:
				textList.append(field["name"])
			except KeyError:
				pass
			if landmark == "region":
				# The word landmark is superfluous for regions.
				textList.append(aria.landmarkRoles[landmark])
			else:
				# Translators: This is spoken and brailled to indicate a landmark (example output: main landmark).
				textList.append(_("%s landmark") % aria.landmarkRoles[landmark])
		text = super(VirtualBufferTextInfo, self).getControlFieldBraille(field, ancestors, reportStart, formatConfig)
		if text:
			textList.append(text)
		return " ".join(textList)

	def _get_focusableNVDAObjectAtStart(self):
		try:
			newNode, newStart, newEnd = next(self.obj._iterNodesByType("focusable", "up", self._startOffset))
		except StopIteration:
			return self.obj.rootNVDAObject
		if not newNode:
			return self.obj.rootNVDAObject
		docHandle=ctypes.c_int()
		ID=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getIdentifierFromControlFieldNode(self.obj.VBufHandle, newNode, ctypes.byref(docHandle), ctypes.byref(ID))
		return self.obj.getNVDAObjectFromIdentifier(docHandle.value,ID.value)

	def activate(self):
		self.obj._activatePosition(self)

class ElementsListDialog(wx.Dialog):
	ELEMENT_TYPES = (
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("link", _("Lin&ks")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("heading", _("&Headings")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("landmark", _("Lan&dmarks")),
	)
	Element = collections.namedtuple("Element", ("textInfo", "docHandle", "id", "text", "parent"))

	lastSelectedElementType=0

	def __init__(self, vbuf):
		self.vbuf = vbuf
		# Translators: The title of the browse mode Elements List dialog.
		super(ElementsListDialog, self).__init__(gui.mainFrame, wx.ID_ANY, _("Elements List"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: The label of a group of radio buttons to select the type of element
		# in the browse mode Elements List dialog.
		child = wx.RadioBox(self, wx.ID_ANY, label=_("Type:"), choices=tuple(et[1] for et in self.ELEMENT_TYPES))
		child.SetSelection(self.lastSelectedElementType)
		child.Bind(wx.EVT_RADIOBOX, self.onElementTypeChange)
		mainSizer.Add(child,proportion=1)

		self.tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_SINGLE)
		self.tree.Bind(wx.EVT_SET_FOCUS, self.onTreeSetFocus)
		self.tree.Bind(wx.EVT_CHAR, self.onTreeChar)
		self.treeRoot = self.tree.AddRoot("root")
		mainSizer.Add(self.tree,proportion=7,flag=wx.EXPAND)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of an editable text field to filter the elements
		# in the browse mode Elements List dialog.
		label = wx.StaticText(self, wx.ID_ANY, _("&Filter by:"))
		sizer.Add(label)
		self.filterEdit = wx.TextCtrl(self, wx.ID_ANY)
		self.filterEdit.Bind(wx.EVT_TEXT, self.onFilterEditTextChange)
		sizer.Add(self.filterEdit)
		mainSizer.Add(sizer,proportion=1)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to activate an element
		# in the browse mode Elements List dialog.
		self.activateButton = wx.Button(self, wx.ID_ANY, _("&Activate"))
		self.activateButton.Bind(wx.EVT_BUTTON, lambda evt: self.onAction(True))
		sizer.Add(self.activateButton)
		# Translators: The label of a button to move to an element
		# in the browse mode Elements List dialog.
		self.moveButton = wx.Button(self, wx.ID_ANY, _("&Move to"))
		self.moveButton.Bind(wx.EVT_BUTTON, lambda evt: self.onAction(False))
		sizer.Add(self.moveButton)
		sizer.Add(wx.Button(self, wx.ID_CANCEL))
		mainSizer.Add(sizer,proportion=1)

		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

		self.tree.SetFocus()
		self.initElementType(self.ELEMENT_TYPES[self.lastSelectedElementType][0])

	def onElementTypeChange(self, evt):
		elementType=evt.GetInt()
		# We need to make sure this gets executed after the focus event.
		# Otherwise, NVDA doesn't seem to get the event.
		queueHandler.queueFunction(queueHandler.eventQueue, self.initElementType, self.ELEMENT_TYPES[elementType][0])
		self.lastSelectedElementType=elementType

	def initElementType(self, elType):
		if elType == "link":
			# Links can be activated.
			self.activateButton.Enable()
			self.SetAffirmativeId(self.activateButton.GetId())
		else:
			# No other element type can be activated.
			self.activateButton.Disable()
			self.SetAffirmativeId(self.moveButton.GetId())

		# Gather the elements of this type.
		self._elements = []
		self._initialElement = None

		caret = self.vbuf.selection
		caret.expand("character")

		parentElements = []
		for node, start, end in self.vbuf._iterNodesByType(elType):
			docHandle = ctypes.c_int()
			id = ctypes.c_int()
			NVDAHelper.localLib.VBuf_getIdentifierFromControlFieldNode(self.vbuf.VBufHandle, node, ctypes.byref(docHandle), ctypes.byref(id))
			docHandle = docHandle.value
			id = id.value
			elInfo = self.vbuf.makeTextInfo(textInfos.offsets.Offsets(start, end))

			# Find the parent element, if any.
			for parent in reversed(parentElements):
				if self.isChildElement(elType, parent, elInfo, docHandle, id):
					break
				else:
					# We're not a child of this parent, so this parent has no more children and can be removed from the stack.
					parentElements.pop()
			else:
				# No parent found, so we're at the root.
				# Note that parentElements will be empty at this point, as all parents are no longer relevant and have thus been removed from the stack.
				parent = None

			element = self.Element(elInfo, docHandle, id,
				self.getElementText(elInfo, docHandle, id, elType), parent)
			self._elements.append(element)

			if not self._initialElement and elInfo.compareEndPoints(caret, "startToStart") > 0:
				# The element immediately preceding or overlapping the caret should be the initially selected element.
				# This element immediately follows the caret, so we want the previous element.
				try:
					self._initialElement = self._elements[-2]
				except IndexError:
					# No previous element.
					pass

			# This could be the parent of a subsequent element, so add it to the parents stack.
			parentElements.append(element)

		# Start with no filtering.
		self.filter("", newElementType=True)

	def filter(self, filterText, newElementType=False):
		# If this is a new element type, use the element nearest the cursor.
		# Otherwise, use the currently selected element.
		defaultElement = self._initialElement if newElementType else self.tree.GetItemPyData(self.tree.GetSelection())
		# Clear the tree.
		self.tree.DeleteChildren(self.treeRoot)

		# Populate the tree with elements matching the filter text.
		elementsToTreeItems = {}
		item = None
		defaultItem = None
		matched = False
		#Do case-insensitive matching by lowering both filterText and each element's text.
		filterText=filterText.lower()
		for element in self._elements:
			if filterText not in element.text.lower():
				item = None
				continue
			matched = True
			parent = element.parent
			if parent:
				parent = elementsToTreeItems.get(parent)
			item = self.tree.AppendItem(parent or self.treeRoot, element.text)
			self.tree.SetItemPyData(item, element)
			elementsToTreeItems[element] = item
			if element == defaultElement:
				defaultItem = item

		self.tree.ExpandAll()

		if not matched:
			# No items, so disable the buttons.
			self.activateButton.Disable()
			self.moveButton.Disable()
			return

		# If there's no default item, use the first item in the tree.
		self.tree.SelectItem(defaultItem or self.tree.GetFirstChild(self.treeRoot)[0])
		# Enable the button(s).
		# If the activate button isn't the default button, it is disabled for this element type and shouldn't be enabled here.
		if self.AffirmativeId == self.activateButton.Id:
			self.activateButton.Enable()
		self.moveButton.Enable()

	def _getControlFieldAttribs(self, info, docHandle, id):
		info = info.copy()
		info.expand(textInfos.UNIT_CHARACTER)
		for field in reversed(info.getTextWithFields()):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			if int(attrs["controlIdentifier_docHandle"]) == docHandle and int(attrs["controlIdentifier_ID"]) == id:
				return attrs
		raise LookupError

	def getElementText(self, elInfo, docHandle, id, elType):
		if elType == "landmark":
			attrs = self._getControlFieldAttribs(elInfo, docHandle, id)
			name = attrs.get("name", "")
			if name:
				name += " "
			return name + aria.landmarkRoles[attrs["landmark"]]

		else:
			return elInfo.text.strip()

	def isChildElement(self, elType, parent, childInfo, childDoc, childId):
		if parent.textInfo.isOverlapping(childInfo):
			return True

		elif elType == "heading":
			try:
				if (int(self._getControlFieldAttribs(childInfo, childDoc, childId)["level"])
						> int(self._getControlFieldAttribs(parent.textInfo, parent.docHandle, parent.id)["level"])):
					return True
			except (KeyError, ValueError, TypeError):
				return False

		return False

	def onTreeSetFocus(self, evt):
		# Start with no search.
		self._searchText = ""
		self._searchCallLater = None
		evt.Skip()

	def onTreeChar(self, evt):
		key = evt.KeyCode

		if key == wx.WXK_RETURN:
			# The enter key should be propagated to the dialog and thus activate the default button,
			# but this is broken (wx ticket #3725).
			# Therefore, we must catch the enter key here.
			# Activate the current default button.
			evt = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_ANY)
			button = self.FindWindowById(self.AffirmativeId)
			if button.Enabled:
				button.ProcessEvent(evt)
			else:
				wx.Bell()

		elif key >= wx.WXK_START or key == wx.WXK_BACK:
			# Non-printable character.
			self._searchText = ""
			evt.Skip()

		else:
			# Search the list.
			# We have to implement this ourselves, as tree views don't accept space as a search character.
			char = unichr(evt.UnicodeKey).lower()
			# IF the same character is typed twice, do the same search.
			if self._searchText != char:
				self._searchText += char
			if self._searchCallLater:
				self._searchCallLater.Restart()
			else:
				self._searchCallLater = wx.CallLater(1000, self._clearSearchText)
			self.search(self._searchText)

	def _clearSearchText(self):
		self._searchText = ""

	def search(self, searchText):
		item = self.tree.GetSelection()
		if not item:
			# No items.
			return

		# First try searching from the current item.
		# Failing that, search from the first item.
		items = itertools.chain(self._iterReachableTreeItemsFromItem(item), self._iterReachableTreeItemsFromItem(self.tree.GetFirstChild(self.treeRoot)[0]))
		if len(searchText) == 1:
			# If only a single character has been entered, skip (search after) the current item.
			next(items)

		for item in items:
			if self.tree.GetItemText(item).lower().startswith(searchText):
				self.tree.SelectItem(item)
				return

		# Not found.
		wx.Bell()

	def _iterReachableTreeItemsFromItem(self, item):
		while item:
			yield item

			childItem = self.tree.GetFirstChild(item)[0]
			if childItem and self.tree.IsExpanded(item):
				# Has children and is reachable, so recurse.
				for childItem in self._iterReachableTreeItemsFromItem(childItem):
					yield childItem

			item = self.tree.GetNextSibling(item)

	def onFilterEditTextChange(self, evt):
		self.filter(self.filterEdit.GetValue())
		evt.Skip()

	def onAction(self, activate):
		self.Close()
		# Save off the last selected element type on to the class so its used in initialization next time.
		self.__class__.lastSelectedElementType=self.lastSelectedElementType
		item = self.tree.GetSelection()
		element = self.tree.GetItemPyData(item).textInfo
		newCaret = element.copy()
		newCaret.collapse()
		self.vbuf.selection = newCaret

		if activate:
			self.vbuf._activatePosition(element)
		else:
			wx.CallLater(100, self._reportElement, element)

	def _reportElement(self, element):
		speech.cancelSpeech()
		speech.speakTextInfo(element,reason=controlTypes.REASON_FOCUS)

class VirtualBuffer(cursorManager.CursorManager, treeInterceptorHandler.TreeInterceptor):

	REASON_QUICKNAV = "quickNav"

	TextInfo=VirtualBufferTextInfo
	programmaticScrollMayFireEvent = False

	#: Maps root identifiers (docHandle and ID) to buffers.
	rootIdentifiers = weakref.WeakValueDictionary()

	def __init__(self,rootNVDAObject,backendName=None):
		super(VirtualBuffer,self).__init__(rootNVDAObject)
		self.backendName=backendName
		self.VBufHandle=None
		self.isLoading=False
		self.disableAutoPassThrough = False
		self.rootDocHandle,self.rootID=self.getIdentifierFromNVDAObject(self.rootNVDAObject)
		self._lastFocusObj = None
		self._hadFirstGainFocus = False
		self._lastProgrammaticScrollTime = None
		# We need to cache this because it will be unavailable once the document dies.
		self.documentConstantIdentifier = self.documentConstantIdentifier
		if not hasattr(self.rootNVDAObject.appModule, "_vbufRememberedCaretPositions"):
			self.rootNVDAObject.appModule._vbufRememberedCaretPositions = {}
		self._lastCaretPosition = None
		self.rootIdentifiers[self.rootDocHandle, self.rootID] = self
		self._enteringFromOutside = True

	def prepare(self):
		self.shouldPrepare=False
		self.loadBuffer()

	def _get_shouldPrepare(self):
		return not self.isLoading and not self.VBufHandle

	def terminate(self):
		if not self.VBufHandle:
			return

		if self.shouldRememberCaretPositionAcrossLoads and self._lastCaretPosition:
			try:
				self.rootNVDAObject.appModule._vbufRememberedCaretPositions[self.documentConstantIdentifier] = self._lastCaretPosition
			except AttributeError:
				# The app module died.
				pass

		self.unloadBuffer()

	def _get_isReady(self):
		return bool(self.VBufHandle and not self.isLoading)

	def loadBuffer(self):
		self.isLoading = True
		self._loadProgressCallLater = wx.CallLater(1000, self._loadProgress)
		threading.Thread(target=self._loadBuffer).start()

	def _loadBuffer(self):
		try:
			self.VBufHandle=NVDAHelper.localLib.VBuf_createBuffer(self.rootNVDAObject.appModule.helperLocalBindingHandle,self.rootDocHandle,self.rootID,unicode(self.backendName))
			if not self.VBufHandle:
				raise RuntimeError("Could not remotely create virtualBuffer")
		except:
			log.error("", exc_info=True)
			queueHandler.queueFunction(queueHandler.eventQueue, self._loadBufferDone, success=False)
			return
		queueHandler.queueFunction(queueHandler.eventQueue, self._loadBufferDone)

	def _loadBufferDone(self, success=True):
		self._loadProgressCallLater.Stop()
		del self._loadProgressCallLater
		self.isLoading = False
		if not success:
			self.passThrough=True
			return
		if self._hadFirstGainFocus:
			# If this buffer has already had focus once while loaded, this is a refresh.
			# Translators: Reported when a page reloads (example: after refreshing a webpage).
			speech.speakMessage(_("Refreshed"))
		if api.getFocusObject().treeInterceptor == self:
			self.event_treeInterceptor_gainFocus()

	def _loadProgress(self):
		# Translators: Reported while loading a document.
		ui.message(_("Loading document..."))

	def unloadBuffer(self):
		if self.VBufHandle is not None:
			try:
				watchdog.cancellableExecute(NVDAHelper.localLib.VBuf_destroyBuffer, ctypes.byref(ctypes.c_int(self.VBufHandle)))
			except WindowsError:
				pass
			self.VBufHandle=None

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	def isNVDAObjectPartOfLayoutTable(self,obj):
		docHandle,ID=self.getIdentifierFromNVDAObject(obj)
		ID=unicode(ID)
		info=self.makeTextInfo(obj)
		info.collapse()
		info.expand(textInfos.UNIT_CHARACTER)
		fieldCommands=[x for x in info.getTextWithFields() if isinstance(x,textInfos.FieldCommand)]
		tableLayout=None
		tableID=None
		for fieldCommand in fieldCommands:
			fieldID=fieldCommand.field.get("controlIdentifier_ID") if fieldCommand.field else None
			if fieldID==ID:
				tableLayout=fieldCommand.field.get('table-layout')
				if tableLayout is not None:
					return tableLayout
				tableID=fieldCommand.field.get('table-id')
				break
		if tableID is None:
			return False
		for fieldCommand in fieldCommands:
			fieldID=fieldCommand.field.get("controlIdentifier_ID") if fieldCommand.field else None
			if fieldID==tableID:
				tableLayout=fieldCommand.field.get('table-layout',False)
				break
		return tableLayout

 


	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		"""Retrieve an NVDAObject for a given node identifier.
		Subclasses must override this method.
		@param docHandle: The document handle.
		@type docHandle: int
		@param ID: The ID of the node.
		@type ID: int
		@return: The NVDAObject.
		@rtype: L{NVDAObjects.NVDAObject}
		"""
		raise NotImplementedError

	def getIdentifierFromNVDAObject(self,obj):
		"""Retreaves the virtualBuffer field identifier from an NVDAObject.
		@param obj: the NVDAObject to retreave the field identifier from.
		@type obj: L{NVDAObject}
		@returns: a the field identifier as a doc handle and ID paire.
		@rtype: 2-tuple.
		"""
		raise NotImplementedError

	def event_treeInterceptor_gainFocus(self):
		"""Triggered when this virtual buffer gains focus.
		This event is only fired upon entering this buffer when it was not the current buffer before.
		This is different to L{event_gainFocus}, which is fired when an object inside this buffer gains focus, even if that object is in the same buffer.
		"""
		doSayAll=False
		if not self._hadFirstGainFocus:
			# This buffer is gaining focus for the first time.
			# Fake a focus event on the focus object, as the buffer may have missed the actual focus event.
			focus = api.getFocusObject()
			self.event_gainFocus(focus, lambda: focus.event_gainFocus())
			if not self.passThrough:
				# We only set the caret position if in browse mode.
				# If in focus mode, the document must have forced the focus somewhere,
				# so we don't want to override it.
				initialPos = self._getInitialCaretPos()
				if initialPos:
					self.selection = self.makeTextInfo(initialPos)
				reportPassThrough(self)
				doSayAll=config.conf['virtualBuffers']['autoSayAllOnPageLoad']
			self._hadFirstGainFocus = True

		if not self.passThrough:
			if doSayAll:
				speech.speakObjectProperties(self.rootNVDAObject,name=True,states=True,reason=controlTypes.REASON_FOCUS)
				sayAllHandler.readText(sayAllHandler.CURSOR_CARET)
			else:
				# Speak it like we would speak focus on any other document object.
				speech.speakObject(self.rootNVDAObject, reason=controlTypes.REASON_FOCUS)
				info = self.selection
				if not info.isCollapsed:
					speech.speakSelectionMessage(_("selected %s"), info.text)
				else:
					info.expand(textInfos.UNIT_LINE)
					speech.speakTextInfo(info, reason=controlTypes.REASON_CARET, unit=textInfos.UNIT_LINE)

		reportPassThrough(self)
		braille.handler.handleGainFocus(self)

	def event_treeInterceptor_loseFocus(self):
		"""Triggered when this virtual buffer loses focus.
		This event is only fired when the focus moves to a new object which is not within this virtual buffer; i.e. upon leaving this virtual buffer.
		"""

	def event_caret(self, obj, nextHandler):
		if self.passThrough:
			nextHandler()

	def _activateNVDAObject(self, obj):
		"""Activate an object in response to a user request.
		This should generally perform the default action or click on the object.
		@param obj: The object to activate.
		@type obj: L{NVDAObjects.NVDAObject}
		"""
		obj.doAction()

	def _activateLongDesc(self,controlField):
		"""
		Activates (presents) the long description for a particular field (usually a graphic).
		@param controlField: the field who's long description should be activated. This field is guaranteed to have states containing HASLONGDESC state. 
		@type controlField: dict
		"""
		raise NotImplementedError

	def _activatePosition(self, info):
		obj = info.NVDAObjectAtStart
		if not obj:
			return
		if self.shouldPassThrough(obj):
			obj.setFocus()
			self.passThrough = True
			reportPassThrough(self)
		elif obj.role == controlTypes.ROLE_EMBEDDEDOBJECT or obj.role in self.APPLICATION_ROLES:
			obj.setFocus()
			speech.speakObject(obj, reason=controlTypes.REASON_FOCUS)
		else:
			self._activateNVDAObject(obj)

	def _set_selection(self, info, reason=controlTypes.REASON_CARET):
		super(VirtualBuffer, self)._set_selection(info)
		if isScriptWaiting() or not info.isCollapsed:
			return
		# Save the last caret position for use in terminate().
		# This must be done here because the buffer might be cleared just before terminate() is called,
		# causing the last caret position to be lost.
		caret = info.copy()
		caret.collapse()
		self._lastCaretPosition = caret.bookmark
		review.handleCaretMove(caret)
		if reason == controlTypes.REASON_FOCUS:
			focusObj = api.getFocusObject()
			if focusObj==self.rootNVDAObject:
				return
		else:
			focusObj=info.focusableNVDAObjectAtStart
			obj=info.NVDAObjectAtStart
			if not obj:
				log.debugWarning("Invalid NVDAObjectAtStart")
				return
			if obj==self.rootNVDAObject:
				return
			if focusObj and not eventHandler.isPendingEvents("gainFocus") and focusObj!=self.rootNVDAObject and focusObj != api.getFocusObject() and self._shouldSetFocusToObj(focusObj):
				focusObj.setFocus()
			obj.scrollIntoView()
			if self.programmaticScrollMayFireEvent:
				self._lastProgrammaticScrollTime = time.time()
		self.passThrough=self.shouldPassThrough(focusObj,reason=reason)
		# Queue the reporting of pass through mode so that it will be spoken after the actual content.
		queueHandler.queueFunction(queueHandler.eventQueue, reportPassThrough, self)

	def _shouldSetFocusToObj(self, obj):
		"""Determine whether an object should receive focus.
		Subclasses may extend or override this method.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		"""
		return obj.role not in self.APPLICATION_ROLES and obj.isFocusable and obj.role!=controlTypes.ROLE_EMBEDDEDOBJECT

	def script_activateLongDesc(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand("character")
		for field in reversed(info.getTextWithFields()):
			if isinstance(field,textInfos.FieldCommand) and field.command=="controlStart":
				states=field.field.get('states')
				if states and controlTypes.STATE_HASLONGDESC in states:
					self._activateLongDesc(field.field)
					break
		else:
			# Translators: the message presented when the activateLongDescription script cannot locate a long description to activate.
			ui.message(_("No long description"))
	# Translators: the description for the activateLongDescription script on virtualBuffers.
	script_activateLongDesc.__doc__=_("Shows the long description at this position if one is found.")

	def script_activatePosition(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		self._activatePosition(info)
	# Translators: the description for the activatePosition script on virtualBuffers.
	script_activatePosition.__doc__ = _("activates the current object in the document")

	def script_refreshBuffer(self,gesture):
		if scriptHandler.isScriptWaiting():
			# This script may cause subsequently queued scripts to fail, so don't execute.
			return
		self.unloadBuffer()
		self.loadBuffer()
	# Translators: the description for the refreshBuffer script on virtualBuffers.
	script_refreshBuffer.__doc__ = _("Refreshes the document content")

	def script_toggleScreenLayout(self,gesture):
		config.conf["virtualBuffers"]["useScreenLayout"]=not config.conf["virtualBuffers"]["useScreenLayout"]
		if config.conf["virtualBuffers"]["useScreenLayout"]:
			# Translators: Presented when use screen layout option is toggled.
			speech.speakMessage(_("use screen layout on"))
		else:
			# Translators: Presented when use screen layout option is toggled.
			speech.speakMessage(_("use screen layout off"))
	# Translators: the description for the toggleScreenLayout script on virtualBuffers.
	script_toggleScreenLayout.__doc__ = _("Toggles on and off if the screen layout is preserved while rendering the document content")

	def _searchableAttributesForNodeType(self,nodeType):
		pass

	def _iterNodesByType(self,nodeType,direction="next",offset=-1):
		if nodeType == "notLinkBlock":
			return self._iterNotLinkBlock(direction=direction, offset=offset)
		attribs=self._searchableAttribsForNodeType(nodeType)
		if not attribs:
			return iter(())
		return self._iterNodesByAttribs(attribs, direction, offset)

	def _iterNodesByAttribs(self, attribs, direction="next", offset=-1):
		reqAttrs, regexp = _prepareForFindByAttributes(attribs)
		startOffset=ctypes.c_int()
		endOffset=ctypes.c_int()
		if direction=="next":
			direction=VBufStorage_findDirection_forward
		elif direction=="previous":
			direction=VBufStorage_findDirection_back
		elif direction=="up":
			direction=VBufStorage_findDirection_up
		else:
			raise ValueError("unknown direction: %s"%direction)
		while True:
			try:
				node=VBufRemote_nodeHandle_t()
				NVDAHelper.localLib.VBuf_findNodeByAttributes(self.VBufHandle,offset,direction,reqAttrs,regexp,ctypes.byref(startOffset),ctypes.byref(endOffset),ctypes.byref(node))
			except:
				return
			if not node:
				return
			yield node, startOffset.value, endOffset.value
			offset=startOffset

	def _quickNavScript(self,gesture, nodeType, direction, errorMessage, readUnit):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		startOffset=info._startOffset
		endOffset=info._endOffset
		try:
			node, startOffset, endOffset = next(self._iterNodesByType(nodeType, direction, startOffset))
		except StopIteration:
			speech.speakMessage(errorMessage)
			return
		info = self.makeTextInfo(textInfos.offsets.Offsets(startOffset, endOffset))
		if not willSayAllResume(gesture):
			if readUnit:
				fieldInfo = info.copy()
				info.collapse()
				info.move(readUnit, 1, endPoint="end")
				if info.compareEndPoints(fieldInfo, "endToEnd") > 0:
					# We've expanded past the end of the field, so limit to the end of the field.
					info.setEndPoint(fieldInfo, "endToEnd")
			speech.speakTextInfo(info, reason=controlTypes.REASON_FOCUS)
		info.collapse()
		self._set_selection(info, reason=self.REASON_QUICKNAV)

	@classmethod
	def addQuickNav(cls, nodeType, key, nextDoc, nextError, prevDoc, prevError, readUnit=None):
		scriptSuffix = nodeType[0].upper() + nodeType[1:]
		scriptName = "next%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,gesture: self._quickNavScript(gesture, nodeType, "next", nextError, readUnit)
		script.__doc__ = nextDoc
		script.__name__ = funcName
		script.resumeSayAllMode=sayAllHandler.CURSOR_CARET
		setattr(cls, funcName, script)
		cls.__gestures["kb:%s" % key] = scriptName
		scriptName = "previous%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,gesture: self._quickNavScript(gesture, nodeType, "previous", prevError, readUnit)
		script.__doc__ = prevDoc
		script.__name__ = funcName
		script.resumeSayAllMode=sayAllHandler.CURSOR_CARET
		setattr(cls, funcName, script)
		cls.__gestures["kb:shift+%s" % key] = scriptName

	def script_elementsList(self,gesture):
		# We need this to be a modal dialog, but it mustn't block this script.
		def run():
			gui.mainFrame.prePopup()
			d = ElementsListDialog(self)
			d.ShowModal()
			d.Destroy()
			gui.mainFrame.postPopup()
		wx.CallAfter(run)
	# Translators: the description for the elements list dialog script on virtualBuffers.
	script_elementsList.__doc__ = _("Presents a list of links, headings or landmarks")

	def shouldPassThrough(self, obj, reason=None):
		"""Determine whether pass through mode should be enabled or disabled for a given object.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@param reason: The reason for this query; one of the output reasons, L{REASON_QUICKNAV}, or C{None} for manual pass through mode activation by the user.
		@return: C{True} if pass through mode should be enabled, C{False} if it should be disabled.
		"""
		if reason and (
			self.disableAutoPassThrough
			or (reason == controlTypes.REASON_FOCUS and not config.conf["virtualBuffers"]["autoPassThroughOnFocusChange"])
			or (reason == controlTypes.REASON_CARET and not config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"])
		):
			# This check relates to auto pass through and auto pass through is disabled, so don't change the pass through state.
			return self.passThrough
		if reason == self.REASON_QUICKNAV:
			return False
		states = obj.states
		role = obj.role
		# Menus sometimes get focus due to menuStart events even though they don't report as focused/focusable.
		if not obj.isFocusable and controlTypes.STATE_FOCUSED not in states and role != controlTypes.ROLE_POPUPMENU:
			return False
		if controlTypes.STATE_READONLY in states and role not in (controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_COMBOBOX):
			return False
		if reason == controlTypes.REASON_CARET:
			return role == controlTypes.ROLE_EDITABLETEXT or (role == controlTypes.ROLE_DOCUMENT and controlTypes.STATE_EDITABLE in states)
		if reason == controlTypes.REASON_FOCUS and role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_RADIOBUTTON, controlTypes.ROLE_TAB):
			return True
		if role in (controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_LIST, controlTypes.ROLE_SLIDER, controlTypes.ROLE_TABCONTROL, controlTypes.ROLE_MENUBAR, controlTypes.ROLE_POPUPMENU, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_SPINBUTTON, controlTypes.ROLE_TABLEROW, controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLEROWHEADER, controlTypes.ROLE_TABLECOLUMNHEADER) or controlTypes.STATE_EDITABLE in states:
			return True
		if reason == controlTypes.REASON_FOCUS:
			# If this is a focus change, pass through should be enabled for certain ancestor containers.
			while obj and obj != self.rootNVDAObject:
				if obj.role == controlTypes.ROLE_TOOLBAR:
					return True
				obj = obj.parent
		return False

	def event_caretMovementFailed(self, obj, nextHandler, gesture=None):
		if not self.passThrough or not gesture or not config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"]:
			return nextHandler()
		if gesture.mainKeyName in ("home", "end"):
			# Home, end, control+home and control+end should not disable pass through.
			return nextHandler()
		script = self.getScript(gesture)
		if not script:
			return nextHandler()

		# We've hit the edge of the focused control.
		# Therefore, move the virtual caret to the same edge of the field.
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(info.UNIT_CONTROLFIELD)
		if gesture.mainKeyName in ("leftArrow", "upArrow", "pageUp"):
			info.collapse()
		else:
			info.collapse(end=True)
			info.move(textInfos.UNIT_CHARACTER, -1)
		info.updateCaret()

		scriptHandler.queueScript(script, gesture)

	def script_disablePassThrough(self, gesture):
		if not self.passThrough or self.disableAutoPassThrough:
			return gesture.send()
		self.passThrough = False
		self.disableAutoPassThrough = False
		reportPassThrough(self)
	script_disablePassThrough.ignoreTreeInterceptorPassThrough = True

	def script_collapseOrExpandControl(self, gesture):
		oldFocus = api.getFocusObject()
		oldFocusStates = oldFocus.states
		gesture.send()
		if controlTypes.STATE_COLLAPSED in oldFocusStates:
			self.passThrough = True
		elif not self.disableAutoPassThrough:
			self.passThrough = False
		reportPassThrough(self)
	script_collapseOrExpandControl.ignoreTreeInterceptorPassThrough = True

	def _tabOverride(self, direction):
		"""Override the tab order if the virtual buffer caret is not within the currently focused node.
		This is done because many nodes are not focusable and it is thus possible for the virtual buffer caret to be unsynchronised with the focus.
		In this case, we want tab/shift+tab to move to the next/previous focusable node relative to the virtual buffer caret.
		If the virtual buffer caret is within the focused node, the tab/shift+tab key should be passed through to allow normal tab order navigation.
		Note that this method does not pass the key through itself if it is not overridden. This should be done by the calling script if C{False} is returned.
		@param direction: The direction in which to move.
		@type direction: str
		@return: C{True} if the tab order was overridden, C{False} if not.
		@rtype: bool
		"""
		focus = api.getFocusObject()
		try:
			focusInfo = self.makeTextInfo(focus)
		except:
			return False
		# We only want to override the tab order if the caret is not within the focused node.
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		#Only check that the caret is within the focus for things that ar not documents
		#As for documents we should always override
		if focus.role!=controlTypes.ROLE_DOCUMENT or controlTypes.STATE_EDITABLE in focus.states:
			# Expand to one character, as isOverlapping() doesn't yield the desired results with collapsed ranges.
			caretInfo.expand(textInfos.UNIT_CHARACTER)
			if focusInfo.isOverlapping(caretInfo):
				return False
		# If we reach here, we do want to override tab/shift+tab if possible.
		# Find the next/previous focusable node.
		try:
			newNode, newStart, newEnd = next(self._iterNodesByType("focusable", direction, caretInfo._startOffset))
		except StopIteration:
			return False
		docHandle=ctypes.c_int()
		ID=ctypes.c_int()
		NVDAHelper.localLib.VBuf_getIdentifierFromControlFieldNode(self.VBufHandle, newNode, ctypes.byref(docHandle), ctypes.byref(ID))
		obj=self.getNVDAObjectFromIdentifier(docHandle.value,ID.value)
		newInfo=self.makeTextInfo(textInfos.offsets.Offsets(newStart,newEnd))
		if obj == api.getFocusObject():
			# This node is already focused, so we need to move to and speak this node here.
			newCaret = newInfo.copy()
			newCaret.collapse()
			self._set_selection(newCaret,reason=controlTypes.REASON_FOCUS)
			if self.passThrough:
				obj.event_gainFocus()
			else:
				speech.speakTextInfo(newInfo,reason=controlTypes.REASON_FOCUS)
		else:
			# This node doesn't have the focus, so just set focus to it. The gainFocus event will handle the rest.
			obj.setFocus()
		return True

	def script_tab(self, gesture):
		if not self._tabOverride("next"):
			gesture.send()

	def script_shiftTab(self, gesture):
		if not self._tabOverride("previous"):
			gesture.send()

	def event_focusEntered(self,obj,nextHandler):
		if obj==self.rootNVDAObject:
			self._enteringFromOutside = True
		if self.passThrough:
			 nextHandler()

	def _shouldIgnoreFocus(self, obj):
		"""Determines whether focus on a given object should be ignored.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if focus on L{obj} should be ignored, C{False} otherwise.
		@rtype: bool
		"""
		return False

	def _postGainFocus(self, obj):
		"""Executed after a gainFocus within the virtual buffer.
		This will not be executed if L{event_gainFocus} determined that it should abort and call nextHandler.
		@param obj: The object that gained focus.
		@type obj: L{NVDAObjects.NVDAObject}
		"""

	def _replayFocusEnteredEvents(self):
		# We blocked the focusEntered events because we were in browse mode,
		# but now that we've switched to focus mode, we need to fire them.
		for parent in api.getFocusAncestors()[api.getFocusDifferenceLevel():]:
			try:
				parent.event_focusEntered()
			except:
				log.exception("Error executing focusEntered event: %s" % parent)

	def event_gainFocus(self, obj, nextHandler):
		enteringFromOutside=self._enteringFromOutside
		self._enteringFromOutside=False
		if not self.isReady:
			if self.passThrough:
				nextHandler()
			return
		if enteringFromOutside and not self.passThrough and self._lastFocusObj==obj:
			# We're entering the document from outside (not returning from an inside object/application; #3145)
			# and this was the last non-root node with focus, so ignore this focus event.
			# Otherwise, if the user switches away and back to this document, the cursor will jump to this node.
			# This is not ideal if the user was positioned over a node which cannot receive focus.
			return
		if obj==self.rootNVDAObject:
			if self.passThrough:
				return nextHandler()
			return 
		if not self.passThrough and self._shouldIgnoreFocus(obj):
			return
		self._lastFocusObj=obj

		try:
			focusInfo = self.makeTextInfo(obj)
		except:
			# This object is not in the virtual buffer, even though it resides beneath the document.
			# Automatic pass through should be enabled in certain circumstances where this occurs.
			if not self.passThrough and self.shouldPassThrough(obj,reason=controlTypes.REASON_FOCUS):
				self.passThrough=True
				reportPassThrough(self)
				self._replayFocusEnteredEvents()
			return nextHandler()

		#We only want to update the caret and speak the field if we're not in the same one as before
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textInfos.UNIT_CHARACTER)
		if not self._hadFirstGainFocus or not focusInfo.isOverlapping(caretInfo):
			# The virtual buffer caret is not within the focus node.
			oldPassThrough=self.passThrough
			passThrough=self.shouldPassThrough(obj,reason=controlTypes.REASON_FOCUS)
			if not oldPassThrough and (passThrough or sayAllHandler.isRunning()):
				# If pass-through is disabled, cancel speech, as a focus change should cause page reading to stop.
				# This must be done before auto-pass-through occurs, as we want to stop page reading even if pass-through will be automatically enabled by this focus change.
				speech.cancelSpeech()
			self.passThrough=passThrough
			if not self.passThrough:
				# We read the info from the buffer instead of the control itself.
				speech.speakTextInfo(focusInfo,reason=controlTypes.REASON_FOCUS)
				# However, we still want to update the speech property cache so that property changes will be spoken properly.
				speech.speakObject(obj,controlTypes.REASON_ONLYCACHE)
			else:
				if not oldPassThrough:
					self._replayFocusEnteredEvents()
				nextHandler()
			focusInfo.collapse()
			self._set_selection(focusInfo,reason=controlTypes.REASON_FOCUS)
		else:
			# The virtual buffer caret was already at the focused node.
			if not self.passThrough:
				# This focus change was caused by a virtual caret movement, so don't speak the focused node to avoid double speaking.
				# However, we still want to update the speech property cache so that property changes will be spoken properly.
				speech.speakObject(obj,controlTypes.REASON_ONLYCACHE)
			else:
				return nextHandler()

		self._postGainFocus(obj)

	event_gainFocus.ignoreIsReady=True

	def _handleScrollTo(self, obj):
		"""Handle scrolling the buffer to a given object in response to an event.
		Subclasses should call this from an event which indicates that the buffer has scrolled.
		@postcondition: The buffer caret is moved to L{obj} and the buffer content for L{obj} is reported.
		@param obj: The object to which the buffer should scroll.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if the buffer was scrolled, C{False} if not.
		@rtype: bool
		@note: If C{False} is returned, calling events should probably call their nextHandler.
		"""
		if self.programmaticScrollMayFireEvent and self._lastProgrammaticScrollTime and time.time() - self._lastProgrammaticScrollTime < 0.4:
			# This event was probably caused by this buffer's call to scrollIntoView().
			# Therefore, ignore it. Otherwise, the cursor may bounce back to the scroll point.
			# However, pretend we handled it, as we don't want it to be passed on to the object either.
			return True

		try:
			scrollInfo = self.makeTextInfo(obj)
		except:
			return False

		#We only want to update the caret and speak the field if we're not in the same one as before
		caretInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		# Expand to one character, as isOverlapping() doesn't treat, for example, (4,4) and (4,5) as overlapping.
		caretInfo.expand(textInfos.UNIT_CHARACTER)
		if not scrollInfo.isOverlapping(caretInfo):
			if scrollInfo.isCollapsed:
				scrollInfo.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(scrollInfo,reason=controlTypes.REASON_CARET)
			scrollInfo.collapse()
			self.selection = scrollInfo
			return True

		return False

	def _getTableCellCoords(self, info):
		if info.isCollapsed:
			info = info.copy()
			info.expand(textInfos.UNIT_CHARACTER)
		for field in reversed(info.getTextWithFields()):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			if "table-id" in attrs and "table-rownumber" in attrs:
				break
		else:
			raise LookupError("Not in a table cell")
		return (int(attrs["table-id"]),
			int(attrs["table-rownumber"]), int(attrs["table-columnnumber"]),
			int(attrs.get("table-rowsspanned", 1)), int(attrs.get("table-columnsspanned", 1)))

	def _iterTableCells(self, tableID, startPos=None, direction="next", row=None, column=None):
		attrs = {"table-id": [str(tableID)]}
		# row could be 0.
		if row is not None:
			attrs["table-rownumber"] = [str(row)]
		if column is not None:
			attrs["table-columnnumber"] = [str(column)]
		startPos = startPos._startOffset if startPos else -1
		results = self._iterNodesByAttribs(attrs, offset=startPos, direction=direction)
		if not startPos and not row and not column and direction == "next":
			# The first match will be the table itself, so skip it.
			next(results)
		for node, start, end in results:
			yield self.makeTextInfo(textInfos.offsets.Offsets(start, end))

	def _getNearestTableCell(self, tableID, startPos, origRow, origCol, origRowSpan, origColSpan, movement, axis):
		if not axis:
			# First or last.
			if movement == "first":
				startPos = None
				direction = "next"
			elif movement == "last":
				startPos = self.makeTextInfo(textInfos.POSITION_LAST)
				direction = "previous"
			try:
				return next(self._iterTableCells(tableID, startPos=startPos, direction=direction))
			except StopIteration:
				raise LookupError

		# Determine destination row and column.
		destRow = origRow
		destCol = origCol
		if axis == "row":
			destRow += origRowSpan if movement == "next" else -1
		elif axis == "column":
			destCol += origColSpan if movement == "next" else -1

		if destCol < 1:
			# Optimisation: We're definitely at the edge of the column.
			raise LookupError

		# Optimisation: Try searching for exact destination coordinates.
		# This won't work if they are covered by a cell spanning multiple rows/cols, but this won't be true in the majority of cases.
		try:
			return next(self._iterTableCells(tableID, row=destRow, column=destCol))
		except StopIteration:
			pass

		# Cells are grouped by row, so in most cases, we simply need to search in the right direction.
		for info in self._iterTableCells(tableID, direction=movement, startPos=startPos):
			_ignore, row, col, rowSpan, colSpan = self._getTableCellCoords(info)
			if row <= destRow < row + rowSpan and col <= destCol < col + colSpan:
				return info
			elif row > destRow and movement == "next":
				# Optimisation: We've gone forward past destRow, so we know we won't find the cell.
				# We can't reverse this logic when moving backwards because there might be a prior cell on an earlier row which spans multiple rows.
				break

		if axis == "row" or (axis == "column" and movement == "previous"):
			# In most cases, there's nothing more to try.
			raise LookupError

		else:
			# We're moving forward by column.
			# In this case, there might be a cell on an earlier row which spans multiple rows.
			# Therefore, try searching backwards.
			for info in self._iterTableCells(tableID, direction="previous", startPos=startPos):
				_ignore, row, col, rowSpan, colSpan = self._getTableCellCoords(info)
				if row <= destRow < row + rowSpan and col <= destCol < col + colSpan:
					return info
			else:
				raise LookupError

	def _tableMovementScriptHelper(self, movement="next", axis=None):
		if isScriptWaiting():
			return
		formatConfig=config.conf["documentFormatting"].copy()
		formatConfig["reportTables"]=True
		formatConfig["includeLayoutTables"]=True
		try:
			tableID, origRow, origCol, origRowSpan, origColSpan = self._getTableCellCoords(self.selection)
		except LookupError:
			# Translators: The message reported when a user attempts to use a table movement command
			# when the cursor is not within a table.
			ui.message(_("Not in a table cell"))
			return

		try:
			info = self._getNearestTableCell(tableID, self.selection, origRow, origCol, origRowSpan, origColSpan, movement, axis)
		except LookupError:
			# Translators: The message reported when a user attempts to use a table movement command
			# but the cursor can't be moved in that direction because it is at the edge of the table.
			ui.message(_("edge of table"))
			# Retrieve the cell on which we started.
			info = next(self._iterTableCells(tableID, row=origRow, column=origCol))

		speech.speakTextInfo(info,formatConfig=formatConfig,reason=controlTypes.REASON_CARET)
		info.collapse()
		self.selection = info

	def script_nextRow(self, gesture):
		self._tableMovementScriptHelper(axis="row", movement="next")
	# Translators: the description for the next table row script on virtualBuffers.
	script_nextRow.__doc__ = _("moves to the next table row")


	def script_previousRow(self, gesture):
		self._tableMovementScriptHelper(axis="row", movement="previous")
	# Translators: the description for the previous table row script on virtualBuffers.
	script_previousRow.__doc__ = _("moves to the previous table row")

	def script_nextColumn(self, gesture):
		self._tableMovementScriptHelper(axis="column", movement="next")
	# Translators: the description for the next table column script on virtualBuffers.
	script_nextColumn.__doc__ = _("moves to the next table column")

	def script_previousColumn(self, gesture):
		self._tableMovementScriptHelper(axis="column", movement="previous")
	# Translators: the description for the previous table column script on virtualBuffers.
	script_previousColumn.__doc__ = _("moves to the previous table column")

	APPLICATION_ROLES = (controlTypes.ROLE_APPLICATION, controlTypes.ROLE_DIALOG)
	def _isNVDAObjectInApplication(self, obj):
		"""Determine whether a given object is within an application.
		The object is considered to be within an application if it or one of its ancestors has an application role.
		This should only be called on objects beneath the buffer's root NVDAObject.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if L{obj} is within an application, C{False} otherwise.
		@rtype: bool
		"""
		while obj and obj != self.rootNVDAObject:
			if obj.role in self.APPLICATION_ROLES:
				return True
			obj = obj.parent
		return False

	NOT_LINK_BLOCK_MIN_LEN = 30
	def _iterNotLinkBlock(self, direction="next", offset=-1):
		links = self._iterNodesByType("link", direction=direction, offset=offset)
		# We want to compare each link against the next link.
		link1node, link1start, link1end = next(links)
		while True:
			link2node, link2start, link2end = next(links)
			# If the distance between the links is small, this is probably just a piece of non-link text within a block of links; e.g. an inactive link of a nav bar.
			if direction == "next" and link2start - link1end > self.NOT_LINK_BLOCK_MIN_LEN:
				yield 0, link1end, link2start
			# If we're moving backwards, the order of the links in the document will be reversed.
			elif direction == "previous" and link1start - link2end > self.NOT_LINK_BLOCK_MIN_LEN:
				yield 0, link2end, link1start
			link1node, link1start, link1end = link2node, link2start, link2end

	def _getInitialCaretPos(self):
		"""Retrieve the initial position of the caret after the buffer has been loaded.
		This position, if any, will be passed to L{makeTextInfo}.
		Subclasses should extend this method.
		@return: The initial position of the caret, C{None} if there isn't one.
		@rtype: TextInfo position
		"""
		if self.shouldRememberCaretPositionAcrossLoads:
			try:
				return self.rootNVDAObject.appModule._vbufRememberedCaretPositions[self.documentConstantIdentifier]
			except KeyError:
				pass
		return None

	def _get_documentConstantIdentifier(self):
		"""Get the constant identifier for this document.
		This identifier should uniquely identify all instances (not just one instance) of a document for at least the current session of the hosting application.
		Generally, the document URL should be used.
		@return: The constant identifier for this document, C{None} if there is none.
		"""
		return None

	def _get_shouldRememberCaretPositionAcrossLoads(self):
		"""Specifies whether the position of the caret should be remembered when this document is loaded again.
		This is useful when the browser remembers the scroll position for the document,
		but does not communicate this information via APIs.
		The remembered caret position is associated with this document using L{documentConstantIdentifier}.
		@return: C{True} if the caret position should be remembered, C{False} if not.
		@rtype: bool
		"""
		docConstId = self.documentConstantIdentifier
		# Return True if the URL indicates that this is probably a web browser document.
		# We do this check because we don't want to remember caret positions for email messages, etc.
		return isinstance(docConstId, basestring) and docConstId.split("://", 1)[0] in ("http", "https", "ftp", "ftps", "file")

	def getEnclosingContainerRange(self,range):
		formatConfig=config.conf['documentFormatting'].copy()
		formatConfig.update({"reportBlockQuotes":True,"reportTables":True,"reportLists":True,"reportFrames":True})
		controlFields=[]
		for cmd in range.getTextWithFields():
			if not isinstance(cmd,textInfos.FieldCommand) or cmd.command!="controlStart":
				break
			controlFields.append(cmd.field)
		containerField=None
		while controlFields:
			field=controlFields.pop()
			if field.getPresentationCategory(controlFields,formatConfig)==field.PRESCAT_CONTAINER:
				containerField=field
				break
		if not containerField: return None
		docHandle=int(containerField['controlIdentifier_docHandle'])
		ID=int(containerField['controlIdentifier_ID'])
		offsets=range._getOffsetsFromFieldIdentifier(docHandle,ID)
		return self.makeTextInfo(textInfos.offsets.Offsets(*offsets))

	def script_moveToStartOfContainer(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		container=self.getEnclosingContainerRange(info)
		if not container:
			# Translators: Reported when the user attempts to move to the start or end of a container (list, table, etc.) 
			# But there is no container. 
			ui.message(_("Not in a container"))
			return
		container.collapse()
		self._set_selection(container, reason=self.REASON_QUICKNAV)
		if not willSayAllResume(gesture):
			container.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(container, reason=controlTypes.REASON_FOCUS)
	script_moveToStartOfContainer.resumeSayAllMode=sayAllHandler.CURSOR_CARET
	# Translators: Description for the Move to start of container command in browse mode. 
	script_moveToStartOfContainer.__doc__=_("Moves to the start of the container element, such as a list or table")

	def script_movePastEndOfContainer(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		container=self.getEnclosingContainerRange(info)
		if not container:
			ui.message(_("Not in a container"))
			return
		container.collapse(end=True)
		if container._startOffset>=container._getStoryLength():
			container.move(textInfos.UNIT_CHARACTER,-1)
			# Translators: a message reported when:
			# Review cursor is at the bottom line of the current navigator object.
			# Landing at the end of a browse mode document when trying to jump to the end of the current container. 
			ui.message(_("bottom"))
		self._set_selection(container, reason=self.REASON_QUICKNAV)
		if not willSayAllResume(gesture):
			container.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(container, reason=controlTypes.REASON_FOCUS)
	script_movePastEndOfContainer.resumeSayAllMode=sayAllHandler.CURSOR_CARET
	# Translators: Description for the Move past end of container command in browse mode. 
	script_movePastEndOfContainer.__doc__=_("Moves past the end  of the container element, such as a list or table")

	@classmethod
	def changeNotify(cls, rootDocHandle, rootID):
		try:
			queueHandler.queueFunction(queueHandler.eventQueue, cls.rootIdentifiers[rootDocHandle, rootID]._handleUpdate)
		except KeyError:
			pass

	def _handleUpdate(self):
		"""Handle an update to this buffer.
		"""
		braille.handler.handleUpdate(self)

	__gestures = {
		"kb:NVDA+d": "activateLongDesc",
		"kb:enter": "activatePosition",
		"kb:space": "activatePosition",
		"kb:NVDA+f5": "refreshBuffer",
		"kb:NVDA+v": "toggleScreenLayout",
		"kb:NVDA+f7": "elementsList",
		"kb:escape": "disablePassThrough",
		"kb:alt+upArrow": "collapseOrExpandControl",
		"kb:alt+downArrow": "collapseOrExpandControl",
		"kb:tab": "tab",
		"kb:shift+tab": "shiftTab",
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+upArrow": "previousRow",
		"kb:control+alt+rightArrow": "nextColumn",
		"kb:control+alt+leftArrow": "previousColumn",
		"kb:shift+,": "moveToStartOfContainer",
		"kb:,": "movePastEndOfContainer",
	}

# Add quick navigation scripts.
qn = VirtualBuffer.addQuickNav
qn("heading", key="h",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next heading"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next heading"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous heading"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous heading"))
qn("heading1", key="1",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next heading at level 1"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next heading at level 1"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous heading at level 1"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous heading at level 1"))
qn("heading2", key="2",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next heading at level 2"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next heading at level 2"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous heading at level 2"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous heading at level 2"))
qn("heading3", key="3",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next heading at level 3"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next heading at level 3"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous heading at level 3"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous heading at level 3"))
qn("heading4", key="4",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next heading at level 4"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next heading at level 4"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous heading at level 4"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous heading at level 4"))
qn("heading5", key="5",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next heading at level 5"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next heading at level 5"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous heading at level 5"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous heading at level 5"))
qn("heading6", key="6",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next heading at level 6"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next heading at level 6"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous heading at level 6"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous heading at level 6"))
qn("table", key="t",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next table"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next table"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous table"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous table"),
	readUnit=textInfos.UNIT_LINE)
qn("link", key="k",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next link"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next link"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous link"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous link"))
qn("visitedLink", key="v",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next visited link"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next visited link"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous visited link"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous visited link"))
qn("unvisitedLink", key="u",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next unvisited link"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next unvisited link"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous unvisited link"), 
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous unvisited link"))
qn("formField", key="f",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next form field"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next form field"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous form field"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous form field"),
	readUnit=textInfos.UNIT_LINE)
qn("list", key="l",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next list"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next list"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous list"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous list"),
	readUnit=textInfos.UNIT_LINE)
qn("listItem", key="i",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next list item"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next list item"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous list item"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous list item"))
qn("button", key="b",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next button"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next button"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous button"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous button"))
qn("edit", key="e",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next edit field"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next edit field"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous edit field"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous edit field"),
	readUnit=textInfos.UNIT_LINE)
qn("frame", key="m",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next frame"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next frame"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous frame"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous frame"),
	readUnit=textInfos.UNIT_LINE)
qn("separator", key="s",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next separator"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next separator"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous separator"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous separator"))
qn("radioButton", key="r",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next radio button"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next radio button"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous radio button"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous radio button"))
qn("comboBox", key="c",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next combo box"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next combo box"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous combo box"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous combo box"))
qn("checkBox", key="x",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next check box"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next check box"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous check box"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous check box"))
qn("graphic", key="g",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next graphic"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next graphic"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous graphic"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous graphic"))
qn("blockQuote", key="q",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next block quote"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next block quote"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous block quote"), 
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous block quote"))
qn("notLinkBlock", key="n",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("skips forward past a block of links"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no more text after a block of links"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("skips backward past a block of links"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no more text before a block of links"),
	readUnit=textInfos.UNIT_LINE)
qn("landmark", key="d",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next landmark"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next landmark"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous landmark"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous landmark"),
	readUnit=textInfos.UNIT_LINE)
qn("embeddedObject", key="o",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next embedded object"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next embedded object"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous embedded object"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous embedded object"))
del qn

def reportPassThrough(virtualBuffer):
	"""Reports the virtual buffer pass through mode if it has changed.
	@param virtualBuffer: The current virtual buffer.
	@type virtualBuffer: L{virtualBuffers.VirtualBuffer}
	"""
	if virtualBuffer.passThrough != reportPassThrough.last:
		if config.conf["virtualBuffers"]["passThroughAudioIndication"]:
			sound = r"waves\focusMode.wav" if virtualBuffer.passThrough else r"waves\browseMode.wav"
			nvwave.playWaveFile(sound)
		else:
			if virtualBuffer.passThrough:
				speech.speakMessage(_("focus mode"))
			else:
				speech.speakMessage(_("browse mode"))
		reportPassThrough.last = virtualBuffer.passThrough
reportPassThrough.last = False
