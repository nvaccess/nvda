#keyboardHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>, Peter Vágner <peter.v@datagate.sk>, Aleksey Sadovoy <lex@onm.su>

"""Keyboard support"""

import winUser
import time
import vkCodes
import speech
import ui
from keyUtils import localizedKeyLabels
from logHandler import log
import queueHandler
import config
import api
import winInputHook
import watchdog
import inputCore

# Fake vk codes.
VK_WIN = "win"

#: Keys which should not be passed to the OS on key up.
keyUpIgnoreSet=set()
#: Tracks the number of keys passed through by request of the user.
#: If -1, pass through is disabled.
#: If 0 or higher then key downs and key ups will be passed straight through.
passKeyThroughCount=-1
#: The last key passed through by request of the user.
lastPassThroughKeyDown=None
#: The current NVDA modifier key being pressed.
currentNVDAModifierKey=None
#: Whether another key has been pressed since the NVDA modifier key was pressed.
usedNVDAModifierKey=False
#: The last NVDA modifier key that was released.
lastNVDAModifierKey=None
#: When the last NVDA modifier key was released.
lastNVDAModifierKeyTime=None
#: The modifiers currently being pressed.
currentModifiers=set()

def passNextKeyThrough():
	global passKeyThroughCount, lastPassThroughKeyDown
	if passKeyThroughCount==-1:
		passKeyThroughCount=0
		lastPassThroughKeyDown=None

def isNVDAModifierKey(vkCode,extended):
	if config.conf["keyboard"]["useNumpadInsertAsNVDAModifierKey"] and vkCode==winUser.VK_INSERT and not extended:
		return True
	elif config.conf["keyboard"]["useExtendedInsertAsNVDAModifierKey"] and vkCode==winUser.VK_INSERT and extended:
		return True
	elif config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"] and vkCode==winUser.VK_CAPITAL:
		return True
	else:
		return False

def internal_keyDownEvent(vkCode,scanCode,extended,injected):
	"""Event called by winInputHook when it receives a keyDown.
	"""
	try:
		global currentNVDAModifierKey, usedNVDAModifierKey, lastNVDAModifierKey, lastNVDAModifierKeyTime, passKeyThroughCount, lastPassThroughKeyDown, currentModifiers
		#Injected keys should be ignored
		if injected:
			return True
		# IF we're passing keys through, increment the pass key through count,
		# but only if this isn't a repeat of the previous key down, as we don't receive key ups for repeated key downs.
		if passKeyThroughCount>=0 and lastPassThroughKeyDown!=(vkCode,extended):
			passKeyThroughCount+=1
			lastPassThroughKeyDown=(vkCode,extended)
			return True
		if watchdog.isAttemptingRecovery:
			# The core is dead, so let keys pass through unhindered.
			return True

		gesture = KeyboardInputGesture(currentModifiers, vkCode, scanCode, extended)
		if (vkCode, extended) == lastNVDAModifierKey:
			lastNVDAModifierKey = None
			if time.time() - lastNVDAModifierKeyTime < 0.5:
				# The user wants the key to serve its normal function instead of acting as an NVDA modifier key.
				gesture.isNVDAModifierKey = False
		if gesture.isNVDAModifierKey:
			currentNVDAModifierKey = (vkCode, extended)
		elif currentNVDAModifierKey:
			# A key was pressed after the NVDA modifier key, so consider it used.
			usedNVDAModifierKey = True
		if gesture.isModifier:
			currentModifiers.add((vkCode, extended))

		try:
			inputCore.manager.executeGesture(gesture)
			keyUpIgnoreSet.add((vkCode,extended))
			return False
		except inputCore.NoInputGestureAction:
			if gesture.isNVDAModifierKey:
				# Never pass the NVDA modifier key to the OS.
				keyUpIgnoreSet.add((vkCode,extended))
				return False
			return True
	except:
		log.error("internal_keyDownEvent", exc_info=True)
		return True

