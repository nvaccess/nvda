# -*- coding: UTF-8 -*-
#globalCommands.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2018 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Rui Batista, Joseph Lee, Leonard de Ruijter, Derek Riemer, Babbage B.V., Davy Kager, Ethan Holliger, Łukasz Golonka

import time
import itertools
from typing import Optional

import tones
import audioDucking
import touchHandler
import keyboardHandler
import mouseHandler
import eventHandler
import review
import controlTypes
import api
import textInfos
import speech
import sayAllHandler
from NVDAObjects import NVDAObject, NVDAObjectTextInfo
import globalVars
from logHandler import log
from synthDriverHandler import *
import gui
import wx
import config
import winUser
import appModuleHandler
import winKernel
import treeInterceptorHandler
import browseMode
import scriptHandler
from scriptHandler import script
import ui
import braille
import brailleInput
import inputCore
import virtualBuffers
import characterProcessing
from baseObject import ScriptableObject
import core
import winVersion
from base64 import b16encode
import vision

#: Script category for text review commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_TEXTREVIEW = _("Text review")
#: Script category for Object navigation commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_OBJECTNAVIGATION = _("Object navigation")
#: Script category for system caret commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_SYSTEMCARET = _("System caret")
#: Script category for mouse commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_MOUSE = _("Mouse")
#: Script category for speech commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_SPEECH = _("Speech")
#: Script category for configuration dialogs commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_CONFIG = _("Configuration")
#: Script category for configuration profile activation and management commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_CONFIG_PROFILES = _("Configuration profiles")
#: Script category for Braille commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_BRAILLE = _("Braille")
#: Script category for Vision commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_VISION = _("Vision")
#: Script category for tools commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_TOOLS = pgettext('script category', 'Tools')
#: Script category for touch commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_TOUCH = _("Touch screen")
#: Script category for focus commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_FOCUS = _("System focus")
#: Script category for system status commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_SYSTEM = _("System status")
#: Script category for input commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_INPUT = _("Input")
#: Script category for document formatting commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_DOCUMENTFORMATTING = _("Document formatting")

