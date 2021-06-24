# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from typing import Dict


STATE_UNAVAILABLE=0X1
STATE_FOCUSED=0X2
STATE_SELECTED=0X4
STATE_BUSY=0X8
STATE_PRESSED=0X10
STATE_CHECKED=0X20
STATE_HALFCHECKED=0X40
STATE_READONLY=0X80
STATE_EXPANDED=0X100
STATE_COLLAPSED=0X200
STATE_INVISIBLE=0X400
STATE_VISITED=0X800
STATE_LINKED=0X1000
STATE_HASPOPUP=0X2000
STATE_PROTECTED=0X4000
STATE_REQUIRED=0X8000
STATE_DEFUNCT=0X10000
STATE_INVALID_ENTRY=0X20000
STATE_MODAL=0X40000
STATE_AUTOCOMPLETE=0x80000
STATE_MULTILINE=0X100000
STATE_ICONIFIED=0x200000
STATE_OFFSCREEN=0x400000
STATE_SELECTABLE=0x800000
STATE_FOCUSABLE=0x1000000
STATE_CLICKABLE=0x2000000
STATE_EDITABLE=0x4000000
STATE_CHECKABLE=0x8000000
STATE_DRAGGABLE=0x10000000
STATE_DRAGGING=0x20000000
STATE_DROPTARGET=0x40000000
STATE_SORTED=0x80000000
STATE_SORTED_ASCENDING=0x100000000
STATE_SORTED_DESCENDING=0x200000000
STATES_SORTED=frozenset([STATE_SORTED,STATE_SORTED_ASCENDING,STATE_SORTED_DESCENDING])
STATE_HASLONGDESC=0x400000000
STATE_PINNED=0x800000000
STATE_HASFORMULA=0x1000000000 #Mostly for spreadsheets
STATE_HASCOMMENT=0X2000000000
STATE_OBSCURED=0x4000000000
STATE_CROPPED=0x8000000000
STATE_OVERFLOWING=0x10000000000
STATE_UNLOCKED=0x20000000000
STATE_HAS_ARIA_DETAILS = 0x40000000000


stateLabels: Dict[int, str] = {
	# Translators: This is presented when a control or document is unavailable.
	STATE_UNAVAILABLE:_("unavailable"),
	# Translators: This is presented when a control has focus.
	STATE_FOCUSED:_("focused"),
	# Translators: This is presented when the control is selected.
	STATE_SELECTED:_("selected"),
	# Translators: This is presented when a document is busy.
	STATE_BUSY:_("busy"),
	# Translators: This is presented when a button is pressed.
	STATE_PRESSED:_("pressed"),
	# Translators: This is presented when a check box is checked.
	STATE_CHECKED:_("checked"),
	# Translators: This is presented when a three state check box is half checked.
	STATE_HALFCHECKED:_("half checked"),
	# Translators: This is presented when the control is a read-only control such as read-only edit box.
	STATE_READONLY:_("read only"),
	# Translators: This is presented when a tree view or submenu item is expanded.
	STATE_EXPANDED:_("expanded"),
	# Translators: This is presented when a tree view or submenu is collapsed.
	STATE_COLLAPSED:_("collapsed"),
	# Translators: This is presented when a control or a document becomes invisible.
	STATE_INVISIBLE:_("invisible"),
	# Translators: This is presented when a visited link is encountered.
	STATE_VISITED:_("visited"),
	# Translators: This is presented when a link is encountered.
	STATE_LINKED:_("linked"),
	# Translators: This is presented when the control menu item has a submenu.
	STATE_HASPOPUP:_("subMenu"),
	# Translators: This is presented when a protected control or a document is encountered.
	STATE_PROTECTED:_("protected"),
	# Translators: This is presented when a required form field is encountered.
	STATE_REQUIRED:_("required"),
	# Translators: Reported when an object no longer exists in the user interface;
	# i.e. it is dead and is no longer usable.
	STATE_DEFUNCT:_("defunct"),
	# Translators: This is presented when an invalid entry has been made.
	STATE_INVALID_ENTRY:_("invalid entry"),
	STATE_MODAL:_("modal"),
	# Translators: This is presented when a field supports auto completion of entered text such as email address field in Microsoft Outlook.
	STATE_AUTOCOMPLETE:_("has auto complete"),
	# Translators: This is presented when an edit field allows typing multiple lines of text such as comment fields on websites.
	STATE_MULTILINE:_("multi line"),
	STATE_ICONIFIED:_("iconified"),
	# Translators: Presented when the current control is located off screen.
	STATE_OFFSCREEN:_("off screen"),
	# Translators: Presented when the control allows selection such as text fields.
	STATE_SELECTABLE:_("selectable"),
	# Translators: Presented when a control can be moved to using system focus.
	STATE_FOCUSABLE:_("focusable"),
	# Translators: Presented when a control allows clicking via mouse (mostly presented on web controls).
	STATE_CLICKABLE:_("clickable"),
	STATE_EDITABLE:_("editable"),
	STATE_CHECKABLE:_("checkable"),
	STATE_DRAGGABLE:_("draggable"),
	STATE_DRAGGING:_("dragging"),
	# Translators: Reported where an object which is being dragged can be dropped.
	# This is only reported for objects that support accessible drag and drop.
	STATE_DROPTARGET:_("drop target"),
	STATE_SORTED:_("sorted"),
	STATE_SORTED_ASCENDING:_("sorted ascending"),
	STATE_SORTED_DESCENDING:_("sorted descending"),
	# Translators: a state that denotes that an object (usually a graphic) has a long description.
	STATE_HASLONGDESC:_("has long description"),
	# Translators: a state that denotes that an object has additional details (such as a comment section).
	STATE_HAS_ARIA_DETAILS: _("has details"),
	# Translators: a state that denotes that an object is pinned in its current location
	STATE_PINNED:_("pinned"),
	# Translators: a state that denotes the existance of a formula on a spreadsheet cell
	STATE_HASFORMULA:_("has formula"),
	# Translators: a state that denotes the existance of a comment.
	STATE_HASCOMMENT:_("has comment"),
	# Translators: a state that denotes that the object is covered partially or fully by another object
	STATE_OBSCURED:_("obscured"),
	# Translators: a state that denotes that the object(text) is cropped as it couldn't be accommodated in the allocated/available space
	STATE_CROPPED:_("cropped"),
	# Translators: a state that denotes that the object(text) is overflowing into the adjacent space
	STATE_OVERFLOWING:_("overflowing"),
	# Translators: a state that denotes that the object is unlocked (such as an unlocked cell in a protected Excel spreadsheet). 
	STATE_UNLOCKED:_("unlocked"),
}

negativeStateLabels={
	# Translators: This is presented when a selectable object (e.g. a list item) is not selected.
	STATE_SELECTED:_("not selected"),
	# Translators: This is presented when a button is not pressed.
	STATE_PRESSED:_("not pressed"),
	# Translators: This is presented when a checkbox is not checked.
	STATE_CHECKED:_("not checked"),
	# Translators: This is presented when drag and drop is finished.
	# This is only reported for objects which support accessible drag and drop.
	STATE_DROPTARGET:_("done dragging"),
}