def internal_keyUpEvent(vkCode,scanCode,extended,injected):
	"""Event called by winInputHook when it receives a keyUp.
	"""
	try:
		global currentNVDAModifierKey, usedNVDAModifierKey, lastNVDAModifierKey, lastNVDAModifierKeyTime, passKeyThroughCount, currentModifiers
		if injected:
			return True
		if passKeyThroughCount>=1:
			passKeyThroughCount-=1
			if passKeyThroughCount==0:
				passKeyThroughCount=-1
			return True
		if watchdog.isAttemptingRecovery:
			# The core is dead, so let keys pass through unhindered.
			return True

		if currentNVDAModifierKey and (vkCode,extended)==currentNVDAModifierKey:
			# The current NVDA modifier key is being released.
			if not usedNVDAModifierKey:
				# It wasn't used, so the user may want to pass it through.
				lastNVDAModifierKey=currentNVDAModifierKey
				lastNVDAModifierKeyTime=time.time()
			currentNVDAModifierKey=None
			usedNVDAModifierKey=False

		currentModifiers.discard((vkCode, extended))

		if (vkCode,extended) in keyUpIgnoreSet:
			keyUpIgnoreSet.remove((vkCode,extended))
			return False
	except:
		log.error("", exc_info=True)
	return True

#Register internal key press event with  operating system

def initialize():
	"""Initialises keyboard support."""
	winInputHook.initialize()
	winInputHook.setCallbacks(keyDown=internal_keyDownEvent,keyUp=internal_keyUpEvent)

def terminate():
	winInputHook.terminate()

