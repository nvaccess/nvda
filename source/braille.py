# -*- coding: UTF-8 -*-
#braille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2018 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau

import sys
import itertools
import os
import pkgutil
import ctypes.wintypes
import threading
import time
import wx
import louis
import gui
import winKernel
import keyboardHandler
import baseObject
import config
from logHandler import log
import controlTypes
import api
import textInfos
import brailleDisplayDrivers
import inputCore
import brailleTables
import re
import scriptHandler
import collections
import extensionPoints
import hwPortUtils
import bdDetect
import winUser

roleLabels = {
	# Translators: Displayed in braille for an object which is a
	# window.
	controlTypes.ROLE_WINDOW: _("wnd"),
	# Translators: Displayed in braille for an object which is a
	# dialog.
	controlTypes.ROLE_DIALOG: _("dlg"),
	# Translators: Displayed in braille for an object which is a
	# check box.
	controlTypes.ROLE_CHECKBOX: _("chk"),
	# Translators: Displayed in braille for an object which is a
	# radio button.
	controlTypes.ROLE_RADIOBUTTON: _("rbtn"),
	# Translators: Displayed in braille for an object which is an
	# editable text field.
	controlTypes.ROLE_EDITABLETEXT: _("edt"),
	# Translators: Displayed in braille for an object which is a
	# button.
	controlTypes.ROLE_BUTTON: _("btn"),
	# Translators: Displayed in braille for an object which is a
	# menu bar.
	controlTypes.ROLE_MENUBAR: _("mnubar"),
	# Translators: Displayed in braille for an object which is a
	# menu item.
	controlTypes.ROLE_MENUITEM: _("mnuitem"),
	# Translators: Displayed in braille for an object which is a
	# menu.
	controlTypes.ROLE_POPUPMENU: _("mnu"),
	# Translators: Displayed in braille for an object which is a
	# combo box.
	controlTypes.ROLE_COMBOBOX: _("cbo"),
	# Translators: Displayed in braille for an object which is a
	# list.
	controlTypes.ROLE_LIST: _("lst"),
	# Translators: Displayed in braille for an object which is a
	# graphic.
	controlTypes.ROLE_GRAPHIC: _("gra"),
	# Translators: Displayed in braille for an object which is a
	# help balloon.
	controlTypes.ROLE_HELPBALLOON: _("hlp"),
	# Translators: Displayed in braille for an object which is a
	# tool tip.
	controlTypes.ROLE_TOOLTIP: _("tltip"),
	# Translators: Displayed in braille for an object which is a
	# link.
	controlTypes.ROLE_LINK: _("lnk"),
	# Translators: Displayed in braille for an object which is a
	# tree view.
	controlTypes.ROLE_TREEVIEW: _("tv"),
	# Translators: Displayed in braille for an object which is a
	# tree view item.
	controlTypes.ROLE_TREEVIEWITEM: _("tvitem"),
	# Translators: Displayed in braille for an object which is a
	# tab control.
	controlTypes.ROLE_TABCONTROL: _("tabctl"),
	# Translators: Displayed in braille for an object which is a
	# progress bar.
	controlTypes.ROLE_PROGRESSBAR: _("prgbar"),
	# Translators: Displayed in braille for an object which is a
	# scroll bar.
	controlTypes.ROLE_SCROLLBAR: _("scrlbar"),
	# Translators: Displayed in braille for an object which is a
	# status bar.
	controlTypes.ROLE_STATUSBAR: _("stbar"),
	# Translators: Displayed in braille for an object which is a
	# table.
	controlTypes.ROLE_TABLE: _("tbl"),
	# Translators: Displayed in braille for an object which is a
	# tool bar.
	controlTypes.ROLE_TOOLBAR: _("tlbar"),
	# Translators: Displayed in braille for an object which is a
	# drop down button.
	controlTypes.ROLE_DROPDOWNBUTTON: _("drbtn"),
	# Displayed in braille for an object which is a
	# separator.
	controlTypes.ROLE_SEPARATOR: u"⠤⠤⠤⠤⠤",
	# Translators: Displayed in braille for an object which is a
	# block quote.
	controlTypes.ROLE_BLOCKQUOTE: _("bqt"),
	# Translators: Displayed in braille for an object which is a
	# document.
	controlTypes.ROLE_DOCUMENT: _("doc"),
	# Translators: Displayed in braille for an object which is a
	# application.
	controlTypes.ROLE_APPLICATION: _("app"),
	# Translators: Displayed in braille for an object which is a
	# grouping.
	controlTypes.ROLE_GROUPING: _("grp"),
	# Translators: Displayed in braille for an object which is a
	# embedded object.
	controlTypes.ROLE_EMBEDDEDOBJECT: _("embedded"),
	# Translators: Displayed in braille for an object which is a
	# end note.
	controlTypes.ROLE_ENDNOTE: _("enote"),
	# Translators: Displayed in braille for an object which is a
	# foot note.
	controlTypes.ROLE_FOOTNOTE: _("fnote"),
	# Translators: Displayed in braille for an object which is a
	# terminal.
	controlTypes.ROLE_TERMINAL: _("term"),
	# Translators: Displayed in braille for an object which is a
	# section.
	controlTypes.ROLE_SECTION: _("sect"),
	# Translators: Displayed in braille for an object which is a
	# toggle button.
	controlTypes.ROLE_TOGGLEBUTTON: _("tgbtn"),
	# Translators: Displayed in braille for an object which is a
	# split button.
	controlTypes.ROLE_SPLITBUTTON: _("splbtn"),
	# Translators: Displayed in braille for an object which is a
	# menu button.
	controlTypes.ROLE_MENUBUTTON: _("mnubtn"),
	# Translators: Displayed in braille for an object which is a
	# spin button.
	controlTypes.ROLE_SPINBUTTON: _("spnbtn"),
	# Translators: Displayed in braille for an object which is a
	# tree view button.
	controlTypes.ROLE_TREEVIEWBUTTON: _("tvbtn"),
	# Translators: Displayed in braille for an object which is a
	# menu.
	controlTypes.ROLE_MENU: _("mnu"),
	# Translators: Displayed in braille for an object which is a
	# panel.
	controlTypes.ROLE_PANEL: _("pnl"),
	# Translators: Displayed in braille for an object which is a
	# password edit.
	controlTypes.ROLE_PASSWORDEDIT: _("pwdedt"),
	# Translators: Displayed in braille for an object which is deleted.
	controlTypes.ROLE_DELETED_CONTENT: _("del"),
	# Translators: Displayed in braille for an object which is inserted.
	controlTypes.ROLE_INSERTED_CONTENT: _("ins"),
}

positiveStateLabels = {
	# Translators: Displayed in braille when an object is selected.
	controlTypes.STATE_SELECTED: _("sel"),
	# Displayed in braille when an object (e.g. a toggle button) is pressed.
	controlTypes.STATE_PRESSED: u"⢎⣿⡱",
	# Displayed in braille when an object (e.g. a check box) is checked.
	controlTypes.STATE_CHECKED: u"⣏⣿⣹",
	# Displayed in braille when an object (e.g. a check box) is half checked.
	controlTypes.STATE_HALFCHECKED: u"⣏⣸⣹",
	# Translators: Displayed in braille when an object (e.g. an editable text field) is read-only.
	controlTypes.STATE_READONLY: _("ro"),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is expanded.
	controlTypes.STATE_EXPANDED: _("-"),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is collapsed.
	controlTypes.STATE_COLLAPSED: _("+"),
	# Translators: Displayed in braille when an object has a popup (usually a sub-menu).
	controlTypes.STATE_HASPOPUP: _("submnu"),
	# Translators: Displayed in braille when a protected control or a document is encountered.
	controlTypes.STATE_PROTECTED: _("***"),
	# Translators: Displayed in braille when a required form field is encountered.
	controlTypes.STATE_REQUIRED: _("req"),
	# Translators: Displayed in braille when an invalid entry has been made.
	controlTypes.STATE_INVALID_ENTRY: _("invalid"),
	# Translators: Displayed in braille when an object supports autocompletion.
	controlTypes.STATE_AUTOCOMPLETE: _("..."),
	# Translators: Displayed in braille when an edit field allows typing multiple lines of text such as comment fields on websites.
	controlTypes.STATE_MULTILINE: _("mln"),
	# Translators: Displayed in braille when an object is clickable.
	controlTypes.STATE_CLICKABLE: _("clk"),
	# Translators: Displayed in braille when an object is sorted ascending.
	controlTypes.STATE_SORTED_ASCENDING: _("sorted asc"),
	# Translators: Displayed in braille when an object is sorted descending.
	controlTypes.STATE_SORTED_DESCENDING: _("sorted desc"),
	# Translators: Displayed in braille when an object (usually a graphic) has a long description.
	controlTypes.STATE_HASLONGDESC: _("ldesc"),
	# Translators: Displayed in braille when there is a formula on a spreadsheet cell.
	controlTypes.STATE_HASFORMULA: _("frml"),
	# Translators: Displayed in braille when there is a comment for a spreadsheet cell or piece of text in a document.
	controlTypes.STATE_HASCOMMENT: _("cmnt"),
}
negativeStateLabels = {
	# Translators: Displayed in braille when an object is not selected.
	controlTypes.STATE_SELECTED: _("nsel"),
	# Displayed in braille when an object (e.g. a toggle button) is not pressed.
	controlTypes.STATE_PRESSED: u"⢎⣀⡱",
	# Displayed in braille when an object (e.g. a check box) is not checked.
	controlTypes.STATE_CHECKED: u"⣏⣀⣹",
}

landmarkLabels = {
	# Translators: Displayed in braille for the banner landmark, normally found on web pages.
	"banner": pgettext("braille landmark abbreviation", "bnnr"),
	# Translators: Displayed in braille for the complementary landmark, normally found on web pages.
	"complementary": pgettext("braille landmark abbreviation", "cmpl"),
	# Translators: Displayed in braille for the contentinfo landmark, normally found on web pages.
	"contentinfo": pgettext("braille landmark abbreviation", "cinf"),
	# Translators: Displayed in braille for the main landmark, normally found on web pages.
	"main": pgettext("braille landmark abbreviation", "main"),
	# Translators: Displayed in braille for the navigation landmark, normally found on web pages.
	"navigation": pgettext("braille landmark abbreviation", "navi"),
	# Translators: Displayed in braille for the search landmark, normally found on web pages.
	"search": pgettext("braille landmark abbreviation", "srch"),
	# Translators: Displayed in braille for the form landmark, normally found on web pages.
	"form": pgettext("braille landmark abbreviation", "form"),
	# Strictly speaking, region isn't a landmark, but it is very similar.
	# Translators: Displayed in braille for a significant region, normally found on web pages.
	"region": pgettext("braille landmark abbreviation", "rgn"),
}

#: Cursor shapes
CURSOR_SHAPES = (
	# Translators: The description of a braille cursor shape.
	(0xC0, _("Dots 7 and 8")),
	# Translators: The description of a braille cursor shape.
	(0x80, _("Dot 8")),
	# Translators: The description of a braille cursor shape.
	(0xFF, _("All dots")),
)
SELECTION_SHAPE = 0xC0 #: Dots 7 and 8

#: Unicode braille indicator at the start of untranslated braille input.
INPUT_START_IND = u"⣏"
#: Unicode braille indicator at the end of untranslated braille input.
INPUT_END_IND = u" ⣹"

# used to separate chunks of text when programmatically joined
TEXT_SEPARATOR = " "

#: Identifier for a focus context presentation setting that
#: only shows as much as possible focus context information when the context has changed.
CONTEXTPRES_CHANGEDCONTEXT = "changedContext"
#: Identifier for a focus context presentation setting that
#: shows as much as possible focus context information if the focus object doesn't fill up the whole display.
CONTEXTPRES_FILL = "fill"
#: Identifier for a focus context presentation setting that
#: always shows the object with focus at the very left of the braille display.
CONTEXTPRES_SCROLL = "scroll"
#: Focus context presentations associated with their user readable and translatable labels
focusContextPresentations=[
	# Translators: The label for a braille focus context presentation setting that
	# only shows as much as possible focus context information when the context has changed.
	(CONTEXTPRES_CHANGEDCONTEXT, _("Fill display for context changes")),
	# Translators: The label for a braille focus context presentation setting that
	# shows as much as possible focus context information if the focus object doesn't fill up the whole display.
	# This was the pre NVDA 2017.3 default.
	(CONTEXTPRES_FILL, _("Always fill display")),
	# Translators: The label for a braille focus context presentation setting that
	# always shows the object with focus at the very left of the braille display
	# (i.e. you will have to scroll back for focus context information).
	(CONTEXTPRES_SCROLL, _("Only when scrolling back")),
]

