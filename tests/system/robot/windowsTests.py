# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for testing NVDA interacting with the Windows system.
"""
# relative import not used for 'systemTestUtils' because the folder is added to the path for 'libraries'
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)

# Imported for type information
import NvdaLib as _nvdaLib
from NotepadLib import NotepadLib as _NotepadLib


_notepad: _NotepadLib = _getLib("NotepadLib")


def open_clipboard_history() -> str:
	"""
	Returns the last read item after opening the clipboard history.
	"""
	return _notepad.getSpeechAfterKey("leftWindows+.")


def copy_text():
	"""
	Expects an editable field to be focused.
	"""
	spy = _nvdaLib.getSpyLib()
	spy.emulateKeyPress("control+a")
	spy.emulateKeyPress("control+x")


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
	lastSpeech = _notepad.getSpeechAfterKey("leftWindows+.")
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
