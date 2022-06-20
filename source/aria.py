# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2019 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Dict
from enum import Enum
import controlTypes

ariaRolesToNVDARoles: Dict[str, int] = {
	"description": controlTypes.Role.STATICTEXT,  # Not in ARIA 1.1 spec
	"alert":controlTypes.Role.ALERT,
	"alertdialog":controlTypes.Role.DIALOG,
	"article": controlTypes.Role.ARTICLE,
	"application":controlTypes.Role.APPLICATION,
	"button":controlTypes.Role.BUTTON,
	"checkbox":controlTypes.Role.CHECKBOX,
	"columnheader":controlTypes.Role.TABLECOLUMNHEADER,
	"combobox":controlTypes.Role.COMBOBOX,
	"definition":controlTypes.Role.LISTITEM,
	"dialog":controlTypes.Role.DIALOG,
	"directory":controlTypes.Role.LIST,
	"document":controlTypes.Role.DOCUMENT,
	"figure": controlTypes.Role.FIGURE,
	"form":controlTypes.Role.FORM,
	"grid":controlTypes.Role.TABLE,
	"gridcell":controlTypes.Role.TABLECELL,
	"group":controlTypes.Role.GROUPING,
	"heading":controlTypes.Role.HEADING,
	"img":controlTypes.Role.GRAPHIC,
	"link":controlTypes.Role.LINK,
	"list":controlTypes.Role.LIST,
	"listbox":controlTypes.Role.LIST,
	"listitem":controlTypes.Role.LISTITEM,
	"mark": controlTypes.Role.MARKED_CONTENT,
	"menu":controlTypes.Role.POPUPMENU,
	"menubar":controlTypes.Role.MENUBAR,
	"menuitem":controlTypes.Role.MENUITEM,
	"menuitemcheckbox":controlTypes.Role.MENUITEM,
	"menuitemradio":controlTypes.Role.MENUITEM,
	"option":controlTypes.Role.LISTITEM,
	"progressbar":controlTypes.Role.PROGRESSBAR,
	"radio":controlTypes.Role.RADIOBUTTON,
	"radiogroup":controlTypes.Role.GROUPING,
	"region": controlTypes.Role.REGION,
	"row":controlTypes.Role.TABLEROW,
	"rowgroup":controlTypes.Role.GROUPING,
	"rowheader":controlTypes.Role.TABLEROWHEADER,
	"search": controlTypes.Role.LANDMARK,
	"separator":controlTypes.Role.SEPARATOR,
	"scrollbar":controlTypes.Role.SCROLLBAR,
	"slider":controlTypes.Role.SLIDER,
	"spinbutton":controlTypes.Role.SPINBUTTON,
	"status":controlTypes.Role.STATUSBAR,
	"tab":controlTypes.Role.TAB,
	"tablist":controlTypes.Role.TABCONTROL,
	"tabpanel":controlTypes.Role.PROPERTYPAGE,
	"textbox":controlTypes.Role.EDITABLETEXT,
	"toolbar":controlTypes.Role.TOOLBAR,
	"tooltip":controlTypes.Role.TOOLTIP,
	"tree":controlTypes.Role.TREEVIEW,
	"treegrid":controlTypes.Role.TREEVIEW,
	"treeitem":controlTypes.Role.TREEVIEWITEM,
}

ariaSortValuesToNVDAStates: Dict[str, controlTypes.State] = {
	'descending':controlTypes.State.SORTED_DESCENDING,
	'ascending':controlTypes.State.SORTED_ASCENDING,
	'other':controlTypes.State.SORTED,
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
	role: controlTypes.Role.LANDMARK
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


class AriaLivePoliteness(str, Enum):
	OFF = "off"
	POLITE = "polite"
	ASSERTIVE = "assertive"
