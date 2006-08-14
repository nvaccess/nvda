# NVDA app module for Microsoft Word

import win32com.client
import api
from audio import speakText, speakMessage, speakSymbol
import globalVars
from default import *
from keyEventHandler import sendKey

### Constants
classEdit = "_WwG"
wdWord                        =0x2        # from enum WdUnits
wdLine                        =0x5        # from enum WdUnits

### Globals
word = None

def event_moduleStart():
	global word
	word = win32com.client.Dispatch("Word.Application")
	default["event_moduleStart"]()

def script_speakCharacter(key):
	sendKey(key)
	if getWindowClass(globalVars.focus_locator[0]) == classEdit:
		try:
			speakSymbol(word.ActiveWindow.ActivePane.Selection.Text[0])
		except Exception, e:
			pass

def script_speakLine(key):
	sendKey(key)
	if getWindowClass(globalVars.focus_locator[0]) == classEdit:
		try:
			sel = word.ActiveWindow.ActivePane.Selection
			# Ok, this is evil, but we have no other way of getting the current line!
			# Save the selection range, then expand the selection to the current line.
			sr = sel.Range
			sel.Expand(wdLine)
			text = sel.Text
			sel.SetRange(sr.Start, sr.End)
			speakText(text)
		except Exception, e:
			pass

def script_backspace(key):
	if getWindowClass(globalVars.focus_locator[0]) == classEdit:
		try:
			sel = word.ActiveWindow.ActivePane.Selection
			r = sel.Range
			r.SetRange(r.Start - 1, r.Start)
			bsText = r.Text
			bsStart = sel.Start
			sendKey(key)
			if sel.Start < bsStart:
				speakSymbol(bsText)
		except:
			pass

def script_speakWord(key):
	sendKey(key)
	if getWindowClass(globalVars.focus_locator[0]) == classEdit:
		try:
			sr = word.ActiveWindow.ActivePane.Selection.Range
			sr.Expand(wdWord)
			speakText(sr.Text)
		except:
			pass

keyMap.update({
(None, "ExtendedRight"): script_speakCharacter,
(None, "ExtendedLeft"): script_speakCharacter,
(None, "ExtendedUp"): script_speakLine,
(None, "ExtendedDown"): script_speakLine,
(None, "Back"): script_backspace,
(frozenset(["Control"]), "ExtendedLeft"): script_speakWord,
(frozenset(["Control"]), "ExtendedRight"): script_speakWord,
})
