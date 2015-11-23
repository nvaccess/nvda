#braille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2014 NV Access Limited

import itertools
import os
import pkgutil
import wx
import louis
import keyboardHandler
import baseObject
import config
from logHandler import log
import controlTypes
import api
import textInfos
import brailleDisplayDrivers
import inputCore

#: The directory in which liblouis braille tables are located.
TABLES_DIR = r"louis\tables"

#: The table file names and information.
TABLES = (
	# (fileName, displayName, supportsInput),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ar-ar-g1.utb", _("Arabic grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ar-fa.utb", _("Farsi grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("as-in-g1.utb", _("Assamese grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("be-in-g1.utb", _("Bengali grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("bg.ctb", _("Bulgarian 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("cy-cy-g1.utb", _("Welsh grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("cy-cy-g2.ctb", _("Welsh grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("cz-cz-g1.utb", _("Czech grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("da-dk-g16.utb", _("Danish 6 dot grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("da-dk-g18.utb", _("Danish 8 dot grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("da-dk-g26.ctb", _("Danish 6 dot grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("da-dk-g28.ctb", _("Danish 8 dot grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("de-de-comp8.ctb", _("German 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("de-de-g0.utb", _("German grade 0"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("de-de-g1.ctb", _("German grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("de-de-g2.ctb", _("German grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("en-gb-comp8.ctb", _("English (U.K.) 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("en-gb-g1.utb", _("English (U.K.) grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("en-GB-g2.ctb", _("English (U.K.) grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("en-us-comp6.ctb", _("English (U.S.) 6 dot computer braille"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("en-us-comp8.ctb", _("English (U.S.) 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("en-us-g1.ctb", _("English (U.S.) grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("en-us-g2.ctb", _("English (U.S.) grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("Es-Es-G0.utb", _("Spanish 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("es-g1.ctb", _("Spanish grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("et-g0.utb", _("Estonian grade 0"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ethio-g1.ctb", _("Ethiopic grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("fi.utb", _("Finnish 6 dot"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("fi-fi-8dot.ctb", _("Finnish 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("fr-bfu-comp6.utb", _("French (unified) 6 dot computer braille"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("fr-bfu-comp8.utb", _("French (unified) 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("fr-bfu-g2.ctb", _("French (unified) Grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("fr-ca-g1.utb", _("French (Canada) grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("Fr-Ca-g2.ctb", _("French (Canada) grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ga-g1.utb", _("Irish grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ga-g2.ctb", _("Irish grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("gu-in-g1.utb", _("Gujarati grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("gr-gr-g1.utb", _("Greek (Greece) grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("he.ctb", _("Hebrew 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("hi-in-g1.utb", _("Hindi grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("hr.ctb", _("Croatian 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("hu-hu-comp8.ctb", _("Hungarian 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("hu-hu-g1.ctb", _("Hungarian grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("is.ctb", _("Icelandic 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("it-it-comp6.utb", _("Italian 6 dot computer braille"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("it-it-comp8.utb", _("Italian 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ka-in-g1.utb", _("Kannada grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ko-2006-g1.ctb", _("Korean grade 1 (2006)"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ko-2006-g2.ctb", _("Korean grade 2 (2006)"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ko-g1.ctb", _("Korean grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ko-g2.ctb", _("Korean grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ks-in-g1.utb", _("Kashmiri grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("Lv-Lv-g1.utb", _("Latvian grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ml-in-g1.utb", _("Malayalam grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("mn-in-g1.utb", _("Manipuri grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("mr-in-g1.utb", _("Marathi grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("nl-BE-g1.ctb", _("Dutch (Belgium) grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("nl-NL-g1.ctb", _("Dutch (Netherlands) grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("no-no.ctb", _("Norwegian 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("No-No-g0.utb", _("Norwegian grade 0"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("No-No-g1.ctb", _("Norwegian grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("No-No-g2.ctb", _("Norwegian grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("No-No-g3.ctb", _("Norwegian grade 3"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("np-in-g1.utb", _("Nepali grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("or-in-g1.utb", _("Oriya grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("Pl-Pl-g1.utb", _("Polish grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("pt-pt-comp8.ctb", _("Portuguese 8 dot computer braille"), True),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("Pt-Pt-g1.utb", _("Portuguese grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("Pt-Pt-g2.ctb", _("Portuguese grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("pu-in-g1.utb", _("Punjabi grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ru-compbrl.ctb", _("Russian braille for computer code"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ru-ru-g1.utb", _("Russian grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("sa-in-g1.utb", _("Sanskrit grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("Se-Se-g1.utb", _("Swedish grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("sk-sk-g1.utb", _("Slovak grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("sl-si-g1.utb", _("Slovene grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("sr-g1.ctb", _("Serbian grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("ta-ta-g1.ctb", _("Tamil grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("te-in-g1.utb", _("Telegu grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("tr.ctb", _("Turkish grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("UEBC-g1.utb", _("Unified English Braille Code grade 1"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("UEBC-g2.ctb", _("Unified English Braille Code grade 2"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("zh-hk.ctb", _("Chinese (Hong Kong, Cantonese)"), False),
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	("zh-tw.ctb", _("Chinese (Taiwan, Mandarin)"), False),
)

