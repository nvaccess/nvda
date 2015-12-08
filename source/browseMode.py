#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import itertools
import collections
import winsound
import time
import weakref
import wx
import queueHandler
from logHandler import log
import review
import scriptHandler
import eventHandler
import nvwave
import queueHandler
import gui
import ui
import cursorManager
from scriptHandler import isScriptWaiting, willSayAllResume
import aria
import controlTypes
import config
import textInfos
import braille
import speech
import sayAllHandler
import treeInterceptorHandler
import inputCore
import api
from NVDAObjects import NVDAObject

REASON_QUICKNAV = "quickNav"

def reportPassThrough(treeInterceptor,onlyIfChanged=True):
	"""Reports the pass through mode if it has changed.
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

def mergeQuickNavItemIterators(iterators,direction="next"):
	"""
	Merges multiple iterators that emit L{QuickNavItem} objects, yielding them from first to last. 
	They are sorted using min or max (__lt__ should be implemented on the L{QuickNavItem} objects).
	@param iters: the iterators you want to merge. 
	@type iters: sequence of iterators that emit L{QuicknavItem} objects.
	@param direction: the direction these iterators are searching (e.g. next, previuos)
	@type direction: string
	"""
	finder=min if direction=="next" else max
	curValues=[]
	# Populate a list with all iterators and their corisponding first value
	for it in iterators:
		try:
			val=next(it)
		except StopIteration:
			continue
		curValues.append((it,val))
	# Until all iterators have been used up,
	# Find the first (minimum or maximum) of all the values,
	# emit that, and update the list with the next available value for the iterator who's value was emitted.
	while len(curValues)>0:
		first=finder(curValues,key=lambda x: x[1])
		curValues.remove(first)
		it,val=first
		yield val
		try:
			newVal=next(it)
		except StopIteration:
			continue
		curValues.append((it,newVal))

class QuickNavItem(object):
	""" Emitted by L{BrowseModeTreeInterceptor._iterNodesByType}, this represents one of many positions in a browse mode document, based on the type of item being searched for (e.g. link, heading, table etc)."""  

	itemType=None #: The type of items searched for (e.g. link, heading, table etc) 
	label=None #: The label that should represent this item in the Elements list.
	isAfterSelection=False #: Is this item positioned after the caret in the document? Used by the elements list to plae its own selection.

	def __init__(self,itemType,document):
		"""
		@param itemType: the type that was searched for (e.g. link, heading, table etc)
		@ type itemType: string
		@ param document: the browse mode document this item is a part of.
		@type document: L{BrowseModeTreeInterceptor}
		"""
		self.itemType=itemType
		self.document=document

	def isChild(self,parent):
		"""
		Is this item a child of the given parent?
		This is used when representing items in a hierarchical tree structure, such as the Elements List.
		@param parent: the item of whom this item may be a child of.
		@type parent: L{QuickNavItem}
		@return: True if this item is a child, false otherwise.
		@rtype: bool
		"""
		raise NotImplementedError

	def report(self,readUnit=None):
		"""
		Reports the contents of this item.
		@param readUnit: the optional unit (e.g. line, paragraph) that should be used to announce the item position when moved to. If not given, then the full sise of the item is used.
		@type readUnit: a L{textInfos}.UNIT_* constant.
		"""
		raise NotImplementedError

	def moveTo(self):
		"""
		Moves the browse mode caret or focus to this item.
		"""
		raise NotImplementedError

	def activate(self):
		"""
		Activates this item's position. E.g. follows a link, presses a button etc.
		"""
		raise NotImplementedError

	def rename(self,newName):
		"""
		Renames this item with the new name.
		"""
		raise NotImplementedError

	@property
	def isRenameAllowed(self):
		return False

class TextInfoQuickNavItem(QuickNavItem):
	""" Represents a quick nav item in a browse mode document who's positions are represented by a L{textInfos.TextInfo}. """

	def __init__(self,itemType,document,textInfo):
		"""
		See L{QuickNavItem.__init__} for itemType and document argument definitions.
		@param textInfo: the textInfo position this item represents.
		@type textInfo: L{textInfos.TextInfo}
		"""
		self.textInfo=textInfo
		super(TextInfoQuickNavItem,self).__init__(itemType,document)

	def __lt__(self,other):
		return self.textInfo.compareEndPoints(other.textInfo,"startToStart")<0

	@property
	def obj(self):
		return self.textInfo.basePosition if isinstance(self.textInfo.basePosition,NVDAObject) else None

	@property
	def label(self):
		return self.textInfo.text.strip()

	def isChild(self,parent):
		if parent.textInfo.isOverlapping(self.textInfo):
			return True
		return False

	def report(self,readUnit=None):
		info=self.textInfo
		if readUnit:
			fieldInfo = info.copy()
			info.collapse()
			info.move(readUnit, 1, endPoint="end")
			if info.compareEndPoints(fieldInfo, "endToEnd") > 0:
				# We've expanded past the end of the field, so limit to the end of the field.
				info.setEndPoint(fieldInfo, "endToEnd")
		speech.speakTextInfo(info, reason=controlTypes.REASON_FOCUS)

	def activate(self):
		self.textInfo.obj._activatePosition(self.textInfo)

	def moveTo(self):
		info=self.textInfo.copy()
		info.collapse()
		self.document._set_selection(info,reason=REASON_QUICKNAV)

	@property
	def isAfterSelection(self):
		caret=self.document.makeTextInfo(textInfos.POSITION_CARET)
		return self.textInfo.compareEndPoints(caret, "startToStart") > 0

