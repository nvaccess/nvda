#aria.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2009-2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import controlTypes

ariaRolesToNVDARoles={
	"description":controlTypes.ROLE_STATICTEXT,
	"search":controlTypes.ROLE_SECTION,
	"alert":controlTypes.ROLE_ALERT,
	"alertdialog":controlTypes.ROLE_DIALOG,
	"application":controlTypes.ROLE_APPLICATION,
	"button":controlTypes.ROLE_BUTTON,
	"checkbox":controlTypes.ROLE_CHECKBOX,
	"columnheader":controlTypes.ROLE_TABLECOLUMNHEADER,
	"combobox":controlTypes.ROLE_COMBOBOX,
	"definition":controlTypes.ROLE_LISTITEM,
	"dialog":controlTypes.ROLE_DIALOG,
	"directory":controlTypes.ROLE_LIST,
	"document":controlTypes.ROLE_DOCUMENT,
	"form":controlTypes.ROLE_FORM,
	"grid":controlTypes.ROLE_TABLE,
	"gridcell":controlTypes.ROLE_TABLECELL,
	"group":controlTypes.ROLE_GROUPING,
	"heading":controlTypes.ROLE_HEADING,
	"img":controlTypes.ROLE_GRAPHIC,
	"link":controlTypes.ROLE_LINK,
	"list":controlTypes.ROLE_LIST,
	"listbox":controlTypes.ROLE_LIST,
	"listitem":controlTypes.ROLE_LISTITEM,
	"menu":controlTypes.ROLE_POPUPMENU,
	"menubar":controlTypes.ROLE_MENUBAR,
	"menuitem":controlTypes.ROLE_MENUITEM,
	"menuitemcheckbox":controlTypes.ROLE_MENUITEM,
	"menuitemradio":controlTypes.ROLE_MENUITEM,
	"option":controlTypes.ROLE_LISTITEM,
	"progressbar":controlTypes.ROLE_PROGRESSBAR,
	"radio":controlTypes.ROLE_RADIOBUTTON,
	"radiogroup":controlTypes.ROLE_GROUPING,
	"row":controlTypes.ROLE_TABLEROW,
	"rowgroup":controlTypes.ROLE_GROUPING,
	"rowheader":controlTypes.ROLE_TABLEROWHEADER,
	"separator":controlTypes.ROLE_SEPARATOR,
	"scrollbar":controlTypes.ROLE_SCROLLBAR,
	"slider":controlTypes.ROLE_SLIDER,
	"spinbutton":controlTypes.ROLE_SPINBUTTON,
	"status":controlTypes.ROLE_STATUSBAR,
	"tab":controlTypes.ROLE_TAB,
	"tablist":controlTypes.ROLE_TABCONTROL,
	"tabpanel":controlTypes.ROLE_PROPERTYPAGE,
	"textbox":controlTypes.ROLE_EDITABLETEXT,
	"toolbar":controlTypes.ROLE_TOOLBAR,
	"tooltip":controlTypes.ROLE_TOOLTIP,
	"tree":controlTypes.ROLE_TREEVIEW,
	"treegrid":controlTypes.ROLE_TREEVIEW,
	"treeitem":controlTypes.ROLE_TREEVIEWITEM,
}

ariaSortValuesToNVDAStates={
	'descending':controlTypes.STATE_SORTED_DESCENDING,
	'ascending':controlTypes.STATE_SORTED_ASCENDING,
	'other':controlTypes.STATE_SORTED,
}

landmarkRoles = {
	# Translators: Reported for the banner landmark, normally found on web pages.
	"banner": _("banner"),
	# Translators: Reported for the complementary landmark, normally found on web pages.
	"complementary": _("complementary"),
	# Translators: Reported for the contentinfo landmark, normally found on web pages.
	"contentinfo": _("content info"),
	# Translators: Reported for the main landmark, normally found on web pages.
	"main": _("main"),
	# Translators: Reported for the navigation landmark, normally found on web pages.
	"navigation": _("navigation"),
	# Translators: Reported for the search landmark, normally found on web pages.
	"search": _("search"),
	# Translators: Reported for the form landmark, normally found on web pages.
	"form": _("form"),
	# Strictly speaking, region isn't a landmark, but it is very similar.
	# Translators: Reported for a significant region, normally found on web pages.
	"region": _("region"),
}