#: Braille tables that support input (only computer braille tables yet).
INPUT_TABLES = tuple(t for t in TABLES if t[2])

roleLabels = {
	# Translators: Displayed in braille for an object which is an
	# editable text field.
	controlTypes.ROLE_EDITABLETEXT: _("edt"),
	# Translators: Displayed in braille for an object which is a
	# list.
	controlTypes.ROLE_LIST: _("lst"),
	# Translators: Displayed in braille for an object which is a
	# menu bar.
	controlTypes.ROLE_MENUBAR: _("mnubar"),
	# Translators: Displayed in braille for an object which is a
	# menu.
	controlTypes.ROLE_POPUPMENU: _("mnu"),
	# Translators: Displayed in braille for an object which is a
	# button.
	controlTypes.ROLE_BUTTON: _("btn"),
	# Translators: Displayed in braille for an object which is a
	# check box.
	controlTypes.ROLE_CHECKBOX: _("chk"),
	# Translators: Displayed in braille for an object which is a
	# radio button.
	controlTypes.ROLE_RADIOBUTTON: _("rbtn"),
	# Translators: Displayed in braille for an object which is a
	# combo box.
	controlTypes.ROLE_COMBOBOX: _("cbo"),
	# Translators: Displayed in braille for an object which is a
	# link.
	controlTypes.ROLE_LINK: _("lnk"),
	# Translators: Displayed in braille for an object which is a
	# dialog.
	controlTypes.ROLE_DIALOG: _("dlg"),
	# Translators: Displayed in braille for an object which is a
	# tree view.
	controlTypes.ROLE_TREEVIEW: _("tv"),
	# Translators: Displayed in braille for an object which is a
	# table.
	controlTypes.ROLE_TABLE: _("tb"),
	# Translators: Displayed in braille for an object which is a
	# separator.
	controlTypes.ROLE_SEPARATOR: _("-----"),
	# Translators: Displayed in braille for an object which is a
	# graphic.
	controlTypes.ROLE_GRAPHIC: _("gra"),
}

