# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from typing import Dict


ROLE_UNKNOWN=0
ROLE_WINDOW=1
ROLE_TITLEBAR=2
ROLE_PANE=3
ROLE_DIALOG=4
ROLE_CHECKBOX=5
ROLE_RADIOBUTTON=6
ROLE_STATICTEXT=7
ROLE_EDITABLETEXT=8
ROLE_BUTTON=9
ROLE_MENUBAR=10
ROLE_MENUITEM=11
ROLE_POPUPMENU=12
ROLE_COMBOBOX=13
ROLE_LIST=14
ROLE_LISTITEM=15
ROLE_GRAPHIC=16
ROLE_HELPBALLOON=17
ROLE_TOOLTIP=18
ROLE_LINK=19
ROLE_TREEVIEW=20
ROLE_TREEVIEWITEM=21
ROLE_TAB=22
ROLE_TABCONTROL=23
ROLE_SLIDER=24
ROLE_PROGRESSBAR=25
ROLE_SCROLLBAR=26
ROLE_STATUSBAR=27
ROLE_TABLE=28
ROLE_TABLECELL=29
ROLE_TABLECOLUMN=30
ROLE_TABLEROW=31
ROLE_TABLECOLUMNHEADER=32
ROLE_TABLEROWHEADER=33
ROLE_FRAME=34
ROLE_TOOLBAR=35
ROLE_DROPDOWNBUTTON=36
ROLE_CLOCK=37
ROLE_SEPARATOR=38
ROLE_FORM=39
ROLE_HEADING=40
ROLE_HEADING1=41
ROLE_HEADING2=42
ROLE_HEADING3=43
ROLE_HEADING4=44
ROLE_HEADING5=45
ROLE_HEADING6=46
ROLE_PARAGRAPH=47
ROLE_BLOCKQUOTE=48
ROLE_TABLEHEADER=49
ROLE_TABLEBODY=50
ROLE_TABLEFOOTER=51
ROLE_DOCUMENT=52
ROLE_ANIMATION=53
ROLE_APPLICATION=54
ROLE_BOX=55
ROLE_GROUPING=56
ROLE_PROPERTYPAGE=57
ROLE_CANVAS=58
ROLE_CAPTION=59
ROLE_CHECKMENUITEM=60
ROLE_DATEEDITOR=61
ROLE_ICON=62
ROLE_DIRECTORYPANE=63
ROLE_EMBEDDEDOBJECT=64
ROLE_ENDNOTE=65
ROLE_FOOTER=66
ROLE_FOOTNOTE=67
ROLE_GLASSPANE=69
ROLE_HEADER=70
ROLE_IMAGEMAP=71
ROLE_INPUTWINDOW=72
ROLE_LABEL=73
ROLE_NOTE=74
ROLE_PAGE=75
ROLE_RADIOMENUITEM=76
ROLE_LAYEREDPANE=77
ROLE_REDUNDANTOBJECT=78
ROLE_ROOTPANE=79
ROLE_EDITBAR=80
ROLE_TERMINAL=82
ROLE_RICHEDIT=83
ROLE_RULER=84
ROLE_SCROLLPANE=85
ROLE_SECTION=86
ROLE_SHAPE=87
ROLE_SPLITPANE=88
ROLE_VIEWPORT=89
ROLE_TEAROFFMENU=90
ROLE_TEXTFRAME=91
ROLE_TOGGLEBUTTON=92
ROLE_BORDER=93
ROLE_CARET=94
ROLE_CHARACTER=95
ROLE_CHART=96
ROLE_CURSOR=97
ROLE_DIAGRAM=98
ROLE_DIAL=99
ROLE_DROPLIST=100
ROLE_SPLITBUTTON=101
ROLE_MENUBUTTON=102
ROLE_DROPDOWNBUTTONGRID=103
ROLE_MATH=104
ROLE_GRIP=105
ROLE_HOTKEYFIELD=106
ROLE_INDICATOR=107
ROLE_SPINBUTTON=108
ROLE_SOUND=109
ROLE_WHITESPACE=110
ROLE_TREEVIEWBUTTON=111
ROLE_IPADDRESS=112
ROLE_DESKTOPICON=113
ROLE_INTERNALFRAME=115
ROLE_DESKTOPPANE=116
ROLE_OPTIONPANE=117
ROLE_COLORCHOOSER=118
ROLE_FILECHOOSER=119
ROLE_FILLER=120
ROLE_MENU=121
ROLE_PANEL=122
ROLE_PASSWORDEDIT=123
ROLE_FONTCHOOSER=124
ROLE_LINE=125
ROLE_FONTNAME=126
ROLE_FONTSIZE=127
ROLE_BOLD=128
ROLE_ITALIC=129
ROLE_UNDERLINE=130
ROLE_FGCOLOR=131
ROLE_BGCOLOR=132
ROLE_SUPERSCRIPT=133
ROLE_SUBSCRIPT=134
ROLE_STYLE=135
ROLE_INDENT=136
ROLE_ALIGNMENT=137
ROLE_ALERT=138
ROLE_DATAGRID=139
ROLE_DATAITEM=140
ROLE_HEADERITEM=141
ROLE_THUMB=142
ROLE_CALENDAR=143
ROLE_VIDEO=144
ROLE_AUDIO=145
ROLE_CHARTELEMENT=146
ROLE_DELETED_CONTENT=147
ROLE_INSERTED_CONTENT=148
ROLE_LANDMARK = 149
ROLE_ARTICLE = 150
ROLE_REGION = 151
ROLE_FIGURE = 152
ROLE_MARKED_CONTENT = 153


