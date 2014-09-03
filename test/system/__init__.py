#test/system/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 NV Access Limited

"""NVDA system testing.
All system tests should reside within this package and should be grouped into sub-packages.
Test modules must have a C{test_} prefix
and should contain one or more classes which subclass L{TestCase}.
"""

import sys
import os
import time
import socket
import threading
import ctypes.wintypes
import unittest
import subprocess

# Allow import of NVDA modules.
nvdaSourcePath = os.path.abspath(os.path.join(__file__, "..", "..", "..", "source"))
sys.path.append(nvdaSourcePath)
import winKernel
import vkCodes
import winUser
import shellapi

pythonw = os.path.join(sys.prefix, "pythonw.exe")
nvdaPyw = os.path.join(nvdaSourcePath, "nvda.pyw")
nvdaConfig = os.path.abspath(os.path.join(__file__, "..", "nvdaConfig"))

FD_READ = 0x01

class TestCase(unittest.TestCase):
	"""Base class for system test cases.
	All system tests should be contained within a subclass of this class.
	Test methods should be named with a C{test_} prefix.
	A new NVDA session will be used for each class.
	"""

	@classmethod
	def setUpClass(cls):
		cls._startNvda()
		cls._nvdaSock = sock = socket.socket()
		sock.connect(("127.0.0.1", 6838))
		cls._nvdaR = sock.makefile("r")
		cls._nvdaW = sock.makefile("w")
		cls._nvdaEvent = ctypes.windll.kernel32.CreateEventW(None, False, False, None)
		cls._isTearingDown = False
		cls._nvdaPres = []
		cls._nvdaWatchThread = threading.Thread(target=cls._nvdaWatcher)
		cls._nvdaWatchThread.start()

	@classmethod
	def _nvdaWatcher(cls):
		# Swallow the welcome and initial prompt.
		cls._nvdaR.readline()
		cls._nvdaR.read(4)
		while True:
			ctypes.windll.ws2_32.WSAEventSelect(cls._nvdaSock.fileno(), cls._nvdaEvent, FD_READ)
			winKernel.waitForSingleObject(cls._nvdaEvent, winKernel.INFINITE)
			if cls._isTearingDown:
				return
			cls._nvdaSock.setblocking(True)
			line = cls._nvdaR.readline()
			if line.startswith("PRES "):
				line = line.rstrip("\r\n")
				command, message = line.split(" ", 1)
				if message[0] == "u":
					message = message[2:-1].decode("unicode_escape")
				else:
					message = message[1:-1].decode("string_escape")
				cls._nvdaPres.append(message)

	@classmethod
	def expectPresentation(cls, expected):
		"""Assert that NVDA speech and braille output is as expected.
		Captured output will be cleared regardless of success.
		@param expected: A list of speech and braille log messages.
			The best way to get these is from the NVDA log itself.
		@type expected: list of str
		"""
		# Wait for test actions to generate output.
		time.sleep(0.5)
		actual = cls._nvdaPres
		cls._nvdaPres = []
		assert actual == expected, "Actual output: %r" % actual

	@classmethod
	def resetPresentation(cls):
		"""Clear captured presentation output.
		This is useful if you don't care about the output of an action;
		e.g. if that action is purely to set up for a test.
		"""
		time.sleep(0.5)
		cls._nvdaPres = []

	@classmethod
	def tearDownClass(cls):
		cls._isTearingDown = True
		ctypes.windll.kernel32.SetEvent(cls._nvdaEvent)
		cls._nvdaWatchThread.join()
		winKernel.closeHandle(cls._nvdaEvent)
		cls._nvdaW.write("exit()\r\n")
		cls._nvdaW.flush()
		cls._nvdaSock.close()
		cls._quitNvda()

	ctypes.windll.user32.VkKeyScanW.restype = ctypes.wintypes.SHORT
	FAKE_KEYS = {
		"windows": winUser.VK_LWIN,
		"nvda": winUser.VK_INSERT,
	}
	@classmethod
	def keyCommand(cls, keys):
		"""Send a keyboard command.
		@param keys: The keys to send; e.g. C{"NVDA+f12"}.
		@type keys: basestring
		"""
		keys = keys.lower().split("+")
		mainKey = keys.pop()
		if len(mainKey) == 1:
			# Modifiers aren't handled here.
			mainVk = ctypes.windll.user32.VkKeyScanW(ctypes.wintypes.WCHAR(mainKey)) & 0xFF
			mainExt = False
		else:
			mainVk, mainExt = vkCodes.byName[keys.pop()]
		modifiers = {cls.FAKE_KEYS.get(key) or vkCodes.byName[key][0]
			for key in keys}

		isWinDown = winUser.getAsyncKeyState(winUser.VK_LWIN) & 32768 or winUser.getAsyncKeyState(winUser.VK_RWIN) & 32768
		neededModifiers = []
		# Record any currently held modifier keys that must be released while sending this key press
		for mod in (winUser.VK_SHIFT, winUser.VK_CONTROL, winUser.VK_MENU, winUser.VK_LWIN):
			if mod in modifiers:
				continue
			if mod == winUser.VK_LWIN:
				if not isWinDown:
					continue
			elif not winUser.getAsyncKeyState(mod) & 32768: 
				continue
			neededModifiers.append((mod, False))
		# Record any modifiers that must be included for this key press that arn't already held down. 
		for mod in modifiers:
			if mod == winUser.VK_LWIN:
				if isWinDown:
					continue
			elif winUser.getAsyncKeyState(mod) & 32768:
				continue
			neededModifiers.append((mod, True))
		# Find out if the main key for the key press is already pressed or not
		mainKeyWasDown = winUser.getAsyncKeyState(mainVk) & 32768
		# Prepair the input sequence for sending
		inputs = []
		# Press any modifiers needed but not yet down, and release any modifiers down but not needed
		for mod, press in neededModifiers:
			input = winUser.Input(type=winUser.INPUT_KEYBOARD)
			input.ii.ki.wVk = mod
			if not press:
				input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
			inputs.append(input)
		# Release the main key if its already down so it can be pressed again
		if mainKeyWasDown:
			input = winUser.Input(type=winUser.INPUT_KEYBOARD)
			input.ii.ki.wVk = mainVk
			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
			if mainExt:
				input.ii.ki.dwFlags += winUser.KEYEVENTF_EXTENDEDKEY
			inputs.append(input)
		# Press the main key
		input = winUser.Input(type=winUser.INPUT_KEYBOARD)
		input.ii.ki.wVk = mainVk
		if mainExt:
			input.ii.ki.dwFlags += winUser.KEYEVENTF_EXTENDEDKEY
		inputs.append(input)
		# Release the main key
		if not mainKeyWasDown:
			input = winUser.Input(type=winUser.INPUT_KEYBOARD)
			input.ii.ki.wVk = mainVk
			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
			if mainExt:
				input.ii.ki.dwFlags += winUser.KEYEVENTF_EXTENDEDKEY
			inputs.append(input)
		# Release any needed modifiers that were needed but not originally down, and press any unneeded modifiers that were originally down
		for mod, press in neededModifiers:
			input = winUser.Input(type=winUser.INPUT_KEYBOARD)
			input.ii.ki.wVk = mod
			if press:
				input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
			inputs.append(input)
		# Send the input to the Operating System
		winUser.SendInput(inputs)

	@classmethod
	def typeText(cls, text):
		"""Send text as if it were typed on the keyboard.
		@param text: The text to send.
		@type text: basestring
		"""
		inputs = []
		for ch in text:
			input = winUser.Input()
			input.type = winUser.INPUT_KEYBOARD
			input.ii.ki.wScan = ord(ch)
			input.ii.ki.dwFlags = winUser.KEYEVENTF_UNICODE
			inputs.append(input)
			input = winUser.Input()
			input.type = winUser.INPUT_KEYBOARD
			input.ii.ki.wScan = ord(ch)
			input.ii.ki.dwFlags = winUser.KEYEVENTF_UNICODE | winUser.KEYEVENTF_KEYUP
			inputs.append(input)
		winUser.SendInput(inputs)

	@classmethod
	def runApp(cls, app, params=None):
		"""Run an application.
		This will return once the application is ready.
		@param app: The application to run.
		@type app: basestring
		@param params: Command line parameters.
		@type params: list of basestring
		"""
		if params is not None:
			params = unicode(subprocess.list2cmdline(params))
		sei = shellapi.SHELLEXECUTEINFO(lpFile=unicode(app),
			lpParameters=params,
			nShow=winUser.SW_SHOWNORMAL,
			fMask=shellapi.SEE_MASK_NOCLOSEPROCESS)
		shellapi.ShellExecuteEx(sei)
		try:
			if ctypes.windll.user32.WaitForInputIdle(sei.hProcess, 20000) != 0:
				raise ctypes.WinError()
		finally:
			winKernel.closeHandle(sei.hProcess)
		time.sleep(0.1)

	@classmethod
	def _startNvda(cls):
		cls.runApp(pythonw, params=(nvdaPyw, "-mrc", nvdaConfig))

	@classmethod
	def _quitNvda(cls):
		cls.runApp(pythonw, params=(nvdaPyw, "-q"))
