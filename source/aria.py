#aria.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import controlTypes

ariaRolesToNVDARoles={
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
	"listbox":controlTypes.ROLE_LISTITEM,
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
	"textbox":controlTypes.ROLE_STATICTEXT,
	"toolbar":controlTypes.ROLE_TOOLBAR,
	"tooltip":controlTypes.ROLE_TOOLTIP,
	"tree":controlTypes.ROLE_TREEVIEW,
	"treegrid":controlTypes.ROLE_TREEVIEW,
	"treeitem":controlTypes.ROLE_TREEVIEWITEM,
}

landmarkRoles = {
	"banner": _("banner"),
	"complementary": _("complementary"),
	"contentinfo": _("content info"),
	"main": _("main"),
	"navigation": _("navigation"),
	"search": _("search"),
}
