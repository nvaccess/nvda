#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2014 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import itertools
import collections
import wx
import nvwave
import queueHandler
import gui
from scriptHandler import isScriptWaiting, willSayAllResume
import controlTypes
import config
import textInfos
import speech
import sayAllHandler
import treeInterceptorHandler

REASON_QUICKNAV = "quickNav"

def reportPassThrough(treeInterceptor,onlyIfChanged=True):
	"""Reports the virtual buffer pass through mode if it has changed.
	@param treeInterceptor: The current Browse Mode treeInterceptor.
	@type treeInterceptor: L{BrowseModeTreeInterceptor}
	@param onlyIfChanged: if true reporting will not happen if the last reportPassThrough reported the same thing.
	@type onlyIfChanged: bool
	"""
	if not onlyIfChanged or treeInterceptor.passThrough != reportPassThrough.last:
		if config.conf["virtualBuffers"]["passThroughAudioIndication"]:
			sound = r"waves\focusMode.wav" if treeInterceptor.passThrough else r"waves\browseMode.wav"
			nvwave.playWaveFile(sound)
		else:
			if treeInterceptor.passThrough:
				speech.speakMessage(_("focus mode"))
			else:
				speech.speakMessage(_("browse mode"))
		reportPassThrough.last = treeInterceptor.passThrough
reportPassThrough.last = False

class QuickNavItem(object):

	itemType=None
	label=None
	isAfterSelection=False

	def __init__(self,itemType,document):
		self.itemType=itemType
		self.document=document

	def isChild(self,parent):
		raise NotImplementedError

	def moveTo(self,gesture=None,readUnit=None,cancelSpeech=False):
		raise NotImplementedError

	canActivate=False
	def activate(self):
		raise NotImplementedError

class TextInfoQuickNavItem(QuickNavItem):

	def __init__(self,itemType,document,textInfo):
		self.textInfo=textInfo
		super(TextInfoQuickNavItem,self).__init__(itemType,document)

	@property
	def label(self):
		return self.textInfo.text.strip()

	def activate(self):
		self.textInfo.activate()

	def isChild(self,parent):
		if parent.textInfo.isOverlapping(self.textInfo):
			return True
		return False

	def moveTo(self,gesture=None,readUnit=None,cancelSpeech=False):
		info=self.textInfo
		if not willSayAllResume(gesture):
			if cancelSpeech:
				speech.cancelSpeech()
			if readUnit:
				fieldInfo = info.copy()
				info.collapse()
				info.move(readUnit, 1, endPoint="end")
				if info.compareEndPoints(fieldInfo, "endToEnd") > 0:
					# We've expanded past the end of the field, so limit to the end of the field.
					info.setEndPoint(fieldInfo, "endToEnd")
			speech.speakTextInfo(info, reason=controlTypes.REASON_FOCUS)
		info.collapse()
		self.document.selection=info

	@property
	def isAfterSelection(self):
		caret=self.document.makeTextInfo(textInfos.POSITION_CARET)
		return self.textInfo.compareEndPoints(caret, "startToStart") <= 0

class BrowseModeTreeInterceptor(treeInterceptorHandler.TreeInterceptor):

	def _iterNodesByType(self,itemType,direction="next",pos=None):
		return iter(())

	def _quickNavScript(self,gesture, itemType, direction, errorMessage, readUnit):
		info=self.selection
		try:
			item = next(self._iterNodesByType(itemType, direction, info))
		except StopIteration:
			speech.speakMessage(errorMessage)
			return
		item.moveTo(gesture=gesture,readUnit=readUnit)

	@classmethod
	def addQuickNav(cls, itemType, key, nextDoc, nextError, prevDoc, prevError, readUnit=None):
		scriptSuffix = itemType[0].upper() + itemType[1:]
		scriptName = "next%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,gesture: self._quickNavScript(gesture, itemType, "next", nextError, readUnit)
		script.__doc__ = nextDoc
		script.__name__ = funcName
		script.resumeSayAllMode=sayAllHandler.CURSOR_CARET
		setattr(cls, funcName, script)
		cls.__gestures["kb:%s" % key] = scriptName
		scriptName = "previous%s" % scriptSuffix
		funcName = "script_%s" % scriptName
		script = lambda self,gesture: self._quickNavScript(gesture, itemType, "previous", prevError, readUnit)
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

	def _activatePosition(self,info):
		info.activate()

	def script_activatePosition(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		self._activatePosition(info)
	# Translators: the description for the activatePosition script on virtualBuffers.
	script_activatePosition.__doc__ = _("activates the current object in the document")

	__gestures={
		"kb:NVDA+f7": "elementsList",
		"kb:enter": "activatePosition",
		"kb:space": "activatePosition",
	}

# Add quick navigation scripts.
qn = BrowseModeTreeInterceptor.addQuickNav
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

	Element = collections.namedtuple("Element", ("item", "parent"))

	lastSelectedElementType=0

	def __init__(self, document):
		self.document = document
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
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

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

		caret = self.document.makeTextInfo(textInfos.POSITION_CARET)
		caret.expand("character")

		parentElements = []
		for item in self.document._iterNodesByType(elType):
			# Find the parent element, if any.
			for parent in reversed(parentElements):
				if item.isChild(parent.item):
					break
				else:
					# We're not a child of this parent, so this parent has no more children and can be removed from the stack.
					parentElements.pop()
			else:
				# No parent found, so we're at the root.
				# Note that parentElements will be empty at this point, as all parents are no longer relevant and have thus been removed from the stack.
				parent = None

			element=self.Element(item,parent)
			self._elements.append(element)

			if item.isAfterSelection:
				# The element immediately preceding or overlapping the caret should be the initially selected element.
				# This element immediately follows the caret, so we want the previous element.
				try:
					self._initialElement = self._elements[-1]
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
			if filterText not in element.item.label.lower():
				item = None
				continue
			matched = True
			parent = element.parent
			if parent:
				parent = elementsToTreeItems.get(parent)
			item = self.tree.AppendItem(parent or self.treeRoot, element.item.label)
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
		item = self.tree.GetItemPyData(item).item
		if activate:
			item.activate()
		else:
			wx.CallLater(100, item.moveTo,cancelSpeech=True)
