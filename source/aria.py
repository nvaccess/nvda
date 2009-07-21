#aria.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import controlTypes

ariaRolesToNVDARoles={
	"application":controlTypes.ROLE_APPLICATION,
	"link":controlTypes.ROLE_LINK,
	"combobox":controlTypes.ROLE_COMBOBOX,
	"option":controlTypes.ROLE_LISTITEM,
	"checkbox":controlTypes.ROLE_CHECKBOX,
	"checkboxtristate":controlTypes.ROLE_CHECKBOX,
	"radio":controlTypes.ROLE_RADIOBUTTON,
	"radiogroup":controlTypes.ROLE_GROUPING,
	"button":controlTypes.ROLE_BUTTON,
	"menuitemradio":controlTypes.ROLE_MENUITEM,
	"menuitemcheckbox":controlTypes.ROLE_MENUITEM,
	"progressbar":controlTypes.ROLE_PROGRESSBAR,
	"secret":controlTypes.ROLE_EDITABLETEXT,
	"separator":controlTypes.ROLE_SEPARATOR,
	"slider":controlTypes.ROLE_SLIDER,
	"spinbutton":controlTypes.ROLE_SPINBUTTON,
	"textarea":controlTypes.ROLE_EDITABLETEXT,
	"textfield":controlTypes.ROLE_EDITABLETEXT,
	"tree":controlTypes.ROLE_TREEVIEW,
	"treegroup":controlTypes.ROLE_TREEVIEWITEM,
	"treeitem":controlTypes.ROLE_TREEVIEWITEM,
	"status":controlTypes.ROLE_STATUSBAR,
	"alert":controlTypes.ROLE_ALERT,
	"alertdialog":controlTypes.ROLE_DIALOG,
	"dialog":controlTypes.ROLE_DIALOG,
	"presentation":controlTypes.ROLE_TEXTFRAME,
	"document":controlTypes.ROLE_DOCUMENT,
	"group":controlTypes.ROLE_GROUPING,
	"imggroup":controlTypes.ROLE_GROUPING,
	"directory":controlTypes.ROLE_LIST,
	"region":controlTypes.ROLE_SECTION,
	"liveregion":controlTypes.ROLE_SECTION,
	"grid":controlTypes.ROLE_TABLE,
	"gridcell":controlTypes.ROLE_TABLECELL,
	"tabcontainer":controlTypes.ROLE_TABCONTROL,
	"tab":controlTypes.ROLE_TAB,
	"tabpanel":controlTypes.ROLE_PROPERTYPAGE,
	"tablist":controlTypes.ROLE_TABCONTROL,
	"table":controlTypes.ROLE_TABLE,
	"td":controlTypes.ROLE_TABLECELL,
	"th":controlTypes.ROLE_TABLECELL,
	"rowheader":controlTypes.ROLE_TABLEROWHEADER,
	"columnheader":controlTypes.ROLE_TABLECOLUMNHEADER,
	"list":controlTypes.ROLE_LIST,
	"listitem":controlTypes.ROLE_LISTITEM,
	"menu":controlTypes.ROLE_POPUPMENU,
	"toolbar":controlTypes.ROLE_TOOLBAR,
	"menubar":controlTypes.ROLE_MENUBAR,
	"menuitem":controlTypes.ROLE_MENUITEM,
	"breadcrumbs":controlTypes.ROLE_LIST,
}

landmarkRoles = {
	"banner": _("banner"),
	"complementary": _("complementary"),
	"contentinfo": _("content info"),
	"main": _("main"),
	"navigation": _("navigation"),
	"search": _("search"),
}
