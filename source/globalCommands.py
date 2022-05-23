# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Rui Batista, Joseph Lee,
# Leonard de Ruijter, Derek Riemer, Babbage B.V., Davy Kager, Ethan Holliger, Łukasz Golonka, Accessolutions,
# Julien Cochuyt, Jakub Lukowicz

import itertools

from typing import (
	Optional,
	Tuple,
	Union,
)

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
from speech import sayAll
from NVDAObjects import NVDAObject, NVDAObjectTextInfo
import globalVars
from logHandler import log
import gui
import wx
import config
import winUser
import appModuleHandler
import winKernel
import treeInterceptorHandler
import browseMode
import languageHandler
import scriptHandler
from scriptHandler import script
import ui
import braille
import brailleInput
import inputCore
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

	@script(
		description=_(
			# Translators: Describes the Cycle audio ducking mode command.
			"Cycles through audio ducking modes which determine when NVDA lowers the volume of other sounds"
		),
		gesture="kb:NVDA+shift+d"
	)
	def script_cycleAudioDuckingMode(self,gesture):
		if not audioDucking.isAudioDuckingSupported():
			# Translators: a message when audio ducking is not supported on this machine
			ui.message(_("Audio ducking not supported"))
			return
		curMode=config.conf['audio']['audioDuckingMode']
		numModes = len(audioDucking.AudioDuckingMode)
		nextMode=(curMode+1)%numModes
		audioDucking.setAudioDuckingMode(nextMode)
		config.conf['audio']['audioDuckingMode']=nextMode
		nextLabel = audioDucking.AudioDuckingMode(nextMode).displayString
		ui.message(nextLabel)

	@script(
		description=_(
			# Translators: Input help mode message for toggle input help command.
			"Turns input help on or off. "
			"When on, any input such as pressing a key on the keyboard "
			"will tell you what script is associated with that input, if any."
		),
		category=SCRCAT_INPUT,
		gesture="kb:NVDA+1"
	)
	def script_toggleInputHelp(self,gesture):
		inputCore.manager.isInputHelpActive = not inputCore.manager.isInputHelpActive
		# Translators: This will be presented when the input help is toggled.
		stateOn = _("input help on")
		# Translators: This will be presented when the input help is toggled.
		stateOff = _("input help off")
		state = stateOn if inputCore.manager.isInputHelpActive else stateOff
		ui.message(state)

	@script(
		# Translators: Input help mode message for toggle sleep mode command.
		description=_("Toggles sleep mode on and off for the active application."),
		gestures=("kb(desktop):NVDA+shift+s", "kb(laptop):NVDA+shift+z"),
		allowInSleepMode=True
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for report current line command.
			"Reports the current line under the application cursor. "
			"Pressing this key twice will spell the current line. "
			"Pressing three times will spell the line using character descriptions."
		),
		category=SCRCAT_SYSTEMCARET,
		gestures=("kb(desktop):NVDA+upArrow", "kb(laptop):NVDA+l")
	)
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
			speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
		else:
			speech.spellTextInfo(info,useCharacterDescriptions=scriptCount>1)

	@script(
		# Translators: Input help mode message for left mouse click command.
		description=_("Clicks the left mouse button once at the current mouse position"),
		category=SCRCAT_MOUSE,
		gestures=("kb:numpadDivide", "kb(laptop):NVDA+[")
	)
	def script_leftMouseClick(self,gesture):
		# Translators: Reported when left mouse button is clicked.
		ui.message(_("Left click"))
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)

	@script(
		# Translators: Input help mode message for right mouse click command.
		description=_("Clicks the right mouse button once at the current mouse position"),
		category=SCRCAT_MOUSE,
		gestures=("kb:numpadMultiply", "kb(laptop):NVDA+]")
	)
	def script_rightMouseClick(self,gesture):
		# Translators: Reported when right mouse button is clicked.
		ui.message(_("Right click"))
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP,0,0)

	@script(
		# Translators: Input help mode message for left mouse lock/unlock toggle command.
		description=_("Locks or unlocks the left mouse button"),
		category=SCRCAT_MOUSE,
		gestures=("kb:shift+numpadDivide", "kb(laptop):NVDA+control+[")
	)
	def script_toggleLeftMouseButton(self,gesture):
		if mouseHandler.isLeftMouseButtonLocked():
			mouseHandler.unlockLeftMouseButton()
		else:
			mouseHandler.lockLeftMouseButton()

	@script(
		# Translators: Input help mode message for right mouse lock/unlock command.
		description=_("Locks or unlocks the right mouse button"),
		category=SCRCAT_MOUSE,
		gestures=("kb:shift+numpadMultiply", "kb(laptop):NVDA+control+]")
	)
	def script_toggleRightMouseButton(self,gesture):
		if mouseHandler.isRightMouseButtonLocked():
			mouseHandler.unlockRightMouseButton()
		else:
			mouseHandler.lockRightMouseButton()

	@script(
		description=_(
			# Translators: Input help mode message for report current selection command.
			"Announces the current selection in edit controls and documents. "
			"If there is no selection it says so."
		),
		category=SCRCAT_SYSTEMCARET,
		gestures=("kb(desktop):NVDA+shift+upArrow", "kb(laptop):NVDA+shift+s")
	)
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

	@script(
		# Translators: Input help mode message for report date and time command.
		description=_("If pressed once, reports the current time. If pressed twice, reports the current date"),
		category=SCRCAT_SYSTEM,
		gesture="kb:NVDA+f12"
	)
	def script_dateTime(self,gesture):
		if scriptHandler.getLastScriptRepeatCount()==0:
			text=winKernel.GetTimeFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.TIME_NOSECONDS, None, None)
		else:
			text=winKernel.GetDateFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.DATE_LONGDATE, None, None)
		ui.message(text)

	@script(
		# Translators: Input help mode message for increase synth setting value command.
		description=_("Increases the currently active setting in the synth settings ring"),
		category=SCRCAT_SPEECH,
		gestures=("kb(desktop):NVDA+control+upArrow", "kb(laptop):NVDA+shift+control+upArrow")
	)
	def script_increaseSynthSetting(self,gesture):
		settingName=globalVars.settingsRing.currentSettingName
		if not settingName:
			# Translators: Reported when there are no settings to configure in synth settings ring (example: when there is no setting for language).
			ui.message(_("No settings"))
			return
		settingValue=globalVars.settingsRing.increase()
		ui.message("%s %s" % (settingName,settingValue))

	@script(
		# Translators: Input help mode message for decrease synth setting value command.
		description=_("Decreases the currently active setting in the synth settings ring"),
		category=SCRCAT_SPEECH,
		gestures=("kb(desktop):NVDA+control+downArrow", "kb(laptop):NVDA+control+shift+downArrow")
	)
	def script_decreaseSynthSetting(self,gesture):
		settingName=globalVars.settingsRing.currentSettingName
		if not settingName:
			ui.message(_("No settings"))
			return
		settingValue=globalVars.settingsRing.decrease()
		ui.message("%s %s" % (settingName,settingValue))

	@script(
		# Translators: Input help mode message for next synth setting command.
		description=_("Moves to the next available setting in the synth settings ring"),
		category=SCRCAT_SPEECH,
		gestures=("kb(desktop):NVDA+control+rightArrow", "kb(laptop):NVDA+shift+control+rightArrow")
	)
	def script_nextSynthSetting(self,gesture):
		nextSettingName=globalVars.settingsRing.next()
		if not nextSettingName:
			ui.message(_("No settings"))
			return
		nextSettingValue=globalVars.settingsRing.currentSettingValue
		ui.message("%s %s"%(nextSettingName,nextSettingValue))

	@script(
		# Translators: Input help mode message for previous synth setting command.
		description=_("Moves to the previous available setting in the synth settings ring"),
		category=SCRCAT_SPEECH,
		gestures=("kb(desktop):NVDA+control+leftArrow", "kb(laptop):NVDA+shift+control+leftArrow")
	)
	def script_previousSynthSetting(self,gesture):
		previousSettingName=globalVars.settingsRing.previous()
		if not previousSettingName:
			ui.message(_("No settings"))
			return
		previousSettingValue=globalVars.settingsRing.currentSettingValue
		ui.message("%s %s"%(previousSettingName,previousSettingValue))

	@script(
		# Translators: Input help mode message for toggle speaked typed characters command.
		description=_("Toggles on and off the speaking of typed characters"),
		category=SCRCAT_SPEECH,
		gesture="kb:NVDA+2"
	)
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

	@script(
		# Translators: Input help mode message for toggle speak typed words command.
		description=_("Toggles on and off the speaking of typed words"),
		category=SCRCAT_SPEECH,
		gesture="kb:NVDA+3"
	)
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

	@script(
		# Translators: Input help mode message for toggle speak command keys command.
		description=_("Toggles on and off the speaking of typed keys, that are not specifically characters"),
		category=SCRCAT_SPEECH,
		gesture="kb:NVDA+4"
	)
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

	@script(
		# Translators: Input help mode message for toggle report font name command.
		description=_("Toggles on and off the reporting of font changes"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report font size command.
		description=_("Toggles on and off the reporting of font size changes"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report font attributes command.
		description=_("Toggles on and off the reporting of font attributes"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle superscripts and subscripts command.
		description=_("Toggles on and off the reporting of superscripts and subscripts"),
		category=SCRCAT_DOCUMENTFORMATTING
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

	@script(
		# Translators: Input help mode message for toggle report revisions command.
		description=_("Toggles on and off the reporting of revisions"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report emphasis command.
		description=_("Toggles on and off the reporting of emphasis"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report marked (highlighted) content command.
		description=_("Toggles on and off the reporting of highlighted text"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
	def script_toggleReportHighlightedText(self, gesture):
		shouldReport: bool = not config.conf["documentFormatting"]["reportHighlight"]
		config.conf["documentFormatting"]["reportHighlight"] = shouldReport
		if shouldReport:
			# Translators: The message announced when toggling the report marked document formatting setting.
			state = _("report highlighted on")
		else:
			# Translators: The message announced when toggling the report marked document formatting setting.
			state = _("report highlighted off")
		ui.message(state)

	@script(
		# Translators: Input help mode message for toggle report colors command.
		description=_("Toggles on and off the reporting of colors"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report alignment command.
		description=_("Toggles on and off the reporting of text alignment"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report style command.
		description=_("Toggles on and off the reporting of style changes"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report spelling errors command.
		description=_("Toggles on and off the reporting of spelling errors"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report pages command.
		description=_("Toggles on and off the reporting of pages"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report line numbers command.
		description=_("Toggles on and off the reporting of line numbers"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report line indentation command.
		description=_("Cycles through line indentation settings"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report paragraph indentation command.
		description=_("Toggles on and off the reporting of paragraph indentation"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report line spacing command.
		description=_("Toggles on and off the reporting of line spacing"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report tables command.
		description=_("Toggles on and off the reporting of tables"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report table row/column headers command.
		description=_("Toggles on and off the reporting of table row and column headers"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report table cell coordinates command.
		description=_("Toggles on and off the reporting of table cell coordinates"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report cell borders command.
		description=_("Cycles through the cell border reporting settings"),
		category=SCRCAT_DOCUMENTFORMATTING,
	)
	def script_toggleReportCellBorders(self, gesture):
		if (
			not config.conf["documentFormatting"]["reportBorderStyle"]
			and not config.conf["documentFormatting"]["reportBorderColor"]
		):
			# Translators: A message reported when cycling through cell borders settings.
			ui.message(_("Report styles of cell borders"))
			config.conf["documentFormatting"]["reportBorderStyle"] = True
		elif (
			config.conf["documentFormatting"]["reportBorderStyle"]
			and not config.conf["documentFormatting"]["reportBorderColor"]
		):
			# Translators: A message reported when cycling through cell borders settings.
			ui.message(_("Report colors and styles of cell borders"))
			config.conf["documentFormatting"]["reportBorderColor"] = True
		else:
			# Translators: A message reported when cycling through cell borders settings.
			ui.message(_("Report cell borders off."))
			config.conf["documentFormatting"]["reportBorderStyle"] = False
			config.conf["documentFormatting"]["reportBorderColor"] = False

	@script(
		# Translators: Input help mode message for toggle report links command.
		description=_("Toggles on and off the reporting of links"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report graphics command.
		description=_("Toggles on and off the reporting of graphics"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
	def script_toggleReportGraphics(self, gesture):
		if config.conf["documentFormatting"]["reportGraphics"]:
			# Translators: The message announced when toggling the report graphics document formatting setting.
			state = _("report graphics off")
			config.conf["documentFormatting"]["reportGraphics"] = False
		else:
			# Translators: The message announced when toggling the report graphics document formatting setting.
			state = _("report graphics on")
			config.conf["documentFormatting"]["reportGraphics"] = True
		ui.message(state)

	@script(
		# Translators: Input help mode message for toggle report comments command.
		description=_("Toggles on and off the reporting of comments"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report lists command.
		description=_("Toggles on and off the reporting of lists"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report headings command.
		description=_("Toggles on and off the reporting of headings"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report block quotes command.
		description=_("Toggles on and off the reporting of block quotes"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report landmarks command.
		description=_("Toggles on and off the reporting of landmarks"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report frames command.
		description=_("Toggles on and off the reporting of frames"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		# Translators: Input help mode message for toggle report if clickable command.
		description=_("Toggles on and off reporting if clickable"),
		category=SCRCAT_DOCUMENTFORMATTING
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for cycle through automatic language switching mode command.
			"Cycles through speech modes for automatic language switching: "
			"off, language only and language and dialect."
		),
		category=SCRCAT_SPEECH,
	)
	def script_cycleSpeechAutomaticLanguageSwitching(self, gesture):
		if config.conf["speech"]["autoLanguageSwitching"]:
			if config.conf["speech"]["autoDialectSwitching"]:
				# Translators: A message reported when executing the cycle automatic language switching mode command.
				state = _("Automatic language switching off")
				config.conf["speech"]["autoLanguageSwitching"] = False
				config.conf["speech"]["autoDialectSwitching"] = False
			else:
				# Translators: A message reported when executing the cycle automatic language switching mode command.
				state = _("Automatic language and dialect switching on")
				config.conf["speech"]["autoDialectSwitching"] = True
		else:
			# Translators: A message reported when executing the cycle automatic language switching mode command.
			state = _("Automatic language switching on")
			config.conf["speech"]["autoLanguageSwitching"] = True
			config.conf["speech"]["autoDialectSwitching"] = False
		ui.message(state)

	@script(
		# Translators: Input help mode message for cycle speech symbol level command.
		description=_("Cycles through speech symbol levels which determine what symbols are spoken"),
		category=SCRCAT_SPEECH,
		gesture="kb:NVDA+p"
	)
	def script_cycleSpeechSymbolLevel(self,gesture):
		curLevel = config.conf["speech"]["symbolLevel"]
		for level in characterProcessing.CONFIGURABLE_SPEECH_SYMBOL_LEVELS:
			if level > curLevel:
				break
		else:
			level = characterProcessing.SymbolLevel.NONE
		name = characterProcessing.SPEECH_SYMBOL_LEVEL_LABELS[level]
		config.conf["speech"]["symbolLevel"] = level.value
		# Translators: Reported when the user cycles through speech symbol levels
		# which determine what symbols are spoken.
		# %s will be replaced with the symbol level; e.g. none, some, most and all.
		ui.message(_("Symbol level %s") % name)

	@script(
		# Translators: Input help mode message for move mouse to navigator object command.
		description=_("Moves the mouse pointer to the current navigator object"),
		category=SCRCAT_MOUSE,
		gestures=("kb:NVDA+numpadDivide", "kb(laptop):NVDA+shift+m")
	)
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

	@script(
		# Translators: Input help mode message for move navigator object to mouse command.
		description=_("Sets the navigator object to the current object under the mouse pointer and speaks it"),
		category=SCRCAT_MOUSE,
		gestures=("kb:NVDA+numpadMultiply", "kb(laptop):NVDA+shift+n")
	)
	def script_moveNavigatorObjectToMouse(self,gesture):
		# Translators: Reported when attempting to move the navigator object to the object under mouse pointer.
		ui.message(_("Move navigator object to mouse"))
		obj=api.getMouseObject()
		api.setNavigatorObject(obj)
		speech.speakObject(obj)

	@script(
		description=_(
			# Translators: Script help message for next review mode command.
			"Switches to the next review mode (e.g. object, document or screen) "
			"and positions the review position at the point of the navigator object"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:NVDA+numpad7", "kb(laptop):NVDA+pageUp", "ts(object):2finger_flickUp")
	)
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

	@script(
		description=_(
			# Translators: Script help message for previous review mode command.
			"Switches to the previous review mode (e.g. object, document or screen) "
			"and positions the review position at the point of the navigator object"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:NVDA+numpad1", "kb(laptop):NVDA+pageDown", "ts(object):2finger_flickDown")
	)
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

	@script(
		# Translators: Input help mode message for toggle simple review mode command.
		description=_("Toggles simple review mode on and off"),
		category=SCRCAT_OBJECTNAVIGATION
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for report current navigator object command.
			"Reports the current navigator object. "
			"Pressing twice spells this information, "
			"and pressing three times Copies name and value of this object to the clipboard"
		),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+numpad5", "kb(laptop):NVDA+shift+o")
	)
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
				if name and isinstance(name, str) and not name.isspace():
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
					if prop and isinstance(prop, str) and not prop.isspace():
						textList.append(prop)
			text=" ".join(textList)
			if len(text)>0 and not text.isspace():
				if scriptHandler.getLastScriptRepeatCount()==1:
					speech.speakSpelling(text)
				else:
					api.copyToClip(text, notify=True)
		else:
			speech.speakObject(curObject, reason=controlTypes.OutputReason.QUERY)

	@staticmethod
	def _reportLocationText(objs: Tuple[Union[None, NVDAObject, textInfos.TextInfo], ...]) -> None:
		for obj in objs:
			if obj is not None and obj.locationText:
				ui.message(obj.locationText)
				return
		# Translators: message when there is no location information
		ui.message(_("No location information"))

	@script(
		description=_(
			# Translators: Description for a keyboard command which reports location of the
			# review cursor, falling back to the location of navigator object if needed.
			"Reports information about the location of the text at the review cursor, "
			"or location of the navigator object if there is no text under review cursor."
		),
		category=SCRCAT_OBJECTNAVIGATION,
	)
	def script_reportReviewCursorLocation(self, gesture):
		self._reportLocationText((api.getReviewPosition(), api.getNavigatorObject()))

	@script(
		description=_(
			# Translators: Description for a keyboard command which reports location of the navigator object.
			"Reports information about the location of the current navigator object."
		),
		category=SCRCAT_OBJECTNAVIGATION,
	)
	def script_reportCurrentNavigatorObjectLocation(self, gesture):
		self._reportLocationText((api.getNavigatorObject(),))

	@script(
		description=_(
			# Translators: Description for a keyboard command which reports location of the
			# current caret position falling back to the location of focused object if needed.
			"Reports information about the location of the text at the caret, "
			"or location of the currently focused object if there is no caret."
		),
		category=SCRCAT_SYSTEMCARET,
	)
	def script_reportCaretLocation(self, gesture):
		self._reportLocationText(
			(self._getTIAtCaret(fallbackToPOSITION_FIRST=True, reportFailure=False), api.getFocusObject())
		)

	@script(
		description=_(
			# Translators: Description for a keyboard command which reports location of the
			# currently focused object.
			"Reports information about the location of the currently focused object."
		),
		category=SCRCAT_FOCUS,
	)
	def script_reportFocusObjectLocation(self, gesture):
		self._reportLocationText((api.getFocusObject(),))

	@script(
		description=_(
			# Translators: Description for report review cursor location command.
			"Reports information about the location of the text or object at the review cursor. "
			"Pressing twice may provide further detail."
		),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+shift+numpadDelete", "kb(laptop):NVDA+shift+delete")
	)
	def script_navigatorObject_currentDimensions(self, gesture):
		if scriptHandler.getLastScriptRepeatCount() == 0:
			self.script_reportReviewCursorLocation(gesture)
		else:
			self.script_reportCurrentNavigatorObjectLocation(gesture)

	@script(
		description=_(
			# Translators: Description for a keyboard command
			# which reports location of the text at the caret position
			# or object with focus if there is no caret.
			"Reports information about the location of the text or object at the position of system caret. "
			"Pressing twice may provide further detail."
		),
		category=SCRCAT_SYSTEMCARET,
		gestures=("kb:NVDA+numpadDelete", "kb(laptop):NVDA+delete")
	)
	def script_caretPos_currentDimensions(self, gesture):
		if scriptHandler.getLastScriptRepeatCount() == 0:
			self.script_reportCaretLocation(gesture)
		else:
			self.script_reportFocusObjectLocation(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for move navigator object to current focus command.
			"Sets the navigator object to the current focus, "
			"and the review cursor to the position of the caret inside it, if possible."
		),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+numpadMinus", "kb(laptop):NVDA+backspace")
	)
	def script_navigatorObject_toFocus(self,gesture):
		tIAtCaret = self._getTIAtCaret(True)
		focusedObj = api.getFocusObject()
		api.setNavigatorObject(focusedObj)
		api.setReviewPosition(tIAtCaret)
		# Translators: Reported when attempting to move the navigator object to focus.
		speech.speakMessage(_("Move to focus"))
		speech.speakObject(api.getNavigatorObject(), reason=controlTypes.OutputReason.FOCUS)

	@script(
		description=_(
			# Translators: Input help mode message for move focus to current navigator object command.
			"Pressed once sets the keyboard focus to the navigator object, "
			"pressed twice sets the system caret to the position of the review cursor"
		),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+shift+numpadMinus", "kb(laptop):NVDA+shift+backspace")
	)
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
			speech.speakTextInfo(info, reason=controlTypes.OutputReason.CARET)

	@script(
		# Translators: Input help mode message for move to parent object command.
		description=_("Moves the navigator object to the object containing it"),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+numpad8", "kb(laptop):NVDA+shift+upArrow", "ts(object):flickup")
	)
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
			speech.speakObject(curObject, reason=controlTypes.OutputReason.FOCUS)
		else:
			# Translators: Reported when there is no containing (parent) object such as when focused on desktop.
			ui.reviewMessage(_("No containing object"))

	@script(
		# Translators: Input help mode message for move to next object command.
		description=_("Moves the navigator object to the next object"),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+numpad6", "kb(laptop):NVDA+shift+rightArrow", "ts(object):2finger_flickright")
	)
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
			speech.speakObject(curObject, reason=controlTypes.OutputReason.FOCUS)
		else:
			# Translators: Reported when there is no next object (current object is the last object).
			ui.reviewMessage(_("No next"))

	@script(
		# Translators: Input help mode message for move to previous object command.
		description=_("Moves the navigator object to the previous object"),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+numpad4", "kb(laptop):NVDA+shift+leftArrow", "ts(object):2finger_flickleft")
	)
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
			speech.speakObject(curObject, reason=controlTypes.OutputReason.FOCUS)
		else:
			# Translators: Reported when there is no previous object (current object is the first object).
			ui.reviewMessage(_("No previous"))

	@script(
		# Translators: Input help mode message for move to first child object command.
		description=_("Moves the navigator object to the first object inside it"),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+numpad2", "kb(laptop):NVDA+shift+downArrow", "ts(object):flickdown")
	)
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
			speech.speakObject(curObject, reason=controlTypes.OutputReason.FOCUS)
		else:
			# Translators: Reported when there is no contained (first child) object such as inside a document.
			ui.reviewMessage(_("No objects inside"))

	@script(
		description=_(
			# Translators: Input help mode message for activate current object command.
			"Performs the default action on the current navigator object "
			"(example: presses it if it is a button)."
		),
		category=SCRCAT_OBJECTNAVIGATION,
		gestures=("kb:NVDA+numpadEnter", "kb(laptop):NVDA+enter", "ts:double_tap")
	)
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

	@script(
		# Translators: Input help mode message for move review cursor to top line command.
		description=_("Moves the review cursor to the top line of the current navigator object and speaks it"),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad7", "kb(laptop):NVDA+control+home")
	)
	def script_review_top(self,gesture):
		info=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_FIRST)
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)

	@script(
		# Translators: Input help mode message for move review cursor to previous line command.
		description=_("Moves the review cursor to the previous line of the current navigator object and speaks it"),
		resumeSayAllMode=sayAll.CURSOR.REVIEW,
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad7", "kb(laptop):NVDA+upArrow", "ts(text):flickUp")
	)
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
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)

	@script(
		description=_(
			# Translators: Input help mode message for read current line under review cursor command.
			"Reports the line of the current navigator object where the review cursor is situated. "
			"If this key is pressed twice, the current line will be spelled. "
			"Pressing three times will spell the line using character descriptions."
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad8", "kb(laptop):NVDA+shift+.")
	)
	def script_review_currentLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		# Explicitly tether here
		braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
		else:
			speech.spellTextInfo(info,useCharacterDescriptions=scriptCount>1)

	@script(
		# Translators: Input help mode message for move review cursor to next line command.
		description=_("Moves the review cursor to the next line of the current navigator object and speaks it"),
		resumeSayAllMode=sayAll.CURSOR.REVIEW,
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad9", "kb(laptop):NVDA+downArrow", "ts(text):flickDown")
	)
	def script_review_nextLine(self, gesture):
		origInfo = api.getReviewPosition().copy()
		origInfo.collapse()
		info = origInfo.copy()
		res = info.move(textInfos.UNIT_LINE, 1)
		newLine = info.copy()
		newLine.expand(textInfos.UNIT_LINE)
		# #12808: Some implementations of move forward by one line may succeed one more time than expected,
		# landing on the exclusive end of the document.
		# Therefore, verify that expanding after the move does result in being on a new line,
		# i.e. the new line starts after the original review cursor position.
		if res == 0 or newLine.start <= origInfo.start:
			# Translators: a message reported when review cursor is at the bottom line of the current navigator object.
			ui.reviewMessage(_("Bottom"))
		else:
			api.setReviewPosition(info)
		speech.speakTextInfo(newLine, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)

	@script(
		# Translators: Input help mode message for move review cursor to bottom line command.
		description=_("Moves the review cursor to the bottom line of the current navigator object and speaks it"),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad9", "kb(laptop):NVDA+control+end")
	)
	def script_review_bottom(self,gesture):
		info=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_LAST)
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)

	@script(
		# Translators: Input help mode message for move review cursor to previous word command.
		description=_("Moves the review cursor to the previous word of the current navigator object and speaks it"),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad4", "kb(laptop):NVDA+control+leftArrow", "ts(text):2finger_flickLeft")
	)
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
		speech.speakTextInfo(info, reason=controlTypes.OutputReason.CARET, unit=textInfos.UNIT_WORD)

	@script(
		description=_(
			# Translators: Input help mode message for report current word under review cursor command.
			"Speaks the word of the current navigator object where the review cursor is situated. "
			"Pressing twice spells the word. "
			"Pressing three times spells the word using character descriptions"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad5", "kb(laptop):NVDA+control+.", "ts(text):hoverUp")
	)
	def script_review_currentWord(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_WORD)
		# Explicitly tether here
		braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info, reason=controlTypes.OutputReason.CARET, unit=textInfos.UNIT_WORD)
		else:
			speech.spellTextInfo(info,useCharacterDescriptions=scriptCount>1)

	@script(
		# Translators: Input help mode message for move review cursor to next word command.
		description=_("Moves the review cursor to the next word of the current navigator object and speaks it"),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad6", "kb(laptop):NVDA+control+rightArrow", "ts(text):2finger_flickRight")
	)
	def script_review_nextWord(self, gesture):
		origInfo = api.getReviewPosition().copy()
		origInfo.collapse()
		info = origInfo.copy()
		res = info.move(textInfos.UNIT_WORD, 1)
		newWord = info.copy()
		newWord.expand(textInfos.UNIT_WORD)
		# #12808: Some implementations of move forward by one word may succeed one more time than expected,
		# landing on the exclusive end of the document.
		# Therefore, verify that expanding after the move does result in being on a new word,
		# i.e. the new word starts after the original review cursor position.
		if res == 0 or newWord.start <= origInfo.start:
			# Translators: a message reported when review cursor is at the bottom line of the current navigator object.
			ui.reviewMessage(_("Bottom"))
		else:
			api.setReviewPosition(info)
		speech.speakTextInfo(newWord, unit=textInfos.UNIT_WORD, reason=controlTypes.OutputReason.CARET)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to start of current line command.
			"Moves the review cursor to the first character of the line "
			"where it is situated in the current navigator object and speaks it"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad1", "kb(laptop):NVDA+home")
	)
	def script_review_startOfLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to previous character command.
			"Moves the review cursor to the previous character of the current navigator object and speaks it"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad1", "kb(laptop):NVDA+leftArrow", "ts(text):flickLeft")
	)
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
			speech.speakTextInfo(reviewInfo, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)
		else:
			api.setReviewPosition(charInfo)
			charInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(charInfo, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)

	@script(
		description=_(
			# Translators: Input help mode message for report current character under review cursor command.
			"Reports the character of the current navigator object where the review cursor is situated. "
			"Pressing twice reports a description or example of that character. "
			"Pressing three times reports the numeric value of the character in decimal and hexadecimal"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad2", "kb(laptop):NVDA+.")
	)
	def script_review_currentCharacter(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_CHARACTER)
		# Explicitly tether here
		braille.handler.setTether(braille.handler.TETHER_REVIEW, auto=True)
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)
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
				speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to next character command.
			"Moves the review cursor to the next character of the current navigator object and speaks it"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad3", "kb(laptop):NVDA+rightArrow", "ts(text):flickRight")
	)
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
			speech.speakTextInfo(reviewInfo, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)
		else:
			api.setReviewPosition(charInfo)
			charInfo.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(charInfo, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to end of current line command.
			"Moves the review cursor to the last character of the line "
			"where it is situated in the current navigator object and speaks it"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad3", "kb(laptop):NVDA+end")
	)
	def script_review_endOfLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse(end=True)
		info.move(textInfos.UNIT_CHARACTER,-1)
		api.setReviewPosition(info)
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)

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
		category=SCRCAT_TEXTREVIEW
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

	@script(
		description=_(
			# Translators: Input help mode message for toggle speech mode command.
			"Toggles between the speech modes of off, beep and talk. "
			"When set to off NVDA will not speak anything. "
			"If beeps then NVDA will simply beep each time it its supposed to speak something. "
			"If talk then NVDA will just speak normally."
		),
		category=SCRCAT_SPEECH,
		gesture="kb:NVDA+s"
	)
	def script_speechMode(self,gesture):
		curMode = speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.talk)
		newMode=(curMode+1)%3
		if newMode == speech.SpeechMode.off:
			# Translators: A speech mode which disables speech output.
			name=_("Speech mode off")
		elif newMode == speech.SpeechMode.beeps:
			# Translators: A speech mode which will cause NVDA to beep instead of speaking.
			name=_("Speech mode beeps")
		elif newMode == speech.SpeechMode.talk:
			# Translators: The normal speech mode; i.e. NVDA will talk as normal.
			name=_("Speech mode talk")
		speech.cancelSpeech()
		ui.message(name)
		speech.setSpeechMode(newMode)

	@script(
		description=_(
			# Translators: Input help mode message for move to next document with focus command,
			# mostly used in web browsing to move from embedded object to the webpage document.
			"Moves the focus out of the current embedded object and into the document that contains it"
		),
		category=SCRCAT_FOCUS,
		gesture="kb:NVDA+control+space"
	)
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
			# We must use core.callLater rather than wx.CallLater to ensure that the callback runs within NVDA's core pump.
			# If it didn't, and it directly or indirectly called wx.Yield, it could start executing NVDA's core pump from within the yield, causing recursion.
			core.callLater(50,eventHandler.executeEvent,"gainFocus",parent.treeInterceptor.rootNVDAObject)

	@script(
		description=_(
			# Translators: Input help mode message for toggle focus and browse mode command
			# in web browsing and other situations.
			"Toggles between browse mode and focus mode. "
			"When in focus mode, keys will pass straight through to the application, "
			"allowing you to interact directly with a control. "
			"When in browse mode, you can navigate the document with the cursor, quick navigation keys, etc."
		),
		category=inputCore.SCRCAT_BROWSEMODE,
		gesture="kb:NVDA+space"
	)
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

	@script(
		# Translators: Input help mode message for quit NVDA command.
		description=_("Quits NVDA!"),
		gesture="kb:NVDA+q"
	)
	def script_quit(self,gesture):
		wx.CallAfter(gui.mainFrame.onExitCommand, None)

	@script(
		# Translators: Input help mode message for restart NVDA command.
		description=_("Restarts NVDA!")
	)
	def script_restart(self,gesture):
		core.restart()

	@script(
		# Translators: Input help mode message for show NVDA menu command.
		description=_("Shows the NVDA menu"),
		gestures=("kb:NVDA+n", "ts:2finger_double_tap")
	)
	def script_showGui(self,gesture):
		gui.showGui()

	@script(
		description=_(
			# Translators: Input help mode message for say all in review cursor command.
			"Reads from the review cursor up to the end of the current text,"
			" moving the review cursor as it goes"
		),
		category=SCRCAT_TEXTREVIEW,
		gestures=("kb:numpadPlus", "kb(laptop):NVDA+shift+a", "ts(text):3finger_flickDown")
	)
	def script_review_sayAll(self,gesture):
		sayAll.SayAllHandler.readText(sayAll.CURSOR.REVIEW)

	@script(
		# Translators: Input help mode message for say all with system caret command.
		description=_("Reads from the system caret up to the end of the text, moving the caret as it goes"),
		category=SCRCAT_SYSTEMCARET,
		gestures=("kb(desktop):NVDA+downArrow", "kb(laptop):NVDA+a")
	)
	def script_sayAll(self,gesture):
		sayAll.SayAllHandler.readText(sayAll.CURSOR.CARET)

	def _reportFormattingHelper(self, info, browseable=False):
		# Report all formatting-related changes regardless of user settings
		# when explicitly requested.
		if info is None:
			return
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

	@staticmethod
	def _getTIAtCaret(
			fallbackToPOSITION_FIRST: bool = False,
			reportFailure: bool = True
	) -> Optional[textInfos.TextInfo]:
		# Returns text info at the caret position if there is a caret in the current control, None otherwise.
		# Note that if there is no caret this fact is announced in speech and braille
		# unless reportFailure is set to C{False}
		obj = api.getFocusObject()
		treeInterceptor = obj.treeInterceptor
		if(
			isinstance(treeInterceptor, treeInterceptorHandler.DocumentTreeInterceptor)
			and not treeInterceptor.passThrough
		):
			obj = treeInterceptor
		try:
			return obj.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			if fallbackToPOSITION_FIRST:
				return obj.makeTextInfo(textInfos.POSITION_FIRST)
			else:
				if reportFailure:
					# Translators: Reported when there is no caret.
					ui.message(_("No caret"))

	@script(
		# Translators: Input help mode message for report formatting command.
		description=_("Reports formatting info for the current review cursor position."),
		category=SCRCAT_TEXTREVIEW
	)
	def script_reportFormattingAtReview(self, gesture):
		self._reportFormattingHelper(api.getReviewPosition(), False)

	@script(
		# Translators: Input help mode message for show formatting at review cursor command.
		description=_("Presents, in browse mode, formatting info for the current review cursor position."),
		category=SCRCAT_TEXTREVIEW
	)
	def script_showFormattingAtReview(self, gesture):
		self._reportFormattingHelper(api.getReviewPosition(), True)

	@script(
		description=_(
			# Translators: Input help mode message for report formatting command.
			"Reports formatting info for the current review cursor position."
			" If pressed twice, presents the information in browse mode"
		),
		category=SCRCAT_TEXTREVIEW,
		gesture="kb:NVDA+shift+f"
	)
	def script_reportFormatting(self, gesture):
		repeats = scriptHandler.getLastScriptRepeatCount()
		if repeats == 0:
			self.script_reportFormattingAtReview(gesture)
		elif repeats == 1:
			self.script_showFormattingAtReview(gesture)

	@script(
		# Translators: Input help mode message for report formatting at caret command.
		description=_("Reports formatting info for the text under the caret."),
		category=SCRCAT_SYSTEMCARET
	)
	def script_reportFormattingAtCaret(self, gesture):
		self._reportFormattingHelper(self._getTIAtCaret(True), False)

	@script(
		# Translators: Input help mode message for show formatting at caret position command.
		description=_("Presents, in browse mode, formatting info for the text under the caret."),
		category=SCRCAT_SYSTEMCARET
	)
	def script_showFormattingAtCaret(self, gesture):
		self._reportFormattingHelper(self._getTIAtCaret(True), True)

	@script(
		description=_(
			# Translators: Input help mode message for report formatting at caret command.
			"Reports formatting info for the text under the caret."
			" If pressed twice, presents the information in browse mode"
		),
		category=SCRCAT_SYSTEMCARET,
		gesture="kb:NVDA+f"
	)
	def script_reportOrShowFormattingAtCaret(self, gesture):
		repeats = scriptHandler.getLastScriptRepeatCount()
		if repeats == 0:
			self.script_reportFormattingAtCaret(gesture)
		elif repeats == 1:
			self.script_showFormattingAtCaret(gesture)

	@script(
		gesture="kb:NVDA+d",
		description=_(
			# Translators: the description for the reportDetailsSummary script.
			"Report summary of any annotation details at the system caret."
		),
		category=SCRCAT_SYSTEMCARET,
	)
	def script_reportDetailsSummary(self, gesture):
		"""Report the annotation details summary for the single character under the caret or the object with
		system focus.
		@note: It is tempting to try to report any annotation details that exists in the range formed by prior
			and current location. This would be a new paradigm in NVDA, and may feel natural when moving by line
			to be able to more quickly have the 'details' reported. However, there may be more than one 'details
			relation' in that range, and we don't yet have a way for the user to select which one to report.
			For now, we minimise this risk by only reporting details at the current location.
		"""
		log.debug("Report annotation details summary at current location.")
		try:
			# Common cases use Caret Position: vbuf available or object supports text range
			# Eg editable text, or regular web content
			# Firefox and Chromium support this even in a button within a role=application.
			caret: textInfos.TextInfo = api.getCaretPosition()
		except RuntimeError:
			log.debugWarning("Unable to get the caret position.", exc_info=True)
			return
		caret.expand(textInfos.UNIT_CHARACTER)
		nvdaObject: NVDAObject = caret.NVDAObjectAtStart
		if config.conf["debugLog"]["annotations"]:
			log.debug(f"Trying with nvdaObject : {nvdaObject}")

		annotation: Optional[str] = nvdaObject.detailsSummary
		if annotation:
			log.debug("NVDAObjectAtStart of caret has details.")
		elif api.getFocusObject():
			# If fetching from the caret position fails, try via the focus object
			# This case is to support where there is no virtual buffer or text interface and a caret position can
			# not be fetched.
			# There may still be an object with focus that has details.
			# There isn't a known test case for this, however there isn't a known downside to attempt this.
			focus = api.getFocusObject()
			if config.conf["debugLog"]["annotations"]:
				log.debug(f"Trying focus object: {focus}")
			annotation = focus.detailsSummary
			if annotation:
				if config.conf["debugLog"]["annotations"]:
					log.debug("focus object has details, able to proceed")

		if not annotation:
			if config.conf["debugLog"]["annotations"]:
				log.debug("no details annotation found")
			# Translators: message given when there is no annotation details for the reportDetailsSummary script.
			ui.message(_("No additional details"))
			return

		ui.message(annotation)
		return

	@script(
		# Translators: Input help mode message for report current focus command.
		description=_("Reports the object with focus. If pressed twice, spells the information"),
		category=SCRCAT_FOCUS,
		gesture="kb:NVDA+tab"
	)
	def script_reportCurrentFocus(self,gesture):
		focusObject=api.getFocusObject()
		if isinstance(focusObject,NVDAObject):
			if scriptHandler.getLastScriptRepeatCount()==0:
				speech.speakObject(focusObject, reason=controlTypes.OutputReason.QUERY)
			else:
				speech.speakSpelling(focusObject.name)
		else:
			ui.message(_("No focus"))

	@staticmethod
	def _getStatusBarText(setReviewCursor: bool = False) -> Optional[str]:
		"""Returns text of the current status bar and optionally sets review cursor to it.
		If no status bar has been found `None` is returned and this fact is announced in speech and braille.
		"""
		obj = api.getStatusBar()
		found = False
		if obj:
			text = api.getStatusBarText(obj)
			if setReviewCursor:
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
				if setReviewCursor:
					api.setReviewPosition(info)
				found = True
		if not found:
			# Translators: Reported when there is no status line for the current program or window.
			ui.message(_("No status line found"))
			return None
		return text

	@script(
		description=_(
			# Translators: Input help mode message for command which reads content of the status bar.
			"Reads the current application status bar."
		),
		category=SCRCAT_FOCUS,
	)
	def script_readStatusLine(self, gesture):
		text = self._getStatusBarText()
		if text is None:
			return
		if not text.strip():
			# Translators: Reported when status line exist, but is empty.
			ui.message(_("no status bar information"))
		else:
			ui.message(text)

	@script(
		description=_(
			# Translators: Input help mode message for command which spells content of the status bar.
			"Spells the current application status bar."
		),
		category=SCRCAT_FOCUS,
	)
	def script_spellStatusLine(self, gesture):
		text = self._getStatusBarText()
		if text is None:
			return
		if not text.strip():
			# Translators: Reported when status line exist, but is empty.
			ui.message(_("no status bar information"))
		else:
			speech.speakSpelling(text)

	@script(
		description=_(
			# Translators: Input help mode message for command which copies status bar content to the clipboard.
			"Copies content of the status bar  of current application to the clipboard."
		),
		category=SCRCAT_FOCUS,
	)
	def script_copyStatusLine(self, gesture):
		text = self._getStatusBarText()
		if text is None:
			return
		if not text.strip():
			# Translators: Reported when user attempts to copy content of the empty status line.
			ui.message(_("Unable to copy status bar content to clipboard"))
		else:
			api.copyToClip(text, notify=True)

	@script(
		description=_(
			# Translators: Input help mode message for Command which moves review cursor to the status bar.
			"Reads the current application status bar and moves navigator object into it."
		),
		category=SCRCAT_OBJECTNAVIGATION,
	)
	def script_reviewCursorToStatusLine(self, gesture):
		text = self._getStatusBarText(setReviewCursor=True)
		if text is None:
			return
		if not text.strip():
			# Translators: Reported when status line exist, but is empty.
			ui.message(_("no status bar information"))
		else:
			ui.message(text)

	@script(
		description=_(
			# Translators: Input help mode message for report status line text command.
			"Reads the current application status bar. "
			"If pressed twice, spells the information. "
			"If pressed three times, copies the status bar to the clipboard"
		),
		category=SCRCAT_FOCUS,
		gestures=("kb(desktop):NVDA+end", "kb(laptop):NVDA+shift+end")
	)
	def script_reportStatusLine(self, gesture):
		text = self._getStatusBarText()
		if text is None:
			return
		repeats = scriptHandler.getLastScriptRepeatCount()
		if repeats == 0:
			self.script_readStatusLine(gesture)
		elif repeats == 1:
			self.script_spellStatusLine(gesture)
		else:
			self.script_copyStatusLine(gesture)

	@script(
		# Translators: Input help mode message for toggle mouse tracking command.
		description=_("Toggles the reporting of information as the mouse moves"),
		category=SCRCAT_MOUSE,
		gesture="kb:NVDA+m"
	)
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

	@script(
		# Translators: Input help mode message for toggle mouse text unit resolution command.
		description=_("Toggles how much text will be spoken when the mouse moves"),
		category=SCRCAT_MOUSE
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for report title bar command.
			"Reports the title of the current application or foreground window. "
			"If pressed twice, spells the title. "
			"If pressed three times, copies the title to the clipboard"
		),
		category=SCRCAT_FOCUS,
		gesture="kb:NVDA+t"
	)
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
			api.copyToClip(title, notify=True)

	@script(
		# Translators: Input help mode message for read foreground object command (usually the foreground window).
		description=_("Reads all controls in the active window"),
		category=SCRCAT_FOCUS,
		gesture="kb:NVDA+b"
	)
	def script_speakForeground(self,gesture):
		obj=api.getForegroundObject()
		if obj:
			sayAll.SayAllHandler.readObjects(obj)

	@script(
		gesture="kb(desktop):NVDA+control+f2"
	)
	def script_test_navigatorDisplayModelText(self,gesture):
		obj=api.getNavigatorObject()
		text=obj.displayText
		speech.speakMessage(text)
		log.info(text)

	@script(
		description=_(
			# Translators: GUI development tool, to get information about the components used in the NVDA GUI
			"Opens the WX GUI inspection tool. Used to get more information about the state of GUI components."
		),
		category=SCRCAT_TOOLS
	)
	@gui.blockAction.when(gui.blockAction.Context.SECURE_MODE)
	def script_startWxInspectionTool(self, gesture):
		import wx.lib.inspection
		wx.lib.inspection.InspectionTool().Show()

	@script(
		description=_(
			# Translators: Input help mode message for developer info for current navigator object command,
			# used by developers to examine technical info on navigator object.
			# This command also serves as a shortcut to open NVDA log viewer.
			"Logs information about the current navigator object which is useful to developers "
			"and activates the log viewer so the information can be examined."
		),
		category=SCRCAT_TOOLS,
		gesture="kb:NVDA+f1"
	)
	@gui.blockAction.when(gui.blockAction.Context.SECURE_MODE)
	def script_navigatorObject_devInfo(self,gesture):
		obj=api.getNavigatorObject()
		if hasattr(obj, "devInfo"):
			log.info("Developer info for navigator object:\n%s" % "\n".join(obj.devInfo), activateLogViewer=True)
		else:
			log.info("No developer info for navigator object", activateLogViewer=True)

	@script(
		description=_(
			# Translators: Input help mode message for a command to delimit then
			# copy a fragment of the log to clipboard
			"Mark the current end of the log as the start of the fragment to be"
			" copied to clipboard by pressing again."
		),
		category=SCRCAT_TOOLS,
		gesture="kb:NVDA+control+shift+f1"
	)
	@gui.blockAction.when(gui.blockAction.Context.SECURE_MODE)
	def script_log_markStartThenCopy(self, gesture):
		if log.fragmentStart is None:
			if log.markFragmentStart():
				# Translators: Message when marking the start of a fragment of the log file for later copy
				# to clipboard
				ui.message(_("Log fragment start position marked, press again to copy to clipboard"))
			else:
				# Translators: Message when failed to mark the start of a
				# fragment of the log file for later copy to clipboard
				ui.message(_("Unable to mark log position"))
			return
		text = log.getFragment()
		if not text:
			# Translators: Message when attempting to copy an empty fragment of the log file
			ui.message(_("No new log entry to copy"))
			return
		if api.copyToClip(text):
			# Translators: Message when a fragment of the log file has been
			# copied to clipboard
			ui.message(_("Log fragment copied to clipboard"))
		else:
			# Translators: Presented when unable to copy to the clipboard because of an error.
			ui.message(_("Unable to copy"))

	@script(
		# Translators: Input help mode message for Open user configuration directory command.
		description=_("Opens NVDA configuration directory for the current user."),
		category=SCRCAT_TOOLS
	)
	@gui.blockAction.when(gui.blockAction.Context.SECURE_MODE)
	def script_openUserConfigurationDirectory(self, gesture):
		import systemUtils
		systemUtils.openUserConfigurationDirectory()

	@script(
		description=_(
			# Translators: Input help mode message for toggle progress bar output command.
			"Toggles between beeps, speech, beeps and speech, and off, for reporting progress bar updates"
		),
		category=SCRCAT_SPEECH,
		gesture="kb:NVDA+u"
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for toggle dynamic content changes command.
			"Toggles on and off the reporting of dynamic content changes, "
			"such as new text in dos console windows"
		),
		category=SCRCAT_SPEECH,
		gesture="kb:NVDA+5"
	)
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

	@script(
		# Translators: Input help mode message for toggle caret moves review cursor command.
		description=_("Toggles on and off the movement of the review cursor due to the caret moving."),
		category=SCRCAT_TEXTREVIEW,
		gesture="kb:NVDA+6"
	)
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

	@script(
		# Translators: Input help mode message for toggle focus moves navigator object command.
		description=_("Toggles on and off the movement of the navigator object due to focus changes"),
		category=SCRCAT_OBJECTNAVIGATION,
		gesture="kb:NVDA+7"
	)
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

	@script(
		# Translators: Input help mode message for toggle auto focus focusable elements command.
		description=_("Toggles on and off automatic movement of the system focus due to browse mode commands"),
		category=inputCore.SCRCAT_BROWSEMODE,
		gesture="kb:NVDA+8"
	)
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

	# added by Rui Batista<ruiandrebatista@gmail.com> to implement a battery status script
	@script(
		# Translators: Input help mode message for report battery status command.
		description=_("Reports battery status and time remaining if AC is not plugged in"),
		category=SCRCAT_SYSTEM,
		gesture="kb:NVDA+shift+b"
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for pass next key through command.
			"The next key that is pressed will not be handled at all by NVDA, "
			"it will be passed directly through to Windows."
		),
		category=SCRCAT_INPUT,
		gesture="kb:NVDA+f2"
	)
	def script_passNextKeyThrough(self,gesture):
		keyboardHandler.passNextKeyThrough()
		# Translators: Spoken to indicate that the next key press will be sent straight to the current program as though NVDA is not running.
		ui.message(_("Pass next key through"))

	@script(
		description=_(
			# Translators: Input help mode message for report current program name and app module name command.
			"Speaks the filename of the active application along with the name of the currently loaded appModule"
		),
		category=SCRCAT_TOOLS,
		gesture="kb:NVDA+control+f1"
	)
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

	@script(
		# Translators: Input help mode message for go to general settings command.
		description=_("Shows NVDA's general settings"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+g"
	)
	def script_activateGeneralSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onGeneralSettingsCommand, None)

	@script(
		# Translators: Input help mode message for go to select synthesizer command.
		description=_("Shows the NVDA synthesizer selection dialog"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+s"
	)
	def script_activateSynthesizerDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSelectSynthesizerCommand, None)

	@script(
		# Translators: Input help mode message for go to speech settings command.
		description=_("Shows NVDA's speech settings"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+v"
	)
	def script_activateVoiceDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSpeechSettingsCommand, None)

	@script(
		# Translators: Input help mode message for go to select braille display command.
		description=_("Shows the NVDA braille display selection dialog"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+a"
	)
	def script_activateBrailleDisplayDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSelectBrailleDisplayCommand, None)

	@script(
		# Translators: Input help mode message for go to braille settings command.
		description=_("Shows NVDA's braille settings"),
		category=SCRCAT_CONFIG
	)
	def script_activateBrailleSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onBrailleSettingsCommand, None)

	@script(
		# Translators: Input help mode message for go to keyboard settings command.
		description=_("Shows NVDA's keyboard settings"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+k"
	)
	def script_activateKeyboardSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onKeyboardSettingsCommand, None)

	@script(
		# Translators: Input help mode message for go to mouse settings command.
		description=_("Shows NVDA's mouse settings"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+m"
	)
	def script_activateMouseSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onMouseSettingsCommand, None)

	@script(
		# Translators: Input help mode message for go to review cursor settings command.
		description=_("Shows NVDA's review cursor settings"),
		category=SCRCAT_CONFIG
	)
	def script_activateReviewCursorDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onReviewCursorCommand, None)

	@script(
		# Translators: Input help mode message for go to input composition settings command.
		description=_("Shows NVDA's input composition settings"),
		category=SCRCAT_CONFIG
	)
	def script_activateInputCompositionDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onInputCompositionCommand, None)

	@script(
		# Translators: Input help mode message for go to object presentation settings command.
		description=_("Shows NVDA's object presentation settings"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+o"
	)
	def script_activateObjectPresentationDialog(self, gesture):
		wx.CallAfter(gui.mainFrame. onObjectPresentationCommand, None)

	@script(
		# Translators: Input help mode message for go to browse mode settings command.
		description=_("Shows NVDA's browse mode settings"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+b"
	)
	def script_activateBrowseModeDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onBrowseModeCommand, None)

	@script(
		# Translators: Input help mode message for go to document formatting settings command.
		description=_("Shows NVDA's document formatting settings"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+d"
	)
	def script_activateDocumentFormattingDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onDocumentFormattingCommand, None)

	@script(
		# Translators: Input help mode message for opening default dictionary dialog.
		description=_("Shows the NVDA default dictionary dialog"),
		category=SCRCAT_CONFIG
	)
	def script_activateDefaultDictionaryDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onDefaultDictionaryCommand, None)

	@script(
		# Translators: Input help mode message for opening voice-specific dictionary dialog.
		description=_("Shows the NVDA voice-specific dictionary dialog"),
		category=SCRCAT_CONFIG
	)
	def script_activateVoiceDictionaryDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onVoiceDictionaryCommand, None)

	@script(
		# Translators: Input help mode message for opening temporary dictionary.
		description=_("Shows the NVDA temporary dictionary dialog"),
		category=SCRCAT_CONFIG
	)
	def script_activateTemporaryDictionaryDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onTemporaryDictionaryCommand, None)

	@script(
		# Translators: Input help mode message for go to punctuation/symbol pronunciation dialog.
		description=_("Shows the NVDA symbol pronunciation dialog"),
		category=SCRCAT_CONFIG
	)
	def script_activateSpeechSymbolsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSpeechSymbolsCommand, None)

	@script(
		# Translators: Input help mode message for go to input gestures dialog command.
		description=_("Shows the NVDA input gestures dialog"),
		category=SCRCAT_CONFIG
	)
	def script_activateInputGesturesDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onInputGesturesCommand, None)

	@script(
		# Translators: Input help mode message for the report current configuration profile command.
		description=_("Reports the name of the current NVDA configuration profile"),
		category=SCRCAT_CONFIG
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

	@script(
		# Translators: Input help mode message for save current configuration command.
		description=_("Saves the current NVDA configuration"),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+c"
	)
	def script_saveConfiguration(self,gesture):
		wx.CallAfter(gui.mainFrame.onSaveConfigurationCommand, None)

	@script(
		description=_(
			# Translators: Input help mode message for apply last saved or default settings command.
			"Pressing once reverts the current configuration to the most recently saved state."
			" Pressing three times resets to factory defaults."
		),
		category=SCRCAT_CONFIG,
		gesture="kb:NVDA+control+r"
	)
	def script_revertConfiguration(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			gui.mainFrame.onRevertToSavedConfigurationCommand(None)
		elif scriptCount==2:
			gui.mainFrame.onRevertToDefaultConfigurationCommand(None)

	@script(
		# Translators: Input help mode message for activate python console command.
		description=_("Activates the NVDA Python Console, primarily useful for development"),
		category=SCRCAT_TOOLS,
		gesture="kb:NVDA+control+z"
	)
	@gui.blockAction.when(
		gui.blockAction.Context.WINDOWS_STORE_VERSION,
		gui.blockAction.Context.SECURE_MODE
	)
	def script_activatePythonConsole(self,gesture):
		import pythonConsole
		if not pythonConsole.consoleUI:
			pythonConsole.initialize()
		# Take a snapshot of the vars before opening the window. Once the python console window is opened calls
		# to the 'api' module will refer to this new focus.
		pythonConsole.consoleUI.console.updateNamespaceSnapshotVars()
		pythonConsole.activate()

	@script(
		# Translators: Input help mode message for activate manage add-ons command.
		description=_("Activates the NVDA Add-ons Manager to install and uninstall add-on packages for NVDA"),
		category=SCRCAT_TOOLS
	)
	def script_activateAddonsManager(self,gesture):
		wx.CallAfter(gui.mainFrame.onAddonsManagerCommand, None)

	@script(
		description=_(
			# Translators: Input help mode message for toggle speech viewer command.
			"Toggles the NVDA Speech viewer, "
			"a floating window that allows you to view all the text that NVDA is currently speaking"
		),
		category=SCRCAT_TOOLS
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for toggle Braille viewer command.
			"Toggles the NVDA Braille viewer, a floating window that allows you to view braille output, "
			"and the text equivalent for each braille character"
		),
		category=SCRCAT_TOOLS
	)
	def script_toggleBrailleViewer(self, gesture):
		import brailleViewer
		if brailleViewer.isBrailleViewerActive():
			# Translators: The message announced when disabling braille viewer.
			state = _("Braille viewer disabled")
			brailleViewer.destroyBrailleViewer()
			gui.mainFrame.sysTrayIcon.menu_tools_toggleBrailleViewer.Check(False)
		else:
			# Translators: The message announced when enabling Braille viewer.
			state = _("Braille viewer enabled")
			brailleViewer.createBrailleViewerTool()
			gui.mainFrame.sysTrayIcon.menu_tools_toggleBrailleViewer.Check(True)
		ui.message(state)

	@script(
		# Translators: Input help mode message for toggle braille tether to command
		# (tethered means connected to or follows).
		description=_("Toggle tethering of braille between the focus and the review position"),
		category=SCRCAT_BRAILLE,
		gesture="kb:NVDA+control+t"
	)
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

	@script(
		# Translators: Input help mode message for toggle braille focus context presentation command.
		description=_("Toggle the way context information is presented in braille"),
		category=SCRCAT_BRAILLE
	)
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

	@script(
		# Translators: Input help mode message for toggle braille cursor command.
		description=_("Toggle the braille cursor on and off"),
		category=SCRCAT_BRAILLE
	)
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

	@script(
		# Translators: Input help mode message for cycle braille cursor shape command.
		description=_("Cycle through the braille cursor shapes"),
		category=SCRCAT_BRAILLE
	)
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

	@script(
		# Translators: Input help mode message for report clipboard text command.
		description=_("Reports the text on the Windows clipboard"),
		category=SCRCAT_SYSTEM,
		gesture="kb:NVDA+c"
	)
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

	@script(
		description=_(
			# Translators: Input help mode message for mark review cursor position for a select or copy command
			# (that is, marks the current review cursor position as the starting point for text to be selected).
			"Marks the current position of the review cursor as the start of text to be selected or copied"
		),
		category=SCRCAT_TEXTREVIEW,
		gesture="kb:NVDA+f9"
	)
	def script_review_markStartForCopy(self, gesture):
		reviewPos = api.getReviewPosition()
		# attach the marker to obj so that the marker is cleaned up when obj is cleaned up.
		reviewPos.obj._copyStartMarker = reviewPos.copy() # represents the start location
		reviewPos.obj._selectThenCopyRange = None # we may be part way through a select, reset the copy range.
		# Translators: Indicates start of review cursor text to be copied to clipboard.
		ui.message(_("Start marked"))

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to marked start position for a
			# select or copy command
			"Move the review cursor to the position marked as the start of text to be selected or copied"
		),
		category=SCRCAT_TEXTREVIEW,
		gesture="kb:NVDA+shift+F9"
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
		speech.speakTextInfo(startMarker, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)

	@script(
		description=_(
			# Translators: Input help mode message for the select then copy command.
			# The select then copy command first selects the review cursor text, then copies it to the clipboard.
			"If pressed once, the text from the previously set start marker up to and including the current "
			"position of the review cursor is selected. If pressed twice, the text is copied to the clipboard"
		),
		category=SCRCAT_TEXTREVIEW,
		gesture="kb:NVDA+f10"
	)
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
			copyMarker.copyToClipboard(notify=True)
			# on the second call always clean up the start marker
			api.getReviewPosition().obj._selectThenCopyRange = None
			api.getReviewPosition().obj._copyStartMarker = None
		return

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Scrolls the braille display back"),
		category=SCRCAT_BRAILLE,
		bypassInputHelp=True
	)
	def script_braille_scrollBack(self, gesture):
		braille.handler.scrollBack()

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Scrolls the braille display forward"),
		category=SCRCAT_BRAILLE,
		bypassInputHelp=True
	)
	def script_braille_scrollForward(self, gesture):
		braille.handler.scrollForward()

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Routes the cursor to or activates the object under this braille cell"),
		category=SCRCAT_BRAILLE
	)
	def script_braille_routeTo(self, gesture):
		braille.handler.routeTo(gesture.routingIndex)

	@script(
		# Translators: Input help mode message for Braille report formatting command.
		description=_("Reports formatting info for the text under this braille cell"),
		category=SCRCAT_BRAILLE
	)
	def script_braille_reportFormatting(self, gesture):
		info = braille.handler.getTextInfoForWindowPos(gesture.routingIndex)
		if info is None:
			# Translators: Reported when trying to obtain formatting information (such as font name, indentation and so on) but there is no formatting information for the text under cursor.
			ui.message(_("No formatting information"))
			return
		self._reportFormattingHelper(info, False)

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Moves the braille display to the previous line"),
		category=SCRCAT_BRAILLE
	)
	def script_braille_previousLine(self, gesture):
		if braille.handler.buffer.regions: 
			braille.handler.buffer.regions[-1].previousLine(start=True)

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Moves the braille display to the next line"),
		category=SCRCAT_BRAILLE
	)
	def script_braille_nextLine(self, gesture):
		if braille.handler.buffer.regions: 
			braille.handler.buffer.regions[-1].nextLine()

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Inputs braille dots via the braille keyboard"),
		category=SCRCAT_BRAILLE,
		gesture="bk:dots"
	)
	def script_braille_dots(self, gesture):
		brailleInput.handler.input(gesture.dots)

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Moves the braille display to the current focus"),
		category=SCRCAT_BRAILLE
	)
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

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Erases the last entered braille cell or character"),
		category=SCRCAT_BRAILLE,
		gesture="bk:dot7"
	)
	def script_braille_eraseLastCell(self, gesture):
		brailleInput.handler.eraseLastCell()

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Translates any braille input and presses the enter key"),
		category=SCRCAT_BRAILLE,
		gesture="bk:dot8"
	)
	def script_braille_enter(self, gesture):
		brailleInput.handler.enter()

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Translates any braille input"),
		category=SCRCAT_BRAILLE,
		gesture="bk:dot7+dot8"
	)
	def script_braille_translate(self, gesture):
		brailleInput.handler.translate()

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Virtually toggles the shift key to emulate a keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleShift(self, gesture):
		brailleInput.handler.toggleModifier("shift")

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Virtually toggles the control key to emulate a keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleControl(self, gesture):
		brailleInput.handler.toggleModifier("control")

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Virtually toggles the alt key to emulate a keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleAlt(self, gesture):
		brailleInput.handler.toggleModifier("alt")

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Virtually toggles the left windows key to emulate a keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleWindows(self, gesture):
		brailleInput.handler.toggleModifier("leftWindows")

	@script(
		# Translators: Input help mode message for a braille command.
		description=_("Virtually toggles the NVDA key to emulate a keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleNVDAKey(self, gesture):
		brailleInput.handler.toggleModifier("NVDA")

	@script(
		description=_(
			# Translators: Input help mode message for a braille command.
			"Virtually toggles the control and shift keys to emulate a "
			"keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleControlShift(self, gesture):
		brailleInput.handler.toggleModifiers(["control", "shift"])

	@script(
		description=_(
			# Translators: Input help mode message for a braille command.
			"Virtually toggles the alt and shift keys to emulate a "
			"keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleAltShift(self, gesture):
		brailleInput.handler.toggleModifiers(["alt", "shift"])

	@script(
		description=_(
			# Translators: Input help mode message for a braille command.
			"Virtually toggles the left windows and shift keys to emulate a "
			"keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleWindowsShift(self, gesture):
		brailleInput.handler.toggleModifiers(["leftWindows", "shift"])

	@script(
		description=_(
			# Translators: Input help mode message for a braille command.
			"Virtually toggles the NVDA and shift keys to emulate a "
			"keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleNVDAKeyShift(self, gesture):
		brailleInput.handler.toggleModifiers(["NVDA", "shift"])

	@script(
		description=_(
			# Translators: Input help mode message for a braille command.
			"Virtually toggles the control and alt keys to emulate a "
			"keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleControlAlt(self, gesture):
		brailleInput.handler.toggleModifiers(["control", "alt"])

	@script(
		description=_(
			# Translators: Input help mode message for a braille command.
			"Virtually toggles the control, alt, and shift keys to emulate a "
			"keyboard shortcut with braille input"),
		category=inputCore.SCRCAT_KBEMU,
		bypassInputHelp=True
	)
	def script_braille_toggleControlAltShift(self, gesture):
		brailleInput.handler.toggleModifiers(["control", "alt", "shift"])

	@script(
		description=_(
			# Translators: Input help mode message for reload plugins command.
			"Reloads app modules and global plugins without restarting NVDA, which can be Useful for developers"
		),
		category=SCRCAT_TOOLS,
		gesture="kb:NVDA+control+f3"
	)
	def script_reloadPlugins(self, gesture):
		import globalPluginHandler
		appModuleHandler.reloadAppModules()
		globalPluginHandler.reloadGlobalPlugins()
		NVDAObject.clearDynamicClassCache()
		# Translators: Presented when plugins (app modules and global plugins) are reloaded.
		ui.message(_("Plugins reloaded"))

	@script(
		# Translators: Input help mode message for a touchscreen gesture.
		description=_("Moves to the next object in a flattened view of the object navigation hierarchy"),
		category=SCRCAT_OBJECTNAVIGATION,
		gesture="ts(object):flickright"
	)
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
			speech.speakObject(newObject, reason=controlTypes.OutputReason.FOCUS)
		else:
			# Translators: a message when there is no next object when navigating
			ui.reviewMessage(_("No next"))

	@script(
		# Translators: Input help mode message for a touchscreen gesture.
		description=_("Moves to the previous object in a flattened view of the object navigation hierarchy"),
		category=SCRCAT_OBJECTNAVIGATION,
		gesture="ts(object):flickleft"
	)
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
			speech.speakObject(newObject, reason=controlTypes.OutputReason.FOCUS)
		else:
			# Translators: a message when there is no previous object when navigating
			ui.reviewMessage(_("No previous"))

	@script(
		# Translators: Describes a command.
		description=_("Toggles the support of touch interaction"),
		category=SCRCAT_TOUCH,
		gesture="kb:NVDA+control+alt+t"
	)
	def script_toggleTouchSupport(self, gesture):
		enabled = not bool(config.conf["touch"]["enabled"])
		try:
			touchHandler.setTouchSupport(enabled)
		except NotImplementedError:
			# Translators: Presented when attempting to toggle touch interaction support
			ui.message(_("Touch interaction not supported"))
			return
		# Set configuration upon success
		config.conf["touch"]["enabled"] = enabled
		if enabled:
			# Translators: Presented when support of touch interaction has been enabled
			ui.message(_("Touch interaction enabled"))
		else:
			# Translators: Presented when support of touch interaction has been disabled
			ui.message(_("Touch interaction disabled"))

	@script(
		# Translators: Input help mode message for a touchscreen gesture.
		description=_("Cycles between available touch modes"),
		category=SCRCAT_TOUCH,
		gesture="ts:3finger_tap"
	)
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

	@script(
		# Translators: Input help mode message for a touchscreen gesture.
		description=_("Reports the object and content directly under your finger"),
		category=SCRCAT_TOUCH,
		gestures=("ts:tap", "ts:hoverDown")
	)
	def script_touch_newExplore(self,gesture):
		touchHandler.handler.screenExplorer.moveTo(gesture.x,gesture.y,new=True)

	@script(
		description=_(
			# Translators: Input help mode message for a touchscreen gesture.
			"Reports the new object or content under your finger "
			"if different to where your finger was last"
		),
		category=SCRCAT_TOUCH,
		gesture="ts:hover"
	)
	def script_touch_explore(self,gesture):
		touchHandler.handler.screenExplorer.moveTo(gesture.x,gesture.y)

	@script(
		category=SCRCAT_TOUCH,
		gesture="ts:hoverUp"
	)
	def script_touch_hoverUp(self,gesture):
		#Specifically for touch typing with onscreen keyboard keys
		# #7309: by default, one must double-tap the touch key.
		# To restore old behavior, go to Touch Interaction dialog and change touch typing option.
		if config.conf["touch"]["touchTyping"]:
			obj=api.getNavigatorObject()
			import NVDAObjects.UIA
			if isinstance(obj,NVDAObjects.UIA.UIA) and obj.UIAElement.cachedClassName=="CRootKey":
				obj.doAction()

	@script(
		description=_(
			# Translators: Input help mode message for touch right click command.
			"Clicks the right mouse button at the current touch position. "
			"This is generally used to activate a context menu."
		),
		category=SCRCAT_TOUCH,
		gesture="ts:tapAndHold"
	)
	def script_touch_rightClick(self, gesture):
		obj = api.getNavigatorObject()
		# Ignore invisible or offscreen objects as they cannot even be navigated with touch gestures.
		if controlTypes.State.INVISIBLE in obj.states or controlTypes.State.OFFSCREEN in obj.states:
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

	@script(
		# Translators: Describes the command to open the Configuration Profiles dialog.
		description=_("Shows the NVDA Configuration Profiles dialog"),
		category=SCRCAT_CONFIG_PROFILES,
		gesture="kb:NVDA+control+p"
	)
	def script_activateConfigProfilesDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onConfigProfilesCommand, None)

	@script(
		description=_(
			# Translators: Input help mode message for toggle configuration profile triggers command.
			"Toggles disabling of all configuration profile triggers. "
			"Disabling remains in effect until NVDA is restarted"
		),
		category=SCRCAT_CONFIG
	)
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

	@script(
		# Translators: Describes a command.
		description=_("Begins interaction with math content"),
		gesture="kb:NVDA+alt+m"
	)
	def script_interactWithMath(self, gesture):
		import mathPres
		mathMl = mathPres.getMathMlFromTextInfo(api.getReviewPosition())
		if not mathMl:
			obj = api.getNavigatorObject()
			if obj.role == controlTypes.Role.MATH:
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

	@script(
		# Translators: Describes a command.
		description=_("Recognizes the content of the current navigator object with Windows OCR"),
		gesture="kb:NVDA+r"
	)
	def script_recognizeWithUwpOcr(self, gesture):
		if not winVersion.isUwpOcrAvailable():
			# Translators: Reported when Windows OCR is not available.
			ui.message(_("Windows OCR not available"))
			return
		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
		isScreenCurtainRunning = bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))
		if isScreenCurtainRunning:
			# Translators: Reported when screen curtain is enabled.
			ui.message(_("Please disable screen curtain before using Windows OCR."))
			return
		from contentRecog import uwpOcr, recogUi
		recog = uwpOcr.UwpOcr()
		recogUi.recognizeNavigatorObject(recog)

	_tempEnableScreenCurtain = True
	_waitingOnScreenCurtainWarningDialog: Optional[wx.Dialog] = None
	_toggleScreenCurtainMessage: Optional[str] = None
	@script(
		# Translators: Input help mode message for toggle report CLDR command.
		description=_("Toggles on and off the reporting of CLDR characters, such as emojis"),
		category=SCRCAT_SPEECH
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
				reason=controlTypes.OutputReason.FOCUS
			)
			speech.speakObject(
				api.getFocusObject(),
				reason=controlTypes.OutputReason.FOCUS
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
			if C{None}, the gestures are only removed for the current profile script.
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
