# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import typing
from enum import StrEnum
from typing import Final, NamedTuple

import config
from config.configFlags import OutputMode, ReportSpellingErrors

import controlTypes

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
	# Translators: Displayed in braille when an object supports multiple selected items.
	controlTypes.State.MULTISELECTABLE: _("msel"),
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
CONTINUATION_SHAPE = 0xC0  #: Dots 7 and 8

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

#: Automatic constant to be used by braille displays that support the "automatic" port
#: and automatic braille display detection
#: @type: tuple
# Translators: String representing automatic port selection for braille displays.
AUTOMATIC_PORT = ("auto", _("Automatic"))
#: Used in place of a specific braille display driver name to indicate that
#: braille displays should be automatically detected and used.
#: @type: str
AUTO_DISPLAY_NAME = AUTOMATIC_PORT[0]

NO_BRAILLE_DISPLAY_NAME: Final[str] = "noBraille"
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

	def shouldBeUsed(self, key) -> bool:
		"""Determines if the formatting marker should be reported in braille.
		:param key: A key which represents an element that may be reported in braille.
		:return: `True` if the element should be reported, `False` otherwise.
		"""
		formatConfig = config.conf["documentFormatting"]
		if key in ("invalid-spelling", "invalid-grammar"):
			return bool(formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.BRAILLE)
		return formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE


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
	"invalid-spelling": FormattingMarker(
		# Translators: Brailled at the start of invalid spelling text.
		# This is the English letter "e" in braille.
		start=pgettext("braille formatting symbol", "⠑"),
		# Translators: Brailled at the end of invalid spelling text.
		# This is the English letter "e" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡑"),
	),
	"invalid-grammar": FormattingMarker(
		# Translators: Brailled at the start of invalid grammar text.
		# This is the English letter "g" in braille.
		start=pgettext("braille formatting symbol", "⠛"),
		# Translators: Brailled at the end of invalid grammar text.
		# This is the English letter "g" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡛"),
	),
}