roleLabels: Dict[int, str] = {
	# Translators: The word for an unknown control type.
	ROLE_UNKNOWN:_("unknown"),
	# Translators: The word for window of a program such as document window.
	ROLE_WINDOW:_("window"),
	# Translators: Used to identify title bar of a program.
	ROLE_TITLEBAR:_("title bar"),
	# Translators: The word used for pane such as desktop pane.
	ROLE_PANE:_("pane"),
	# Translators: The word used to denote a dialog box such as open dialog.
	ROLE_DIALOG:_("dialog"),
	# Translators: The text used to identify check boxes such as select check box.
	ROLE_CHECKBOX:_("check box"),
	# Translators: The text used to identify radio buttons such as yes or no radio button.
	ROLE_RADIOBUTTON:_("radio button"),
	# Translators: The word used to identify a static text such as dialog text.
	ROLE_STATICTEXT:_("text"),
	# Translators: The word used to identify edit fields such as subject edit field.
	ROLE_EDITABLETEXT:_("edit"),
	# Translators: The word used to identify a button such as OK button.
	ROLE_BUTTON:_("button"),
	# Translators: Text used to identify menu bar of a program.
	ROLE_MENUBAR:_("menu bar"),
	# Translators: Used to identify a menu item such as an item in file menu.
	ROLE_MENUITEM:_("menu item"),
	# Translators: The word used for menus such as edit menu.
	ROLE_POPUPMENU:_("menu"),
	# Translators: Used to identify combo boxes such as file type combo box.
	ROLE_COMBOBOX:_("combo box"),
	# Translators: The word used for lists such as folder list.
	ROLE_LIST:_("list"),
	# Translators: Used to identify a list item such as email list items.
	ROLE_LISTITEM:_("list item"),
	# Translators: The word used to identify graphics such as webpage graphics.
	ROLE_GRAPHIC:_("graphic"),
	# Translators: Used to identify help balloon (a circular window with helpful text such as notification text).
	ROLE_HELPBALLOON:_("help balloon"),
	# Translators: Used to identify a tooltip (a small window with additional text about selected item such as file information).
	ROLE_TOOLTIP:_("tool tip"),
	# Translators: Identifies a link in webpage documents.
	ROLE_LINK:_("link"),
	# Translators: Identifies a treeview (a tree-like structure such as treeviews for subfolders).
	ROLE_TREEVIEW:_("tree view"),
	# Translators: Identifies a tree view item.
	ROLE_TREEVIEWITEM:_("tree view item"),
	# Translators: The word presented for tabs in a tab enabled window.
	ROLE_TAB: pgettext("controlType", "tab"),
	# Translators: Identifies a tab control such as webpage tabs in web browsers.
	ROLE_TABCONTROL:_("tab control"),
	# Translators: Identifies a slider such as volume slider.
	ROLE_SLIDER:_("slider"),
	# Translators: Identifies a progress bar such as NvDA update progress.
	ROLE_PROGRESSBAR:_("progress bar"),
	# Translators: Identifies a scroll bar.
	ROLE_SCROLLBAR:_("scroll bar"),
	# Translators: Identifies a status bar (text at the bottom bar of the screen such as cursor position in a document).
	ROLE_STATUSBAR:_("status bar"),
	# Translators: Identifies a table such as ones used in various websites.
	ROLE_TABLE:_("table"),
	# Translators: Identifies a cell in a table.
	ROLE_TABLECELL:_("cell"),
	# Translators: Identifies a column (a group of vertical cells in a table).
	ROLE_TABLECOLUMN:_("column"),
	# Translators: Identifies a row (a group of horizontal cells in a table).
	ROLE_TABLEROW:_("row"),
	# Translators: Identifies a frame (a smaller window in a webpage or a document).
	ROLE_FRAME:_("frame"),
	# Translators: Identifies a tool bar.
	ROLE_TOOLBAR:_("tool bar"),
	# Translators: Identifies a column header in tables and spreadsheets.
	ROLE_TABLECOLUMNHEADER:_("column header"),
	# Translators: Identifies a row header in tables and spreadsheets.
	ROLE_TABLEROWHEADER:_("row header"),
	# Translators: Identifies a drop down button (a button that, when clicked, opens a menu of its own).
	ROLE_DROPDOWNBUTTON:_("drop down button"),
	# Translators: Identifies an element.
	ROLE_CLOCK:_("clock"),
	# Translators: Identifies a separator (a horizontal line drawn on the screen).
	ROLE_SEPARATOR:_("separator"),
	# Translators: Identifies a form (controls such as edit boxes, combo boxes and so on).
	ROLE_FORM:_("form"),
	# Translators: Identifies a heading (a bold text used for identifying a section).
	ROLE_HEADING:_("heading"),
	# Translators: Identifies a heading level.
	ROLE_HEADING1:_("heading 1"),
	# Translators: Identifies a heading level.
	ROLE_HEADING2:_("heading 2"),
	# Translators: Identifies a heading level.
	ROLE_HEADING3:_("heading 3"),
	# Translators: Identifies a heading level.
	ROLE_HEADING4:_("heading 4"),
	# Translators: Identifies a heading level.
	ROLE_HEADING5:_("heading 5"),
	# Translators: Identifies a heading level.
	ROLE_HEADING6:_("heading 6"),
	# Translators: Identifies a paragraph (a group of text surrounded by blank lines).
	ROLE_PARAGRAPH:_("paragraph"),
	# Translators: Presented for a section in a document which is a block quotation;
	# i.e. a long quotation in a separate paragraph distinguished by indentation, etc.
	# See http://en.wikipedia.org/wiki/Block_quotation
	ROLE_BLOCKQUOTE:_("block quote"),
	# Translators: Identifies a table header (a short text at the start of a table which describes what the table is about).
	ROLE_TABLEHEADER:_("table header"),
	# Translators: Identifies a table body (the main body of the table).
	ROLE_TABLEBODY:_("table body"),
	# Translators: Identifies a table footer (text placed at the end of the table).
	ROLE_TABLEFOOTER:_("table footer"),
	# Translators: Identifies a document (for example, a webpage document).
	ROLE_DOCUMENT:_("document"),
	# Translators: Identifies an animation in a document or a webpage.
	ROLE_ANIMATION:_("animation"),
	# Translators: Identifies an application in webpages.
	ROLE_APPLICATION:_("application"),
	# Translators: Identifies a box element.
	ROLE_BOX:_("box"),
	# Translators: Identifies a grouping (a number of related items grouped together, such as related options in dialogs).
	ROLE_GROUPING:_("grouping"),
	# Translators: Identifies a property page such as drive properties dialog.
	ROLE_PROPERTYPAGE:_("property page"),
	# Translators: Identifies a canvas element on webpages (a box with some background color with some text drawn on the box, like a canvas).
	ROLE_CANVAS:_("canvas"),
	# Translators: Identifies a caption (usually a short text identifying a picture or a graphic on websites).
	ROLE_CAPTION:_("caption"),
	# Translators: Identifies a check menu item (a menu item with a checkmark as part of the menu item's name).
	ROLE_CHECKMENUITEM:_("check menu item"),
	# Translators: Identifies a data edit field.
	ROLE_DATEEDITOR:_("date edit"),
	# Translators: Identifies an icon.
	ROLE_ICON:_("icon"),
	# Translators: Identifies a directory pane.
	ROLE_DIRECTORYPANE:_("directory pane"),
	# Translators: Identifies an object that is embedded in a document.
	ROLE_EMBEDDEDOBJECT:_("embedded object"),
	# Translators: Identifies an end note.
	ROLE_ENDNOTE:_("end note"),
	# Translators: Identifies a footer (usually text).
	ROLE_FOOTER:_("footer"),
	# Translators: Identifies a foot note (text at the end of a passage or used for anotations).
	ROLE_FOOTNOTE:_("foot note"),
	# Translators: Reported for an object which is a glass pane; i.e.
	# a pane that is guaranteed to be on top of all panes beneath it.
	ROLE_GLASSPANE:_("glass pane"),
	# Translators: Identifies a header (usually text at top of documents or on tops of pages).
	ROLE_HEADER:_("header"),
	# Translators: Identifies an image map (a type of graphical link).
	ROLE_IMAGEMAP:_("image map"),
	# Translators: Identifies an input window.
	ROLE_INPUTWINDOW:_("input window"),
	# Translators: Identifies a label.
	ROLE_LABEL:_("label"),
	# Translators: Identifies a note field.
	ROLE_NOTE:_("note"),
	# Translators: Identifies a page.
	ROLE_PAGE:_("page"),
	# Translators: Identifies a radio menu item.
	ROLE_RADIOMENUITEM:_("radio menu item"),
	# Translators: Identifies a layered pane.
	ROLE_LAYEREDPANE:_("layered pane"),
	# Translators: Identifies a redundant object.
	ROLE_REDUNDANTOBJECT:_("redundant object"),
	# Translators: Identifies a root pane.
	ROLE_ROOTPANE:_("root pane"),
	# Translators: May be reported for an editable text object in a toolbar.
	# This is deprecated and is not often (if ever) used.
	ROLE_EDITBAR:_("edit bar"),
	# Translators: Identifies a terminal window such as command prompt.
	ROLE_TERMINAL:_("terminal"),
	# Translators: Identifies a rich edit box (an edit box which allows entering formatting commands in addition to text; encountered on webpages and NvDA log viewer).
	ROLE_RICHEDIT:_("rich edit"),
	# Translators: Identifies a ruler object (commonly seen on some webpages and in some Office programs).
	ROLE_RULER:_("ruler"),
	# Translators: Identifies a scroll pane.
	ROLE_SCROLLPANE:_("scroll pane"),
	# Translators: Identifies a section of text.
	ROLE_SECTION:_("section"),
	# Translators: Identifies a shape.
	ROLE_SHAPE:_("shape"),
	# Translators: Identifies a split pane.
	ROLE_SPLITPANE:_("split pane"),
	# Translators: Reported for a view port; i.e. an object usually used in a scroll pane
	# which represents the portion of the entire data that the user can see.
	# As the user manipulates the scroll bars, the contents of the view port can change.
	ROLE_VIEWPORT:_("view port"),
	# Translators: Reported for an object that forms part of a menu system
	# but which can be undocked from or torn off the menu system
	# to exist as a separate window.
	ROLE_TEAROFFMENU:_("tear off menu"),
	# Translators: Identifies a text frame (a frame window which contains text).
	ROLE_TEXTFRAME:_("text frame"),
	# Translators: Identifies a toggle button (a button used to toggle something).
	ROLE_TOGGLEBUTTON:_("toggle button"),
	ROLE_BORDER:_("border"),
	# Translators: Identifies a caret object.
	ROLE_CARET:_("caret"),
	# Translators: Identifies a character field (should not be confused with edit fields).
	ROLE_CHARACTER:_("character"),
	# Translators: Identifies a chart (commonly seen on some websites and in some Office documents).
	ROLE_CHART:_("chart"),
	# Translators: Identifies a cursor object.
	ROLE_CURSOR:_("cursor"),
	# Translators: Identifies a diagram (seen on some websites and on Office documents).
	ROLE_DIAGRAM:_("diagram"),
	# Translators: Identifies a dial object.
	ROLE_DIAL:_("dial"),
	# Translators: Identifies a drop list.
	ROLE_DROPLIST:_("drop list"),
	# Translators: Identifies a split button (a control which performs different actions when different parts are clicked).
	ROLE_SPLITBUTTON:_("split button"),
	# Translators: Identifies a menu button (a button which opens a menu of items).
	ROLE_MENUBUTTON:_("menu button"),
	# Translators: Reported for a button which expands a grid when it is pressed.
	ROLE_DROPDOWNBUTTONGRID:_("drop down button grid"),
	# Translators: Identifies mathematical content.
	ROLE_MATH:_("math"),
	# Translators: Identifies a grip control.
	ROLE_GRIP:_("grip"),
	# Translators: Identifies a hot key field (a field where one can enter a hot key for something, such as assigning shortcut for icons on the desktop).
	ROLE_HOTKEYFIELD:_("hot key field"),
	# Translators: Identifies an indicator control.
	ROLE_INDICATOR:_("indicator"),
	# Translators: Identifies a spin button (a button used to go through options in a spinning fashion).
	ROLE_SPINBUTTON:_("spin button"),
	# Translators: Identifies a sound clip on websites.
	ROLE_SOUND:_("sound"),
	# Translators: Identifies a whitespace.
	ROLE_WHITESPACE:_("white space"),
	# Translators: Identifies a tree view button.
	ROLE_TREEVIEWBUTTON:_("tree view button"),
	# Translators: Identifies an IP address (an IP address field element).
	ROLE_IPADDRESS:_("IP address"),
	# Translators: Identifies a desktop icon (the icons on the desktop such as computer and various shortcuts for programs).
	ROLE_DESKTOPICON:_("desktop icon"),
	# Translators: Identifies an internal frame. This is usually a frame on a web page; i.e. a web page embedded within a web page.
	ROLE_INTERNALFRAME:_("frame"),
	# Translators: Identifies desktop pane (the desktop window).
	ROLE_DESKTOPPANE:_("desktop pane"),
	# Translators: Identifies an option pane.
	ROLE_OPTIONPANE:_("option pane"),
	# Translators: Identifies a color chooser.
	ROLE_COLORCHOOSER:_("color chooser"),
	# Translators: Identifies a file chooser (to select a file or groups of files from a list).
	ROLE_FILECHOOSER:_("file chooser"),
	ROLE_FILLER:_("filler"),
	# Translators: Identifies a menu such as file menu.
	ROLE_MENU:_("menu"),
	# Translators: Identifies a panel control for grouping related options.
	ROLE_PANEL:_("panel"),
	# Translators: Identifies a password field (a protected edit field for entering passwords such as when logging into web-based email sites).
	ROLE_PASSWORDEDIT:_("password edit"),
	# Translators: Identifies a font chooser.
	ROLE_FONTCHOOSER:_("font chooser"),
	ROLE_LINE:_("line"),
	# Translators: Identifies a font name.
	ROLE_FONTNAME:_("font name"),
	# Translators: Identifies font size.
	ROLE_FONTSIZE:_("font size"),
	# Translators: Describes text formatting.
	ROLE_BOLD:_("bold"),
	# Translators: Describes text formatting.
	ROLE_ITALIC:_("italic"),
	# Translators: Describes text formatting.
	ROLE_UNDERLINE:_("underline"),
	# Translators: Describes text formatting.
	ROLE_FGCOLOR:_("foreground color"),
	# Translators: Describes text formatting.
	ROLE_BGCOLOR:_("background color"),
	# Translators: Describes text formatting.
	ROLE_SUPERSCRIPT:_("superscript"),
	# Translators: Describes text formatting.
	ROLE_SUBSCRIPT:_("subscript"),
	# Translators: Describes style of text.
	ROLE_STYLE:_("style"),
	# Translators: Describes text formatting.
	ROLE_INDENT:_("indent"),
	# Translators: Describes text formatting.
	ROLE_ALIGNMENT:_("alignment"),
	# Translators: Identifies an alert window or bar (usually on Internet Explorer 9 and above for alerts such as file downloads or pop-up blocker).
	ROLE_ALERT:_("alert"),
	# Translators: Identifies a data grid control (a grid which displays data).
	ROLE_DATAGRID:_("data grid"),
	ROLE_DATAITEM:_("data item"),
	ROLE_HEADERITEM:_("header item"),
	# Translators: Identifies a thumb control (a button-like control for changing options).
	ROLE_THUMB:_("thumb control"),
	ROLE_CALENDAR:_("calendar"),
	ROLE_VIDEO:_("video"),
	ROLE_AUDIO:_("audio"),
	# Translators: Identifies a chart element.
	ROLE_CHARTELEMENT:_("chart element"),
	# Translators: Identifies deleted content. 
	ROLE_DELETED_CONTENT:_("deleted"),
	# Translators: Identifies inserted content. 
	ROLE_INSERTED_CONTENT:_("inserted"),
	# Translators: Identifies a landmark.
	ROLE_LANDMARK: _("landmark"),
	# Translators: Identifies an article.
	ROLE_ARTICLE: _("article"),
	# Translators: Identifies a region.
	ROLE_REGION: _("region"),
	# Translators: Identifies a figure (commonly seen on some websites).
	ROLE_FIGURE: _("figure"),
	# Translators: Identifies marked (highlighted) content
	ROLE_MARKED_CONTENT: _("marked content"),
}


silentRolesOnFocus={
	ROLE_PANE,
	ROLE_ROOTPANE,
	ROLE_FRAME,
	ROLE_UNKNOWN,
	ROLE_APPLICATION,
	ROLE_TABLECELL,
	ROLE_LISTITEM,
	ROLE_MENUITEM,
	ROLE_CHECKMENUITEM,
	ROLE_TREEVIEWITEM,
	ROLE_STATICTEXT,
	ROLE_BORDER,
}


silentValuesForRoles={
	ROLE_CHECKBOX,
	ROLE_RADIOBUTTON,
	ROLE_LINK,
	ROLE_MENUITEM,
	ROLE_APPLICATION,
}
