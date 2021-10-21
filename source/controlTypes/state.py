# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from typing import Dict

from utils.displayString import DisplayStringIntEnum


class State(DisplayStringIntEnum):
	@property
	def _displayStringLabels(self):
		return _stateLabels

	@property
	def negativeDisplayString(self) -> str:
		"""
		@return: The translated UI display string, used when referring to this value of the enum in the
		negative.
		"""
		try:
			return _negativeStateLabels[self]
		except KeyError:
			# Translators: Indicates that a particular state of an object is negated.
			# Separate strings have now been defined for commonly negated states (e.g. not selected and not
			# checked), but this still might be used in some other cases.
			# %s will be replaced with the full identifier of the negated state (e.g. selected).
			return _("not %s") % self.displayString

	UNAVAILABLE = 0x1
	FOCUSED = 0x2
	SELECTED = 0x4
	BUSY = 0x8
	PRESSED = 0x10
	CHECKED = 0x20
	HALFCHECKED = 0x40
	READONLY = 0x80
	EXPANDED = 0x100
	COLLAPSED = 0x200
	INVISIBLE = 0x400
	VISITED = 0x800
	LINKED = 0x1000
	HASPOPUP = 0x2000
	PROTECTED = 0x4000
	REQUIRED = 0x8000
	DEFUNCT = 0x10000
	INVALID_ENTRY = 0x20000
	MODAL = 0x40000
	AUTOCOMPLETE = 0x80000
	MULTILINE = 0x100000
	ICONIFIED = 0x200000
	OFFSCREEN = 0x400000
	SELECTABLE = 0x800000
	FOCUSABLE = 0x1000000
	CLICKABLE = 0x2000000
	EDITABLE = 0x4000000
	CHECKABLE = 0x8000000
	DRAGGABLE = 0x10000000
	DRAGGING = 0x20000000
	DROPTARGET = 0x40000000
	SORTED = 0x80000000
	SORTED_ASCENDING = 0x100000000
	SORTED_DESCENDING = 0x200000000
	HASLONGDESC = 0x400000000
	PINNED = 0x800000000
	HASFORMULA = 0x1000000000  # Mostly for spreadsheets
	HASCOMMENT = 0x2000000000
	OBSCURED = 0x4000000000
	CROPPED = 0x8000000000
	OVERFLOWING = 0x10000000000
	UNLOCKED = 0x20000000000
	HAS_ARIA_DETAILS = 0x40000000000
	HASNOTE = 0x80000000000


STATES_SORTED = frozenset([State.SORTED, State.SORTED_ASCENDING, State.SORTED_DESCENDING])


_stateLabels: Dict[State, str] = {
	# Translators: This is presented when a control or document is unavailable.
	State.UNAVAILABLE: _("unavailable"),
	# Translators: This is presented when a control has focus.
	State.FOCUSED: _("focused"),
	# Translators: This is presented when the control is selected.
	State.SELECTED: _("selected"),
	# Translators: This is presented when a document is busy.
	State.BUSY: _("busy"),
	# Translators: This is presented when a button is pressed.
	State.PRESSED: _("pressed"),
	# Translators: This is presented when a check box is checked.
	State.CHECKED: _("checked"),
	# Translators: This is presented when a three state check box is half checked.
	State.HALFCHECKED: _("half checked"),
	# Translators: This is presented when the control is a read-only control such as read-only edit box.
	State.READONLY: _("read only"),
	# Translators: This is presented when a tree view or submenu item is expanded.
	State.EXPANDED: _("expanded"),
	# Translators: This is presented when a tree view or submenu is collapsed.
	State.COLLAPSED: _("collapsed"),
	# Translators: This is presented when a control or a document becomes invisible.
	State.INVISIBLE: _("invisible"),
	# Translators: This is presented when a visited link is encountered.
	State.VISITED: _("visited"),
	# Translators: This is presented when a link is encountered.
	State.LINKED: _("linked"),
	# Translators: This is presented when the control menu item has a submenu.
	State.HASPOPUP: _("subMenu"),
	# Translators: This is presented when a protected control or a document is encountered.
	State.PROTECTED: _("protected"),
	# Translators: This is presented when a required form field is encountered.
	State.REQUIRED: _("required"),
	# Translators: Reported when an object no longer exists in the user interface;
	# i.e. it is dead and is no longer usable.
	State.DEFUNCT: _("defunct"),
	# Translators: This is presented when an invalid entry has been made.
	State.INVALID_ENTRY: _("invalid entry"),
	State.MODAL: _("modal"),
	# Translators: This is presented when a field supports auto completion of entered text such as email
	# address field in Microsoft Outlook.
	State.AUTOCOMPLETE: _("has auto complete"),
	# Translators: This is presented when an edit field allows typing multiple lines of text such as comment
	# fields on websites.
	State.MULTILINE: _("multi line"),
	State.ICONIFIED: _("iconified"),
	# Translators: Presented when the current control is located off screen.
	State.OFFSCREEN: _("off screen"),
	# Translators: Presented when the control allows selection such as text fields.
	State.SELECTABLE: _("selectable"),
	# Translators: Presented when a control can be moved to using system focus.
	State.FOCUSABLE: _("focusable"),
	# Translators: Presented when a control allows clicking via mouse (mostly presented on web controls).
	State.CLICKABLE: _("clickable"),
	State.EDITABLE: _("editable"),
	State.CHECKABLE: _("checkable"),
	State.DRAGGABLE: _("draggable"),
	State.DRAGGING: _("dragging"),
	# Translators: Reported where an object which is being dragged can be dropped.
	# This is only reported for objects that support accessible drag and drop.
	State.DROPTARGET: _("drop target"),
	State.SORTED: _("sorted"),
	State.SORTED_ASCENDING: _("sorted ascending"),
	State.SORTED_DESCENDING: _("sorted descending"),
	# Translators: a state that denotes that an object (usually a graphic) has a long description.
	State.HASLONGDESC: _("has long description"),
	# Translators: a state that denotes that an object has additional details (such as a comment section).
	State.HAS_ARIA_DETAILS: _("has details"),
	# Translators: a state that denotes that an object is pinned in its current location
	State.PINNED: _("pinned"),
	# Translators: a state that denotes the existance of a formula on a spreadsheet cell
	State.HASFORMULA: _("has formula"),
	# Translators: a state that denotes the existance of a comment.
	State.HASCOMMENT: _("has comment"),
	# Translators: a state that denotes that the object is covered partially or fully by another object
	State.OBSCURED: _("obscured"),
	# Translators: a state that denotes that the object(text) is cropped as it couldn't be accommodated in the
	# allocated/available space
	State.CROPPED: _("cropped"),
	# Translators: a state that denotes that the object(text) is overflowing into the adjacent space
	State.OVERFLOWING: _("overflowing"),
	# Translators: a state that denotes that the object is unlocked (such as an unlocked cell in a protected
	# Excel spreadsheet).
	State.UNLOCKED: _("unlocked"),
	# Translators: a state that denotes the existance of a note.
	State.HASNOTE: _("has note"),
}


_negativeStateLabels: Dict[State, str] = {
	# Translators: This is presented when a selectable object (e.g. a list item) is not selected.
	State.SELECTED: _("not selected"),
	# Translators: This is presented when a button is not pressed.
	State.PRESSED: _("not pressed"),
	# Translators: This is presented when a checkbox is not checked.
	State.CHECKED: _("not checked"),
	# Translators: This is presented when drag and drop is finished.
	# This is only reported for objects which support accessible drag and drop.
	State.DROPTARGET: _("done dragging"),
}
