# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2022 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Dict, Union
from enum import Enum
import controlTypes
from logHandler import log


def normalizeDetailsRole(detailsRole: Union[str, controlTypes.Role, None]) -> controlTypes.Role:
	"""
	The attribute detailsRole is determined in a number of cases.
	With focus mode, detailsRole is normalized on the NVDAObject level to controlType.Role.
	With browse mode, the attribute is added directly to the buffer as a string,
	either as a role string or a role integer.
	Braille and speech needs consistent normalization for translation and reporting.
	"""
	if detailsRole is None or detailsRole == controlTypes.Role.UNKNOWN:
		return controlTypes.Role.UNKNOWN

	if isinstance(detailsRole, str):
		if detailsRole.isdigit():
			from IAccessibleHandler import IAccessibleRolesToNVDARoles
			# get a role, but it may be unsupported
			detailsRole = IAccessibleRolesToNVDARoles.get(int(detailsRole), controlTypes.Role.UNKNOWN)
		else:
			# return a supported details role
			return supportedAriaDetailsRoles.get(detailsRole, controlTypes.Role.UNKNOWN)

	if isinstance(detailsRole, controlTypes.Role):
		if detailsRole in supportedAriaDetailsRoles.values():
			return detailsRole

	log.debug(f"Unexpected detailsRole: {type(detailsRole)}, value {repr(detailsRole)}")
	return controlTypes.Role.UNKNOWN


# Currently only defined in Chrome as of May 2022
# Refer to ComputeDetailsRoles
# https://chromium.googlesource.com/chromium/src/+/main/ui/accessibility/platform/ax_platform_node_base.cc#2419
supportedAriaDetailsRoles = {
	"comment": controlTypes.Role.COMMENT,
	"doc-footnote": controlTypes.Role.FOOTNOTE,
	# These roles are current unsupported by IAccessible2,
	# and as such, have not been fully implemented in NVDA.
	# They can only be fetched via the IA2Attribute "details-roles",
	# which is only supported in Chrome.
	# Currently maps to the IA2 role ROLE_LIST_ITEM
	# "doc-endnote": controlTypes.Role.ENDNOTE,
	# Currently maps to the IA2 role ROLE_GENERIC
	# "definition": controlTypes.Role.DEFINITION,
}


ariaRolesToNVDARoles: Dict[str, controlTypes.Role] = {
	"description": controlTypes.Role.STATICTEXT,  # Not in ARIA 1.1 spec
	"alert":controlTypes.Role.ALERT,
	"alertdialog":controlTypes.Role.DIALOG,
	"article": controlTypes.Role.ARTICLE,
	"application":controlTypes.Role.APPLICATION,
	"button":controlTypes.Role.BUTTON,
	"checkbox":controlTypes.Role.CHECKBOX,
	"columnheader":controlTypes.Role.TABLECOLUMNHEADER,
	"combobox":controlTypes.Role.COMBOBOX,
	"definition": controlTypes.Role.DEFINITION,
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
	"suggestion": controlTypes.Role.SUGGESTION,
	"comment": controlTypes.Role.COMMENT,
	"deletion": controlTypes.Role.DELETED_CONTENT,
	"insertion": controlTypes.Role.INSERTED_CONTENT,
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