positiveStateLabels = {
	# Translators: Displayed in braille when an object (e.g. a check box) is checked.
	controlTypes.STATE_CHECKED: _("(x)"),
	# Translators: Displayed in braille when an object (e.g. a check box) is half checked.
	controlTypes.STATE_HALFCHECKED: _("(-)"),
	# Translators: Displayed in braille when an object is selected.
	controlTypes.STATE_SELECTED: _("sel"),
	# Translators: Displayed in braille when an object has a popup (usually a sub-menu).
	controlTypes.STATE_HASPOPUP: _("submnu"),
	# Translators: Displayed in braille when an object supports autocompletion.
	controlTypes.STATE_AUTOCOMPLETE: _("..."),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is expanded.
	controlTypes.STATE_EXPANDED: _("-"),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is collapsed.
	controlTypes.STATE_COLLAPSED: _("+"),
	# Translators: Displayed in braille when an object (e.g. an editable text field) is read-only.
	controlTypes.STATE_READONLY: _("ro"),
	# Translators: Displayed in braille when an object is clickable.
	controlTypes.STATE_CLICKABLE: _("clk"),
}
negativeStateLabels = {
	# Translators: Displayed in braille when an object (e.g. a check box) is not checked.
	controlTypes.STATE_CHECKED: _("( )"),
}

DOT7 = 64
DOT8 = 128

def NVDAObjectHasUsefulText(obj):
	import displayModel
	role = obj.role
	states = obj.states
	return (issubclass(obj.TextInfo,displayModel.DisplayModelTextInfo)
		or role in (controlTypes.ROLE_EDITABLETEXT, controlTypes.ROLE_TERMINAL)
		or controlTypes.STATE_EDITABLE in states
		or (role == controlTypes.ROLE_DOCUMENT and controlTypes.STATE_READONLY not in obj.states))

def _getDisplayDriver(name):
	return __import__("brailleDisplayDrivers.%s" % name, globals(), locals(), ("brailleDisplayDrivers",)).BrailleDisplayDriver