class BrowseModeTreeInterceptor(treeInterceptorHandler.TreeInterceptor):
	scriptCategory = inputCore.SCRCAT_BROWSEMODE

	def _get_shouldTrapNonCommandGestures(self):
		return config.conf['virtualBuffers']['trapNonCommandGestures']

	def script_trapNonCommandGesture(self,gesture):
		winsound.PlaySound("default",1)

	singleLetterNavEnabled=True #: Whether single letter navigation scripts should be active (true) or if these letters should fall to the application.

	def getAlternativeScript(self,gesture,script):
		if self.passThrough or not gesture.isCharacter:
			return script
		if not self.singleLetterNavEnabled:
			return None
		if not script and self.shouldTrapNonCommandGestures: 
			script=self.script_trapNonCommandGesture
		return script

	def script_toggleSingleLetterNav(self,gesture):
		if self.singleLetterNavEnabled:
			self.singleLetterNavEnabled=False
			# Translators: Reported when single letter navigation in browse mode is turned off.
			ui.message(_("Single letter navigation off"))
		else:
			self.singleLetterNavEnabled=True
			# Translators: Reported when single letter navigation in browse mode is turned on.
			ui.message(_("Single letter navigation on"))
	# Translators: the description for the toggleSingleLetterNavigation command in browse mode.
	script_toggleSingleLetterNav.__doc__=_("Toggles single letter navigation on and off. When on, single letter keys in browse mode jump to various kinds of elements on the page. When off, these keys are passed to the application")

	def _get_ElementsListDialog(self):
		return ElementsListDialog

	def _iterNodesByType(self,itemType,direction="next",pos=None):
		"""
		Yields L{QuickNavItem} objects representing the ordered positions in this document according to the type being searched for (e.g. link, heading, table etc).
		@param itemType: the type being searched for (e.g. link, heading, table etc)
		@type itemType: string
		@param direction: the direction in which to search (next, previous, up)
		@ type direction: string
		@param pos: the position in the document from where to seart the search.
		@type pos: Usually an L{textInfos.TextInfo} 
		"""
		return iter(())

	def _iterNotLinkBlock(self, direction="next", pos=None):
		raise NotImplementedError

	def _quickNavScript(self,gesture, itemType, direction, errorMessage, readUnit):
		if itemType=="notLinkBlock":
			iterFactory=self._iterNotLinkBlock
		else:
			iterFactory=lambda direction,info: self._iterNodesByType(itemType,direction,info)
		info=self.selection
		try:
			item = next(iterFactory(direction, info))
		except NotImplementedError:
			# Translators: a message when a particular quick nav command is not supported in the current document.
			ui.message(_("Not supported in this document"))
			return
		except StopIteration:
			ui.message(errorMessage)
			return
		item.moveTo()
		if not gesture or not willSayAllResume(gesture):
			item.report(readUnit=readUnit)

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
			d = self.ElementsListDialog(self)
			d.ShowModal()
			d.Destroy()
			gui.mainFrame.postPopup()
		wx.CallAfter(run)
	# Translators: the description for the Elements List command in browse mode.
	script_elementsList.__doc__ = _("Lists various types of elements in this document")

	def _activatePosition(self):
		raise NotImplementedError

	def script_activatePosition(self,gesture):
		self._activatePosition()
	# Translators: the description for the activatePosition script on browseMode documents.
	script_activatePosition.__doc__ = _("activates the current object in the document")

	__gestures={
		"kb:NVDA+f7": "elementsList",
		"kb:enter": "activatePosition",
		"kb:space": "activatePosition",
		"kb:NVDA+shift+space":"toggleSingleLetterNav",
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
qn("annotation", key="a",
	# Translators: Input help message for a quick navigation command in browse mode.
	nextDoc=_("moves to the next annotation"),
	# Translators: Message presented when the browse mode element is not found.
	nextError=_("no next annotation"),
	# Translators: Input help message for a quick navigation command in browse mode.
	prevDoc=_("moves to the previous annotation"),
	# Translators: Message presented when the browse mode element is not found.
	prevError=_("no previous annotation"))
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

		self.tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_SINGLE | wx.TR_EDIT_LABELS)
		self.tree.Bind(wx.EVT_SET_FOCUS, self.onTreeSetFocus)
		self.tree.Bind(wx.EVT_CHAR, self.onTreeChar)
		self.tree.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.onTreeLabelEditBegin)
		self.tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.onTreeLabelEditEnd)
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

		parentElements = []
		isAfterSelection=False
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

			if not isAfterSelection:
				isAfterSelection=item.isAfterSelection
				if not isAfterSelection:
					# The element immediately preceding or overlapping the caret should be the initially selected element.
					# Since we have not yet passed the selection, use this as the initial element. 
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

		elif key == wx.WXK_F2:
			item=self.tree.GetSelection()
			if item:
				selectedItemType=self.tree.GetItemPyData(item).item
				self.tree.EditLabel(item)
				evt.Skip()

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

	def onTreeLabelEditBegin(self,evt):
		item=self.tree.GetSelection()
		selectedItemType = self.tree.GetItemPyData(item).item
		if not selectedItemType.isRenameAllowed:
			evt.Veto()

	def onTreeLabelEditEnd(self,evt):
			selectedItemNewName=evt.GetLabel()
			item=self.tree.GetSelection()
			selectedItemType = self.tree.GetItemPyData(item).item
			selectedItemType.rename(selectedItemNewName)

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
			def move():
				speech.cancelSpeech()
				item.moveTo()
				item.report()
			wx.CallLater(100, move)

