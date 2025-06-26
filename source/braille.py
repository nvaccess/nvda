# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2025 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
# Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt

from enum import StrEnum
import itertools
import typing
from typing import (
	TYPE_CHECKING,
	Any,
	Callable,
	Dict,
	Generator,
	Iterable,
	List,
	NamedTuple,
	Optional,
	Set,
	Tuple,
	Union,
	Type,
)
from locale import strxfrm

from annotation import _AnnotationRolesT
import driverHandler
import pkgutil
import importlib
import contextlib
import ctypes.wintypes
import threading
import time
import wx
import louisHelper
import louis
import gui
from controlTypes.state import State
import winKernel
import keyboardHandler
import baseObject
import config
from config.configFlags import (
	ShowMessages,
	TetherTo,
	BrailleMode,
	ReportTableHeaders,
	OutputMode,
)
from config.featureFlagEnums import ReviewRoutingMovesSystemCaretFlag, FontFormattingBrailleModeFlag
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
import queueHandler
import brailleViewer
from autoSettingsUtils.driverSetting import BooleanDriverSetting, NumericDriverSetting
from utils.security import objectBelowLockScreenAndWindowsIsLocked, post_sessionLockStateChanged
from textUtils import isUnicodeNormalized, UnicodeNormalizationOffsetConverter
import hwIo
from editableText import EditableText

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject
	from speech.types import SpeechSequence

FALLBACK_TABLE = config.conf.getConfigValidation(("braille", "translationTable")).default
"""Table to use if the output table configuration is invalid."""

roleLabels: typing.Dict[controlTypes.Role, str] = {
	# Translators: Displayed in braille for an object which is a
	# window.
	controlTypes.Role.WINDOW: _("wnd"),
	# Translators: Displayed in braille for an object which is a
	# dialog.
	controlTypes.Role.DIALOG: _("dlg"),
	# Translators: Displayed in braille for an object which is a
	# check box.
	controlTypes.Role.CHECKBOX: _("chk"),
	# Translators: Displayed in braille for an object which is a
	# radio button.
	controlTypes.Role.RADIOBUTTON: _("rbtn"),
	# Translators: Displayed in braille for an object which is an
	# editable text field.
	controlTypes.Role.EDITABLETEXT: _("edt"),
	# Translators: Displayed in braille for an object which is a
	# button.
	controlTypes.Role.BUTTON: _("btn"),
	# Translators: Displayed in braille for an object which is a
	# menu bar.
	controlTypes.Role.MENUBAR: _("mnubar"),
	# Translators: Displayed in braille for an object which is a
	# menu item.
	controlTypes.Role.MENUITEM: _("mnuitem"),
	# Translators: Displayed in braille for an object which is a
	# menu.
	controlTypes.Role.POPUPMENU: _("mnu"),
	# Translators: Displayed in braille for an object which is a
	# combo box.
	controlTypes.Role.COMBOBOX: _("cbo"),
	# Translators: Displayed in braille for an object which is a
	# list.
	controlTypes.Role.LIST: _("lst"),
	# Translators: Displayed in braille for an object which is a
	# graphic.
	controlTypes.Role.GRAPHIC: _("gra"),
	# Translators: Displayed in braille for toast notifications and for an object which is a
	# help balloon.
	controlTypes.Role.HELPBALLOON: _("hlp"),
	# Translators: Displayed in braille for an object which is a
	# tool tip.
	controlTypes.Role.TOOLTIP: _("tltip"),
	# Translators: Displayed in braille for an object which is a
	# link.
	controlTypes.Role.LINK: _("lnk"),
	# Translators: Displayed in braille for an object which is a
	# tree view.
	controlTypes.Role.TREEVIEW: _("tv"),
	# Translators: Displayed in braille for an object which is a
	# tree view item.
	controlTypes.Role.TREEVIEWITEM: _("tvitem"),
	# Translators: Displayed in braille for an object which is a
	# tab control.
	controlTypes.Role.TABCONTROL: _("tabctl"),
	# Translators: Displayed in braille for an object which is a
	# progress bar.
	controlTypes.Role.PROGRESSBAR: _("prgbar"),
	# Translators: Displayed in braille for an object which is an
	# indeterminate progress bar, aka busy indicator.
	controlTypes.Role.BUSY_INDICATOR: _("bsyind"),
	# Translators: Displayed in braille for an object which is a
	# scroll bar.
	controlTypes.Role.SCROLLBAR: _("scrlbar"),
	# Translators: Displayed in braille for an object which is a
	# status bar.
	controlTypes.Role.STATUSBAR: _("stbar"),
	# Translators: Displayed in braille for an object which is a
	# table.
	controlTypes.Role.TABLE: _("tbl"),
	# Translators: Displayed in braille for an object which is a
	# tool bar.
	controlTypes.Role.TOOLBAR: _("tlbar"),
	# Translators: Displayed in braille for an object which is a
	# drop down button.
	controlTypes.Role.DROPDOWNBUTTON: _("drbtn"),
	# Displayed in braille for an object which is a
	# separator.
	controlTypes.Role.SEPARATOR: "⠤⠤⠤⠤⠤",
	# Translators: Displayed in braille for an object which is a
	# block quote.
	controlTypes.Role.BLOCKQUOTE: _("bqt"),
	# Translators: Displayed in braille for an object which is a
	# document.
	controlTypes.Role.DOCUMENT: _("doc"),
	# Translators: Displayed in braille for an object which is a
	# application.
	controlTypes.Role.APPLICATION: _("app"),
	# Translators: Displayed in braille for an object which is a
	# grouping.
	controlTypes.Role.GROUPING: _("grp"),
	# Translators: Displayed in braille for an object which is a
	# caption.
	controlTypes.Role.CAPTION: _("cap"),
	# Translators: Displayed in braille for an object which is a
	# embedded object.
	controlTypes.Role.EMBEDDEDOBJECT: _("embedded"),
	# Translators: Displayed in braille for an object which is a
	# end note.
	controlTypes.Role.ENDNOTE: _("enote"),
	# Translators: Displayed in braille for an object which is a
	# foot note.
	controlTypes.Role.FOOTNOTE: _("fnote"),
	# Translators: Displayed in braille for an object which is a
	# terminal.
	controlTypes.Role.TERMINAL: _("term"),
	# Translators: Displayed in braille for an object which is a
	# section.
	controlTypes.Role.SECTION: _("sect"),
	# Translators: Displayed in braille for an object which is a
	# toggle button.
	controlTypes.Role.TOGGLEBUTTON: _("tgbtn"),
	# Translators: Displayed in braille for an object which is a
	# split button.
	controlTypes.Role.SPLITBUTTON: _("splbtn"),
	# Translators: Displayed in braille for an object which is a
	# menu button.
	controlTypes.Role.MENUBUTTON: _("mnubtn"),
	# Translators: Displayed in braille for an object which is a
	# spin button.
	controlTypes.Role.SPINBUTTON: _("spnbtn"),
	# Translators: Displayed in braille for an object which is a
	# tree view button.
	controlTypes.Role.TREEVIEWBUTTON: _("tvbtn"),
	# Translators: Displayed in braille for an object which is a
	# menu.
	controlTypes.Role.MENU: _("mnu"),
	# Translators: Displayed in braille for an object which is a
	# panel.
	controlTypes.Role.PANEL: _("pnl"),
	# Translators: Displayed in braille for an object which is a
	# password edit.
	controlTypes.Role.PASSWORDEDIT: _("pwdedt"),
	# Translators: Displayed in braille for an object which is deleted.
	controlTypes.Role.DELETED_CONTENT: _("del"),
	# Translators: Displayed in braille for an object which is inserted.
	controlTypes.Role.INSERTED_CONTENT: _("ins"),
	# Translators: Displayed in braille for a landmark.
	controlTypes.Role.LANDMARK: _("lmk"),
	# Translators: Displayed in braille for an object which is an article.
	controlTypes.Role.ARTICLE: _("art"),
	# Translators: Displayed in braille for an object which is a region.
	controlTypes.Role.REGION: _("rgn"),
	# Translators: Displayed in braille for an object which is a figure.
	controlTypes.Role.FIGURE: _("fig"),
	# Translators: Displayed in braille for an object which represents marked (highlighted) content
	controlTypes.Role.MARKED_CONTENT: _("hlght"),
	# Translators: Displayed in braille when an object is a comment.
	controlTypes.Role.COMMENT: _("cmnt"),
	# Translators: Displayed in braille when an object is a suggestion.
	controlTypes.Role.SUGGESTION: _("sggstn"),
	# Translators: Displayed in braille when an object is a definition.
	controlTypes.Role.DEFINITION: _("definition"),
	# Translators: Displayed in braille when an object is a switch control
	controlTypes.Role.SWITCH: _("swtch"),
}

