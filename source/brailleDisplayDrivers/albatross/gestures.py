# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, Burman's Computer and Education Ltd.

"""Gesture handling for Tivomatic Caiku Albatross 46 and 80 display driver."""

from logHandler import log
from typing import (
	Optional,
	Set,
	Tuple
)

import braille
import inputCore

from .constants import Key

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
		"braille_scrollBack": ("br(albatross):left", "br(albatross):lWheelLeft", "br(albatross):rWheelLeft",),
		"braille_scrollForward": (
			"br(albatross):right", "br(albatross):lWheelRight", "br(albatross):rWheelRight",),
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

	def __init__(self, keys: Set[int], name: str):
		super().__init__()
		self.source = name
		# Dictionary keys contain routing and second routing value ranges,
		# and values subtraction required to get actual routing index
		# and corresponding routing name.
		self._routingRanges = {  # range values are inclusive
			(2, 41): (2, "routing"),
			(43, 82): (43, "secondRouting"),
			(111, 150): (71, "routing"),
			(152, 191): (112, "secondRouting"),
		}
		self.keyCodes = set(keys)
		names = []
		for key in self.keyCodes:
			routingTuple = self._getRoutingIndex(key)
			if routingTuple:
				names.append(routingTuple[0])
				self.routingIndex = routingTuple[1]
			else:
				try:
					names.append(Key(key).name)
					log.debug(f"Key is {key} and key name is {Key(key).name}")
				except (KeyError, ValueError):
					log.debug(f"Unknown key with id {key}")
		self.id = "+".join(names)

	def _getRoutingIndex(self, key: int) -> Optional[Tuple[str, int]]:
		""" Get the routing index, if the key is in a routing index range, returns the name of the range and the
		index within that range.
		See _routingRanges
		"""
		for rangeStart, rangeEnd in self._routingRanges:
			value = self._routingRanges[(rangeStart, rangeEnd)]
			indexOffset = value[0]
			routingName = value[1]
			if rangeStart <= key <= rangeEnd:
				return routingName, key - indexOffset
		return None
