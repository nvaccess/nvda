# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from typing import Dict, List, Optional, Set

from .role import Role, clickableRoles
from .state import State, STATES_SORTED
from .outputReason import OutputReason


def _processPositiveStates(
		role: Role,
		states: Set[State],
		reason: OutputReason,
		positiveStates: Optional[Set[State]] = None
) -> Set[State]:
	"""Processes the states for an object and returns the positive states to output for a specified reason.
	For example, if C{State.CHECKED} is in the returned states, it means that the processed object is checked.
	@param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
	@param states: The raw states for an object to process.
	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
	@param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
	positive.
	@return: The processed positive states.
	"""
	positiveStates = positiveStates.copy() if positiveStates is not None else states.copy()
	# The user never cares about certain states.
	if role == Role.EDITABLETEXT:
		positiveStates.discard(State.EDITABLE)
	if role != Role.LINK:
		positiveStates.discard(State.VISITED)
	positiveStates.discard(State.SELECTABLE)
	positiveStates.discard(State.FOCUSABLE)
	positiveStates.discard(State.CHECKABLE)
	if State.DRAGGING in positiveStates:
		# It's obvious that the control is draggable if it's being dragged.
		positiveStates.discard(State.DRAGGABLE)
	if role == Role.COMBOBOX:
		# Combo boxes inherently have a popup, so don't report it.
		positiveStates.discard(State.HASPOPUP)
	import config
	if not config.conf['documentFormatting']['reportClickable'] or role in clickableRoles:
		# This control is clearly clickable according to its role,
		# or reporting clickable just isn't useful,
		# or the user has explicitly requested no reporting clickable
		positiveStates.discard(State.CLICKABLE)
	if reason == OutputReason.QUERY:
		return positiveStates
	positiveStates.discard(State.DEFUNCT)
	positiveStates.discard(State.MODAL)
	positiveStates.discard(State.FOCUSED)
	positiveStates.discard(State.OFFSCREEN)
	positiveStates.discard(State.INVISIBLE)
	positiveStates.discard(State.INDETERMINATE)
	if reason != OutputReason.CHANGE:
		positiveStates.discard(State.LINKED)
		if role in (
			Role.LISTITEM,
			Role.TREEVIEWITEM,
			Role.MENUITEM,
			Role.TABLEROW,
			Role.CHECKBOX,
		) and State.SELECTABLE in states:
			positiveStates.discard(State.SELECTED)
	if role not in (Role.EDITABLETEXT, Role.CHECKBOX):
		positiveStates.discard(State.READONLY)
	if role == Role.CHECKBOX:
		positiveStates.discard(State.PRESSED)
	if role == Role.MENUITEM and State.HASPOPUP in positiveStates:
		# The user doesn't usually care if a submenu is expanded or collapsed.
		positiveStates.discard(State.COLLAPSED)
		positiveStates.discard(State.EXPANDED)
	if State.FOCUSABLE not in states:
		positiveStates.discard(State.EDITABLE)
	return positiveStates


def _processNegativeStates(
		role: Role,
		states: Set[State],
		reason: OutputReason,
		negativeStates: Optional[Set[State]] = None
) -> Set[State]:
	"""Processes the states for an object and returns the negative states to output for a specified reason.
	For example, if C{State.CHECKED} is in the returned states, it means that the processed object is not
	checked.
	@param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
	@param states: The raw states for an object to process.
	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS)}.
	@param negativeStates: Used for C{OutputReason.CHANGE}, specifies states changed from positive to
	negative.
	@return: The processed negative states.
	"""
	if reason == OutputReason.CHANGE and not isinstance(negativeStates, set):
		raise TypeError("negativeStates must be a set for this reason")
	speakNegatives = set()
	# Add the negative selected state if the control is selectable,
	# but only if it is reported for the reason of focus, or this is a change to the focused object.
	# The condition stops "not selected" from being spoken in some broken controls
	# when the state change for the previous focus is issued before the focus change.
	if (
		# Only include if the object is actually selectable
		State.SELECTABLE in states
		# Only include if the object is focusable (E.g. ARIA grid cells, but not standard html tables)
		and State.FOCUSABLE in states
		# Only include  if reporting the focus or when states are changing on the focus.
		# This is to avoid exposing it for things like caret movement in browse mode.
		and (reason == OutputReason.FOCUS or (reason == OutputReason.CHANGE and State.FOCUSED in states))
		and role in (
			Role.LISTITEM,
			Role.TREEVIEWITEM,
			Role.TABLEROW,
			Role.TABLECELL,
			Role.TABLECOLUMNHEADER,
			Role.TABLEROWHEADER,
			Role.CHECKBOX,
		)
	):
		speakNegatives.add(State.SELECTED)
	# Restrict "not checked" in a similar way to "not selected".
	if(
		(role in (Role.CHECKBOX, Role.RADIOBUTTON, Role.CHECKMENUITEM) or State.CHECKABLE in states)
		and (State.HALFCHECKED not in states)
		and (reason != OutputReason.CHANGE or State.FOCUSED in states)
	):
		speakNegatives.add(State.CHECKED)
	if role == Role.TOGGLEBUTTON:
		speakNegatives.add(State.PRESSED)
	if reason == OutputReason.CHANGE:
		# We want to speak this state only if it is changing to negative.
		speakNegatives.add(State.DROPTARGET)
		# We were given states which have changed to negative.
		# Return only those supplied negative states which should be spoken;
		# i.e. the states in both sets.
		speakNegatives &= negativeStates
		# #6946: if HALFCHECKED is present but CHECKED isn't, we should make sure we add CHECKED to speakNegatives.
		if (State.HALFCHECKED in negativeStates and State.CHECKED not in states):
			speakNegatives.add(State.CHECKED)
		if STATES_SORTED & negativeStates and not STATES_SORTED & states:
			# If the object has just stopped being sorted, just report not sorted.
			# The user doesn't care how it was sorted before.
			speakNegatives.add(State.SORTED)
		return speakNegatives
	else:
		# This is not a state change; only positive states were supplied.
		# Return all negative states which should be spoken, excluding the positive states.
		return speakNegatives - states


def processAndLabelStates(
		role: Role,
		states: Set[State],
		reason: OutputReason,
		positiveStates: Optional[Set[State]] = None,
		negativeStates: Optional[Set[State]] = None,
		positiveStateLabelDict: Dict[State, str] = {},
		negativeStateLabelDict: Dict[State, str] = {},
) -> List[str]:
	"""Processes the states for an object and returns the appropriate state labels for both positive and
	negative states.
	@param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
	@param states: The raw states for an object to process.
	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
	@param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
	positive.
	@param negativeStates: Used for C{OutputReason.CHANGE}, specifies states changed from positive to
	negative.
	@param positiveStateLabelDict: Dictionary containing state identifiers as keys and associated positive
	labels as their values.
	@param negativeStateLabelDict: Dictionary containing state identifiers as keys and associated negative
	labels as their values.
	@return: The labels of the relevant positive and negative states.
	"""
	mergedStateLabels = []
	positiveStates = _processPositiveStates(role, states, reason, positiveStates)
	negativeStates = _processNegativeStates(role, states, reason, negativeStates)
	for state in sorted(positiveStates | negativeStates):
		if state in positiveStates:
			mergedStateLabels.append(positiveStateLabelDict.get(state, state.displayString))
		elif state in negativeStates:
			mergedStateLabels.append(negativeStateLabelDict.get(state, state.negativeDisplayString))
	return mergedStateLabels