class GlobalCommands(ScriptableObject):
	"""Commands that are available at all times, regardless of the current focus.
	"""

	def script_cycleAudioDuckingMode(self,gesture):
		if not audioDucking.isAudioDuckingSupported():
			# Translators: a message when audio ducking is not supported on this machine
			ui.message(_("Audio ducking not supported"))
			return
		curMode=config.conf['audio']['audioDuckingMode']
		numModes=len(audioDucking.audioDuckingModes)
		nextMode=(curMode+1)%numModes
		audioDucking.setAudioDuckingMode(nextMode)
		config.conf['audio']['audioDuckingMode']=nextMode
		nextLabel=audioDucking.audioDuckingModes[nextMode]
		ui.message(nextLabel)
	# Translators: Describes the Cycle audio ducking mode command.
	script_cycleAudioDuckingMode.__doc__=_("Cycles through audio ducking modes which determine when NVDA lowers the volume of other sounds")

	def script_toggleInputHelp(self,gesture):
		inputCore.manager.isInputHelpActive = not inputCore.manager.isInputHelpActive
		# Translators: This will be presented when the input help is toggled.
		stateOn = _("input help on")
		# Translators: This will be presented when the input help is toggled.
		stateOff = _("input help off")
		state = stateOn if inputCore.manager.isInputHelpActive else stateOff
		ui.message(state)
	# Translators: Input help mode message for toggle input help command.
	script_toggleInputHelp.__doc__=_("Turns input help on or off. When on, any input such as pressing a key on the keyboard will tell you what script is associated with that input, if any.")
	script_toggleInputHelp.category=SCRCAT_INPUT

	def script_toggleCurrentAppSleepMode(self,gesture):
		curFocus=api.getFocusObject()
		curApp=curFocus.appModule
		if curApp.sleepMode:
			curApp.sleepMode=False
			# Translators: This is presented when sleep mode is deactivated, NVDA will continue working as expected.
			ui.message(_("Sleep mode off"))
			eventHandler.executeEvent("gainFocus",curFocus)
		else:
			eventHandler.executeEvent("loseFocus",curFocus)
			curApp.sleepMode=True
			# Translators: This is presented when sleep mode is activated, the focused application is self voicing, such as klango or openbook.
			ui.message(_("Sleep mode on"))
	# Translators: Input help mode message for toggle sleep mode command.
	script_toggleCurrentAppSleepMode.__doc__=_("Toggles sleep mode on and off for the active application.")
	script_toggleCurrentAppSleepMode.allowInSleepMode=True

	def script_reportCurrentLine(self,gesture):
		obj=api.getFocusObject()
		treeInterceptor=obj.treeInterceptor
		if isinstance(treeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor) and not treeInterceptor.passThrough:
			obj=treeInterceptor
		try:
			info=obj.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			info=obj.makeTextInfo(textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_LINE)
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
		else:
			speech.spellTextInfo(info,useCharacterDescriptions=scriptCount>1)
	# Translators: Input help mode message for report current line command.
	script_reportCurrentLine.__doc__=_("Reports the current line under the application cursor. Pressing this key twice will spell the current line. Pressing three times will spell the line using character descriptions.")
	script_reportCurrentLine.category=SCRCAT_SYSTEMCARET

	def script_leftMouseClick(self,gesture):
		# Translators: Reported when left mouse button is clicked.
		ui.message(_("Left click"))
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)
	# Translators: Input help mode message for left mouse click command.
	script_leftMouseClick.__doc__=_("Clicks the left mouse button once at the current mouse position")
	script_leftMouseClick.category=SCRCAT_MOUSE

	def script_rightMouseClick(self,gesture):
		# Translators: Reported when right mouse button is clicked.
		ui.message(_("Right click"))
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP,0,0)
	# Translators: Input help mode message for right mouse click command.
	script_rightMouseClick.__doc__=_("Clicks the right mouse button once at the current mouse position")
	script_rightMouseClick.category=SCRCAT_MOUSE

	def script_toggleLeftMouseButton(self,gesture):
		if winUser.getKeyState(winUser.VK_LBUTTON)&32768:
			# Translators: This is presented when the left mouse button lock is released (used for drag and drop).
			ui.message(_("Left mouse button unlock"))
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)
		else:
			# Translators: This is presented when the left mouse button is locked down (used for drag and drop).
			ui.message(_("Left mouse button lock"))
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
	# Translators: Input help mode message for left mouse lock/unlock toggle command.
	script_toggleLeftMouseButton.__doc__=_("Locks or unlocks the left mouse button")
	script_toggleLeftMouseButton.category=SCRCAT_MOUSE

	def script_toggleRightMouseButton(self,gesture):
		if winUser.getKeyState(winUser.VK_RBUTTON)&32768:
			# Translators: This is presented when the right mouse button lock is released (used for drag and drop).
			ui.message(_("Right mouse button unlock"))
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP,0,0)
		else:
			# Translators: This is presented when the right mouse button is locked down (used for drag and drop).
			ui.message(_("Right mouse button lock"))
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN,0,0)
	# Translators: Input help mode message for right mouse lock/unlock command.
	script_toggleRightMouseButton.__doc__=_("Locks or unlocks the right mouse button")
	script_toggleRightMouseButton.category=SCRCAT_MOUSE

	def script_reportCurrentSelection(self,gesture):
		obj=api.getFocusObject()
		treeInterceptor=obj.treeInterceptor
		if isinstance(treeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor) and not treeInterceptor.passThrough:
			obj=treeInterceptor
		try:
			info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except (RuntimeError, NotImplementedError):
			info=None
		if not info or info.isCollapsed:
			speech.speakMessage(_("No selection"))
		else:
			speech.speakTextSelected(info.text)
	# Translators: Input help mode message for report current selection command.
	script_reportCurrentSelection.__doc__=_("Announces the current selection in edit controls and documents. If there is no selection it says so.")
	script_reportCurrentSelection.category=SCRCAT_SYSTEMCARET

	def script_dateTime(self,gesture):
		if scriptHandler.getLastScriptRepeatCount()==0:
			text=winKernel.GetTimeFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.TIME_NOSECONDS, None, None)
		else:
			text=winKernel.GetDateFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.DATE_LONGDATE, None, None)
		ui.message(text)
	# Translators: Input help mode message for report date and time command.
	script_dateTime.__doc__=_("If pressed once, reports the current time. If pressed twice, reports the current date")
	script_dateTime.category=SCRCAT_SYSTEM

	def script_increaseSynthSetting(self,gesture):
		settingName=globalVars.settingsRing.currentSettingName
		if not settingName:
			# Translators: Reported when there are no settings to configure in synth settings ring (example: when there is no setting for language).
			ui.message(_("No settings"))
			return
		settingValue=globalVars.settingsRing.increase()
		ui.message("%s %s" % (settingName,settingValue))
	# Translators: Input help mode message for increase synth setting value command.
	script_increaseSynthSetting.__doc__=_("Increases the currently active setting in the synth settings ring")
	script_increaseSynthSetting.category=SCRCAT_SPEECH

	def script_decreaseSynthSetting(self,gesture):
		settingName=globalVars.settingsRing.currentSettingName
		if not settingName:
			ui.message(_("No settings"))
			return
		settingValue=globalVars.settingsRing.decrease()
		ui.message("%s %s" % (settingName,settingValue))
	# Translators: Input help mode message for decrease synth setting value command.
	script_decreaseSynthSetting.__doc__=_("Decreases the currently active setting in the synth settings ring")
	script_decreaseSynthSetting.category=SCRCAT_SPEECH

	def script_nextSynthSetting(self,gesture):
		nextSettingName=globalVars.settingsRing.next()
		if not nextSettingName:
			ui.message(_("No settings"))
			return
		nextSettingValue=globalVars.settingsRing.currentSettingValue
		ui.message("%s %s"%(nextSettingName,nextSettingValue))
	# Translators: Input help mode message for next synth setting command.
	script_nextSynthSetting.__doc__=_("Moves to the next available setting in the synth settings ring")
	script_nextSynthSetting.category=SCRCAT_SPEECH

	def script_previousSynthSetting(self,gesture):
		previousSettingName=globalVars.settingsRing.previous()
		if not previousSettingName:
			ui.message(_("No settings"))
			return
		previousSettingValue=globalVars.settingsRing.currentSettingValue
		ui.message("%s %s"%(previousSettingName,previousSettingValue))
	# Translators: Input help mode message for previous synth setting command.
	script_previousSynthSetting.__doc__=_("Moves to the previous available setting in the synth settings ring")
	script_previousSynthSetting.category=SCRCAT_SPEECH

	def script_toggleSpeakTypedCharacters(self,gesture):
		if config.conf["keyboard"]["speakTypedCharacters"]:
			# Translators: The message announced when toggling the speak typed characters keyboard setting.
			state = _("speak typed characters off")
			config.conf["keyboard"]["speakTypedCharacters"]=False
		else:
			# Translators: The message announced when toggling the speak typed characters keyboard setting.
			state = _("speak typed characters on")
			config.conf["keyboard"]["speakTypedCharacters"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle speaked typed characters command.
	script_toggleSpeakTypedCharacters.__doc__=_("Toggles on and off the speaking of typed characters")
	script_toggleSpeakTypedCharacters.category=SCRCAT_SPEECH

	def script_toggleSpeakTypedWords(self,gesture):
		if config.conf["keyboard"]["speakTypedWords"]:
			# Translators: The message announced when toggling the speak typed words keyboard setting.
			state = _("speak typed words off")
			config.conf["keyboard"]["speakTypedWords"]=False
		else:
			# Translators: The message announced when toggling the speak typed words keyboard setting.
			state = _("speak typed words on")
			config.conf["keyboard"]["speakTypedWords"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle speak typed words command.
	script_toggleSpeakTypedWords.__doc__=_("Toggles on and off the speaking of typed words")
	script_toggleSpeakTypedWords.category=SCRCAT_SPEECH

	def script_toggleSpeakCommandKeys(self,gesture):
		if config.conf["keyboard"]["speakCommandKeys"]:
			# Translators: The message announced when toggling the speak typed command keyboard setting.
			state = _("speak command keys off")
			config.conf["keyboard"]["speakCommandKeys"]=False
		else:
			# Translators: The message announced when toggling the speak typed command keyboard setting.
			state = _("speak command keys on")
			config.conf["keyboard"]["speakCommandKeys"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle speak command keys command.
	script_toggleSpeakCommandKeys.__doc__=_("Toggles on and off the speaking of typed keys, that are not specifically characters")
	script_toggleSpeakCommandKeys.category=SCRCAT_SPEECH

	def script_toggleReportFontName(self,gesture):
		if config.conf["documentFormatting"]["reportFontName"]:
			# Translators: The message announced when toggling the report font name document formatting setting.
			state = _("report font name off")
			config.conf["documentFormatting"]["reportFontName"]=False
		else:
			# Translators: The message announced when toggling the report font name document formatting setting.
			state = _("report font name on")
			config.conf["documentFormatting"]["reportFontName"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report font name command.
	script_toggleReportFontName.__doc__=_("Toggles on and off the reporting of font changes")
	script_toggleReportFontName.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportFontSize(self,gesture):
		if config.conf["documentFormatting"]["reportFontSize"]:
			# Translators: The message announced when toggling the report font size document formatting setting.
			state = _("report font size off")
			config.conf["documentFormatting"]["reportFontSize"]=False
		else:
			# Translators: The message announced when toggling the report font size document formatting setting.
			state = _("report font size on")
			config.conf["documentFormatting"]["reportFontSize"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report font size command.
	script_toggleReportFontSize.__doc__=_("Toggles on and off the reporting of font size changes")
	script_toggleReportFontSize.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportFontAttributes(self,gesture):
		if config.conf["documentFormatting"]["reportFontAttributes"]:
			# Translators: The message announced when toggling the report font attributes document formatting setting.
			state = _("report font attributes off")
			config.conf["documentFormatting"]["reportFontAttributes"]=False
		else:
			# Translators: The message announced when toggling the report font attributes document formatting setting.
			state = _("report font attributes on")
			config.conf["documentFormatting"]["reportFontAttributes"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report font attributes command.
	script_toggleReportFontAttributes.__doc__=_("Toggles on and off the reporting of font attributes")
	script_toggleReportFontAttributes.category=SCRCAT_DOCUMENTFORMATTING

	@script(
		# Translators: Input help mode message for toggle superscripts and subscripts command.
		description=_("Toggles on and off the reporting of superscripts and subscripts"),
		category=SCRCAT_DOCUMENTFORMATTING,
	)
	def script_toggleReportSuperscriptsAndSubscripts(self, gesture):
		shouldReport: bool = not config.conf["documentFormatting"]["reportSuperscriptsAndSubscripts"]
		config.conf["documentFormatting"]["reportSuperscriptsAndSubscripts"] = shouldReport
		if shouldReport:
			# Translators: The message announced when toggling the report superscripts and subscripts
			# document formatting setting.
			state = _("report superscripts and subscripts on")
		else:
			# Translators: The message announced when toggling the report superscripts and subscripts
			# document formatting setting.
			state = _("report superscripts and subscripts off")
		ui.message(state)
	
	def script_toggleReportRevisions(self,gesture):
		if config.conf["documentFormatting"]["reportRevisions"]:
			# Translators: The message announced when toggling the report revisions document formatting setting.
			state = _("report revisions off")
			config.conf["documentFormatting"]["reportRevisions"]=False
		else:
			# Translators: The message announced when toggling the report revisions document formatting setting.
			state = _("report revisions on")
			config.conf["documentFormatting"]["reportRevisions"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report revisions command.
	script_toggleReportRevisions.__doc__=_("Toggles on and off the reporting of revisions")
	script_toggleReportRevisions.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportEmphasis(self,gesture):
		if config.conf["documentFormatting"]["reportEmphasis"]:
			# Translators: The message announced when toggling the report emphasis document formatting setting.
			state = _("report emphasis off")
			config.conf["documentFormatting"]["reportEmphasis"]=False
		else:
			# Translators: The message announced when toggling the report emphasis document formatting setting.
			state = _("report emphasis on")
			config.conf["documentFormatting"]["reportEmphasis"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report emphasis command.
	script_toggleReportEmphasis.__doc__=_("Toggles on and off the reporting of emphasis")
	script_toggleReportEmphasis.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportColor(self,gesture):
		if config.conf["documentFormatting"]["reportColor"]:
			# Translators: The message announced when toggling the report colors document formatting setting.
			state = _("report colors off")
			config.conf["documentFormatting"]["reportColor"]=False
		else:
			# Translators: The message announced when toggling the report colors document formatting setting.
			state = _("report colors on")
			config.conf["documentFormatting"]["reportColor"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report colors command.
	script_toggleReportColor.__doc__=_("Toggles on and off the reporting of colors")
	script_toggleReportColor.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportAlignment(self,gesture):
		if config.conf["documentFormatting"]["reportAlignment"]:
			# Translators: The message announced when toggling the report alignment document formatting setting.
			state = _("report alignment off")
			config.conf["documentFormatting"]["reportAlignment"]=False
		else:
			# Translators: The message announced when toggling the report alignment document formatting setting.
			state = _("report alignment on")
			config.conf["documentFormatting"]["reportAlignment"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report alignment command.
	script_toggleReportAlignment.__doc__=_("Toggles on and off the reporting of text alignment")
	script_toggleReportAlignment.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportStyle(self,gesture):
		if config.conf["documentFormatting"]["reportStyle"]:
			# Translators: The message announced when toggling the report style document formatting setting.
			state = _("report style off")
			config.conf["documentFormatting"]["reportStyle"]=False
		else:
			# Translators: The message announced when toggling the report style document formatting setting.
			state = _("report style on")
			config.conf["documentFormatting"]["reportStyle"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report style command.
	script_toggleReportStyle.__doc__=_("Toggles on and off the reporting of style changes")
	script_toggleReportStyle.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportSpellingErrors(self,gesture):
		if config.conf["documentFormatting"]["reportSpellingErrors"]:
			# Translators: The message announced when toggling the report spelling errors document formatting setting.
			state = _("report spelling errors off")
			config.conf["documentFormatting"]["reportSpellingErrors"]=False
		else:
			# Translators: The message announced when toggling the report spelling errors document formatting setting.
			state = _("report spelling errors on")
			config.conf["documentFormatting"]["reportSpellingErrors"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report spelling errors command.
	script_toggleReportSpellingErrors.__doc__=_("Toggles on and off the reporting of spelling errors")
	script_toggleReportSpellingErrors.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportPage(self,gesture):
		if config.conf["documentFormatting"]["reportPage"]:
			# Translators: The message announced when toggling the report pages document formatting setting.
			state = _("report pages off")
			config.conf["documentFormatting"]["reportPage"]=False
		else:
			# Translators: The message announced when toggling the report pages document formatting setting.
			state = _("report pages on")
			config.conf["documentFormatting"]["reportPage"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report pages command.
	script_toggleReportPage.__doc__=_("Toggles on and off the reporting of pages")
	script_toggleReportPage.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportLineNumber(self,gesture):
		if config.conf["documentFormatting"]["reportLineNumber"]:
			# Translators: The message announced when toggling the report line numbers document formatting setting.
			state = _("report line numbers off")
			config.conf["documentFormatting"]["reportLineNumber"]=False
		else:
			# Translators: The message announced when toggling the report line numbers document formatting setting.
			state = _("report line numbers on")
			config.conf["documentFormatting"]["reportLineNumber"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report line numbers command.
	script_toggleReportLineNumber.__doc__=_("Toggles on and off the reporting of line numbers")
	script_toggleReportLineNumber.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportLineIndentation(self,gesture):
		lineIndentationSpeech = config.conf["documentFormatting"]["reportLineIndentation"]
		lineIndentationTones = config.conf["documentFormatting"]["reportLineIndentationWithTones"]
		if not lineIndentationSpeech and not lineIndentationTones:
			# Translators: A message reported when cycling through line indentation settings.
			ui.message(_("Report line indentation with speech"))
			lineIndentationSpeech = True
		elif lineIndentationSpeech and not lineIndentationTones:
			# Translators: A message reported when cycling through line indentation settings.
			ui.message(_("Report line indentation with tones"))
			lineIndentationSpeech = False
			lineIndentationTones = True
		elif not lineIndentationSpeech and lineIndentationTones:
			# Translators: A message reported when cycling through line indentation settings.
			ui.message(_("Report line indentation with speech and tones"))
			lineIndentationSpeech = True
		else:
			# Translators: A message reported when cycling through line indentation settings.
			ui.message(_("Report line indentation off"))
			lineIndentationSpeech = False
			lineIndentationTones = False
		config.conf["documentFormatting"]["reportLineIndentation"] = lineIndentationSpeech
		config.conf["documentFormatting"]["reportLineIndentationWithTones"] = lineIndentationTones
	# Translators: Input help mode message for toggle report line indentation command.
	script_toggleReportLineIndentation.__doc__=_("Cycles through line indentation settings")
	script_toggleReportLineIndentation.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportParagraphIndentation(self,gesture):
		if config.conf["documentFormatting"]["reportParagraphIndentation"]:
			# Translators: The message announced when toggling the report paragraph indentation document formatting setting.
			state = _("report paragraph indentation off")
			config.conf["documentFormatting"]["reportParagraphIndentation"]=False
		else:
			# Translators: The message announced when toggling the report paragraph indentation document formatting setting.
			state = _("report paragraph indentation on")
			config.conf["documentFormatting"]["reportParagraphIndentation"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report paragraph indentation command.
	script_toggleReportParagraphIndentation.__doc__=_("Toggles on and off the reporting of paragraph indentation")
	script_toggleReportParagraphIndentation.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportLineSpacing(self,gesture):
		if config.conf["documentFormatting"]["reportLineSpacing"]:
			# Translators: The message announced when toggling the report line spacing document formatting setting.
			state = _("report line spacing off")
			config.conf["documentFormatting"]["reportLineSpacing"]=False
		else:
			# Translators: The message announced when toggling the report line spacing document formatting setting.
			state = _("report line spacing on")
			config.conf["documentFormatting"]["reportLineSpacing"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report line spacing command.
	script_toggleReportLineSpacing.__doc__=_("Toggles on and off the reporting of line spacing")
	script_toggleReportLineSpacing.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportTables(self,gesture):
		if config.conf["documentFormatting"]["reportTables"]:
			# Translators: The message announced when toggling the report tables document formatting setting.
			state = _("report tables off")
			config.conf["documentFormatting"]["reportTables"]=False
		else:
			# Translators: The message announced when toggling the report tables document formatting setting.
			state = _("report tables on")
			config.conf["documentFormatting"]["reportTables"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report tables command.
	script_toggleReportTables.__doc__=_("Toggles on and off the reporting of tables")
	script_toggleReportTables.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportTableHeaders(self,gesture):
		if config.conf["documentFormatting"]["reportTableHeaders"]:
			# Translators: The message announced when toggling the report table row/column headers document formatting setting.
			state = _("report table row and column headers off")
			config.conf["documentFormatting"]["reportTableHeaders"]=False
		else:
			# Translators: The message announced when toggling the report table row/column headers document formatting setting.
			state = _("report table row and column headers on")
			config.conf["documentFormatting"]["reportTableHeaders"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report table row/column headers command.
	script_toggleReportTableHeaders.__doc__=_("Toggles on and off the reporting of table row and column headers")
	script_toggleReportTableHeaders.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportTableCellCoords(self,gesture):
		if config.conf["documentFormatting"]["reportTableCellCoords"]:
			# Translators: The message announced when toggling the report table cell coordinates document formatting setting.
			state = _("report table cell coordinates off")
			config.conf["documentFormatting"]["reportTableCellCoords"]=False
		else:
			# Translators: The message announced when toggling the report table cell coordinates document formatting setting.
			state = _("report table cell coordinates on")
			config.conf["documentFormatting"]["reportTableCellCoords"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report table cell coordinates command.
	script_toggleReportTableCellCoords.__doc__=_("Toggles on and off the reporting of table cell coordinates")
	script_toggleReportTableCellCoords.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportLinks(self,gesture):
		if config.conf["documentFormatting"]["reportLinks"]:
			# Translators: The message announced when toggling the report links document formatting setting.
			state = _("report links off")
			config.conf["documentFormatting"]["reportLinks"]=False
		else:
			# Translators: The message announced when toggling the report links document formatting setting.
			state = _("report links on")
			config.conf["documentFormatting"]["reportLinks"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report links command.
	script_toggleReportLinks.__doc__=_("Toggles on and off the reporting of links")
	script_toggleReportLinks.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportComments(self,gesture):
		if config.conf["documentFormatting"]["reportComments"]:
			# Translators: The message announced when toggling the report comments document formatting setting.
			state = _("report comments off")
			config.conf["documentFormatting"]["reportComments"]=False
		else:
			# Translators: The message announced when toggling the report comments document formatting setting.
			state = _("report comments on")
			config.conf["documentFormatting"]["reportComments"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report comments command.
	script_toggleReportComments.__doc__=_("Toggles on and off the reporting of comments")
	script_toggleReportComments.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportLists(self,gesture):
		if config.conf["documentFormatting"]["reportLists"]:
			# Translators: The message announced when toggling the report lists document formatting setting.
			state = _("report lists off")
			config.conf["documentFormatting"]["reportLists"]=False
		else:
			# Translators: The message announced when toggling the report lists document formatting setting.
			state = _("report lists on")
			config.conf["documentFormatting"]["reportLists"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report lists command.
	script_toggleReportLists.__doc__=_("Toggles on and off the reporting of lists")
	script_toggleReportLists.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportHeadings(self,gesture):
		if config.conf["documentFormatting"]["reportHeadings"]:
			# Translators: The message announced when toggling the report headings document formatting setting.
			state = _("report headings off")
			config.conf["documentFormatting"]["reportHeadings"]=False
		else:
			# Translators: The message announced when toggling the report headings document formatting setting.
			state = _("report headings on")
			config.conf["documentFormatting"]["reportHeadings"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report headings command.
	script_toggleReportHeadings.__doc__=_("Toggles on and off the reporting of headings")
	script_toggleReportHeadings.category=SCRCAT_DOCUMENTFORMATTING

	@script(
		# Translators: Input help mode message for toggle report groupings command.
		description=_("Toggles on and off the reporting of groupings"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
	def script_toggleReportGroupings(self, gesture):
		if config.conf["documentFormatting"]["reportGroupings"]:
			# Translators: The message announced when toggling the report block quotes document formatting setting.
			state = _("report groupings off")
			config.conf["documentFormatting"]["reportGroupings"] = False
		else:
			# Translators: The message announced when toggling the report block quotes document formatting setting.
			state = _("report groupings on")
			config.conf["documentFormatting"]["reportGroupings"] = True
		ui.message(state)

	def script_toggleReportBlockQuotes(self,gesture):
		if config.conf["documentFormatting"]["reportBlockQuotes"]:
			# Translators: The message announced when toggling the report block quotes document formatting setting.
			state = _("report block quotes off")
			config.conf["documentFormatting"]["reportBlockQuotes"]=False
		else:
			# Translators: The message announced when toggling the report block quotes document formatting setting.
			state = _("report block quotes on")
			config.conf["documentFormatting"]["reportBlockQuotes"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report block quotes command.
	script_toggleReportBlockQuotes.__doc__=_("Toggles on and off the reporting of block quotes")
	script_toggleReportBlockQuotes.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportLandmarks(self,gesture):
		if config.conf["documentFormatting"]["reportLandmarks"]:
			# Translators: The message announced when toggling the report landmarks document formatting setting.
			state = _("report landmarks and regions off")
			config.conf["documentFormatting"]["reportLandmarks"]=False
		else:
			# Translators: The message announced when toggling the report landmarks document formatting setting.
			state = _("report landmarks and regions on")
			config.conf["documentFormatting"]["reportLandmarks"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report landmarks command.
	script_toggleReportLandmarks.__doc__=_("Toggles on and off the reporting of landmarks")
	script_toggleReportLandmarks.category=SCRCAT_DOCUMENTFORMATTING

	@script(
		# Translators: Input help mode message for toggle report articles command.
		description=_("Toggles on and off the reporting of articles"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
	def script_toggleReportArticles(self, gesture):
		if config.conf["documentFormatting"]["reportArticles"]:
			# Translators: The message announced when toggling the report articles document formatting setting.
			state = _("report articles off")
			config.conf["documentFormatting"]["reportArticles"] = False
		else:
			# Translators: The message announced when toggling the report articles document formatting setting.
			state = _("report articles on")
			config.conf["documentFormatting"]["reportArticles"] = True
		ui.message(state)

	def script_toggleReportFrames(self,gesture):
		if config.conf["documentFormatting"]["reportFrames"]:
			# Translators: The message announced when toggling the report frames document formatting setting.
			state = _("report frames off")
			config.conf["documentFormatting"]["reportFrames"]=False
		else:
			# Translators: The message announced when toggling the report frames document formatting setting.
			state = _("report frames on")
			config.conf["documentFormatting"]["reportFrames"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report frames command.
	script_toggleReportFrames.__doc__=_("Toggles on and off the reporting of frames")
	script_toggleReportFrames.category=SCRCAT_DOCUMENTFORMATTING

	def script_toggleReportClickable(self,gesture):
		if config.conf["documentFormatting"]["reportClickable"]:
			# Translators: The message announced when toggling the report if clickable document formatting setting.
			state = _("report if clickable off")
			config.conf["documentFormatting"]["reportClickable"]=False
		else:
			# Translators: The message announced when toggling the report if clickable document formatting setting.
			state = _("report if clickable on")
			config.conf["documentFormatting"]["reportClickable"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report if clickable command.
	script_toggleReportClickable.__doc__=_("Toggles on and off reporting if clickable")
	script_toggleReportClickable.category=SCRCAT_DOCUMENTFORMATTING

	def script_cycleSpeechSymbolLevel(self,gesture):
		curLevel = config.conf["speech"]["symbolLevel"]
		for level in characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS:
			if level > curLevel:
				break
		else:
			level = characterProcessing.SYMLVL_NONE
		name = characterProcessing.SPEECH_SYMBOL_LEVEL_LABELS[level]
		config.conf["speech"]["symbolLevel"] = level
		# Translators: Reported when the user cycles through speech symbol levels
		# which determine what symbols are spoken.
		# %s will be replaced with the symbol level; e.g. none, some, most and all.
		ui.message(_("Symbol level %s") % name)
	# Translators: Input help mode message for cycle speech symbol level command.
	script_cycleSpeechSymbolLevel.__doc__=_("Cycles through speech symbol levels which determine what symbols are spoken")
	script_cycleSpeechSymbolLevel.category=SCRCAT_SPEECH

	def script_moveMouseToNavigatorObject(self,gesture):
		try:
			p=api.getReviewPosition().pointAtStart
		except (NotImplementedError, LookupError):
			p=None
		if p:
			x=p.x
			y=p.y
		else:
			try:
				(left,top,width,height)=api.getNavigatorObject().location
			except:
				# Translators: Reported when the object has no location for the mouse to move to it.
				ui.message(_("Object has no location"))
				return
			x=left+(width//2)
			y=top+(height//2)
		winUser.setCursorPos(x,y)
		mouseHandler.executeMouseMoveEvent(x,y)
	# Translators: Input help mode message for move mouse to navigator object command.
	script_moveMouseToNavigatorObject.__doc__=_("Moves the mouse pointer to the current navigator object")
	script_moveMouseToNavigatorObject.category=SCRCAT_MOUSE

	def script_moveNavigatorObjectToMouse(self,gesture):
		# Translators: Reported when attempting to move the navigator object to the object under mouse pointer.
		ui.message(_("Move navigator object to mouse"))
		obj=api.getMouseObject()
		api.setNavigatorObject(obj)
		speech.speakObject(obj)
	# Translators: Input help mode message for move navigator object to mouse command.
	script_moveNavigatorObjectToMouse.__doc__=_("Sets the navigator object to the current object under the mouse pointer and speaks it")
	script_moveNavigatorObjectToMouse.category=SCRCAT_MOUSE

	def script_reviewMode_next(self,gesture):
		label=review.nextMode()
		if label:
			ui.reviewMessage(label)
			pos=api.getReviewPosition().copy()
			pos.expand(textInfos.UNIT_LINE)
			braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
			speech.speakTextInfo(pos)
		else:
			# Translators: reported when there are no other available review modes for this object 
			ui.reviewMessage(_("No next review mode"))
	# Translators: Script help message for next review mode command.
	script_reviewMode_next.__doc__=_("Switches to the next review mode (e.g. object, document or screen) and positions the review position at the point of the navigator object")
	script_reviewMode_next.category=SCRCAT_TEXTREVIEW

	def script_reviewMode_previous(self,gesture):
		label=review.nextMode(prev=True)
		if label:
			ui.reviewMessage(label)
			pos=api.getReviewPosition().copy()
			pos.expand(textInfos.UNIT_LINE)
			braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
			speech.speakTextInfo(pos)
		else:
			# Translators: reported when there are no other available review modes for this object 
			ui.reviewMessage(_("No previous review mode"))
	# Translators: Script help message for previous review mode command.
	script_reviewMode_previous.__doc__=_("Switches to the previous review mode (e.g. object, document or screen) and positions the review position at the point of the navigator object") 
	script_reviewMode_previous.category=SCRCAT_TEXTREVIEW

	def script_toggleSimpleReviewMode(self,gesture):
		if config.conf["reviewCursor"]["simpleReviewMode"]:
			# Translators: The message announced when toggling simple review mode.
			state = _("Simple review mode off")
			config.conf["reviewCursor"]["simpleReviewMode"]=False
		else:
			# Translators: The message announced when toggling simple review mode.
			state = _("Simple review mode on")
			config.conf["reviewCursor"]["simpleReviewMode"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle simple review mode command.
	script_toggleSimpleReviewMode.__doc__=_("Toggles simple review mode on and off")
	script_toggleSimpleReviewMode.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_current(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			# Translators: Reported when the user tries to perform a command related to the navigator object
			# but there is no current navigator object.
			ui.reviewMessage(_("No navigator object"))
			return
		if scriptHandler.getLastScriptRepeatCount()>=1:
			if curObject.TextInfo!=NVDAObjectTextInfo:
				textList=[]
				name = curObject.name
				if isinstance(name, str) and not name.isspace():
					textList.append(name)
				try:
					info=curObject.makeTextInfo(textInfos.POSITION_SELECTION)
					if not info.isCollapsed:
						textList.append(info.text)
					else:
						info.expand(textInfos.UNIT_LINE)
						if not info.isCollapsed:
							textList.append(info.text)
				except (RuntimeError, NotImplementedError):
					# No caret or selection on this object.
					pass
			else:
				textList=[]
				for prop in (curObject.name, curObject.value):
					if isinstance(prop,str) and not prop.isspace():
						textList.append(prop)
			text=" ".join(textList)
			if len(text)>0 and not text.isspace():
				if scriptHandler.getLastScriptRepeatCount()==1:
					speech.speakSpelling(text)
				else:
					if api.copyToClip(text):
						# Translators: Indicates something has been copied to clipboard (example output: title text copied to clipboard).
						speech.speakMessage(_("%s copied to clipboard")%text)
		else:
			speech.speakObject(curObject,reason=controlTypes.REASON_QUERY)
	# Translators: Input help mode message for report current navigator object command.
	script_navigatorObject_current.__doc__=_("Reports the current navigator object. Pressing twice spells this information, and pressing three times Copies name and value of this object to the clipboard")
	script_navigatorObject_current.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_currentDimensions(self,gesture):
		count=scriptHandler.getLastScriptRepeatCount()
		locationText=api.getReviewPosition().locationText if count==0 else None
		if not locationText:
			locationText=api.getNavigatorObject().locationText
		if not locationText:
			# Translators: message when there is no location information for the review cursor
			ui.message(_("No location information"))
			return
		ui.message(locationText)
	# Translators: Description for report review cursor location command.
	script_navigatorObject_currentDimensions.__doc__=_("Reports information about the location of the text or object at the review cursor. Pressing twice may provide further detail.") 
	script_navigatorObject_currentDimensions.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_toFocus(self,gesture):
		obj=api.getFocusObject()
		try:
			pos=obj.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError,RuntimeError):
			pos=obj.makeTextInfo(textInfos.POSITION_FIRST)
		api.setReviewPosition(pos)
		# Translators: Reported when attempting to move the navigator object to focus.
		speech.speakMessage(_("Move to focus"))
		speech.speakObject(obj,reason=controlTypes.REASON_FOCUS)
	# Translators: Input help mode message for move navigator object to current focus command.
	script_navigatorObject_toFocus.__doc__=_("Sets the navigator object to the current focus, and the review cursor to the position of the caret inside it, if possible.")
	script_navigatorObject_toFocus.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_moveFocus(self,gesture):
		obj=api.getNavigatorObject()
		if not isinstance(obj,NVDAObject):
			# Translators: Reported when:
			# 1. There is no focusable object e.g. cannot use tab and shift tab to move to controls.
			# 2. Trying to move focus to navigator object but there is no focus.
			ui.message(_("No focus"))
		if scriptHandler.getLastScriptRepeatCount()==0:
			# Translators: Reported when attempting to move focus to navigator object.
			ui.message(_("Move focus"))
			obj.setFocus()
		else:
			review=api.getReviewPosition()
			try:
				review.updateCaret()
			except NotImplementedError:
				# Translators: Reported when trying to move caret to the position of the review cursor but there is no caret.
				ui.message(_("No caret"))
				return
			info=review.copy()
			info.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(info,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move focus to current navigator object command.
	script_navigatorObject_moveFocus.__doc__=_("Pressed once sets the keyboard focus to the navigator object, pressed twice sets the system caret to the position of the review cursor")
	script_navigatorObject_moveFocus.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_parent(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			# Translators: Reported when the user tries to perform a command related to the navigator object
			# but there is no current navigator object.
			ui.reviewMessage(_("No navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simpleParent if simpleReviewMode else curObject.parent
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no containing (parent) object such as when focused on desktop.
			ui.reviewMessage(_("No containing object"))
	# Translators: Input help mode message for move to parent object command.
	script_navigatorObject_parent.__doc__=_("Moves the navigator object to the object containing it")
	script_navigatorObject_parent.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_next(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			# Translators: Reported when the user tries to perform a command related to the navigator object
			# but there is no current navigator object.
			ui.reviewMessage(_("No navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simpleNext if simpleReviewMode else curObject.next
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no next object (current object is the last object).
			ui.reviewMessage(_("No next"))
	# Translators: Input help mode message for move to next object command.
	script_navigatorObject_next.__doc__=_("Moves the navigator object to the next object")
	script_navigatorObject_next.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_previous(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			# Translators: Reported when the user tries to perform a command related to the navigator object
			# but there is no current navigator object.
			ui.reviewMessage(_("No navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simplePrevious if simpleReviewMode else curObject.previous
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no previous object (current object is the first object).
			ui.reviewMessage(_("No previous"))
	# Translators: Input help mode message for move to previous object command.
	script_navigatorObject_previous.__doc__=_("Moves the navigator object to the previous object")
	script_navigatorObject_previous.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_firstChild(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			# Translators: Reported when the user tries to perform a command related to the navigator object
			# but there is no current navigator object.
			ui.reviewMessage(_("No navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simpleFirstChild if simpleReviewMode else curObject.firstChild
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no contained (first child) object such as inside a document.
			ui.reviewMessage(_("No objects inside"))
	# Translators: Input help mode message for move to first child object command.
	script_navigatorObject_firstChild.__doc__=_("Moves the navigator object to the first object inside it")
	script_navigatorObject_firstChild.category=SCRCAT_OBJECTNAVIGATION

	def script_review_activate(self,gesture):
		# Translators: a message reported when the action at the position of the review cursor or navigator object is performed.
		actionName=_("Activate")
		pos=api.getReviewPosition()
		try:
			pos.activate()
			if isinstance(gesture,touchHandler.TouchInputGesture):
				touchHandler.handler.notifyInteraction(pos.NVDAObjectAtStart)
			ui.message(actionName)
			return
		except NotImplementedError:
			pass
		obj=api.getNavigatorObject()
		while obj:
			realActionName=actionName
			try:
				realActionName=obj.getActionName()
			except:
				pass
			try:
				obj.doAction()
				if isinstance(gesture,touchHandler.TouchInputGesture):
					touchHandler.handler.notifyInteraction(obj)
				ui.message(realActionName)
				return
			except NotImplementedError:
				pass
			obj=obj.parent
		# Translators: the message reported when there is no action to perform on the review position or navigator object.
		ui.message(_("No action"))
	# Translators: Input help mode message for activate current object command.
	script_review_activate.__doc__=_("Performs the default action on the current navigator object (example: presses it if it is a button).")
	script_review_activate.category=SCRCAT_OBJECTNAVIGATION

	def script_review_top(self,gesture):
		info=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_FIRST)
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to top line command.
	script_review_top.__doc__=_("Moves the review cursor to the top line of the current navigator object and speaks it")
	script_review_top.category=SCRCAT_TEXTREVIEW

	def script_review_previousLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		res=info.move(textInfos.UNIT_LINE,-1)
		if res==0:
			# Translators: a message reported when review cursor is at the top line of the current navigator object.
			ui.reviewMessage(_("Top"))
		else:
			api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to previous line command.
	script_review_previousLine.__doc__=_("Moves the review cursor to the previous line of the current navigator object and speaks it")
	script_review_previousLine.resumeSayAllMode=sayAllHandler.CURSOR_REVIEW
	script_review_previousLine.category=SCRCAT_TEXTREVIEW

	def script_review_currentLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		# Explicitly tether here
		braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
		else:
			speech.spellTextInfo(info,useCharacterDescriptions=scriptCount>1)
	# Translators: Input help mode message for read current line under review cursor command.
	script_review_currentLine.__doc__=_("Reports the line of the current navigator object where the review cursor is situated. If this key is pressed twice, the current line will be spelled. Pressing three times will spell the line using character descriptions.")
	script_review_currentLine.category=SCRCAT_TEXTREVIEW

	def script_review_nextLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		res=info.move(textInfos.UNIT_LINE,1)
		if res==0:
			# Translators: a message reported when review cursor is at the bottom line of the current navigator object.
			ui.reviewMessage(_("Bottom"))
		else:
			api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to next line command.
	script_review_nextLine.__doc__=_("Moves the review cursor to the next line of the current navigator object and speaks it")
	script_review_nextLine.resumeSayAllMode=sayAllHandler.CURSOR_REVIEW
	script_review_nextLine.category=SCRCAT_TEXTREVIEW

	def script_review_bottom(self,gesture):
		info=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_LAST)
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to bottom line command.
	script_review_bottom.__doc__=_("Moves the review cursor to the bottom line of the current navigator object and speaks it")
	script_review_bottom.category=SCRCAT_TEXTREVIEW

	def script_review_previousWord(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_WORD)
		info.collapse()
		res=info.move(textInfos.UNIT_WORD,-1)
		if res==0:
			# Translators: a message reported when review cursor is at the top line of the current navigator object.
			ui.reviewMessage(_("Top"))
		else:
			api.setReviewPosition(info)
		info.expand(textInfos.UNIT_WORD)
		speech.speakTextInfo(info,reason=controlTypes.REASON_CARET,unit=textInfos.UNIT_WORD)
	# Translators: Input help mode message for move review cursor to previous word command.
	script_review_previousWord.__doc__=_("Moves the review cursor to the previous word of the current navigator object and speaks it")
	script_review_previousWord.category=SCRCAT_TEXTREVIEW

	def script_review_currentWord(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_WORD)
		# Explicitly tether here
		braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info,reason=controlTypes.REASON_CARET,unit=textInfos.UNIT_WORD)
		else:
			speech.spellTextInfo(info,useCharacterDescriptions=scriptCount>1)
	# Translators: Input help mode message for report current word under review cursor command.
	script_review_currentWord.__doc__=_("Speaks the word of the current navigator object where the review cursor is situated. Pressing twice spells the word. Pressing three times spells the word using character descriptions")
	script_review_currentWord.category=SCRCAT_TEXTREVIEW

	def script_review_nextWord(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_WORD)
		info.collapse()
		res=info.move(textInfos.UNIT_WORD,1)
		if res==0:
			# Translators: a message reported when review cursor is at the bottom line of the current navigator object.
			ui.reviewMessage(_("Bottom"))
		else:
			api.setReviewPosition(info)
		info.expand(textInfos.UNIT_WORD)
		speech.speakTextInfo(info,reason=controlTypes.REASON_CARET,unit=textInfos.UNIT_WORD)
	# Translators: Input help mode message for move review cursor to next word command.
	script_review_nextWord.__doc__=_("Moves the review cursor to the next word of the current navigator object and speaks it")
	script_review_nextWord.category=SCRCAT_TEXTREVIEW

	def script_review_startOfLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to start of current line command.
	script_review_startOfLine.__doc__=_("Moves the review cursor to the first character of the line where it is situated in the current navigator object and speaks it")
	script_review_startOfLine.category=SCRCAT_TEXTREVIEW

	def script_review_previousCharacter(self,gesture):
		lineInfo=api.getReviewPosition().copy()
		lineInfo.expand(textInfos.UNIT_LINE)
		charInfo=api.getReviewPosition().copy()
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		res=charInfo.move(textInfos.UNIT_CHARACTER,-1)
		if res==0 or charInfo.compareEndPoints(lineInfo,"startToStart")<0:
			# Translators: a message reported when review cursor is at the leftmost character of the current navigator object's text.
			ui.reviewMessage(_("Left"))
			reviewInfo=api.getReviewPosition().copy()
			reviewInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(reviewInfo,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
		else:
			api.setReviewPosition(charInfo)
			charInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(charInfo,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to previous character command.
	script_review_previousCharacter.__doc__=_("Moves the review cursor to the previous character of the current navigator object and speaks it")
	script_review_previousCharacter.category=SCRCAT_TEXTREVIEW

	def script_review_currentCharacter(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_CHARACTER)
		# Explicitly tether here
		braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
		elif scriptCount==1:
			speech.spellTextInfo(info,useCharacterDescriptions=True)
		else:
			try:
				c = ord(info.text)
			except TypeError:
				c = None
			if c is not None:
				speech.speakMessage("%d," % c)
				speech.speakSpelling(hex(c))
			else:
				log.debugWarning("Couldn't calculate ordinal for character %r" % info.text)
				speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for report current character under review cursor command.
	script_review_currentCharacter.__doc__=_("Reports the character of the current navigator object where the review cursor is situated. Pressing twice reports a description or example of that character. Pressing three times reports the numeric value of the character in decimal and hexadecimal")
	script_review_currentCharacter.category=SCRCAT_TEXTREVIEW

	def script_review_nextCharacter(self,gesture):
		lineInfo=api.getReviewPosition().copy()
		lineInfo.expand(textInfos.UNIT_LINE)
		charInfo=api.getReviewPosition().copy()
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		res=charInfo.move(textInfos.UNIT_CHARACTER,1)
		if res==0 or charInfo.compareEndPoints(lineInfo,"endToEnd")>=0:
			# Translators: a message reported when review cursor is at the rightmost character of the current navigator object's text.
			ui.reviewMessage(_("Right"))
			reviewInfo=api.getReviewPosition().copy()
			reviewInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(reviewInfo,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
		else:
			api.setReviewPosition(charInfo)
			charInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(charInfo,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to next character command.
	script_review_nextCharacter.__doc__=_("Moves the review cursor to the next character of the current navigator object and speaks it")
	script_review_nextCharacter.category=SCRCAT_TEXTREVIEW

	def script_review_endOfLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse(end=True)
		info.move(textInfos.UNIT_CHARACTER,-1)
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to end of current line command.
	script_review_endOfLine.__doc__=_("Moves the review cursor to the last character of the line where it is situated in the current navigator object and speaks it")
	script_review_endOfLine.category=SCRCAT_TEXTREVIEW

	def _getCurrentLanguageForTextInfo(self, info):
		curLanguage = None
		if config.conf['speech']['autoLanguageSwitching']:
			for field in info.getTextWithFields({}):
				if isinstance(field, textInfos.FieldCommand) and field.command == "formatChange":
					curLanguage = field.field.get('language')
		if curLanguage is None:
			curLanguage = speech.getCurrentLanguage()
		return curLanguage

	@script(
		# Translators: Input help mode message for Review Current Symbol command.
		description=_("Reports the symbol where the review cursor is positioned. Pressed twice, shows the symbol and the text used to speak it in browse mode"),
		category=SCRCAT_TEXTREVIEW,
	)
	def script_review_currentSymbol(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_CHARACTER)
		curLanguage = self._getCurrentLanguageForTextInfo(info)
		text = info.text
		expandedSymbol = characterProcessing.processSpeechSymbol(curLanguage, text)
		if expandedSymbol == text:
			# Translators: Reported when there is no replacement for the symbol at the position of the review cursor.
			ui.message(_("No symbol replacement"))
			return
		repeats=scriptHandler.getLastScriptRepeatCount()
		if repeats == 0:
			ui.message(expandedSymbol)
		else:
			# Translators: Character and its replacement used from the "Review current Symbol" command. Example: "Character: ? Replacement: question"
			message = _("Character: {}\nReplacement: {}").format(text, expandedSymbol)
			languageDescription = languageHandler.getLanguageDescription(curLanguage)
			# Translators: title for expanded symbol dialog. Example: "Expanded symbol (English)"
			title = _("Expanded symbol ({})").format(languageDescription)
			ui.browseableMessage(message, title)

	def script_speechMode(self,gesture):
		curMode=speech.speechMode
		speech.speechMode=speech.speechMode_talk
		newMode=(curMode+1)%3
		if newMode==speech.speechMode_off:
			# Translators: A speech mode which disables speech output.
			name=_("Speech mode off")
		elif newMode==speech.speechMode_beeps:
			# Translators: A speech mode which will cause NVDA to beep instead of speaking.
			name=_("Speech mode beeps")
		elif newMode==speech.speechMode_talk:
			# Translators: The normal speech mode; i.e. NVDA will talk as normal.
			name=_("Speech mode talk")
		speech.cancelSpeech()
		ui.message(name)
		speech.speechMode=newMode
	# Translators: Input help mode message for toggle speech mode command.
	script_speechMode.__doc__=_("Toggles between the speech modes of off, beep and talk. When set to off NVDA will not speak anything. If beeps then NVDA will simply beep each time it its supposed to speak something. If talk then NVDA wil just speak normally.")
	script_speechMode.category=SCRCAT_SPEECH

	def script_moveToParentTreeInterceptor(self,gesture):
		obj=api.getFocusObject()
		parent=obj.parent
		#Move up parents until the tree interceptor of the parent is different to the tree interceptor of the object.
		#Note that this could include the situation where the parent has no tree interceptor but the object did.
		while parent and parent.treeInterceptor==obj.treeInterceptor:
			parent=parent.parent
		#If the parent has no tree interceptor, keep moving up the parents until we find a parent that does have one.
		while parent and not parent.treeInterceptor:
			parent=parent.parent
		if parent:
			parent.treeInterceptor.rootNVDAObject.setFocus()
			import eventHandler
			import wx
			# We must use core.callLater rather than wx.CallLater to ensure that the callback runs within NVDA's core pump.
			# If it didn't, and it directly or indirectly called wx.Yield, it could start executing NVDA's core pump from within the yield, causing recursion.
			core.callLater(50,eventHandler.executeEvent,"gainFocus",parent.treeInterceptor.rootNVDAObject)
	# Translators: Input help mode message for move to next document with focus command, mostly used in web browsing to move from embedded object to the webpage document.
	script_moveToParentTreeInterceptor.__doc__=_("Moves the focus to the next closest document that contains the focus")
	script_moveToParentTreeInterceptor.category=SCRCAT_FOCUS

	def script_toggleVirtualBufferPassThrough(self,gesture):
		focus = api.getFocusObject()
		vbuf = focus.treeInterceptor
		if not vbuf:
			for obj in itertools.chain((api.getFocusObject(),), reversed(api.getFocusAncestors())):
				try:
					obj.treeInterceptorClass
				except:
					continue
				break
			else:
				return
			# Force the tree interceptor to be created.
			ti = treeInterceptorHandler.update(obj, force=True)
			if not ti:
				return
			if focus in ti:
				# Update the focus, as it will have cached that there is no tree interceptor.
				focus.treeInterceptor = ti
				# If we just happened to create a browse mode TreeInterceptor
				# Then ensure that browse mode is reported here. From the users point of view, browse mode was turned on.
				if isinstance(ti,browseMode.BrowseModeTreeInterceptor) and not ti.passThrough:
					browseMode.reportPassThrough(ti,False)
					# #8716: Only let braille handle the focus when the tree interceptor is ready.
					# If not ready (e.g. a loading virtual buffer),
					# the buffer will take responsibility to update braille as soon as it completed loading.
					if ti.isReady:
						braille.handler.handleGainFocus(ti)
			return

		if not isinstance(vbuf, browseMode.BrowseModeTreeInterceptor):
			return
		# Toggle browse mode pass-through.
		vbuf.passThrough = not vbuf.passThrough
		if isinstance(vbuf,browseMode.BrowseModeTreeInterceptor):
			# If we are enabling pass-through, the user has explicitly chosen to do so, so disable auto-pass-through.
			# If we're disabling pass-through, re-enable auto-pass-through.
			vbuf.disableAutoPassThrough = vbuf.passThrough
		browseMode.reportPassThrough(vbuf)
	# Translators: Input help mode message for toggle focus and browse mode command in web browsing and other situations.
	script_toggleVirtualBufferPassThrough.__doc__=_("Toggles between browse mode and focus mode. When in focus mode, keys will pass straight through to the application, allowing you to interact directly with a control. When in browse mode, you can navigate the document with the cursor, quick navigation keys, etc.")
	script_toggleVirtualBufferPassThrough.category=inputCore.SCRCAT_BROWSEMODE

	def script_quit(self,gesture):
		gui.quit()
	# Translators: Input help mode message for quit NVDA command.
	script_quit.__doc__=_("Quits NVDA!")

	def script_restart(self,gesture):
		core.restart()
	# Translators: Input help mode message for restart NVDA command.
	script_restart.__doc__=_("Restarts NVDA!")

	def script_showGui(self,gesture):
		gui.showGui()
	# Translators: Input help mode message for show NVDA menu command.
	script_showGui.__doc__=_("Shows the NVDA menu")

	def script_review_sayAll(self,gesture):
		sayAllHandler.readText(sayAllHandler.CURSOR_REVIEW)
	script_review_sayAll.__doc__ = _(
		# Translators: Input help mode message for say all in review cursor command.
		"Reads from the review cursor up to the end of the current text,"
		" moving the review cursor as it goes"
	)
	script_review_sayAll.category=SCRCAT_TEXTREVIEW

	def script_sayAll(self,gesture):
		sayAllHandler.readText(sayAllHandler.CURSOR_CARET)
	# Translators: Input help mode message for say all with system caret command.
	script_sayAll.__doc__ = _("Reads from the system caret up to the end of the text, moving the caret as it goes")
	script_sayAll.category=SCRCAT_SYSTEMCARET

	def _reportFormattingHelper(self, info, browseable=False):
		# Report all formatting-related changes regardless of user settings
		# when explicitly requested.
		# These are the options we want reported when reporting formatting manually.
		# for full list of options that may be reported see the "documentFormatting" section of L{config.configSpec}
		reportFormattingOptions = (
			"reportFontName",
			"reportFontSize",
			"reportFontAttributes",
			"reportSuperscriptsAndSubscripts",
			"reportColor",
			"reportStyle",
			"reportAlignment",
			"reportSpellingErrors",
			"reportLineIndentation",
			"reportParagraphIndentation",
			"reportLineSpacing",
			"reportBorderStyle",
			"reportBorderColor",
		)

		# Create a dictionary to replace the config section that would normally be
		# passed to getFormatFieldsSpeech / getFormatFieldsBraille
		formatConfig = dict()
		from config import conf
		for i in conf["documentFormatting"]:
			formatConfig[i] = i in reportFormattingOptions

		textList = []
		# First, fetch indentation.
		line=info.copy()
		line.expand(textInfos.UNIT_LINE)
		indentation,content=speech.splitTextIndentation(line.text)
		if indentation:
			textList.extend(speech.getIndentationSpeech(indentation, formatConfig))
		
		info=info.copy()
		info.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		for field in info.getTextWithFields(formatConfig):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				formatField.update(field.field)

		if not browseable:
			if formatField:
				sequence = info.getFormatFieldSpeech(formatField, formatConfig=formatConfig)
				textList.extend(sequence)

			if not textList:
			# Translators: Reported when trying to obtain formatting information (such as font name, indentation and so on) but there is no formatting information for the text under cursor.
				ui.message(_("No formatting information"))
				return
				
			ui.message(" ".join(textList))
		else:
			if formatField:
				sequence = info.getFormatFieldSpeech(formatField, formatConfig=formatConfig)
				textList.extend(sequence)

			if not textList:
				# Translators: Reported when trying to obtain formatting information (such as font name, indentation and so on) but there is no formatting information for the text under cursor.
				ui.message(_("No formatting information"))
				return

			# browseable message only supports a string, remove commands:
			message = "\n".join(
				stringItem for stringItem in textList if isinstance(stringItem, str)
			)

			ui.browseableMessage(
				message,
				# Translators: title for formatting information dialog.
				_("Formatting")
			)

	def script_reportFormatting(self,gesture):
		info=api.getReviewPosition()
		repeats=scriptHandler.getLastScriptRepeatCount()
		if repeats==0:
			self._reportFormattingHelper(info,False)
		elif repeats==1:
			self._reportFormattingHelper(info,True)
	# Translators: Input help mode message for report formatting command.
	script_reportFormatting.__doc__ = _("Reports formatting info for the current review cursor position within a document. If pressed twice, presents the information in browse mode")
	script_reportFormatting.category=SCRCAT_TEXTREVIEW

	def script_reportCurrentFocus(self,gesture):
		focusObject=api.getFocusObject()
		if isinstance(focusObject,NVDAObject):
			if scriptHandler.getLastScriptRepeatCount()==0:
				speech.speakObject(focusObject, reason=controlTypes.REASON_QUERY)
			else:
				speech.speakSpelling(focusObject.name)
		else:
			ui.message(_("No focus"))
	# Translators: Input help mode message for report current focus command.
	script_reportCurrentFocus.__doc__ = _("Reports the object with focus. If pressed twice, spells the information")
	script_reportCurrentFocus.category=SCRCAT_FOCUS

	def script_reportStatusLine(self,gesture):
		obj = api.getStatusBar()
		found=False
		if obj:
			text = api.getStatusBarText(obj)
			api.setNavigatorObject(obj)
			found = True
		else:
			foreground = api.getForegroundObject()
			try:
				info = foreground.appModule.statusBarTextInfo
			except NotImplementedError:
				info = foreground.flatReviewPosition
				if info:
					info.expand(textInfos.UNIT_STORY)
					info.collapse(True)
					info.expand(textInfos.UNIT_LINE)
			if info:
				text = info.text
				info.collapse()
				api.setReviewPosition(info)
				found = True
		if not found:
			# Translators: Reported when there is no status line for the current program or window.
			ui.message(_("No status line found"))
			return
		if scriptHandler.getLastScriptRepeatCount()==0:
			if not text.strip():
				# Translators: Reported when status line exist, but is empty.
				ui.message(_("no status bar information"))
			else:
				ui.message(text)
		elif scriptHandler.getLastScriptRepeatCount()==1:
			if not  text.strip():
				# Translators: Reported when status line exist, but is empty.
				ui.message(_("no status bar information"))
			else:
				speech.speakSpelling(text)
		else:
			if not text.strip():
				# Translators: Reported when user attempts to copy content of the empty status line.
				ui.message(_("unable to copy status bar content to clipboard"))
			else:
				if api.copyToClip(text):
					# Translators: The message presented when the status bar is copied to the clipboard.
					ui.message(_("%s copied to clipboard")%text)
	# Translators: Input help mode message for report status line text command.
	script_reportStatusLine.__doc__ = _("Reads the current application status bar and moves the navigator to it. If pressed twice, spells the information. If pressed three times, copies the status bar to the clipboard")
	script_reportStatusLine.category=SCRCAT_FOCUS

	def script_toggleMouseTracking(self,gesture):
		if config.conf["mouse"]["enableMouseTracking"]:
			# Translators: presented when the mouse tracking is toggled.
			state = _("Mouse tracking off")
			config.conf["mouse"]["enableMouseTracking"]=False
		else:
			# Translators: presented when the mouse tracking is toggled.
			state = _("Mouse tracking on")
			config.conf["mouse"]["enableMouseTracking"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle mouse tracking command.
	script_toggleMouseTracking.__doc__=_("Toggles the reporting of information as the mouse moves")
	script_toggleMouseTracking.category=SCRCAT_MOUSE

	def script_toggleMouseTextResolution(self,gesture):
		values = textInfos.MOUSE_TEXT_RESOLUTION_UNITS
		labels = [textInfos.unitLabels[x] for x in values]
		try:
			index = values.index(config.conf["mouse"]["mouseTextUnit"])
		except ValueError:
			log.debugWarning("Couldn't get current mouse text resolution setting", exc_info=True)
			default = 				config.conf.getConfigValidation(("mouse", "mouseTextUnit")).default
			index = values.index(default)
		newIndex = (index+1) % len(values)
		config.conf["mouse"]["mouseTextUnit"]= values[newIndex]
		# Translators: Reports the new state of the mouse text unit resolution:.
		# %s will be replaced with the new label.
		# For example, the full message might be "Mouse text unit resolution character"
		ui.message(_("Mouse text unit resolution %s")%labels[newIndex])
	# Translators: Input help mode message for toggle mouse text unit resolution command.
	script_toggleMouseTextResolution.__doc__=_("Toggles how much text will be spoken when the mouse moves")
	script_toggleMouseTextResolution.category=SCRCAT_MOUSE

	def script_title(self,gesture):
		obj=api.getForegroundObject()
		title=obj.name
		if not isinstance(title,str) or not title or title.isspace():
			title=obj.appModule.appName if obj.appModule else None
			if not isinstance(title,str) or not title or title.isspace():
				# Translators: Reported when there is no title text for current program or window.
				title=_("No title")
		repeatCount=scriptHandler.getLastScriptRepeatCount()
		if repeatCount==0:
			ui.message(title)
		elif repeatCount==1:
			speech.speakSpelling(title)
		else:
			if api.copyToClip(title):
				ui.message(_("%s copied to clipboard")%title)
	# Translators: Input help mode message for report title bar command.
	script_title.__doc__=_("Reports the title of the current application or foreground window. If pressed twice, spells the title. If pressed three times, copies the title to the clipboard")
	script_title.category=SCRCAT_FOCUS

	def script_speakForeground(self,gesture):
		obj=api.getForegroundObject()
		if obj:
			sayAllHandler.readObjects(obj)
	# Translators: Input help mode message for read foreground object command (usually the foreground window).
	script_speakForeground.__doc__ = _("Reads all controls in the active window")
	script_speakForeground.category=SCRCAT_FOCUS

	def script_test_navigatorDisplayModelText(self,gesture):
		obj=api.getNavigatorObject()
		text=obj.displayText
		speech.speakMessage(text)
		log.info(text)

	def script_startWxInspectionTool(self, gesture):
		import wx.lib.inspection
		wx.lib.inspection.InspectionTool().Show()
	script_startWxInspectionTool.__doc__ = _(
		# Translators: GUI development tool, to get information about the components used in the NVDA GUI
		"Opens the WX GUI inspection tool. Used to get more information about the state of GUI components."
	)
	script_startWxInspectionTool.category = SCRCAT_TOOLS

	def script_navigatorObject_devInfo(self,gesture):
		obj=api.getNavigatorObject()
		if hasattr(obj, "devInfo"):
			log.info("Developer info for navigator object:\n%s" % "\n".join(obj.devInfo), activateLogViewer=True)
		else:
			log.info("No developer info for navigator object", activateLogViewer=True)
	# Translators: Input help mode message for developer info for current navigator object command, used by developers to examine technical info on navigator object. This command also serves as a shortcut to open NVDA log viewer.
	script_navigatorObject_devInfo.__doc__ = _("Logs information about the current navigator object which is useful to developers and activates the log viewer so the information can be examined.")
	script_navigatorObject_devInfo.category=SCRCAT_TOOLS

	@script(
		# Translators: Input help mode message for Open user configuration directory command.
		description=_("Opens NVDA configuration directory for the current user."),
		category=SCRCAT_TOOLS
	)
	def script_openUserConfigurationDirectory(self, gesture):
		if globalVars.appArgs.secure:
			return
		import systemUtils
		systemUtils.openUserConfigurationDirectory()

	def script_toggleProgressBarOutput(self,gesture):
		outputMode=config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]
		if outputMode=="both":
			outputMode="off"
			# Translators: A mode where no progress bar updates are given.
			ui.message(_("No progress bar updates"))
		elif outputMode=="off":
			outputMode="speak"
			# Translators: A mode where progress bar updates will be spoken.
			ui.message(_("Speak progress bar updates"))
		elif outputMode=="speak":
			outputMode="beep"
			# Translators: A mode where beeps will indicate progress bar updates (beeps rise in pitch as progress bar updates).
			ui.message(_("Beep for progress bar updates"))
		else:
			outputMode="both"
			# Translators: A mode where both speech and beeps will indicate progress bar updates.
			ui.message(_("Beep and speak progress bar updates"))
		config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]=outputMode
	# Translators: Input help mode message for toggle progress bar output command.
	script_toggleProgressBarOutput.__doc__=_("Toggles between beeps, speech, beeps and speech, and off, for reporting progress bar updates")
	script_toggleProgressBarOutput.category=SCRCAT_SPEECH

	def script_toggleReportDynamicContentChanges(self,gesture):
		if config.conf["presentation"]["reportDynamicContentChanges"]:
			# Translators: presented when the present dynamic changes is toggled.
			state = _("report dynamic content changes off")
			config.conf["presentation"]["reportDynamicContentChanges"]=False
		else:
			# Translators: presented when the present dynamic changes is toggled.
			state = _("report dynamic content changes on")
			config.conf["presentation"]["reportDynamicContentChanges"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle dynamic content changes command.
	script_toggleReportDynamicContentChanges.__doc__=_("Toggles on and off the reporting of dynamic content changes, such as new text in dos console windows")
	script_toggleReportDynamicContentChanges.category=SCRCAT_SPEECH

	def script_toggleCaretMovesReviewCursor(self,gesture):
		if config.conf["reviewCursor"]["followCaret"]:
			# Translators: presented when toggled.
			state = _("caret moves review cursor off")
			config.conf["reviewCursor"]["followCaret"]=False
		else:
			# Translators: presented when toggled.
			state = _("caret moves review cursor on")
			config.conf["reviewCursor"]["followCaret"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle caret moves review cursor command.
	script_toggleCaretMovesReviewCursor.__doc__=_("Toggles on and off the movement of the review cursor due to the caret moving.")
	script_toggleCaretMovesReviewCursor.category=SCRCAT_TEXTREVIEW

	def script_toggleFocusMovesNavigatorObject(self,gesture):
		if config.conf["reviewCursor"]["followFocus"]:
			# Translators: presented when toggled.
			state = _("focus moves navigator object off")
			config.conf["reviewCursor"]["followFocus"]=False
		else:
			# Translators: presented when toggled.
			state = _("focus moves navigator object on")
			config.conf["reviewCursor"]["followFocus"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle focus moves navigator object command.
	script_toggleFocusMovesNavigatorObject.__doc__=_("Toggles on and off the movement of the navigator object due to focus changes") 
	script_toggleFocusMovesNavigatorObject.category=SCRCAT_OBJECTNAVIGATION

	def script_toggleAutoFocusFocusableElements(self,gesture):
		if config.conf["virtualBuffers"]["autoFocusFocusableElements"]:
			# Translators: presented when toggled.
			state = _("Automatically set system focus to focusable elements off")
			config.conf["virtualBuffers"]["autoFocusFocusableElements"]=False
		else:
			# Translators: presented when toggled.
			state = _("Automatically set system focus to focusable elements on")
			config.conf["virtualBuffers"]["autoFocusFocusableElements"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle auto focus focusable elements command.
	script_toggleAutoFocusFocusableElements.__doc__=_("Toggles on and off automatic movement of the system focus due to browse mode commands") 
	script_toggleAutoFocusFocusableElements.category=inputCore.SCRCAT_BROWSEMODE

	#added by Rui Batista<ruiandrebatista@gmail.com> to implement a battery status script
	def script_say_battery_status(self,gesture):
		UNKNOWN_BATTERY_STATUS = 0xFF
		AC_ONLINE = 0X1
		NO_SYSTEM_BATTERY = 0X80
		sps = winKernel.SYSTEM_POWER_STATUS()
		if not winKernel.GetSystemPowerStatus(sps) or sps.BatteryFlag is UNKNOWN_BATTERY_STATUS:
			log.error("error accessing system power status")
			return
		if sps.BatteryFlag & NO_SYSTEM_BATTERY:
			# Translators: This is presented when there is no battery such as desktop computers and laptops with battery pack removed.
			ui.message(_("No system battery"))
			return
		# Translators: This is presented to inform the user of the current battery percentage.
		text = _("%d percent") % sps.BatteryLifePercent + " "
		# Translators: This is presented when AC power is connected such as when recharging a laptop battery.
		if sps.ACLineStatus & AC_ONLINE: text += _("AC power on")
		elif sps.BatteryLifeTime!=0xffffffff: 
			# Translators: This is the estimated remaining runtime of the laptop battery.
			text += _("{hours:d} hours and {minutes:d} minutes remaining") .format(hours=sps.BatteryLifeTime // 3600, minutes=(sps.BatteryLifeTime % 3600) // 60)
		ui.message(text)
	# Translators: Input help mode message for report battery status command.
	script_say_battery_status.__doc__ = _("Reports battery status and time remaining if AC is not plugged in")
	script_say_battery_status.category=SCRCAT_SYSTEM

	def script_passNextKeyThrough(self,gesture):
		keyboardHandler.passNextKeyThrough()
		# Translators: Spoken to indicate that the next key press will be sent straight to the current program as though NVDA is not running.
		ui.message(_("Pass next key through"))
	# Translators: Input help mode message for pass next key through command.
	script_passNextKeyThrough.__doc__=_("The next key that is pressed will not be handled at all by NVDA, it will be passed directly through to Windows.")
	script_passNextKeyThrough.category=SCRCAT_INPUT

	def script_reportAppModuleInfo(self,gesture):
		focus=api.getFocusObject()
		message = ''
		mod=focus.appModule
		if isinstance(mod,appModuleHandler.AppModule) and type(mod)!=appModuleHandler.AppModule:
			# Translators: Indicates the name of the appModule for the current program (example output: explorer module is loaded).
			# This message will not be presented if there is no module for the current program.
			message = _(" %s module is loaded. ") % mod.appModuleName.split(".")[0]
		appName=appModuleHandler.getAppNameFromProcessID(focus.processID,True)
		# Translators: Indicates the name of the current program (example output: explorer.exe is currently running).
		# Note that it does not give friendly name such as Windows Explorer; it presents the file name of the current application.
		# For example, the complete message for Windows explorer is: "explorer module is loaded. Explorer.exe is currenty running."
		message +=_(" %s is currently running.") % appName
		ui.message(message)
	# Translators: Input help mode message for report current program name and app module name command.
	script_reportAppModuleInfo.__doc__ = _("Speaks the filename of the active application along with the name of the currently loaded appModule")
	script_reportAppModuleInfo.category=SCRCAT_TOOLS

	def script_activateGeneralSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onGeneralSettingsCommand, None)
	# Translators: Input help mode message for go to general settings command.
	script_activateGeneralSettingsDialog.__doc__ = _("Shows NVDA's general settings")
	script_activateGeneralSettingsDialog.category=SCRCAT_CONFIG

	def script_activateSynthesizerDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSelectSynthesizerCommand, None)
	# Translators: Input help mode message for go to select synthesizer command.
	script_activateSynthesizerDialog.__doc__ = _("Shows the NVDA synthesizer selection dialog")
	script_activateSynthesizerDialog.category=SCRCAT_CONFIG

	def script_activateVoiceDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSpeechSettingsCommand, None)
	# Translators: Input help mode message for go to speech settings command.
	script_activateVoiceDialog.__doc__ = _("Shows NVDA's speech settings")
	script_activateVoiceDialog.category=SCRCAT_CONFIG

	def script_activateBrailleDisplayDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSelectBrailleDisplayCommand, None)
	# Translators: Input help mode message for go to select braille display command.
	script_activateBrailleDisplayDialog.__doc__ = _("Shows the NVDA braille display selection dialog")
	script_activateBrailleDisplayDialog.category=SCRCAT_CONFIG

	def script_activateBrailleSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onBrailleSettingsCommand, None)
	# Translators: Input help mode message for go to braille settings command.
	script_activateBrailleSettingsDialog.__doc__ = _("Shows NVDA's braille settings")
	script_activateBrailleSettingsDialog.category=SCRCAT_CONFIG

	def script_activateKeyboardSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onKeyboardSettingsCommand, None)
	# Translators: Input help mode message for go to keyboard settings command.
	script_activateKeyboardSettingsDialog.__doc__ = _("Shows NVDA's keyboard settings")
	script_activateKeyboardSettingsDialog.category=SCRCAT_CONFIG

	def script_activateMouseSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onMouseSettingsCommand, None)
	# Translators: Input help mode message for go to mouse settings command.
	script_activateMouseSettingsDialog.__doc__ = _("Shows NVDA's mouse settings")
	script_activateMouseSettingsDialog.category=SCRCAT_CONFIG

	def script_activateReviewCursorDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onReviewCursorCommand, None)
	# Translators: Input help mode message for go to review cursor settings command.
	script_activateReviewCursorDialog.__doc__ = _("Shows NVDA's review cursor settings")
	script_activateReviewCursorDialog.category=SCRCAT_CONFIG

	def script_activateInputCompositionDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onInputCompositionCommand, None)
	# Translators: Input help mode message for go to input composition settings command.
	script_activateInputCompositionDialog.__doc__ = _("Shows NVDA's input composition settings")
	script_activateInputCompositionDialog.category=SCRCAT_CONFIG

	def script_activateObjectPresentationDialog(self, gesture):
		wx.CallAfter(gui.mainFrame. onObjectPresentationCommand, None)
	# Translators: Input help mode message for go to object presentation settings command.
	script_activateObjectPresentationDialog.__doc__ = _("Shows NVDA's object presentation settings")
	script_activateObjectPresentationDialog.category=SCRCAT_CONFIG

	def script_activateBrowseModeDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onBrowseModeCommand, None)
	# Translators: Input help mode message for go to browse mode settings command.
	script_activateBrowseModeDialog.__doc__ = _("Shows NVDA's browse mode settings")
	script_activateBrowseModeDialog.category=SCRCAT_CONFIG

	def script_activateDocumentFormattingDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onDocumentFormattingCommand, None)
	# Translators: Input help mode message for go to document formatting settings command.
	script_activateDocumentFormattingDialog.__doc__ = _("Shows NVDA's document formatting settings")
	script_activateDocumentFormattingDialog.category=SCRCAT_CONFIG

	def script_activateDefaultDictionaryDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onDefaultDictionaryCommand, None)
	# Translators: Input help mode message for opening default dictionary dialog.
	script_activateDefaultDictionaryDialog.__doc__ = _("Shows the NVDA default dictionary dialog")
	script_activateDefaultDictionaryDialog.category=SCRCAT_CONFIG

	def script_activateVoiceDictionaryDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onVoiceDictionaryCommand, None)
	# Translators: Input help mode message for opening voice-specific dictionary dialog.
	script_activateVoiceDictionaryDialog.__doc__ = _("Shows the NVDA voice-specific dictionary dialog")
	script_activateVoiceDictionaryDialog.category=SCRCAT_CONFIG

	def script_activateTemporaryDictionaryDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onTemporaryDictionaryCommand, None)
	# Translators: Input help mode message for opening temporary dictionary.
	script_activateTemporaryDictionaryDialog.__doc__ = _("Shows the NVDA temporary dictionary dialog")
	script_activateTemporaryDictionaryDialog.category=SCRCAT_CONFIG

	def script_activateSpeechSymbolsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSpeechSymbolsCommand, None)
	# Translators: Input help mode message for go to punctuation/symbol pronunciation dialog.
	script_activateSpeechSymbolsDialog.__doc__ = _("Shows the NVDA symbol pronunciation dialog")
	script_activateSpeechSymbolsDialog.category=SCRCAT_CONFIG

	def script_activateInputGesturesDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onInputGesturesCommand, None)
	# Translators: Input help mode message for go to input gestures dialog command.
	script_activateInputGesturesDialog.__doc__ = _("Shows the NVDA input gestures dialog")
	script_activateInputGesturesDialog.category=SCRCAT_CONFIG

	@script(
		# Translators: Input help mode message for the report current configuration profile command.
		description=_("Reports the name of the current NVDA configuration profile"),
		category=SCRCAT_CONFIG,
	)
	def script_reportActiveConfigurationProfile(self, gesture):
		activeProfileName = config.conf.profiles[-1].name

		if not activeProfileName:
			# Translators: Message announced when the command to report the current configuration profile and
			# the default configuration profile is active.
			activeProfileMessage = _("normal configuration profile active")
		else:
			# Translators: Message announced when the command to report the current configuration profile
			# is active. The placeholder '{profilename}' is replaced with the name of the current active profile.
			activeProfileMessage = _("{profileName} configuration profile active").format(
				profileName=activeProfileName
			)
		ui.message(activeProfileMessage)

	def script_saveConfiguration(self,gesture):
		wx.CallAfter(gui.mainFrame.onSaveConfigurationCommand, None)
	# Translators: Input help mode message for save current configuration command.
	script_saveConfiguration.__doc__ = _("Saves the current NVDA configuration")
	script_saveConfiguration.category=SCRCAT_CONFIG

	def script_revertConfiguration(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			gui.mainFrame.onRevertToSavedConfigurationCommand(None)
		elif scriptCount==2:
			gui.mainFrame.onRevertToDefaultConfigurationCommand(None)
	script_revertConfiguration.__doc__ = _(
		# Translators: Input help mode message for apply last saved or default settings command.
		"Pressing once reverts the current configuration to the most recently saved state."
		" Pressing three times resets to factory defaults."
	)
	script_revertConfiguration.category=SCRCAT_CONFIG

	def script_activatePythonConsole(self,gesture):
		if globalVars.appArgs.secure or config.isAppX:
			return
		import pythonConsole
		if not pythonConsole.consoleUI:
			pythonConsole.initialize()
		pythonConsole.consoleUI.console.updateNamespaceSnapshotVars()
		pythonConsole.activate()
	# Translators: Input help mode message for activate python console command.
	script_activatePythonConsole.__doc__ = _("Activates the NVDA Python Console, primarily useful for development")
	script_activatePythonConsole.category=SCRCAT_TOOLS

	def script_activateAddonsManager(self,gesture):
		wx.CallAfter(gui.mainFrame.onAddonsManagerCommand, None)
		# Translators: Input help mode message for activate manage add-ons command.
	script_activateAddonsManager.__doc__ = _("Activates the NVDA Add-ons Manager to install and uninstall add-on packages for NVDA")
	script_activateAddonsManager.category=SCRCAT_TOOLS

	def script_toggleSpeechViewer(self,gesture):
		if gui.speechViewer.isActive:
			# Translators: The message announced when disabling speech viewer.
			state = _("speech viewer disabled")
			gui.speechViewer.deactivate()
			gui.mainFrame.sysTrayIcon.menu_tools_toggleSpeechViewer.Check(False)
		else:
			# Translators: The message announced when enabling speech viewer.
			state = _("speech viewer enabled")
			gui.speechViewer.activate()
			gui.mainFrame.sysTrayIcon.menu_tools_toggleSpeechViewer.Check(True)
		ui.message(state)
		# Translators: Input help mode message for toggle speech viewer command.
	script_toggleSpeechViewer.__doc__ = _("Toggles the NVDA Speech viewer, a floating window that allows you to view all the text that NVDA is currently speaking")
	script_toggleSpeechViewer.category=SCRCAT_TOOLS

	def script_braille_toggleTether(self, gesture):
		values = [x[0] for x in braille.handler.tetherValues]
		labels = [x[1] for x in braille.handler.tetherValues]
		try:
			index = values.index(
				braille.handler.TETHER_AUTO if config.conf["braille"]["autoTether"] else config.conf["braille"]["tetherTo"]
			)
		except:
			index=0
		newIndex = (index+1) % len(values)
		newTetherChoice = values[newIndex]
		if newTetherChoice==braille.handler.TETHER_AUTO:
			config.conf["braille"]["autoTether"] = True
			config.conf["braille"]["tetherTo"] = braille.handler.TETHER_FOCUS
		else:
			config.conf["braille"]["autoTether"] = False
			braille.handler.setTether(newTetherChoice, auto=False)
			if newTetherChoice==braille.handler.TETHER_REVIEW:
				braille.handler.handleReviewMove(shouldAutoTether=False)
			else:
				braille.handler.handleGainFocus(api.getFocusObject(),shouldAutoTether=False)
		# Translators: Reports which position braille is tethered to
		# (braille can be tethered automatically or to either focus or review position).
		ui.message(_("Braille tethered %s") % labels[newIndex])
	# Translators: Input help mode message for toggle braille tether to command (tethered means connected to or follows).
	script_braille_toggleTether.__doc__ = _("Toggle tethering of braille between the focus and the review position")
	script_braille_toggleTether.category=SCRCAT_BRAILLE

	def script_braille_toggleFocusContextPresentation(self, gesture):
		values = [x[0] for x in braille.focusContextPresentations]
		labels = [x[1] for x in braille.focusContextPresentations]
		try:
			index = values.index(config.conf["braille"]["focusContextPresentation"])
		except:
			index=0
		newIndex = (index+1) % len(values)
		config.conf["braille"]["focusContextPresentation"] = values[newIndex]
		braille.invalidateCachedFocusAncestors(0)
		braille.handler.handleGainFocus(api.getFocusObject())
		# Translators: Reports the new state of braille focus context presentation.
		# %s will be replaced with the context presentation setting.
		# For example, the full message might be "Braille focus context presentation: fill display for context changes"
		ui.message(_("Braille focus context presentation: %s")%labels[newIndex].lower())
	# Translators: Input help mode message for toggle braille focus context presentation command.
	script_braille_toggleFocusContextPresentation.__doc__ = _("Toggle the way context information is presented in braille")
	script_braille_toggleFocusContextPresentation.category=SCRCAT_BRAILLE

	def script_braille_toggleShowCursor(self, gesture):
		if config.conf["braille"]["showCursor"]:
			# Translators: The message announced when toggling the braille cursor.
			state = _("Braille cursor off")
			config.conf["braille"]["showCursor"]=False
		else:
			# Translators: The message announced when toggling the braille cursor.
			state = _("Braille cursor on")
			config.conf["braille"]["showCursor"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle braille cursor command.
	script_braille_toggleShowCursor.__doc__ = _("Toggle the braille cursor on and off")
	script_braille_toggleShowCursor.category=SCRCAT_BRAILLE

	def script_braille_cycleCursorShape(self, gesture):
		if not config.conf["braille"]["showCursor"]:
			# Translators: A message reported when changing the braille cursor shape when the braille cursor is turned off.
			ui.message(_("Braille cursor is turned off"))
			return
		shapes = [s[0] for s in braille.CURSOR_SHAPES]
		if braille.handler.getTether() == braille.handler.TETHER_FOCUS:
			cursorShape = "cursorShapeFocus"
		else:
			cursorShape = "cursorShapeReview"
		try:
			index = shapes.index(config.conf["braille"][cursorShape]) + 1
		except:
			index = 1
		if index >= len(braille.CURSOR_SHAPES):
			index = 0
		config.conf["braille"][cursorShape] = braille.CURSOR_SHAPES[index][0]
		shapeMsg = braille.CURSOR_SHAPES[index][1]
		# Translators: Reports which braille cursor shape is activated.
		ui.message(_("Braille cursor %s") % shapeMsg)
	# Translators: Input help mode message for cycle braille cursor shape command.
	script_braille_cycleCursorShape.__doc__ = _("Cycle through the braille cursor shapes")
	script_braille_cycleCursorShape.category=SCRCAT_BRAILLE

	def script_reportClipboardText(self,gesture):
		try:
			text = api.getClipData()
		except:
			text = None
		if not text or not isinstance(text,str) or text.isspace():
			# Translators: Presented when there is no text on the clipboard.
			ui.message(_("There is no text on the clipboard"))
			return
		if len(text) < 1024: 
			ui.message(text)
		else:
			# Translators: If the number of characters on the clipboard is greater than about 1000, it reports this message and gives number of characters on the clipboard.
			# Example output: The clipboard contains a large portion of text. It is 2300 characters long.
			ui.message(_("The clipboard contains a large portion of text. It is %s characters long") % len(text))
	# Translators: Input help mode message for report clipboard text command.
	script_reportClipboardText.__doc__ = _("Reports the text on the Windows clipboard")
	script_reportClipboardText.category=SCRCAT_SYSTEM

	def script_review_markStartForCopy(self, gesture):
		reviewPos = api.getReviewPosition()
		# attach the marker to obj so that the marker is cleaned up when obj is cleaned up.
		reviewPos.obj._copyStartMarker = reviewPos.copy() # represents the start location
		reviewPos.obj._selectThenCopyRange = None # we may be part way through a select, reset the copy range.
		# Translators: Indicates start of review cursor text to be copied to clipboard.
		ui.message(_("Start marked"))
	# Translators: Input help mode message for mark review cursor position for a select or copy command (that is, marks the current review cursor position as the starting point for text to be selected).
	script_review_markStartForCopy.__doc__ = _("Marks the current position of the review cursor as the start of text to be selected or copied")
	script_review_markStartForCopy.category=SCRCAT_TEXTREVIEW

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to marked start position for a
			# select or copy command
			"Move the review cursor to the position marked as the start of text to be selected or copied"
		),
		category=SCRCAT_TEXTREVIEW,
		gesture="kb:NVDA+shift+F9",
	)
	def script_review_moveToStartMarkedForCopy(self, gesture):
		pos = api.getReviewPosition()
		if not getattr(pos.obj, "_copyStartMarker", None):
			# Translators: Presented when attempting to move to the start marker for copy but none has been set.
			ui.reviewMessage(_("No start marker set"))
			return
		startMarker = pos.obj._copyStartMarker.copy()
		api.setReviewPosition(startMarker)
		startMarker.collapse()
		startMarker.expand(textInfos.UNIT_CHARACTER)
		speech.speakTextInfo(startMarker, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.REASON_CARET)

	def script_review_copy(self, gesture):
		pos = api.getReviewPosition().copy()
		if not getattr(pos.obj, "_copyStartMarker", None):
			# Translators: Presented when attempting to copy some review cursor text but there is no start marker.
			ui.message(_("No start marker set"))
			return
		startMarker = api.getReviewPosition().obj._copyStartMarker
		# first call, try to set the selection.
		if scriptHandler.getLastScriptRepeatCount()==0 :
			if getattr(pos.obj, "_selectThenCopyRange", None):
				# we have already tried selecting the text, dont try again. For now selections can not be ammended.
				# Translators: Presented when text has already been marked for selection, but not yet copied.
				ui.message(_("Press twice to copy or reset the start marker"))
				return
			copyMarker = startMarker.copy()
			# Check if the end position has moved
			if pos.compareEndPoints(startMarker, "endToEnd") > 0: # user has moved the cursor 'forward'
				# start becomes the original start
				copyMarker.setEndPoint(startMarker, "startToStart")
				# end needs to be updated to the current cursor position.
				copyMarker.setEndPoint(pos, "endToEnd")
				copyMarker.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
			else:# user has moved the cursor 'backwards' or not at all.
				# when the cursor is not moved at all we still want to select the character have under the cursor
				# start becomes the current cursor position position
				copyMarker.setEndPoint(pos, "startToStart")
				# end becomes the original start position plus 1
				copyMarker.setEndPoint(startMarker, "endToEnd")
				copyMarker.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
			if copyMarker.compareEndPoints(copyMarker, "startToEnd") == 0:
				# Translators: Presented when there is no text selection to copy from review cursor.
				ui.message(_("No text to copy"))
				api.getReviewPosition().obj._copyStartMarker = None
				return
			api.getReviewPosition().obj._selectThenCopyRange = copyMarker
			# for applications such as word, where the selected text is not automatically spoken we must monitor it ourself
			try:
				# old selection info must be saved so that its possible to report on the changes to the selection.
				oldInfo=pos.obj.makeTextInfo(textInfos.POSITION_SELECTION)
			except Exception as e:
				log.debug("Error trying to get initial selection information %s" % e)
				pass
			try:
				copyMarker.updateSelection()
				if hasattr(pos.obj, "reportSelectionChange"):
					# wait for applications such as word to update their selection so that we can detect it
					try:
						pos.obj.reportSelectionChange(oldInfo)
					except Exception as e:
						log.debug("Error trying to report the updated selection: %s" % e)
			except NotImplementedError as e:
				# we are unable to select the text, leave the _copyStartMarker in place in case the user wishes to copy the text.
				# Translators: Presented when unable to select the marked text.
				ui.message(_("Can't select text, press twice to copy"))
				log.debug("Error trying to update selection: %s" % e)
				return
		elif scriptHandler.getLastScriptRepeatCount()==1: # the second call, try to copy the text
			copyMarker = pos.obj._selectThenCopyRange
			if copyMarker.copyToClipboard():
				# Translators: Presented when some review text has been copied to clipboard.
				ui.message(_("Review selection copied to clipboard"))
			else:
				# Translators: Presented when unable to copy to the clipboard because of an error.
				ui.message(_("Unable to copy"))
			# on the second call always clean up the start marker
			api.getReviewPosition().obj._selectThenCopyRange = None
			api.getReviewPosition().obj._copyStartMarker = None
		return
	# Translators: Input help mode message for the select then copy command. The select then copy command first selects the review cursor text, then copies it to the clipboard.
	script_review_copy.__doc__ = _("If pressed once, the text from the previously set start marker up to and including the current position of the review cursor is selected. If pressed twice, the text is copied to the clipboard")
	script_review_copy.category=SCRCAT_TEXTREVIEW

	def script_braille_scrollBack(self, gesture):
		braille.handler.scrollBack()
	# Translators: Input help mode message for a braille command.
	script_braille_scrollBack.__doc__ = _("Scrolls the braille display back")
	script_braille_scrollBack.bypassInputHelp = True
	script_braille_scrollBack.category=SCRCAT_BRAILLE

	def script_braille_scrollForward(self, gesture):
		braille.handler.scrollForward()
	# Translators: Input help mode message for a braille command.
	script_braille_scrollForward.__doc__ = _("Scrolls the braille display forward")
	script_braille_scrollForward.bypassInputHelp = True
	script_braille_scrollForward.category=SCRCAT_BRAILLE

	def script_braille_routeTo(self, gesture):
		braille.handler.routeTo(gesture.routingIndex)
	# Translators: Input help mode message for a braille command.
	script_braille_routeTo.__doc__ = _("Routes the cursor to or activates the object under this braille cell")
	script_braille_routeTo.category=SCRCAT_BRAILLE

	def script_braille_reportFormatting(self, gesture):
		info = braille.handler.getTextInfoForWindowPos(gesture.routingIndex)
		if info is None:
			# Translators: Reported when trying to obtain formatting information (such as font name, indentation and so on) but there is no formatting information for the text under cursor.
			ui.message(_("No formatting information"))
			return
		self._reportFormattingHelper(info, False)
	# Translators: Input help mode message for Braille report formatting command.
	script_braille_reportFormatting.__doc__ = _("Reports formatting info for the text under this braille cell")
	script_braille_reportFormatting.category=SCRCAT_BRAILLE

	def script_braille_previousLine(self, gesture):
		if braille.handler.buffer.regions: 
			braille.handler.buffer.regions[-1].previousLine(start=True)
	# Translators: Input help mode message for a braille command.
	script_braille_previousLine.__doc__ = _("Moves the braille display to the previous line")
	script_braille_previousLine.category=SCRCAT_BRAILLE

	def script_braille_nextLine(self, gesture):
		if braille.handler.buffer.regions: 
			braille.handler.buffer.regions[-1].nextLine()
	# Translators: Input help mode message for a braille command.
	script_braille_nextLine.__doc__ = _("Moves the braille display to the next line")
	script_braille_nextLine.category=SCRCAT_BRAILLE

	def script_braille_dots(self, gesture):
		brailleInput.handler.input(gesture.dots)
	# Translators: Input help mode message for a braille command.
	script_braille_dots.__doc__= _("Inputs braille dots via the braille keyboard")
	script_braille_dots.category=SCRCAT_BRAILLE

	def script_braille_toFocus(self, gesture):
		braille.handler.setTether(braille.handler.TETHER_FOCUS, auto=True)
		if braille.handler.getTether() == braille.handler.TETHER_REVIEW:
			self.script_navigatorObject_toFocus(gesture)
		else:
			obj = api.getFocusObject()
			region = braille.handler.mainBuffer.regions[-1] if braille.handler.mainBuffer.regions else None
			if region and region.obj==obj:
				braille.handler.mainBuffer.focus(region)
				if region.brailleCursorPos is not None:
					braille.handler.mainBuffer.scrollTo(region, region.brailleCursorPos)
				elif region.brailleSelectionStart is not None:
					braille.handler.mainBuffer.scrollTo(region, region.brailleSelectionStart)
				braille.handler.mainBuffer.updateDisplay()
			else:
				braille.handler.handleGainFocus(obj,shouldAutoTether=False)
	# Translators: Input help mode message for a braille command.
	script_braille_toFocus.__doc__= _("Moves the braille display to the current focus")
	script_braille_toFocus.category=SCRCAT_BRAILLE

	def script_braille_eraseLastCell(self, gesture):
		brailleInput.handler.eraseLastCell()
	# Translators: Input help mode message for a braille command.
	script_braille_eraseLastCell.__doc__= _("Erases the last entered braille cell or character")
	script_braille_eraseLastCell.category=SCRCAT_BRAILLE

	def script_braille_enter(self, gesture):
		brailleInput.handler.enter()
	# Translators: Input help mode message for a braille command.
	script_braille_enter.__doc__= _("Translates any braille input and presses the enter key")
	script_braille_enter.category=SCRCAT_BRAILLE

	def script_braille_translate(self, gesture):
		brailleInput.handler.translate()
	# Translators: Input help mode message for a braille command.
	script_braille_translate.__doc__= _("Translates any braille input")
	script_braille_translate.category=SCRCAT_BRAILLE

	def script_braille_toggleShift(self, gesture):
		brailleInput.handler.toggleModifier("shift")
	# Translators: Input help mode message for a braille command.
	script_braille_toggleShift.__doc__= _("Virtually toggles the shift key to emulate a keyboard shortcut with braille input")
	script_braille_toggleShift.category=inputCore.SCRCAT_KBEMU
	script_braille_toggleShift.bypassInputHelp = True

	def script_braille_toggleControl(self, gesture):
		brailleInput.handler.toggleModifier("control")
	# Translators: Input help mode message for a braille command.
	script_braille_toggleControl.__doc__= _("Virtually toggles the control key to emulate a keyboard shortcut with braille input")
	script_braille_toggleControl.category=inputCore.SCRCAT_KBEMU
	script_braille_toggleControl.bypassInputHelp = True

	def script_braille_toggleAlt(self, gesture):
		brailleInput.handler.toggleModifier("alt")
	# Translators: Input help mode message for a braille command.
	script_braille_toggleAlt.__doc__= _("Virtually toggles the alt key to emulate a keyboard shortcut with braille input")
	script_braille_toggleAlt.category=inputCore.SCRCAT_KBEMU
	script_braille_toggleAlt.bypassInputHelp = True

	def script_braille_toggleWindows(self, gesture):
		brailleInput.handler.toggleModifier("leftWindows")
	# Translators: Input help mode message for a braille command.
	script_braille_toggleWindows.__doc__= _("Virtually toggles the left windows key to emulate a keyboard shortcut with braille input")
	script_braille_toggleWindows.category=inputCore.SCRCAT_KBEMU
	script_braille_toggleAlt.bypassInputHelp = True

	def script_braille_toggleNVDAKey(self, gesture):
		brailleInput.handler.toggleModifier("NVDA")
	# Translators: Input help mode message for a braille command.
	script_braille_toggleNVDAKey.__doc__= _("Virtually toggles the NVDA key to emulate a keyboard shortcut with braille input")
	script_braille_toggleNVDAKey.category=inputCore.SCRCAT_KBEMU
	script_braille_toggleNVDAKey.bypassInputHelp = True

	def script_reloadPlugins(self, gesture):
		import globalPluginHandler
		appModuleHandler.reloadAppModules()
		globalPluginHandler.reloadGlobalPlugins()
		NVDAObject.clearDynamicClassCache()
		# Translators: Presented when plugins (app modules and global plugins) are reloaded.
		ui.message(_("Plugins reloaded"))
	# Translators: Input help mode message for reload plugins command.
	script_reloadPlugins.__doc__=_("Reloads app modules and global plugins without restarting NVDA, which can be Useful for developers")
	script_reloadPlugins.category=SCRCAT_TOOLS

	def script_navigatorObject_nextInFlow(self,gesture):
		curObject=api.getNavigatorObject()
		newObject=None
		if curObject.simpleFirstChild:
			newObject=curObject.simpleFirstChild
		elif curObject.simpleNext:
			newObject=curObject.simpleNext
		elif curObject.simpleParent:
			parent=curObject.simpleParent
			while parent and not parent.simpleNext:
				parent=parent.simpleParent
			if parent:
				newObject=parent.simpleNext
		if newObject:
			api.setNavigatorObject(newObject)
			speech.speakObject(newObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: a message when there is no next object when navigating
			ui.reviewMessage(_("No next"))
	# Translators: Input help mode message for a touchscreen gesture.
	script_navigatorObject_nextInFlow.__doc__=_("Moves to the next object in a flattened view of the object navigation hierarchy")
	script_navigatorObject_nextInFlow.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_previousInFlow(self,gesture):
		curObject=api.getNavigatorObject()
		newObject=curObject.simplePrevious
		if newObject:
			while newObject.simpleLastChild:
				newObject=newObject.simpleLastChild
		else:
			newObject=curObject.simpleParent
		if newObject:
			api.setNavigatorObject(newObject)
			speech.speakObject(newObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: a message when there is no previous object when navigating
			ui.reviewMessage(_("No previous"))
	# Translators: Input help mode message for a touchscreen gesture.
	script_navigatorObject_previousInFlow.__doc__=_("Moves to the previous object in a flattened view of the object navigation hierarchy")
	script_navigatorObject_previousInFlow.category=SCRCAT_OBJECTNAVIGATION

	def script_touch_changeMode(self,gesture):
		mode=touchHandler.handler._curTouchMode
		index=touchHandler.availableTouchModes.index(mode)
		index=(index+1)%len(touchHandler.availableTouchModes)
		newMode=touchHandler.availableTouchModes[index]
		touchHandler.handler._curTouchMode=newMode
		try:
			newModeLabel=touchHandler.touchModeLabels[newMode]
		except KeyError:
			# Translators: Cycles through available touch modes (a group of related touch gestures; example output: "object mode"; see the user guide for more information on touch modes).
			newModeLabel=_("%s mode")%newMode
		ui.message(newModeLabel)
	# Translators: Input help mode message for a touchscreen gesture.
	script_touch_changeMode.__doc__=_("Cycles between available touch modes")
	script_touch_changeMode.category=SCRCAT_TOUCH


	def script_touch_newExplore(self,gesture):
		touchHandler.handler.screenExplorer.moveTo(gesture.x,gesture.y,new=True)
	# Translators: Input help mode message for a touchscreen gesture.
	script_touch_newExplore.__doc__=_("Reports the object and content directly under your finger")
	script_touch_newExplore.category=SCRCAT_TOUCH

	def script_touch_explore(self,gesture):
		touchHandler.handler.screenExplorer.moveTo(gesture.x,gesture.y)
	# Translators: Input help mode message for a touchscreen gesture.
	script_touch_explore.__doc__=_("Reports the new object or content under your finger if different to where your finger was last")
	script_touch_explore.category=SCRCAT_TOUCH

	def script_touch_hoverUp(self,gesture):
		#Specifically for touch typing with onscreen keyboard keys
		# #7309: by default, one mustdouble tap the touch key. To restore old behavior, go to Touch Interaction dialog and change touch typing option.
		if config.conf["touch"]["touchTyping"]:
			obj=api.getNavigatorObject()
			import NVDAObjects.UIA
			if isinstance(obj,NVDAObjects.UIA.UIA) and obj.UIAElement.cachedClassName=="CRootKey":
				obj.doAction()
	script_touch_hoverUp.category=SCRCAT_TOUCH

	def script_touch_rightClick(self, gesture):
		obj = api.getNavigatorObject()
		# Ignore invisible or offscreen objects as they cannot even be navigated with touch gestures.
		if controlTypes.STATE_INVISIBLE in obj.states or controlTypes.STATE_OFFSCREEN in obj.states:
			return
		try:
			p = api.getReviewPosition().pointAtStart
		except (NotImplementedError, LookupError):
			p = None
		if p:
			x = p.x
			y = p.y
		else:
			try:
				(left, top, width, height) = obj.location
			# Flake8/E722: stems from object location script.
			except: # noqa
				# Translators: Reported when the object has no location for the mouse to move to it.
				ui.message(_("object has no location"))
				return
			# Don't bother clicking when parts or the entire object is offscreen.
			if min(left, top, width, height) < 0:
				return
			x = left + (width // 2)
			y = top + (height // 2)
		winUser.setCursorPos(x, y)
		self.script_rightMouseClick(gesture)
	# Translators: Input help mode message for touch right click command.
	script_touch_rightClick.__doc__ = _("Clicks the right mouse button at the current touch position. This is generally used to activate a context menu.") # noqa Flake8/E501
	script_touch_rightClick.category = SCRCAT_TOUCH

	def script_activateConfigProfilesDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onConfigProfilesCommand, None)
	# Translators: Describes the command to open the Configuration Profiles dialog.
	script_activateConfigProfilesDialog.__doc__ = _("Shows the NVDA Configuration Profiles dialog")
	script_activateConfigProfilesDialog.category=SCRCAT_CONFIG_PROFILES

	def script_toggleConfigProfileTriggers(self,gesture):
		if config.conf.profileTriggersEnabled:
			config.conf.disableProfileTriggers()
			# Translators: The message announced when temporarily disabling all configuration profile triggers.
			state = _("Configuration profile triggers disabled")
		else:
			config.conf.enableProfileTriggers()
			# Explicitly trigger profiles for the current application.
			mod = api.getForegroundObject().appModule
			trigger = mod._configProfileTrigger = appModuleHandler.AppProfileTrigger(mod.appName)
			trigger.enter()
			# Translators: The message announced when re-enabling all configuration profile triggers.
			state = _("Configuration profile triggers enabled")
		ui.message(state)
	# Translators: Input help mode message for toggle configuration profile triggers command.
	script_toggleConfigProfileTriggers.__doc__=_("Toggles disabling of all configuration profile triggers. Disabling remains in effect until NVDA is restarted")
	script_toggleConfigProfileTriggers.category=SCRCAT_CONFIG

	def script_interactWithMath(self, gesture):
		import mathPres
		mathMl = mathPres.getMathMlFromTextInfo(api.getReviewPosition())
		if not mathMl:
			obj = api.getNavigatorObject()
			if obj.role == controlTypes.ROLE_MATH:
				try:
					mathMl = obj.mathMl
				except (NotImplementedError, LookupError):
					mathMl = None
		if not mathMl:
			# Translators: Reported when the user attempts math interaction
			# with something that isn't math.
			ui.message(_("Not math"))
			return
		mathPres.interactWithMathMl(mathMl)
	# Translators: Describes a command.
	script_interactWithMath.__doc__ = _("Begins interaction with math content")

	def script_recognizeWithUwpOcr(self, gesture):
		if not winVersion.isUwpOcrAvailable():
			# Translators: Reported when Windows 10 OCR is not available.
			ui.message(_("Windows 10 OCR not available"))
			return
		from contentRecog import uwpOcr, recogUi
		recog = uwpOcr.UwpOcr()
		recogUi.recognizeNavigatorObject(recog)
	# Translators: Describes a command.
	script_recognizeWithUwpOcr.__doc__ = _("Recognizes the content of the current navigator object with Windows 10 OCR")

	_tempEnableScreenCurtain = True
	_waitingOnScreenCurtainWarningDialog: Optional[wx.Dialog] = None
	_toggleScreenCurtainMessage: Optional[str] = None
	@script(
		# Translators: Input help mode message for toggle report CLDR command.
		description=_("Toggles on and off the reporting of CLDR characters, such as emojis"),
		category=SCRCAT_SPEECH,
	)
	def script_toggleReportCLDR(self, gesture):
		if config.conf["speech"]["includeCLDR"]:
			# Translators: presented when the report CLDR is toggled.
			state = _("report CLDR characters off")
			config.conf["speech"]["includeCLDR"] = False
		else:
			# Translators: presented when the report CLDR is toggled.
			state = _("report CLDR characters on")
			config.conf["speech"]["includeCLDR"] = True
		characterProcessing.clearSpeechSymbols()
		ui.message(state)

	@script(
		description=_(
			# Translators: Describes a command.
			"Toggles the state of the screen curtain, "
			"enable to make the screen black or disable to show the contents of the screen. "
			"Pressed once, screen curtain is enabled until you restart NVDA. "
			"Pressed twice, screen curtain is enabled until you disable it"
		),
		category=SCRCAT_VISION
	)
	def script_toggleScreenCurtain(self, gesture):
		scriptCount = scriptHandler.getLastScriptRepeatCount()
		if scriptCount == 0:  # first call should reset last message
			self._toggleScreenCurtainMessage = None

		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
		alreadyRunning = bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))

		GlobalCommands._tempEnableScreenCurtain = scriptCount == 0

		if self._waitingOnScreenCurtainWarningDialog:
			# Already in the process of enabling the screen curtain, exit early.
			# Ensure that the dialog is in the foreground, and read it again.
			self._waitingOnScreenCurtainWarningDialog.Raise()

			# Key presses interrupt speech, so it maybe that the dialog wasn't
			# announced properly (if the user triggered the gesture more
			# than once). So we speak the objects to imitate the dialog getting
			# focus again. It might be useful to have something like this in a
			# script: see https://github.com/nvaccess/nvda/issues/9147#issuecomment-454278313
			speech.cancelSpeech()
			speech.speakObject(
				api.getForegroundObject(),
				reason=controlTypes.REASON_FOCUS
			)
			speech.speakObject(
				api.getFocusObject(),
				reason=controlTypes.REASON_FOCUS
			)
			return

		if scriptCount >= 2 and self._toggleScreenCurtainMessage:
			# Only the first two presses have actions, all subsequent presses should just repeat the last outcome.
			# This is important when not showing warning dialog, otherwise the script completion message can be
			# suppressed.
			# Must happen after the code to raise / read the warning dialog, since if there is a warning dialog
			# it takes preference, and there shouldn't be a valid completion message in this case anyway.
			ui.message(
				self._toggleScreenCurtainMessage,
				speechPriority=speech.priorities.Spri.NOW
			)
			return

		# Disable if running
		if (
			alreadyRunning
			and scriptCount == 0  # a second press might be trying to achieve non temp enable
		):
			# Translators: Reported when the screen curtain is disabled.
			message = _("Screen curtain disabled")
			try:
				vision.handler.terminateProvider(screenCurtainProviderInfo)
			except Exception:
				# If the screen curtain was enabled, we do not expect exceptions.
				log.error("Screen curtain termination error", exc_info=True)
				# Translators: Reported when the screen curtain could not be enabled.
				message = _("Could not disable screen curtain")
			finally:
				self._toggleScreenCurtainMessage = message
				ui.message(message, speechPriority=speech.priorities.Spri.NOW)
				return
		elif (  # enable it
			scriptCount in (0, 1)  # 1 press (temp enable) or 2 presses (enable)
		):
			# Check if screen curtain is available, exit early if not.
			if not screenCurtainProviderInfo.providerClass.canStart():
				# Translators: Reported when the screen curtain is not available.
				message = _("Screen curtain not available")
				self._toggleScreenCurtainMessage = message
				ui.message(message, speechPriority=speech.priorities.Spri.NOW)
				return

			def _enableScreenCurtain(doEnable: bool = True):
				self._waitingOnScreenCurtainWarningDialog = None
				if not doEnable:
					return  # exit early with no ui.message because the user has decided to abort.

				tempEnable = GlobalCommands._tempEnableScreenCurtain
				# Translators: Reported when the screen curtain is enabled.
				enableMessage = _("Screen curtain enabled")
				if tempEnable:
					# Translators: Reported when the screen curtain is temporarily enabled.
					enableMessage = _("Temporary Screen curtain, enabled until next restart")

				try:
					if alreadyRunning:
						screenCurtainProviderInfo.providerClass.enableInConfig(True)
					else:
						vision.handler.initializeProvider(
							screenCurtainProviderInfo,
							temporary=tempEnable,
						)
				except Exception:
					log.error("Screen curtain initialization error", exc_info=True)
					# Translators: Reported when the screen curtain could not be enabled.
					enableMessage = _("Could not enable screen curtain")
				finally:
					self._toggleScreenCurtainMessage = enableMessage
					ui.message(enableMessage, speechPriority=speech.priorities.Spri.NOW)

			#  Show warning if necessary and do enable.
			settingsStorage = ScreenCurtainProvider.getSettings()
			if settingsStorage.warnOnLoad:
				from visionEnhancementProviders.screenCurtain import WarnOnLoadDialog
				parent = gui.mainFrame
				dlg = WarnOnLoadDialog(
					screenCurtainSettingsStorage=settingsStorage,
					parent=parent
				)
				self._waitingOnScreenCurtainWarningDialog = dlg
				gui.runScriptModalDialog(
					dlg,
					lambda res: wx.CallLater(
						millis=100,
						callableObj=_enableScreenCurtain,
						doEnable=res == wx.YES
					)
				)
			else:
				_enableScreenCurtain()

	__gestures = {
		# Basic
		"kb:NVDA+n": "showGui",
		"kb:NVDA+1": "toggleInputHelp",
		"kb:NVDA+q": "quit",
		"kb:NVDA+f2": "passNextKeyThrough",
		"kb(desktop):NVDA+shift+s":"toggleCurrentAppSleepMode",
		"kb(laptop):NVDA+shift+z":"toggleCurrentAppSleepMode",

		# System status
		"kb:NVDA+f12": "dateTime",
		"kb:NVDA+shift+b": "say_battery_status",
		"kb:NVDA+c": "reportClipboardText",

		# System focus
		"kb:NVDA+tab": "reportCurrentFocus",
		"kb:NVDA+t": "title",
		"kb:NVDA+b": "speakForeground",
		"kb(desktop):NVDA+end": "reportStatusLine",
		"kb(laptop):NVDA+shift+end": "reportStatusLine",

		# System caret
		"kb(desktop):NVDA+downArrow": "sayAll",
		"kb(laptop):NVDA+a": "sayAll",
		"kb(desktop):NVDA+upArrow": "reportCurrentLine",
		"kb(laptop):NVDA+l": "reportCurrentLine",
		"kb(desktop):NVDA+shift+upArrow": "reportCurrentSelection",
		"kb(laptop):NVDA+shift+s": "reportCurrentSelection",
		"kb:NVDA+f": "reportFormatting",

		# Object navigation
		"kb:NVDA+numpad5": "navigatorObject_current",
		"kb(laptop):NVDA+shift+o": "navigatorObject_current",
		"kb:NVDA+numpad8": "navigatorObject_parent",
		"kb(laptop):NVDA+shift+upArrow": "navigatorObject_parent",
		"ts(object):flickup":"navigatorObject_parent",
		"kb:NVDA+numpad4": "navigatorObject_previous",
		"kb(laptop):NVDA+shift+leftArrow": "navigatorObject_previous",
		"ts(object):flickleft":"navigatorObject_previousInFlow",
		"ts(object):2finger_flickleft":"navigatorObject_previous",
		"kb:NVDA+numpad6": "navigatorObject_next",
		"kb(laptop):NVDA+shift+rightArrow": "navigatorObject_next",
		"ts(object):flickright":"navigatorObject_nextInFlow",
		"ts(object):2finger_flickright":"navigatorObject_next",
		"kb:NVDA+numpad2": "navigatorObject_firstChild",
		"kb(laptop):NVDA+shift+downArrow": "navigatorObject_firstChild",
		"ts(object):flickdown":"navigatorObject_firstChild",
		"kb:NVDA+numpadMinus": "navigatorObject_toFocus",
		"kb(laptop):NVDA+backspace": "navigatorObject_toFocus",
		"kb:NVDA+numpadEnter": "review_activate",
		"kb(laptop):NVDA+enter": "review_activate",
		"ts:double_tap": "review_activate",
		"kb:NVDA+shift+numpadMinus": "navigatorObject_moveFocus",
		"kb(laptop):NVDA+shift+backspace": "navigatorObject_moveFocus",
		"kb:NVDA+numpadDelete": "navigatorObject_currentDimensions",
		"kb(laptop):NVDA+delete": "navigatorObject_currentDimensions",

		#Touch-specific commands
		"ts:tap":"touch_newExplore",
		"ts:hoverDown":"touch_newExplore",
		"ts:hover":"touch_explore",
		"ts:3finger_tap":"touch_changeMode",
		"ts:2finger_double_tap":"showGui",
		"ts:hoverUp":"touch_hoverUp",
		"ts:tapAndHold": "touch_rightClick", # noqa (Flake8/ET121)

		# Review cursor
		"kb:shift+numpad7": "review_top",
		"kb(laptop):NVDA+control+home": "review_top",
		"kb:numpad7": "review_previousLine",
		"ts(text):flickUp":"review_previousLine",
		"kb(laptop):NVDA+upArrow": "review_previousLine",
		"kb:numpad8": "review_currentLine",
		"kb(laptop):NVDA+shift+.": "review_currentLine",
		"kb:numpad9": "review_nextLine",
		"kb(laptop):NVDA+downArrow": "review_nextLine",
		"ts(text):flickDown":"review_nextLine",
		"kb:shift+numpad9": "review_bottom",
		"kb(laptop):NVDA+control+end": "review_bottom",
		"kb:numpad4": "review_previousWord",
		"kb(laptop):NVDA+control+leftArrow": "review_previousWord",
		"ts(text):2finger_flickLeft":"review_previousWord",
		"kb:numpad5": "review_currentWord",
		"kb(laptop):NVDA+control+.": "review_currentWord",
		"ts(text):hoverUp":"review_currentWord",
		"kb:numpad6": "review_nextWord",
		"kb(laptop):NVDA+control+rightArrow": "review_nextWord",
		"ts(text):2finger_flickRight":"review_nextWord",
		"kb:shift+numpad1": "review_startOfLine",
		"kb(laptop):NVDA+home": "review_startOfLine",
		"kb:numpad1": "review_previousCharacter",
		"kb(laptop):NVDA+leftArrow": "review_previousCharacter",
		"ts(text):flickLeft":"review_previousCharacter",
		"kb:numpad2": "review_currentCharacter",
		"kb(laptop):NVDA+.": "review_currentCharacter",
		"kb:numpad3": "review_nextCharacter",
		"kb(laptop):NVDA+rightArrow": "review_nextCharacter",
		"ts(text):flickRight":"review_nextCharacter",
		"kb:shift+numpad3": "review_endOfLine",
		"kb(laptop):NVDA+end": "review_endOfLine",
		"kb:numpadPlus": "review_sayAll",
		"kb(laptop):NVDA+shift+a": "review_sayAll",
		"ts(text):3finger_flickDown":"review_sayAll",
		"kb:NVDA+f9": "review_markStartForCopy",
		"kb:NVDA+f10": "review_copy",

		# Flat review
		"kb:NVDA+numpad7": "reviewMode_next",
		"kb(laptop):NVDA+pageUp": "reviewMode_next",
		"ts(object):2finger_flickUp": "reviewMode_next",
		"kb:NVDA+numpad1": "reviewMode_previous",
		"kb(laptop):NVDA+pageDown": "reviewMode_previous",
		"ts(object):2finger_flickDown": "reviewMode_previous",

		# Mouse
		"kb:numpadDivide": "leftMouseClick",
		"kb(laptop):NVDA+[": "leftMouseClick",
		"kb:shift+numpadDivide": "toggleLeftMouseButton",
		"kb(laptop):NVDA+control+[": "toggleLeftMouseButton",
		"kb:numpadMultiply": "rightMouseClick",
		"kb(laptop):NVDA+]": "rightMouseClick",
		"kb:shift+numpadMultiply": "toggleRightMouseButton",
		"kb(laptop):NVDA+control+]": "toggleRightMouseButton",
		"kb:NVDA+numpadDivide": "moveMouseToNavigatorObject",
		"kb(laptop):NVDA+shift+m": "moveMouseToNavigatorObject",
		"kb:NVDA+numpadMultiply": "moveNavigatorObjectToMouse",
		"kb(laptop):NVDA+shift+n": "moveNavigatorObjectToMouse",

		# Tree interceptors
		"kb:NVDA+space": "toggleVirtualBufferPassThrough",
		"kb:NVDA+control+space": "moveToParentTreeInterceptor",

		# Preferences dialogs and panels
		"kb:NVDA+control+g": "activateGeneralSettingsDialog",
		"kb:NVDA+control+s": "activateSynthesizerDialog",
		"kb:NVDA+control+v": "activateVoiceDialog",
		"kb:NVDA+control+a": "activateBrailleDisplayDialog",
		"kb:NVDA+control+k": "activateKeyboardSettingsDialog",
		"kb:NVDA+control+m": "activateMouseSettingsDialog",
		"kb:NVDA+control+o": "activateObjectPresentationDialog",
		"kb:NVDA+control+b": "activateBrowseModeDialog",
		"kb:NVDA+control+d": "activateDocumentFormattingDialog",

		# Configuration management
		"kb:NVDA+control+c": "saveConfiguration",
		"kb:NVDA+control+r": "revertConfiguration",
		"kb:NVDA+control+p": "activateConfigProfilesDialog",

		# Settings
		"kb:NVDA+shift+d":"cycleAudioDuckingMode",
		"kb:NVDA+2": "toggleSpeakTypedCharacters",
		"kb:NVDA+3": "toggleSpeakTypedWords",
		"kb:NVDA+4": "toggleSpeakCommandKeys",
		"kb:NVDA+p": "cycleSpeechSymbolLevel",
		"kb:NVDA+s": "speechMode",
		"kb:NVDA+m": "toggleMouseTracking",
		"kb:NVDA+u": "toggleProgressBarOutput",
		"kb:NVDA+5": "toggleReportDynamicContentChanges",
		"kb:NVDA+6": "toggleCaretMovesReviewCursor",
		"kb:NVDA+7": "toggleFocusMovesNavigatorObject",
		"kb:NVDA+8": "toggleAutoFocusFocusableElements",
		"kb:NVDA+control+t": "braille_toggleTether",

		# Synth settings ring
		"kb(desktop):NVDA+control+leftArrow": "previousSynthSetting",
		"kb(laptop):NVDA+shift+control+leftArrow": "previousSynthSetting",
		"kb(desktop):NVDA+control+rightArrow": "nextSynthSetting",
		"kb(laptop):NVDA+shift+control+rightArrow": "nextSynthSetting",
		"kb(desktop):NVDA+control+upArrow": "increaseSynthSetting",
		"kb(laptop):NVDA+shift+control+upArrow": "increaseSynthSetting",
		"kb(desktop):NVDA+control+downArrow": "decreaseSynthSetting",
		"kb(laptop):NVDA+control+shift+downArrow": "decreaseSynthSetting",

		# Braille keyboard
		"bk:dots" : "braille_dots",
		"bk:dot7" : "braille_eraseLastCell",
		"bk:dot8" : "braille_enter",
		"bk:dot7+dot8" : "braille_translate",

		# Tools
		"kb:NVDA+f1": "navigatorObject_devInfo",
		"kb:NVDA+control+f1": "reportAppModuleInfo",
		"kb:NVDA+control+z": "activatePythonConsole",
		"kb:NVDA+control+f3": "reloadPlugins",
		"kb(desktop):NVDA+control+f2": "test_navigatorDisplayModelText",
		"kb:NVDA+alt+m": "interactWithMath",
		"kb:NVDA+r": "recognizeWithUwpOcr",
	}

#: The single global commands instance.
#: @type: L{GlobalCommands}
commands = GlobalCommands()

class ConfigProfileActivationCommands(ScriptableObject):
	"""Singleton scriptable object that collects scripts for available configuration profiles."""

	scriptCategory = SCRCAT_CONFIG_PROFILES

	@classmethod
	def __new__(cls, *args, **kwargs):
		# Iterate through the available profiles, creating scripts for them.
		for profile in config.conf.listProfiles():
			cls.addScriptForProfile(profile)
		return 		super(ConfigProfileActivationCommands, cls).__new__(cls)

	@classmethod
	def _getScriptNameForProfile(cls, name):
		invalidChars = set()
		for c in name:
			if not c.isalnum() and c != "_":
				invalidChars.add(c)
		for c in invalidChars:
			name=name.replace(c, b16encode(c.encode()).decode("ascii"))
		return "profile_%s" % name

	@classmethod
	def _profileScript(cls, name):
		if gui.shouldConfigProfileTriggersBeSuspended():
			# Translators: a message indicating that configuration profiles can't be activated using gestures,
			# due to profile activation being suspended.
			state = _("Can't change the active profile while an NVDA dialog is open")
		elif config.conf.profiles[-1].name == name:
			config.conf.manualActivateProfile(None)
			# Translators: a message when a configuration profile is manually deactivated.
			# {profile} is replaced with the profile's name.
			state = _("{profile} profile deactivated").format(profile=name)
		else:
			config.conf.manualActivateProfile(name)
			# Translators: a message when a configuration profile is manually activated.
			# {profile} is replaced with the profile's name.
			state = _("{profile} profile activated").format(profile=name)
		ui.message(state)

	@classmethod
	def addScriptForProfile(cls, name):
		"""Adds a script for the given configuration profile.
		This method will not check a profile's existence.
		@param name: The name of the profile to add a script for.
		@type name: str
		"""
		script = lambda self, gesture: cls._profileScript(name)
		funcName = script.__name__ = "script_%s" % cls._getScriptNameForProfile(name)
		# Just set the doc string of the script, using the decorator is overkill here.
		# Translators: The description shown in input help for a script that
		# activates or deactivates a config profile.
		# {profile} is replaced with the profile's name.
		script.__doc__ = _("Activates or deactivates the {profile} configuration profile").format(profile=name)
		setattr(cls, funcName, script)

	@classmethod
	def removeScriptForProfile(cls, name):
		"""Removes a script for the given configuration profile.
		@param name: The name of the profile to remove a script for.
		@type name: str
		"""
		scriptName = cls._getScriptNameForProfile(name)
		cls._moveGesturesForProfileActivationScript(scriptName)
		delattr(cls, "script_%s" % scriptName)

	@classmethod
	def _moveGesturesForProfileActivationScript(cls, oldScriptName, newScriptName=None):
		"""Patches the user gesture map to reflect updates to profile scripts.
		@param oldScriptName: The current name of the profile activation script.
		@type oldScriptName: str
		@param newScriptName: The new name for the profile activation script, if any.
			if C{None}, the gestures are only removed for the current profile sript.
		@type newScriptName: str
		"""
		gestureMap = inputCore.manager.userGestureMap
		for scriptCls, gesture, scriptName in gestureMap.getScriptsForAllGestures():
			if scriptName != oldScriptName:
				continue
			moduleName = scriptCls.__module__
			className = scriptCls.__name__
			gestureMap.remove(gesture, moduleName, className, scriptName)
			if newScriptName is not None:
				gestureMap.add(gesture, moduleName, className, newScriptName)
		try:
			gestureMap.save()
		except:
			log.debugWarning("Couldn't save user gesture map after renaming profile script", exc_info=True)

	@classmethod
	def updateScriptForRenamedProfile(cls, oldName, newName):
		"""Removes a script for the oldName configuration profile,
		and adds a new script for newName.
		Existing gestures in the gesture map are moved from the oldName to the newName profile.
		@param oldName: The current name of the profile.
		@type oldName: str
		@param newName: The new name for the profile.
		@type newName: str
		"""
		oldScriptName = cls._getScriptNameForProfile(oldName)
		newScriptName = cls._getScriptNameForProfile(newName)
		cls._moveGesturesForProfileActivationScript(oldScriptName, newScriptName)
		delattr(cls, "script_%s" % oldScriptName)
		cls.addScriptForProfile(newName)

#: The single instance for the configuration profile activation commands.
#: @type: L{ConfigProfileActivationCommands}
configProfileActivationCommands = ConfigProfileActivationCommands()