positiveStateLabels = {
	# Translators: Displayed in braille when an object is selected.
	controlTypes.State.SELECTED: _("sel"),
	# Displayed in braille when an object (e.g. a toggle button) is pressed.
	controlTypes.State.PRESSED: "⢎⣿⡱",
	# Displayed in braille when an object (e.g. a toggle button) is half pressed.
	controlTypes.State.HALF_PRESSED: "⢎⣸⡱",
	# Displayed in braille when an object (e.g. a check box) is checked.
	controlTypes.State.CHECKED: "⣏⣿⣹",
	# Displayed in braille when an object (e.g. a check box) is half checked.
	controlTypes.State.HALFCHECKED: "⣏⣸⣹",
	# Translators: Displayed in braille when an object (e.g. an editable text field) is read-only.
	controlTypes.State.READONLY: _("ro"),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is expanded.
	controlTypes.State.EXPANDED: _("-"),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is collapsed.
	controlTypes.State.COLLAPSED: _("+"),
	# Translators: Displayed in braille when an object has a popup (usually a sub-menu).
	controlTypes.State.HASPOPUP: _("submnu"),
	# Translators: Displayed in braille when a protected control or a document is encountered.
	controlTypes.State.PROTECTED: _("***"),
	# Translators: Displayed in braille when a required form field is encountered.
	controlTypes.State.REQUIRED: _("req"),
	# Translators: Displayed in braille when an invalid entry has been made.
	controlTypes.State.INVALID_ENTRY: _("invalid"),
	# Translators: Displayed in braille when an object supports autocompletion.
	controlTypes.State.AUTOCOMPLETE: _("..."),
	# Translators: Displayed in braille when an edit field allows typing multiple lines of text such as comment fields on websites.
	controlTypes.State.MULTILINE: _("mln"),
	# Translators: Displayed in braille when an object is clickable.
	controlTypes.State.CLICKABLE: _("clk"),
	# Translators: Displayed in braille when an object is sorted ascending.
	controlTypes.State.SORTED_ASCENDING: _("sorted asc"),
	# Translators: Displayed in braille when an object is sorted descending.
	controlTypes.State.SORTED_DESCENDING: _("sorted desc"),
	# Translators: Displayed in braille when an object (usually a graphic) has a long description.
	controlTypes.State.HASLONGDESC: _("ldesc"),
	# Translators: Displayed in braille when there is a formula on a spreadsheet cell.
	controlTypes.State.HASFORMULA: _("frml"),
	# Translators: Displayed in braille when there is a comment for a spreadsheet cell or piece of text in a document.
	controlTypes.State.HASCOMMENT: _("cmnt"),
	# Translators: Displayed in braille when a control is switched on
	controlTypes.State.ON: "⣏⣿⣹",
	# Translators: Displayed in braille when a link destination points to the same page
	controlTypes.State.INTERNAL_LINK: _("smp"),
}
negativeStateLabels = {
	# Translators: Displayed in braille when an object is not selected.
	controlTypes.State.SELECTED: _("nsel"),
	# Displayed in braille when an object (e.g. a toggle button) is not pressed.
	controlTypes.State.PRESSED: "⢎⣀⡱",
	# Displayed in braille when an object (e.g. a check box) is not checked.
	controlTypes.State.CHECKED: "⣏⣀⣹",
	# Displayed in braille when an object (e.g. a switch control) is switched off.
	controlTypes.State.ON: "⣏⣀⣹",
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
SELECTION_SHAPE = 0xC0  #: Dots 7 and 8

END_OF_BRAILLE_OUTPUT_SHAPE = 0xFF  # All dots
"""
The braille shape shown on a braille display when
the number of cells used by the braille handler is lower than the actual number of cells.
The 0 based position of the shape is equal to the number of cells used by the braille handler.
"""

#: Unicode braille indicator at the start of untranslated braille input.
INPUT_START_IND = "⣏"
#: Unicode braille indicator at the end of untranslated braille input.
INPUT_END_IND = " ⣹"


class FormatTagDelimiter(StrEnum):
	"""Delimiters for the start and end of format tags.

	As these are shapes, they should be provided in unicode braille.
	"""

	START = "⣋"
	END = "⣙"


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
focusContextPresentations = [
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
RegionWithPositions = collections.namedtuple("RegionWithPositions", ("region", "start", "end"))

#: Automatic constant to be used by braille displays that support the "automatic" port
#: and automatic braille display detection
#: @type: tuple
# Translators: String representing automatic port selection for braille displays.
AUTOMATIC_PORT = ("auto", _("Automatic"))
#: Used in place of a specific braille display driver name to indicate that
#: braille displays should be automatically detected and used.
#: @type: str
AUTO_DISPLAY_NAME = AUTOMATIC_PORT[0]

NO_BRAILLE_DISPLAY_NAME: str = "noBraille"
"""The name of the noBraille display driver."""

#: A port name which indicates that USB should be used.
#: @type: tuple
# Translators: String representing the USB port selection for braille displays.
USB_PORT = ("usb", _("USB"))
#: A port name which indicates that Bluetooth should be used.
#: @type: tuple
# Translators: String representing the Bluetooth port selection for braille displays.
BLUETOOTH_PORT = ("bluetooth", _("Bluetooth"))


class FormattingMarker(NamedTuple):
	"""A pair of braille symbols that indicate the start and end of a particular type of font formatting.

	As these are shapes, they should be provided in unicode braille.
	"""

	start: str
	end: str


fontAttributeFormattingMarkers: dict[str, FormattingMarker] = {
	"bold": FormattingMarker(
		# Translators: Brailled at the start of bold text.
		# This is the English letter "b" in braille.
		start=pgettext("braille formatting symbol", "⠃"),
		# Translators: Brailled at the end of bold text.
		# This is the English letter "b" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡃"),
	),
	"italic": FormattingMarker(
		# Translators: Brailled at the start of italic text.
		# This is the English letter "i" in braille.
		start=pgettext("braille formatting symbol", "⠊"),
		# Translators: Brailled at the end of italic text.
		# This is the English letter "i" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡊"),
	),
	"underline": FormattingMarker(
		# Translators: Brailled at the start of underlined text.
		# This is the English letter "u" in braille.
		start=pgettext("braille formatting symbol", "⠥"),
		# Translators: Brailled at the end of underlined text.
		# This is the English letter "u" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡥"),
	),
	"strikethrough": FormattingMarker(
		# Translators: Brailled at the start of strikethrough text.
		# This is the English letter "s" in braille.
		start=pgettext("braille formatting symbol", "⠎"),
		# Translators: Brailled at the end of strikethrough text.
		# This is the English letter "s" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡎"),
	),
}


def NVDAObjectHasUsefulText(obj: "NVDAObject") -> bool:
	"""Does obj contain useful text to display in braille

	:param obj: object to check
	:return: True if there is useful text, False if not
	"""
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return False
	import displayModel

	if issubclass(obj.TextInfo, displayModel.DisplayModelTextInfo):
		# #1711: Flat review (using displayModel) should always be presented on the braille display
		return True
	if obj._hasNavigableText or isinstance(obj, EditableText):
		return True
	return False


def _getDisplayDriver(moduleName: str, caseSensitive: bool = True) -> Type["BrailleDisplayDriver"]:
	try:
		return importlib.import_module(
			"brailleDisplayDrivers.%s" % moduleName,
			package="brailleDisplayDrivers",
		).BrailleDisplayDriver
	except ImportError as initialException:
		if caseSensitive:
			raise initialException
		for loader, name, isPkg in pkgutil.iter_modules(brailleDisplayDrivers.__path__):
			if name.startswith("_") or name.lower() != moduleName.lower():
				continue
			return importlib.import_module(
				"brailleDisplayDrivers.%s" % name,
				package="brailleDisplayDrivers",
			).BrailleDisplayDriver
		else:
			raise initialException


def getDisplayList(excludeNegativeChecks=True) -> List[Tuple[str, str]]:
	"""Gets a list of available display driver names with their descriptions.
	@param excludeNegativeChecks: excludes all drivers for which the check method returns C{False}.
	@type excludeNegativeChecks: bool
	@return: list of tuples with driver names and descriptions.
	"""
	displayList = []
	# The display that should be placed at the end of the list.
	lastDisplay = None
	for display in getDisplayDrivers():
		try:
			if not excludeNegativeChecks or display.check():
				if display.name == "noBraille":
					lastDisplay = (display.name, display.description)
				else:
					displayList.append((display.name, display.description))
			else:
				log.debugWarning(f"Braille display driver {display.name} reports as unavailable, excluding")
		except:  # noqa: E722
			log.error("", exc_info=True)
	displayList.sort(key=lambda d: strxfrm(d[1]))
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
		self.brailleCursorPos: Optional[int] = None
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

		converter: UnicodeNormalizationOffsetConverter | None = None
		textToTranslate = self.rawText
		textToTranslateTypeforms = self.rawTextTypeforms
		cursorPos = self.cursorPos
		if config.conf["braille"]["unicodeNormalization"] and not isUnicodeNormalized(textToTranslate):
			converter = UnicodeNormalizationOffsetConverter(textToTranslate)
			textToTranslate = converter.encoded
			if textToTranslateTypeforms is not None:
				# Typeforms must be adapted to represent normalized characters.
				textToTranslateTypeforms = [
					textToTranslateTypeforms[strOffset] for strOffset in converter.computedEncodedToStrOffsets
				]
			if cursorPos is not None:
				# Convert the cursor position to a normalized offset.
				cursorPos = converter.strToEncodedOffsets(cursorPos)
		self.brailleCells, brailleToRawPos, rawToBraillePos, self.brailleCursorPos = louisHelper.translate(
			[handler.table.fileName, "braille-patterns.cti"],
			textToTranslate,
			typeform=textToTranslateTypeforms,
			mode=mode,
			cursorPos=cursorPos,
		)

		if converter:
			# The received brailleToRawPos contains braille to normalized positions.
			# Process them to represent real raw positions by converting them from normalized ones.
			brailleToRawPos = [converter.encodedToStrOffsets(i) for i in brailleToRawPos]
			# The received rawToBraillePos contains normalized to braille positions.
			# Create a new list based on real raw positions.
			rawToBraillePos = [rawToBraillePos[i] for i in converter.computedStrToEncodedOffsets]
		self.brailleToRawPos = brailleToRawPos
		self.rawToBraillePos = rawToBraillePos

		if (
			self.selectionStart is not None
			and self.selectionEnd is not None
			and config.conf["braille"]["showSelection"]
		):
			try:
				# Mark the selection.
				self.brailleSelectionStart = self.rawToBraillePos[self.selectionStart]
				if self.selectionEnd >= len(self.rawText):
					self.brailleSelectionEnd = len(self.brailleCells)
				else:
					self.brailleSelectionEnd = self.rawToBraillePos[self.selectionEnd]
				for pos in range(self.brailleSelectionStart, self.brailleSelectionEnd):
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
		"""Move to the next line if possible."""

	def previousLine(self, start=False):
		"""Move to the previous line if possible.
		@param start: C{True} to move to the start of the line, C{False} to move to the end.
		@type start: bool
		"""

	def __repr__(self):
		return f"{self.__class__.__name__} ({self.rawText!r})"


class TextRegion(Region):
	"""A simple region containing a string of text."""

	def __init__(self, text):
		super(TextRegion, self).__init__()
		self.rawText = text


def _getAnnotationProperty(
	propertyValues: Dict[str, Any],
) -> str:
	# Translators: Braille when there are further details/annotations that can be fetched manually.
	genericDetailsRole = _("details")
	detailsRoles: _AnnotationRolesT = propertyValues.get("detailsRoles", tuple())
	if not detailsRoles:
		log.debugWarning(
			"There should always be detailsRoles (at least a single None value) when hasDetails is true.",
		)
		return genericDetailsRole
	else:
		# Translators: Braille when there are further details/annotations that can be fetched manually.
		# %s specifies the type of details (e.g. "has comment suggestion")
		hasDetailsRoleTemplate = _("has %s")
		rolesLabels = list(
			(
				hasDetailsRoleTemplate % roleLabels.get(role, role.displayString)
				for role in detailsRoles
				if role  # handle None case without the "has X" grammar.
			)
		)
		if None in detailsRoles:
			rolesLabels.insert(0, genericDetailsRole)
		return " ".join(rolesLabels)  # no comma to save cells on braille display


# C901 'getPropertiesBraille' is too complex
# Note: when working on getPropertiesBraille, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
	textList = []
	name = propertyValues.get("name")
	if name:
		textList.append(name)
	role: Optional[Union[controlTypes.Role, int]] = propertyValues.get("role")
	roleText = propertyValues.get("roleText")
	states = propertyValues.get("states")
	positionInfo = propertyValues.get("positionInfo")
	level = positionInfo.get("level") if positionInfo else None
	cellCoordsText = propertyValues.get("cellCoordsText")
	rowNumber = propertyValues.get("rowNumber")
	columnNumber = propertyValues.get("columnNumber")
	# When fetching row and column span
	# default the values to 1 to make further checks a lot simpler.
	# After all, a table cell that has no rowspan implemented is assumed to span one row.
	rowSpan = propertyValues.get("rowSpan") or 1
	columnSpan = propertyValues.get("columnSpan") or 1
	includeTableCellCoords = propertyValues.get("includeTableCellCoords", True)
	if role is not None and not roleText:
		role = controlTypes.Role(role)
		if role == controlTypes.Role.HEADING and level:
			# Translators: Displayed in braille for a heading with a level.
			# %s is replaced with the level.
			roleText = _("h%s") % level
			level = None
		elif role == controlTypes.Role.LINK and states and controlTypes.State.VISITED in states:
			states = states.copy()
			states.discard(controlTypes.State.VISITED)
			# Translators: Displayed in braille for a link which has been visited.
			roleText = _("vlnk")
		elif (
			name or cellCoordsText or rowNumber or columnNumber
		) and role in controlTypes.silentRolesOnFocus:
			roleText = None
		else:
			roleText = roleLabels.get(role, role.displayString)
	elif role is None:
		role = propertyValues.get("_role")
	value = propertyValues.get("value")
	if value and role not in controlTypes.silentValuesForRoles:
		textList.append(value)
	if states is not None:
		textList.extend(
			controlTypes.processAndLabelStates(
				role,
				states,
				controlTypes.OutputReason.FOCUS,
				states,
				None,
				positiveStateLabels,
				negativeStateLabels,
			),
		)
	if roleText:
		textList.append(roleText)

	errorMessage = propertyValues.get("errorMessage")
	if errorMessage:
		textList.append(errorMessage)

	description = propertyValues.get("description")
	if description:
		textList.append(description)
	hasDetails = propertyValues.get("hasDetails")
	if hasDetails:
		textList.append(_getAnnotationProperty(propertyValues))
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
			textList.append(_("lv %s") % positionInfo["level"])
	if rowNumber:
		if includeTableCellCoords and not cellCoordsText:
			if rowSpan > 1:
				# Translators: Displayed in braille for the table cell row numbers when a cell spans multiple rows.
				# Occurences of %s are replaced with the corresponding row numbers.
				rowStr = _("r{rowNumber}-{rowSpan}").format(
					rowNumber=rowNumber,
					rowSpan=rowNumber + rowSpan - 1,
				)
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
			if columnSpan > 1:
				# Translators: Displayed in braille for the table cell column numbers when a cell spans multiple columns.
				# Occurences of %s are replaced with the corresponding column numbers.
				columnStr = _("c{columnNumber}-{columnSpan}").format(
					columnNumber=columnNumber,
					columnSpan=columnNumber + columnSpan - 1,
				)
			else:
				# Translators: Displayed in braille for a table cell column number.
				# %s is replaced with the column number.
				columnStr = _("c{columnNumber}").format(columnNumber=columnNumber)
			textList.append(columnStr)
	isCurrent = propertyValues.get("current", controlTypes.IsCurrent.NO)
	if isCurrent != controlTypes.IsCurrent.NO:
		textList.append(isCurrent.displayString)
	placeholder = propertyValues.get("placeholder", None)
	if placeholder:
		textList.append(placeholder)
	if includeTableCellCoords and cellCoordsText:
		textList.append(cellCoordsText)
	return TEXT_SEPARATOR.join([x for x in textList if x])


class NVDAObjectRegion(Region):
	"""A region to provide a braille representation of an NVDAObject.
	This region will update based on the current state of the associated NVDAObject.
	A cursor routing request will activate the object's default action.
	"""

	def __init__(self, obj: "NVDAObject", appendText: str = ""):
		"""Constructor.
		@param obj: The associated NVDAObject.
		@param appendText: Text which should always be appended to the NVDAObject text, useful if this region will always precede other regions.
		"""
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			raise RuntimeError("NVDA object is secure and should not be initialized as a braille region")
		super().__init__()
		self.obj = obj
		self.appendText = appendText

	def update(self):
		obj = self.obj
		presConfig = config.conf["presentation"]
		role = obj.role
		name = obj.name
		placeholderValue = obj.placeholder
		if placeholderValue and not obj._isTextEmpty:
			placeholderValue = None
		errorMessage = obj.errorMessage
		if errorMessage and State.INVALID_ENTRY not in obj.states:
			errorMessage = None

		# determine if description should be read
		_shouldUseDescription = (
			obj.description  # is there a description
			and obj.description
			!= name  # the description must not be a duplicate of name, prevent double braille
			and (
				presConfig["reportObjectDescriptions"]  # report description always
				or (
					# aria description provides more relevant information than other sources of description such as
					# a 'title' attribute.
					# It should be used for extra details that would be obvious visually.
					config.conf["annotations"]["reportAriaDescription"]
					and obj.descriptionFrom == controlTypes.DescriptionFrom.ARIA_DESCRIPTION
				)
			)
		)
		description = obj.description if _shouldUseDescription else None
		detailsRoles = obj.annotations.roles if obj.annotations else None
		text = getPropertiesBraille(
			name=name,
			role=role,
			roleText=obj.roleTextBraille,
			current=obj.isCurrent,
			placeholder=placeholderValue,
			hasDetails=bool(obj.annotations),
			detailsRoles=detailsRoles,
			value=obj.value if not NVDAObjectHasUsefulText(obj) else None,
			states=obj.states,
			description=description,
			keyboardShortcut=obj.keyboardShortcut if presConfig["reportKeyboardShortcuts"] else None,
			positionInfo=obj.positionInfo if presConfig["reportObjectPositionInformation"] else None,
			cellCoordsText=obj.cellCoordsText
			if config.conf["documentFormatting"]["reportTableCellCoords"]
			else None,
			errorMessage=errorMessage,
		)
		if role == controlTypes.Role.MATH:
			import mathPres

			if mathPres.brailleProvider:
				try:
					text += TEXT_SEPARATOR + mathPres.brailleProvider.getBrailleForMathMl(
						obj.mathMl,
					)
				except (NotImplementedError, LookupError):
					pass
		self.rawText = text + self.appendText
		super(NVDAObjectRegion, self).update()

	def routeTo(self, braillePos):
		try:
			self.obj.doAction()
		except NotImplementedError:
			pass


class ReviewNVDAObjectRegion(NVDAObjectRegion):
	"""A region to provide a braille representation of an NVDAObject when braille is tethered to review.
	This region behaves very similar to its base class.
	However, when the move system caret when routing review cursor braille setting is active,
	pressing a routing key will first focus the object before executing the default action.
	"""

	def routeTo(self, braillePos: int):
		if _routingShouldMoveSystemCaret() and self.obj.isFocusable and not self.obj.hasFocus:
			self.obj.setFocus()
		super().routeTo(braillePos)


def getControlFieldBraille(
	info: textInfos.TextInfo,
	field: textInfos.Field,
	ancestors: typing.List[textInfos.Field],
	reportStart: bool,
	formatConfig: config.AggregatedSection,
) -> Optional[str]:
	presCat = field.getPresentationCategory(ancestors, formatConfig)
	# Cache this for later use.
	field._presCat = presCat
	role = field.get("role", controlTypes.Role.UNKNOWN)
	if reportStart:
		# If this is a container, only report it if this is the start of the node.
		if presCat == field.PRESCAT_CONTAINER and not field.get("_startOfNode"):
			return None
	else:
		# We only report ends for containers that are not landmarks/regions
		# and only if this is the end of the node.
		if (
			presCat != field.PRESCAT_CONTAINER
			or not field.get("_endOfNode")
			or role == controlTypes.Role.LANDMARK
		):
			return None

	description = None
	_descriptionFrom: controlTypes.DescriptionFrom = field.get("_description-from")
	_descriptionIsContent: bool = field.get("descriptionIsContent", False)
	if (
		not _descriptionIsContent
		# Note "reportObjectDescriptions" is not a reason to include description,
		# "Object" implies focus/object nav, getControlFieldBraille calculates text for Browse mode.
		# There is no way to identify getControlFieldBraille being called for reason focus, as is done in speech.
		and (
			config.conf["annotations"]["reportAriaDescription"]
			and _descriptionFrom == controlTypes.DescriptionFrom.ARIA_DESCRIPTION
		)
	):
		description = field.get("description", None)

	states = field.get("states", set())
	value = field.get("value", None)
	current = field.get("current", controlTypes.IsCurrent.NO)
	placeholder = field.get("placeholder", None)
	errorMessage = None
	if errorMessage and State.INVALID_ENTRY in states:
		errorMessage = field.get("errorMessage", None)

	hasDetails = field.get("hasDetails", False) and config.conf["annotations"]["reportDetails"]
	if config.conf["annotations"]["reportDetails"]:
		detailsRoles: Set[Union[None, controlTypes.Role]] = field.get("detailsRoles")
	else:
		detailsRoles = set()

	roleText = field.get("roleTextBraille", field.get("roleText"))
	landmark = field.get("landmark")
	if not roleText and role == controlTypes.Role.LANDMARK and landmark:
		roleText = f"{roleLabels[controlTypes.Role.LANDMARK]} {landmarkLabels[landmark]}"

	content = field.get("content")

	if presCat == field.PRESCAT_LAYOUT:
		return _getControlFieldForLayoutPresentation(
			description=description,
			current=current,
			hasDetails=hasDetails,
			detailsRoles=detailsRoles,
			role=role,
			content=content,
		)

	elif role in (
		controlTypes.Role.TABLECELL,
		controlTypes.Role.TABLECOLUMNHEADER,
		controlTypes.Role.TABLEROWHEADER,
	) and field.get("table-id"):
		return _getControlFieldForTableCell(
			description=description,
			current=current,
			hasDetails=hasDetails,
			detailsRoles=detailsRoles,
			field=field,
			formatConfig=formatConfig,
			states=states,
		)

	elif reportStart:
		return _getControlFieldForReportStart(
			description=description,
			current=current,
			hasDetails=hasDetails,
			detailsRoles=detailsRoles,
			field=field,
			role=role,
			states=states,
			content=content,
			info=info,
			value=value,
			roleText=roleText,
			placeholder=placeholder,
			errorMessage=errorMessage,
		)

	else:
		# Translators: Displayed in braille at the end of a control field such as a list or table.
		# %s is replaced with the control's role.
		return _("%s end") % getPropertiesBraille(
			role=role,
			roleText=roleText,
		)


def _getControlFieldForLayoutPresentation(
	description: Optional[str],
	current: controlTypes.IsCurrent,
	hasDetails: bool,
	detailsRoles: _AnnotationRolesT,
	role: controlTypes.Role,
	content: Optional[str],
) -> Optional[str]:
	text = []
	if description:
		text.append(getPropertiesBraille(description=description))
	if current:
		text.append(getPropertiesBraille(current=current))
	if hasDetails:
		text.append(getPropertiesBraille(hasDetails=hasDetails, detailsRoles=detailsRoles))
	if role == controlTypes.Role.GRAPHIC and content:
		text.append(content)

	if text:
		return TEXT_SEPARATOR.join(text)
	return None


def _getControlFieldForTableCell(
	description: Optional[str],
	current: controlTypes.IsCurrent,
	hasDetails: bool,
	detailsRoles: _AnnotationRolesT,
	field: textInfos.Field,
	formatConfig: config.AggregatedSection,
	states: Set[controlTypes.State],
) -> str:
	reportTableHeaders = formatConfig["reportTableHeaders"]
	reportTableCellCoords = formatConfig["reportTableCellCoords"]
	props = {
		"states": states,
		"rowNumber": (field.get("table-rownumber-presentational") or field.get("table-rownumber")),
		"columnNumber": (field.get("table-columnnumber-presentational") or field.get("table-columnnumber")),
		"rowSpan": field.get("table-rowsspanned"),
		"columnSpan": field.get("table-columnsspanned"),
		"includeTableCellCoords": reportTableCellCoords,
		"current": current,
		"description": description,
		"hasDetails": hasDetails,
		"detailsRoles": detailsRoles,
	}
	if reportTableHeaders in (ReportTableHeaders.ROWS_AND_COLUMNS, ReportTableHeaders.COLUMNS):
		props["columnHeaderText"] = field.get("table-columnheadertext")
	return getPropertiesBraille(**props)


def _getControlFieldForReportStart(
	description: Optional[str],
	current: controlTypes.IsCurrent,
	hasDetails: bool,
	detailsRoles: _AnnotationRolesT,
	field: textInfos.Field,
	role: controlTypes.Role,
	states: Set[controlTypes.State],
	content: Optional[str],
	info: textInfos.TextInfo,
	value: Optional[str],
	roleText: str,
	placeholder: Optional[str],
	errorMessage: str | None,
) -> str:
	props = {
		"states": states,
		"value": value,
		"current": current,
		"placeholder": placeholder,
		"roleText": roleText,
		"description": description,
		"hasDetails": hasDetails,
		"detailsRoles": detailsRoles,
		"errorMessage": errorMessage,
	}

	if role == controlTypes.Role.MATH:
		# Don't report the role for math here.
		# However, we still need to pass it (hence "_role").
		props["_role"] = role
	else:
		props["role"] = role

	if field.get("alwaysReportName", False):
		# Ensure that the name of the field gets presented even if normally it wouldn't.
		name = field.get("name")
		if name:
			props["name"] = name

	if config.conf["presentation"]["reportKeyboardShortcuts"]:
		kbShortcut = field.get("keyboardShortcut")
		if kbShortcut:
			props["keyboardShortcut"] = kbShortcut

	level = field.get("level")
	if level:
		props["positionInfo"] = {"level": level}

	text = getPropertiesBraille(**props)
	if content:
		if text:
			text += TEXT_SEPARATOR
		text += content
	elif role == controlTypes.Role.MATH:
		import mathPres

		if mathPres.brailleProvider:
			try:
				if text:
					text += TEXT_SEPARATOR
				text += mathPres.brailleProvider.getBrailleForMathMl(
					info.getMathMl(field),
				)
			except (NotImplementedError, LookupError):
				pass
	return text


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
		paragraphStartMarker = getParagraphStartMarker()
		if paragraphStartMarker:
			textList.append(paragraphStartMarker)
		if formatConfig["reportLineNumber"]:
			lineNumber = field.get("line-number")
			if lineNumber:
				textList.append("%s" % lineNumber)
		linePrefix = field.get("line-prefix")
		if linePrefix:
			textList.append(linePrefix)
		if formatConfig["reportHeadings"]:
			headingLevel = field.get("heading-level")
			if headingLevel:
				# Translators: Displayed in braille for a heading with a level.
				# %s is replaced with the level.
				textList.append(_("h%s") % headingLevel)
		collapsed = field.get("collapsed")
		if collapsed:
			textList.append(positiveStateLabels[controlTypes.State.COLLAPSED])
	if formatConfig["reportLinks"]:
		link = field.get("link")
		oldLink = fieldCache.get("link")
		if link and link != oldLink:
			textList.append(roleLabels[controlTypes.Role.LINK])
	if formatConfig["reportComments"]:
		comment = field.get("comment")
		oldComment = fieldCache.get("comment") if fieldCache is not None else None
		if (comment or oldComment is not None) and comment != oldComment:
			if comment:
				if comment is textInfos.CommentType.DRAFT:
					# Translators: Brailled when text contains a draft comment.
					text = _("drft cmnt")
				elif comment is textInfos.CommentType.RESOLVED:
					# Translators: Brailled when text contains a resolved comment.
					text = _("rslvd cmnt")
				else:  # generic
					# Translators: Brailled when text contains a generic comment.
					text = _("cmnt")
				textList.append(text)
	if formatConfig["reportBookmarks"]:
		bookmark = field.get("bookmark")
		oldBookmark = fieldCache.get("bookmark") if fieldCache is not None else None
		if (bookmark or oldBookmark is not None) and bookmark != oldBookmark:
			if bookmark:
				# Translators: brailled when text contains a bookmark
				text = _("bkmk")
				textList.append(text)

	if (
		config.conf["braille"]["fontFormattingDisplay"].calculated() == FontFormattingBrailleModeFlag.TAGS
		and (formattingTags := _getFormattingTags(field, fieldCache, formatConfig)) is not None
	):
		textList.append(formattingTags)

	fieldCache.clear()
	fieldCache.update(field)
	return TEXT_SEPARATOR.join([x for x in textList if x])


def getParagraphStartMarker() -> str | None:
	brailleConfig = config.conf["braille"]
	if brailleConfig["readByParagraph"]:
		paragraphStartMarker = brailleConfig["paragraphStartMarker"]
		if paragraphStartMarker == "¶":
			# Translators: This is a paragraph start marker used in braille.
			# The default symbol is the pilcrow,
			# a symbol also known as "paragraph symbol" or "paragraph marker".
			# This symbol should translate in braille via LibLouis automatically.
			# If there is a more appropriate character for your locale,
			# consider overwriting this (e.g. for Ge'ez ፨).
			# You can also use Unicode Braille such as ⠘⠏.
			# Ensure this is consistent with other strings with the context "paragraphMarker".
			paragraphStartMarker = pgettext("paragraphMarker", "¶")
	else:
		paragraphStartMarker = None
	return paragraphStartMarker


def _getFormattingTags(
	field: dict[str, str],
	fieldCache: dict[str, str],
	formatConfig: dict[str, bool],
) -> str | None:
	"""Get the formatting tags for the given field and cache.

	Formatting tags are calculated according to the preferences passed in formatConfig.

	:param field: The format current field.
	:param fieldCache: The previous format field.
	:param formatConfig: The user's formatting preferences.
	:return: The braille formatting tag as a string, or None if no pertinant formatting is applied.
	"""
	textList: list[str] = []
	if formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE:
		# Only calculate font attribute tags if the user has enabled font attribute reporting in braille.
		for fontAttribute, formattingMarker in fontAttributeFormattingMarkers.items():
			_appendFormattingMarker(fontAttribute, formattingMarker, textList, field, fieldCache)
	if len(textList) > 0:
		return f"{FormatTagDelimiter.START}{''.join(textList)}{FormatTagDelimiter.END}"


def _appendFormattingMarker(
	attribute: str,
	marker: FormattingMarker,
	textList: list[str],
	field: dict[str, str],
	fieldCache: dict[str, str],
) -> None:
	"""Append a formatting marker to the text list if the attribute has changed.

	:param attribute: The attribute to check.
	:param marker: The formatting marker to use.
	:param textList: The list of marker strings to append to.
	:param field: The current format field.
	:param fieldCache: The previous format field.
	"""
	newVal = field.get(attribute, False)
	oldVal = fieldCache.get(attribute, False) if fieldCache is not None else False
	if newVal and not oldVal:
		textList.append(marker.start)
	elif oldVal and not newVal:
		textList.append(marker.end)


class TextInfoRegion(Region):
	pendingCaretUpdate = False  #: True if the cursor should be updated for this region on the display
	allowPageTurns = True  #: True if a page turn should be tried when a TextInfo cannot move anymore and the object supports page turns.

	def __init__(self, obj: "NVDAObject"):
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			raise RuntimeError("NVDA object is secure and should not be initialized as a braille region")
		super().__init__()
		self.obj = obj

	def _isMultiline(self):
		# A region's object can either be an NVDAObject or a tree interceptor.
		# Tree interceptors should always be multiline.
		from treeInterceptorHandler import TreeInterceptor

		if isinstance(self.obj, TreeInterceptor):
			return True
		# Terminals and documents are inherently multiline, so they don't have the multiline state.
		return (
			self.obj.role in (controlTypes.Role.TERMINAL, controlTypes.Role.DOCUMENT)
			or controlTypes.State.MULTILINE in self.obj.states
		)

	def _getSelection(self):
		"""Retrieve the selection.
		If there is no selection, retrieve the collapsed cursor.
		@return: The selection.
		@rtype: L{textInfos.TextInfo}
		"""
		try:
			return self.obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except:  # noqa: E722
			return self.obj.makeTextInfo(textInfos.POSITION_FIRST)

	def _setCursor(self, info: textInfos.TextInfo):
		"""Set the cursor.
		@param info: The range to which the cursor should be moved.
		"""
		try:
			info.updateCaret()
		except NotImplementedError:
			log.debugWarning("", exc_info=True)

	def _getTypeformFromFormatField(self, field, formatConfig):
		typeform = louis.plain_text
		if not (
			(formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE)
			and (
				config.conf["braille"]["fontFormattingDisplay"].calculated()
				== FontFormattingBrailleModeFlag.LIBLOUIS
			)
		):
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
		# When true, we are inside a clickable field, and should therefore not report any more new clickable fields
		inClickable = False
		# Collapsed ranges should never produce text and fields,
		# But later on we may still need to draw the cursor at this position.
		if not info.isCollapsed:
			commands = info.getTextWithFields(formatConfig=formatConfig)
		else:
			commands = []
		for command in commands:
			if isinstance(command, str):
				# Text should break a run of clickables
				inClickable = False
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
				self._rawToContentPos.extend(range(self._currentContentPos, endPos))
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
					text = getFormatFieldBraille(
						field,
						formatFieldAttributesCache,
						self._isFormatFieldAtStart,
						formatConfig,
					)
					if not text:
						continue
					# Map this field text to the start of the field's content.
					self._addFieldText(text, self._currentContentPos)
				elif cmd == "controlStart":
					if self._skipFieldsNotAtStartOfNode and not field.get("_startOfNode"):
						text = None
					else:
						textList = []
						if not inClickable and formatConfig["reportClickable"]:
							states = field.get("states")
							if states and controlTypes.State.CLICKABLE in states:
								# We have entered an outer most clickable or entered a new clickable after exiting a previous one
								# Report it if there is nothing else interesting about the field
								field._presCat = presCat = field.getPresentationCategory(
									ctrlFields,
									formatConfig,
								)
								if not presCat or presCat is field.PRESCAT_LAYOUT:
									textList.append(positiveStateLabels[controlTypes.State.CLICKABLE])
								inClickable = True
						text = info.getControlFieldBraille(field, ctrlFields, True, formatConfig)
						if text:
							textList.append(text)
						text = " ".join(textList)
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
					# Exiting a controlField should break a run of clickables
					inClickable = False
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
			# del self._rawToContentPos[rawTextLen:]
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
		self.hidePreviousRegions = start.compareEndPoints(readingInfo, "startToStart") < 0
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

	def getTextInfoForBraillePos(self, braillePos: int) -> textInfos.TextInfo:
		"""Fetches a collapsed TextInfo at the specified braille position in the region.
		:param braillePos: The braille position.
			If no textInfo could be found at braillePos,
			try to find one at braillePos - 1 until a position has been found.
		"""
		pos = self._rawToContentPos[self.brailleToRawPos[braillePos]]
		# pos is relative to the start of the reading unit.
		maxIterations = 10
		startTime = time.time()
		for i, curPos in enumerate(range(pos, max(-1, pos - maxIterations), -1)):
			if curPos == 0:
				# Not necessary to find offset.
				break
			# Move curPos code points from the start.
			# Note that, as liblouis uses 32 bit encoding internally,
			# it is really safe to assume that one code point offset is equal to one character within liblouis.
			# If an attempt fails, we try to move to the previous character
			try:
				return self._readingInfo.moveToCodepointOffset(curPos)
			except RuntimeError:
				msg = f"Error in moveToCodepointOffset in iteration {i + 1} (position {curPos}"
				if i + 1 >= maxIterations or (exceeded := time.time() - startTime > 0.5):
					logFunc = log.exception
					curPos = pos
					if exceeded:
						msg += ", exceeded time limit of 0.5 seconds"
				else:
					logFunc = log.debug
				logFunc(msg)
		dest = self._readingInfo.copy()
		dest.collapse()
		if curPos > 0:
			dest.move(textInfos.UNIT_CHARACTER, curPos)
		return dest

	def routeTo(self, braillePos: int):
		if (
			self._brailleInputIndStart is not None
			and self._brailleInputIndStart <= braillePos < self._brailleInputIndEnd
		):
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

		dest = self.getTextInfoForBraillePos(braillePos)
		self._routeToTextInfo(dest)

	def _routeToTextInfo(self, info: textInfos.TextInfo):
		# When there is a selection, brailleCursorPos will be None
		# Don't activate, but move the cursor to the new cell (dropping the
		# selection). An alternative behavior may be to activate on the selection.
		# Moving the cursor was considered more intuitive.
		if self.brailleCursorPos is not None:
			cursor = self.getTextInfoForBraillePos(self.brailleCursorPos)
			if info.compareEndPoints(cursor, "startToStart") == 0:
				# The cursor is already at this position,
				# so activate the position.
				try:
					self._getSelection().activate()
				except NotImplementedError:
					pass
				return
		self._setCursor(info)
		_speakOnRouting(info.copy())

	def nextLine(self):
		dest = self._readingInfo.copy()
		shouldCollapseToEnd = False
		moved = dest.move(self._getReadingUnit(), 1)
		if not moved:
			if self.allowPageTurns and isinstance(dest.obj, textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage()
				except RuntimeError:
					pass
				else:
					dest = dest.obj.makeTextInfo(textInfos.POSITION_FIRST)
			else:  # no page turn support
				shouldCollapseToEnd = True
		dest.collapse(shouldCollapseToEnd)
		self._setCursor(dest)
		_speakOnNavigatingByUnit(dest, self._getReadingUnit())

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
			if self.allowPageTurns and isinstance(dest.obj, textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage(previous=True)
				except RuntimeError:
					pass
				else:
					dest = dest.obj.makeTextInfo(textInfos.POSITION_LAST)
					dest.expand(unit)
			else:
				# no page turn support
				return
		dest.collapse()
		self._setCursor(dest)
		_speakOnNavigatingByUnit(dest, self._getReadingUnit())


class CursorManagerRegion(TextInfoRegion):
	def _isMultiline(self):
		return True

	def _getSelection(self):
		return self.obj.selection

	def _setCursor(self, info: textInfos.TextInfo):
		self.obj.selection = info


class ReviewTextInfoRegion(TextInfoRegion):
	allowPageTurns = False

	def _getSelection(self):
		return api.getReviewPosition().copy()

	def _routeToTextInfo(self, info: textInfos.TextInfo):
		super()._routeToTextInfo(info)
		if not _routingShouldMoveSystemCaret():
			return
		from displayModel import DisplayModelTextInfo, EditableTextDisplayModelTextInfo

		if isinstance(info, DisplayModelTextInfo) and not isinstance(info, EditableTextDisplayModelTextInfo):
			# This region either reviews the screen or an object that has
			# DisplayModelTextInfo without a caret, e.g. IAccessible.ContentGenericClient.
			# In this case, we can at least emulate a kind of caret
			# by trying to focus the object at start of the range.
			obj = info.NVDAObjectAtStart
			if not objectBelowLockScreenAndWindowsIsLocked(obj) and obj.isFocusable and not obj.hasFocus:
				obj.setFocus()
		else:
			# Update the physical caret using the super class.
			super()._setCursor(info)

	def _setCursor(self, info: textInfos.TextInfo):
		api.setReviewPosition(info)


class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion): ...


def _routingShouldMoveSystemCaret() -> bool:
	"""Returns whether pressing a braille routing key should move the system caret."""
	reviewRoutingMovesSystemCaret = config.conf["braille"]["reviewRoutingMovesSystemCaret"].calculated()
	configuredTether = config.conf["braille"]["tetherTo"]
	shouldMoveCaretTetheredReview = (
		configuredTether == TetherTo.REVIEW.value
		and reviewRoutingMovesSystemCaret == ReviewRoutingMovesSystemCaretFlag.ALWAYS
	)
	shouldMoveCaretTetheredAuto = (
		configuredTether == TetherTo.AUTO.value
		and reviewRoutingMovesSystemCaret != ReviewRoutingMovesSystemCaretFlag.NEVER
	)
	return shouldMoveCaretTetheredAuto or shouldMoveCaretTetheredReview


def rindex(seq, item, start, end):
	for index in range(end - 1, start - 1, -1):
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
		self._windowRowBufferOffsets: list[tuple[int, int]] = [(0, 0)]
		"""
		A list representing the rows in the braille window,
		each item being a tuple of start and end braille buffer offsets.
		Splitting the window into independent rows allows for optional avoidance of splitting words across rows.
		"""

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

	def _get_rawToBraillePos(self):
		"""@return: a list mapping positions in L{rawText} to positions in L{brailleCells} for the entire buffer.
		@rtype: [int, ...]
		"""
		rawToBraillePos = []
		for region, regionStart, regionEnd in self.regionsWithPositions:
			rawToBraillePos.extend(p + regionStart for p in region.rawToBraillePos)
		return rawToBraillePos

	brailleToRawPos: List[int]

	def _get_brailleToRawPos(self):
		"""@return: a list mapping positions in L{brailleCells} to positions in L{rawText} for the entire buffer.
		@rtype: [int, ...]
		"""
		brailleToRawPos = []
		start = 0
		for region in self.visibleRegions:
			brailleToRawPos.extend(p + start for p in region.brailleToRawPos)
			start += len(region.rawText)
		return brailleToRawPos

	def bufferPosToRegionPos(self, bufferPos):
		for region, start, end in self.regionsWithPositions:
			if end > bufferPos:
				return region, bufferPos - start
		raise LookupError("No such position")

	def regionPosToBufferPos(self, region, pos, allowNearest=False):
		start: int = 0
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
		brailleToRawPos = self.brailleToRawPos
		if not brailleToRawPos or not self.rawText:
			# if either are empty, just return an empty string.
			return ""
		try:
			lastIndex = len(brailleToRawPos) - 1
			rawTextStart = brailleToRawPos[min(lastIndex, startPos)]
			rawTextEnd = brailleToRawPos[min(lastIndex, endPos)] + 1
			lastIndex = len(self.rawText)
			return self.rawText[rawTextStart : min(lastIndex, rawTextEnd)]
		except IndexError:
			log.debugWarning(
				f"Unable to get raw text for buffer positions"
				f"(startPos-endPos): {startPos}-{endPos}, "
				f"for rawText: {self.rawText}, "
				f"with brailleToRawPos: {brailleToRawPos}",
				exc_info=True,
			)
			return ""

	def bufferPosToWindowPos(self, bufferPos: int) -> int:
		for row, (start, end) in enumerate(self._windowRowBufferOffsets):
			if start <= bufferPos < end:
				return row * self.handler.displayDimensions.numCols + (bufferPos - start)
		raise LookupError("buffer pos not in window")

	def windowPosToBufferPos(self, windowPos: int) -> int:
		"""
		Converts a position relative to the braille window to a position relative to the braille buffer.
		"""
		if self.handler.displaySize == 0:
			return 0
		windowPos = max(min(windowPos, self.handler.displaySize), 0)
		row, col = divmod(windowPos, self.handler.displayDimensions.numCols)
		if row < len(self._windowRowBufferOffsets):
			start, end = self._windowRowBufferOffsets[row]
			return max(min(start + col, end - 1), 0)
		raise ValueError("Position outside window")

	windowStartPos: int
	"""The start position of the braille window in the braille buffer."""

	def _get_windowStartPos(self) -> int:
		return self.windowPosToBufferPos(0)

	def _set_windowStartPos(self, pos: int) -> None:
		self._calculateWindowRowBufferOffsets(pos)

	def _calculateWindowRowBufferOffsets(self, pos: int) -> None:
		"""
		Calculates the start and end positions of each row in the braille window.
		Ensures that words are not split across rows when word wrap is enabled.
		Ensures that the window does not extend past the end of the braille buffer.
		:param pos: The start position of the braille window.
		"""
		self._windowRowBufferOffsets.clear()
		if len(self.brailleCells) == 0:
			# Initialising with no actual braille content.
			self._windowRowBufferOffsets = [(0, 0)]
			return
		doWordWrap = config.conf["braille"]["wordWrap"]
		bufferEnd = len(self.brailleCells)
		start = pos
		clippedEnd = False
		for row in range(self.handler.displayDimensions.numRows):
			end = start + self.handler.displayDimensions.numCols
			if end > bufferEnd:
				end = bufferEnd
				clippedEnd = True
			elif doWordWrap:
				try:
					end = rindex(self.brailleCells, 0, start, end) + 1
				except (ValueError, IndexError):
					pass  # No space on line
			self._windowRowBufferOffsets.append((start, end))
			if clippedEnd:
				break
			start = end

	windowEndPos: int
	"""The end position of the braille window in the braille buffer."""

	def _get_windowEndPos(self) -> int:
		start, end = self._windowRowBufferOffsets[-1]
		return end

	def _set_windowEndPos(self, endPos: int) -> None:
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
			if regionStart < endPos:
				if region.focusToHardLeft:
					# Only scroll to the start of this region.
					restrictPos = regionStart
					break
				elif config.conf["braille"]["focusContextPresentation"] != CONTEXTPRES_CHANGEDCONTEXT:
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
			for startPos in range(startPos, endPos):
				if self.brailleCells[startPos] != 0:
					break
		except ValueError:
			pass
		# When word wrap is enabled, the first block of spaces may be removed from the current window.
		# This may prevent displaying the start of paragraphs.
		paragraphStartMarker = getParagraphStartMarker()
		if paragraphStartMarker and self.regions[-1].rawText.startswith(
			paragraphStartMarker + TEXT_SEPARATOR,
		):
			region, regionStart, regionEnd = list(self.regionsWithPositions)[-1]
			# Show paragraph start indicator if it is now at the left of the current braille window
			if startPos <= len(paragraphStartMarker) + 1:
				startPos = self.regionPosToBufferPos(region, regionStart)
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

	def focus(self, region):
		"""Bring the specified region into focus.
		The region is placed at the start of the display.
		However, if the region has not set L{Region.focusToHardLeft} and there is extra space at the end of the display, the display is scrolled left so that as much as possible is displayed.
		@param region: The region to focus.
		@type region: L{Region}
		"""
		pos = self.regionPosToBufferPos(region, 0)
		self.windowStartPos = pos
		if region.focusToHardLeft or config.conf["braille"]["focusContextPresentation"] == CONTEXTPRES_SCROLL:
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
			self.rawText += rawText
			self.brailleCells.extend(cells)
			if region.brailleCursorPos is not None:
				self.cursorPos = start + region.brailleCursorPos
			start += len(cells)
		if log.isEnabledFor(log.IO):
			log.io("Braille regions text: %r" % logRegions)
		self._calculateWindowRowBufferOffsets(self.windowStartPos)

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
		return self.bufferPositionsToRawText(self.windowStartPos, self.windowEndPos)

	def _get_windowBrailleCells(self) -> list[int]:
		windowCells = []
		for start, end in self._windowRowBufferOffsets:
			rowCells = self.brailleCells[start:end]
			remaining = self.handler.displayDimensions.numCols - len(rowCells)
			if remaining > 0:
				rowCells.extend([0] * remaining)
			windowCells.extend(rowCells)
		return windowCells

	def routeTo(self, windowPos):
		pos = self.windowPosToBufferPos(windowPos)
		if pos >= self.windowEndPos:
			return
		region, pos = self.bufferPosToRegionPos(pos)
		region.routeTo(pos)

	def getTextInfoForWindowPos(self, windowPos):
		pos = self.windowPosToBufferPos(windowPos)
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


def getFocusContextRegions(
	obj: "NVDAObject",
	oldFocusRegions: Optional[List[Region]] = None,
) -> Generator[Region, None, None]:
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return
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
			for index, ancestor in zip(range(len(ancestors) - 1, 0, -1), reversed(ancestors)):
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
		for index, region in zip(range(len(oldFocusRegions) - 1, -1, -1), reversed(oldFocusRegions)):
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
		if (
			config.conf["braille"]["focusContextPresentation"] == CONTEXTPRES_CHANGEDCONTEXT
			and not focusToHardLeftSet
		):
			# We are presenting context changes to the user
			# Thus, only scroll back as far as the start of the first new focus ancestor
			# focusToHardLeftSet is used since the first new ancestor isn't always represented by a region
			region.focusToHardLeft = True
			focusToHardLeftSet = True
		region.update()
		yield region

	_cachedFocusAncestorsEnd = ancestorsEnd


def getFocusRegions(
	obj: "NVDAObject",
	review: bool = False,
) -> Generator[Region, None, None]:
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return
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
		region2 = (ReviewCursorManagerRegion if review else CursorManagerRegion)(obj)
	elif isinstance(obj, DocumentTreeInterceptor) or (
		isinstance(obj, NVDAObject) and NVDAObjectHasUsefulText(obj)
	):
		region2 = (ReviewTextInfoRegion if review else TextInfoRegion)(obj)
	else:
		region2 = None
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
	region = (ReviewNVDAObjectRegion if review else NVDAObjectRegion)(
		obj,
		appendText=TEXT_SEPARATOR if region2 else "",
	)
	region.update()
	yield region
	if region2:
		region2.update()
		yield region2


def formatCellsForLog(cells: List[int]) -> str:
	"""Formats a sequence of braille cells so that it is suitable for logging.
	The output contains the dot numbers for each cell, with each cell separated by a space.
	A C{-} indicates an empty cell.
	@param cells: The cells to format.
	@return: The formatted cells.
	"""
	# optimisation: This gets called a lot, so needs to be as efficient as possible.
	# List comprehensions without function calls are faster than loops.
	# For str.join, list comprehensions are faster than generator comprehensions.
	return TEXT_SEPARATOR.join(
		["".join([str(dot + 1) for dot in range(8) if cell & (1 << dot)]) if cell else "-" for cell in cells],
	)


pre_writeCells = extensionPoints.Action()
"""
Notifies when cells are about to be written to a braille display.
This allows components and add-ons to perform an action.
For example, when a system is controlled by a braille enabled remote system,
the remote system should know what cells to show on its display.
@param cells: The list of braille cells.
@type cells: List[int]
@param rawText: The raw text that corresponds with the cells.
@type rawText: str
@param currentCellCount: The current number of cells
@type currentCellCount: bool
"""

filter_displaySize = extensionPoints.Filter[int](
	_deprecationMessage="braille.filter_displaySize is deprecated. Use braille.filter_displayDimensions instead.",
)
"""
Note: filter_displayDimensions should now be used in place of this filter.
If this filter is used, NVDA will assume that the display has 1 row of `displaySize` cells.

Filter that allows components or add-ons to change the display size used for braille output.
For example, when a system has an 80 cell display, but is being controlled by a remote system with a 40 cell
display, the display size should be lowered to 40 .
:param value: the number of cells of the current display.
"""


class DisplayDimensions(NamedTuple):
	numRows: int
	numCols: int

	@property
	def displaySize(self) -> int:
		return self.numCols * self.numRows


filter_displayDimensions = extensionPoints.Filter[DisplayDimensions]()
"""
Filter that allows components or add-ons to change the number of rows and columns used for braille output.
For example, when a system has a display with 10 rows and 20 columns, but is being controlled by a remote system with a display of 5 rows and 40 coluns, the display number of rows should be lowered to 5.
:param value: a DisplayDimensions namedtuple with the number of rows and columns of the current display.
Note: this should be used in place of filter_displaySize.
"""

displaySizeChanged = extensionPoints.Action()
"""
Action that allows components or add-ons to be notified of display size changes.
For example, when a system is controlled by a remote system and the remote system swaps displays,
The local system should be notified about display size changes at the remote system.
:param displaySize: The current display size used by the braille handler.
:type displaySize: int
:param displayDimensions.numRows: The current number of rows used by the braille handler.
:type displayDimensions.numRows: int
:param displayDimensions.numCols: The current number of columns used by the braille handler.
:type displayDimensions.numCols: int
"""

displayChanged = extensionPoints.Action()
"""
Action that allows components or add-ons to be notified of braille display changes.
For example, when a system is controlled by a remote system and the remote system swaps displays,
The local system should be notified about display parameters at the remote system,
e.g. name and cellcount.
@param display: The new braille display driver
@type display: L{BrailleDisplayDriver}
@param isFallback: Whether the display is set as fallback display due to another display's failure
@type isFallback: bool
@param detected: If the display was set by auto detection, the device match that matched the driver
@type detected: bdDetect.DeviceMatch or C{None}
"""

decide_enabled = extensionPoints.Decider()
"""
Allows components or add-ons to decide whether the braille handler should be forcefully disabled.
For example, when a system is controlling a remote system with braille,
the local braille handler should be disabled as long as the system is in control of the remote system.
Handlers are called without arguments.
"""


class BrailleHandler(baseObject.AutoPropertyObject):
	# TETHER_AUTO, TETHER_FOCUS, TETHER_REVIEW and tetherValues
	# are deprecated, but remain to retain API backwards compatibility
	TETHER_AUTO = TetherTo.AUTO.value
	TETHER_FOCUS = TetherTo.FOCUS.value
	TETHER_REVIEW = TetherTo.REVIEW.value
	tetherValues = [(v.value, v.displayString) for v in TetherTo]

	queuedWrite: Optional[List[int]] = None
	queuedWriteLock: threading.Lock
	ackTimerHandle: int
	_regionsPendingUpdate: Set[Union[NVDAObjectRegion, TextInfoRegion]]
	"""
	Regions pending an update.
	Regions are added by L{handleUpdate} and L{handleCaretMove} and cleared in L{_handlePendingUpdate}.
	"""

	def __init__(self):
		louisHelper.initialize()
		self._table: brailleTables.BrailleTable = brailleTables.getTable(FALLBACK_TABLE)
		self.display: Optional[BrailleDisplayDriver] = None
		self._displayDimensions: DisplayDimensions = DisplayDimensions(1, 0)
		"""
		Internal cache for the displayDimensions property.
		This attribute is used to compare the displaySize output by l{filter_displayDimensions} or l{filter_displaySize}
		with its previous output.
		If the value differs, L{displaySizeChanged} is notified.
		"""
		self._enabled: bool = False
		"""
		Internal cache for the enabled property.
		This attribute is used to compare the enabled output by l{decide_enabled}
		with its previous output.
		If L{decide_enabled} decides to disable the handler, pending output should be cleared.
		"""
		self._regionsPendingUpdate = set()

		self.mainBuffer = BrailleBuffer(self)
		self.messageBuffer = BrailleBuffer(self)
		self._messageCallLater = None
		self.buffer = self.mainBuffer
		self._keyCountForLastMessage = 0
		self._cursorPos = None
		self._cursorBlinkUp = True
		self._cells = []
		self._cursorBlinkTimer = None
		config.post_configProfileSwitch.register(self.handlePostConfigProfileSwitch)
		if config.conf["braille"]["tetherTo"] == TetherTo.AUTO.value:
			self._tether = TetherTo.FOCUS.value
		else:
			self._tether = config.conf["braille"]["tetherTo"]
		self._detector = None
		self._rawText = ""

		self.queuedWriteLock = threading.Lock()
		self.ackTimerHandle = winKernel.createWaitableTimer()

		post_sessionLockStateChanged.register(self._onSessionLockStateChanged)
		brailleViewer.postBrailleViewerToolToggledAction.register(self._onBrailleViewerChangedState)
		# noqa: F401 avoid module level import to prevent cyclical dependency
		# between speech and braille
		from speech.extensions import pre_speech, pre_speechCanceled

		pre_speech.register(self._showSpeechInBraille)
		pre_speechCanceled.register(self.clearBrailleRegions)

	def terminate(self):
		# noqa: F401 avoid module level import to prevent cyclical dependency
		# between speech and braille
		from speech.extensions import pre_speech, pre_speechCanceled

		pre_speechCanceled.unregister(self.clearBrailleRegions)
		pre_speech.unregister(self._showSpeechInBraille)
		self._disableDetection()
		if self._messageCallLater:
			self._messageCallLater.Stop()
			self._messageCallLater = None
		if self._cursorBlinkTimer:
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		config.post_configProfileSwitch.unregister(self.handlePostConfigProfileSwitch)
		post_sessionLockStateChanged.unregister(self._onSessionLockStateChanged)
		if self.display:
			self.display.terminate()
			self.display = None
		if self.ackTimerHandle:
			if not ctypes.windll.kernel32.CancelWaitableTimer(self.ackTimerHandle):
				raise ctypes.WinError()
			winKernel.closeHandle(self.ackTimerHandle)
			self.ackTimerHandle = None
		louisHelper.terminate()

	def _clearAll(self) -> None:
		"""Clear the braille buffers and update the braille display."""
		self.mainBuffer.clear()
		if self.buffer is self.messageBuffer:
			self._dismissMessage(False)
		self.update()

	def _onSessionLockStateChanged(self, isNowLocked: bool):
		"""Clear the braille buffers and update the braille display to prevent leaking potentially sensitive information from a locked session.

		:param isNowLocked: True if the session is now locked; false if it is now unlocked.
		"""
		if isNowLocked:
			self._clearAll()

	table: brailleTables.BrailleTable
	"""Type definition for auto prop '_get_table/_set_table'"""

	def _get_table(self) -> brailleTables.BrailleTable:
		"""The translation table to use for braille output."""
		return self._table

	def _set_table(self, table: brailleTables.BrailleTable):
		self._table = table
		config.conf["braille"]["translationTable"] = table.fileName

	# The list containing the regions that will be shown in braille when the speak function is called
	# and the braille mode is set to speech output
	_showSpeechInBrailleRegions: list[TextRegion] = []

	def _showSpeechInBraille(self, speechSequence: "SpeechSequence"):
		if config.conf["braille"]["mode"] == BrailleMode.FOLLOW_CURSORS.value or not self.enabled:
			return
		_showSpeechInBrailleRegions = self._showSpeechInBrailleRegions
		regionsText = "".join([i.rawText for i in _showSpeechInBrailleRegions])
		if len(regionsText) > 100000:
			return
		text = " ".join([x for x in speechSequence if isinstance(x, str)])
		currentRegions = False
		if _showSpeechInBrailleRegions:
			text = f" {text}"
			currentRegions = True

		region = TextRegion(text)
		region.update()
		_showSpeechInBrailleRegions.append(region)
		self.mainBuffer.regions = _showSpeechInBrailleRegions.copy()
		if not currentRegions:
			handler.mainBuffer.focus(_showSpeechInBrailleRegions[0])
		handler.mainBuffer.update()
		handler.update()

	_suppressClearBrailleRegions: bool = False

	@contextlib.contextmanager
	def suppressClearBrailleRegions(self, script: inputCore.ScriptT):
		from globalCommands import commands

		suppress = script in [commands.script_braille_scrollBack, commands.script_braille_scrollForward]
		self._suppressClearBrailleRegions = suppress
		yield

	def clearBrailleRegions(self):
		if not self._suppressClearBrailleRegions:
			self._showSpeechInBrailleRegions.clear()
		self._suppressClearBrailleRegions = False

	def getTether(self):
		return self._tether

	def setTether(self, tether, auto=False):
		if auto and not self.shouldAutoTether:
			return
		if not auto:
			config.conf["braille"]["tetherTo"] = tether
		if tether == self._tether:
			return
		self._tether = tether
		self.mainBuffer.clear()

	def _get_shouldAutoTether(self) -> bool:
		return self.enabled and config.conf["braille"]["tetherTo"] == TetherTo.AUTO.value

	displaySize: int
	_cache_displaySize = True

	def _get_displaySize(self) -> int:
		"""Returns the display size to use for braille output.
		This is calculated from l{displayDimensions}.
		Handlers can register themselves to L{filter_displayDimensions} to change this value on the fly.
		Therefore, this is a read only property and can't be set.
		"""
		displaySize = self.displayDimensions.displaySize
		# For backwards compatibility, we still set the internal cache.
		self._displaySize = displaySize
		return displaySize

	def _set_displaySize(self, value):
		"""While the display size can be changed while a display is connected
		(for instance see L{brailleDisplayDrivers.alva.BrailleDisplayDriver} split point feature),
		it is not possible to override the display size using this property.
		Consider registering a handler to L{filter_displayDimensions} instead.
		"""
		raise AttributeError(
			f"Can't set displaySize to {value}, consider registering a handler to filter_displayDimensions",
		)

	displayDimensions: DisplayDimensions
	_cache_displayDimensions = True

	def _get_displayDimensions(self) -> DisplayDimensions:
		if not self.display:
			numRows = numCols = 0
		else:
			numRows = self.display.numRows
			numCols = self.display.numCols if numRows > 1 else self.display.numCells
		rawDisplayDimensions = DisplayDimensions(
			numRows=numRows,
			numCols=numCols,
		)
		filteredDisplayDimensions = filter_displayDimensions.apply(rawDisplayDimensions)
		# Would be nice if there were a more official way to find out if the displaySize filter is currently registered by at least 1 handler.
		calculatedDisplaySize = filteredDisplayDimensions.displaySize
		if next(filter_displaySize.handlers, None):
			# There is technically a race condition here if a handler is unregistered before the apply call.
			# But worse case is that a multiline display will be singleline for a short time.
			filteredDisplaySize = filter_displaySize.apply(calculatedDisplaySize)
			if filteredDisplaySize != calculatedDisplaySize:
				calculatedDisplaySize = filteredDisplaySize
				filteredDisplayDimensions = DisplayDimensions(
					numRows=1,
					numCols=filteredDisplaySize,
				)
		if self._displayDimensions != filteredDisplayDimensions:
			displaySizeChanged.notify(
				displaySize=calculatedDisplaySize,
				numRows=filteredDisplayDimensions.numRows,
				numCols=filteredDisplayDimensions.numCols,
			)
		self._displayDimensions = filteredDisplayDimensions
		return filteredDisplayDimensions

	def _set_displayDimensions(self, value: DisplayDimensions):
		"""
		It is not possible to override the display dimensions using this property.
		Consider registering a handler to L{filter_displayDimensions} instead.
		"""
		raise AttributeError(
			f"Can't set displayDimensions to {value}, consider registering a handler to filter_displayDimensions",
		)

	enabled: bool
	_cache_enabled = True

	def _get_enabled(self):
		"""Returns whether braille is enabled.
		Handlers can register themselves to L{decide_enabled} and return C{False}
		to forcefully disable the braille handler.
		If components need to change the state from disabled to enabled instead,
		they should register to L{filter_displaySize}.
		By default, the enabled/disabled state is based on the boolean value of L{displaySize},
		and thus is C{True} when the display size is greater than 0.
		This is a read only property and can't be set.
		"""
		currentEnabled = bool(self.displaySize) and decide_enabled.decide()
		if self._enabled != currentEnabled:
			self._enabled = currentEnabled
			if currentEnabled is False:
				wx.CallAfter(self._handleEnabledDecisionFalse)
		return currentEnabled

	def _set_enabled(self, value):
		raise AttributeError(
			f"Can't set enabled to {value}, consider registering a handler to decide_enabled or filter_displaySize",
		)

	def _handleEnabledDecisionFalse(self):
		"""When a decider handler decides to disable the braille handler, ensure braille doesn't continue.
		This should be called from the main thread to avoid wx assertions.
		"""
		if self._cursorBlinkTimer:
			# A blinking cursor should be stopped
			self._cursorBlinkTimer.Stop()
			self._cursorBlinkTimer = None
		if self.buffer is self.messageBuffer:
			self._dismissMessage(shouldUpdate=False)

	_lastRequestedDisplayName = None
	"""The name of the last requested braille display driver with setDisplayByName,
	even if it failed and has fallen back to no braille.
	"""

	def setDisplayByName(
		self,
		name: str,
		isFallback: bool = False,
		detected: typing.Optional[bdDetect.DeviceMatch] = None,
	) -> bool:
		if name == AUTO_DISPLAY_NAME:
			# Calling _enableDetection will set the display to noBraille until a display is detected.
			# Note that L{isFallback} is ignored in these cases.
			self._enableDetection()
			return True
		elif not isFallback:
			# #8032: Take note of the display requested, even if it is going to fail.
			self._lastRequestedDisplayName = name
			if not detected:
				self._disableDetection()

		try:
			newDisplayClass = _getDisplayDriver(name)
			self._setDisplay(newDisplayClass, isFallback=isFallback, detected=detected)
			if not isFallback:
				if not detected:
					config.conf["braille"]["display"] = newDisplayClass.name
				elif (
					"bluetoothName" in detected.deviceInfo
					or detected.deviceInfo.get("provider") == "bluetooth"
				):
					# As USB devices have priority over Bluetooth, keep a detector running to switch to USB when connected.
					# Note that the detector should always be running in this situation, so we can trigger a rescan.
					self._detector.rescan(bluetooth=False, limitToDevices=[newDisplayClass.name])
				else:
					self._disableDetection()
			return True
		except Exception:
			# For auto display detection, logging an error for every failure is too obnoxious.
			if not detected:
				log.error(f"Error initializing display driver {name!r}", exc_info=True)
			elif bdDetect._isDebug():
				log.debugWarning(f"Couldn't initialize display driver {name!r}", exc_info=True)
			fallbackDisplayClass = _getDisplayDriver(NO_BRAILLE_DISPLAY_NAME)
			# Only initialize the fallback if it is not already set
			if self.display.__class__ != fallbackDisplayClass:
				self._setDisplay(fallbackDisplayClass, isFallback=False)
			return False

	def _switchDisplay(
		self,
		oldDisplay: Optional["BrailleDisplayDriver"],
		newDisplayClass: Type["BrailleDisplayDriver"],
		**kwargs,
	) -> "BrailleDisplayDriver":
		sameDisplayReInit = newDisplayClass == oldDisplay.__class__
		if sameDisplayReInit:
			# This is the same driver as was already set, so just re-initialize it.
			log.debug(f"Reinitializing {newDisplayClass.name!r} braille display")
			oldDisplay.terminate()
			newDisplay = oldDisplay
		else:
			newDisplay = newDisplayClass.__new__(newDisplayClass)
		extensionPoints.callWithSupportedKwargs(newDisplay.__init__, **kwargs)
		if not sameDisplayReInit:
			if oldDisplay:
				log.debug(f"Switching braille display from {oldDisplay.name!r} to {newDisplay.name!r}")
				try:
					oldDisplay.terminate()
				except Exception:
					log.error("Error terminating previous display driver", exc_info=True)
		newDisplay.initSettings()
		return newDisplay

	def _setDisplay(
		self,
		newDisplayClass: Type["BrailleDisplayDriver"],
		isFallback: bool = False,
		detected: typing.Optional[bdDetect.DeviceMatch] = None,
	):
		kwargs = {}
		if detected:
			kwargs["port"] = detected
		else:
			# See if the user has defined a specific port to connect to
			try:
				kwargs["port"] = config.conf["braille"][newDisplayClass.name]["port"]
			except KeyError:
				pass

		if bdDetect._isDebug() and detected:
			log.debug(f"Possibly detected display {newDisplayClass.description!r}")
		oldDisplay = self.display
		newDisplay = self._switchDisplay(oldDisplay, newDisplayClass, **kwargs)
		self.display = newDisplay
		log.info(
			f"Loaded braille display driver {newDisplay.name!r}, current display has {newDisplay.numCells} cells.",
		)
		displayChanged.notify(display=newDisplay, isFallback=isFallback, detected=detected)
		queueHandler.queueFunction(queueHandler.eventQueue, self.initialDisplay)

	def _onBrailleViewerChangedState(self, created):
		if created:
			self._updateDisplay()
		log.debug("Braille Viewer enabled: {}".format(self.enabled))

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
			# This is called from another thread when a display is auto detected.
			# Make sure we start the blink timer from the main thread to avoid wx assertions
			wx.CallAfter(self._cursorBlinkTimer.Start, blinkRate)

	def _normalizeCellArraySize(
		self,
		oldCells: list[int],
		oldCellCount: int,
		oldNumRows: int,
		newCellCount: int,
		newNumRows: int,
	) -> list[int]:
		"""
		Given a list of braille cells of length oldCell Count layed out in sequencial rows of oldNumRows,
		return a list of braille cells of length newCellCount layed out in sequencial rows of newNumRows,
		padding or truncating the rows and columns as necessary.
		"""
		oldNumCols = oldCellCount // oldNumRows
		newNumCols = newCellCount // newNumRows
		if len(oldCells) < oldCellCount:
			log.warning("Braille cells are shorter than the display size. Padding with blank cells.")
			oldCells.extend([0] * (oldCellCount - len(oldCells)))
		newCells = []
		if newCellCount != oldCellCount or newNumRows != oldNumRows:
			for rowIndex in range(newNumRows):
				if rowIndex < oldNumRows:
					start = rowIndex * oldNumCols
					rowLen = min(oldNumCols, newNumCols)
					end = start + rowLen
					row = oldCells[start:end]
					if rowLen < newNumCols:
						row.extend([0] * (newNumCols - rowLen))
				else:
					row = [0] * newNumCols
				newCells.extend(row)
		else:
			newCells = oldCells
		return newCells

	def _writeCells(self, cells: List[int]):
		handlerCellCount = self.displaySize
		pre_writeCells.notify(cells=cells, rawText=self._rawText, currentCellCount=handlerCellCount)
		displayCellCount = self.display.numCells
		if not displayCellCount:
			# No physical display to write to
			return
		# Braille displays expect cells to be padded up to displayCellCount.
		# However, the braille handler uses handlerCellCount to calculate the number of cells.
		# number of rows / columns may also differ.
		cells = self._normalizeCellArraySize(
			cells,
			handlerCellCount,
			self.displayDimensions.numRows,
			displayCellCount,
			self.display.numRows,
		)
		if not self.display.isThreadSafe:
			try:
				self.display.display(cells)
			except:  # noqa: E722
				log.error("Error displaying cells. Disabling display", exc_info=True)
				self.handleDisplayUnavailable()
			return
		with self.queuedWriteLock:
			alreadyQueued: Optional[List[int]] = self.queuedWrite
			self.queuedWrite = cells
		# If a write was already queued, we don't need to queue another;
		# we just replace the data.
		# This means that if multiple writes occur while an earlier write is still in progress,
		# we skip all but the last.
		if not alreadyQueued and not self.display._awaitingAck:
			# Queue a call to the background thread.
			self._writeCellsInBackground()

	def _writeCellsInBackground(self):
		"""Writes cells to a braille display in the background by queuing a function to the i/o thread."""
		hwIo.bgThread.queueAsApc(self._bgThreadExecutor)

	def _displayWithCursor(self):
		if not self._cells:
			return
		cells = list(self._cells)
		if self._cursorPos is not None and self._cursorBlinkUp:
			if self.getTether() == TetherTo.FOCUS.value:
				cells[self._cursorPos] |= config.conf["braille"]["cursorShapeFocus"]
			else:
				cells[self._cursorPos] |= config.conf["braille"]["cursorShapeReview"]
		self._writeCells(cells)

	def _blink(self):
		self._cursorBlinkUp = not self._cursorBlinkUp
		self._displayWithCursor()

	def update(self):
		cells = self.buffer.windowBrailleCells
		self._rawText = self.buffer.windowRawText
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
		If a key is pressed the message will be dismissed by the next text being written to the display.
		@postcondition: The message is displayed.
		"""
		if (
			not self.enabled
			or config.conf["braille"]["showMessages"] == ShowMessages.DISABLED
			or text is None
			or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value
		):
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
		self._keyCountForLastMessage = keyboardHandler.keyCounter

	def _resetMessageTimer(self):
		"""Reset the message timeout.
		@precondition: A message is currently being displayed.
		"""
		if config.conf["braille"]["showMessages"] == ShowMessages.SHOW_INDEFINITELY:
			return
		# Configured timeout is in seconds.
		timeout = config.conf["braille"]["messageTimeout"] * 1000
		if self._messageCallLater:
			self._messageCallLater.Restart(timeout)
		else:
			self._messageCallLater = wx.CallLater(timeout, self._dismissMessage)

	def _dismissMessage(self, shouldUpdate: bool = True):
		"""Dismiss the current message.
		@param shouldUpdate: Whether to call update after dismissing.
		@precondition: A message is currently being displayed.
		@postcondition: The display returns to the main buffer.
		"""
		self.buffer.clear()
		self.buffer = self.mainBuffer
		if self._messageCallLater:
			self._messageCallLater.Stop()
			self._messageCallLater = None
		if shouldUpdate:
			self.update()

	def handleGainFocus(self, obj: "NVDAObject", shouldAutoTether: bool = True) -> None:
		if not self.enabled or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value:
			return
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			return
		if shouldAutoTether:
			self.setTether(TetherTo.FOCUS.value, auto=True)
		if self._tether != TetherTo.FOCUS.value:
			return
		if (
			getattr(obj, "treeInterceptor", None)
			and not obj.treeInterceptor.passThrough
			and obj.treeInterceptor.isReady
		):
			obj = obj.treeInterceptor
		self._doNewObject(
			itertools.chain(
				getFocusContextRegions(obj, oldFocusRegions=self.mainBuffer.regions),
				getFocusRegions(obj),
			),
		)

	def _doNewObject(self, regions):
		self.mainBuffer.clear()
		focusToHardLeftSet = False
		for region in regions:
			if (
				self.getTether() == TetherTo.FOCUS.value
				and config.conf["braille"]["focusContextPresentation"] == CONTEXTPRES_CHANGEDCONTEXT
			):
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
		elif self.buffer is self.messageBuffer and keyboardHandler.keyCounter > self._keyCountForLastMessage:
			self._dismissMessage()

	def handleCaretMove(
		self,
		obj: "NVDAObject",
		shouldAutoTether: bool = True,
	) -> None:
		if not self.enabled or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value:
			return
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			return
		prevTether = self._tether
		if shouldAutoTether:
			self.setTether(TetherTo.FOCUS.value, auto=True)
		if self._tether != TetherTo.FOCUS.value:
			return
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj == obj:
			region.pendingCaretUpdate = True
			self._regionsPendingUpdate.add(region)
		elif prevTether == TetherTo.REVIEW.value:
			# The caret moved in a different object than the review position.
			self._doNewObject(getFocusRegions(obj, review=False))

	def _handlePendingUpdate(self):
		"""When any region is pending an update, updates the region and the braille display."""
		if not self._regionsPendingUpdate:
			return
		try:
			scrollTo: Optional[TextInfoRegion] = None
			self.mainBuffer.saveWindow()
			for region in self._regionsPendingUpdate:
				from treeInterceptorHandler import TreeInterceptor

				if isinstance(region.obj, TreeInterceptor) and not region.obj.isAlive:
					log.debug("Skipping region update for died tree interceptor")
					continue
				try:
					region.update()
				except Exception:
					log.debugWarning(
						f"Region update failed for {region}, object probably died",
						exc_info=True,
					)
					continue
				if isinstance(region, TextInfoRegion) and region.pendingCaretUpdate:
					scrollTo = region
					region.pendingCaretUpdate = False
			self.mainBuffer.update()
			self.mainBuffer.restoreWindow()
			if scrollTo is not None:
				self.scrollToCursorOrSelection(scrollTo)
			if self.buffer is self.mainBuffer:
				self.update()
			elif (
				self.buffer is self.messageBuffer
				and keyboardHandler.keyCounter > self._keyCountForLastMessage
			):
				self._dismissMessage()
		finally:
			self._regionsPendingUpdate.clear()

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
	def _handleProgressBarUpdate(
		self,
		obj: "NVDAObject",
	) -> None:
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			return
		oldTime = getattr(self, "_lastProgressBarUpdateTime", None)
		newTime = time.time()
		if oldTime and newTime - oldTime < 1:
			# Fetching dialog text is expensive, so update at most once a second.
			return
		self._lastProgressBarUpdateTime = newTime
		for obj in reversed(api.getFocusAncestors()[:-1]):
			if obj.role == controlTypes.Role.DIALOG:
				self.handleUpdate(obj)
				return

	def handleUpdate(self, obj: "NVDAObject") -> None:
		if not self.enabled:
			return
		if objectBelowLockScreenAndWindowsIsLocked(obj):
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
			if self._tether != TetherTo.FOCUS.value:
				return
			# Late import to avoid circular import.
			from NVDAObjects import NVDAObject

			if (
				isinstance(obj, NVDAObject)
				and obj.role == controlTypes.Role.PROGRESSBAR
				and obj.isInForeground
			):
				self._handleProgressBarUpdate(obj)
			return
		self._regionsPendingUpdate.add(region)

	def handleReviewMove(self, shouldAutoTether=True):
		if not self.enabled or config.conf["braille"]["mode"] == BrailleMode.SPEECH_OUTPUT.value:
			return
		reviewPos = api.getReviewPosition()
		if shouldAutoTether:
			self.setTether(TetherTo.REVIEW.value, auto=True)
		if self._tether != TetherTo.REVIEW.value:
			return
		region = self.mainBuffer.regions[-1] if self.mainBuffer.regions else None
		if region and region.obj == reviewPos.obj:
			region.pendingCaretUpdate = True
			self._regionsPendingUpdate.add(region)
		else:
			# We're reviewing a different object.
			self._doNewObject(getFocusRegions(reviewPos.obj, review=True))

	def initialDisplay(self):
		if not self.enabled or not api.getDesktopObject():
			# Braille is disabled or focus/review hasn't yet been initialised.
			return
		try:
			if self.getTether() == TetherTo.FOCUS.value:
				self.handleGainFocus(api.getFocusObject(), shouldAutoTether=False)
			else:
				self.handleReviewMove(shouldAutoTether=False)
		except Exception:
			# #8877: initialDisplay might fail because NVDA tries to focus
			# an object for which property fetching raises an exception.
			log.debugWarning("Error in initial display", exc_info=True)

	def handlePostConfigProfileSwitch(self):
		display = config.conf["braille"]["display"]
		# #7459: the syncBraille has been dropped in favor of the native hims driver.
		# Migrate to renamed drivers as smoothly as possible.
		newDriverName = RENAMED_DRIVERS.get(display)
		if newDriverName:
			display = config.conf["braille"]["display"] = newDriverName
		if (
			self.display is None
			# Do not choose a new display if:
			or not (
				# The display in the new profile is equal to the last requested display name
				display == self._lastRequestedDisplayName
				# or the new profile uses auto detection, which supports detection of the currently active display.
				or (
					display == AUTO_DISPLAY_NAME
					and bdDetect.driverIsEnabledForAutoDetection(self.display.name)
				)
			)
		):
			self.setDisplayByName(display)
		elif (
			# Auto detection should be active
			display == AUTO_DISPLAY_NAME
			and self._detector is not None
			# And the current display should be no braille.
			# If not, there is an active detector for the current driver
			# to switch from bluetooth to USB.
			and self.display.name == NO_BRAILLE_DISPLAY_NAME
		):
			self._detector._limitToDevices = bdDetect.getBrailleDisplayDriversEnabledForDetection()

		if (configuredTether := config.conf["braille"]["tetherTo"]) != TetherTo.AUTO.value:
			self._tether = configuredTether

		tableName = config.conf["braille"]["translationTable"]
		# #6140: Migrate to new table names as smoothly as possible.
		newTableName = brailleTables.RENAMED_TABLES.get(tableName)
		if newTableName:
			tableName = config.conf["braille"]["translationTable"] = newTableName
		if config.conf["braille"]["translationTable"] == "auto":
			table = brailleTables.getDefaultTableForCurLang(brailleTables.TableType.OUTPUT)
		else:
			table = tableName
		if tableName != self._table.fileName:
			try:
				self._table = brailleTables.getTable(table)
			except LookupError:
				log.error(
					f"Invalid translation table ({tableName}), falling back to default ({FALLBACK_TABLE}).",
				)
				self._table = brailleTables.getTable(FALLBACK_TABLE)

	def handleDisplayUnavailable(self):
		"""Called when the braille display becomes unavailable.
		This logs an error and disables the display.
		This is called when displaying cells raises an exception,
		but drivers can also call it themselves if appropriate.
		"""
		log.error("Braille display unavailable. Disabling", exc_info=True)
		newDisplay = (
			AUTO_DISPLAY_NAME
			if config.conf["braille"]["display"] == AUTO_DISPLAY_NAME
			else NO_BRAILLE_DISPLAY_NAME
		)
		self.setDisplayByName(newDisplay, isFallback=True)

	def _enableDetection(
		self,
		usb: bool = True,
		bluetooth: bool = True,
		limitToDevices: Optional[List[str]] = None,
	):
		"""Enables automatic detection of braille displays.
		When auto detection is already active, this will force a rescan for devices.
		This should also be executed when auto detection should be resumed due to loss of display connectivity.
		In that case, it is triggered by L{setDisplayByname}.
		@param usb: Whether to scan for USB devices
		@param bluetooth: Whether to scan for Bluetooth devices.
		@param limitToDevices: An optional list of driver names a scan should be limited to.
			This is used when a Bluetooth device is detected, in order to switch to USB
			when an USB device for the same driver is found.
			C{None} if no driver filtering should occur.
		"""
		self.setDisplayByName(NO_BRAILLE_DISPLAY_NAME, isFallback=True)
		if self._detector:
			self._detector.rescan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)
			return
		config.conf["braille"]["display"] = AUTO_DISPLAY_NAME
		self._detector = bdDetect._Detector()
		self._detector._queueBgScan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)

	def _disableDetection(self):
		"""Disables automatic detection of braille displays."""
		if self._detector:
			self._detector.terminate()
			self._detector = None

	def _bgThreadExecutor(self, param: int):
		"""Executed as APC when cells have to be written to a display asynchronously."""
		if not self.display:
			# Sometimes, the bg thread executor is triggered when a display is not fully initialized.
			# For example, this happens when handling an ACK during initialisation.
			# We can safely ignore this.
			return
		if self.display._awaitingAck:
			# Do not write cells when we are awaiting an ACK
			return
		with self.queuedWriteLock:
			data: Optional[List[int]] = self.queuedWrite
			self.queuedWrite = None
		if not data:
			return
		try:
			self.display.display(data)
		except:  # noqa: E722
			log.error("Error displaying cells. Disabling display", exc_info=True)
			self.handleDisplayUnavailable()
		else:
			if self.display.receivesAckPackets:
				self.display._awaitingAck = True
				SECOND_TO_MS = 1000
				hwIo.bgThread.setWaitableTimer(
					self.ackTimerHandle,
					# Wait twice the display driver timeout for acknowledgement packets
					# Note: timeout is in seconds whereas setWaitableTimer expects milliseconds
					int(self.display.timeout * 2 * SECOND_TO_MS),
					self._ackTimeoutResetter,
				)

	def _ackTimeoutResetter(self, param: int):
		if self.display and self.display.receivesAckPackets and self.display._awaitingAck:
			log.debugWarning(f"Waiting for {self.display.name} ACK packet timed out")
			self.display._awaitingAck = False
			self._writeCellsInBackground()


# Maps old braille display driver names to new drivers that supersede old drivers.
# Ensure that if a user has set a preferred driver which has changed name, the new
# user preference is retained.
RENAMED_DRIVERS = {
	# "oldDriverName": "newDriverName"
	"syncBraille": "hims",
	"alvaBC6": "alva",
	"hid": "hidBrailleStandard",
}

handler: Optional[BrailleHandler] = None


def initialize():
	global handler
	log.info("Using liblouis version %s" % louis.version())
	import serial

	log.info("Using pySerial version %s" % serial.VERSION)
	handler = BrailleHandler()
	handler.handlePostConfigProfileSwitch()
	config.post_configProfileSwitch.register(handler.handlePostConfigProfileSwitch)


def pumpAll():
	"""Runs tasks at the end of each core cycle. For now just region updates, e.g. for caret movement."""
	handler._handlePendingUpdate()


def terminate():
	global handler
	handler.terminate()
	handler = None


class BrailleDisplayDriver(driverHandler.Driver):
	"""
	Abstract base braille display driver.

	Each braille display driver should be a separate Python module in the root ``brailleDisplayDrivers`` directory,
	containing a ``BrailleDisplayDriver`` class that inherits from this base class.

	At a minimum, drivers must:
		- Set :attr:`name` and :attr:`description`.
		- Override :meth:`check`.

	To display braille:
		- :meth:`display` must be implemented.
		- For a single-line display, :attr:`numCells` must be implemented.
		- For a multi-line display, :attr:`numRows` and :attr:`numCols` must be implemented.

	To support automatic detection of braille displays belonging to this driver:
		* The driver must be thread-safe, and :attr:`isThreadSafe` should be set to ``True``.
		* :attr:`supportsAutomaticDetection` must be set to ``True``.
		* :meth:`registerAutomaticDetection` must be implemented.

	Drivers should dispatch input (e.g., button presses or controls) using the :mod:`inputCore` framework.
	They should subclass :class:`BrailleDisplayGesture` and execute instances of those gestures
	using :meth:`inputCore.manager.executeGesture`. These gestures can be mapped in :attr:`gestureMap`.
	A driver can also inherit from :class:`baseObject.ScriptableObject` to provide display-specific scripts.

	.. seealso::
		:mod:`hwIo` for raw serial and HID I/O.

	There are factory functions to create :class:`autoSettingsUtils.driverSetting.DriverSetting` instances
	for common display-specific settings, such as :meth:`DotFirmnessSetting`.
	"""

	_configSection = "braille"
	# Most braille display drivers don't have settings yet.
	# Make sure supportedSettings is not abstract for these.
	supportedSettings = ()
	#: Whether this driver is thread-safe.
	#: If it is, NVDA may initialize, terminate or call this driver  on any thread.
	#: This allows NVDA to read from and write to the display in the background,
	#: which means the rest of NVDA is not blocked while this occurs,
	#: thus resulting in better performance.
	#: This is also required to use the L{hwIo} module.
	isThreadSafe: bool = False
	#: Whether this driver is supported for automatic detection of braille displays.
	supportsAutomaticDetection: bool = False
	#: Whether displays for this driver return acknowledgements for sent packets.
	#: L{_handleAck} should be called when an ACK is received.
	#: Note that thread safety is required for the generic implementation to function properly.
	#: If a display is not thread safe, a driver should manually implement ACK processing.
	receivesAckPackets: bool = False
	#: Whether this driver is awaiting an Ack for a connected display.
	#: This is set to C{True} after displaying cells when L{receivesAckPackets} is True,
	#: and set to C{False} by L{_handleAck} or when C{timeout} has elapsed.
	#: This is for internal use by NVDA core code only and shouldn't be touched by a driver itself.
	_awaitingAck: bool = False
	#: Maximum timeout to use for communication with a device (in seconds).
	#: This can be used for serial connections.
	#: Furthermore, it is used to stop waiting for missed acknowledgement packets.
	timeout: float = 0.2

	def __init__(self, port: typing.Union[None, str, bdDetect.DeviceMatch] = None):
		"""Constructor
		@param port: Information on how to connect to the device.
			Use L{_getTryPorts} to normalise to L{DeviceMatch} instances.
			- A string (from config "config.conf["braille"][name]["port"]"). When manually configured.
				This value is set via the settings dialog, the source of the options provided to the user
				is the BrailleDisplayDriver.getPossiblePorts method.
			- A L{DeviceMatch} instance. When automatically detected.
		"""
		super().__init__()

	@classmethod
	def check(cls) -> bool:
		"""Determine whether this braille display is available.
		The display will be excluded from the list of available displays if this method returns C{False}.
		For example, if this display is not present, C{False} should be returned.
		@return: C{True} if this display is available, C{False} if not.
		"""
		if cls.isThreadSafe:
			supportsAutomaticDetection = cls.supportsAutomaticDetection
			if supportsAutomaticDetection and bdDetect.driverHasPossibleDevices(cls.name):
				return True
		try:
			next(cls.getManualPorts())
		except (StopIteration, NotImplementedError):
			pass
		else:
			return True
		return False

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: bdDetect.DriverRegistrar):
		"""
		This method may register the braille display driver in the braille display automatic detection framework.
		The framework provides a L{bdDetect.DriverRegistrar} object as its only parameter.
		The methods on the driver registrar can be used to register devices or device scanners.
		This method should only register itself with the bdDetect framework,
		and should refrain from doing anything else.
		Drivers with L{supportsAutomaticDetection} set to C{True} must implement this method.
		@param driverRegistrar: An object containing several methods to register device identifiers for this driver.
		"""
		raise NotImplementedError

	def terminate(self):
		"""Terminate this display driver.
		This will be called when NVDA is finished with this display driver.
		It should close any open connections, perform cleanup, etc.
		Subclasses should call the superclass method first.
		@postcondition: This instance can no longer be used unless it is constructed again.
		"""
		super().terminate()
		# Clear the display.
		try:
			self.display([0] * self.numCells)
		except Exception:
			# The display driver seems to be failing, but we're terminating anyway, so just ignore it.
			log.error(f"Display driver {self} failed to display while terminating.", exc_info=True)

	#: typing information for autoproperty _get_numCells
	numCells: int

	def _get_numCells(self) -> int:
		"""Obtain the number of braille cells on this display.
		@note: 0 indicates that braille should be disabled.
		@note: For multi line displays, this is the total number of cells (e.g. numRows * numCols)
		@return: The number of cells.
		"""
		return self.numRows * self.numCols

	def _set_numCells(self, numCells: int):
		if self.numRows > 1:
			raise ValueError(
				"Please set numCols explicitly and don't set numCells for multi line braille displays",
			)
		self.numCols = numCells

	#: Number of rows of the braille display, this will be 1 for most displays
	#: Note: Setting this to 0 will cause numCells to be 0 and hence will disable braille.
	numRows: int = 1

	#: Number of columns (cells per row) of the braille display
	#: 0 indicates that braille should be disabled.
	numCols: int = 0

	def __repr__(self):
		return f"{self.__class__.__name__}({self.name!r}, numCells={self.numCells!r})"

	def display(self, cells):
		"""Display the given braille cells.
		@param cells: The braille cells to display.
		@type cells: [int, ...]
		"""

	#: Automatic port constant to be used by braille displays that support the "automatic" port
	#: Kept for backwards compatibility
	AUTOMATIC_PORT = AUTOMATIC_PORT

	@classmethod
	def getPossiblePorts(cls) -> typing.OrderedDict[str, str]:
		"""Returns possible hardware ports for this driver.
		Optionally and in addition to the values from L{getManualPorts},
		three special values may be returned if the driver supports
		them, "auto", "usb", and "bluetooth".

		Generally, drivers shouldn't implement this method directly.
		Instead, they should provide automatic detection data via L{bdDetect}
		and implement L{getPossibleManualPorts} if they support manual ports
		such as serial ports.

		@return: Ordered dictionary for each port a (key : value) of name : translated description.
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
	def _getAutoPorts(cls, usb=True, bluetooth=True) -> Iterable[bdDetect.DeviceMatch]:
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
	def getManualPorts(cls) -> typing.Iterator[typing.Tuple[str, str]]:
		"""Get possible manual hardware ports for this driver.
		This is for ports which cannot be detected automatically
		such as serial ports.
		@return: An iterator containing the name and description for each port.
		"""
		raise NotImplementedError

	@classmethod
	def _getTryPorts(
		cls,
		port: Union[str, bdDetect.DeviceMatch],
	) -> typing.Iterator[bdDetect.DeviceMatch]:
		"""Returns the ports for this driver to which a connection attempt should be made.
		This generator function is usually used in L{__init__} to connect to the desired display.
		@param port: the port to connect to.
		@return: The name and description for each port
		"""
		if isinstance(port, bdDetect.DeviceMatch):
			yield port
		elif isinstance(port, str):
			isUsb = port in (AUTOMATIC_PORT[0], USB_PORT[0])
			isBluetooth = port in (AUTOMATIC_PORT[0], BLUETOOTH_PORT[0])
			if not isUsb and not isBluetooth:
				# Assume we are connecting to a com port, since these are the only manual ports supported.
				try:
					portInfo = next(info for info in hwPortUtils.listComPorts() if info["port"] == port)
				except StopIteration:
					pass
				else:
					yield bdDetect.DeviceMatch(
						bdDetect.ProtocolType.SERIAL,
						portInfo["bluetoothName" if "bluetoothName" in portInfo else "friendlyName"],
						portInfo["port"],
						portInfo,
					)
			else:
				for match in cls._getAutoPorts(usb=isUsb, bluetooth=isBluetooth):
					yield match

	#: Global input gesture map for this display driver.
	gestureMap: Optional[inputCore.GlobalGestureMap] = None

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
		prefixes = ["br({source})".format(source=cls.name)]
		if model:
			prefixes.insert(0, "br({source}.{model})".format(source=cls.name, model=model))
		for globalMap in globalMaps:
			for scriptCls, gesture, scriptName in globalMap.getScriptsForAllGestures():
				if (
					any(gesture.startswith(prefix.lower()) for prefix in prefixes)
					and scriptCls is globalCommands.GlobalCommands
					and scriptName
					and scriptName.startswith("kb")
				):
					emuGesture = keyboardHandler.KeyboardInputGesture.fromName(scriptName.split(":")[1])
					if emuGesture.isModifier:
						yield set(gesture.split(":")[1].split("+")), set(emuGesture._keyNamesInDisplayOrder)

	def _handleAck(self):
		"""Base implementation to handle acknowledgement packets."""
		if not self.receivesAckPackets:
			raise NotImplementedError("This display driver does not support ACK packet handling")
		if not ctypes.windll.kernel32.CancelWaitableTimer(handler.ackTimerHandle):
			raise ctypes.WinError()
		self._awaitingAck = False
		handler._writeCellsInBackground()

	@classmethod
	def DotFirmnessSetting(cls, defaultVal, minVal, maxVal, useConfig=False):
		"""Factory function for creating dot firmness setting."""
		return NumericDriverSetting(
			"dotFirmness",
			# Translators: Label for a setting in braille settings dialog.
			_("Dot firm&ness"),
			defaultVal=defaultVal,
			minVal=minVal,
			maxVal=maxVal,
			useConfig=useConfig,
		)

	@classmethod
	def BrailleInputSetting(cls, useConfig=True):
		"""Factory function for creating braille input setting."""
		return BooleanDriverSetting(
			"brailleInput",
			# Translators: Label for a setting in braille settings dialog.
			_("Braille inp&ut"),
			useConfig=useConfig,
		)

	@classmethod
	def HIDInputSetting(cls, useConfig):
		"""Factory function for creating HID input setting."""
		return BooleanDriverSetting(
			"hidKeyboardInput",
			# Translators: Label for a setting in braille settings dialog.
			_("&HID keyboard input simulation"),
			useConfig=useConfig,
		)


class BrailleDisplayGesture(inputCore.InputGesture):
	"""A button, wheel or other control pressed on a braille display.
	Subclasses must provide L{source} and L{id}.
	Optionally, L{model} can be provided to facilitate model specific gestures.
	L{routingIndex} should be provided for routing buttons.
	Subclasses can also inherit from L{brailleInput.BrailleInputGesture} if the display has a braille keyboard.
	If the braille display driver is a L{baseObject.ScriptableObject}, it can provide scripts specific to input gestures from this display.
	"""

	shouldPreventSystemIdle = True

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
		ids = ["br({source}):{id}".format(source=self.source, id=self.id)]
		if self.model:
			# Model based ids should take priority.
			ids.insert(
				0,
				"br({source}.{model}):{id}".format(source=self.source, model=self.model, id=self.id),
			)
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
		script = scriptHandler.findScript(self)
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
		if len(gestureKeys) > 1:
			for keys, modifiers in handler.display._getModifierGestures(self.model):
				if keys < gestureKeys:
					gestureModifiers |= modifiers
					gestureKeys -= keys
		if not gestureModifiers:
			return None
		if gestureKeys != set(self.keyNames):
			# Find a script for L{gestureKeys}.
			id = "+".join(gestureKeys)
			fakeGestureIds = ["br({source}):{id}".format(source=self.source, id=id)]
			if self.model:
				fakeGestureIds.insert(
					0,
					"br({source}.{model}):{id}".format(source=self.source, model=self.model, id=id),
				)
			scriptNames = []
			globalMaps = [inputCore.manager.userGestureMap, handler.display.gestureMap]
			for globalMap in globalMaps:
				for fakeGestureId in fakeGestureIds:
					scriptNames.extend(
						scriptName
						for cls, scriptName in globalMap.getScriptsForGesture(fakeGestureId.lower())
						if scriptName and scriptName.startswith("kb")
					)
			if not scriptNames:
				# Gesture contains modifiers, but no keyboard emulate script exists for the gesture without modifiers
				return None
			# We can't bother about multiple scripts for a gesture, we will just use the first one
			combinedScriptName = "kb:{modifiers}+{keys}".format(
				modifiers="+".join(gestureModifiers),
				keys=scriptNames[0].split(":")[1],
			)
		elif script and scriptName:
			combinedScriptName = "kb:{modifiers}+{keys}".format(
				modifiers="+".join(gestureModifiers),
				keys=scriptName.split(":")[1],
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

	def _get_speechEffectWhenExecuted(self) -> Optional[str]:
		from globalCommands import commands

		if not config.conf["braille"]["interruptSpeechWhileScrolling"] and self.script in {
			commands.script_braille_scrollBack,
			commands.script_braille_scrollForward,
		}:
			return None
		return super().speechEffectWhenExecuted

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
			log.error("Invalid braille gesture identifier: %s" % identifier)
			return unknownDisplayDescription, "malformed:%s" % identifier
		source, modelName, key = idParts.groups()
		# Optimisation: Do not try to get the braille display class if this identifier belongs to the current driver.
		if handler.display.name.lower() == source.lower():
			description = handler.display.description
		else:
			try:
				description = _getDisplayDriver(source, caseSensitive=False).description
			except ImportError:
				description = unknownDisplayDescription
		if modelName:  # The identifier contains a model name
			return description, "{modelName}: {key}".format(
				modelName=modelName,
				key=key,
			)
		else:
			return description, key


inputCore.registerGestureSource("br", BrailleDisplayGesture)


def getSerialPorts(filterFunc=None) -> typing.Iterator[typing.Tuple[str, str]]:
	"""Get available serial ports in a format suitable for L{BrailleDisplayDriver.getManualPorts}.
	@param filterFunc: a function executed on every dictionary retrieved using L{hwPortUtils.listComPorts}.
		For example, this can be used to filter by USB or Bluetooth com ports.
	@type filterFunc: callable
	"""
	if filterFunc and not callable(filterFunc):
		raise TypeError("The provided filterFunc is not callable")
	for info in hwPortUtils.listComPorts():
		if filterFunc and not filterFunc(info):
			continue
		if "bluetoothName" in info:
			yield (
				info["port"],
				# Translators: Name of a Bluetooth serial communications port.
				_("Bluetooth Serial: {port} ({deviceName})").format(
					port=info["port"],
					deviceName=info["bluetoothName"],
				),
			)
		else:
			yield (
				info["port"],
				# Translators: Name of a serial communications port.
				_("Serial: {portName}").format(portName=info["friendlyName"]),
			)


def getDisplayDrivers(
	filterFunc: Optional[Callable[[Type[BrailleDisplayDriver]], bool]] = None,
) -> Generator[Type[BrailleDisplayDriver], Any, Any]:
	"""Gets an iterator of braille display drivers meeting the given filter callable.
	@param filterFunc: an optional callable that receives a driver as its only argument and returns
		either True or False.
	@return: Iterator of braille display drivers.
	"""
	for loader, name, isPkg in pkgutil.iter_modules(brailleDisplayDrivers.__path__):
		if name.startswith("_"):
			continue
		try:
			display = _getDisplayDriver(name)
		except Exception:
			log.error(
				f"Error while importing braille display driver {name}",
				exc_info=True,
			)
			continue
		if not filterFunc or filterFunc(display):
			yield display


def _speakOnRouting(info: textInfos.TextInfo):
	"""Speaks the character at the cursor position after routing.

	:param info: The TextInfo at the cursor position after routing.
	"""
	if not config.conf["braille"]["speakOnRouting"]:
		return
	# Import late to avoid circular import.
	from speech.speech import spellTextInfo

	info.expand(textInfos.UNIT_CHARACTER)
	spellTextInfo(info)


def _speakOnNavigatingByUnit(info: textInfos.TextInfo, readingUnit: str) -> None:
	"""Speaks the reading unit after navigating by it with braille.

	This only has an effect if the user has enabled "Speak when navigating by line or paragraph" in braille settings.

	:param info: The TextInfo at the cursor position after navigating.
	:param readingUnit: The reading unit to expand TextInfo.
	"""
	if not config.conf["braille"]["speakOnNavigatingByUnit"]:
		return
	# Import late to avoid circular import.
	from speech.speech import cancelSpeech, speakTextInfo

	copy = info.copy()
	copy.expand(readingUnit)
	cancelSpeech()
	speakTextInfo(copy, unit=readingUnit, reason=controlTypes.OutputReason.CARET)
