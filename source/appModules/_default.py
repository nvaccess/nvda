#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gc
import comtypesClient
import datetime
from keyUtils import key
import IAccessibleHandler
import api
import debug
import speech
import sayAllHandler
import virtualBuffers
import NVDAObjects
import globalVars
from synthDriverHandler import *
import gui
import core
import config
import winUser
import appModuleHandler
import winKernel

class appModule(appModuleHandler.appModule):

	def event_switchStart(self,obj,nextHandler):
		speech.cancelSpeech()

	def event_switchEnd(self,obj,nextHandler):
		speech.cancelSpeech()

	def script_keyboardHelp(self,keyPress,nextScript):
		if not globalVars.keyboardHelp:
 			state=_("on")
			globalVars.keyboardHelp=True
		else:
			state=_("off")
			globalVars.keyboardHelp=False
		speech.speakMessage(_("keyboard help %s")%state)
	script_keyboardHelp.__doc__=_("Turns keyboard help on and off. When on, pressing a key on the keyboard will tell you what script is associated with it, if any.")

	def script_dateTime(self,keyPress,nextScript):
		text=datetime.datetime.today().strftime("%I:%M %p, %A %B %d %Y")
		if text[0]=='0':
			text=text[1:]
		speech.speakMessage(text)
	script_dateTime.__doc__=_("Reports the current date and time")

	def script_increaseRate(self,keyPress,nextScript):
		rate=getSynth().rate+5
		getSynth().rate=rate
		config.conf["speech"][getSynth().name]["rate"]=rate
		speech.speakMessage(_("rate %d%%")%rate)
	script_increaseRate.__doc__=_("Increases the speech rate by 5 percent")

	def script_decreaseRate(self,keyPress,nextScript):
		rate=getSynth().rate-5
		getSynth().rate=rate
		config.conf["speech"][getSynth().name]["rate"]=rate
		speech.speakMessage(_("rate %d%%")%rate)
	script_decreaseRate.__doc__=_("decreases the speech rate by 5 percent")

	def script_toggleSpeakTypedCharacters(self,keyPress,nextScript):
		if config.conf["keyboard"]["speakTypedCharacters"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedCharacters"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedCharacters"]=True
		speech.speakMessage(_("speak typed characters")+" "+onOff)
	script_toggleSpeakTypedCharacters.__doc__=_("Toggles on and off the speaking of typed characters")

	def script_toggleSpeakTypedWords(self,keyPress,nextScript):
		if config.conf["keyboard"]["speakTypedWords"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedWords"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedWords"]=True
		speech.speakMessage(_("speak typed words")+" "+onOff)
	script_toggleSpeakTypedWords.__doc__=_("Toggles on and off the speaking of typed words")

	def script_toggleSpeakCommandKeys(self,keyPress,nextScript):
		if config.conf["keyboard"]["speakCommandKeys"]:
			onOff=_("off")
			config.conf["keyboard"]["speakCommandKeys"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakCommandKeys"]=True
		speech.speakMessage(_("speak command keys")+" "+onOff)
	script_toggleSpeakCommandKeys.__doc__=_("Toggles on and off the speaking of typed keys, that are not specifically characters")

	def script_toggleSpeakPunctuation(self,keyPress,nextScript):
		if config.conf["speech"]["speakPunctuation"]:
			onOff=_("off")
			config.conf["speech"]["speakPunctuation"]=False
		else:
			onOff=_("on")
			config.conf["speech"]["speakPunctuation"]=True
		speech.speakMessage(_("speak punctuation")+" "+onOff)
	script_toggleSpeakPunctuation.__doc__=_("Toggles on and off the speaking of punctuation. When on NVDA will say the names of punctuation symbols, when off it will be up to the synthesizer as to how it speaks punctuation")

	def script_moveMouseToNavigatorObject(self,keyPress,nextScript):
		speech.speakMessage("Move mouse to navigator")
		api.moveMouseToNVDAObject(api.getNavigatorObject())
	script_moveMouseToNavigatorObject.__doc__=_("Moves the mouse pointer to the current navigator object.")

	def script_moveNavigatorObjectToMouse(self,keyPress,nextScript):
		speech.speakMessage("Move navigator object to mouse")
		(x,y)=winUser.getCursorPos()
		obj=NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y)
		if obj:
			api.setNavigatorObject(obj)
			obj.speakObject()
	script_moveNavigatorObjectToMouse.__doc__=_("Sets the navigator object to the object that is directly under the mouse pointer")

	def script_navigatorObject_current(self,keyPress,nextScript):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject.speakObject()
		return False
	script_navigatorObject_current.__doc__=_("Reports the current navigator object")

	def script_navigatorObject_currentDimensions(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if not obj:
			speech.speakMessage(_("no navigator object"))
		location=obj.location
		if not location:
			speech.speakMessage(_("No location information for navigator object"))
		(left,top,width,height)=location
		speech.speakMessage(_("%d wide by %d high, located %d from left and %d from top")%(width,height,left,top))
	script_navigatorObject_currentDimensions.__doc__=_("Reports the hight, width and position of the current navigator object")

	def script_navigatorObject_toFocus(self,keyPress,nextScript):
		obj=api.getFocusObject()
		if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no focus"))
		api.setNavigatorObject(obj)
		speech.speakMessage(_("move to focus"))
		obj.speakObject()
	script_navigatorObject_toFocus.__doc__=_("Sets the navigator object to the current focus")

	def script_navigatorObject_parent(self,keyPress,nextScript):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			speech.speakMessage(_("No parents"))
	script_navigatorObject_parent.__doc__=_("Sets the navigator object to the parent of the object it is currently on.")

	def script_navigatorObject_next(self,keyPress,nextScript):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.next
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			speech.speakMessage(_("No next"))
	script_navigatorObject_next.__doc__=_("Sets the navigator object to the next object to the one it is currently on")

	def script_navigatorObject_previous(self,keyPress,nextScript):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.previous
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			speech.speakMessage(_("No previous"))
	script_navigatorObject_previous.__doc__=_("Sets the navigator object to the previous object to the one it is currently on")

	def script_navigatorObject_firstChild(self,keyPress,nextScript):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.firstChild
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			speech.speakMessage(_("No children"))
	script_navigatorObject_firstChild.__doc__=_("Sets the navigator object to the first child object to the one it is currently on")

	def script_navigatorObject_doDefaultAction(self,keyPress,nextScript):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject.doDefaultAction()
	script_navigatorObject_doDefaultAction.__doc__=_("Performs the default action on the current navigator object (example: presses it if it is a button).")

	def script_navigatorObject_where(self,keyPress,nextScript):
		"""Reports where the current navigator object is by reporting each of its ancestors""" 
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		while curObject is not None:
			speech.speakMessage("in")
			curObject.speakObject()
			curObject=curObject.parent
	script_navigatorObject_where.__doc__=_("Reports where the current navigator object is by reporting each of its ancestors")

	def script_review_top(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_top(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_top.__doc__=_("Moves the review cursor to the top line of the current navigator object")

	def script_review_bottom(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_bottom(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_bottom.__doc__=_("Moves the review cursor to the bottom line of the current navigator object")

	def script_review_previousLine(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevLine(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_previousLine.__doc__=_("Moves the review cursor to the previous line of the current navigator object")

	def script_review_currentLine(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentLine(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_currentLine.__doc__=_("Reports the line of the current navigator object where the review cursor is situated")

	def script_review_nextLine(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextLine(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_nextLine.__doc__=_("Moves the review cursor to the next line of the current navigator object")

	def script_review_previousWord(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevWord(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_previousWord.__doc__=_("Moves the review cursor to the previous word of the current navigator object")

	def script_review_currentWord(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentWord(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_currentWord.__doc__=_("Speaks the word of the current navigator object where the review cursor is situated")

	def script_review_nextWord(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextWord(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_nextWord.__doc__=_("Moves the review cursor to the next word of the current navigator object")

	def script_review_previousCharacter(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevCharacter(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_previousCharacter.__doc__=_("Moves the review cursor to the previous character of the current navigator object")

	def script_review_currentCharacter(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentCharacter(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_currentCharacter.__doc__=_("Reports the character of the current navigator object where the review cursor is situated")

	def script_review_nextCharacter(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextCharacter(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_nextCharacter.__doc__=_("Moves the review cursor to the next character of the current navigator object")

	def script_review_startOfLine(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_startOfLine(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_startOfLine.__doc__=_("Moves the review cursor to the start of the line where it is situated, in the current navigator object")

	def script_review_endOfLine(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_endOfLine(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_endOfLine.__doc__=_("Moves the review cursor to the end of the line where it is situated, in the current navigator object")

	def script_review_moveToCaret(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_moveToCaret(keyPress,None)
		else:
			speech.speakMessage(_("no navigator object"))
	script_review_moveToCaret.__doc__=_("Moves the review cursor to the position of the system caret, in the current navigator object")

	def script_speechMode(self,keyPress,nextScript):
		curMode=speech.speechMode
		speech.speechMode=speech.speechMode_talk
		newMode=(curMode+1)%3
		if newMode==speech.speechMode_off:
			name=_("off")
		elif newMode==speech.speechMode_beeps:
			name=_("beeps")
		elif newMode==speech.speechMode_talk:
			name=_("talk")
		speech.speakMessage(_("speech mode %s")%name)
		speech.speechMode=newMode
	script_speechMode.__doc__=_("Toggles between the speech modes of off, beep and talk. When set to off NVDA will not speak anything. If beeps then NVDA will simply beep each time it its supposed to speak something. If talk then NVDA wil just speak normally.")

	def script_toggleVirtualBufferPassThrough(self,keyPress,nextScript):
		api.toggleVirtualBufferPassThrough()
	script_toggleVirtualBufferPassThrough.__doc__=_("Toggles virtualBuffer pass-through mode on and off. When on, keys will pass straight through the current virtualBuffer, allowing you to interact with a control with out the virtualBuffer doing something else with the key.")

	def script_quit(self,keyPress,nextScript):
		gui.quit()
	script_quit.__doc__=_("Quits NVDA!")

	def script_showGui(self,keyPress,nextScript):
		gui.showGui()
	script_showGui.__doc__=_("Shows the NVDA interface window")

	def script_sayAll_review(self,keyPress,nextScript):
		o=api.getNavigatorObject()
		sayAllHandler.sayAll(o.text_reviewOffset,o.text_characterCount,o.text_getNextFieldOffsets,o.text_getText,o.text_reportNewPresentation,o._set_text_reviewOffset)

	def script_sayAll_caret(self,keyPress,nextScript):
		o=api.getFocusObject()
		v=virtualBuffers.getVirtualBuffer(o)
		if v and not api.isVirtualBufferPassThrough():
			sayAllHandler.sayAll(v.text_reviewOffset,v.text_characterCount,v.text_getNextLineOffsets,v.text_getText,v.text_reportNewPresentation,v._set_text_reviewOffset)
		else:
			sayAllHandler.sayAll(o.text_caretOffset,o.text_characterCount,o.text_getNextFieldOffsets,o.text_getText,o.text_reportNewPresentation,o._set_text_caretOffset)

	def script_review_reportPresentation(self,keyPress,nextScript):
		o=api.getFocusObject()
		v=virtualBuffers.getVirtualBuffer(o)
		if v and not api.isVirtualBufferPassThrough():
			o=v
		o.text_reportPresentation(o.text_reviewOffset)

	def script_reportCurrentFocus(self,keyPress,nextScript):
		focusObject=api.getFocusObject()
		if isinstance(focusObject,NVDAObjects.baseType.NVDAObject):
			focusObject.speakObject()
		else:
			speech.speakMessage(_("no focus"))

	def script_reportStatusLine(self,keyPress,nextScript):
		foregroundObject=api.getForegroundObject()
		if not foregroundObject:
			speech.speakMessage(_("no foreground object"))
			return
		statusBarObject=foregroundObject.statusBar
		if not statusBarObject:
			speech.speakMessage(_("no status bar found"))
			return
		statusBarObject.speakObject()
		api.setNavigatorObject(statusBarObject)

	def script_toggleReportObjectUnderMouse(self,keyPress,nextScript):
		if config.conf["mouse"]["reportObjectUnderMouse"]:
			onOff=_("off")
			config.conf["mouse"]["reportObjectUnderMouse"]=False
		else:
			onOff=_("on")
			config.conf["mouse"]["reportObjectUnderMouse"]=True
		speech.speakMessage(_("Report object under mouse")+" "+onOff)
	script_toggleReportObjectUnderMouse.__doc__=_("Toggles on and off the reporting of objects under the mouse")

	def script_title(self,keyPress,nextScript):
		obj=api.getForegroundObject()
		if obj:
			obj.speakObject()
	script_title.__doc__=_("Reports the title of the current application or foreground window")

	def script_speakForeground(self,keyPress,nextScript):
		obj=api.getForegroundObject()
		if obj:
			obj.speakObject()
			obj.speakDescendantObjects()

	def script_test_navigatorWindowInfo(self,keyPress,nextScript):
		obj=api.getNavigatorObject()
		speech.speakMessage("Control ID: %s"%winUser.getControlID(obj.windowHandle))
		speech.speakMessage("Class: %s"%obj.windowClassName)
		for char in obj.windowClassName:
			speech.speakSymbol("%s"%char)
		speech.speakMessage("internal text: %s"%winUser.getWindowText(obj.windowHandle))
		speech.speakMessage("text: %s"%obj.windowText)

	def script_toggleBeepOnProgressBarUpdates(self,keyPress,nextScript):
		if config.conf["presentation"]["beepOnProgressBarUpdates"]:
			onOff=_("off")
			config.conf["presentation"]["beepOnProgressBarUpdates"]=False
		else:
			onOff=_("on")
			config.conf["presentation"]["beepOnProgressBarUpdates"]=True
		speech.speakMessage(_("Beep on progress bar updates")+" "+onOff)
	script_toggleBeepOnProgressBarUpdates.__doc__=_("Toggles on and off the beeping on progress bar updates")

	def script_toggleReportDynamicContentChanges(self,keyPress,nextScript):
		if globalVars.reportDynamicContentChanges:
			onOff=_("off")
			globalVars.reportDynamicContentChanges=False
		else:
			onOff=_("on")
			globalVars.reportDynamicContentChanges=True
		speech.speakMessage(_("report dynamic content changes")+" "+onOff)
	script_toggleReportDynamicContentChanges.__doc__=_("Toggles on and off the reporting of dynamic content changes, such as new text in dos console windows")

	def script_toggleCaretMovesReviewCursor(self,keyPress,nextScript):
		if globalVars.caretMovesReviewCursor:
			onOff=_("off")
			globalVars.caretMovesReviewCursor=False
		else:
			onOff=_("on")
			globalVars.caretMovesReviewCursor=True
		speech.speakMessage(_("caret moves review cursor")+" "+onOff)
	script_toggleCaretMovesReviewCursor.__doc__=_("Toggles on and off the movement of the review cursor due to the caret moving.")

	def script_toggleFocusMovesNavigatorObject(self,keyPress,nextScript):
		if globalVars.focusMovesNavigatorObject:
			onOff=_("off")
			globalVars.focusMovesNavigatorObject=False
		else:
			onOff=_("on")
			globalVars.focusMovesNavigatorObject=True
		speech.speakMessage(_("focus moves navigator object")+" "+onOff)
	script_toggleFocusMovesNavigatorObject.__doc__=_("Toggles on and off the movement of the navigator object due to focus changes") 

	#added by Rui Batista<ruiandrebatista@gmail.com> to implement a battery status script
	def script_say_battery_status(self, keyPress, nextScript):
		UNKNOWN_BATTERY_STATUS = 0xFF
		AC_ONLINE = 0X1
		NO_SYSTEM_BATTERY = 0X80
		sps = winKernel.SYSTEM_POWER_STATUS()
		if not winKernel.GetSystemPowerStatus(sps) or sps.BatteryFlag is UNKNOWN_BATTERY_STATUS:
			debug.writeError("error accessing system power status")
			return
		if sps.BatteryFlag & NO_SYSTEM_BATTERY:
			speech.speakMessage("no system battery")
			return
		text = _("%d percent") % sps.BatteryLifePercent + " "
		if sps.ACLineStatus & AC_ONLINE: text += _("AC power on")
		elif sps.BatteryLifeTime!=0xffffffff: 
			text += _("%d hours and %d minutes remaining") % (sps.BatteryLifeTime / 3600, (sps.BatteryLifeTime % 3600) / 60)
		speech.speakMessage(text)
	script_say_battery_status.__doc__ = _("reports battery status and time remaining if AC is not plugged in")