#: Named tuple for a region with start and end positions in a buffer
RegionWithPositions = collections.namedtuple("RegionWithPositions",("region","start","end"))

#: Automatic constant to be used by braille displays that support the "automatic" port
#: and automatic braille display detection
#: @type: tuple
# Translators: String representing automatic port selection for braille displays.
AUTOMATIC_PORT = ("auto", _("Automatic"))
#: Used in place of a specific braille display driver name to indicate that
#: braille displays should be automatically detected and used.
#: @type: str
AUTO_DISPLAY_NAME = AUTOMATIC_PORT[0]
#: A port name which indicates that USB should be used.
#: @type: tuple
# Translators: String representing the USB port selection for braille displays.
USB_PORT =  ("usb", _("USB"))
#: A port name which indicates that Bluetooth should be used.
#: @type: tuple
# Translators: String representing the Bluetooth port selection for braille displays.
BLUETOOTH_PORT =  ("bluetooth", _("Bluetooth"))

def NVDAObjectHasUsefulText(obj):
	import displayModel
	if issubclass(obj.TextInfo,displayModel.DisplayModelTextInfo):
		# #1711: Flat review (using displayModel) should always be presented on the braille display
		return True
	else:
		# Let the NVDAObject choose if the text should be presented
		return obj._hasNavigableText

def _getDisplayDriver(moduleName, caseSensitive=True):
	try:
		return __import__("brailleDisplayDrivers.%s" % moduleName, globals(), locals(), ("brailleDisplayDrivers",)).BrailleDisplayDriver
	except ImportError as initialException:
		if caseSensitive:
			raise initialException
		for loader, name, isPkg in pkgutil.iter_modules(brailleDisplayDrivers.__path__):
			if name.startswith('_') or name.lower() != moduleName.lower():
				continue
			return __import__("brailleDisplayDrivers.%s" % name, globals(), locals(), ("brailleDisplayDrivers",)).BrailleDisplayDriver
		else:
			raise initialException

def getDisplayList(excludeNegativeChecks=True):
	"""Gets a list of available display driver names with their descriptions.
	@param excludeNegativeChecks: excludes all drivers for which the check method returns C{False}.
	@type excludeNegativeChecks: bool
	@return: list of tuples with driver names and descriptions.
	@rtype: [(str,unicode)]
	"""
	displayList = []
	# The display that should be placed at the end of the list.
	lastDisplay = None
	for loader, name, isPkg in pkgutil.iter_modules(brailleDisplayDrivers.__path__):
		if name.startswith('_'):
			continue
		try:
			display = _getDisplayDriver(name)
		except:
			log.error("Error while importing braille display driver %s" % name,
				exc_info=True)
			continue
		try:
			if not excludeNegativeChecks or display.check():
				if display.name == "noBraille":
					lastDisplay = (display.name, display.description)
				else:
					displayList.append((display.name, display.description))
			else:
				log.debugWarning("Braille display driver %s reports as unavailable, excluding" % name)
		except:
			log.error("", exc_info=True)
	displayList.sort(key=lambda d : d[1].lower())
	if lastDisplay:
		displayList.append(lastDisplay)
	return displayList

class Region(object):
	"""A region of braille to be displayed.
	Each portion of braille to be displayed is represented by a region.
	The region is responsible for retrieving its text and the cursor and selection positions, translating it into braille cells and handling cursor routing requests relative to its braille cells.
	The L{BrailleBuffer} containing this region will call L{update} and expect that L{brailleCells}, L{brailleCursorPos}, L{brailleSelectionStart} and L{brailleSelectionEnd} will be set appropriately.
	L{routeTo} will be called to handle a cursor routing request.
	"""

	def __init__(self):
		#: The original, raw text of this region.
		self.rawText = ""
		#: The position of the cursor in L{rawText}, C{None} if the cursor is not in this region.
		#: @type: int
		self.cursorPos = None
		#: The start of the selection in L{rawText} (inclusive), C{None} if there is no selection in this region.
		#: @type: int
		self.selectionStart = None
		#: The end of the selection in L{rawText} (exclusive), C{None} if there is no selection in this region.
		#: @type: int
		self.selectionEnd = None
		#: The translated braille representation of this region.
		#: @type: [int, ...]
		self.brailleCells = []
		#: liblouis typeform flags for each character in L{rawText},
		#: C{None} if no typeform info.
		#: @type: [int, ...]
		self.rawTextTypeforms = None
		#: A list mapping positions in L{rawText} to positions in L{brailleCells}.
		#: @type: [int, ...]
		self.rawToBraillePos = []
		#: A list mapping positions in L{brailleCells} to positions in L{rawText}.
		#: @type: [int, ...]
		self.brailleToRawPos = []
		#: The position of the cursor in L{brailleCells}, C{None} if the cursor is not in this region.
		#: @type: int
		self.brailleCursorPos = None
		#: The position of the selection start in L{brailleCells}, C{None} if there is no selection in this region.
		#: @type: int
		self.brailleSelectionStart = None
		#: The position of the selection end in L{brailleCells}, C{None} if there is no selection in this region.
		#: @type: int
		self.brailleSelectionEnd = None
		#: Whether to hide all previous regions.
		#: @type: bool
		self.hidePreviousRegions = False
		#: Whether this region should be positioned at the absolute left of the display when focused.
		#: @type: bool
		self.focusToHardLeft = False

	def update(self):
		"""Update this region.
		Subclasses should extend this to update L{rawText}, L{cursorPos}, L{selectionStart} and L{selectionEnd} if necessary.
		The base class method handles translation of L{rawText} into braille, placing the result in L{brailleCells}.
		Typeform information from L{rawTextTypeforms} is used, if any.
		L{rawToBraillePos} and L{brailleToRawPos} are updated according to the translation.
		L{brailleCursorPos}, L{brailleSelectionStart} and L{brailleSelectionEnd} are similarly updated based on L{cursorPos}, L{selectionStart} and L{selectionEnd}, respectively.
		@postcondition: L{brailleCells}, L{brailleCursorPos}, L{brailleSelectionStart} and L{brailleSelectionEnd} are updated and ready for rendering.
		"""
		mode = louis.dotsIO
		if config.conf["braille"]["expandAtCursor"] and self.cursorPos is not None:
			mode |= louis.compbrlAtCursor
		text=unicode(self.rawText).replace('\0','')
		braille, self.brailleToRawPos, self.rawToBraillePos, brailleCursorPos = louis.translate(
			[os.path.join(brailleTables.TABLES_DIR, config.conf["braille"]["translationTable"]),
				"braille-patterns.cti"],
			text,
			# liblouis mutates typeform if it is a list.
			typeform=tuple(self.rawTextTypeforms) if isinstance(self.rawTextTypeforms, list) else self.rawTextTypeforms,
			mode=mode, cursorPos=self.cursorPos or 0)
		# liblouis gives us back a character string of cells, so convert it to a list of ints.
		# For some reason, the highest bit is set, so only grab the lower 8 bits.
		self.brailleCells = [ord(cell) & 255 for cell in braille]
		# #2466: HACK: liblouis incorrectly truncates trailing spaces from its output in some cases.
		# Detect this and add the spaces to the end of the output.
		if self.rawText and self.rawText[-1] == " ":
			# rawToBraillePos isn't truncated, even though brailleCells is.
			# Use this to figure out how long brailleCells should be and thus how many spaces to add.
			correctCellsLen = self.rawToBraillePos[-1] + 1
			currentCellsLen = len(self.brailleCells)
			if correctCellsLen > currentCellsLen:
				self.brailleCells.extend((0,) * (correctCellsLen - currentCellsLen))
		if self.cursorPos is not None:
			# HACK: The cursorPos returned by liblouis is notoriously buggy (#2947 among other issues).
			# rawToBraillePos is usually accurate.
			try:
				brailleCursorPos = self.rawToBraillePos[self.cursorPos]
			except IndexError:
				pass
		else:
			brailleCursorPos = None
		self.brailleCursorPos = brailleCursorPos
		if self.selectionStart is not None and self.selectionEnd is not None:
			try:
				# Mark the selection.
				self.brailleSelectionStart = self.rawToBraillePos[self.selectionStart]
				if self.selectionEnd >= len(self.rawText):
					self.brailleSelectionEnd = len(self.brailleCells)
				else:
					self.brailleSelectionEnd = self.rawToBraillePos[self.selectionEnd]
				for pos in xrange(self.brailleSelectionStart, self.brailleSelectionEnd):
					self.brailleCells[pos] |= SELECTION_SHAPE
			except IndexError:
				pass

	def routeTo(self, braillePos):
		"""Handle a cursor routing request.
		For example, this might activate an object or move the cursor to the requested position.
		@param braillePos: The routing position in L{brailleCells}.
		@type braillePos: int
		@note: If routing the cursor, L{brailleToRawPos} can be used to translate L{braillePos} into a position in L{rawText}.
		"""

	def nextLine(self):
		"""Move to the next line if possible.
		"""

	def previousLine(self, start=False):
		"""Move to the previous line if possible.
		@param start: C{True} to move to the start of the line, C{False} to move to the end.
		@type start: bool
		"""

class TextRegion(Region):
	"""A simple region containing a string of text.
	"""

	def __init__(self, text):
		super(TextRegion, self).__init__()
		self.rawText = text

def getBrailleTextForProperties(**propertyValues):
	textList = []
	name = propertyValues.get("name")
	if name:
		textList.append(name)
	role = propertyValues.get("role")
	roleText = propertyValues.get("roleText")
	states = propertyValues.get("states")
	positionInfo = propertyValues.get("positionInfo")
	level = positionInfo.get("level") if positionInfo else None
	cellCoordsText=propertyValues.get('cellCoordsText')
	rowNumber = propertyValues.get("rowNumber")
	columnNumber = propertyValues.get("columnNumber")
	rowSpan = propertyValues.get("rowSpan")
	columnSpan = propertyValues.get("columnSpan")
	includeTableCellCoords = propertyValues.get("includeTableCellCoords", True)
	if role is not None and not roleText:
		if role == controlTypes.ROLE_HEADING and level:
			# Translators: Displayed in braille for a heading with a level.
			# %s is replaced with the level.
			roleText = _("h%s") % level
			level = None
		elif role == controlTypes.ROLE_LINK and states and controlTypes.STATE_VISITED in states:
			states = states.copy()
			states.discard(controlTypes.STATE_VISITED)
			# Translators: Displayed in braille for a link which has been visited.
			roleText = _("vlnk")
		elif (name or cellCoordsText or rowNumber or columnNumber) and role in controlTypes.silentRolesOnFocus:
			roleText = None
		else:
			roleText = roleLabels.get(role, controlTypes.roleLabels[role])
	elif role is None: 
		role = propertyValues.get("_role")
	value = propertyValues.get("value")
	if value and role not in controlTypes.silentValuesForRoles:
		textList.append(value)
	if states:
		textList.extend(
			controlTypes.processAndLabelStates(role, states, controlTypes.REASON_FOCUS, states, None, positiveStateLabels, negativeStateLabels)
		)
	if roleText:
		textList.append(roleText)
	description = propertyValues.get("description")
	if description:
		textList.append(description)
	keyboardShortcut = propertyValues.get("keyboardShortcut")
	if keyboardShortcut:
		textList.append(keyboardShortcut)
	if positionInfo:
		indexInGroup = positionInfo.get("indexInGroup")
		similarItemsInGroup = positionInfo.get("similarItemsInGroup")
		if indexInGroup and similarItemsInGroup:
			# Translators: Brailled to indicate the position of an item in a group of items (such as a list).
			# {number} is replaced with the number of the item in the group.
			# {total} is replaced with the total number of items in the group.
			textList.append(_("{number} of {total}").format(number=indexInGroup, total=similarItemsInGroup))
		if level is not None:
			# Translators: Displayed in braille when an object (e.g. a tree view item) has a hierarchical level.
			# %s is replaced with the level.
			textList.append(_('lv %s')%positionInfo['level'])
	if rowNumber:
		if includeTableCellCoords and not cellCoordsText: 
			if rowSpan>1:
				# Translators: Displayed in braille for the table cell row numbers when a cell spans multiple rows.
				# Occurences of %s are replaced with the corresponding row numbers.
				rowStr = _("r{rowNumber}-{rowSpan}").format(rowNumber=rowNumber,rowSpan=rowNumber+rowSpan-1)
			else:
				# Translators: Displayed in braille for a table cell row number.
				# %s is replaced with the row number.
				rowStr = _("r{rowNumber}").format(rowNumber=rowNumber)
			textList.append(rowStr)
	if columnNumber:
		columnHeaderText = propertyValues.get("columnHeaderText")
		if columnHeaderText:
			textList.append(columnHeaderText)
		if includeTableCellCoords and not cellCoordsText:
			if columnSpan>1:
				# Translators: Displayed in braille for the table cell column numbers when a cell spans multiple columns.
				# Occurences of %s are replaced with the corresponding column numbers.
				columnStr = _("c{columnNumber}-{columnSpan}").format(columnNumber=columnNumber,columnSpan=columnNumber+columnSpan-1)
			else:
				# Translators: Displayed in braille for a table cell column number.
				# %s is replaced with the column number.
				columnStr = _("c{columnNumber}").format(columnNumber=columnNumber)
			textList.append(columnStr)
	current = propertyValues.get('current', False)
	if current:
		try:
			textList.append(controlTypes.isCurrentLabels[current])
		except KeyError:
			log.debugWarning("Aria-current value not handled: %s"%current)
			textList.append(controlTypes.isCurrentLabels[True])
	placeholder = propertyValues.get('placeholder', None)
	if placeholder:
		textList.append(placeholder)
	if includeTableCellCoords and  cellCoordsText:
		textList.append(cellCoordsText)
	return TEXT_SEPARATOR.join([x for x in textList if x])

