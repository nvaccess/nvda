# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from enum import (
	auto,
	unique,
)
from typing import Dict, Set

from utils.displayString import DisplayStringIntEnum


@unique
class Role(DisplayStringIntEnum):
	@property
	def _displayStringLabels(self):
		return _roleLabels

	# To maintain backwards compatibility, these Roles must maintain their values.
	# Add-on authors are recommended not to depend on values, instead
	# use role.name, and construct from string with controlTypes.Role[nameOfRole] eg. Role["CHECKBOX"]
	# Although unlikely to change, if names/values changing represents a significant risk for your add-on, then
	# consider decoupling, and maintain an internal mapping of Roles to add-on internal Roles.
	UNKNOWN = 0
	WINDOW = 1
	TITLEBAR = 2
	PANE = 3
	DIALOG = 4
	CHECKBOX = 5
	RADIOBUTTON = 6
	STATICTEXT = 7
	EDITABLETEXT = 8
	BUTTON = 9
	MENUBAR = 10
	MENUITEM = 11
	POPUPMENU = 12
	COMBOBOX = 13
	LIST = 14
	LISTITEM = 15
	GRAPHIC = 16
	HELPBALLOON = 17
	TOOLTIP = 18
	LINK = 19
	TREEVIEW = 20
	TREEVIEWITEM = 21
	TAB = 22
	TABCONTROL = 23
	SLIDER = 24
	PROGRESSBAR = 25
	SCROLLBAR = 26
	STATUSBAR = 27
	TABLE = 28
	TABLECELL = 29
	TABLECOLUMN = 30
	TABLEROW = 31
	TABLECOLUMNHEADER = 32
	TABLEROWHEADER = 33
	FRAME = 34
	TOOLBAR = 35
	DROPDOWNBUTTON = 36
	CLOCK = 37
	SEPARATOR = 38
	FORM = 39
	HEADING = 40
	HEADING1 = 41
	HEADING2 = 42
	HEADING3 = 43
	HEADING4 = 44
	HEADING5 = 45
	HEADING6 = 46
	PARAGRAPH = 47
	BLOCKQUOTE = 48
	TABLEHEADER = 49
	TABLEBODY = 50
	TABLEFOOTER = 51
	DOCUMENT = 52
	ANIMATION = 53
	APPLICATION = 54
	BOX = 55
	GROUPING = 56
	PROPERTYPAGE = 57
	CANVAS = 58
	CAPTION = 59
	CHECKMENUITEM = 60
	DATEEDITOR = 61
	ICON = 62
	DIRECTORYPANE = 63
	EMBEDDEDOBJECT = 64
	ENDNOTE = 65
	FOOTER = 66
	FOOTNOTE = 67
	GLASSPANE = 69
	HEADER = 70
	IMAGEMAP = 71
	INPUTWINDOW = 72
	LABEL = 73
	NOTE = 74
	PAGE = 75
	RADIOMENUITEM = 76
	LAYEREDPANE = 77
	REDUNDANTOBJECT = 78
	ROOTPANE = 79
	EDITBAR = 80
	# note 81 is missing
	TERMINAL = 82
	RICHEDIT = 83
	RULER = 84
	SCROLLPANE = 85
	SECTION = 86
	SHAPE = 87
	SPLITPANE = 88
	VIEWPORT = 89
	TEAROFFMENU = 90
	TEXTFRAME = 91
	TOGGLEBUTTON = 92
	BORDER = 93
	CARET = 94
	CHARACTER = 95
	CHART = 96
	CURSOR = 97
	DIAGRAM = 98
	DIAL = 99
	DROPLIST = 100
	SPLITBUTTON = 101
	MENUBUTTON = 102
	DROPDOWNBUTTONGRID = 103
	MATH = 104
	GRIP = 105
	HOTKEYFIELD = 106
	INDICATOR = 107
	SPINBUTTON = 108
	SOUND = 109
	WHITESPACE = 110
	TREEVIEWBUTTON = 111
	IPADDRESS = 112
	DESKTOPICON = 113
	INTERNALFRAME = 115
	DESKTOPPANE = 116
	OPTIONPANE = 117
	COLORCHOOSER = 118
	FILECHOOSER = 119
	FILLER = 120
	MENU = 121
	PANEL = 122
	PASSWORDEDIT = 123
	FONTCHOOSER = 124
	LINE = 125
	FONTNAME = 126
	FONTSIZE = 127
	BOLD = 128
	ITALIC = 129
	UNDERLINE = 130
	FGCOLOR = 131
	BGCOLOR = 132
	SUPERSCRIPT = 133
	SUBSCRIPT = 134
	STYLE = 135
	INDENT = 136
	ALIGNMENT = 137
	ALERT = 138
	DATAGRID = 139
	DATAITEM = 140
	HEADERITEM = 141
	THUMB = 142
	CALENDAR = 143
	VIDEO = 144
	AUDIO = 145
	CHARTELEMENT = 146
	DELETED_CONTENT = 147
	INSERTED_CONTENT = 148
	LANDMARK = 149
	ARTICLE = 150
	REGION = 151
	FIGURE = 152
	MARKED_CONTENT = 153
	BUSY_INDICATOR = 154  # Used for progress bars with indeterminate state
	# To maintain backwards compatibility, above Roles must maintain their values.