class BrowseModeDocumentTextInfo(textInfos.TextInfo):

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
		textList.append(super(BrowseModeDocumentTextInfo, self).getControlFieldSpeech(attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason))
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
		text = super(BrowseModeDocumentTextInfo, self).getControlFieldBraille(field, ancestors, reportStart, formatConfig)
		if text:
			textList.append(text)
		return " ".join(textList)

	def _get_focusableNVDAObjectAtStart(self):
		try:
			item = next(self.obj._iterNodesByType("focusable", "up", self))
		except StopIteration:
			return self.obj.rootNVDAObject
		if not item:
			return self.obj.rootNVDAObject
		return item.obj

class BrowseModeDocumentTreeInterceptor(cursorManager.CursorManager,BrowseModeTreeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor):

	programmaticScrollMayFireEvent = False

	def __init__(self,obj):
		super(BrowseModeDocumentTreeInterceptor,self).__init__(obj)
		self.disableAutoPassThrough = False
		self._lastProgrammaticScrollTime = None
		self.documentConstantIdentifier = self.documentConstantIdentifier
		self._lastFocusObj = None
		self._hadFirstGainFocus = False
		self._enteringFromOutside = True
		# We need to cache this because it will be unavailable once the document dies.
		if not hasattr(self.rootNVDAObject.appModule, "_browseModeRememberedCaretPositions"):
			self.rootNVDAObject.appModule._browseModeRememberedCaretPositions = {}
		self._lastCaretPosition = None
		#: True if the last caret move was due to a focus change.
		self._lastCaretMoveWasFocus = False

	def terminate(self):
		if self.shouldRememberCaretPositionAcrossLoads and self._lastCaretPosition:
			try:
				self.rootNVDAObject.appModule._browseModeRememberedCaretPositions[self.documentConstantIdentifier] = self._lastCaretPosition
			except AttributeError:
				# The app module died.
				pass

	def event_treeInterceptor_gainFocus(self):
		"""Triggered when this browse mode document gains focus.
		This event is only fired upon entering this treeInterceptor when it was not the current treeInterceptor before.
		This is different to L{event_gainFocus}, which is fired when an object inside this treeInterceptor gains focus, even if that object is in the same treeInterceptor.
		"""
		doSayAll=False
		hadFirstGainFocus=self._hadFirstGainFocus
		if not hadFirstGainFocus:
			# This treeInterceptor is gaining focus for the first time.
			# Fake a focus event on the focus object, as the treeInterceptor may have missed the actual focus event.
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
				# This includes when entering the treeInterceptor for the first time:
				if not hadFirstGainFocus:
					speech.speakObject(self.rootNVDAObject, reason=controlTypes.REASON_FOCUS)
				else:
					# And when coming in from an outside object
					# #4069 But not when coming up from a non-rendered descendant.
					ancestors=api.getFocusAncestors()
					fdl=api.getFocusDifferenceLevel()
					try:
						tl=ancestors.index(self.rootNVDAObject)
					except ValueError:
						tl=len(ancestors)
					if fdl<=tl:
						speech.speakObject(self.rootNVDAObject, reason=controlTypes.REASON_FOCUS)
				info = self.selection
				if not info.isCollapsed:
					speech.speakSelectionMessage(_("selected %s"), info.text)
				else:
					info.expand(textInfos.UNIT_LINE)
					speech.speakTextInfo(info, reason=controlTypes.REASON_CARET, unit=textInfos.UNIT_LINE)

		reportPassThrough(self)
		braille.handler.handleGainFocus(self)

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

	def _activatePosition(self, info=None):
		if not info:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		obj = info.NVDAObjectAtStart
		if not obj:
			return
		if obj.role == controlTypes.ROLE_MATH:
			import mathPres
			try:
				return mathPres.interactWithMathMl(obj.mathMl)
			except (NotImplementedError, LookupError):
				pass
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
		super(BrowseModeDocumentTreeInterceptor, self)._set_selection(info)
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
			self._lastCaretMoveWasFocus = True
			focusObj = api.getFocusObject()
			if focusObj==self.rootNVDAObject:
				return
		else:
			self._lastCaretMoveWasFocus = False
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
	# Translators: the description for the activateLongDescription script on browseMode documents.
	script_activateLongDesc.__doc__=_("Shows the long description at this position if one is found.")

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
		if reason == REASON_QUICKNAV:
			return False
		states = obj.states
		role = obj.role
		if controlTypes.STATE_EDITABLE in states and controlTypes.STATE_UNAVAILABLE not in states:
			return True
		# Menus sometimes get focus due to menuStart events even though they don't report as focused/focusable.
		if not obj.isFocusable and controlTypes.STATE_FOCUSED not in states and role != controlTypes.ROLE_POPUPMENU:
			return False
		# many controls that are read-only should not switch to passThrough. 
		# However, certain controls such as combo boxes and readonly edits are read-only but still interactive.
		# #5118: read-only ARIA grids should also be allowed (focusable table cells, rows and headers).
		if controlTypes.STATE_READONLY in states and role not in (controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_TABLEROW, controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLEROWHEADER, controlTypes.ROLE_TABLECOLUMNHEADER):
			return False
		if reason == controlTypes.REASON_FOCUS and role in (controlTypes.ROLE_LISTITEM, controlTypes.ROLE_RADIOBUTTON, controlTypes.ROLE_TAB):
			return True
		if role in (controlTypes.ROLE_COMBOBOX, controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_LIST, controlTypes.ROLE_SLIDER, controlTypes.ROLE_TABCONTROL, controlTypes.ROLE_MENUBAR, controlTypes.ROLE_POPUPMENU, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_SPINBUTTON, controlTypes.ROLE_TABLEROW, controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLEROWHEADER, controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_CHECKMENUITEM, controlTypes.ROLE_RADIOMENUITEM) or controlTypes.STATE_EDITABLE in states:
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
		"""Override the tab order if the virtual  caret is not within the currently focused node.
		This is done because many nodes are not focusable and it is thus possible for the virtual caret to be unsynchronised with the focus.
		In this case, we want tab/shift+tab to move to the next/previous focusable node relative to the virtual caret.
		If the virtual caret is within the focused node, the tab/shift+tab key should be passed through to allow normal tab order navigation.
		Note that this method does not pass the key through itself if it is not overridden. This should be done by the calling script if C{False} is returned.
		@param direction: The direction in which to move.
		@type direction: str
		@return: C{True} if the tab order was overridden, C{False} if not.
		@rtype: bool
		"""
		if self._lastCaretMoveWasFocus:
			# #5227: If the caret was last moved due to a focus change, don't override tab.
			# This ensures that tabbing behaves as expected after tabbing hits an iframe document.
			return False
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
			item = next(self._iterNodesByType("focusable", direction, caretInfo))
		except StopIteration:
			return False
		obj=item.obj
		newInfo=item.textInfo
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
		"""Executed after a gainFocus within the browseMode document.
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
			# This object is not in the treeInterceptor, even though it resides beneath the document.
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
			# The virtual caret is not within the focus node.
			oldPassThrough=self.passThrough
			passThrough=self.shouldPassThrough(obj,reason=controlTypes.REASON_FOCUS)
			if not oldPassThrough and (passThrough or sayAllHandler.isRunning()):
				# If pass-through is disabled, cancel speech, as a focus change should cause page reading to stop.
				# This must be done before auto-pass-through occurs, as we want to stop page reading even if pass-through will be automatically enabled by this focus change.
				speech.cancelSpeech()
			self.passThrough=passThrough
			if not self.passThrough:
				# We read the info from the browseMode document  instead of the control itself.
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
			# The virtual caret was already at the focused node.
			if not self.passThrough:
				# This focus change was caused by a virtual caret movement, so don't speak the focused node to avoid double speaking.
				# However, we still want to update the speech property cache so that property changes will be spoken properly.
				speech.speakObject(obj,controlTypes.REASON_ONLYCACHE)
			else:
				return nextHandler()

		self._postGainFocus(obj)

	event_gainFocus.ignoreIsReady=True

	def _handleScrollTo(self, obj):
		"""Handle scrolling the browseMode document to a given object in response to an event.
		Subclasses should call this from an event which indicates that the document has scrolled.
		@postcondition: The virtual caret is moved to L{obj} and the buffer content for L{obj} is reported.
		@param obj: The object to which the document should scroll.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if the document was scrolled, C{False} if not.
		@rtype: bool
		@note: If C{False} is returned, calling events should probably call their nextHandler.
		"""
		if self.programmaticScrollMayFireEvent and self._lastProgrammaticScrollTime and time.time() - self._lastProgrammaticScrollTime < 0.4:
			# This event was probably caused by this browseMode document's call to scrollIntoView().
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

	APPLICATION_ROLES = (controlTypes.ROLE_APPLICATION, controlTypes.ROLE_DIALOG)
	def _isNVDAObjectInApplication(self, obj):
		"""Determine whether a given object is within an application.
		The object is considered to be within an application if it or one of its ancestors has an application role.
		This should only be called on objects beneath the treeInterceptor's root NVDAObject.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if L{obj} is within an application, C{False} otherwise.
		@rtype: bool
		"""
		# We cache the result for each object we walk.
		# There can be browse mode documents within other documents and the result might be different between these,
		# so the cache must be maintained on the TreeInterceptor rather than the object itself.
		try:
			cache = self._isInAppCache
		except AttributeError:
			# Create this lazily, as this method isn't used by all browse mode implementations.
			cache = self._isInAppCache = weakref.WeakKeyDictionary()
		objs = []
		def doResult(result):
			# Cache this on descendants we've walked over.
			for obj in objs:
				cache[obj] = result
			return result

		while obj and obj != self.rootNVDAObject:
			inApp = cache.get(obj)
			if inApp is not None:
				# We found a cached result.
				return doResult(inApp)
			objs.append(obj)
			if obj.role in self.APPLICATION_ROLES:
				return doResult(True)
			# Cache container.
			container = obj.container
			obj.container = container
			obj = container
		return doResult(False)

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

	def _getInitialCaretPos(self):
		"""Retrieve the initial position of the caret after the buffer has been loaded.
		This position, if any, will be passed to L{makeTextInfo}.
		Subclasses should extend this method.
		@return: The initial position of the caret, C{None} if there isn't one.
		@rtype: TextInfo position
		"""
		if self.shouldRememberCaretPositionAcrossLoads:
			try:
				return self.rootNVDAObject.appModule._browseModeRememberedCaretPositions[self.documentConstantIdentifier]
			except KeyError:
				pass
		return None

	def getEnclosingContainerRange(self,range):
		range=range.copy()
		range.collapse()
		try:
			item = next(self._iterNodesByType("container", "up", range))
		except (NotImplementedError,StopIteration):
			return
		return item.textInfo

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
		self._set_selection(container, reason=REASON_QUICKNAV)
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
		docEnd=container.obj.makeTextInfo(textInfos.POSITION_LAST)
		if container.compareEndPoints(docEnd,"endToEnd")>=0:
			container=docEnd
			# Translators: a message reported when:
			# Review cursor is at the bottom line of the current navigator object.
			# Landing at the end of a browse mode document when trying to jump to the end of the current container. 
			ui.message(_("bottom"))
		self._set_selection(container, reason=REASON_QUICKNAV)
		if not willSayAllResume(gesture):
			container.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(container, reason=controlTypes.REASON_FOCUS)
	script_movePastEndOfContainer.resumeSayAllMode=sayAllHandler.CURSOR_CARET
	# Translators: Description for the Move past end of container command in browse mode. 
	script_movePastEndOfContainer.__doc__=_("Moves past the end  of the container element, such as a list or table")

	NOT_LINK_BLOCK_MIN_LEN = 30
	def _isSuitableNotLinkBlock(self,range):
		return len(range.text)>=self.NOT_LINK_BLOCK_MIN_LEN

	def _iterNotLinkBlock(self, direction="next", pos=None):
		links = self._iterNodesByType("link", direction=direction, pos=pos)
		# We want to compare each link against the next link.
		item1 = next(links)
		while True:
			item2 = next(links)
			# If the distance between the links is small, this is probably just a piece of non-link text within a block of links; e.g. an inactive link of a nav bar.
			if direction=="previous":
				range=item1.textInfo.copy()
				range.collapse()
				range.setEndPoint(item2.textInfo,"startToEnd")
			else:
				range=item2.textInfo.copy()
				range.collapse()
				range.setEndPoint(item1.textInfo,"startToEnd")
			if self._isSuitableNotLinkBlock(range):
				yield TextInfoQuickNavItem("notLinkBlock",self,range)
			item1=item2

	__gestures={
		"kb:NVDA+d": "activateLongDesc",
		"kb:escape": "disablePassThrough",
		"kb:alt+upArrow": "collapseOrExpandControl",
		"kb:alt+downArrow": "collapseOrExpandControl",
		"kb:tab": "tab",
		"kb:shift+tab": "shiftTab",
		"kb:shift+,": "moveToStartOfContainer",
		"kb:,": "movePastEndOfContainer",
	}
