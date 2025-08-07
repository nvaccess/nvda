# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2023 NV Access Limited, Babbage B.V., Eurobraille, Cyrille Bougot

from typing import TYPE_CHECKING
import braille
import brailleInput
import inputCore
from . import constants

if TYPE_CHECKING:
	from .driver import BrailleDisplayDriver


GestureMapEntries = {
	"globalCommands.GlobalCommands": {
		"braille_routeTo": ("br(eurobraille):routing",),
		"braille_reportFormatting": ("br(eurobraille):doubleRouting",),
		"braille_scrollBack": (
			"br(eurobraille.bnote):joystick1Left",
			"br(eurobraille):switch1Left",
			"br(eurobraille):l1",
		),
		"braille_scrollForward": (
			"br(eurobraille.bnote):joystick1Right",
			"br(eurobraille):switch1Right",
			"br(eurobraille):l8",
		),
		"braille_toFocus": (
			"br(eurobraille):switch1Left+switch1Right",
			"br(eurobraille):switch2Left+switch2Right",
			"br(eurobraille):switch3Left+switch3Right",
			"br(eurobraille):switch4Left+switch4Right",
			"br(eurobraille):switch5Left+switch5Right",
			"br(eurobraille):switch6Left+switch6Right",
			"br(eurobraille):l1+l8",
		),
		"review_previousLine": ("br(eurobraille):joystick1Up",),
		"review_nextLine": ("br(eurobraille):joystick1Down",),
		"review_previousCharacter": ("br(eurobraille):joystick1Left",),
		"review_nextCharacter": ("br(eurobraille):joystick1Right",),
		"reviewMode_previous": ("br(eurobraille):joystick1Left+joystick1Up",),
		"reviewMode_next": ("br(eurobraille):joystick1Right+joystick1Down",),
		# Esys and esytime have a dedicated key for backspace and combines backspace and space to perform a return.
		"braille_eraseLastCell": ("br(eurobraille):backSpace",),
		"braille_enter": ("br(eurobraille):backSpace+space",),
		"kb:insert": (
			"br(eurobraille):dot1+dot3+dot5+space",
			"br(eurobraille):dot3+dot4+dot5+space",
		),
		"kb:delete": ("br(eurobraille):dot3+dot6+space",),
		"kb:home": ("br(eurobraille):dot1+dot2+dot3+space"),
		"kb:end": ("br(eurobraille):dot4+dot5+dot6+space",),
		"kb:leftArrow": (
			"br(eurobraille):dot2+space",
			"br(eurobraille):joystick2Left",
			"br(eurobraille):leftArrow",
		),
		"kb:rightArrow": (
			"br(eurobraille):dot5+space",
			"br(eurobraille):joystick2Right",
			"br(eurobraille):rightArrow",
		),
		"kb:upArrow": (
			"br(eurobraille):dot4+space",
			"br(eurobraille):joystick2Up",
			"br(eurobraille):upArrow",
		),
		"kb:downArrow": (
			"br(eurobraille):dot6+space",
			"br(eurobraille):joystick2Down",
			"br(eurobraille):downArrow",
		),
		"kb:enter": ("br(eurobraille):joystick2Center",),
		"kb:pageUp": ("br(eurobraille):dot1+dot3+space",),
		"kb:pageDown": ("br(eurobraille):dot4+dot6+space",),
		"kb:numpad1": ("br(eurobraille):dot1+dot6+backspace",),
		"kb:numpad2": ("br(eurobraille):dot1+dot2+dot6+backspace",),
		"kb:numpad3": ("br(eurobraille):dot1+dot4+dot6+backspace",),
		"kb:numpad4": ("br(eurobraille):dot1+dot4+dot5+dot6+backspace",),
		"kb:numpad5": ("br(eurobraille):dot1+dot5+dot6+backspace",),
		"kb:numpad6": ("br(eurobraille):dot1+dot2+dot4+dot6+backspace",),
		"kb:numpad7": ("br(eurobraille):dot1+dot2+dot4+dot5+dot6+backspace",),
		"kb:numpad8": ("br(eurobraille):dot1+dot2+dot5+dot6+backspace",),
		"kb:numpad9": ("br(eurobraille):dot2+dot4+dot6+backspace",),
		"kb:numpadInsert": ("br(eurobraille):dot3+dot4+dot5+dot6+backspace",),
		"kb:numpadDecimal": ("br(eurobraille):dot2+backspace",),
		"kb:numpadDivide": ("br(eurobraille):dot3+dot4+backspace",),
		"kb:numpadMultiply": ("br(eurobraille):dot3+dot5+backspace",),
		"kb:numpadMinus": ("br(eurobraille):dot3+dot6+backspace",),
		"kb:numpadPlus": ("br(eurobraille):dot2+dot3+dot5+backspace",),
		"kb:numpadEnter": ("br(eurobraille):dot3+dot4+dot5+backspace",),
		"kb:escape": (
			"br(eurobraille):dot1+dot2+dot4+dot5+space",
			"br(eurobraille):l2",
		),
		"kb:tab": (
			"br(eurobraille):dot2+dot5+dot6+space",
			"br(eurobraille):l3",
		),
		"kb:shift+tab": ("br(eurobraille):dot2+dot3+dot5+space",),
		"kb:printScreen": ("br(eurobraille):dot1+dot3+dot4+dot6+space",),
		"kb:pause": ("br(eurobraille):dot1+dot4+space",),
		"kb:applications": ("br(eurobraille):dot5+dot6+backspace",),
		"kb:f1": ("br(eurobraille):dot1+backspace",),
		"kb:f2": ("br(eurobraille):dot1+dot2+backspace",),
		"kb:f3": ("br(eurobraille):dot1+dot4+backspace",),
		"kb:f4": ("br(eurobraille):dot1+dot4+dot5+backspace",),
		"kb:f5": ("br(eurobraille):dot1+dot5+backspace",),
		"kb:f6": ("br(eurobraille):dot1+dot2+dot4+backspace",),
		"kb:f7": ("br(eurobraille):dot1+dot2+dot4+dot5+backspace",),
		"kb:f8": ("br(eurobraille):dot1+dot2+dot5+backspace",),
		"kb:f9": ("br(eurobraille):dot2+dot4+backspace",),
		"kb:f10": ("br(eurobraille):dot2+dot4+dot5+backspace",),
		"kb:f11": ("br(eurobraille):dot1+dot3+backspace",),
		"kb:f12": ("br(eurobraille):dot1+dot2+dot3+backspace",),
		"kb:windows": ("br(eurobraille):dot1+dot2+dot4+dot5+dot6+space",),
		"kb:capsLock": ("br(eurobraille):dot7+backspace", "br(eurobraille):dot8+backspace"),
		"kb:numLock": ("br(eurobraille):dot3+backspace", "br(eurobraille):dot6+backspace"),
		"braille_toggleShift": (
			"br(eurobraille):dot1+dot7+space",
			"br(eurobraille):dot4+dot7+space",
			"br(eurobraille):l4",
		),
		"kb:shift": ("br(eurobraille):dot7+space",),
		"braille_toggleControl": (
			"br(eurobraille):dot1+dot7+dot8+space",
			"br(eurobraille):dot4+dot7+dot8+space",
			"br(eurobraille):l5",
		),
		"kb:control": ("br(eurobraille):dot7+dot8+space",),
		"braille_toggleAlt": (
			"br(eurobraille):dot1+dot8+space",
			"br(eurobraille):dot4+dot8+space",
			"br(eurobraille):l6",
		),
		"kb:alt": ("br(eurobraille):dot8+space"),
		"braille_toggleNVDAKey": ("br(eurobraille):l7", "br(eurobraille):dot3+dot5+space"),
		"kb:control+home": (
			"br(eurobraille):joystick2left+joystick2up",
			"br(eurobraille):l1+l2+l3",
			"br(eurobraille):l2+l3+l4",
		),
		"kb:control+end": (
			"br(eurobraille):joystick2right+joystick2up",
			"br(eurobraille):l6+l7+l8",
			"br(eurobraille):l5+l6+l7",
		),
		"braille_toggleWindows": (
			"br(eurobraille):backspace+dot1+dot2+dot3+dot4",
			"br(eurobraille):dot2+dot4+dot5+dot6+space",
		),
		"kb:control+shift+e": ("br(eurobraille):dot1+dot5+space",),
	},
}
_gestureMap = inputCore.GlobalGestureMap(GestureMapEntries)


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = constants.name

	def __init__(self, display: "BrailleDisplayDriver"):
		super().__init__()
		self.model = display.deviceType.lower().split(" ")[0]
		keysDown = dict(display.keysDown)

		self.keyNames = names = []
		for group, groupKeysDown in keysDown.items():
			if group == constants.EB_KEY_BRAILLE:
				if sum(keysDown.values()) == groupKeysDown and not groupKeysDown & 0x100:
					# This is braille input.
					# 0x1000 is backspace, 0x2000 is space
					self.dots = groupKeysDown & 0xFF
					self.space = groupKeysDown & 0x200
				names.extend(f"dot{i + 1}" for i in range(8) if (groupKeysDown & 0xFF) & (1 << i))
				if groupKeysDown & 0x200:
					names.append("space")
				if groupKeysDown & 0x100:
					names.append("backSpace")
			if group == constants.EB_KEY_INTERACTIVE:  # Routing
				self.routingIndex = (groupKeysDown & 0xFF) - 1
				if groupKeysDown >> 8 == ord(constants.EB_KEY_INTERACTIVE_DOUBLE_CLICK):
					names.append("doubleRouting")
				else:
					names.append("routing")
			if group == constants.EB_KEY_COMMAND:
				for key, keyName in display.keys.items():
					if groupKeysDown & key:
						# This key is pressed
						names.append(keyName)

		self.id = "+".join(names)