class NVDAObjectRegion(Region):
	"""A region to provide a braille representation of an NVDAObject.
	This region will update based on the current state of the associated NVDAObject.
	A cursor routing request will activate the object's default action.
	"""

	def __init__(self, obj, appendText=""):
		"""Constructor.
		@param obj: The associated NVDAObject.
		@type obj: L{NVDAObjects.NVDAObject}
		@param appendText: Text which should always be appended to the NVDAObject text, useful if this region will always precede other regions.
		@type appendText: str
		"""
		super(NVDAObjectRegion, self).__init__()
		self.obj = obj
		self.appendText = appendText

	def update(self):
		obj = self.obj
		presConfig = config.conf["presentation"]
		role = obj.role
		placeholderValue = obj.placeholder
		if placeholderValue and not obj._isTextEmpty:
			placeholderValue = None
		text = getBrailleTextForProperties(
			name=obj.name,
			role=role,
			roleText=obj.roleText,
			current=obj.isCurrent,
			placeholder=placeholderValue,
			value=obj.value if not NVDAObjectHasUsefulText(obj) else None ,
			states=obj.states,
			description=obj.description if presConfig["reportObjectDescriptions"] else None,
			keyboardShortcut=obj.keyboardShortcut if presConfig["reportKeyboardShortcuts"] else None,
			positionInfo=obj.positionInfo if presConfig["reportObjectPositionInformation"] else None,
			cellCoordsText=obj.cellCoordsText if config.conf["documentFormatting"]["reportTableCellCoords"] else None,
		)
		if role == controlTypes.ROLE_MATH:
			import mathPres
			mathPres.ensureInit()
			if mathPres.brailleProvider:
				try:
					text += TEXT_SEPARATOR + mathPres.brailleProvider.getBrailleForMathMl(
						obj.mathMl)
				except (NotImplementedError, LookupError):
					pass
		self.rawText = text + self.appendText
		super(NVDAObjectRegion, self).update()

	def routeTo(self, braillePos):
		try:
			self.obj.doAction()
		except NotImplementedError:
			pass

def getControlFieldBraille(info, field, ancestors, reportStart, formatConfig):
	presCat = field.getPresentationCategory(ancestors, formatConfig)
	# Cache this for later use.
	field._presCat = presCat
	if reportStart:
		# If this is a container, only report it if this is the start of the node.
		if presCat == field.PRESCAT_CONTAINER and not field.get("_startOfNode"):
			return None
	else:
		# We only report ends for containers
		# and only if this is the end of the node.
		if presCat != field.PRESCAT_CONTAINER or not field.get("_endOfNode"):
			return None

	role = field.get("role", controlTypes.ROLE_UNKNOWN)
	states = field.get("states", set())
	value=field.get('value',None)
	current=field.get('current', None)
	placeholder=field.get('placeholder', None)
	roleText=field.get('roleText')

	if presCat == field.PRESCAT_LAYOUT:
		text = []
		# The only item we report for these fields is clickable, if present.
		if controlTypes.STATE_CLICKABLE in states:
			text.append(getBrailleTextForProperties(states={controlTypes.STATE_CLICKABLE}))
		if current:
			text.append(getBrailleTextForProperties(current=current))
		return TEXT_SEPARATOR.join(text) if len(text) != 0 else None

	elif role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER) and field.get("table-id"):
		# Table cell.
		reportTableHeaders = formatConfig["reportTableHeaders"]
		reportTableCellCoords = formatConfig["reportTableCellCoords"]
		props = {
			"states": states,
			"rowNumber": field.get("table-rownumber"),
			"columnNumber": field.get("table-columnnumber"),
			"rowSpan": field.get("table-rowsspanned"),
			"columnSpan": field.get("table-columnsspanned"),
			"includeTableCellCoords": reportTableCellCoords,
			"current": current,
		}
		if reportTableHeaders:
			props["columnHeaderText"] = field.get("table-columnheadertext")
		return getBrailleTextForProperties(**props)

	elif reportStart:
		props = {
			# Don't report the role for math here.
			# However, we still need to pass it (hence "_role").
			"_role" if role == controlTypes.ROLE_MATH else "role": role,
			"states": states,"value":value, "current":current, "placeholder":placeholder,"roleText":roleText}
		if config.conf["presentation"]["reportKeyboardShortcuts"]:
			kbShortcut = field.get("keyboardShortcut")
			if kbShortcut:
				props["keyboardShortcut"] = kbShortcut
		level = field.get("level")
		if level:
			props["positionInfo"] = {"level": level}
		text = getBrailleTextForProperties(**props)
		content = field.get("content")
		if content:
			if text:
				text += TEXT_SEPARATOR
			text += content
		elif role == controlTypes.ROLE_MATH:
			import mathPres
			mathPres.ensureInit()
			if mathPres.brailleProvider:
				try:
					if text:
						text += TEXT_SEPARATOR
					text += mathPres.brailleProvider.getBrailleForMathMl(
						info.getMathMl(field))
				except (NotImplementedError, LookupError):
					pass
		return text
	else:
		# Translators: Displayed in braille at the end of a control field such as a list or table.
		# %s is replaced with the control's role.
		return (_("%s end") %
			getBrailleTextForProperties(role=role,roleText=roleText))

def getFormatFieldBraille(field, fieldCache, isAtStart, formatConfig):
	"""Generates the braille text for the given format field.
	@param field: The format field to examine.
	@type field: {str : str, ...}
	@param fieldCache: The format field of the previous run; i.e. the cached format field.
	@type fieldCache: {str : str, ...}
	@param isAtStart: True if this format field precedes any text in the line/paragraph.
	This is useful to restrict display of information which should only appear at the start of the line/paragraph;
	e.g. the line number or line prefix (list bullet/number).
	@type isAtStart: bool
	@param formatConfig: The formatting config.
	@type formatConfig: {str : bool, ...}
	"""
	textList = []
	if isAtStart:
		if formatConfig["reportLineNumber"]:
			lineNumber = field.get("line-number")
			if lineNumber:
				textList.append("%s" % lineNumber)
		linePrefix = field.get("line-prefix")
		if linePrefix:
			textList.append(linePrefix)
		if formatConfig["reportHeadings"]:
			headingLevel=field.get('heading-level')
			if headingLevel:
				# Translators: Displayed in braille for a heading with a level.
				# %s is replaced with the level.
				textList.append(_("h%s")%headingLevel)
	if formatConfig["reportLinks"]:
		link=field.get("link")
		oldLink=fieldCache.get("link")
		if link and link != oldLink:
			textList.append(roleLabels[controlTypes.ROLE_LINK])
	fieldCache.clear()
	fieldCache.update(field)
	return TEXT_SEPARATOR.join([x for x in textList if x])

