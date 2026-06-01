# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import typing

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
