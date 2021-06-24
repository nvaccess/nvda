# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from typing import Any, Dict, List, Optional, Set

from .role import *
from .state import STATES_SORTED, negativeStateLabels, stateLabels, *
from .outputReason import OutputReason


def processPositiveStates(role, states, reason: OutputReason, positiveStates=None):
	"""Processes the states for an object and returns the positive states to output for a specified reason.
	For example, if C{STATE_CHECKED} is in the returned states, it means that the processed object is checked.
	@param role: The role of the object to process states for (e.g. C{ROLE_CHECKBOX}.
	@type role: int
	@param states: The raw states for an object to process.
	@type states: set
	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}.
	@param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to positive;
	@type positiveStates: set
	@return: The processed positive states.
	@rtype: set
	"""
	positiveStates = positiveStates.copy() if positiveStates is not None else states.copy()
	# The user never cares about certain states.
	if role==ROLE_EDITABLETEXT:
		positiveStates.discard(STATE_EDITABLE)
	if role!=ROLE_LINK:
		positiveStates.discard(STATE_VISITED)
	positiveStates.discard(STATE_SELECTABLE)
	positiveStates.discard(STATE_FOCUSABLE)
	positiveStates.discard(STATE_CHECKABLE)
	if STATE_DRAGGING in positiveStates:
		# It's obvious that the control is draggable if it's being dragged.
		positiveStates.discard(STATE_DRAGGABLE)
	if role == ROLE_COMBOBOX:
		# Combo boxes inherently have a popup, so don't report it.
		positiveStates.discard(STATE_HASPOPUP)
	import config
	if not config.conf['documentFormatting']['reportClickable'] or role in (ROLE_LINK, ROLE_BUTTON, ROLE_CHECKBOX, ROLE_RADIOBUTTON, ROLE_TOGGLEBUTTON, ROLE_MENUITEM, ROLE_TAB, ROLE_SLIDER, ROLE_DOCUMENT, ROLE_CHECKMENUITEM, ROLE_RADIOMENUITEM):
		# This control is clearly clickable according to its role,
		# or reporting clickable just isn't useful,
		# or the user has explicitly requested no reporting clickable
		positiveStates.discard(STATE_CLICKABLE)
	if reason == OutputReason.QUERY:
		return positiveStates
	positiveStates.discard(STATE_DEFUNCT)
	positiveStates.discard(STATE_MODAL)
	positiveStates.discard(STATE_FOCUSED)
	positiveStates.discard(STATE_OFFSCREEN)
	positiveStates.discard(STATE_INVISIBLE)
	if reason != OutputReason.CHANGE:
		positiveStates.discard(STATE_LINKED)
		if role in (
			ROLE_LISTITEM,
			ROLE_TREEVIEWITEM,
			ROLE_MENUITEM,
			ROLE_TABLEROW,
			ROLE_CHECKBOX,
		) and STATE_SELECTABLE in states:
			positiveStates.discard(STATE_SELECTED)
	if role not in (ROLE_EDITABLETEXT, ROLE_CHECKBOX):
		positiveStates.discard(STATE_READONLY)
	if role == ROLE_CHECKBOX:
		positiveStates.discard(STATE_PRESSED)
	if role == ROLE_MENUITEM and STATE_HASPOPUP in positiveStates:
		# The user doesn't usually care if a submenu is expanded or collapsed.
		positiveStates.discard(STATE_COLLAPSED)
		positiveStates.discard(STATE_EXPANDED)
	if STATE_FOCUSABLE not in states:
		positiveStates.discard(STATE_EDITABLE)
	if not config.conf["annotations"]["reportDetails"]:
		# reading aria-details is an experimental feature still and should not always be reported.
		positiveStates.discard(STATE_HAS_ARIA_DETAILS)
	return positiveStates


