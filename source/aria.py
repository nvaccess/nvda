# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2019 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
from typing import Dict

import controlTypes

ariaRolesToNVDARoles: Dict[str, int] = {
	"description": controlTypes.ROLE_STATICTEXT,  # Not in ARIA 1.1 spec
	"alert":controlTypes.ROLE_ALERT,
	"alertdialog":controlTypes.ROLE_DIALOG,
	"article": controlTypes.ROLE_ARTICLE,
	"application":controlTypes.ROLE_APPLICATION,
	"button":controlTypes.ROLE_BUTTON,
	"checkbox":controlTypes.ROLE_CHECKBOX,
	"columnheader":controlTypes.ROLE_TABLECOLUMNHEADER,
	"combobox":controlTypes.ROLE_COMBOBOX,
	"definition":controlTypes.ROLE_LISTITEM,
	"dialog":controlTypes.ROLE_DIALOG,
	"directory":controlTypes.ROLE_LIST,
	"document":controlTypes.ROLE_DOCUMENT,
	"figure": controlTypes.ROLE_FIGURE,
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
	"mark": controlTypes.ROLE_MARKED_CONTENT,
	"menu":controlTypes.ROLE_POPUPMENU,
	"menubar":controlTypes.ROLE_MENUBAR,
	"menuitem":controlTypes.ROLE_MENUITEM,
	"menuitemcheckbox":controlTypes.ROLE_MENUITEM,
	"menuitemradio":controlTypes.ROLE_MENUITEM,
	"option":controlTypes.ROLE_LISTITEM,
	"progressbar":controlTypes.ROLE_PROGRESSBAR,
	"radio":controlTypes.ROLE_RADIOBUTTON,
	"radiogroup":controlTypes.ROLE_GROUPING,
	"region": controlTypes.ROLE_REGION,
	"row":controlTypes.ROLE_TABLEROW,
	"rowgroup":controlTypes.ROLE_GROUPING,
	"rowheader":controlTypes.ROLE_TABLEROWHEADER,
	"search": controlTypes.ROLE_LANDMARK,
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

ariaSortValuesToNVDAStates: Dict[str, int] = {
	'descending':controlTypes.STATE_SORTED_DESCENDING,
	'ascending':controlTypes.STATE_SORTED_ASCENDING,
	'other':controlTypes.STATE_SORTED,
}

landmarkRoles: Dict[str, str] = {
	# Translators: Reported for the banner landmark, normally found on web pages.
	"banner": pgettext("aria", "banner"),
	# Translators: Reported for the complementary landmark, normally found on web pages.
	"complementary": pgettext("aria", "complementary"),
	# Translators: Reported for the contentinfo landmark, normally found on web pages.
	"contentinfo": pgettext("aria", "content info"),
	# Translators: Reported for the main landmark, normally found on web pages.
	"main": pgettext("aria", "main"),
	# Translators: Reported for the navigation landmark, normally found on web pages.
	"navigation": pgettext("aria", "navigation"),
	# Translators: Reported for the search landmark, normally found on web pages.
	"search": pgettext("aria", "search"),
	# Translators: Reported for the form landmark, normally found on web pages.
	"form": pgettext("aria", "form"),
}

ariaRolesToNVDARoles.update({
	role: controlTypes.ROLE_LANDMARK
	for role in landmarkRoles
	if role not in ariaRolesToNVDARoles
})

htmlNodeNameToAriaRoles: Dict[str, str] = {
	"header": "banner",
	"nav": "navigation",
	"main": "main",
	"footer": "contentinfo",
	"article": "article",
	"section": "region",
	"aside": "complementary",
	"dialog": "dialog",
	"figure": "figure",
	"mark": "mark",
}
