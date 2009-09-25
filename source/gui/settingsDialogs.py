#settingsDialogs.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import glob
import os
import wx
import logHandler
from synthDriverHandler import *
import config
import languageHandler
import speech
import gui
import globalVars
from logHandler import log
import nvwave
import speechDictHandler
import appModuleHandler
import scriptUI
import queueHandler
import braille
import core

class SettingsDialog(wx.Dialog):
	"""A settings dialog.
	A settings dialog consists of one or more settings controls and OK and Cancel buttons.
	Action may be taken in response to the OK or Cancel buttons.

	To use this dialog:
		* Set L{title} to the title of the dialog.
		* Override L{makeSettings} to populate a given sizer with the settings controls.
		* Optionally, override L{postInit} to perform actions after the dialog is created, such as setting the focus.
		* Optionally, extend one or both of L{onOk} or L{onCancel} to perform actions in response to the OK or Cancel buttons, respectively.

	@ivar title: The title of the dialog.
	@type title: str
	"""
	title = ""

	def __init__(self, parent):
		"""
		@param parent: The parent for this dialog; C{None} for no parent.
		@type parent: wx.Window
		"""
		super(SettingsDialog, self).__init__(parent, wx.ID_ANY, self.title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		self.settingsSizer=wx.BoxSizer(wx.VERTICAL)
		self.makeSettings(self.settingsSizer)
		mainSizer.Add(self.settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		self.postInit()

	def makeSettings(self, sizer):
		"""Populate the dialog with settings controls.
		Subclasses must override this method.
		@param sizer: The sizer to which to add the settings controls.
		@type sizer: wx.Sizer
		"""
		raise NotImplementedError

	def postInit(self):
		"""Called after the dialog has been created.
		For example, this might be used to set focus to the desired control.
		Sub-classes may override this method.
		"""

	def onOk(self, evt):
		"""Take action in response to the OK button being pressed.
		Sub-classes may extend this method.
		This base method should always be called to clean up the dialog.
		"""
		self.Destroy()

	def onCancel(self, evt):
		"""Take action in response to the Cancel button being pressed.
		Sub-classes may extend this method.
		This base method should always be called to clean up the dialog.
		"""
		self.Destroy()

class GeneralSettingsDialog(SettingsDialog):
	title = _("General settings")
	LOG_LEVELS = (
		(log.INFO, _("info")),
		(log.DEBUGWARNING, _("debug warning")),
		(log.IO, _("input/output")),
		(log.DEBUG, _("debug"))
	)

 	def makeSettings(self, settingsSizer):
		languageSizer=wx.BoxSizer(wx.HORIZONTAL)
		languageLabel=wx.StaticText(self,-1,label=_("&Language (requires restart to fully take affect):"))
		languageSizer.Add(languageLabel)
		languageListID=wx.NewId()
		self.languageNames=languageHandler.getAvailableLanguages()
		self.languageList=wx.Choice(self,languageListID,name=_("Language"),choices=[x[1] for x in self.languageNames])
		try:
			self.oldLanguage=config.conf["general"]["language"]
			index=[x[0] for x in self.languageNames].index(self.oldLanguage)
			self.languageList.SetSelection(index)
		except:
			pass
		languageSizer.Add(self.languageList)
		settingsSizer.Add(languageSizer,border=10,flag=wx.BOTTOM)
		self.saveOnExitCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Save configuration on exit"))
		self.saveOnExitCheckBox.SetValue(config.conf["general"]["saveConfigurationOnExit"])
		settingsSizer.Add(self.saveOnExitCheckBox,border=10,flag=wx.BOTTOM)
		self.askToExitCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Warn before exiting NVDA"))
		self.askToExitCheckBox.SetValue(config.conf["general"]["askToExit"])
		settingsSizer.Add(self.askToExitCheckBox,border=10,flag=wx.BOTTOM)
		logLevelSizer=wx.BoxSizer(wx.HORIZONTAL)
		logLevelLabel=wx.StaticText(self,-1,label=_("L&ogging level:"))
		logLevelSizer.Add(logLevelLabel)
		logLevelListID=wx.NewId()
		self.logLevelList=wx.Choice(self,logLevelListID,name=_("Log level"),choices=[name for level, name in self.LOG_LEVELS])
		curLevel = log.getEffectiveLevel()
		for index, (level, name) in enumerate(self.LOG_LEVELS):
			if level == curLevel:
				self.logLevelList.SetSelection(index)
				break
		else:
			log.debugWarning("Could not set log level list to current log level") 
		logLevelSizer.Add(self.logLevelList)
		settingsSizer.Add(logLevelSizer,border=10,flag=wx.BOTTOM)
		self.startAfterLogonCheckBox = wx.CheckBox(self, wx.ID_ANY, label=_("&Automatically start NVDA after I log on to Windows"))
		self.startAfterLogonCheckBox.SetValue(config.getStartAfterLogon())
		if not config.isInstalledCopy():
			self.startAfterLogonCheckBox.Disable()
		settingsSizer.Add(self.startAfterLogonCheckBox)
		self.startOnLogonScreenCheckBox = wx.CheckBox(self, wx.ID_ANY, label=_("Use NVDA on the Windows logon screen (requires administrator privileges)"))
		self.startOnLogonScreenCheckBox.SetValue(config.getStartOnLogonScreen())
		if not config.isServiceInstalled():
			self.startOnLogonScreenCheckBox.Disable()
		settingsSizer.Add(self.startOnLogonScreenCheckBox)

	def postInit(self):
		self.languageList.SetFocus()

	def onOk(self,evt):
		newLanguage=[x[0] for x in self.languageNames][self.languageList.GetSelection()]
		if newLanguage!=self.oldLanguage:
			try:
				languageHandler.setLanguage(newLanguage)
			except:
				log.error("languageHandler.setLanguage", exc_info=True)
				wx.MessageDialog(self,_("Error in %s language file")%newLanguage,_("Language Error"),wx.OK|wx.ICON_WARNING).ShowModal()
				return
		config.conf["general"]["language"]=newLanguage
		config.conf["general"]["saveConfigurationOnExit"]=self.saveOnExitCheckBox.IsChecked()
		config.conf["general"]["askToExit"]=self.askToExitCheckBox.IsChecked()
		logLevel=self.LOG_LEVELS[self.logLevelList.GetSelection()][0]
		config.conf["general"]["loggingLevel"]=logHandler.levelNames[logLevel]
		logHandler.setLogLevelFromConfig()
		if self.startAfterLogonCheckBox.IsEnabled():
			config.setStartAfterLogon(self.startAfterLogonCheckBox.GetValue())
		if self.startOnLogonScreenCheckBox.IsEnabled():
			try:
				config.setStartOnLogonScreen(self.startOnLogonScreenCheckBox.GetValue())
			except (WindowsError, RuntimeError):
				wx.MessageBox(_("This change requires administrator privileges."), _("Insufficient Privileges"), style=wx.OK | wx.ICON_ERROR)
		if self.oldLanguage!=newLanguage:
			if wx.MessageDialog(self,_("For the new language to take effect, the configuration must be saved and NVDA must be restarted. Press enter to save and restart NVDA, or cancel to manually save and exit at a later time."),_("Language Configuration Change"),wx.OK|wx.CANCEL|wx.ICON_WARNING).ShowModal()==wx.ID_OK:
				config.save()
				queueHandler.queueFunction(queueHandler.eventQueue,core.restart)
		super(GeneralSettingsDialog, self).onOk(evt)

class SynthesizerDialog(SettingsDialog):
	title = _("Synthesizer")

	def makeSettings(self, settingsSizer):
		synthListSizer=wx.BoxSizer(wx.HORIZONTAL)
		synthListLabel=wx.StaticText(self,-1,label=_("&Synthesizer:"))
		synthListID=wx.NewId()
		driverList=getSynthList()
		self.synthNames=[x[0] for x in driverList]
		options=['%s, %s'%x for x in driverList]
		self.synthList=wx.Choice(self,synthListID,choices=options)
		try:
			index=self.synthNames.index(getSynth().name)
			self.synthList.SetSelection(index)
		except:
			pass
		synthListSizer.Add(synthListLabel)
		synthListSizer.Add(self.synthList)
		settingsSizer.Add(synthListSizer,border=10,flag=wx.BOTTOM)
		deviceListSizer=wx.BoxSizer(wx.HORIZONTAL)
		deviceListLabel=wx.StaticText(self,-1,label=_("Output &device:"))
		deviceListID=wx.NewId()
		deviceNames=nvwave.getOutputDeviceNames()
		self.deviceList=wx.Choice(self,deviceListID,choices=deviceNames)
		try:
			selection = deviceNames.index(config.conf["speech"]["outputDevice"])
		except ValueError:
			selection = 0
		self.deviceList.SetSelection(selection)
		deviceListSizer.Add(deviceListLabel)
		deviceListSizer.Add(self.deviceList)
		settingsSizer.Add(deviceListSizer,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.synthList.SetFocus()

	def onOk(self,evt):
		config.conf["speech"]["outputDevice"]=self.deviceList.GetStringSelection()
		newSynth=self.synthNames[self.synthList.GetSelection()]
		if not setSynth(newSynth):
			wx.MessageDialog(self,_("Could not load the %s synthesizer.")%newSynth,_("Synthesizer Error"),wx.OK|wx.ICON_WARNING).ShowModal()
			return 
		super(SynthesizerDialog, self).onOk(evt)

class SynthSettingChanger(object):
	"""Functor which acts as calback for GUI events."""

	def __init__(self,setting):
		self.setting=setting

	def __call__(self,evt):
		val=evt.GetSelection()
		setattr(getSynth(),self.setting.name,val)

class StringSynthSettingChanger(SynthSettingChanger):
	"""Same as L{SynthSettingChanger} but handles combobox events."""
	def __init__(self,setting,dialog):
		self.dialog=dialog
		super(StringSynthSettingChanger,self).__init__(setting)

	def __call__(self,evt):
		if self.setting.name=="voice":
			# Cancel speech first so that the voice will change immediately instead of the change being queued.
			speech.cancelSpeech()
			changeVoice(getSynth(),getattr(self.dialog,"_%ss"%self.setting.name)[evt.GetSelection()].ID)
			self.dialog.updateVoiceSettings(changedSetting=self.setting.name)
		else:
			setattr(getSynth(),self.setting.name,getattr(self.dialog,"_%ss"%self.setting.name)[evt.GetSelection()].ID)

class VoiceSettingsDialog(SettingsDialog):
	title = _("Voice settings")

	@classmethod
	def _setSliderStepSizes(cls, slider, minStep):
		slider.SetLineSize(minStep)
		slider.SetPageSize(max(minStep, 10))

	def makeSettingControl(self,setting):
		"""Constructs appropriate GUI controls for given L{SynthSetting} such as label and slider.
		@param setting: Setting to construct controls for
		@type setting: L{SynthSetting}
		@returns: WXSizer containing newly created controls.
		@rtype: L{wx.BoxSizer}
		"""
		sizer=wx.BoxSizer(wx.HORIZONTAL)
		label=wx.StaticText(self,wx.ID_ANY,label="%s:"%setting.i18nName)
		slider=wx.Slider(self,wx.ID_ANY,minValue=0,maxValue=100,name="%s:"%setting.i18nName)
		setattr(self,"%sSlider"%setting.name,slider)
		slider.Bind(wx.EVT_SLIDER,SynthSettingChanger(setting))
		self._setSliderStepSizes(slider,setting.minStep)
		slider.SetValue(getattr(getSynth(),setting.name))
		sizer.Add(label)
		sizer.Add(slider)
		if self.lastControl:
			slider.MoveAfterInTabOrder(self.lastControl)
		self.lastControl=slider
		return sizer

	def makeStringSettingControl(self,setting):
		"""Same as L{makeSettingControl} but for string settings. Returns sizer with label and combobox."""
		sizer=wx.BoxSizer(wx.HORIZONTAL)
		label=wx.StaticText(self,wx.ID_ANY,label="%s:"%setting.i18nName)
		synth=getSynth()
		setattr(self,"_%ss"%setting.name,getattr(synth,"available%ss"%setting.name.capitalize()))
		l=getattr(self,"_%ss"%setting.name)###
		lCombo=wx.Choice(self,wx.ID_ANY,name="%s:"%setting.i18nName,choices=[x.name for x in l])
		setattr(self,"%sList"%setting.name,lCombo)
		try:
			cur=getattr(synth,setting.name)
			i=[x.ID for x in l].index(cur)
			lCombo.SetSelection(i)
		except ValueError:
			pass
		lCombo.Bind(wx.EVT_CHOICE,StringSynthSettingChanger(setting,self))
		sizer.Add(label)
		sizer.Add(lCombo)
		if self.lastControl:
			lCombo.MoveAfterInTabOrder(self.lastControl)
		self.lastControl=lCombo
		return sizer

	def makeSettings(self, settingsSizer):
		self.sizerDict={}
		self.lastControl=None
		#Create controls for Synth Settings
		self.updateVoiceSettings()
		self.punctuationCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Speak all punctuation"))
		self.punctuationCheckBox.SetValue(config.conf["speech"]["speakPunctuation"])
		settingsSizer.Add(self.punctuationCheckBox,border=10,flag=wx.BOTTOM)
		self.raisePitchForCapsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Raise pitch for capitals"))
		self.raisePitchForCapsCheckBox.SetValue(config.conf["speech"][getSynth().name]["raisePitchForCapitals"])
		settingsSizer.Add(self.raisePitchForCapsCheckBox,border=10,flag=wx.BOTTOM)
		self.sayCapForCapsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Say &cap before capitals"))
		self.sayCapForCapsCheckBox.SetValue(config.conf["speech"][getSynth().name]["sayCapForCapitals"])
		settingsSizer.Add(self.sayCapForCapsCheckBox,border=10,flag=wx.BOTTOM)
		self.beepForCapsCheckBox = wx.CheckBox(self, wx.NewId(), label = _("&Beep for capitals"))
		self.beepForCapsCheckBox.SetValue(config.conf["speech"][getSynth().name]["beepForCapitals"])
		settingsSizer.Add(self.beepForCapsCheckBox,border=10,flag=wx.BOTTOM)
		self.useSpellingFunctionalityCheckBox = wx.CheckBox(self, wx.NewId(), label = _("Use &spelling functionality if supported"))
		self.useSpellingFunctionalityCheckBox.SetValue(config.conf["speech"][getSynth().name]["useSpellingFunctionality"])
		settingsSizer.Add(self.useSpellingFunctionalityCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		try:
			setting=getSynth().supportedSettings[-1]
			control=getattr(self,"%sSlider"%setting.name) if isinstance(setting,NumericSynthSetting) else getattr(self,"%sList"%setting.name)
			control.SetFocus()
		except IndexError:
			self.punctuationCheckBox.SetFocus()

	def updateVoiceSettings(self, changedSetting=None):
		"""Creates, hides or updates existing GUI controls for all of supported settings."""
		synth=getSynth()
		#firstly check already created options
		for name,sizer in self.sizerDict.iteritems():
			if name == changedSetting:
				# Changing a setting shouldn't cause that setting itself to disappear.
				continue
			if not synth.isSupported(name):
				self.settingsSizer.Hide(sizer)
		#Create new controls, update already existing
		for setting in reversed(synth.supportedSettings):
			if setting.name == changedSetting:
				# Changing a setting shouldn't cause that setting's own values to change.
				continue
			b=isinstance(setting,NumericSynthSetting)
			if setting.name in self.sizerDict: #update a value
				self.settingsSizer.Show(self.sizerDict[setting.name])
				if b:
					getattr(self,"%sSlider"%setting.name).SetValue(getattr(synth,setting.name))
				else:
					l=getattr(self,"_%ss"%setting.name)
					lCombo=getattr(self,"%sList"%setting.name)
					try:
						cur=getattr(synth,setting.name)
						i=[x.ID for x in l].index(cur)
						lCombo.SetSelection(i)
					except ValueError:
						pass
			else: #create a new control
				settingMaker=self.makeSettingControl if b else self.makeStringSettingControl
				s=settingMaker(setting)
				self.sizerDict[setting.name]=s
				self.settingsSizer.Insert(len(self.sizerDict)-1,s,border=10,flag=wx.BOTTOM)
		#Update graphical layout of the dialog
		self.settingsSizer.Layout()

	def onCancel(self,evt):
		#unbind change events for string settings as wx closes combo boxes on cancel
		for setting in getSynth().supportedSettings:
			if isinstance(setting,NumericSynthSetting): continue
			getattr(self,"%sList"%setting.name).Unbind(wx.EVT_CHOICE)
		#restore settings
		getSynth().loadSettings()
		super(VoiceSettingsDialog, self).onCancel(evt)

	def onOk(self,evt):
		getSynth().saveSettings()
		config.conf["speech"]["speakPunctuation"]=self.punctuationCheckBox.IsChecked()
		config.conf["speech"][getSynth().name]["raisePitchForCapitals"]=self.raisePitchForCapsCheckBox.IsChecked()
		config.conf["speech"][getSynth().name]["sayCapForCapitals"]=self.sayCapForCapsCheckBox.IsChecked()
		config.conf["speech"][getSynth().name]["beepForCapitals"]=self.beepForCapsCheckBox.IsChecked()
		config.conf["speech"][getSynth().name]["useSpellingFunctionality"]=self.useSpellingFunctionalityCheckBox.IsChecked()
		super(VoiceSettingsDialog, self).onOk(evt)

class KeyboardSettingsDialog(SettingsDialog):
	title = _("Keyboard Settings")

	def makeSettings(self, settingsSizer):
		kbdSizer=wx.BoxSizer(wx.HORIZONTAL)
		kbdLabel=wx.StaticText(self,-1,label=_("&Keyboard layout:"))
		kbdSizer.Add(kbdLabel)
		kbdListID=wx.NewId()
		self.kbdNames=list(set(os.path.splitext(x)[0].split('_')[-1] for x in glob.glob('appModules/*.kbd')))
		self.kbdNames.sort()
		self.kbdList=wx.Choice(self,kbdListID,name=_("Keyboard layout"),choices=self.kbdNames)
		try:
			index=self.kbdNames.index(config.conf['keyboard']['keyboardLayout'])
			self.kbdList.SetSelection(index)
		except:
			log.debugWarning("Could not set Keyboard layout list to current layout",exc_info=True) 
		kbdSizer.Add(self.kbdList)
		settingsSizer.Add(kbdSizer,border=10,flag=wx.BOTTOM)
		self.capsAsNVDAModifierCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Use CapsLock as an NVDA modifier key"))
		self.capsAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"])
		settingsSizer.Add(self.capsAsNVDAModifierCheckBox,border=10,flag=wx.BOTTOM)
		self.numpadInsertAsNVDAModifierCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Use numpad Insert as an NVDA modifier key"))
		self.numpadInsertAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useNumpadInsertAsNVDAModifierKey"])
		settingsSizer.Add(self.numpadInsertAsNVDAModifierCheckBox,border=10,flag=wx.BOTTOM)
		self.extendedInsertAsNVDAModifierCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Use extended Insert as an NVDA modifier key"))
		self.extendedInsertAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useExtendedInsertAsNVDAModifierKey"])
		settingsSizer.Add(self.extendedInsertAsNVDAModifierCheckBox,border=10,flag=wx.BOTTOM)
		self.charsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Speak typed &characters"))
		self.charsCheckBox.SetValue(config.conf["keyboard"]["speakTypedCharacters"])
		settingsSizer.Add(self.charsCheckBox,border=10,flag=wx.BOTTOM)
		self.wordsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Speak typed &words"))
		self.wordsCheckBox.SetValue(config.conf["keyboard"]["speakTypedWords"])
		settingsSizer.Add(self.wordsCheckBox,border=10,flag=wx.BOTTOM)
		self.commandKeysCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Speak command &keys"))
		self.commandKeysCheckBox.SetValue(config.conf["keyboard"]["speakCommandKeys"])
		settingsSizer.Add(self.commandKeysCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.kbdList.SetFocus()

	def onOk(self,evt):
		layout=self.kbdNames[self.kbdList.GetSelection()]
		oldLayout=config.conf['keyboard']['keyboardLayout']
		if layout!=oldLayout:
			config.conf['keyboard']['keyboardLayout']=layout
			for m in appModuleHandler.runningTable.values():
				m.loadKeyMap()
		config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"]=self.capsAsNVDAModifierCheckBox.IsChecked()
		config.conf["keyboard"]["useNumpadInsertAsNVDAModifierKey"]=self.numpadInsertAsNVDAModifierCheckBox.IsChecked()
		config.conf["keyboard"]["useExtendedInsertAsNVDAModifierKey"]=self.extendedInsertAsNVDAModifierCheckBox.IsChecked()
		config.conf["keyboard"]["speakTypedCharacters"]=self.charsCheckBox.IsChecked()
		config.conf["keyboard"]["speakTypedWords"]=self.wordsCheckBox.IsChecked()
		config.conf["keyboard"]["speakCommandKeys"]=self.commandKeysCheckBox.IsChecked()
		super(KeyboardSettingsDialog, self).onOk(evt)

class MouseSettingsDialog(SettingsDialog):
	title = _("Mouse settings")

 	def makeSettings(self, settingsSizer):
		self.shapeCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report mouse &shape changes"))
		self.shapeCheckBox.SetValue(config.conf["mouse"]["reportMouseShapeChanges"])
		settingsSizer.Add(self.shapeCheckBox,border=10,flag=wx.BOTTOM)
		self.reportTextCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &text under the mouse"))
		self.reportTextCheckBox.SetValue(config.conf["mouse"]["reportTextUnderMouse"])
		settingsSizer.Add(self.reportTextCheckBox,border=10,flag=wx.BOTTOM)
		textUnitSizer=wx.BoxSizer(wx.HORIZONTAL)
		textUnitLabel=wx.StaticText(self,-1,label=_("Text &unit resolution:"))
		textUnitSizer.Add(textUnitLabel)
		import textInfos
		self.textUnits=[textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD,textInfos.UNIT_LINE,textInfos.UNIT_PARAGRAPH]
		self.textUnitComboBox=wx.Choice(self,wx.ID_ANY,name=_("text reporting unit"),choices=[textInfos.unitLabels[x] for x in self.textUnits])
		try:
			index=self.textUnits.index(config.conf["mouse"]["mouseTextUnit"])
		except:
			index=0
		self.textUnitComboBox.SetSelection(index)
		textUnitSizer.Add(self.textUnitComboBox)
		settingsSizer.Add(textUnitSizer,border=10,flag=wx.BOTTOM)
		self.reportObjectRoleCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &role when mouse enters object"))
		self.reportObjectRoleCheckBox.SetValue(config.conf["mouse"]["reportObjectRoleOnMouseEnter"])
		settingsSizer.Add(self.reportObjectRoleCheckBox,border=10,flag=wx.BOTTOM)
		self.audioCheckBox=wx.CheckBox(self,wx.NewId(),label=_("play audio coordinates when mouse moves"))
		self.audioCheckBox.SetValue(config.conf["mouse"]["audioCoordinatesOnMouseMove"])
		settingsSizer.Add(self.audioCheckBox,border=10,flag=wx.BOTTOM)
		self.audioDetectBrightnessCheckBox=wx.CheckBox(self,wx.NewId(),label=_("brightness controls audio coordinates volume"))
		self.audioDetectBrightnessCheckBox.SetValue(config.conf["mouse"]["audioCoordinates_detectBrightness"])
		settingsSizer.Add(self.audioDetectBrightnessCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.shapeCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["mouse"]["reportMouseShapeChanges"]=self.shapeCheckBox.IsChecked()
		config.conf["mouse"]["reportTextUnderMouse"]=self.reportTextCheckBox.IsChecked()
		config.conf["mouse"]["mouseTextUnit"]=self.textUnits[self.textUnitComboBox.GetSelection()]
		config.conf["mouse"]["reportObjectRoleOnMouseEnter"]=self.reportObjectRoleCheckBox.IsChecked()
		config.conf["mouse"]["audioCoordinatesOnMouseMove"]=self.audioCheckBox.IsChecked()
		config.conf["mouse"]["audioCoordinates_detectBrightness"]=self.audioDetectBrightnessCheckBox.IsChecked()

		super(MouseSettingsDialog, self).onOk(evt)

class ObjectPresentationDialog(SettingsDialog):
	title = _("Object presentation")
	progressLabels = (
		("off", _("off")),
		("speak", _("Speak")),
		("beep", _("Beep")),
		("both", _("Speak and beep")),
	)

	def makeSettings(self, settingsSizer):
		self.tooltipCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &tooltips"))
		self.tooltipCheckBox.SetValue(config.conf["presentation"]["reportTooltips"])
		settingsSizer.Add(self.tooltipCheckBox,border=10,flag=wx.BOTTOM)
		self.balloonCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &help balloons"))
		self.balloonCheckBox.SetValue(config.conf["presentation"]["reportHelpBalloons"])
		settingsSizer.Add(self.balloonCheckBox,border=10,flag=wx.BOTTOM)
		self.shortcutCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report object shortcut &keys"))
		self.shortcutCheckBox.SetValue(config.conf["presentation"]["reportKeyboardShortcuts"])
		settingsSizer.Add(self.shortcutCheckBox,border=10,flag=wx.BOTTOM)
		self.positionInfoCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report object &position information"))
		self.positionInfoCheckBox.SetValue(config.conf["presentation"]["reportObjectPositionInformation"])
		settingsSizer.Add(self.positionInfoCheckBox,border=10,flag=wx.BOTTOM)
		self.descriptionCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report object &descriptions"))
		self.descriptionCheckBox.SetValue(config.conf["presentation"]["reportObjectDescriptions"])
		settingsSizer.Add(self.descriptionCheckBox,border=10,flag=wx.BOTTOM)
		progressSizer=wx.BoxSizer(wx.HORIZONTAL)
		progressLabel=wx.StaticText(self,-1,label=_("Progress &bar output:"))
		progressSizer.Add(progressLabel)
		progressListID=wx.NewId()
		self.progressList=wx.Choice(self,progressListID,name=_("Progress bar output"),choices=[name for setting, name in self.progressLabels])
		for index, (setting, name) in enumerate(self.progressLabels):
			if setting == config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]:
				self.progressList.SetSelection(index)
				break
		else:
			log.debugWarning("Could not set progress list to current report progress bar updates setting")
		progressSizer.Add(self.progressList)
		settingsSizer.Add(progressSizer,border=10,flag=wx.BOTTOM)
		self.reportBackgroundProgressBarsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report background progress bars"))
		self.reportBackgroundProgressBarsCheckBox.SetValue(config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"])
		settingsSizer.Add(self.reportBackgroundProgressBarsCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.tooltipCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["presentation"]["reportTooltips"]=self.tooltipCheckBox.IsChecked()
		config.conf["presentation"]["reportHelpBalloons"]=self.balloonCheckBox.IsChecked()
		config.conf["presentation"]["reportKeyboardShortcuts"]=self.shortcutCheckBox.IsChecked()
		config.conf["presentation"]["reportObjectPositionInformation"]=self.positionInfoCheckBox.IsChecked()
		config.conf["presentation"]["reportObjectDescriptions"]=self.descriptionCheckBox.IsChecked()
		config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"]=self.progressLabels[self.progressList.GetSelection()][0]
		config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"]=self.reportBackgroundProgressBarsCheckBox.IsChecked()
		super(ObjectPresentationDialog, self).onOk(evt)

class VirtualBuffersDialog(SettingsDialog):
	title = _("virtual buffers")

	def makeSettings(self, settingsSizer):
		maxLengthLabel=wx.StaticText(self,-1,label=_("&Maximum number of characters on one line"))
		settingsSizer.Add(maxLengthLabel)
		self.maxLengthEdit=wx.TextCtrl(self,wx.NewId())
		self.maxLengthEdit.SetValue(str(config.conf["virtualBuffers"]["maxLineLength"]))
		settingsSizer.Add(self.maxLengthEdit,border=10,flag=wx.BOTTOM)
		pageLinesLabel=wx.StaticText(self,-1,label=_("&Number of lines per page"))
		settingsSizer.Add(pageLinesLabel)
		self.pageLinesEdit=wx.TextCtrl(self,wx.NewId())
		self.pageLinesEdit.SetValue(str(config.conf["virtualBuffers"]["linesPerPage"]))
		settingsSizer.Add(self.pageLinesEdit,border=10,flag=wx.BOTTOM)
		self.useScreenLayoutCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Use &screen layout (when supported)"))
		self.useScreenLayoutCheckBox.SetValue(config.conf["virtualBuffers"]["useScreenLayout"])
		settingsSizer.Add(self.useScreenLayoutCheckBox,border=10,flag=wx.BOTTOM)
		self.layoutTablesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report l&ayout tables"))
		self.layoutTablesCheckBox.SetValue(config.conf["documentFormatting"]["includeLayoutTables"])
		settingsSizer.Add(self.layoutTablesCheckBox,border=10,flag=wx.BOTTOM)

		self.autoPassThroughOnFocusChangeCheckBox=wx.CheckBox(self,wx.ID_ANY,label=_("Automatic focus mode for focus changes"))
		self.autoPassThroughOnFocusChangeCheckBox.SetValue(config.conf["virtualBuffers"]["autoPassThroughOnFocusChange"])
		settingsSizer.Add(self.autoPassThroughOnFocusChangeCheckBox,border=10,flag=wx.BOTTOM)
		self.autoPassThroughOnCaretMoveCheckBox=wx.CheckBox(self,wx.ID_ANY,label=_("Automatic focus mode for caret movement"))
		self.autoPassThroughOnCaretMoveCheckBox.SetValue(config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"])
		settingsSizer.Add(self.autoPassThroughOnCaretMoveCheckBox,border=10,flag=wx.BOTTOM)
		self.passThroughAudioIndicationCheckBox=wx.CheckBox(self,wx.ID_ANY,label=_("Audio indication of focus and browse modes"))
		self.passThroughAudioIndicationCheckBox.SetValue(config.conf["virtualBuffers"]["passThroughAudioIndication"])
		settingsSizer.Add(self.passThroughAudioIndicationCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.maxLengthEdit.SetFocus()

	def onOk(self,evt):
		try:
			newMaxLength=int(self.maxLengthEdit.GetValue())
		except:
			newMaxLength=0
		if newMaxLength >=10 and newMaxLength <=250:
			config.conf["virtualBuffers"]["maxLineLength"]=newMaxLength
		try:
			newPageLines=int(self.pageLinesEdit.GetValue())
		except:
			newPageLines=0
		if newPageLines >=5 and newPageLines <=150:
			config.conf["virtualBuffers"]["linesPerPage"]=newPageLines
		config.conf["virtualBuffers"]["useScreenLayout"]=self.useScreenLayoutCheckBox.IsChecked()
		config.conf["documentFormatting"]["includeLayoutTables"]=self.layoutTablesCheckBox.IsChecked()
		config.conf["virtualBuffers"]["autoPassThroughOnFocusChange"]=self.autoPassThroughOnFocusChangeCheckBox.IsChecked()
		config.conf["virtualBuffers"]["autoPassThroughOnCaretMove"]=self.autoPassThroughOnCaretMoveCheckBox.IsChecked()
		config.conf["virtualBuffers"]["passThroughAudioIndication"]=self.passThroughAudioIndicationCheckBox.IsChecked()
		super(VirtualBuffersDialog, self).onOk(evt)

class DocumentFormattingDialog(SettingsDialog):
	title = _("Document formatting")

	def makeSettings(self, settingsSizer):
		self.detectFormatAfterCursorCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Announce formatting changes after the cursor (can cause a lag)"))
		self.detectFormatAfterCursorCheckBox.SetValue(config.conf["documentFormatting"]["detectFormatAfterCursor"])
		settingsSizer.Add(self.detectFormatAfterCursorCheckBox,border=10,flag=wx.BOTTOM)
		self.fontNameCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report font &name"))
		self.fontNameCheckBox.SetValue(config.conf["documentFormatting"]["reportFontName"])
		settingsSizer.Add(self.fontNameCheckBox,border=10,flag=wx.BOTTOM)
		self.fontSizeCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report font &size"))
		self.fontSizeCheckBox.SetValue(config.conf["documentFormatting"]["reportFontSize"])
		settingsSizer.Add(self.fontSizeCheckBox,border=10,flag=wx.BOTTOM)
		self.fontAttrsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report font attri&butes"))
		self.fontAttrsCheckBox.SetValue(config.conf["documentFormatting"]["reportFontAttributes"])
		settingsSizer.Add(self.fontAttrsCheckBox,border=10,flag=wx.BOTTOM)
		self.alignmentCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &alignment"))
		self.alignmentCheckBox.SetValue(config.conf["documentFormatting"]["reportAlignment"])
		settingsSizer.Add(self.alignmentCheckBox,border=10,flag=wx.BOTTOM)
		self.styleCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report st&yle"))
		self.styleCheckBox.SetValue(config.conf["documentFormatting"]["reportStyle"])
		settingsSizer.Add(self.styleCheckBox,border=10,flag=wx.BOTTOM)
		self.spellingErrorsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report spelling errors"))
		self.spellingErrorsCheckBox.SetValue(config.conf["documentFormatting"]["reportSpellingErrors"])
		settingsSizer.Add(self.spellingErrorsCheckBox,border=10,flag=wx.BOTTOM)
		self.pageCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &pages"))
		self.pageCheckBox.SetValue(config.conf["documentFormatting"]["reportPage"])
		settingsSizer.Add(self.pageCheckBox,border=10,flag=wx.BOTTOM)
		self.lineNumberCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &line numbers"))
		self.lineNumberCheckBox.SetValue(config.conf["documentFormatting"]["reportLineNumber"])
		settingsSizer.Add(self.lineNumberCheckBox,border=10,flag=wx.BOTTOM)
		self.tablesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &tables"))
		self.tablesCheckBox.SetValue(config.conf["documentFormatting"]["reportTables"])
		settingsSizer.Add(self.tablesCheckBox,border=10,flag=wx.BOTTOM)
		self.linksCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &links"))
		self.linksCheckBox.SetValue(config.conf["documentFormatting"]["reportLinks"])
		settingsSizer.Add(self.linksCheckBox,border=10,flag=wx.BOTTOM)
		self.headingsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &headings"))
		self.headingsCheckBox.SetValue(config.conf["documentFormatting"]["reportHeadings"])
		settingsSizer.Add(self.headingsCheckBox,border=10,flag=wx.BOTTOM)
		self.listsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report l&ists"))
		self.listsCheckBox.SetValue(config.conf["documentFormatting"]["reportLists"])
		settingsSizer.Add(self.listsCheckBox,border=10,flag=wx.BOTTOM)
		self.blockQuotesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report block &quotes"))
		self.blockQuotesCheckBox.SetValue(config.conf["documentFormatting"]["reportBlockQuotes"])
		settingsSizer.Add(self.blockQuotesCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.detectFormatAfterCursorCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["documentFormatting"]["detectFormatAfterCursor"]=self.detectFormatAfterCursorCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontName"]=self.fontNameCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontSize"]=self.fontSizeCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontAttributes"]=self.fontAttrsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportAlignment"]=self.alignmentCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportStyle"]=self.styleCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportSpellingErrors"]=self.spellingErrorsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportPage"]=self.pageCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLineNumber"]=self.lineNumberCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportTables"]=self.tablesCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLinks"]=self.linksCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportHeadings"]=self.headingsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLists"]=self.listsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportBlockQuotes"]=self.blockQuotesCheckBox.IsChecked()
		super(DocumentFormattingDialog, self).onOk(evt)

class DictionaryEntryDialog(wx.Dialog):

	def __init__(self,parent):
		super(DictionaryEntryDialog,self).__init__(parent,title=_("Edit dictionary entry"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer.Add(wx.StaticText(self,-1,label=_("&Pattern")))
		self.patternTextCtrl=wx.TextCtrl(self,wx.NewId())
		settingsSizer.Add(self.patternTextCtrl)
		settingsSizer.Add(wx.StaticText(self,-1,label=_("&Replacement")))
		self.replacementTextCtrl=wx.TextCtrl(self,wx.NewId())
		settingsSizer.Add(self.replacementTextCtrl)
		settingsSizer.Add(wx.StaticText(self,-1,label=_("&Comment")))
		self.commentTextCtrl=wx.TextCtrl(self,wx.NewId())
		settingsSizer.Add(self.commentTextCtrl)
		self.caseSensitiveCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Case &sensitive"))
		settingsSizer.Add(self.caseSensitiveCheckBox)
		self.regexpCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Regular &expression"))
		settingsSizer.Add(self.regexpCheckBox)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.patternTextCtrl.SetFocus()

class DictionaryDialog(SettingsDialog):

	def __init__(self,parent,title,speechDict):
		self.title = title
		self.speechDict = speechDict
		self.tempSpeechDict=speechDictHandler.SpeechDict()
		self.tempSpeechDict.extend(self.speechDict)
		globalVars.speechDictionaryProcessing=False
		super(DictionaryDialog, self).__init__(parent)

	def makeSettings(self, settingsSizer):
		dictListID=wx.NewId()
		entriesSizer=wx.BoxSizer(wx.HORIZONTAL)
		entriesLabel=wx.StaticText(self,-1,label=_("&Dictionary entries"))
		entriesSizer.Add(entriesLabel)
		self.dictList=wx.ListCtrl(self,dictListID,style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		self.dictList.InsertColumn(0,_("Comment"))
		self.dictList.InsertColumn(1,_("Pattern"))
		self.dictList.InsertColumn(2,_("Replacement"))
		self.dictList.InsertColumn(3,_("case sensitive"))
		self.dictList.InsertColumn(4,_("Regular expression"))
		for entry in self.tempSpeechDict:
			self.dictList.Append((entry.comment,entry.pattern,entry.replacement,str(entry.caseSensitive),str(entry.regexp)))
		self.editingIndex=-1
		entriesSizer.Add(self.dictList)
		settingsSizer.Add(entriesSizer)
		addButtonID=wx.NewId()
		addButton=wx.Button(self,addButtonID,_("&Add"),wx.DefaultPosition)
		settingsSizer.Add(addButton)
		editButtonID=wx.NewId()
		editButton=wx.Button(self,editButtonID,_("&edit"),wx.DefaultPosition)
		settingsSizer.Add(editButton)
		removeButtonID=wx.NewId()
		removeButton=wx.Button(self,removeButtonID,_("&Remove"),wx.DefaultPosition)
		settingsSizer.Add(removeButton)
		self.Bind(wx.EVT_BUTTON,self.OnAddClick,id=addButtonID)
		self.Bind(wx.EVT_BUTTON,self.OnEditClick,id=editButtonID)
		self.Bind(wx.EVT_BUTTON,self.OnRemoveClick,id=removeButtonID)

	def postInit(self):
		self.dictList.SetFocus()

	def onCancel(self,evt):
		globalVars.speechDictionaryProcessing=True
		super(DictionaryDialog, self).onCancel(evt)

	def onOk(self,evt):
		globalVars.speechDictionaryProcessing=True
		if self.tempSpeechDict!=self.speechDict:
			del self.speechDict[:]
			self.speechDict.extend(self.tempSpeechDict)
			self.speechDict.save()
		super(DictionaryDialog, self).onOk(evt)

	def OnAddClick(self,evt):
		entryDialog=DictionaryEntryDialog(self)
		if entryDialog.ShowModal()==wx.ID_OK:
			self.tempSpeechDict.append(speechDictHandler.SpeechDictEntry(entryDialog.patternTextCtrl.GetValue(),entryDialog.replacementTextCtrl.GetValue(),entryDialog.commentTextCtrl.GetValue(),bool(entryDialog.caseSensitiveCheckBox.GetValue()),bool(entryDialog.regexpCheckBox.GetValue())))
			self.dictList.Append((entryDialog.commentTextCtrl.GetValue(),entryDialog.patternTextCtrl.GetValue(),entryDialog.replacementTextCtrl.GetValue(),str(bool(entryDialog.caseSensitiveCheckBox.GetValue())),str(bool(entryDialog.regexpCheckBox.GetValue()))))
			index=self.dictList.GetFirstSelected()
			while index>=0:
				self.dictList.Select(index,on=0)
				index=self.dictList.GetNextSelected(index)
			addedIndex=self.dictList.GetItemCount()-1
			self.dictList.Select(addedIndex)
			self.dictList.Focus(addedIndex)
			self.dictList.SetFocus()
		entryDialog.Destroy()

	def OnEditClick(self,evt):
		if self.dictList.GetSelectedItemCount()!=1:
			return
		editIndex=self.dictList.GetFirstSelected()
		if editIndex<0:
			return
		entryDialog=DictionaryEntryDialog(self)
		entryDialog.patternTextCtrl.SetValue(self.tempSpeechDict[editIndex].pattern)
		entryDialog.replacementTextCtrl.SetValue(self.tempSpeechDict[editIndex].replacement)
		entryDialog.commentTextCtrl.SetValue(self.tempSpeechDict[editIndex].comment)
		entryDialog.caseSensitiveCheckBox.SetValue(self.tempSpeechDict[editIndex].caseSensitive)
		entryDialog.regexpCheckBox.SetValue(self.tempSpeechDict[editIndex].regexp)
		if entryDialog.ShowModal()==wx.ID_OK:
			self.tempSpeechDict[editIndex]=speechDictHandler.SpeechDictEntry(entryDialog.patternTextCtrl.GetValue(),entryDialog.replacementTextCtrl.GetValue(),entryDialog.commentTextCtrl.GetValue(),bool(entryDialog.caseSensitiveCheckBox.GetValue()),bool(entryDialog.regexpCheckBox.GetValue()))
			self.dictList.SetStringItem(editIndex,0,entryDialog.commentTextCtrl.GetValue())
			self.dictList.SetStringItem(editIndex,1,entryDialog.patternTextCtrl.GetValue())
			self.dictList.SetStringItem(editIndex,2,entryDialog.replacementTextCtrl.GetValue())
			self.dictList.SetStringItem(editIndex,3,str(bool(entryDialog.caseSensitiveCheckBox.GetValue())))
			self.dictList.SetStringItem(editIndex,4,str(bool(entryDialog.regexpCheckBox.GetValue())))
			self.dictList.SetFocus()
		entryDialog.Destroy()

	def OnRemoveClick(self,evt):
		index=self.dictList.GetFirstSelected()
		while index>=0:
			self.dictList.DeleteItem(index)
			del self.tempSpeechDict[index]
			index=self.dictList.GetNextSelected(index)
		self.dictList.SetFocus()

class BrailleSettingsDialog(SettingsDialog):
	title = _("Braille Settings")

	def makeSettings(self, settingsSizer):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, wx.ID_ANY, label=_("Braille &display:"))
		driverList = braille.getDisplayList()
		self.displayNames = [driver[0] for driver in driverList]
		self.displayList = wx.Choice(self, wx.ID_ANY, choices=[driver[1] for driver in driverList])
		try:
			selection = self.displayNames.index(braille.handler.display.name)
			self.displayList.SetSelection(selection)
		except:
			pass
		sizer.Add(label)
		sizer.Add(self.displayList)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, wx.ID_ANY, label=_("Translation &table:"))
		self.tableNames = [table[0] for table in braille.TABLES]
		self.tableList = wx.Choice(self, wx.ID_ANY, choices=[table[1] for table in braille.TABLES])
		try:
			selection = self.tableNames.index(config.conf["braille"]["translationTable"])
			self.tableList.SetSelection(selection)
		except:
			pass
		sizer.Add(label)
		sizer.Add(self.tableList)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		self.expandAtCursorCheckBox = wx.CheckBox(self, wx.ID_ANY, label=_("E&xpand to computer braille for the word at the cursor"))
		self.expandAtCursorCheckBox.SetValue(config.conf["braille"]["expandAtCursor"])
		settingsSizer.Add(self.expandAtCursorCheckBox, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, wx.ID_ANY, label=_("Cursor blink rate (ms)"))
		sizer.Add(label)
		self.cursorBlinkRateEdit = wx.TextCtrl(self, wx.ID_ANY)
		self.cursorBlinkRateEdit.SetValue(str(config.conf["braille"]["cursorBlinkRate"]))
		sizer.Add(self.cursorBlinkRateEdit)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		label = wx.StaticText(self, wx.ID_ANY, label=_("Message timeout (sec)"))
		sizer.Add(label)
		self.messageTimeoutEdit = wx.TextCtrl(self, wx.ID_ANY)
		self.messageTimeoutEdit.SetValue(str(config.conf["braille"]["messageTimeout"]))
		sizer.Add(self.messageTimeoutEdit)
		settingsSizer.Add(sizer, border=10, flag=wx.BOTTOM)

	def postInit(self):
		self.displayList.SetFocus()

	def onOk(self, evt):
		display = self.displayNames[self.displayList.GetSelection()]
		if not braille.handler.setDisplayByName(display):
			wx.MessageDialog(self, _("Could not load the %s display.")%display, _("Braille Display Error"), wx.OK|wx.ICON_WARNING).ShowModal()
			return 
		config.conf["braille"]["translationTable"] = self.tableNames[self.tableList.GetSelection()]
		config.conf["braille"]["expandAtCursor"] = self.expandAtCursorCheckBox.GetValue()
		try:
			val = int(self.cursorBlinkRateEdit.GetValue())
		except (ValueError, TypeError):
			val = None
		if 0 <= val <= 2000:
			config.conf["braille"]["cursorBlinkRate"] = val
		try:
			val = int(self.messageTimeoutEdit.GetValue())
		except (ValueError, TypeError):
			val = None
		if 1 <= val <= 20:
			config.conf["braille"]["messageTimeout"] = val
		braille.handler.configDisplay()
		super(BrailleSettingsDialog,  self).onOk(evt)