_roleLabels: Dict[Role, str] = {
	# Translators: The word for an unknown control type.
	Role.UNKNOWN: _("unknown"),
	# Translators: The word for window of a program such as document window.
	Role.WINDOW: _("window"),
	# Translators: Used to identify title bar of a program.
	Role.TITLEBAR: _("title bar"),
	# Translators: The word used for pane such as desktop pane.
	Role.PANE: _("pane"),
	# Translators: The word used to denote a dialog box such as open dialog.
	Role.DIALOG: _("dialog"),
	# Translators: The text used to identify check boxes such as select check box.
	Role.CHECKBOX: _("check box"),
	# Translators: The text used to identify radio buttons such as yes or no radio button.
	Role.RADIOBUTTON: _("radio button"),
	# Translators: The word used to identify a static text such as dialog text.
	Role.STATICTEXT: _("text"),
	# Translators: The word used to identify edit fields such as subject edit field.
	Role.EDITABLETEXT: _("edit"),
	# Translators: The word used to identify a button such as OK button.
	Role.BUTTON: _("button"),
	# Translators: Text used to identify menu bar of a program.
	Role.MENUBAR: _("menu bar"),
	# Translators: Used to identify a menu item such as an item in file menu.
	Role.MENUITEM: _("menu item"),
	# Translators: The word used for menus such as edit menu.
	Role.POPUPMENU: _("menu"),
	# Translators: Used to identify combo boxes such as file type combo box.
	Role.COMBOBOX: _("combo box"),
	# Translators: The word used for lists such as folder list.
	Role.LIST: _("list"),
	# Translators: Used to identify a list item such as email list items.
	Role.LISTITEM: _("list item"),
	# Translators: The word used to identify graphics such as webpage graphics.
	Role.GRAPHIC: _("graphic"),
	# Translators: Used to identify help balloon (a circular window with helpful text such as notification
	# text).
	Role.HELPBALLOON: _("help balloon"),
	# Translators: Used to identify a tooltip (a small window with additional text about selected item such as
	# file information).
	Role.TOOLTIP: _("tool tip"),
	# Translators: Identifies a link in webpage documents.
	Role.LINK: _("link"),
	# Translators: Identifies a treeview (a tree-like structure such as treeviews for subfolders).
	Role.TREEVIEW: _("tree view"),
	# Translators: Identifies a tree view item.
	Role.TREEVIEWITEM: _("tree view item"),
	# Translators: The word presented for tabs in a tab enabled window.
	Role.TAB: pgettext("controlType", "tab"),
	# Translators: Identifies a tab control such as webpage tabs in web browsers.
	Role.TABCONTROL: _("tab control"),
	# Translators: Identifies a slider such as volume slider.
	Role.SLIDER: _("slider"),
	# Translators: Identifies a progress bar such as NvDA update progress.
	Role.PROGRESSBAR: _("progress bar"),
	# Translators: Identifies a scroll bar.
	Role.SCROLLBAR: _("scroll bar"),
	# Translators: Identifies a status bar (text at the bottom bar of the screen such as cursor position in a
	# document).
	Role.STATUSBAR: _("status bar"),
	# Translators: Identifies a table such as ones used in various websites.
	Role.TABLE: _("table"),
	# Translators: Identifies a cell in a table.
	Role.TABLECELL: _("cell"),
	# Translators: Identifies a column (a group of vertical cells in a table).
	Role.TABLECOLUMN: _("column"),
	# Translators: Identifies a row (a group of horizontal cells in a table).
	Role.TABLEROW: _("row"),
	# Translators: Identifies a frame (a smaller window in a webpage or a document).
	Role.FRAME: _("frame"),
	# Translators: Identifies a tool bar.
	Role.TOOLBAR: _("tool bar"),
	# Translators: Identifies a column header in tables and spreadsheets.
	Role.TABLECOLUMNHEADER: _("column header"),
	# Translators: Identifies a row header in tables and spreadsheets.
	Role.TABLEROWHEADER: _("row header"),
	# Translators: Identifies a drop down button (a button that, when clicked, opens a menu of its own).
	Role.DROPDOWNBUTTON: _("drop down button"),
	# Translators: Identifies an element.
	Role.CLOCK: _("clock"),
	# Translators: Identifies a separator (a horizontal line drawn on the screen).
	Role.SEPARATOR: _("separator"),
	# Translators: Identifies a form (controls such as edit boxes, combo boxes and so on).
	Role.FORM: _("form"),
	# Translators: Identifies a heading (a bold text used for identifying a section).
	Role.HEADING: _("heading"),
	# Translators: Identifies a heading level.
	Role.HEADING1: _("heading 1"),
	# Translators: Identifies a heading level.
	Role.HEADING2: _("heading 2"),
	# Translators: Identifies a heading level.
	Role.HEADING3: _("heading 3"),
	# Translators: Identifies a heading level.
	Role.HEADING4: _("heading 4"),
	# Translators: Identifies a heading level.
	Role.HEADING5: _("heading 5"),
	# Translators: Identifies a heading level.
	Role.HEADING6: _("heading 6"),
	# Translators: Identifies a paragraph (a group of text surrounded by blank lines).
	Role.PARAGRAPH: _("paragraph"),
	# Translators: Presented for a section in a document which is a block quotation;
	# i.e. a long quotation in a separate paragraph distinguished by indentation, etc.
	# See http://en.wikipedia.org/wiki/Block_quotation
	Role.BLOCKQUOTE: _("block quote"),
	# Translators: Identifies a table header (a short text at the start of a table which describes what the
	# table is about).
	Role.TABLEHEADER: _("table header"),
	# Translators: Identifies a table body (the main body of the table).
	Role.TABLEBODY: _("table body"),
	# Translators: Identifies a table footer (text placed at the end of the table).
	Role.TABLEFOOTER: _("table footer"),
	# Translators: Identifies a document (for example, a webpage document).
	Role.DOCUMENT: _("document"),
	# Translators: Identifies an animation in a document or a webpage.
	Role.ANIMATION: _("animation"),
	# Translators: Identifies an application in webpages.
	Role.APPLICATION: _("application"),
	# Translators: Identifies a box element.
	Role.BOX: _("box"),
	# Translators: Identifies a grouping (a number of related items grouped together, such as related options
	# in dialogs).
	Role.GROUPING: _("grouping"),
	# Translators: Identifies a property page such as drive properties dialog.
	Role.PROPERTYPAGE: _("property page"),
	# Translators: Identifies a canvas element on webpages (a box with some background color with some text
	# drawn on the box, like a canvas).
	Role.CANVAS: _("canvas"),
	# Translators: Identifies a caption (usually a short text identifying a picture or a graphic on websites).
	Role.CAPTION: _("caption"),
	# Translators: Identifies a check menu item (a menu item with a checkmark as part of the menu item's
	# name).
	Role.CHECKMENUITEM: _("check menu item"),
	# Translators: Identifies a data edit field.
	Role.DATEEDITOR: _("date edit"),
	# Translators: Identifies an icon.
	Role.ICON: _("icon"),
	# Translators: Identifies a directory pane.
	Role.DIRECTORYPANE: _("directory pane"),
	# Translators: Identifies an object that is embedded in a document.
	Role.EMBEDDEDOBJECT: _("embedded object"),
	# Translators: Identifies an end note.
	Role.ENDNOTE: _("end note"),
	# Translators: Identifies a footer (usually text).
	Role.FOOTER: _("footer"),
	# Translators: Identifies a foot note (text at the end of a passage or used for anotations).
	Role.FOOTNOTE: _("foot note"),
	# Translators: Reported for an object which is a glass pane; i.e.
	# a pane that is guaranteed to be on top of all panes beneath it.
	Role.GLASSPANE: _("glass pane"),
	# Translators: Identifies a header (usually text at top of documents or on tops of pages).
	Role.HEADER: _("header"),
	# Translators: Identifies an image map (a type of graphical link).
	Role.IMAGEMAP: _("image map"),
	# Translators: Identifies an input window.
	Role.INPUTWINDOW: _("input window"),
	# Translators: Identifies a label.
	Role.LABEL: _("label"),
	# Translators: Identifies a note field.
	Role.NOTE: _("note"),
	# Translators: Identifies a page.
	Role.PAGE: _("page"),
	# Translators: Identifies a radio menu item.
	Role.RADIOMENUITEM: _("radio menu item"),
	# Translators: Identifies a layered pane.
	Role.LAYEREDPANE: _("layered pane"),
	# Translators: Identifies a redundant object.
	Role.REDUNDANTOBJECT: _("redundant object"),
	# Translators: Identifies a root pane.
	Role.ROOTPANE: _("root pane"),
	# Translators: May be reported for an editable text object in a toolbar.
	# This is deprecated and is not often (if ever) used.
	Role.EDITBAR: _("edit bar"),
	# Translators: Identifies a terminal window such as command prompt.
	Role.TERMINAL: _("terminal"),
	# Translators: Identifies a rich edit box (an edit box which allows entering formatting commands in
	# addition to text; encountered on webpages and NvDA log viewer).
	Role.RICHEDIT: _("rich edit"),
	# Translators: Identifies a ruler object (commonly seen on some webpages and in some Office programs).
	Role.RULER: _("ruler"),
	# Translators: Identifies a scroll pane.
	Role.SCROLLPANE: _("scroll pane"),
	# Translators: Identifies a section of text.
	Role.SECTION: _("section"),
	# Translators: Identifies a shape.
	Role.SHAPE: _("shape"),
	# Translators: Identifies a split pane.
	Role.SPLITPANE: _("split pane"),
	# Translators: Reported for a view port; i.e. an object usually used in a scroll pane
	# which represents the portion of the entire data that the user can see.
	# As the user manipulates the scroll bars, the contents of the view port can change.
	Role.VIEWPORT: _("view port"),
	# Translators: Reported for an object that forms part of a menu system
	# but which can be undocked from or torn off the menu system
	# to exist as a separate window.
	Role.TEAROFFMENU: _("tear off menu"),
	# Translators: Identifies a text frame (a frame window which contains text).
	Role.TEXTFRAME: _("text frame"),
	# Translators: Identifies a toggle button (a button used to toggle something).
	Role.TOGGLEBUTTON: _("toggle button"),
	Role.BORDER: _("border"),
	# Translators: Identifies a caret object.
	Role.CARET: _("caret"),
	# Translators: Identifies a character field (should not be confused with edit fields).
	Role.CHARACTER: _("character"),
	# Translators: Identifies a chart (commonly seen on some websites and in some Office documents).
	Role.CHART: _("chart"),
	# Translators: Identifies a cursor object.
	Role.CURSOR: _("cursor"),
	# Translators: Identifies a diagram (seen on some websites and on Office documents).
	Role.DIAGRAM: _("diagram"),
	# Translators: Identifies a dial object.
	Role.DIAL: _("dial"),
	# Translators: Identifies a drop list.
	Role.DROPLIST: _("drop list"),
	# Translators: Identifies a split button (a control which performs different actions when different parts
	# are clicked).
	Role.SPLITBUTTON: _("split button"),
	# Translators: Identifies a menu button (a button which opens a menu of items).
	Role.MENUBUTTON: _("menu button"),
	# Translators: Reported for a button which expands a grid when it is pressed.
	Role.DROPDOWNBUTTONGRID: _("drop down button grid"),
	# Translators: Identifies mathematical content.
	Role.MATH: _("math"),
	# Translators: Identifies a grip control.
	Role.GRIP: _("grip"),
	# Translators: Identifies a hot key field (a field where one can enter a hot key for something, such as
	# assigning shortcut for icons on the desktop).
	Role.HOTKEYFIELD: _("hot key field"),
	# Translators: Identifies an indicator control.
	Role.INDICATOR: _("indicator"),
	# Translators: Identifies a spin button (a button used to go through options in a spinning fashion).
	Role.SPINBUTTON: _("spin button"),
	# Translators: Identifies a sound clip on websites.
	Role.SOUND: _("sound"),
	# Translators: Identifies a whitespace.
	Role.WHITESPACE: _("white space"),
	# Translators: Identifies a tree view button.
	Role.TREEVIEWBUTTON: _("tree view button"),
	# Translators: Identifies an IP address (an IP address field element).
	Role.IPADDRESS: _("IP address"),
	# Translators: Identifies a desktop icon (the icons on the desktop such as computer and various shortcuts
	# for programs).
	Role.DESKTOPICON: _("desktop icon"),
	# Translators: Identifies an internal frame. This is usually a frame on a web page; i.e. a web page
	# embedded within a web page.
	Role.INTERNALFRAME: _("frame"),
	# Translators: Identifies desktop pane (the desktop window).
	Role.DESKTOPPANE: _("desktop pane"),
	# Translators: Identifies an option pane.
	Role.OPTIONPANE: _("option pane"),
	# Translators: Identifies a color chooser.
	Role.COLORCHOOSER: _("color chooser"),
	# Translators: Identifies a file chooser (to select a file or groups of files from a list).
	Role.FILECHOOSER: _("file chooser"),
	Role.FILLER: _("filler"),
	# Translators: Identifies a menu such as file menu.
	Role.MENU: _("menu"),
	# Translators: Identifies a panel control for grouping related options.
	Role.PANEL: _("panel"),
	# Translators: Identifies a password field (a protected edit field for entering passwords such as when
	# logging into web-based email sites).
	Role.PASSWORDEDIT: _("password edit"),
	# Translators: Identifies a font chooser.
	Role.FONTCHOOSER: _("font chooser"),
	Role.LINE: _("line"),
	# Translators: Identifies a font name.
	Role.FONTNAME: _("font name"),
	# Translators: Identifies font size.
	Role.FONTSIZE: _("font size"),
	# Translators: Describes text formatting.
	Role.BOLD: _("bold"),
	# Translators: Describes text formatting.
	Role.ITALIC: _("italic"),
	# Translators: Describes text formatting.
	Role.UNDERLINE: _("underline"),
	# Translators: Describes text formatting.
	Role.FGCOLOR: _("foreground color"),
	# Translators: Describes text formatting.
	Role.BGCOLOR: _("background color"),
	# Translators: Describes text formatting.
	Role.SUPERSCRIPT: _("superscript"),
	# Translators: Describes text formatting.
	Role.SUBSCRIPT: _("subscript"),
	# Translators: Describes style of text.
	Role.STYLE: _("style"),
	# Translators: Describes text formatting.
	Role.INDENT: _("indent"),
	# Translators: Describes text formatting.
	Role.ALIGNMENT: _("alignment"),
	# Translators: Identifies an alert window or bar (usually on Internet Explorer 9 and above for alerts such
	# as file downloads or pop-up blocker).
	Role.ALERT: _("alert"),
	# Translators: Identifies a data grid control (a grid which displays data).
	Role.DATAGRID: _("data grid"),
	Role.DATAITEM: _("data item"),
	Role.HEADERITEM: _("header item"),
	# Translators: Identifies a thumb control (a button-like control for changing options).
	Role.THUMB: _("thumb control"),
	Role.CALENDAR: _("calendar"),
	Role.VIDEO: _("video"),
	Role.AUDIO: _("audio"),
	# Translators: Identifies a chart element.
	Role.CHARTELEMENT: _("chart element"),
	# Translators: Identifies deleted content.
	Role.DELETED_CONTENT: _("deleted"),
	# Translators: Identifies inserted content.
	Role.INSERTED_CONTENT: _("inserted"),
	# Translators: Identifies a landmark.
	Role.LANDMARK: _("landmark"),
	# Translators: Identifies an article.
	Role.ARTICLE: _("article"),
	# Translators: Identifies a region.
	Role.REGION: _("region"),
	# Translators: Identifies a figure (commonly seen on some websites).
	Role.FIGURE: _("figure"),
	# Translators: Identifies marked (highlighted) content
	Role.MARKED_CONTENT: _("highlighted"),
	# Translators: Identifies a progress bar with indeterminate state, I.E. progress can not be determined.
	Role.BUSY_INDICATOR: _("busy indicator"),
}


silentRolesOnFocus: Set[Role] = {
	Role.PANE,
	Role.ROOTPANE,
	Role.FRAME,
	Role.UNKNOWN,
	Role.APPLICATION,
	Role.TABLECELL,
	Role.LISTITEM,
	Role.MENUITEM,
	Role.CHECKMENUITEM,
	Role.TREEVIEWITEM,
	Role.STATICTEXT,
	Role.BORDER,
}


silentValuesForRoles: Set[Role] = {
	Role.CHECKBOX,
	Role.RADIOBUTTON,
	Role.LINK,
	Role.MENUITEM,
	Role.APPLICATION,
	Role.BUSY_INDICATOR,
}


clickableRoles: Set[Role] = {
	Role.LINK,
	Role.BUTTON,
	Role.CHECKBOX,
	Role.RADIOBUTTON,
	Role.TOGGLEBUTTON,
	Role.MENUITEM,
	Role.TAB,
	Role.SLIDER,
	Role.DOCUMENT,
	Role.CHECKMENUITEM,
	Role.RADIOMENUITEM,
}
