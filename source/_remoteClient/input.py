# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes
from enum import IntEnum

import api
import baseObject
import braille
import brailleInput
import globalPluginHandler
import scriptHandler
import vision
from winBindings import user32


class VKMapType(IntEnum):
	"""Type of mapping to be performed between virtual key code and virtual scan code.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw
	"""

	VK_TO_VSC = 0
	"""Maps a virtual key code to a scan code."""


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
	input = user32.INPUT()
	input.ii.ki.wVk = vk
	if scan:
		input.ii.ki.wScan = scan
	else:  # No scancode provided, try to get one
		input.ii.ki.wScan = user32.MapVirtualKey(vk, VKMapType.VK_TO_VSC)
	if not pressed:
		input.ii.ki.dwFlags |= user32.KEYEVENTF.KEYUP
	if extended:
		input.ii.ki.dwFlags |= user32.KEYEVENTF.EXTENDEDKEY
	input.type = user32.INPUT_TYPE.KEYBOARD
	user32.SendInput(1, ctypes.byref(input), ctypes.sizeof(user32.INPUT))