def processNegativeStates(role, states, reason: OutputReason, negativeStates=None):
	"""Processes the states for an object and returns the negative states to output for a specified reason.
	For example, if C{STATE_CHECKED} is in the returned states, it means that the processed object is not checked.
	@param role: The role of the object to process states for (e.g. C{ROLE_CHECKBOX}.
	@type role: int
	@param states: The raw states for an object to process.
	@type states: set
	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}.
	@param negativeStates: Used for C{OutputReason.CHANGE}, specifies states changed from positive to negative;
	@type negativeStates: set
	@return: The processed negative states.
	@rtype: set
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
		STATE_SELECTABLE in states
		# Only include if the object is focusable (E.g. ARIA grid cells, but not standard html tables)
		and STATE_FOCUSABLE in states
		# Only include  if reporting the focus or when states are changing on the focus.
		# This is to avoid exposing it for things like caret movement in browse mode. 
		and (reason == OutputReason.FOCUS or (reason == OutputReason.CHANGE and STATE_FOCUSED in states))
		and role in (
			ROLE_LISTITEM, 
			ROLE_TREEVIEWITEM, 
			ROLE_TABLEROW,
			ROLE_TABLECELL,
			ROLE_TABLECOLUMNHEADER,
			ROLE_TABLEROWHEADER,
			ROLE_CHECKBOX,
		)
	):
		speakNegatives.add(STATE_SELECTED)
	# Restrict "not checked" in a similar way to "not selected".
	if(
		(role in (ROLE_CHECKBOX, ROLE_RADIOBUTTON, ROLE_CHECKMENUITEM) or STATE_CHECKABLE in states)
		and (STATE_HALFCHECKED not in states)
		and (reason != OutputReason.CHANGE or STATE_FOCUSED in states)
	):
		speakNegatives.add(STATE_CHECKED)
	if role == ROLE_TOGGLEBUTTON:
		speakNegatives.add(STATE_PRESSED)
	if reason == OutputReason.CHANGE:
		# We want to speak this state only if it is changing to negative.
		speakNegatives.add(STATE_DROPTARGET)
		# We were given states which have changed to negative.
		# Return only those supplied negative states which should be spoken;
		# i.e. the states in both sets.
		speakNegatives &= negativeStates
		# #6946: if HALFCHECKED is present but CHECKED isn't, we should make sure we add CHECKED to speakNegatives.
		if (STATE_HALFCHECKED in negativeStates and STATE_CHECKED not in states):
			speakNegatives.add(STATE_CHECKED)
		if STATES_SORTED & negativeStates and not STATES_SORTED & states:
			# If the object has just stopped being sorted, just report not sorted.
			# The user doesn't care how it was sorted before.
			speakNegatives.add(STATE_SORTED)
		return speakNegatives
	else:
		# This is not a state change; only positive states were supplied.
		# Return all negative states which should be spoken, excluding the positive states.
		return speakNegatives - states


def processAndLabelStates(
		role: int,
		states: Set[Any],
		reason: OutputReason,
		positiveStates: Optional[Set[Any]] = None,
		negativeStates: Optional[Set[Any]] = None,
		positiveStateLabelDict: Dict[int, str] = {},
		negativeStateLabelDict: Dict[int, str] = {},
) -> List[str]:
	"""Processes the states for an object and returns the appropriate state labels for both positive and negative states.
	@param role: The role of the object to process states for (e.g. C{ROLE_CHECKBOX}.
	@param states: The raw states for an object to process.
	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}.
	@param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to positive;
	@param negativeStates: Used for C{OutputReason.CHANGE}, specifies states changed from positive to negative;
	@param positiveStateLabelDict: Dictionary containing state identifiers as keys and associated positive labels as their values.
	@param negativeStateLabelDict: Dictionary containing state identifiers as keys and associated negative labels as their values.
	@return: The labels of the relevant positive and negative states.
	"""
	mergedStateLabels=[]
	positiveStates = processPositiveStates(role, states, reason, positiveStates)
	negativeStates = processNegativeStates(role, states, reason, negativeStates)
	for state in sorted(positiveStates | negativeStates):
		if state in positiveStates:
			mergedStateLabels.append(positiveStateLabelDict.get(state, stateLabels[state]))
		elif state in negativeStates:
			# Translators: Indicates that a particular state of an object is negated.
			# Separate strings have now been defined for commonly negated states (e.g. not selected and not checked),
			# but this still might be used in some other cases.
			# %s will be replaced with the full identifier of the negated state (e.g. selected).
			mergedStateLabels.append(negativeStateLabelDict.get(state, negativeStateLabels.get(state, _("not %s") % stateLabels[state])))
	return mergedStateLabels
