# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from enum import (
	auto,
	unique,
)
from typing import Dict

from utils.displayString import DisplayStringIntEnum


def setBit(bitPos: int) -> int:
	return 0x1 << bitPos


@unique
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

	UNAVAILABLE = setBit(0)
	FOCUSED = setBit(1)
	SELECTED = setBit(2)
	BUSY = setBit(3)
	PRESSED = setBit(4)
	CHECKED = setBit(5)
	HALFCHECKED = setBit(6)
	READONLY = setBit(7)
	EXPANDED = setBit(8)
	COLLAPSED = setBit(9)
	INVISIBLE = setBit(10)
	VISITED = setBit(11)
	LINKED = setBit(12)
	HASPOPUP = setBit(13)
	PROTECTED = setBit(14)
	REQUIRED = setBit(15)
	DEFUNCT = setBit(16)
	INVALID_ENTRY = setBit(17)
	MODAL = setBit(18)
	AUTOCOMPLETE = setBit(19)
	MULTILINE = setBit(20)
	ICONIFIED = setBit(21)
	OFFSCREEN = setBit(22)
	SELECTABLE = setBit(23)
	FOCUSABLE = setBit(24)
	CLICKABLE = setBit(25)
	EDITABLE = setBit(26)
	CHECKABLE = setBit(27)
	DRAGGABLE = setBit(28)
	DRAGGING = setBit(29)
	DROPTARGET = setBit(30)
	SORTED = setBit(31)
	SORTED_ASCENDING = setBit(32)
	SORTED_DESCENDING = setBit(33)
	HASLONGDESC = setBit(34)
	PINNED = setBit(35)
	HASFORMULA = setBit(36)  # Mostly for spreadsheets
	HASCOMMENT = setBit(37)
	OBSCURED = setBit(38)
	CROPPED = setBit(39)
	OVERFLOWING = setBit(40)
	UNLOCKED = setBit(41)
	# HAS_ARIA_DETAILS is not used internally.
	# See instead NVDAObject.hasDetails introduced with commit aa351c55ada5254e061957097a9e0e638091b13d
	# This enum value was initially added to controlTypes.py in commit d6787b8f47861f5e76aba68da7a13a217404196f
	HAS_ARIA_DETAILS = setBit(42)  # Restored for backwards compat only.
	HASNOTE = setBit(43)
	# indeterminate progress bar, aka busy indicator. No specific state label.
	# when combined with role of 'progress bar', role is mutated to 'busy indicator'
	INDETERMINATE = setBit(44)


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
	# Translators: a state that denotes the existence of a note.
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
