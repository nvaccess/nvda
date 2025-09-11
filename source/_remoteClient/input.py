# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes
from ctypes import POINTER, Structure, Union, c_long, c_ulong, wintypes
from enum import IntEnum, IntFlag

import api
import baseObject
import braille
import brailleInput
import globalPluginHandler
import scriptHandler
import vision
from winBindings import user32


class InputType(IntEnum):
	"""Values permissible as the `type` field in an `INPUT` struct.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
	"""

	MOUSE = 0
	"""The event is a mouse event. Use the mi structure of the union."""

	KEYBOARD = 1
	"""The event is a keyboard event. Use the ki structure of the union."""

	HARDWARE = 2
	"""The event is a hardware event. Use the hi structure of the union."""


class VKMapType(IntEnum):
	"""Type of mapping to be performed between virtual key code and virtual scan code.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw
	"""

	VK_TO_VSC = 0
	"""Maps a virtual key code to a scan code."""


class KeyEventFlag(IntFlag):
	"""Specifies various aspects of a keystroke in a KEYBDINPUT struct.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
	"""

	EXTENDED_KEY = 0x0001
	"""If specified, the wScan scan code consists of a sequence of two bytes, where the first byte has a value of 0xE0."""

	KEY_UP = 0x0002
	"""If specified, the key is being released. If not specified, the key is being pressed. """

	SCAN_CODE = 0x0008
	"""If specified, wScan identifies the key and wVk is ignored. """

	UNICODE = 0x0004
	"""If specified, the system synthesizes a VK_PACKET keystroke.

	.. warning::
		Must only be combined with :const:`KEY_UP`.
	"""


class MOUSEINPUT(Structure):
	_fields_ = (
		("dx", c_long),
		("dy", c_long),
		("mouseData", wintypes.DWORD),
		("dwFlags", wintypes.DWORD),
		("time", wintypes.DWORD),
		("dwExtraInfo", POINTER(c_ulong)),
	)


class KEYBDINPUT(Structure):
	_fields_ = (
		("wVk", wintypes.WORD),
		("wScan", wintypes.WORD),
		("dwFlags", wintypes.DWORD),
		("time", wintypes.DWORD),
		("dwExtraInfo", POINTER(c_ulong)),
	)


class HARDWAREINPUT(Structure):
	_fields_ = (
		("uMsg", wintypes.DWORD),
		("wParamL", wintypes.WORD),
		("wParamH", wintypes.WORD),
	)


class INPUTUnion(Union):
	_fields_ = (
		("mi", MOUSEINPUT),
		("ki", KEYBDINPUT),
		("hi", HARDWAREINPUT),
	)


class INPUT(Structure):
	"""Stores information for synthesizing input events.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
	"""

	_fields_ = (
		("type", wintypes.DWORD),
		("union", INPUTUnion),
	)


class BrailleInputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	def __init__(self, **kwargs):
		super().__init__()
		for key, value in kwargs.items():
			setattr(self, key, value)
		self.source = f"remote{self.source.capitalize()}"
		self.scriptPath = getattr(self, "scriptPath", None)
		self.script = self.findScript() if self.scriptPath else None

	def findScript(self) -> scriptHandler._ScriptFunctionT | None:
		"""Find and return a script function based on the script path.

		The script path must be a list containing three elements:
		module name, class name, and script name. Searches through multiple levels
		for the script.

		Search order:
		    * Global plugins
		    * App modules
		    * Vision enhancement providers
		    * Tree interceptors
		    * NVDA objects
		    * Global commands

		Returns:
		    Callable: The script function if found
		    None: If no matching script is found

		Note:
		    If scriptName starts with "kb:", returns a keyboard emulation script
		"""
		if not (isinstance(self.scriptPath, list) and len(self.scriptPath) == 3):
			return None
		module, cls, scriptName = self.scriptPath
		focus = api.getFocusObject()
		if not focus:
			return None
		if scriptName.startswith("kb:"):
			# Emulate a key press.
			return scriptHandler._makeKbEmulateScript(scriptName)

		import globalCommands

		# Global plugin level.
		if cls == "GlobalPlugin":
			for plugin in globalPluginHandler.runningPlugins:
				if module == plugin.__module__:
					func = getattr(plugin, f"script_{scriptName}", None)
					if func:
						return func

		# App module level.
		app = focus.appModule
		if app and cls == "AppModule" and module == app.__module__:
			func = getattr(app, f"script_{scriptName}", None)
			if func:
				return func

		# Vision enhancement provider level
		for provider in vision.handler.getActiveProviderInstances():
			if isinstance(provider, baseObject.ScriptableObject):
				if cls == "VisionEnhancementProvider" and module == provider.__module__:
					func = getattr(app, "script_{scriptName}", None)
					if func:
						return func

		# Tree interceptor level.
		treeInterceptor = focus.treeInterceptor
		if treeInterceptor and treeInterceptor.isReady:
			func = getattr(treeInterceptor, f"script_{scriptName}", None)
			if func:
				return func

		# NVDAObject level.
		func = getattr(focus, f"script_{scriptName}", None)
		if func:
			return func
		for obj in reversed(api.getFocusAncestors()):
			func = getattr(obj, "script_%s" % scriptName, None)
			if func and getattr(func, "canPropagate", False):
				return func

		# Global commands.
		func = getattr(globalCommands.commands, f"script_{scriptName}", None)
		if func:
			return func

		return None


def sendKey(vk: int | None = None, scan: int | None = None, extended: bool = False, pressed: bool = True):
	"""Execute remote keyboard input locally.

	:param vk: Virtual key code, defaults to None
	:param scan: Scan code, defaults to None
	:param extended: Whether this is an extended key, defaults to False
	:param pressed: ``True`` if key pressed; ``False`` if released, defaults to True
	"""
	i = INPUT()
	i.union.ki.wVk = vk
	if scan:
		i.union.ki.wScan = scan
	else:  # No scancode provided, try to get one
		i.union.ki.wScan = user32.MapVirtualKey(vk, VKMapType.VK_TO_VSC)
	if not pressed:
		i.union.ki.dwFlags |= KeyEventFlag.KEY_UP
	if extended:
		i.union.ki.dwFlags |= KeyEventFlag.EXTENDED_KEY
	i.type = InputType.KEYBOARD
	user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))
