# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for testing NVDA interacting with the Windows system.
"""
import re

from robot.libraries.BuiltIn import BuiltIn
# relative import not used for 'systemTestUtils' because the folder is added to the path for 'libraries'
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)
from SystemTestSpy.windows import SetForegroundWindow

# Imported for type information
from robot.libraries.Process import Process as _ProcessLib

from AssertsLib import AssertsLib as _AssertsLib
import NvdaLib as _nvdaLib
from NvdaLib import NvdaLib as _nvdaRobotLib
_nvdaProcessAlias = _nvdaRobotLib.nvdaProcessAlias

builtIn: BuiltIn = BuiltIn()
_process: _ProcessLib = _getLib("Process")
_asserts: _AssertsLib = _getLib("AssertsLib")

run_dialog_title = re.compile("^Run$")


def open_clipboard_history() -> str:
	"""
	Returns the last read item after opening the clipboard history.
	"""
	spy = _nvdaLib.getSpyLib()
	spy.emulateKeyPress("leftWindows+v")
	spy.wait_for_speech_to_finish()
	return spy.get_last_speech()


def write_and_copy_text(text: str):
	"""
	Expects an editable field to be focused.
	"""
	spy = _nvdaLib.getSpyLib()
	spy.emulateKeyPress("control+a")
	spy.emulateKeyPress("backspace")
	for c in text:
		spy.emulateKeyPress(c)
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("control+a")
	spy.emulateKeyPress("control+x")
	spy.reset_all_speech_index()


def read_clipboard_history(*expectedClipboardHistory: str):
	"""
	Expects the clipboard panel to already be open and focused on an editable field.
	"""
	spy = _nvdaLib.getSpyLib()
	spy.wait_for_speech_to_finish()
	for copyText in expectedClipboardHistory:
		spy.wait_for_specific_speech(copyText)
		spy.emulateKeyPress('rightArrow')


def open_emoji_panel() -> str:
	"""
	Returns the first read emoji after opening the emoji panel.
	"""
	spy = _nvdaLib.getSpyLib()
	spy.emulateKeyPress("leftWindows+.")
	spy.wait_for_speech_to_finish()
	lastSpeech = spy.get_last_speech()
	try:
		return lastSpeech.split("  ")[1]
	except IndexError:
		raise AssertionError(f"Emoji not announced. Last speech: '{lastSpeech}'")


def search_emojis(emojiNameSearchStr: str):
	"""
	Types a string search with the emoji panel open.
	Expects the emoji panel to already be open and focused on an editable field.
	"""
	spy = _nvdaLib.getSpyLib()
	for c in emojiNameSearchStr:
		spy.emulateKeyPress(c, blockUntilProcessed=False)
	spy.wait_for_speech_to_finish()


def read_emojis(*expectedEmojiNameList: str):
	"""
	Navigates the emoji panel and confirms the expected emoji list.
	Expects the emoji panel to already be open.
	"""
	spy = _nvdaLib.getSpyLib()
	for emojiName in expectedEmojiNameList:
		spy.wait_for_specific_speech(emojiName)
		spy.emulateKeyPress('rightArrow')


def open_text_field():
	spy = _nvdaLib.getSpyLib()
	spy.emulateKeyPress("leftWindows+r")
	spy.wait_for_speech_to_finish()


def close_text_field():
	spy = _nvdaLib.getSpyLib()
	SetForegroundWindow(run_dialog_title)
	spy.emulateKeyPress("escape")  # escape any focus or close the win search bar
	spy.emulateKeyPress("escape")  # ensure the win search bar is closed