class KeyboardInputGesture(inputCore.InputGesture):
	"""A key pressed on the traditional system keyboard.
	"""

	#: All normal modifier keys, where modifier vk codes are mapped to a more general modifier vk code or C{None} if not applicable.
	#: @type: dict
	NORMAL_MODIFIER_KEYS = {
		winUser.VK_LCONTROL: winUser.VK_CONTROL,
		winUser.VK_RCONTROL: winUser.VK_CONTROL,
		winUser.VK_LSHIFT: winUser.VK_SHIFT,
		winUser.VK_RSHIFT: winUser.VK_SHIFT,
		winUser.VK_LMENU: winUser.VK_MENU,
		winUser.VK_RMENU: winUser.VK_MENU,
		winUser.VK_LWIN: VK_WIN,
		winUser.VK_RWIN: VK_WIN,
	}

	#: All possible toggle key vk codes.
	#: @type: frozenset
	TOGGLE_KEYS = frozenset((winUser.VK_CAPITAL, winUser.VK_NUMLOCK, winUser.VK_SCROLL))

	#: All possible keyboard layouts, where layout names are mapped to localised layout names.
	#: @type: dict
	LAYOUTS = {
		"desktop": _("desktop"),
		"laptop": _("laptop"),
	}
	#: The current keyboard layout.
	#: @type: str
	currentLayout = "desktop"

	@classmethod
	def getVkName(cls, vkCode):
		if isinstance(vkCode, str):
			return vkCode
		return vkCodes.byCode.get(vkCode, "").lower()

	def __init__(self, modifiers, vkCode, scanCode, isExtended):
		self.modifiers = modifiers = set(modifiers)
		if vkCode in (winUser.VK_DIVIDE, winUser.VK_MULTIPLY, winUser.VK_SUBTRACT, winUser.VK_ADD) and winUser.getKeyState(winUser.VK_NUMLOCK) & 1:
			# Some numpad keys have the same vkCode regardless of numlock.
			# For these keys, treat numlock as a modifier.
			modifiers.add((winUser.VK_NUMLOCK, False))
		self.generalizedModifiers = set((self.NORMAL_MODIFIER_KEYS.get(mod) or mod, extended) for mod, extended in modifiers)
		self.vkCode = vkCode
		self.scanCode = scanCode
		self.isExtended = isExtended
		super(KeyboardInputGesture, self).__init__()

	def _get_isNVDAModifierKey(self):
		return isNVDAModifierKey(self.vkCode, self.isExtended)

	def _get_isModifier(self):
		return self.vkCode in self.NORMAL_MODIFIER_KEYS or self.isNVDAModifierKey

	def _get_mainKeyName(self):
		if self.isNVDAModifierKey:
			return "NVDA"

		prefix = "extended" if self.isExtended else ""
		name = self.getVkName(self.vkCode)
		if name and not name.startswith("oem"):
			return prefix + name

		if 32 < self.vkCode < 128:
			return unichr(self.vkCode).lower()
		vkChar = winUser.user32.MapVirtualKeyW(self.vkCode, winUser.MAPVK_VK_TO_CHAR)
		if 32 < vkChar < 128:
			return unichr(vkChar).lower()

		return prefix + winUser.getKeyNameText(self.scanCode, self.isExtended)

	def _get__keyNames(self):
		mainKey = self.mainKeyName

		if self.isModifier:
			return (mainKey,)

		modTexts = set()
		for modVk, modExt in self.generalizedModifiers:
			if isNVDAModifierKey(modVk, modExt):
				modTexts.add("NVDA")
			else:
				modTexts.add(self.getVkName(modVk))

		return tuple(modTexts) + (mainKey,)

	def _get_keyName(self):
		return "+".join(self._keyNames)

	def _get_displayName(self):
		return "+".join(localizedKeyLabels.get(key, key) for key in self._keyNames)

	def _get_mapKeys(self):
		return (
			"kb({layout}):{key}".format(layout=self.currentLayout, key=self.keyName),
			"kb:{key}".format(key=self.keyName)
		)

	def _get_shouldReportAsCommand(self):
		if self.isExtended and winUser.VK_VOLUME_MUTE <= self.vkCode <= winUser.VK_VOLUME_UP:
			# Don't report volume controlling keys.
			return False
		if self.vkCode == winUser.VK_SPACE:
			return False
		# Aside from space, a key name of more than 1 character is a command.
		if len(self.mainKeyName) > 1:
			return True
		# If this key has modifiers other than shift, it is a command; e.g. shift+f is text, but control+f is a command.
		modifiers = self.generalizedModifiers
		if modifiers and modifiers != frozenset((winUser.VK_SHIFT,)):
			return True
		return False

	def _get_speechEffectWhenExecuted(self):
		if self.isExtended and winUser.VK_VOLUME_MUTE <= self.vkCode <= winUser.VK_VOLUME_UP:
			return None
		if self.vkCode in (winUser.VK_SHIFT, winUser.VK_LSHIFT, winUser.VK_RSHIFT):
			return self.SPEECHEFFECT_RESUME if speech.isPaused else self.SPEECHEFFECT_PAUSE
		return self.SPEECHEFFECT_CANCEL

	def reportExtra(self):
		if self.vkCode in self.TOGGLE_KEYS:
			queueHandler.queueFunction(queueHandler.eventQueue, self._reportToggleKey)

	def _reportToggleKey(self):
		toggleState = winUser.getKeyState(self.vkCode) & 1
		key = self.mainKeyName
		ui.message("{key} {state}".format(
			key=localizedKeyLabels.get(key, key),
			state=_("on") if toggleState else _("off")))

	def send(self):
		keys = []
		for vk, ext in self.generalizedModifiers:
			if vk == VK_WIN and (winUser.getKeyState(winUser.VK_LWIN) & 32768 or winUser.getKeyState(winUser.VK_RWIN) & 32768):
				# Already down.
				continue
			elif winUser.getKeyState(vk) & 32768:
				# Already down.
				continue
			keys.append((vk, ext))
		keys.append((self.vkCode, self.isExtended))

		if winUser.getKeyState(self.vkCode) & 32768:
			# This key is already down, so send a key up for it first.
			winUser.keybd_event(self.vkCode, 0, self.isExtended + 2, 0)

		# Send key down events for these keys.
		for vk, ext in keys:
			winUser.keybd_event(vk, 0, ext, 0)
		# Send key up events for the keys in reverse order.
		for vk, ext in reversed(keys):
			winUser.keybd_event(vk, 0, ext + 2, 0)

		if not queueHandler.isPendingItems(queueHandler.eventQueue):
			time.sleep(0.01)
			import wx
			wx.Yield()

	@classmethod
	def fromName(cls, name):
		"""Create an instance given a key name.
		@param name: The key name.
		@type name: str
		@return: A gesture for the specified key.
		@rtype: L{KeyboardInputGesture}
		"""
		keyNames = name.split("+")
		keys = []
		for keyName in keyNames:
			if keyName.startswith("extended"):
				ext = True
				keyName = keyName[8:]
			else:
				ext = False
			if keyName == VK_WIN:
				vk = winUser.VK_LWIN
			elif len(keyName) == 1:
				vk = ord(keyName.upper())
				if vk in vkCodes.byCode:
					# TODO: Find a way to fix this.
					raise LookupError("Don't know how to get vk code for %s" % keyName)
			else:
				vk = vkCodes.byName[keyName.upper()]
			keys.append((vk, ext))

		if not keys:
			raise ValueError

		return cls(keys[:-1], vk, 0, ext)
