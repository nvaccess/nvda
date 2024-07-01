# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Burman's Computer and Education Ltd.

"""Gesture handling for Tivomatic Caiku Albatross 46 and 80 display driver."""

from logHandler import log
from typing import (
	Optional,
	Set,
	Tuple,
)

import braille
import inputCore

from .constants import (
	Keys,
	ROUTING_KEY_RANGES,
)
_gestureMap = inputCore.GlobalGestureMap({
	"globalCommands.GlobalCommands": {
		"review_top": ("br(albatross):home1", "br(albatross):home2",),
		"review_bottom": ("br(albatross):end1", "br(albatross):end2",),
		"navigatorObject_toFocus": ("br(albatross):eCursor1", "br(albatross):eCursor2",),
		"braille_toFocus": ("br(albatross):cursor1", "br(albatross):cursor2",),
		"moveMouseToNavigatorObject": ("br(albatross):home1+home2",),
		"moveNavigatorObjectToMouse": ("br(albatross):end1+end2",),
		"navigatorObject_moveFocus": ("br(albatross):eCursor1+eCursor2",),
		"braille_toggleTether": ("br(albatross):cursor1+cursor2",),
		"braille_previousLine": ("br(albatross):up1", "br(albatross):up2", "br(albatross):up3",),
		"braille_nextLine": ("br(albatross):down1", "br(albatross):down2", "br(albatross):down3",),
		"braille_scrollBack": (
			"br(albatross):left",
			"br(albatross):lWheelLeft",
			"br(albatross):rWheelLeft",
		),
		"braille_scrollForward": (
			"br(albatross):right",
			"br(albatross):lWheelRight",
			"br(albatross):rWheelRight",
		),
		"braille_routeTo": ("br(albatross):routing",),
		"braille_reportFormatting": ("br(albatross):secondRouting",),
		"braille_toggleFocusContextPresentation": ("br(albatross):attribute1+attribute3",),
		"speechMode": ("br(albatross):attribute2+attribute4",),
		"reviewMode_previous": ("br(albatross):f1",),
		"reviewMode_next": ("br(albatross):f2",),
		"navigatorObject_parent": ("br(albatross):f3",),
		"navigatorObject_firstChild": ("br(albatross):f4",),
		"navigatorObject_previous": ("br(albatross):f5",),
		"navigatorObject_next": ("br(albatross):f6",),
		"navigatorObject_current": ("br(albatross):f7",),
		"navigatorObject_currentDimensions": ("br(albatross):f8",),
		"activateBrailleSettingsDialog": ("br(albatross):f1+home1", "br(albatross):f9+home2",),
		"reviewCursorToStatusLine": ("br(albatross):f1+end1", "br(albatross):f9+end2",),
		"braille_cycleCursorShape": ("br(albatross):f1+eCursor1", "br(albatross):f9+eCursor2",),
		"braille_toggleShowCursor": ("br(albatross):f1+cursor1", "br(albatross):f9+cursor2",),
		"braille_cycleShowMessages": ("br(albatross):f1+f2", "br(albatross):f9+f10",),
		"braille_cycleShowSelection": ("br(albatross):f1+f5", "br(albatross):f9+f14",),
		"braille_cycleReviewRoutingMovesSystemCaret": ("br(albatross):f1+f3", "br(albatross):f9+f11",),
		"review_activate": ("br(albatross):f7+f8",),
		"dateTime": ("br(albatross):f9",),
		"say_battery_status": ("br(albatross):f10",),
		"title": ("br(albatross):f11",),
		"reportStatusLine": ("br(albatross):f12",),
		"reportCurrentLine": ("br(albatross):f13",),
		"sayAll": ("br(albatross):f14",),
		"review_currentCharacter": ("br(albatross):f15",),
		"review_currentLine": ("br(albatross):f16",),
		"review_currentWord": ("br(albatross):f15+f16",),
		"review_previousLine": ("br(albatross):lWheelUp", "br(albatross):rWheelUp",),
		"review_nextLine": ("br(albatross):lWheelDown", "br(albatross):rWheelDown",),
		"kb:windows+d": ("br(albatross):attribute1"),
		"kb:windows+e": ("br(albatross):attribute2"),
		"kb:windows+b": ("br(albatross):attribute3"),
		"kb:windows+i": ("br(albatross):attribute4"),
	},
})


class InputGestureKeys(braille.BrailleDisplayGesture):
	"""Changes display key presses to gestures for NVDA input system."""

	def __init__(self, keys: Set[int], name: str):
		"""Constructor.
		@param key: set of pressed keys
		@param name: identifies gestures from this display
		"""
		super().__init__()
		self.source = name
		self.keyCodes = set(keys)
		names = []
		for key in self.keyCodes:
			routingTuple = self._getRoutingIndex(key)
			if routingTuple:
				names.append(routingTuple[0])
				self.routingIndex = routingTuple[1]
			else:
				try:
					names.append(Keys(key).name)
				except (KeyError, ValueError):
					log.debug(f"Unknown key with id {key}")
		self.id = "+".join(names)
		# Try to fix the first valid key press was not recognized as a gesture
		if self.id and not self.script:
			self.script = self._get_script()

	def _getRoutingIndex(self, key: int) -> Optional[Tuple[str, int]]:
		"""Get the routing index, if the key is in a routing index range,
		returns the name of the range and the index within that range.
		See L{ROUTING_KEY_RANGES}.
		@param key: key which index to check
		@return: if the key is in a routing index range, returns the name of the
		range and the index within that range
		"""
		for routingKeyRange in ROUTING_KEY_RANGES:
			if routingKeyRange.start <= key <= routingKeyRange.end:
				return routingKeyRange.name, key - routingKeyRange.indexOffset
		return None