def getDisplayList():
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
			if display.check():
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
	The region is responsible for retrieving its text and cursor position, translating it into braille cells and handling cursor routing requests relative to its braille cells.
	The L{BrailleBuffer} containing this region will call L{update} and expect that L{brailleCells} and L{brailleCursorPos} will be set appropriately.
	L{routeTo} will be called to handle a cursor routing request.
	"""

	def __init__(self):
		#: The original, raw text of this region.
		self.rawText = ""
		#: The position of the cursor in L{rawText}, C{None} if the cursor is not in this region.
		#: @type: int
		self.cursorPos = None
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
		#: Whether to hide all previous regions.
		#: @type: bool
		self.hidePreviousRegions = False
		#: Whether this region should be positioned at the absolute left of the display when focused.
		#: @type: bool
		self.focusToHardLeft = False

	def update(self):
		"""Update this region.
		Subclasses should extend this to update L{rawText} and L{cursorPos} if necessary.
		The base class method handles translation of L{rawText} into braille, placing the result in L{brailleCells}.
		Typeform information from L{rawTextTypeforms} is used, if any.
		L{rawToBraillePos} and L{brailleToRawPos} are updated according to the translation.
		L{brailleCursorPos} is similarly updated based on L{cursorPos}.
		@postcondition: L{brailleCells} and L{brailleCursorPos} are updated and ready for rendering.
		"""
		mode = louis.dotsIO | louis.pass1Only
		if config.conf["braille"]["expandAtCursor"] and self.cursorPos is not None:
			mode |= louis.compbrlAtCursor
		text=unicode(self.rawText).replace('\0','')
		braille, self.brailleToRawPos, self.rawToBraillePos, brailleCursorPos = louis.translate(
			[os.path.join(TABLES_DIR, config.conf["braille"]["translationTable"]),
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
	states = propertyValues.get("states")
	positionInfo = propertyValues.get("positionInfo")
	level = positionInfo.get("level") if positionInfo else None
	cellCoordsText=propertyValues.get('cellCoordsText')
	rowNumber = propertyValues.get("rowNumber")
	columnNumber = propertyValues.get("columnNumber")
	includeTableCellCoords = propertyValues.get("includeTableCellCoords", True)
	if role is not None:
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
	else:
		role = propertyValues.get("_role")
		roleText = None
	value = propertyValues.get("value")
	if value and role not in controlTypes.silentValuesForRoles:
		textList.append(value)
	if states:
		positiveStates = controlTypes.processPositiveStates(role, states, controlTypes.REASON_FOCUS, states)
		textList.extend(positiveStateLabels.get(state, controlTypes.stateLabels[state]) for state in positiveStates)
		negativeStates = controlTypes.processNegativeStates(role, states, controlTypes.REASON_FOCUS, None)
		textList.extend(negativeStateLabels.get(state, controlTypes.negativeStateLabels.get(state, _("not %s") % controlTypes.stateLabels[state])) for state in negativeStates)
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
			# Translators: Displayed in braille for a table cell row number.
			# %s is replaced with the row number.
			textList.append(_("r%s") % rowNumber)
	if columnNumber:
		columnHeaderText = propertyValues.get("columnHeaderText")
		if columnHeaderText:
			textList.append(columnHeaderText)
		if includeTableCellCoords and not cellCoordsText:
			# Translators: Displayed in braille for a table cell column number.
			# %s is replaced with the column number.
			textList.append(_("c%s") % columnNumber)
	if includeTableCellCoords and  cellCoordsText:
		textList.append(cellCoordsText)
	return " ".join([x for x in textList if x])

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
		text = getBrailleTextForProperties(name=obj.name, role=role,
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
					text += " " + mathPres.brailleProvider.getBrailleForMathMl(
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

	if presCat == field.PRESCAT_LAYOUT:
		# The only item we report for these fields is clickable, if present.
		if controlTypes.STATE_CLICKABLE in states:
			return getBrailleTextForProperties(states={controlTypes.STATE_CLICKABLE})
		return None

	elif role in (controlTypes.ROLE_TABLECELL, controlTypes.ROLE_TABLECOLUMNHEADER, controlTypes.ROLE_TABLEROWHEADER) and field.get("table-id"):
		# Table cell.
		reportTableHeaders = formatConfig["reportTableHeaders"]
		reportTableCellCoords = formatConfig["reportTableCellCoords"]
		props = {
			"states": states,
			"rowNumber": field.get("table-rownumber"),
			"columnNumber": field.get("table-columnnumber"),
			"includeTableCellCoords": reportTableCellCoords
		}
		if reportTableHeaders:
			props["columnHeaderText"] = field.get("table-columnheadertext")
		return getBrailleTextForProperties(**props)

	elif reportStart:
		props = {
			# Don't report the role for math here.
			# However, we still need to pass it (hence "_role").
			"_role" if role == controlTypes.ROLE_MATH else "role": role,
			"states": states,"value":value}
		if config.conf["presentation"]["reportKeyboardShortcuts"]:
			kbShortcut = field.get("keyboardShortcut")
			if kbShortcut:
				props["keyboardShortcut"] = kbShortcut
		level = field.get("level")
		if level:
			props["positionInfo"] = {"level": level}
		text = getBrailleTextForProperties(**props)
		if role == controlTypes.ROLE_MATH:
			import mathPres
			mathPres.ensureInit()
			if mathPres.brailleProvider:
				try:
					if text:
						text += " "
					text += mathPres.brailleProvider.getBrailleForMathMl(
						info.getMathMl(field))
				except (NotImplementedError, LookupError):
					pass
		return text
	else:
		# Translators: Displayed in braille at the end of a control field such as a list or table.
		# %s is replaced with the control's role.
		return (_("%s end") %
			getBrailleTextForProperties(role=role))

def getFormatFieldBraille(field):
	linePrefix = field.get("line-prefix")
	if linePrefix:
		return linePrefix
	return None

class TextInfoRegion(Region):

	pendingCaretUpdate=False #: True if the cursor should be updated for this region on the display

	def __init__(self, obj):
		super(TextInfoRegion, self).__init__()
		self.obj = obj

	def _isMultiline(self):
		# A region's object can either be an NVDAObject or a tree interceptor.
		# Tree interceptors should always be multiline.
		from treeInterceptorHandler import TreeInterceptor
		if isinstance(self.obj, TreeInterceptor):
			return True
		# Terminals are inherently multiline, so they don't have the multiline state.
		return (self.obj.role == controlTypes.ROLE_TERMINAL or controlTypes.STATE_MULTILINE in self.obj.states)

	def _getCursor(self):
		"""Retrieve the collapsed cursor.
		This should be the start or end of the selection returned by L{_getSelection}.
		@return: The cursor.
		"""
		try:
			return self.obj.makeTextInfo(textInfos.POSITION_CARET)
		except:
			return self.obj.makeTextInfo(textInfos.POSITION_FIRST)

	def _getSelection(self):
		"""Retrieve the selection.
		The start or end of this should be the cursor returned by L{_getCursor}.
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

	def _getTypeformFromFormatField(self, field):
		typeform = louis.plain_text
		if field.get("bold", False):
			typeform |= louis.bold
		if field.get("italic", False):
			typeform |= louis.italic
		if field.get("underline", False):
			typeform |= louis.underline
		return typeform

	def _addFieldText(self, text, contentPos):
		if self.rawText:
			# Separate this field text from the rest of the text.
			text = " " + text
		self.rawText += text
		textLen = len(text)
		self.rawTextTypeforms.extend((louis.plain_text,) * textLen)
		self._rawToContentPos.extend((contentPos,) * textLen)

	def _addTextWithFields(self, info, formatConfig, isSelection=False):
		shouldMoveCursorToFirstContent = not isSelection and self.cursorPos is not None
		ctrlFields = []
		typeform = louis.plain_text
		for command in info.getTextWithFields(formatConfig=formatConfig):
			if isinstance(command, basestring):
				if not command:
					continue
				if self._endsWithField:
					# The last item added was a field,
					# so add a space before the content.
					self.rawText += " "
					self.rawTextTypeforms.append(louis.plain_text)
					self._rawToContentPos.append(self._currentContentPos)
				if isSelection and self._selectionStart is None:
					# This is where the content begins.
					self._selectionStart = len(self.rawText)
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
					self._selectionEnd = len(self.rawText)
				self._endsWithField = False
			elif isinstance(command, textInfos.FieldCommand):
				cmd = command.command
				field = command.field
				if cmd == "formatChange":
					typeform = self._getTypeformFromFormatField(field)
					text = getFormatFieldBraille(field)
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
						if isSelection and self._selectionStart is None:
							self._selectionStart = fieldStart
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
		if isSelection and self._selectionStart is None:
			# There is no selection. This is a cursor.
			self.cursorPos = len(self.rawText)
		if not self._skipFieldsNotAtStartOfNode:
			# We only render fields that aren't at the start of their nodes for the first part of the reading unit.
			# Otherwise, we'll render fields that have already been rendered.
			self._skipFieldsNotAtStartOfNode = True

	def _getReadingUnit(self):
		return textInfos.UNIT_PARAGRAPH if config.conf["braille"]["readByParagraph"] else textInfos.UNIT_LINE

	def update(self):
		formatConfig = config.conf["documentFormatting"]
		unit = self._getReadingUnit()
		# HACK: Some TextInfos only support UNIT_LINE properly if they are based on POSITION_CARET,
		# so use the original cursor TextInfo for line and copy for cursor.
		self._readingInfo = readingInfo = self._getCursor()
		cursor = readingInfo.copy()
		# Get the reading unit at the cursor.
		readingInfo.expand(unit)
		# Get the selection.
		sel = self._getSelection()
		# Restrict the selection to the reading unit at the cursor.
		if sel.compareEndPoints(readingInfo, "startToStart") < 0:
			sel.setEndPoint(readingInfo, "startToStart")
		if sel.compareEndPoints(readingInfo, "endToEnd") > 0:
			sel.setEndPoint(readingInfo, "endToEnd")
		self.rawText = ""
		self.rawTextTypeforms = []
		self.cursorPos = None
		# The output includes text representing fields which isn't part of the real content in the control.
		# Therefore, maintain a map of positions in the output to positions in the content.
		self._rawToContentPos = []
		self._currentContentPos = 0
		self._selectionStart = self._selectionEnd = None
		self._skipFieldsNotAtStartOfNode = False
		self._endsWithField = False

		# Not all text APIs support offsets, so we can't always get the offset of the selection relative to the start of the reading unit.
		# Therefore, grab the reading unit in three parts.
		# First, the chunk from the start of the reading unit to the start of the selection.
		chunk = readingInfo.copy()
		chunk.collapse()
		chunk.setEndPoint(sel, "endToStart")
		self._addTextWithFields(chunk, formatConfig)
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
			self.rawText += " "
			rawTextLen += 1
			self.rawTextTypeforms.append(louis.plain_text)
			self._rawToContentPos.append(self._currentContentPos)
		if self.cursorPos is not None and self.cursorPos >= rawTextLen:
			self.cursorPos = rawTextLen - 1

		# If this is not the start of the object, hide all previous regions.
		start = cursor.obj.makeTextInfo(textInfos.POSITION_FIRST)
		self.hidePreviousRegions = (start.compareEndPoints(readingInfo, "startToStart") < 0)
		# If this is a multiline control, position it at the absolute left of the display when focused.
		self.focusToHardLeft = self._isMultiline()
		super(TextInfoRegion, self).update()

		if self._selectionStart is not None:
			# Mark the selection with dots 7 and 8.
			if self._selectionEnd >= len(self.rawText):
				brailleSelEnd = len(self.brailleCells)
			else:
				brailleSelEnd = self.rawToBraillePos[self._selectionEnd]
			for pos in xrange(self.rawToBraillePos[self._selectionStart], brailleSelEnd):
				self.brailleCells[pos] |= DOT7 | DOT8

	def routeTo(self, braillePos):
		if braillePos == self.brailleCursorPos:
			# The cursor is already at this position,
			# so activate the position.
			try:
				self._getCursor().activate()
			except NotImplementedError:
				pass
			return

		pos = self._rawToContentPos[self.brailleToRawPos[braillePos]]
		# pos is relative to the start of the reading unit.
		# Therefore, get the start of the reading unit...
		dest = self._readingInfo.copy()
		dest.collapse()
		# and move pos characters from there.
		dest.move(textInfos.UNIT_CHARACTER, pos)
		self._setCursor(dest)

	def nextLine(self):
		dest = self._readingInfo.copy()
		moved = dest.move(self._getReadingUnit(), 1)
		if not moved:
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

	def _getCursor(self):
		return api.getReviewPosition().copy()

	_getSelection = _getCursor

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
			yield region, start, end
			start = end

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
		startPos = endPos - self.handler.displaySize
		# Get the last region currently displayed.
		region, regionPos = self.bufferPosToRegionPos(endPos - 1)
		if region.focusToHardLeft:
			# Only scroll to the start of this region.
			restrictPos = endPos - regionPos - 1
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
		if region.focusToHardLeft:
			return
		end = self.windowEndPos
		if end - pos < self.handler.displaySize:
			# We can fit more on the display while still keeping pos visible.
			# Force windowStartPos to be recalculated based on windowEndPos.
			self.windowEndPos = end

	def update(self):
		self.brailleCells = []
		self.cursorPos = None
		start = 0
		if log.isEnabledFor(log.IO):
			logRegions = []
		for region in self.visibleRegions:
			if log.isEnabledFor(log.IO):
				logRegions.append(region.rawText)
			cells = region.brailleCells
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

	def _get_windowBrailleCells(self):
		return self.brailleCells[self.windowStartPos:self.windowEndPos]

	def routeTo(self, windowPos):
		pos = self.windowStartPos + windowPos
		if pos >= self.windowEndPos:
			return
		region, pos = self.bufferPosToRegionPos(pos)
		region.routeTo(pos)

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
			yield region
	else:
		# Fetch all ancestors.
		newAncestorsStart = 1

	for index, parent in enumerate(ancestors[newAncestorsStart:ancestorsEnd], newAncestorsStart):
		if not parent.isPresentableFocusAncestor:
			continue
		region = NVDAObjectRegion(parent, appendText=" ")
		region._focusAncestorIndex = index
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
	from treeInterceptorHandler import TreeInterceptor
	from cursorManager import CursorManager
	if isinstance(obj, CursorManager):
		region2 = (ReviewTextInfoRegion if review else CursorManagerRegion)(obj)
	elif isinstance(obj, TreeInterceptor) or NVDAObjectHasUsefulText(obj): 
		region2 = (ReviewTextInfoRegion if review else TextInfoRegion)(obj)
	else:
		region2 = None
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
	region = NVDAObjectRegion(obj, appendText=" " if region2 else "")
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
	return " ".join([
		"".join([str(dot + 1) for dot in xrange(8) if cell & (1 << dot)])
		if cell else "-"
		for cell in cells])