class TextInfoRegion(Region):

	pendingCaretUpdate=False #: True if the cursor should be updated for this region on the display
	allowPageTurns=True #: True if a page turn should be tried when a TextInfo cannot move anymore and the object supports page turns.

	def __init__(self, obj):
		super(TextInfoRegion, self).__init__()
		self.obj = obj

	def _isMultiline(self):
		# A region's object can either be an NVDAObject or a tree interceptor.
		# Tree interceptors should always be multiline.
		from treeInterceptorHandler import TreeInterceptor
		if isinstance(self.obj, TreeInterceptor):
			return True
		# Terminals and documents are inherently multiline, so they don't have the multiline state.
		return (
			self.obj.role in (controlTypes.ROLE_TERMINAL,controlTypes.ROLE_DOCUMENT)
			or controlTypes.STATE_MULTILINE in self.obj.states
		)

	def _getSelection(self):
		"""Retrieve the selection.
		If there is no selection, retrieve the collapsed cursor.
		@return: The selection.
		@rtype: L{textInfos.TextInfo}
		"""
		try:
			return self.obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			return self.obj.makeTextInfo(textInfos.POSITION_FIRST)

	def _setCursor(self, info):
		"""Set the cursor.
		@param info: The range to which the cursor should be moved.
		@type info: L{textInfos.TextInfo}
		"""
		try:
			info.updateCaret()
		except NotImplementedError:
			log.debugWarning("", exc_info=True)

	def _getTypeformFromFormatField(self, field, formatConfig):
		typeform = louis.plain_text
		if not formatConfig["reportFontAttributes"]:
			return typeform
		if field.get("bold", False):
			typeform |= louis.bold
		if field.get("italic", False):
			typeform |= louis.italic
		if field.get("underline", False):
			typeform |= louis.underline
		return typeform

	def _addFieldText(self, text, contentPos, separate=True):
		if separate and self.rawText:
			# Separate this field text from the rest of the text.
			text = TEXT_SEPARATOR + text
		self.rawText += text
		textLen = len(text)
		self.rawTextTypeforms.extend((louis.plain_text,) * textLen)
		self._rawToContentPos.extend((contentPos,) * textLen)

	def _addTextWithFields(self, info, formatConfig, isSelection=False):
		shouldMoveCursorToFirstContent = not isSelection and self.cursorPos is not None
		ctrlFields = []
		typeform = louis.plain_text
		formatFieldAttributesCache = getattr(info.obj, "_brailleFormatFieldAttributesCache", {})
		for command in info.getTextWithFields(formatConfig=formatConfig):
			if isinstance(command, basestring):
				self._isFormatFieldAtStart = False
				if not command:
					continue
				if self._endsWithField:
					# The last item added was a field,
					# so add a space before the content.
					self.rawText += TEXT_SEPARATOR
					self.rawTextTypeforms.append(louis.plain_text)
					self._rawToContentPos.append(self._currentContentPos)
				if isSelection and self.selectionStart is None:
					# This is where the content begins.
					self.selectionStart = len(self.rawText)
				elif shouldMoveCursorToFirstContent:
					# This is the first piece of content after the cursor.
					# Position the cursor here, as it may currently be positioned on control field text.
					self.cursorPos = len(self.rawText)
					shouldMoveCursorToFirstContent = False
				self.rawText += command
				commandLen = len(command)
				self.rawTextTypeforms.extend((typeform,) * commandLen)
				endPos = self._currentContentPos + commandLen
				self._rawToContentPos.extend(xrange(self._currentContentPos, endPos))
				self._currentContentPos = endPos
				if isSelection:
					# The last time this is set will be the end of the content.
					self.selectionEnd = len(self.rawText)
				self._endsWithField = False
			elif isinstance(command, textInfos.FieldCommand):
				cmd = command.command
				field = command.field
				if cmd == "formatChange":
					typeform = self._getTypeformFromFormatField(field, formatConfig)
					text = getFormatFieldBraille(field, formatFieldAttributesCache, self._isFormatFieldAtStart, formatConfig)
					if not text:
						continue
					# Map this field text to the start of the field's content.
					self._addFieldText(text, self._currentContentPos)
				elif cmd == "controlStart":
					if self._skipFieldsNotAtStartOfNode and not field.get("_startOfNode"):
						text = None
					else:
						text = info.getControlFieldBraille(field, ctrlFields, True, formatConfig)
					# Place this field on a stack so we can access it for controlEnd.
					ctrlFields.append(field)
					if not text:
						continue
					if getattr(field, "_presCat") == field.PRESCAT_MARKER:
						# In this case, the field text is what the user cares about,
						# not the actual content.
						fieldStart = len(self.rawText)
						if fieldStart > 0:
							# There'll be a space before the field text.
							fieldStart += 1
						if isSelection and self.selectionStart is None:
							self.selectionStart = fieldStart
						elif shouldMoveCursorToFirstContent:
							self.cursorPos = fieldStart
							shouldMoveCursorToFirstContent = False
					# Map this field text to the start of the field's content.
					self._addFieldText(text, self._currentContentPos)
				elif cmd == "controlEnd":
					field = ctrlFields.pop()
					text = info.getControlFieldBraille(field, ctrlFields, False, formatConfig)
					if not text:
						continue
					# Map this field text to the end of the field's content.
					self._addFieldText(text, self._currentContentPos - 1)
				self._endsWithField = True
		if isSelection and self.selectionStart is None:
			# There is no selection. This is a cursor.
			self.cursorPos = len(self.rawText)
		if not self._skipFieldsNotAtStartOfNode:
			# We only render fields that aren't at the start of their nodes for the first part of the reading unit.
			# Otherwise, we'll render fields that have already been rendered.
			self._skipFieldsNotAtStartOfNode = True
		info.obj._brailleFormatFieldAttributesCache = formatFieldAttributesCache

	def _getReadingUnit(self):
		return textInfos.UNIT_PARAGRAPH if config.conf["braille"]["readByParagraph"] else textInfos.UNIT_LINE

	def update(self):
		formatConfig = config.conf["documentFormatting"]
		unit = self._getReadingUnit()
		self.rawText = ""
		self.rawTextTypeforms = []
		self.cursorPos = None
		# The output includes text representing fields which isn't part of the real content in the control.
		# Therefore, maintain a map of positions in the output to positions in the content.
		self._rawToContentPos = []
		self._currentContentPos = 0
		self.selectionStart = self.selectionEnd = None
		self._isFormatFieldAtStart = True
		self._skipFieldsNotAtStartOfNode = False
		self._endsWithField = False

		# Selection has priority over cursor.
		# HACK: Some TextInfos only support UNIT_LINE properly if they are based on POSITION_CARET,
		# and copying the TextInfo breaks this ability.
		# So use the original TextInfo for line and a copy for cursor/selection.
		self._readingInfo = readingInfo = self._getSelection()
		sel = readingInfo.copy()
		if not sel.isCollapsed:
			# There is a selection.
			if self.obj.isTextSelectionAnchoredAtStart:
				# The end of the range is exclusive, so make it inclusive first.
				readingInfo.move(textInfos.UNIT_CHARACTER, -1, "end")
			# Collapse the selection to the unanchored end.
			readingInfo.collapse(end=self.obj.isTextSelectionAnchoredAtStart)
			# Get the reading unit at the selection.
			readingInfo.expand(unit)
			# Restrict the selection to the reading unit.
			if sel.compareEndPoints(readingInfo, "startToStart") < 0:
				sel.setEndPoint(readingInfo, "startToStart")
			if sel.compareEndPoints(readingInfo, "endToEnd") > 0:
				sel.setEndPoint(readingInfo, "endToEnd")
		else:
			# There is a cursor.
			# Get the reading unit at the cursor.
			readingInfo.expand(unit)

		# Not all text APIs support offsets, so we can't always get the offset of the selection relative to the start of the reading unit.
		# Therefore, grab the reading unit in three parts.
		# First, the chunk from the start of the reading unit to the start of the selection.
		chunk = readingInfo.copy()
		chunk.collapse()
		chunk.setEndPoint(sel, "endToStart")
		self._addTextWithFields(chunk, formatConfig)
		# If the user is entering braille, place any untranslated braille before the selection.
		# Import late to avoid circular import.
		import brailleInput
		text = brailleInput.handler.untranslatedBraille
		if text:
			rawInputIndStart = len(self.rawText)
			# _addFieldText adds text to self.rawText and updates other state accordingly.
			self._addFieldText(INPUT_START_IND + text + INPUT_END_IND, None, separate=False)
			rawInputIndEnd = len(self.rawText)
		else:
			rawInputIndStart = None
		# Now, the selection itself.
		self._addTextWithFields(sel, formatConfig, isSelection=True)
		# Finally, get the chunk from the end of the selection to the end of the reading unit.
		chunk.setEndPoint(readingInfo, "endToEnd")
		chunk.setEndPoint(sel, "startToEnd")
		self._addTextWithFields(chunk, formatConfig)

		# Strip line ending characters.
		self.rawText = self.rawText.rstrip("\r\n\0\v\f")
		rawTextLen = len(self.rawText)
		if rawTextLen < len(self._rawToContentPos):
			# The stripped text is shorter than the original.
			self._currentContentPos = self._rawToContentPos[rawTextLen]
			del self.rawTextTypeforms[rawTextLen:]
			# Trimming _rawToContentPos doesn't matter,
			# because we'll only ever ask for indexes valid in rawText.
			#del self._rawToContentPos[rawTextLen:]
		if rawTextLen == 0 or not self._endsWithField:
			# There is no text left after stripping line ending characters,
			# or the last item added can be navigated with a cursor.
			# Add a space in case the cursor is at the end of the reading unit.
			self.rawText += TEXT_SEPARATOR
			rawTextLen += 1
			self.rawTextTypeforms.append(louis.plain_text)
			self._rawToContentPos.append(self._currentContentPos)
		if self.cursorPos is not None and self.cursorPos >= rawTextLen:
			self.cursorPos = rawTextLen - 1
		# The selection end doesn't have to be checked, Region.update() makes sure brailleSelectionEnd is valid.

		# If this is not the start of the object, hide all previous regions.
		start = readingInfo.obj.makeTextInfo(textInfos.POSITION_FIRST)
		self.hidePreviousRegions = (start.compareEndPoints(readingInfo, "startToStart") < 0)
		# Don't touch focusToHardLeft if it is already true
		# For example, it can be set to True in getFocusContextRegions when this region represents the first new focus ancestor
		# Alternatively, BrailleHandler._doNewObject can set this to True when this region represents the focus object and the focus ancestry didn't change
		if not self.focusToHardLeft:
			# If this is a multiline control, position it at the absolute left of the display when focused.
			self.focusToHardLeft = self._isMultiline()
		super(TextInfoRegion, self).update()

		if rawInputIndStart is not None:
			assert rawInputIndEnd is not None, "rawInputIndStart set but rawInputIndEnd isn't"
			# These are the start and end of the untranslated input area,
			# including the start and end indicators.
			self._brailleInputIndStart = self.rawToBraillePos[rawInputIndStart]
			self._brailleInputIndEnd = self.rawToBraillePos[rawInputIndEnd]
			# These are the start and end of the actual untranslated input, excluding indicators.
			self._brailleInputStart = self._brailleInputIndStart + len(INPUT_START_IND)
			self._brailleInputEnd = self._brailleInputIndEnd - len(INPUT_END_IND)
			self.brailleCursorPos = self._brailleInputStart + brailleInput.handler.untranslatedCursorPos
		else:
			self._brailleInputIndStart = None

	def getTextInfoForBraillePos(self, braillePos):
		pos = self._rawToContentPos[self.brailleToRawPos[braillePos]]
		# pos is relative to the start of the reading unit.
		# Therefore, get the start of the reading unit...
		dest = self._readingInfo.copy()
		dest.collapse()
		# and move pos characters from there.
		dest.move(textInfos.UNIT_CHARACTER, pos)
		return dest

	def routeTo(self, braillePos):
		if self._brailleInputIndStart is not None and self._brailleInputIndStart <= braillePos < self._brailleInputIndEnd:
			# The user is moving within untranslated braille input.
			if braillePos < self._brailleInputStart:
				# The user routed to the start indicator. Route to the start of the input.
				braillePos = self._brailleInputStart
			elif braillePos > self._brailleInputEnd:
				# The user routed to the end indicator. Route to the end of the input.
				braillePos = self._brailleInputEnd
			# Import late to avoid circular import.
			import brailleInput
			brailleInput.handler.untranslatedCursorPos = braillePos - self._brailleInputStart
			self.brailleCursorPos = self._brailleInputStart + brailleInput.handler.untranslatedCursorPos
			brailleInput.handler.updateDisplay()
			return

		if braillePos == self.brailleCursorPos:
			# The cursor is already at this position,
			# so activate the position.
			try:
				self._getSelection().activate()
			except NotImplementedError:
				pass
			return
		dest = self.getTextInfoForBraillePos(braillePos)
		self._setCursor(dest)

	def nextLine(self):
		dest = self._readingInfo.copy()
		moved = dest.move(self._getReadingUnit(), 1)
		if not moved:
			if self.allowPageTurns and isinstance(dest.obj,textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage()
				except RuntimeError:
					pass
				else:
					dest=dest.obj.makeTextInfo(textInfos.POSITION_FIRST)
			else: # no page turn support
				return
		dest.collapse()
		self._setCursor(dest)

	def previousLine(self, start=False):
		dest = self._readingInfo.copy()
		dest.collapse()
		if start:
			unit = self._getReadingUnit()
		else:
			# If the end of the reading unit is desired, move to the last character.
			unit = textInfos.UNIT_CHARACTER
		moved = dest.move(unit, -1)
		if not moved:
			if self.allowPageTurns and isinstance(dest.obj,textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage(previous=True)
				except RuntimeError:
					pass
				else:
					dest=dest.obj.makeTextInfo(textInfos.POSITION_LAST)
					dest.expand(unit)
			else: # no page turn support
				return
		dest.collapse()
		self._setCursor(dest)

class CursorManagerRegion(TextInfoRegion):

	def _isMultiline(self):
		return True

	def _getSelection(self):
		return self.obj.selection

	def _setCursor(self, info):
		self.obj.selection = info

class ReviewTextInfoRegion(TextInfoRegion):

	allowPageTurns=False

	def _getSelection(self):
		return api.getReviewPosition().copy()

	def _setCursor(self, info):
		api.setReviewPosition(info)

def rindex(seq, item, start, end):
	for index in xrange(end - 1, start - 1, -1):
		if seq[index] == item:
			return index
	raise ValueError("%r is not in sequence" % item)

class BrailleBuffer(baseObject.AutoPropertyObject):

	def __init__(self, handler):
		self.handler = handler
		#: The regions in this buffer.
		#: @type: [L{Region}, ...]
		self.regions = []
		#: The raw text of the entire buffer.
		self.rawText = ""
		#: The position of the cursor in L{brailleCells}, C{None} if no region contains the cursor.
		#: @type: int
		self.cursorPos = None
		#: The translated braille representation of the entire buffer.
		#: @type: [int, ...]
		self.brailleCells = []
		#: The position in L{brailleCells} where the display window starts (inclusive).
		#: @type: int
		self.windowStartPos = 0

	def clear(self):
		"""Clear the entire buffer.
		This removes all regions and resets the window position to 0.
		"""
		self.regions = []
		self.rawText = ""
		self.cursorPos = None
		self.brailleCursorPos = None
		self.brailleCells = []
		self.windowStartPos = 0

	def _get_visibleRegions(self):
		if not self.regions:
			return
		if self.regions[-1].hidePreviousRegions:
			yield self.regions[-1]
			return
		for region in self.regions:
			yield region

	def _get_regionsWithPositions(self):
		start = 0
		for region in self.visibleRegions:
			end = start + len(region.brailleCells)
			yield RegionWithPositions(region, start, end)
			start = end

	_cache_rawToBraillePos=True
	def _get_rawToBraillePos(self):
		"""@return: a list mapping positions in L{rawText} to positions in L{brailleCells} for the entire buffer.
		@rtype: [int, ...]
		"""
		rawToBraillePos = []
		for region, regionStart, regionEnd in self.regionsWithPositions:
			rawToBraillePos.extend(p+regionStart for p in region.rawToBraillePos)
		return rawToBraillePos

	_cache_brailleToRawPos=True
	def _get_brailleToRawPos(self):
		"""@return: a list mapping positions in L{brailleCells} to positions in L{rawText} for the entire buffer.
		@rtype: [int, ...]
		"""
		brailleToRawPos = []
		start = 0
		for region in self.visibleRegions:
			brailleToRawPos.extend(p+start for p in region.brailleToRawPos)
			start+=len(region.rawText)
		return brailleToRawPos

	def bufferPosToRegionPos(self, bufferPos):
		for region, start, end in self.regionsWithPositions:
			if end > bufferPos:
				return region, bufferPos - start
		raise LookupError("No such position")

	def regionPosToBufferPos(self, region, pos, allowNearest=False):
		for testRegion, start, end in self.regionsWithPositions:
			if region == testRegion:
				if pos < end - start:
					# The requested position is still valid within the region.
					return start + pos
				elif allowNearest:
					# The position within the region isn't valid,
					# but the region is valid, so return its start.
					return start
				break
		if allowNearest:
			# Resort to the start of the last region.
			return start
		raise LookupError("No such position")

	def bufferPositionsToRawText(self, startPos, endPos):
		return self.rawText[self.brailleToRawPos[startPos]:self.brailleToRawPos[endPos-1]+1]

	def bufferPosToWindowPos(self, bufferPos):
		if not (self.windowStartPos <= bufferPos < self.windowEndPos):
			raise LookupError("Buffer position not in window")
		return bufferPos - self.windowStartPos

	def _get_windowEndPos(self):
		endPos = self.windowStartPos + self.handler.displaySize
		cellsLen = len(self.brailleCells)
		if endPos >= cellsLen:
			return cellsLen
		if not config.conf["braille"]["wordWrap"]:
			return endPos
		try:
			# Try not to split words across windows.
			# To do this, break after the furthest possible space.
			return min(rindex(self.brailleCells, 0, self.windowStartPos, endPos) + 1,
				endPos)
		except ValueError:
			pass
		return endPos

	def _set_windowEndPos(self, endPos):
		"""Sets the end position for the braille window and recalculates the window start position based on several variables.
		1. Braille display size.
		2. Whether one of the regions should be shown hard left on the braille display;
			i.e. because of The configuration setting for focus context representation 
			or whether the braille region that corresponds with the focus represents a multi line edit box.
		3. Whether word wrap is enabled."""
		startPos = endPos - self.handler.displaySize
		# Loop through the currently displayed regions in reverse order
		# If focusToHardLeft is set for one of the regions, the display shouldn't scroll further back than the start of that region
		for region, regionStart, regionEnd in reversed(list(self.regionsWithPositions)):
			if regionStart<endPos:
				if region.focusToHardLeft:
					# Only scroll to the start of this region.
					restrictPos = regionStart
					break
				elif config.conf["braille"]["focusContextPresentation"]!=CONTEXTPRES_CHANGEDCONTEXT:
					# We aren't currently dealing with context change presentation
					# thus, we only need to consider the last region
					# since it doesn't have focusToHardLeftSet, the window start position isn't restricted
					restrictPos = 0
					break
		else:
			restrictPos = 0
		if startPos <= restrictPos:
			self.windowStartPos = restrictPos
			return
		if not config.conf["braille"]["wordWrap"]:
			self.windowStartPos = startPos
			return
		try:
			# Try not to split words across windows.
			# To do this, break after the furthest possible block of spaces.
			# Find the start of the first block of spaces.
			# Search from 1 cell before in case startPos is just after a space.
			startPos = self.brailleCells.index(0, startPos - 1, endPos)
			# Skip past spaces.
			for startPos in xrange(startPos, endPos):
				if self.brailleCells[startPos] != 0:
					break
		except ValueError:
			pass
		self.windowStartPos = startPos

	def _nextWindow(self):
		oldStart = self.windowStartPos
		end = self.windowEndPos
		if end < len(self.brailleCells):
			self.windowStartPos = end
		return self.windowStartPos != oldStart

	def scrollForward(self):
		if not self._nextWindow():
			# The window could not be scrolled, so try moving to the next line.
			if self.regions:
				self.regions[-1].nextLine()
		else:
			# Scrolling succeeded.
			self.updateDisplay()

	def _previousWindow(self):
		start = self.windowStartPos
		if start > 0:
			self.windowEndPos = start
		return self.windowStartPos != start

	def scrollBack(self):
		if not self._previousWindow():
			# The window could not be scrolled, so try moving to the previous line.
			if self.regions:
				self.regions[-1].previousLine()
		else:
			# Scrolling succeeded.
			self.updateDisplay()

	def scrollTo(self, region, pos):
		pos = self.regionPosToBufferPos(region, pos)
		while pos >= self.windowEndPos:
			if not self._nextWindow():
				break
		while pos < self.windowStartPos:
			if not self._previousWindow():
				break
		self.updateDisplay()

	def focus(self, region):
		"""Bring the specified region into focus.
		The region is placed at the start of the display.
		However, if the region has not set L{Region.focusToHardLeft} and there is extra space at the end of the display, the display is scrolled left so that as much as possible is displayed.
		@param region: The region to focus.
		@type region: L{Region}
		"""
		pos = self.regionPosToBufferPos(region, 0)
		self.windowStartPos = pos
		if region.focusToHardLeft or config.conf["braille"]["focusContextPresentation"]==CONTEXTPRES_SCROLL:
			return
		end = self.windowEndPos
		if end - pos < self.handler.displaySize:
			# We can fit more on the display while still keeping pos visible.
			# Force windowStartPos to be recalculated based on windowEndPos.
			self.windowEndPos = end

	def update(self):
		self.rawText = ""
		self.brailleCells = []
		self.cursorPos = None
		start = 0
		if log.isEnabledFor(log.IO):
			logRegions = []
		for region in self.visibleRegions:
			rawText = region.rawText
			if log.isEnabledFor(log.IO):
				logRegions.append(rawText)
			cells = region.brailleCells
			self.rawText+=rawText
			self.brailleCells.extend(cells)
			if region.brailleCursorPos is not None:
				self.cursorPos = start + region.brailleCursorPos
			start += len(cells)
		if log.isEnabledFor(log.IO):
			log.io("Braille regions text: %r" % logRegions)

	def updateDisplay(self):
		if self is self.handler.buffer:
			self.handler.update()

	def _get_cursorWindowPos(self):
		if self.cursorPos is None:
			return None
		try:
			return self.bufferPosToWindowPos(self.cursorPos)
		except LookupError:
			return None

	def _get_windowRawText(self):
		return self.bufferPositionsToRawText(self.windowStartPos,self.windowEndPos)

	def _get_windowBrailleCells(self):
		return self.brailleCells[self.windowStartPos:self.windowEndPos]

	def routeTo(self, windowPos):
		pos = self.windowStartPos + windowPos
		if pos >= self.windowEndPos:
			return
		region, pos = self.bufferPosToRegionPos(pos)
		region.routeTo(pos)

	def getTextInfoForWindowPos(self, windowPos):
		pos = self.windowStartPos + windowPos
		if pos >= self.windowEndPos:
			return None
		region, pos = self.bufferPosToRegionPos(pos)
		if not isinstance(region, TextInfoRegion):
			return None
		return region.getTextInfoForBraillePos(pos)

	def saveWindow(self):
		"""Save the current window so that it can be restored after the buffer is updated.
		The window start position is saved as a position relative to a region.
		This allows it to be restored even after other regions are added, removed or updated.
		It can be restored with L{restoreWindow}.
		@postcondition: The window is saved and can be restored with L{restoreWindow}.
		"""
		self._savedWindow = self.bufferPosToRegionPos(self.windowStartPos)

	def restoreWindow(self):
		"""Restore the window saved by L{saveWindow}.
		@precondition: L{saveWindow} has been called.
		@postcondition: If the saved position is valid, the window is restored.
			Otherwise, the nearest position is restored.
		"""
		region, pos = self._savedWindow
		self.windowStartPos = self.regionPosToBufferPos(region, pos, allowNearest=True)

_cachedFocusAncestorsEnd = 0
def invalidateCachedFocusAncestors(index):
	"""Invalidate cached focus ancestors from a given index.
	This will cause regions to be generated for the focus ancestors >= index next time L{getFocusContextRegions} is called,
	rather than using cached regions for those ancestors.
	@param index: The index from which cached focus ancestors should be invalidated.
	@type index: int
	"""
	global _cachedFocusAncestorsEnd
	# There could be multiple calls to this function before getFocusContextRegions() is called.
	_cachedFocusAncestorsEnd = min(_cachedFocusAncestorsEnd, index)

def getFocusContextRegions(obj, oldFocusRegions=None):
	global _cachedFocusAncestorsEnd
	# Late import to avoid circular import.
	from treeInterceptorHandler import TreeInterceptor
	ancestors = api.getFocusAncestors()

	ancestorsEnd = len(ancestors)
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
		# We only want the ancestors of the buffer's root NVDAObject.
		if obj != api.getFocusObject():
			# Search backwards through the focus ancestors to find the index of obj.
			for index, ancestor in itertools.izip(xrange(len(ancestors) - 1, 0, -1), reversed(ancestors)):
				if obj == ancestor:
					ancestorsEnd = index
					break

	if oldFocusRegions:
		# We have the regions from the previous focus, so use them as a cache to avoid rebuilding regions which are the same.
		# We need to generate new regions from _cachedFocusAncestorsEnd onwards.
		# However, we must ensure that it is not beyond the last ancestor we wish to consider.
		# Also, we don't ever want to fetch ancestor 0 (the desktop).
		newAncestorsStart = max(min(_cachedFocusAncestorsEnd, ancestorsEnd), 1)
		# Search backwards through the old regions to find the last common region.
		for index, region in itertools.izip(xrange(len(oldFocusRegions) - 1, -1, -1), reversed(oldFocusRegions)):
			ancestorIndex = getattr(region, "_focusAncestorIndex", None)
			if ancestorIndex is None:
				continue
			if ancestorIndex < newAncestorsStart:
				# This is the last common region.
				# An ancestor may have been skipped and not have a region, which means that we need to grab new ancestors from this point.
				newAncestorsStart = ancestorIndex + 1
				commonRegionsEnd = index + 1
				break
		else:
			# No common regions were found.
			commonRegionsEnd = 0
			newAncestorsStart = 1
		# Yield the common regions.
		for region in oldFocusRegions[0:commonRegionsEnd]:
			# We are setting focusToHardLeft to False for every cached region.
			# This is necessary as BrailleHandler._doNewObject checks focusToHardLeft on every region
			# and sets it to True for the first focus region if the context didn't change.
			# If we don't do this, BrailleHandler._doNewObject can't set focusToHardLeft properly.
			region.focusToHardLeft = False
			yield region
	else:
		# Fetch all ancestors.
		newAncestorsStart = 1

	focusToHardLeftSet = False
	for index, parent in enumerate(ancestors[newAncestorsStart:ancestorsEnd], newAncestorsStart):
		if not parent.isPresentableFocusAncestor:
			continue
		region = NVDAObjectRegion(parent, appendText=TEXT_SEPARATOR)
		region._focusAncestorIndex = index
		if config.conf["braille"]["focusContextPresentation"]==CONTEXTPRES_CHANGEDCONTEXT and not focusToHardLeftSet:
			# We are presenting context changes to the user
			# Thus, only scroll back as far as the start of the first new focus ancestor
			# focusToHardLeftSet is used since the first new ancestor isn't always represented by a region
			region.focusToHardLeft = True
			focusToHardLeftSet = True
		region.update()
		yield region

	_cachedFocusAncestorsEnd = ancestorsEnd

def getFocusRegions(obj, review=False):
	# Allow objects to override normal behaviour.
	try:
		regions = obj.getBrailleRegions(review=review)
	except (AttributeError, NotImplementedError):
		pass
	else:
		for region in regions:
			region.update()
			yield region
		return

	# Late import to avoid circular import.
	from treeInterceptorHandler import TreeInterceptor, DocumentTreeInterceptor
	from cursorManager import CursorManager
	from NVDAObjects import NVDAObject
	if isinstance(obj, CursorManager):
		region2 = (ReviewTextInfoRegion if review else CursorManagerRegion)(obj)
	elif isinstance(obj, DocumentTreeInterceptor) or (isinstance(obj,NVDAObject) and NVDAObjectHasUsefulText(obj)): 
		region2 = (ReviewTextInfoRegion if review else TextInfoRegion)(obj)
	else:
		region2 = None
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
	region = NVDAObjectRegion(obj, appendText=TEXT_SEPARATOR if region2 else "")
	region.update()
	yield region
	if region2:
		region2.update()
		yield region2

def formatCellsForLog(cells):
	"""Formats a sequence of braille cells so that it is suitable for logging.
	The output contains the dot numbers for each cell, with each cell separated by a space.
	A C{-} indicates an empty cell.
	@param cells: The cells to format.
	@type cells: sequence of int
	@return: The formatted cells.
	@rtype: str
	"""
	# optimisation: This gets called a lot, so needs to be as efficient as possible.
	# List comprehensions without function calls are faster than loops.
	# For str.join, list comprehensions are faster than generator comprehensions.
	return TEXT_SEPARATOR.join([
		"".join([str(dot + 1) for dot in xrange(8) if cell & (1 << dot)])
		if cell else "-"
		for cell in cells])

class BrailleHandler(baseObject.AutoPropertyObject):
	TETHER_AUTO = "auto"
	TETHER_FOCUS = "focus"
	TETHER_REVIEW = "review"
	tetherValues=[
		# Translators: The label for a braille setting indicating that braille should be
		# tethered to focus or review cursor automatically.
		(TETHER_AUTO,_("automatically")),
		# Translators: The label for a braille setting indicating that braille should be tethered to focus.
		(TETHER_FOCUS,_("to focus")),
		# Translators: The label for a braille setting indicating that braille should be tethered to the review cursor.
		(TETHER_REVIEW,_("to review"))
	]

	def __init__(self):
		self.display = None
		self.displaySize = 0
		self.mainBuffer = BrailleBuffer(self)
		self.messageBuffer = BrailleBuffer(self)
		self._messageCallLater = None
		self.buffer = self.mainBuffer
		#: Whether braille is enabled.
		#: @type: bool
		self.enabled = False
		self._keyCountForLastMessage=0
		self._cursorPos = None
		self._cursorBlinkUp = True
		self._cells = []
		self._cursorBlinkTimer = None
		config.post_configProfileSwitch.register(self.handlePostConfigProfileSwitch)
		self._tether = config.conf["braille"]["tetherTo"]
		self._detectionEnabled = False
		self._detector = None

	def terminate(self):
		bgThreadStopTimeout = 2.5 if self._detectionEnabled else None
		self._disableDetection()
		if self._messageCallLater:
			self._messageCallLater.Stop()
			self._messageCallLater = None
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		config.post_configProfileSwitch.unregister(self.handlePostConfigProfileSwitch)
		if self.display:
			self.display.terminate()
			self.display = None
		_BgThread.stop(timeout=bgThreadStopTimeout)

	def getTether(self):
		return self._tether

	def _get_tether(self):
		"""@deprecated: Use L{getTether instead."""
		return self.getTether()

	def setTether(self, tether, auto=False):
		if auto and not self.shouldAutoTether:
			return
		if not auto:
			config.conf["braille"]["tetherTo"] = tether
		if tether == self._tether:
			return
		self._tether = tether
		self.mainBuffer.clear()

	def _set_tether(self, tether):
		"""@deprecated: Use L{setTether instead."""
		self.setTether(tether, auto=False)

	def _get_shouldAutoTether(self):
		return self.enabled and config.conf["braille"]["autoTether"]

	_lastRequestedDisplayName=None #: the name of the last requested braille display driver with setDisplayByName, even if it failed and has fallen back to no braille.
	def setDisplayByName(self, name, isFallback=False, detected=None):
		if not isFallback:
			# #8032: Take note of the display requested, even if it is going to fail.
			self._lastRequestedDisplayName=name
		if name == AUTO_DISPLAY_NAME:
			self._enableDetection()
			return True
		elif not isFallback and not detected:
			self._disableDetection()

		kwargs = {}
		if detected:
			kwargs["port"]=detected
		else:
			# See if the user has defined a specific port to connect to
			if name not in config.conf["braille"]:
				# No port was set.
				config.conf["braille"][name] = {"port" : ""}
			port = config.conf["braille"][name].get("port")
			# Here we try to keep compatible with old drivers that don't support port setting
			# or situations where the user hasn't set any port.
			if port:
				kwargs["port"] = port

		try:
			newDisplay = _getDisplayDriver(name)
			if detected and bdDetect._isDebug():
				log.debug("Possibly detected display '%s'" % newDisplay.description)
			if newDisplay == self.display.__class__:
				# This is the same driver as was already set, so just re-initialise it.
				log.debug("Reinitializing %s braille display"%name)
				self.display.terminate()
				newDisplay = self.display
				try:
					newDisplay.__init__(**kwargs)
				except TypeError:
					# Re-initialize with supported kwargs.
					extensionPoints.callWithSupportedKwargs(newDisplay.__init__, **kwargs)
			else:
				if newDisplay.isThreadSafe and not detected:
					# Start the thread if it wasn't already.
					# Auto detection implies the thread is already started.
					_BgThread.start()
				try:
					newDisplay = newDisplay(**kwargs)
				except TypeError:
					newDisplay = newDisplay.__new__(newDisplay)
					# initialize with supported kwargs.
					extensionPoints.callWithSupportedKwargs(newDisplay.__init__, **kwargs)
				if self.display:
					log.debug("Switching braille display from %s to %s"%(self.display.name,name))
					try:
						self.display.terminate()
					except:
						log.error("Error terminating previous display driver", exc_info=True)
				self.display = newDisplay
			self.displaySize = newDisplay.numCells
			self.enabled = bool(self.displaySize)
			if isFallback:
				self._resumeDetection()
			elif not detected:
				config.conf["braille"]["display"] = name
			else: # detected:
				self._disableDetection()
			log.info("Loaded braille display driver %s, current display has %d cells." %(name, self.displaySize))
			self.initialDisplay()
			return True
		except:
			# For auto display detection, logging an error for every failure is too obnoxious.
			if not detected:
				log.error("Error initializing display driver for kwargs %r"%kwargs, exc_info=True)
			elif bdDetect._isDebug():
				log.debugWarning("Couldn't initialize display driver for kwargs %r"%(kwargs,), exc_info=True)
			self.setDisplayByName("noBraille", isFallback=True)
			return False

	def _updateDisplay(self):
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		self._cursorBlinkUp = showCursor = config.conf["braille"]["showCursor"]
		self._displayWithCursor()
		if self._cursorPos is None or not showCursor:
			return
		cursorShouldBlink = config.conf["braille"]["cursorBlink"]
		blinkRate = config.conf["braille"]["cursorBlinkRate"]
		if cursorShouldBlink and blinkRate:
			self._cursorBlinkTimer = gui.NonReEntrantTimer(self._blink)
			# This is called from the background thread when a display is auto detected.
			# Make sure we start the blink timer from the main thread to avoid wx assertions
			wx.CallAfter(self._cursorBlinkTimer.Start,blinkRate)

	def _writeCells(self, cells):
		if not self.display.isThreadSafe:
			try:
				self.display.display(cells)
			except:
				log.error("Error displaying cells. Disabling display", exc_info=True)
				self.handleDisplayUnavailable()
			return
		with _BgThread.queuedWriteLock:
			alreadyQueued = _BgThread.queuedWrite
			_BgThread.queuedWrite = cells
		# If a write was already queued, we don't need to queue another;
		# we just replace the data.
		# This means that if multiple writes occur while an earlier write is still in progress,
		# we skip all but the last.
		if not alreadyQueued and not self.display._awaitingAck:
			# Queue a call to the background thread.
			_BgThread.queueApc(_BgThread.executor)

	def _displayWithCursor(self):
		if not self._cells:
			return
		cells = list(self._cells)
		if self._cursorPos is not None and self._cursorBlinkUp:
			if self.tether == self.TETHER_FOCUS:
				cells[self._cursorPos] |= config.conf["braille"]["cursorShapeFocus"]
			else:
				cells[self._cursorPos] |= config.conf["braille"]["cursorShapeReview"]
		self._writeCells(cells)

	def _blink(self):
		self._cursorBlinkUp = not self._cursorBlinkUp
		self._displayWithCursor()

	def update(self):
		cells = self.buffer.windowBrailleCells
		if log.isEnabledFor(log.IO):
			log.io("Braille window dots: %s" % formatCellsForLog(cells))
		# cells might not be the full length of the display.
		# Therefore, pad it with spaces to fill the display.
		self._cells = cells + [0] * (self.displaySize - len(cells))
		self._cursorPos = self.buffer.cursorWindowPos
		self._updateDisplay()

	def scrollForward(self):
		self.buffer.scrollForward()
		if self.buffer is self.messageBuffer:
			self._resetMessageTimer()

	def scrollBack(self):
		self.buffer.scrollBack()
		if self.buffer is self.messageBuffer:
			self._resetMessageTimer()

	def routeTo(self, windowPos):
		self.buffer.routeTo(windowPos)
		if self.buffer is self.messageBuffer:
			self._dismissMessage()

	def getTextInfoForWindowPos(self, windowPos):
		if self.buffer is not self.mainBuffer:
			return None
		return self.buffer.getTextInfoForWindowPos(windowPos)

	def message(self, text):
		"""Display a message to the user which times out after a configured interval.
		The timeout will be reset if the user scrolls the display.
		The message will be dismissed immediately if the user presses a cursor routing key.
		If a key is pressed the message will be dismissed by the next text being written to the display
		@postcondition: The message is displayed.
		"""
		if not self.enabled or config.conf["braille"]["messageTimeout"] == 0:
			return
		if self.buffer is self.messageBuffer:
			self.buffer.clear()
		else:
			self.buffer = self.messageBuffer
		region = TextRegion(text)
		region.update()
		self.buffer.regions.append(region)
		self.buffer.update()
		self.update()
		self._resetMessageTimer()
		self._keyCountForLastMessage=keyboardHandler.keyCounter

	def _resetMessageTimer(self):
		"""Reset the message timeout.
		@precondition: A message is currently being displayed.
		"""
		if config.conf["braille"]["noMessageTimeout"]:
			return
		# Configured timeout is in seconds.
		timeout = config.conf["braille"]["messageTimeout"] * 1000
		if self._messageCallLater:
			self._messageCallLater.Restart(timeout)
		else:
			self._messageCallLater = wx.CallLater(timeout, self._dismissMessage)

	def _dismissMessage(self):
		"""Dismiss the current message.
		@precondition: A message is currently being displayed.
		@postcondition: The display returns to the main buffer.
		"""
		self.buffer.clear()
		self.buffer = self.mainBuffer
		if self._messageCallLater:
			self._messageCallLater.Stop()
			self._messageCallLater = None
		self.update()

	def handleGainFocus(self, obj, shouldAutoTether=True):
		if not self.enabled:
			return
		if shouldAutoTether:
			self.setTether(self.TETHER_FOCUS, auto=True)
		if self._tether != self.TETHER_FOCUS:
			return
		if getattr(obj, "treeInterceptor", None) and not obj.treeInterceptor.passThrough:
			obj = obj.treeInterceptor
		self._doNewObject(itertools.chain(getFocusContextRegions(obj, oldFocusRegions=self.mainBuffer.regions), getFocusRegions(obj)))

	def _doNewObject(self, regions):
		self.mainBuffer.clear()
		focusToHardLeftSet = False
		for region in regions:
			if self.tether == self.TETHER_FOCUS and config.conf["braille"]["focusContextPresentation"]==CONTEXTPRES_CHANGEDCONTEXT:
				# Check focusToHardLeft for every region.
				# If noone of the regions has focusToHardLeft set to True, set it for the first focus region.
				if region.focusToHardLeft:
					focusToHardLeftSet = True
				elif not focusToHardLeftSet and getattr(region, "_focusAncestorIndex", None) is None:
					# Going to display a new object with the same ancestry as the previously displayed object.
					# So, set focusToHardLeft on this region
					# For example, this applies when you are in a list and start navigating through it
					region.focusToHardLeft = True
					focusToHardLeftSet = True
			self.mainBuffer.regions.append(region)
		self.mainBuffer.update()
		# Last region should receive focus.
		self.mainBuffer.focus(region)
		self.scrollToCursorOrSelection(region)
		if self.buffer is self.mainBuffer:
			self.update()
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter>self._keyCountForLastMessage:
			self._dismissMessage()

	def handleCaretMove(self, obj, shouldAutoTether=True):
		if not self.enabled:
			return
		prevTether = self._tether
		if shouldAutoTether:
			self.setTether(self.TETHER_FOCUS, auto=True)
		if self._tether != self.TETHER_FOCUS:
			return
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj==obj:
			region.pendingCaretUpdate=True
		elif prevTether == self.TETHER_REVIEW:
			# The caret moved in a different object than the review position.
			self._doNewObject(getFocusRegions(obj, review=False))

	def handlePendingCaretUpdate(self):
		"""Checks to see if the final text region needs its caret updated and if so calls _doCursorMove for the region."""
		region=self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if isinstance(region,TextInfoRegion) and region.pendingCaretUpdate:
			try:
				self._doCursorMove(region)
			finally:
				region.pendingCaretUpdate=False

	def _doCursorMove(self, region):
		self.mainBuffer.saveWindow()
		region.update()
		self.mainBuffer.update()
		self.mainBuffer.restoreWindow()
		self.scrollToCursorOrSelection(region)
		if self.buffer is self.mainBuffer:
			self.update()
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter>self._keyCountForLastMessage:
			self._dismissMessage()

	def scrollToCursorOrSelection(self, region):
		if region.brailleCursorPos is not None:
			self.mainBuffer.scrollTo(region, region.brailleCursorPos)
		elif not isinstance(region, TextInfoRegion) or not region.obj.isTextSelectionAnchoredAtStart:
			# It is unknown where the selection is anchored, or it is anchored at the end.
			if region.brailleSelectionStart is not None:
				self.mainBuffer.scrollTo(region, region.brailleSelectionStart)
		elif region.brailleSelectionEnd is not None:
			# The selection is anchored at the start.
			self.mainBuffer.scrollTo(region, region.brailleSelectionEnd - 1)

	# #6862: The value change of a progress bar change often goes together with changes of other objects in the dialog,
	# e.g. the time remaining. Therefore, update the dialog when a contained progress bar changes.
	def _handleProgressBarUpdate(self, obj):
		oldTime = getattr(self, "_lastProgressBarUpdateTime", None)
		newTime = time.time()
		if oldTime and newTime - oldTime < 1:
			# Fetching dialog text is expensive, so update at most once a second.
			return
		self._lastProgressBarUpdateTime = newTime
		for obj in reversed(api.getFocusAncestors()[:-1]):
			if obj.role == controlTypes.ROLE_DIALOG:
				self.handleUpdate(obj)
				return

	def handleUpdate(self, obj):
		if not self.enabled:
			return
		# Optimisation: It is very likely that it is the focus object that is being updated.
		# If the focus object is in the braille buffer, it will be the last region, so scan the regions backwards.
		for region in reversed(list(self.mainBuffer.visibleRegions)):
			if hasattr(region, "obj") and region.obj == obj:
				break
		else:
			# No region for this object.
			# There are some objects that require special update behavior even if they have no region.
			# This only applies when tethered to focus, because tethering to review shows only one object at a time,
			# which always has a braille region associated with it.
			if self._tether != self.TETHER_FOCUS:
				return
			# Late import to avoid circular import.
			from NVDAObjects import NVDAObject
			if isinstance(obj, NVDAObject) and obj.role == controlTypes.ROLE_PROGRESSBAR and obj.isInForeground:
				self._handleProgressBarUpdate(obj)
			return
		self.mainBuffer.saveWindow()
		region.update()
		self.mainBuffer.update()
		self.mainBuffer.restoreWindow()
		if self.buffer is self.mainBuffer:
			self.update()
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter>self._keyCountForLastMessage:
			self._dismissMessage()

	def handleReviewMove(self, shouldAutoTether=True):
		if not self.enabled:
			return
		reviewPos = api.getReviewPosition()
		if shouldAutoTether:
			self.setTether(self.TETHER_REVIEW, auto=True)
		if self._tether != self.TETHER_REVIEW:
			return
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj == reviewPos.obj:
			self._doCursorMove(region)
		else:
			# We're reviewing a different object.
			self._doNewObject(getFocusRegions(reviewPos.obj, review=True))

	def initialDisplay(self):
		if not self.enabled or not api.getDesktopObject():
			# Braille is disabled or focus/review hasn't yet been initialised.
			return
		if self.tether == self.TETHER_FOCUS:
			self.handleGainFocus(api.getFocusObject(), shouldAutoTether=False)
		else:
			self.handleReviewMove(shouldAutoTether=False)

	def handlePostConfigProfileSwitch(self):
		display = config.conf["braille"]["display"]
		# Do not choose a new display if:
		if not (
			# The display in the new profile is equal to the last requested display name
			display == self._lastRequestedDisplayName
			# or the new profile uses auto detection, which supports detection of the currently active display.
			or (display == AUTO_DISPLAY_NAME and bdDetect.driverSupportsAutoDetection(self.display.name))
		):
			self.setDisplayByName(display)
		self._tether = config.conf["braille"]["tetherTo"]

	def handleDisplayUnavailable(self):
		"""Called when the braille display becomes unavailable.
		This logs an error and disables the display.
		This is called when displaying cells raises an exception,
		but drivers can also call it themselves if appropriate.
		"""
		log.error("Braille display unavailable. Disabling", exc_info=True)
		self._detectionEnabled = config.conf["braille"]["display"] == AUTO_DISPLAY_NAME
		self.setDisplayByName("noBraille", isFallback=True)

	def _enableDetection(self):
		"""Enables automatic detection of braille displays.
		When auto detection is already active, this will force a rescan for devices.
		"""
		if self._detectionEnabled and self._detector:
			self._detector.rescan()
			return
		_BgThread.start()
		config.conf["braille"]["display"] = AUTO_DISPLAY_NAME
		self.setDisplayByName("noBraille", isFallback=True)
		self._detector = bdDetect.Detector()
		self._detectionEnabled = True

	def _disableDetection(self):
		"""Disables automatic detection of braille displays."""
		if not self._detectionEnabled:
			return
		if self._detector:
			self._detector.terminate()
			self._detector = None
		self._detectionEnabled = False

	def _resumeDetection(self):
		"""Resumes automatic detection of braille displays.
		This is executed when auto detection should be resumed due to loss of display connectivity.
		"""
		if not self._detectionEnabled or self._detector:
			return
		self._detector = bdDetect.Detector()

class _BgThread:
	"""A singleton background thread used for background writes and raw braille display I/O.
	"""

	thread = None
	exit = False
	queuedWrite = None

	@classmethod
	def start(cls):
		if cls.thread:
			return
		cls.queuedWriteLock = threading.Lock()
		thread = cls.thread = threading.Thread(target=cls.func)
		thread.daemon = True
		thread.start()
		cls.handle = ctypes.windll.kernel32.OpenThread(winKernel.THREAD_SET_CONTEXT, False, thread.ident)
		cls.ackTimerHandle = winKernel.createWaitableTimer()

	@classmethod
	def queueApc(cls, func, param=0):
		ctypes.windll.kernel32.QueueUserAPC(func, cls.handle, param)

	@classmethod
	def stop(cls, timeout=None):
		if not cls.thread:
			return
		cls.exit = True
		if not ctypes.windll.kernel32.CancelWaitableTimer(cls.ackTimerHandle):
			raise ctypes.WinError()
		winKernel.closeHandle(cls.ackTimerHandle)
		cls.ackTimerHandle = None
		# Wake up the thread. It will exit when it sees exit is True.
		cls.queueApc(cls.executor)
		cls.thread.join(timeout)
		cls.exit = False
		winKernel.closeHandle(cls.handle)
		cls.handle = None
		cls.thread = None

	@winKernel.PAPCFUNC
	def executor(param):
		if _BgThread.exit:
			# func will see this and exit.
			return
		if not handler.display:
			# Sometimes, the executor is triggered when a display is not fully initialized.
			# For example, this happens when handling an ACK during initialisation.
			# We can safely ignore this.
			return
		if handler.display._awaitingAck:
			# Do not write cells when we are awaiting an ACK
			return
		with _BgThread.queuedWriteLock:
			data = _BgThread.queuedWrite
			_BgThread.queuedWrite = None
		if not data:
			return
		try:
			handler.display.display(data)
		except:
			log.error("Error displaying cells. Disabling display", exc_info=True)
			handler.handleDisplayUnavailable()
		else:
			if handler.display.receivesAckPackets:
				handler.display._awaitingAck = True
				winKernel.setWaitableTimer(
					_BgThread.ackTimerHandle,
					int(handler.display.timeout*2000),
					0,
					_BgThread.ackTimeoutResetter
				)

	@winKernel.PAPCFUNC
	def ackTimeoutResetter(param):
		if handler.display.receivesAckPackets and handler.display._awaitingAck:
			log.debugWarning("Waiting for %s ACK packet timed out"%handler.display.name)
			handler.display._awaitingAck = False
			_BgThread.queueApc(_BgThread.executor)

	@classmethod
	def func(cls):
		while True:
			ctypes.windll.kernel32.SleepEx(winKernel.INFINITE, True)
			if cls.exit:
				break

#: Maps old braille display driver names to new drivers that supersede old drivers.
RENAMED_DRIVERS = {
	"syncBraille":"hims",
	"alvaBC6":"alva"
}

def initialize():
	global handler
	config.addConfigDirsToPythonPackagePath(brailleDisplayDrivers)
	log.info("Using liblouis version %s" % louis.version())
	# #6140: Migrate to new table names as smoothly as possible.
	oldTableName = config.conf["braille"]["translationTable"]
	newTableName = brailleTables.RENAMED_TABLES.get(oldTableName)
	if newTableName:
		config.conf["braille"]["translationTable"] = newTableName
	handler = BrailleHandler()
	# #7459: the syncBraille has been dropped in favor of the native hims driver.
	# Migrate to renamed drivers as smoothly as possible.
	oldDriverName = config.conf["braille"]["display"]
	newDriverName = RENAMED_DRIVERS.get(oldDriverName)
	if newDriverName:
		config.conf["braille"]["display"] = newDriverName
	handler.setDisplayByName(config.conf["braille"]["display"])

def pumpAll():
	"""Runs tasks at the end of each core cycle. For now just caret updates."""
	handler.handlePendingCaretUpdate()

def terminate():
	global handler
	handler.terminate()
	handler = None

class BrailleDisplayDriver(baseObject.AutoPropertyObject):
	"""Abstract base braille display driver.
	Each braille display driver should be a separate Python module in the root brailleDisplayDrivers directory containing a BrailleDisplayDriver class which inherits from this base class.

	At a minimum, drivers must set L{name} and L{description} and override the L{check} method.
	To display braille, L{numCells} and L{display} must be implemented.

	Drivers should dispatch input such as presses of buttons, wheels or other controls using the L{inputCore} framework.
	They should subclass L{BrailleDisplayGesture} and execute instances of those gestures using L{inputCore.manager.executeGesture}.
	These gestures can be mapped in L{gestureMap}.
	A driver can also inherit L{baseObject.ScriptableObject} to provide display specific scripts.

	@see: L{hwIo} for raw serial and HID I/O.
	"""
	#: The name of the braille display; must be the original module file name.
	#: @type: str
	name = ""
	#: A description of the braille display.
	#: @type: str
	description = ""
	#: Whether this driver is thread-safe.
	#: If it is, NVDA may initialize, terminate or call this driver  on any thread.
	#: This allows NVDA to read from and write to the display in the background,
	#: which means the rest of NVDA is not blocked while this occurs,
	#: thus resulting in better performance.
	#: This is also required to use the L{hwIo} module.
	#: @type: bool
	isThreadSafe = False
	#: Whether displays for this driver return acknowledgements for sent packets.
	#: L{_handleAck} should be called when an ACK is received.
	#: Note that thread safety is required for the generic implementation to function properly.
	#: If a display is not thread safe, a driver should manually implement ACK processing.
	#: @type: bool
	receivesAckPackets = False
	#: Whether this driver is awaiting an Ack for a connected display.
	#: This is set to C{True} after displaying cells when L{receivesAckPackets} is True,
	#: and set to C{False} by L{_handleAck} or when C{timeout} has elapsed.
	#: This is for internal use by NVDA core code only and shouldn't be touched by a driver itself.
	_awaitingAck = False
	#: Maximum timeout to use for communication with a device (in seconds).
	#: This can be used for serial connections.
	#: Furthermore, it is used by L{_BgThread} to stop waiting for missed acknowledgement packets.
	#: @type: float
	timeout = 0.2

	@classmethod
	def check(cls):
		"""Determine whether this braille display is available.
		The display will be excluded from the list of available displays if this method returns C{False}.
		For example, if this display is not present, C{False} should be returned.
		@return: C{True} if this display is available, C{False} if not.
		@rtype: bool
		"""
		if cls.isThreadSafe:
			if bdDetect.driverHasPossibleDevices(cls.name):
				return True
			try:
				next(cls.getManualPorts())
			except (StopIteration, NotImplementedError):
				pass
			else:
				return True
		return False

	def terminate(self):
		"""Terminate this display driver.
		This will be called when NVDA is finished with this display driver.
		It should close any open connections, perform cleanup, etc.
		Subclasses should call the superclass method first.
		@postcondition: This instance can no longer be used unless it is constructed again.
		"""
		# Clear the display.
		try:
			self.display([0] * self.numCells)
		except:
			# The display driver seems to be failing, but we're terminating anyway, so just ignore it.
			pass

	def _get_numCells(self):
		"""Obtain the number of braille cells on this  display.
		@note: 0 indicates that braille should be disabled.
		@return: The number of cells.
		@rtype: int
		"""
		return 0

	def display(self, cells):
		"""Display the given braille cells.
		@param cells: The braille cells to display.
		@type cells: [int, ...]
		"""

	#: Automatic port constant to be used by braille displays that support the "automatic" port
	#: Kept for backwards compatibility
	AUTOMATIC_PORT = AUTOMATIC_PORT

	@classmethod
	def getPossiblePorts(cls):
		""" Returns possible hardware ports for this driver.
		Generally, drivers shouldn't implement this method directly.
		Instead, they should provide automatic detection data via L{bdDetect}
		and implement L{getPossibleManualPorts} if they support manual ports
		such as serial ports.
		@return: ordered dictionary of name : description for each port
		@rtype: OrderedDict
		"""
		try:
			next(bdDetect.getConnectedUsbDevicesForDriver(cls.name))
			usb = True
		except (LookupError, StopIteration):
			usb = False
		try:
			next(bdDetect.getPossibleBluetoothDevicesForDriver(cls.name))
			bluetooth = True
		except (LookupError, StopIteration):
			bluetooth = False
		ports = collections.OrderedDict()
		if usb or bluetooth:
			ports.update((AUTOMATIC_PORT,))
			if usb:
				ports.update((USB_PORT,))
			if bluetooth:
				ports.update((BLUETOOTH_PORT,))
		try:
			ports.update(cls.getManualPorts())
		except NotImplementedError:
			pass
		return ports

	@classmethod
	def _getAutoPorts(cls, usb=True, bluetooth=True):
		"""Returns possible ports to connect to using L{bdDetect} automatic detection data.
		@param usb: Whether to search for USB devices.
		@type usb: bool
		@param bluetooth: Whether to search for bluetooth devices.
		@type bluetooth: bool
		@return: The device match for each port.
		@rtype: iterable of L{DeviceMatch}
		"""
		iters = []
		if usb:
			iters.append(bdDetect.getConnectedUsbDevicesForDriver(cls.name))
		if bluetooth:
			iters.append(bdDetect.getPossibleBluetoothDevicesForDriver(cls.name))

		try:
			for match in itertools.chain(*iters):
				yield match
		except LookupError:
			pass

	@classmethod
	def getManualPorts(cls):
		"""Get possible manual hardware ports for this driver.
		This is for ports which cannot be detected automatically
		such as serial ports.
		@return: The name and description for each port.
		@rtype: iterable of basestring, basestring
		"""
		raise NotImplementedError

	@classmethod
	def _getTryPorts(cls, port):
		"""Returns the ports for this driver to which a connection attempt should be made.
		This generator function is usually used in L{__init__} to connect to the desired display.
		@param port: the port to connect to.
		@type port: one of basestring or L{bdDetect.DeviceMatch}
		@return: The name and description for each port.
		@rtype: iterable of basestring, basestring
		"""
		if isinstance(port, bdDetect.DeviceMatch):
			yield port
		elif isinstance(port, basestring):
			isUsb = port in (AUTOMATIC_PORT[0], USB_PORT[0])
			isBluetooth = port in (AUTOMATIC_PORT[0], BLUETOOTH_PORT[0])
			if not isUsb and not isBluetooth:
				# Assume we are connecting to a com port, since these are the only manual ports supported.
				try:
					portInfo = next(info for info in hwPortUtils.listComPorts() if info["port"]==port)
				except StopIteration:
					pass
				else:
					if "bluetoothName" in portInfo:
						yield bdDetect.DeviceMatch(bdDetect.KEY_SERIAL, portInfo["bluetoothName"], portInfo["port"], portInfo)
					else:
						yield bdDetect.DeviceMatch(bdDetect.KEY_SERIAL, portInfo["friendlyName"], portInfo["port"], portInfo)
			else:
				for match in cls._getAutoPorts(usb=isUsb, bluetooth=isBluetooth):
					yield match

	#: Global input gesture map for this display driver.
	#: @type: L{inputCore.GlobalGestureMap}
	gestureMap = None

	@classmethod
	def _getModifierGestures(cls, model=None):
		"""Retrieves modifier gestures from this display driver's L{gestureMap}
		that are bound to modifier only keyboard emulate scripts.
		@param model: the optional braille display model for which modifier gestures should also be included.
		@type model: str; C{None} if model specific gestures should not be included
		@return: the ids of the display keys and the associated generalised modifier names
		@rtype: generator of (set, set)
		"""
		import globalCommands
		# Ignore the locale gesture map when searching for braille display gestures
		globalMaps = [inputCore.manager.userGestureMap]
		if cls.gestureMap:
			globalMaps.append(cls.gestureMap)
		prefixes=["br({source})".format(source=cls.name),]
		if model:
			prefixes.insert(0,"br({source}.{model})".format(source=cls.name, model=model))
		for globalMap in globalMaps:
			for scriptCls, gesture, scriptName in globalMap.getScriptsForAllGestures():
				if (any(gesture.startswith(prefix.lower()) for prefix in prefixes)
					and scriptCls is globalCommands.GlobalCommands
					and scriptName and scriptName.startswith("kb")):
					emuGesture = keyboardHandler.KeyboardInputGesture.fromName(scriptName.split(":")[1])
					if emuGesture.isModifier:
						yield set(gesture.split(":")[1].split("+")), set(emuGesture._keyNamesInDisplayOrder)

	def _handleAck(self):
		"""Base implementation to handle acknowledgement packets."""
		if not self.receivesAckPackets:
			raise NotImplementedError("This display driver does not support ACK packet handling")
		if not ctypes.windll.kernel32.CancelWaitableTimer(_BgThread.ackTimerHandle):
			raise ctypes.WinError()
		self._awaitingAck = False
		_BgThread.queueApc(_BgThread.executor)

class BrailleDisplayGesture(inputCore.InputGesture):
	"""A button, wheel or other control pressed on a braille display.
	Subclasses must provide L{source} and L{id}.
	Optionally, L{model} can be provided to facilitate model specific gestures.
	L{routingIndex} should be provided for routing buttons.
	Subclasses can also inherit from L{brailleInput.BrailleInputGesture} if the display has a braille keyboard.
	If the braille display driver is a L{baseObject.ScriptableObject}, it can provide scripts specific to input gestures from this display.
	"""

	def _get_source(self):
		"""The string used to identify all gestures from this display.
		This should generally be the driver name.
		This string will be included in the source portion of gesture identifiers.
		For example, if this was C{alvaBC6},
		a display specific gesture identifier might be C{br(alvaBC6):etouch1}.
		@rtype: str
		"""
		raise NotImplementedError

	def _get_model(self):
		"""The string used to identify all gestures from a specific braille display model.
		This should be an alphanumeric short version of the model name, without spaces.
		This string will be included in the source portion of gesture identifiers.
		For example, if this was C{alvaBC6},
		the model string could look like C{680},
		and a corresponding display specific gesture identifier might be C{br(alvaBC6.680):etouch1}.
		@rtype: str; C{None} if model specific gestures are not supported
		"""
		return None

	def _get_id(self):
		"""The unique, display specific id for this gesture.
		@rtype: str
		"""
		raise NotImplementedError

	#: The index of the routing key or C{None} if this is not a routing key.
	#: @type: int
	routingIndex = None

	def _get_identifiers(self):
		ids = [u"br({source}):{id}".format(source=self.source, id=self.id)]
		if self.model:
			# Model based ids should take priority.
			ids.insert(0, u"br({source}.{model}):{id}".format(source=self.source, model=self.model, id=self.id))
		import brailleInput
		if isinstance(self, brailleInput.BrailleInputGesture):
			ids.extend(brailleInput.BrailleInputGesture._get_identifiers(self))
		return ids

	def _get_displayName(self):
		import brailleInput
		if isinstance(self, brailleInput.BrailleInputGesture):
			name = brailleInput.BrailleInputGesture._get_displayName(self)
			if name:
				return name
		return self.id

	def _get_scriptableObject(self):
		display = handler.display
		if isinstance(display, baseObject.ScriptableObject):
			return display
		return super(BrailleDisplayGesture, self).scriptableObject

	def _get_script(self):
		# Overrides L{inputCore.InputGesture._get_script} to support modifier keys.
		# Also processes modifiers held by braille input.
		# Import late to avoid circular import.
		import brailleInput
		gestureKeys = set(self.keyNames)
		gestureModifiers = brailleInput.handler.currentModifiers.copy()
		script=scriptHandler.findScript(self)
		if script:
			scriptName = script.__name__
			if not (gestureModifiers and scriptName.startswith("script_kb:")):
				self.script = script
				return self.script
		# Either no script for this gesture has been found, or braille input is holding modifiers.
		# Process this gesture for possible modifiers if it consists of more than one key.
		# For example, if L{self.id} is 'key1+key2',
		# key1 is bound to 'kb:control' and key2 to 'kb:tab',
		# this gesture should execute 'kb:control+tab'.
		# Combining emulated modifiers with braille input (#7306) is not yet supported.
		if len(gestureKeys)>1:
			for keys, modifiers in handler.display._getModifierGestures(self.model):
				if keys<gestureKeys:
					gestureModifiers |= modifiers
					gestureKeys -= keys
		if not gestureModifiers:
			return None
		if gestureKeys != set(self.keyNames):
			# Find a script for L{gestureKeys}.
			id = "+".join(gestureKeys)
			fakeGestureIds = [u"br({source}):{id}".format(source=self.source, id=id),]
			if self.model:
				fakeGestureIds.insert(0,u"br({source}.{model}):{id}".format(source=self.source, model=self.model, id=id))
			scriptNames = []
			globalMaps = [inputCore.manager.userGestureMap, handler.display.gestureMap]
			for globalMap in globalMaps:
				for fakeGestureId in fakeGestureIds:
					scriptNames.extend(scriptName for cls, scriptName in globalMap.getScriptsForGesture(fakeGestureId.lower()) if scriptName and scriptName.startswith("kb"))
			if not scriptNames:
				# Gesture contains modifiers, but no keyboard emulate script exists for the gesture without modifiers
				return None
			# We can't bother about multiple scripts for a gesture, we will just use the first one
			combinedScriptName = "kb:{modifiers}+{keys}".format(
				modifiers="+".join(gestureModifiers),
				keys=scriptNames[0].split(":")[1]
			)
		elif script and scriptName:
			combinedScriptName = "kb:{modifiers}+{keys}".format(
				modifiers="+".join(gestureModifiers),
				keys=scriptName.split(":")[1]
			)
		else:
			return None
		self.script = scriptHandler._makeKbEmulateScript(combinedScriptName)
		brailleInput.handler.currentModifiers.clear()
		return self.script

	def _get_keyNames(self):
		"""The names of the keys that are part of this gesture.
		@rtype: list
		"""
		return self.id.split("+")

	#: Compiled regular expression to match an identifier including an optional model name
	#: The model name should be an alphanumeric string without spaces.
	#: @type: RegexObject
	ID_PARTS_REGEX = re.compile(r"br\((\w+)(?:\.(\w+))?\):([\w+]+)", re.U)

	@classmethod
	def getDisplayTextForIdentifier(cls, identifier):
		# Translators: Displayed when the source driver of a braille display gesture is unknown.
		unknownDisplayDescription = _("Unknown braille display")
		idParts = cls.ID_PARTS_REGEX.match(identifier)
		if not idParts:
			log.error("Invalid braille gesture identifier: %s"%identifier)
			return unknownDisplayDescription, "malformed:%s"%identifier
		source, modelName, key = idParts.groups()
		# Optimisation: Do not try to get the braille display class if this identifier belongs to the current driver.
		if handler.display.name.lower() == source.lower():
			description = handler.display.description
		else:
			try:
				description = _getDisplayDriver(source, caseSensitive=False).description
			except ImportError:
				description = unknownDisplayDescription
		if modelName: # The identifier contains a model name
			return description, "{modelName}: {key}".format(
				modelName=modelName, key=key
			)
		else:
			return description, key

inputCore.registerGestureSource("br", BrailleDisplayGesture)


def getSerialPorts(filterFunc=None):
	"""Get available serial ports in a format suitable for L{BrailleDisplayDriver.getManualPorts}.
	@param filterFunc: a function executed on every dictionary retrieved using L{hwPortUtils.listComPorts}.
		For example, this can be used to filter by USB or Bluetooth com ports.
	@type filterFunc: callable
	"""
	if filterFunc and not callable(filterFunc):
		raise ValueError("The provided filterFunc is not callable")
	for info in hwPortUtils.listComPorts():
		if filterFunc and not filterFunc(info):
			continue
		if "bluetoothName" in info:
			yield (info["port"],
				# Translators: Name of a Bluetooth serial communications port.
				_("Bluetooth Serial: {port} ({deviceName})").format(
					port=info["port"],
					deviceName=info["bluetoothName"]
				))
		else:
			yield (info["port"],
				# Translators: Name of a serial communications port.
				_("Serial: {portName}").format(portName=info["friendlyName"]))
