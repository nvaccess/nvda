# -*- coding: UTF-8 -*-
#globalCommands.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2015 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Rui Batista, Joseph Lee, Leonard de Ruijter

import time
import itertools
import tones
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
import ui
import braille
import brailleInput
import inputCore
import virtualBuffers
import characterProcessing
from baseObject import ScriptableObject

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
#: Script category for Braille commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_BRAILLE = _("Braille")
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
	script_toggleCurrentAppSleepMode.__doc__=_("Toggles  sleep mode on and off for  the active application.")
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
		if scriptHandler.getLastScriptRepeatCount()==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
		else:
			speech.speakSpelling(info.text)
	# Translators: Input help mode message for report current line command.
	script_reportCurrentLine.__doc__=_("Reports the current line under the application cursor. Pressing this key twice will spell the current line")
	script_reportCurrentLine.category=SCRCAT_SYSTEMCARET

	def script_leftMouseClick(self,gesture):
		# Translators: Reported when left mouse button is clicked.
		ui.message(_("left click"))
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
	# Translators: Input help mode message for left mouse click command.
	script_leftMouseClick.__doc__=_("Clicks the left mouse button once at the current mouse position")
	script_leftMouseClick.category=SCRCAT_MOUSE

	def script_rightMouseClick(self,gesture):
		# Translators: Reported when right mouse button is clicked.
		ui.message(_("right click"))
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,0,None,None)
	# Translators: Input help mode message for right mouse click command.
	script_rightMouseClick.__doc__=_("Clicks the right mouse button once at the current mouse position")
	script_rightMouseClick.category=SCRCAT_MOUSE

	def script_toggleLeftMouseButton(self,gesture):
		if winUser.getKeyState(winUser.VK_LBUTTON)&32768:
			# Translators: This is presented when the left mouse button lock is released (used for drag and drop).
			ui.message(_("left mouse button unlock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		else:
			# Translators: This is presented when the left mouse button is locked down (used for drag and drop).
			ui.message(_("left mouse button lock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
	# Translators: Input help mode message for left mouse lock/unlock toggle command.
	script_toggleLeftMouseButton.__doc__=_("Locks or unlocks the left mouse button")
	script_toggleLeftMouseButton.category=SCRCAT_MOUSE

	def script_toggleRightMouseButton(self,gesture):
		if winUser.getKeyState(winUser.VK_RBUTTON)&32768:
			# Translators: This is presented when the right mouse button lock is released (used for drag and drop).
			ui.message(_("right mouse button unlock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,0,None,None)
		else:
			# Translators: This is presented when the right mouse button is locked down (used for drag and drop).
			ui.message(_("right mouse button lock"))
			winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,0,None,None)
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
			speech.speakMessage(_("no selection"))
		else:
			speech.speakMessage(_("selected %s")%info.text)
	# Translators: Input help mode message for report current selection command.
	script_reportCurrentSelection.__doc__=_("Announces the current selection in edit controls and documents. If there is no selection it says so.")
	script_reportCurrentSelection.category=SCRCAT_SYSTEMCARET

	def script_dateTime(self,gesture):
		if scriptHandler.getLastScriptRepeatCount()==0:
			text=winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, None, None)
		else:
			text=winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, None, None)
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
		if config.conf["documentFormatting"]["reportLineIndentation"]:
			# Translators: The message announced when toggling the report line indentation document formatting setting.
			state = _("report line indentation off")
			config.conf["documentFormatting"]["reportLineIndentation"]=False
		else:
			# Translators: The message announced when toggling the report line indentation document formatting setting.
			state = _("report line indentation on")
			config.conf["documentFormatting"]["reportLineIndentation"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report line indentation command.
	script_toggleReportLineIndentation.__doc__=_("Toggles on and off the reporting of line indentation")
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
			state = _("report landmarks off")
			config.conf["documentFormatting"]["reportLandmarks"]=False
		else:
			# Translators: The message announced when toggling the report landmarks document formatting setting.
			state = _("report landmarks on")
			config.conf["documentFormatting"]["reportLandmarks"]=True
		ui.message(state)
	# Translators: Input help mode message for toggle report landmarks command.
	script_toggleReportLandmarks.__doc__=_("Toggles on and off the reporting of landmarks")
	script_toggleReportLandmarks.category=SCRCAT_DOCUMENTFORMATTING

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
		ui.message(_("symbol level %s") % name)
	# Translators: Input help mode message for cycle speech symbol level command.
	script_cycleSpeechSymbolLevel.__doc__=_("Cycles through speech symbol levels which determine what symbols are spoken")
	script_cycleSpeechSymbolLevel.category=SCRCAT_SPEECH

	def script_moveMouseToNavigatorObject(self,gesture):
		obj=api.getNavigatorObject() 
		try:
			p=api.getReviewPosition().pointAtStart
		except (NotImplementedError, LookupError):
			p=None
		if p:
			x=p.x
			y=p.y
		else:
			try:
				(left,top,width,height)=obj.location
			except:
				# Translators: Reported when the object has no location for the mouse to move to it.
				ui.message(_("object has no location"))
				return
			x=left+(width/2)
			y=top+(height/2)
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
			ui.message(label)
			pos=api.getReviewPosition().copy()
			pos.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(pos)
		else:
			# Translators: reported when there are no other available review modes for this object 
			ui.message(_("No next review mode"))
	# Translators: Script help message for next review mode command.
	script_reviewMode_next.__doc__=_("Switches to the next review mode (e.g. object, document or screen) and positions the review position at the point of the navigator object")
	script_reviewMode_next.category=SCRCAT_TEXTREVIEW

	def script_reviewMode_previous(self,gesture):
		label=review.nextMode(prev=True)
		if label:
			ui.message(label)
			pos=api.getReviewPosition().copy()
			pos.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(pos)
		else:
			# Translators: reported when there are no  other available review modes for this object 
			ui.message(_("No previous review mode"))
	# Translators: Script help message for previous review mode command.
	script_reviewMode_previous.__doc__=_("Switches to the previous review mode (e.g. object, document or screen) and positions the review position at the point of the navigator object") 
	script_reviewMode_previous.category=SCRCAT_TEXTREVIEW

	def script_navigatorObject_current(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			# Translators: Reported when the user tries to perform a command related to the navigator object
			# but there is no current navigator object.
			speech.speakMessage(_("no navigator object"))
			return
		if scriptHandler.getLastScriptRepeatCount()>=1:
			if curObject.TextInfo!=NVDAObjectTextInfo:
				textList=[]
				if curObject.name and isinstance(curObject.name, basestring) and not curObject.name.isspace():
					textList.append(curObject.name)
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
				textList=[prop for prop in (curObject.name, curObject.value) if prop and isinstance(prop, basestring) and not prop.isspace()]
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
	script_navigatorObject_current.__doc__=_("Reports the current navigator object. Pressing twice spells this information, and pressing three times Copies name and value of this  object to the clipboard")
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
		speech.speakMessage(_("move to focus"))
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
			speech.speakMessage(_("no focus"))
		if scriptHandler.getLastScriptRepeatCount()==0:
			# Translators: Reported when attempting to move focus to navigator object.
			ui.message(_("move focus"))
			obj.setFocus()
		else:
			review=api.getReviewPosition()
			try:
				review.updateCaret()
			except NotImplementedError:
				# Translators: Reported when trying to move caret to the position of the review cursor but there is no caret.
				ui.message(_("no caret"))
				return
			info=review.copy()
			info.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(info,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move focus to current navigator object command.
	script_navigatorObject_moveFocus.__doc__=_("Pressed once Sets the keyboard focus to the navigator object, pressed twice sets the system caret to the position of the review cursor")
	script_navigatorObject_moveFocus.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_parent(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simpleParent if simpleReviewMode else curObject.parent
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no containing (parent) object such as when focused on desktop.
			speech.speakMessage(_("No containing object"))
	# Translators: Input help mode message for move to parent object command.
	script_navigatorObject_parent.__doc__=_("Moves the navigator object to the object containing it")
	script_navigatorObject_parent.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_next(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simpleNext if simpleReviewMode else curObject.next
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no next object (current object is the last object).
			speech.speakMessage(_("No next"))
	# Translators: Input help mode message for move to next object command.
	script_navigatorObject_next.__doc__=_("Moves the navigator object to the next object")
	script_navigatorObject_next.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_previous(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simplePrevious if simpleReviewMode else curObject.previous
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no previous object (current object is the first object).
			speech.speakMessage(_("No previous"))
	# Translators: Input help mode message for move to previous object command.
	script_navigatorObject_previous.__doc__=_("Moves the navigator object to the previous object")
	script_navigatorObject_previous.category=SCRCAT_OBJECTNAVIGATION

	def script_navigatorObject_firstChild(self,gesture):
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObject):
			speech.speakMessage(_("no navigator object"))
			return
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		curObject=curObject.simpleFirstChild if simpleReviewMode else curObject.firstChild
		if curObject is not None:
			api.setNavigatorObject(curObject)
			speech.speakObject(curObject,reason=controlTypes.REASON_FOCUS)
		else:
			# Translators: Reported when there is no contained (first child) object such as inside a document.
			speech.speakMessage(_("No objects inside"))
	# Translators: Input help mode message for move to first child object command.
	script_navigatorObject_firstChild.__doc__=_("Moves the navigator object to the first object inside it")
	script_navigatorObject_firstChild.category=SCRCAT_OBJECTNAVIGATION

	def script_review_activate(self,gesture):
		# Translators: a message reported when the action at the position of the review cursor or navigator object is performed.
		actionName=_("activate")
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
		speech.speakMessage(_("top"))
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
			speech.speakMessage(_("top"))
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
			speech.speakMessage(_("bottom"))
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
		speech.speakMessage(_("bottom"))
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
			speech.speakMessage(_("top"))
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
			speech.speakMessage(_("bottom"))
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
		speech.speakMessage(_("left"))
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
			speech.speakMessage(_("left"))
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
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
		elif scriptCount==1:
			speech.spellTextInfo(info,useCharacterDescriptions=True)
		else:
			try:
				c = ord(info.text)
				speech.speakMessage("%d," % c)
				speech.speakSpelling(hex(c))
			except:
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
			speech.speakMessage(_("right"))
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
		speech.speakMessage(_("right"))
		speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER,reason=controlTypes.REASON_CARET)
	# Translators: Input help mode message for move review cursor to end of current line command.
	script_review_endOfLine.__doc__=_("Moves the review cursor to the last character of the line where it is situated in the current navigator object and speaks it")
	script_review_endOfLine.category=SCRCAT_TEXTREVIEW

	def script_speechMode(self,gesture):
		curMode=speech.speechMode
		speech.speechMode=speech.speechMode_talk
		newMode=(curMode+1)%3
		if newMode==speech.speechMode_off:
			# Translators: A speech mode which disables speech output.
			name=_("speech mode off")
		elif newMode==speech.speechMode_beeps:
			# Translators: A speech mode which will cause NVDA to beep instead of speaking.
			name=_("speech mode beeps")
		elif newMode==speech.speechMode_talk:
			# Translators: The normal speech mode; i.e. NVDA will talk as normal.
			name=_("speech mode talk")
		speech.cancelSpeech()
		ui.message(name)
		speech.speechMode=newMode
	# Translators: Input help mode message for toggle speech mode command.
	script_speechMode.__doc__=_("Toggles between the speech modes of off, beep and talk. When set to off NVDA will not speak anything. If beeps then NVDA will simply beep each time it its supposed to speak something. If talk then NVDA wil just speak normally.")
	script_speechMode.category=SCRCAT_SPEECH

	def script_moveToParentTreeInterceptor(self,gesture):
		obj=api.getFocusObject()
		parent=obj.parent
		#Move up parents untill  the tree interceptor of the parent is different to the tree interceptor of the object.
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
			wx.CallLater(50,eventHandler.executeEvent,"gainFocus",parent.treeInterceptor.rootNVDAObject)
	# Translators: Input help mode message for move to next document with focus command, mostly used in web browsing to move from embedded object to the webpage document.
	script_moveToParentTreeInterceptor.__doc__=_("Moves the focus to the next closest document that contains the focus")
	script_moveToParentTreeInterceptor.category=SCRCAT_FOCUS

	def script_toggleVirtualBufferPassThrough(self,gesture):
		focus = api.getFocusObject()
		vbuf = focus.treeInterceptor
		if not vbuf:
			# #2023: Search the focus and its ancestors for an object for which browse mode is optional.
			for obj in itertools.chain((api.getFocusObject(),), reversed(api.getFocusAncestors())):
				if obj.shouldCreateTreeInterceptor:
					continue
				try:
					obj.treeInterceptorClass
				except:
					continue
				break
			else:
				return
			# Force the tree interceptor to be created.
			obj.shouldCreateTreeInterceptor = True
			ti = treeInterceptorHandler.update(obj)
			if not ti:
				return
			if focus in ti:
				# Update the focus, as it will have cached that there is no tree interceptor.
				focus.treeInterceptor = ti
				# If we just happened to create a browse mode TreeInterceptor
				# Then ensure that browse mode is reported here. From the users point of view, browse mode was turned on.
				if isinstance(ti,browseMode.BrowseModeTreeInterceptor) and not ti.passThrough:
					browseMode.reportPassThrough(ti,False)
					braille.handler.handleGainFocus(ti)
			return

		if not isinstance(vbuf, browseMode.BrowseModeTreeInterceptor):
			return
		# Toggle browse mode pass-through.
		vbuf.passThrough = not vbuf.passThrough
		if isinstance(vbuf,browseMode.BrowseModeDocumentTreeInterceptor):
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

	def script_showGui(self,gesture):
		gui.showGui()
	# Translators: Input help mode message for show NVDA menu command.
	script_showGui.__doc__=_("Shows the NVDA menu")

	def script_review_sayAll(self,gesture):
		sayAllHandler.readText(sayAllHandler.CURSOR_REVIEW)
	# Translators: Input help mode message for say all in review cursor command.
	script_review_sayAll.__doc__ = _("reads from the review cursor  up to end of current text, moving the review cursor as it goes")
	script_review_sayAll.category=SCRCAT_TEXTREVIEW

	def script_sayAll(self,gesture):
		sayAllHandler.readText(sayAllHandler.CURSOR_CARET)
	# Translators: Input help mode message for say all with system caret command.
	script_sayAll.__doc__ = _("reads from the system caret up to the end of the text, moving the caret as it goes")
	script_sayAll.category=SCRCAT_SYSTEMCARET

	def script_reportFormatting(self,gesture):
		formatConfig={
			"detectFormatAfterCursor":False,
			"reportFontName":True,"reportFontSize":True,"reportFontAttributes":True,"reportColor":True,"reportRevisions":False,"reportEmphasis":False,
			"reportStyle":True,"reportAlignment":True,"reportSpellingErrors":True,
			"reportPage":False,"reportLineNumber":False,"reportParagraphIndentation":True,"reportTables":False,
			"reportLinks":False,"reportHeadings":False,"reportLists":False,
			"reportBlockQuotes":False,"reportComments":False,
		}
		textList=[]
		info=api.getReviewPosition()

		# First, fetch indentation.
		line=info.copy()
		line.expand(textInfos.UNIT_LINE)
		indentation,content=speech.splitTextIndentation(line.text)
		if indentation:
			textList.append(speech.getIndentationSpeech(indentation))
		
		info.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		for field in info.getTextWithFields(formatConfig):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				formatField.update(field.field)
		text=speech.getFormatFieldSpeech(formatField,formatConfig=formatConfig) if formatField else None
		if text:
			textList.append(text)

		if not textList:
			# Translators: Reported when trying to obtain formatting information (such as font name, indentation and so on) but there is no formatting information for the text under cursor.
			ui.message(_("No formatting information"))
			return

		ui.message(" ".join(textList))
	# Translators: Input help mode message for report formatting command.
	script_reportFormatting.__doc__ = _("Reports formatting info for the current review cursor position within a document")
	script_reportFormatting.category=SCRCAT_TEXTREVIEW

	def script_reportCurrentFocus(self,gesture):
		focusObject=api.getFocusObject()
		if isinstance(focusObject,NVDAObject):
			if scriptHandler.getLastScriptRepeatCount()==0:
				speech.speakObject(focusObject, reason=controlTypes.REASON_QUERY)
			else:
				speech.speakSpelling(focusObject.name)
		else:
			speech.speakMessage(_("no focus"))
	# Translators: Input help mode message for report current focus command.
	script_reportCurrentFocus.__doc__ = _("reports the object with focus. If pressed twice, spells the information")
	script_reportCurrentFocus.category=SCRCAT_FOCUS

	def script_reportStatusLine(self,gesture):
		obj = api.getStatusBar()
		found=False
		if obj:
			text = api.getStatusBarText(obj)
			api.setNavigatorObject(obj)
			found=True
		else:
			info=api.getForegroundObject().flatReviewPosition
			if info:
				info.expand(textInfos.UNIT_STORY)
				info.collapse(True)
				info.expand(textInfos.UNIT_LINE)
				text=info.text
				info.collapse()
				api.setReviewPosition(info)
				found=True
		if not found:
			# Translators: Reported when there is no status line for the current program or window.
			ui.message(_("No status line found"))
			return
		if scriptHandler.getLastScriptRepeatCount()==0:
			ui.message(text)
		else:
			speech.speakSpelling(text)
	# Translators: Input help mode message for report status line text command.
	script_reportStatusLine.__doc__ = _("reads the current application status bar and moves the navigator to it. If pressed twice, spells the information")
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

	def script_title(self,gesture):
		obj=api.getForegroundObject()
		title=obj.name
		if not isinstance(title,basestring) or not title or title.isspace():
			title=obj.appModule.appName  if obj.appModule else None
			if not isinstance(title,basestring) or not title or title.isspace():
				# Translators: Reported when there is no title text for current program or window.
				title=_("no title")
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
	script_speakForeground.__doc__ = _("speaks the current foreground object")
	script_speakForeground.category=SCRCAT_FOCUS

	def script_test_navigatorDisplayModelText(self,gesture):
		obj=api.getNavigatorObject()
		text=obj.displayText
		speech.speakMessage(text)
		log.info(text)

	def script_navigatorObject_devInfo(self,gesture):
		obj=api.getNavigatorObject()
		log.info("Developer info for navigator object:\n%s" % "\n".join(obj.devInfo), activateLogViewer=True)
	# Translators: Input help mode message for developer info for current navigator object command, used by developers to examine technical info on navigator object. This command also serves as a shortcut to open NVDA log viewer.
	script_navigatorObject_devInfo.__doc__ = _("Logs information about the current navigator object which is useful to developers and activates the log viewer so the information can be examined.")
	script_navigatorObject_devInfo.category=SCRCAT_TOOLS

	def script_toggleProgressBarOutput(self,gesture):
		outputMode=config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]
		if outputMode=="both":
			outputMode="off"
			# Translators: A mode where no progress bar updates are given.
			ui.message(_("no progress bar updates"))
		elif outputMode=="off":
			outputMode="speak"
			# Translators: A mode where progress bar updates will be spoken.
			ui.message(_("speak progress bar updates"))
		elif outputMode=="speak":
			outputMode="beep"
			# Translators: A mode where beeps will indicate progress bar updates (beeps rise in pitch as progress bar updates).
			ui.message(_("beep for progress bar updates"))
		else:
			outputMode="both"
			# Translators: A mode where both speech and beeps will indicate progress bar updates.
			ui.message(_("beep and speak progress bar updates"))
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
			ui.message(_("no system battery"))
			return
		# Translators: This is presented to inform the user of the current battery percentage.
		text = _("%d percent") % sps.BatteryLifePercent + " "
		# Translators: This is presented when AC power is connected such as when recharging a laptop battery.
		if sps.ACLineStatus & AC_ONLINE: text += _("AC power on")
		elif sps.BatteryLifeTime!=0xffffffff: 
			# Translators: This is the estimated remaining runtime of the laptop battery.
			text += _("{hours:d} hours and {minutes:d} minutes remaining") .format(hours=sps.BatteryLifeTime / 3600, minutes=(sps.BatteryLifeTime % 3600) / 60)
		ui.message(text)
	# Translators: Input help mode message for report battery status command.
	script_say_battery_status.__doc__ = _("reports battery status and time remaining if AC is not plugged in")
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
		appName=appModuleHandler.getAppNameFromProcessID(focus.processID,True)
		# Translators: Indicates the name of the current program (example output: Currently running application is explorer.exe).
		# Note that it does not give friendly name such as Windows Explorer; it presents the file name of the current application.
		# If there is an appModule for the current program, NVDA speaks the name of the module after presenting this message.
		message = _("Currently running application is %s") % appName
		mod=focus.appModule
		if isinstance(mod,appModuleHandler.AppModule) and type(mod)!=appModuleHandler.AppModule:
			# Translators: Indicates the name of the appModule for the current program (example output: and currently loaded module is explorer).
			# For example, the complete message for Windows explorer is: Currently running application is explorer.exe and currently loaded module is explorer.
			# This message will not be presented if there is no module for the current program.
			message += _(" and currently loaded module is %s") % mod.appModuleName.split(".")[0]
		ui.message(message)
	# Translators: Input help mode message for report current program name and app module name command.
	script_reportAppModuleInfo.__doc__ = _("Speaks the filename of the active application along with the name of the currently loaded appModule")
	script_reportAppModuleInfo.category=SCRCAT_TOOLS

	def script_activateGeneralSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onGeneralSettingsCommand, None)
	# Translators: Input help mode message for go to general settings dialog command.
	script_activateGeneralSettingsDialog.__doc__ = _("Shows the NVDA general settings dialog")
	script_activateGeneralSettingsDialog.category=SCRCAT_CONFIG

	def script_activateSynthesizerDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onSynthesizerCommand, None)
	# Translators: Input help mode message for go to synthesizer dialog command.
	script_activateSynthesizerDialog.__doc__ = _("Shows the NVDA synthesizer dialog")
	script_activateSynthesizerDialog.category=SCRCAT_CONFIG

	def script_activateVoiceDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onVoiceCommand, None)
	# Translators: Input help mode message for go to voice settings dialog command.
	script_activateVoiceDialog.__doc__ = _("Shows the NVDA voice settings dialog")
	script_activateVoiceDialog.category=SCRCAT_CONFIG

	def script_activateBrailleSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onBrailleCommand, None)
	# Translators: Input help mode message for go to braille settings dialog command.
	script_activateBrailleSettingsDialog.__doc__ = _("Shows the NVDA braille settings dialog")
	script_activateBrailleSettingsDialog.category=SCRCAT_CONFIG

	def script_activateKeyboardSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onKeyboardSettingsCommand, None)
	# Translators: Input help mode message for go to keyboard settings dialog command.
	script_activateKeyboardSettingsDialog.__doc__ = _("Shows the NVDA keyboard settings dialog")
	script_activateKeyboardSettingsDialog.category=SCRCAT_CONFIG

	def script_activateMouseSettingsDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onMouseSettingsCommand, None)
	# Translators: Input help mode message for go to mouse settings dialog command.
	script_activateMouseSettingsDialog.__doc__ = _("Shows the NVDA mouse settings dialog")
	script_activateMouseSettingsDialog.category=SCRCAT_CONFIG

	def script_activateReviewCursorDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onReviewCursorCommand, None)
	# Translators: Input help mode message for go to review cursor settings dialog command.
	script_activateReviewCursorDialog.__doc__ = _("Shows the NVDA review cursor settings dialog")
	script_activateReviewCursorDialog.category=SCRCAT_CONFIG

	def script_activateInputCompositionDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onInputCompositionCommand, None)
	# Translators: Input help mode message for go to input composition dialog.
	script_activateInputCompositionDialog.__doc__ = _("Shows the NVDA input composition settings dialog")
	script_activateInputCompositionDialog.category=SCRCAT_CONFIG

	def script_activateObjectPresentationDialog(self, gesture):
		wx.CallAfter(gui.mainFrame. onObjectPresentationCommand, None)
	# Translators: Input help mode message for go to object presentation dialog command.
	script_activateObjectPresentationDialog.__doc__ = _("Shows the NVDA object presentation settings dialog")
	script_activateObjectPresentationDialog.category=SCRCAT_CONFIG

	def script_activateBrowseModeDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onBrowseModeCommand, None)
	# Translators: Input help mode message for go to browse mode dialog command.
	script_activateBrowseModeDialog.__doc__ = _("Shows the NVDA browse mode settings dialog")
	script_activateBrowseModeDialog.category=SCRCAT_CONFIG

	def script_activateDocumentFormattingDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onDocumentFormattingCommand, None)
	# Translators: Input help mode message for go to document formatting dialog command.
	script_activateDocumentFormattingDialog.__doc__ = _("Shows the NVDA document formatting settings dialog")
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
	# Translators: Input help mode message for apply last saved or default settings command.
	script_revertConfiguration.__doc__ = _("Pressing once reverts the current configuration to the most recently saved state. Pressing three times reverts to factory defaults.")
	script_revertConfiguration.category=SCRCAT_CONFIG

	def script_activatePythonConsole(self,gesture):
		if globalVars.appArgs.secure:
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
		if braille.handler.tether == braille.handler.TETHER_FOCUS:
			braille.handler.tether = braille.handler.TETHER_REVIEW
			# Translators: One of the options for tethering braille (see the comment on "braille tethered to" message for more information).
			tetherMsg = _("review")
		else:
			braille.handler.tether = braille.handler.TETHER_FOCUS
			# Translators: One of the options for tethering braille (see the comment on "braille tethered to" message for more information).
			tetherMsg = _("focus")
		# Translators: Reports which position braille is tethered to (braille can be tethered to either focus or review position).
		ui.message(_("Braille tethered to %s") % tetherMsg)
	# Translators: Input help mode message for toggle braille tether to command (tethered means connected to or follows).
	script_braille_toggleTether.__doc__ = _("Toggle tethering of braille between the focus and the review position")
	script_braille_toggleTether.category=SCRCAT_BRAILLE

	def script_reportClipboardText(self,gesture):
		try:
			text = api.getClipData()
		except:
			text = None
		if not text or not isinstance(text,basestring) or text.isspace():
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
		self._copyStartMarker = api.getReviewPosition().copy()
		# Translators: Indicates start of review cursor text to be copied to clipboard.
		ui.message(_("Start marked"))
	# Translators: Input help mode message for mark review cursor position for copy command (that is, marks the current review cursor position as the starting point for text to be copied).
	script_review_markStartForCopy.__doc__ = _("Marks the current position of the review cursor as the start of text to be copied")
	script_review_markStartForCopy.category=SCRCAT_TEXTREVIEW

	def script_review_copy(self, gesture):
		if not getattr(self, "_copyStartMarker", None):
			# Translators: Presented when attempting to copy some review cursor text but there is no start marker.
			ui.message(_("No start marker set"))
			return
		pos = api.getReviewPosition().copy()
		if self._copyStartMarker.obj != pos.obj:
			# Translators: Presented when trying to copy text residing on a different object (that is, start marker is in object 1 but trying to copy text from object 2).
			ui.message(_("The start marker must reside within the same object"))
			return
		pos.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
		pos.setEndPoint(self._copyStartMarker, "startToStart")
		if pos.compareEndPoints(pos, "startToEnd") < 0 and pos.copyToClipboard():
			# Translators: Presented when some review text has been copied to clipboard.
			ui.message(_("Review selection copied to clipboard"))
		else:
			# Translators: Presented when there is no text selection to copy from review cursor.
			ui.message(_("No text to copy"))
			return
		self._copyStartMarker = None
	# Translators: Input help mode message for copy selected review cursor text to clipboard command.
	script_review_copy.__doc__ = _("Retrieves the text from the previously set start marker up to and including the current position of the review cursor and copies it to the clipboard")
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
			ui.message(_("no next"))
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
			ui.message(_("no previous"))
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
	script_touch_changeMode.__doc__=_("cycles between available touch modes")
	script_touch_changeMode.category=SCRCAT_TOUCH


	def script_touch_newExplore(self,gesture):
		touchHandler.handler.screenExplorer.moveTo(gesture.tracker.x,gesture.tracker.y,new=True)
	# Translators: Input help mode message for a touchscreen gesture.
	script_touch_newExplore.__doc__=_("Reports the object and content directly under your finger")
	script_touch_newExplore.category=SCRCAT_TOUCH

	def script_touch_explore(self,gesture):
		touchHandler.handler.screenExplorer.moveTo(gesture.tracker.x,gesture.tracker.y)
	# Translators: Input help mode message for a touchscreen gesture.
	script_touch_explore.__doc__=_("Reports the new object or content under your finger if different to where your finger was last")
	script_touch_explore.category=SCRCAT_TOUCH

	def script_touch_hoverUp(self,gesture):
		#Specifically for touch typing with onscreen keyboard keys
		obj=api.getNavigatorObject()
		import NVDAObjects.UIA
		if isinstance(obj,NVDAObjects.UIA.UIA) and obj.UIAElement.cachedClassName=="CRootKey":
			obj.doAction()
	script_touch_hoverUp.category=SCRCAT_TOUCH

	def script_activateConfigProfilesDialog(self, gesture):
		wx.CallAfter(gui.mainFrame.onConfigProfilesCommand, None)
	# Translators: Describes the command to open the Configuration Profiles dialog.
	script_activateConfigProfilesDialog.__doc__ = _("Shows the NVDA Configuration Profiles dialog")
	script_activateConfigProfilesDialog.category=SCRCAT_CONFIG

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

		# Preferences dialogs
		"kb:NVDA+control+g": "activateGeneralSettingsDialog",
		"kb:NVDA+control+s": "activateSynthesizerDialog",
		"kb:NVDA+control+v": "activateVoiceDialog",
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

		# Tools
		"kb:NVDA+f1": "navigatorObject_devInfo",
		"kb:NVDA+control+f1": "reportAppModuleInfo",
		"kb:NVDA+control+z": "activatePythonConsole",
		"kb:NVDA+control+f3": "reloadPlugins",
		"kb(desktop):NVDA+control+f2": "test_navigatorDisplayModelText",
		"kb:NVDA+alt+m": "interactWithMath",
	}

#: The single global commands instance.
#: @type: L{GlobalCommands}
commands = GlobalCommands()