class BrailleHandler(baseObject.AutoPropertyObject):
	TETHER_FOCUS = "focus"
	TETHER_REVIEW = "review"

	cursorShape = 0xc0

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

	def terminate(self):
		if self._messageCallLater:
			self._messageCallLater.Stop()
			self._messageCallLater = None
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		if self.display:
			self.display.terminate()
			self.display = None

	def _get_tether(self):
		return config.conf["braille"]["tetherTo"]

	def _set_tether(self, tether):
		if tether == config.conf["braille"]["tetherTo"]:
			return
		config.conf["braille"]["tetherTo"] = tether
		self.mainBuffer.clear()
		if tether == self.TETHER_REVIEW:
			self.handleReviewMove()
		else:
			self.handleGainFocus(api.getFocusObject())

	def setDisplayByName(self, name, isFallback=False):
		if not name:
			self.display = None
			self.displaySize = 0
			return
		# See if the user have defined a specific port to connect to
		if name not in config.conf["braille"]:
			# No port was set.
			config.conf["braille"][name] = {"port" : ""}
		port = config.conf["braille"][name].get("port")
		# Here we try to keep compatible with old drivers that don't support port setting
		# or situations where the user hasn't set any port.
		kwargs = {}
		if port:
			kwargs["port"] = port
		try:
			newDisplay = _getDisplayDriver(name)
			if newDisplay == self.display.__class__:
				# This is the same driver as was already set, so just re-initialise it.
				self.display.terminate()
				newDisplay = self.display
				newDisplay.__init__(**kwargs)
			else:
				newDisplay = newDisplay(**kwargs)
				if self.display:
					try:
						self.display.terminate()
					except:
						log.error("Error terminating previous display driver", exc_info=True)
				self.display = newDisplay
			self.displaySize = newDisplay.numCells
			self.enabled = bool(self.displaySize)
			if not isFallback:
				config.conf["braille"]["display"] = name
			log.info("Loaded braille display driver %s, current display has %d cells." %(name, self.displaySize))
			return True
		except:
			log.error("Error initializing display driver", exc_info=True)
			self.setDisplayByName("noBraille", isFallback=True)
			return False

	def _updateDisplay(self):
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		self._cursorBlinkUp = True
		self._displayWithCursor()
		blinkRate = config.conf["braille"]["cursorBlinkRate"]
		if blinkRate and self._cursorPos is not None:
			self._cursorBlinkTimer = wx.PyTimer(self._blink)
			self._cursorBlinkTimer.Start(blinkRate)

	def _displayWithCursor(self):
		if not self._cells:
			return
		cells = list(self._cells)
		if self._cursorPos is not None and self._cursorBlinkUp:
			cells[self._cursorPos] |= self.cursorShape
		self.display.display(cells)

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
		self._messageCallLater.Stop()
		self._messageCallLater = None
		self.update()

	def handleGainFocus(self, obj):
		if not self.enabled:
			return
		if self.tether != self.TETHER_FOCUS:
			return
		self._doNewObject(itertools.chain(getFocusContextRegions(obj, oldFocusRegions=self.mainBuffer.regions), getFocusRegions(obj)))

	def _doNewObject(self, regions):
		self.mainBuffer.clear()
		for region in regions:
			self.mainBuffer.regions.append(region)
		self.mainBuffer.update()
		# Last region should receive focus.
		self.mainBuffer.focus(region)
		if region.brailleCursorPos is not None:
			self.mainBuffer.scrollTo(region, region.brailleCursorPos)
		if self.buffer is self.mainBuffer:
			self.update()
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter>self._keyCountForLastMessage:
			self._dismissMessage()

	def handleCaretMove(self, obj):
		if not self.enabled:
			return
		if self.tether != self.TETHER_FOCUS:
			return
		if not self.mainBuffer.regions:
			return
		region = self.mainBuffer.regions[-1]
		if region.obj is not obj:
			return
		region.pendingCaretUpdate=True

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
		if region.brailleCursorPos is not None:
			self.mainBuffer.scrollTo(region, region.brailleCursorPos)
		if self.buffer is self.mainBuffer:
			self.update()
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter>self._keyCountForLastMessage:
			self._dismissMessage()

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
			return
		self.mainBuffer.saveWindow()
		region.update()
		self.mainBuffer.update()
		self.mainBuffer.restoreWindow()
		if self.buffer is self.mainBuffer:
			self.update()
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter>self._keyCountForLastMessage:
			self._dismissMessage()

	def handleReviewMove(self):
		if not self.enabled:
			return
		if self.tether != self.TETHER_REVIEW:
			return
		reviewPos = api.getReviewPosition()
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj == reviewPos.obj:
			self._doCursorMove(region)
		else:
			# We're reviewing a different object.
			self._doNewObject(getFocusRegions(reviewPos.obj, review=True))

	def handleConfigProfileSwitch(self):
		display = config.conf["braille"]["display"]
		if display != self.display.name:
			self.setDisplayByName(display)

def initialize():
	global handler
	config.addConfigDirsToPythonPackagePath(brailleDisplayDrivers)
	log.info("Using liblouis version %s" % louis.version())
	handler = BrailleHandler()
	handler.setDisplayByName(config.conf["braille"]["display"])

	# Update the display to the current focus/review position.
	if not handler.enabled or not api.getDesktopObject():
		# Braille is disabled or focus/review hasn't yet been initialised.
		return
	if handler.tether == handler.TETHER_FOCUS:
		handler.handleGainFocus(api.getFocusObject())
	else:
		handler.handleReviewMove()

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
	"""
	#: The name of the braille display; must be the original module file name.
	#: @type: str
	name = ""
	#: A description of the braille display.
	#: @type: str
	description = ""

	@classmethod
	def check(cls):
		"""Determine whether this braille display is available.
		The display will be excluded from the list of available displays if this method returns C{False}.
		For example, if this display is not present, C{False} should be returned.
		@return: C{True} if this display is available, C{False} if not.
		@rtype: bool
		"""
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
	#: @type: Tupple
	# Translators: String representing the automatic port selection for braille displays.
	AUTOMATIC_PORT = ("auto", _("Automatic"))

	@classmethod
	def getPossiblePorts(cls):
		""" Returns possible hardware ports for this driver.
		If the driver supports automatic port setting it should return as the first port L{brailleDisplayDriver.AUTOMATIC_PORT}

		@return: ordered dictionary of name : description for each port
		@rtype: OrderedDict
		"""
		raise NotImplementedError

	#: Global input gesture map for this display driver.
	#: @type: L{inputCore.GlobalGestureMap}
	gestureMap = None

class BrailleDisplayGesture(inputCore.InputGesture):
	"""A button, wheel or other control pressed on a braille display.
	Subclasses must provide L{source} and L{id}.
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

	def _get_id(self):
		"""The unique, display specific id for this gesture.
		@rtype: str
		"""
		raise NotImplementedError

	#: The index of the routing key or C{None} if this is not a routing key.
	#: @type: int
	routingIndex = None

	def _get_identifiers(self):
		ids = [u"br({source}):{id}".format(source=self.source, id=self.id).lower()]
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

	@classmethod
	def getDisplayTextForIdentifier(cls, identifier):
		return handler.display.description, identifier.split(":", 1)[1]

inputCore.registerGestureSource("br", BrailleDisplayGesture)
