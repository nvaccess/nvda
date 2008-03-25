#settingsDialogs.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import wx
import logging
from synthDriverHandler import *
import config
import languageHandler
import speech
import gui
import globalVars
from ctypes import *
from ctypes.wintypes import *
import speechDictHandler
import scriptUI

MAXPNAMELEN=32

class WAVEOUTCAPS(Structure):
	_fields_=[
		('wMid',WORD),
		('wPid',WORD),
		('vDriverVersion',c_uint),
		('szPname',WCHAR*MAXPNAMELEN),
		('dwFormats',DWORD),
		('wChannels',WORD),
		('wReserved1',WORD),
		('dwSupport',DWORD),
	]

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
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		self.makeSettings(settingsSizer)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
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

 	def makeSettings(self, settingsSizer):
		languageSizer=wx.BoxSizer(wx.HORIZONTAL)
		languageLabel=wx.StaticText(self,-1,label=_("&Language (requires restart to fully take affect)"))
		languageSizer.Add(languageLabel)
		languageListID=wx.NewId()
		self.languageNames=languageHandler.getAvailableLanguages()
		self.languageList=wx.Choice(self,languageListID,name=_("Language"),choices=self.languageNames)
		try:
			self.oldLanguage=config.conf["general"]["language"]
			index=self.languageNames.index(self.oldLanguage)
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
		logLevelLabel=wx.StaticText(self,-1,label=_("L&ogging level"))
		logLevelSizer.Add(logLevelLabel)
		logLevelListID=wx.NewId()
		self.logLevelNames=[logging._levelNames[x] for x in sorted([x for x in logging._levelNames.keys() if isinstance(x,int) and x>0],reverse=True)]
		self.logLevelList=wx.Choice(self,languageListID,name=_("Log level"),choices=self.logLevelNames)
		try:
			index=self.logLevelNames.index(logging._levelNames[globalVars.log.getEffectiveLevel()])
			self.logLevelList.SetSelection(index)
		except:
			globalVars.log.warn("Could not set log level list to current log level",exc_info=True) 
		logLevelSizer.Add(self.logLevelList)
		settingsSizer.Add(logLevelSizer,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.languageList.SetFocus()

	def onOk(self,evt):
		newLanguage=self.languageNames[self.languageList.GetSelection()]
		if newLanguage!=self.oldLanguage:
			try:
				languageHandler.setLanguage(newLanguage)
			except:
				globalVars.log.error("languageHandler.setLanguage", exc_info=True)
				wx.MessageDialog(self,_("Error in %s language file")%newLanguage,_("Language Error"),wx.OK|wx.ICON_WARNING).ShowModal()
				return
		config.conf["general"]["language"]=newLanguage
		config.conf["general"]["saveConfigurationOnExit"]=self.saveOnExitCheckBox.IsChecked()
		config.conf["general"]["askToExit"]=self.askToExitCheckBox.IsChecked()
		logLevelName=self.logLevelNames[self.logLevelList.GetSelection()]
		globalVars.log.setLevel(logging._levelNames[logLevelName])
		config.conf["general"]["loggingLevel"]=logLevelName
		if self.oldLanguage!=newLanguage:
			if wx.MessageDialog(self,_("For the new language to take effect, the configuration must be saved and NVDA must be restarted. Press enter to save and restart NVDA, or cancel to manually save and exit at a later time."),_("Language Configuration Change"),wx.OK|wx.CANCEL|wx.ICON_WARNING).ShowModal()==wx.ID_OK:
				config.save()
				queueHandler.queueFunction(queueHandler.interactiveQueue,gui.restart)
		super(GeneralSettingsDialog, self).onOk(evt)

class SynthesizerDialog(SettingsDialog):
	title = _("Synthesizer")

	def makeSettings(self, settingsSizer):
		synthListSizer=wx.BoxSizer(wx.HORIZONTAL)
		synthListLabel=wx.StaticText(self,-1,label=_("&Synthesizer"))
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
		deviceListLabel=wx.StaticText(self,-1,label=_("Output &device"))
		deviceListID=wx.NewId()
		deviceIndex =-1
		numDevices=windll.winmm.waveOutGetNumDevs()
		deviceNames=[]
		self.deviceIndexes=[]
		caps=WAVEOUTCAPS()
		while deviceIndex<numDevices:
			windll.winmm.waveOutGetDevCapsW(deviceIndex,byref(caps),sizeof(caps))
			deviceNames.append(caps.szPname)
			self.deviceIndexes.append(deviceIndex)
			if deviceIndex==config.conf["speech"]["outputDevice"]:
				selection=deviceIndex+1
			deviceIndex=deviceIndex+1
		self.deviceList=wx.Choice(self,deviceListID,choices=deviceNames)
		try:
			self.deviceList.SetSelection(selection)
		except:
			pass
		deviceListSizer.Add(deviceListLabel)
		deviceListSizer.Add(self.deviceList)
		settingsSizer.Add(deviceListSizer,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.synthList.SetFocus()

	def onOk(self,evt):
		config.conf["speech"]["outputDevice"]=self.deviceIndexes[self.deviceList.GetSelection()]
		newSynth=self.synthNames[self.synthList.GetSelection()]
		if not setSynth(newSynth):
			wx.MessageDialog(self,_("Could not load the %s synthesizer.")%newSynth,_("Synthesizer Error"),wx.OK|wx.ICON_WARNING).ShowModal()
			return 
		super(SynthesizerDialog, self).onOk(evt)

class VoiceSettingsDialog(SettingsDialog):
	title = _("Voice settings")

	def makeSettings(self, settingsSizer):
		if getSynth().hasVoice:
			voiceListSizer=wx.BoxSizer(wx.HORIZONTAL)
			voiceListLabel=wx.StaticText(self,-1,label=_("&Voice"))
			voiceListID=wx.NewId()
			self.voiceList=wx.Choice(self,voiceListID,name="Voice:",choices=[getSynth().getVoiceName(x) for x in range(1,getSynth().voiceCount+1)])
			try:
				voiceIndex=getSynth().voice
				voiceIndex-=1
				if voiceIndex>=0 and voiceIndex<getSynth().voiceCount:
					self.voiceList.SetSelection(voiceIndex)
			except:
				pass
			self.voiceList.Bind(wx.EVT_CHOICE,self.onVoiceChange)
			voiceListSizer.Add(voiceListLabel)
			voiceListSizer.Add(self.voiceList)
			settingsSizer.Add(voiceListSizer,border=10,flag=wx.BOTTOM)
		if getSynth().hasVariant:
			variantListSizer=wx.BoxSizer(wx.HORIZONTAL)
			variantListLabel=wx.StaticText(self,-1,label=_("V&ariant"))
			variantListID=wx.NewId()
			self.variantList=wx.Choice(self,variantListID,name="Variant:",choices=[getSynth().getVariantName(x) for x in range(0,getSynth().variantCount)])
			currentVariant=getSynth().variant
			for x in range(0,getSynth().variantCount):
				if currentVariant==getSynth().getVariantIdentifier(x):
					break
			self.variantList.SetSelection(x)
			self.variantList.Bind(wx.EVT_CHOICE,self.onVariantChange)
			variantListSizer.Add(variantListLabel)
			variantListSizer.Add(self.variantList)
			settingsSizer.Add(variantListSizer,border=10,flag=wx.BOTTOM)
		if getSynth().hasRate:
			rateSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
			rateSliderLabel=wx.StaticText(self,-1,label=_("&Rate"))
			rateSliderID=wx.NewId()
			self.rateSlider=wx.Slider(self,rateSliderID,value=getSynth().rate,minValue=0,maxValue=100,name="Rate:")
			self.rateSlider.Bind(wx.EVT_SLIDER,self.onRateChange)
			rateSliderSizer.Add(rateSliderLabel)
			rateSliderSizer.Add(self.rateSlider)
			settingsSizer.Add(rateSliderSizer,border=10,flag=wx.BOTTOM)
		if getSynth().hasPitch:
			pitchSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
			pitchSliderLabel=wx.StaticText(self,-1,label=_("&Pitch"))
			pitchSliderID=wx.NewId()
			self.pitchSlider=wx.Slider(self,pitchSliderID,value=getSynth().pitch,minValue=0,maxValue=100)
			self.pitchSlider.Bind(wx.EVT_SLIDER,self.onPitchChange)
			pitchSliderSizer.Add(pitchSliderLabel)
			pitchSliderSizer.Add(self.pitchSlider)
			settingsSizer.Add(pitchSliderSizer,border=10,flag=wx.BOTTOM)
		if getSynth().hasInflection:
			inflectionSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
			inflectionSliderLabel=wx.StaticText(self,-1,label=_("&Inflection"))
			inflectionSliderID=wx.NewId()
			self.inflectionSlider=wx.Slider(self,inflectionSliderID,value=getSynth().inflection,minValue=0,maxValue=100)
			self.inflectionSlider.Bind(wx.EVT_SLIDER,self.onInflectionChange)
			inflectionSliderSizer.Add(inflectionSliderLabel)
			inflectionSliderSizer.Add(self.inflectionSlider)
			settingsSizer.Add(inflectionSliderSizer,border=10,flag=wx.BOTTOM)
		if getSynth().hasVolume:
			volumeSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
			volumeSliderLabel=wx.StaticText(self,-1,label=_("V&olume"))
			volumeSliderID=wx.NewId()
			self.volumeSlider=wx.Slider(self,volumeSliderID,value=getSynth().volume,minValue=0,maxValue=100)
			self.volumeSlider.Bind(wx.EVT_SLIDER,self.onVolumeChange)
			volumeSliderSizer.Add(volumeSliderLabel)
			volumeSliderSizer.Add(self.volumeSlider)
			settingsSizer.Add(volumeSliderSizer,border=10,flag=wx.BOTTOM)
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

	def postInit(self):
		self.voiceList.SetFocus()

	def onVoiceChange(self,evt):
		changeVoice(getSynth(),evt.GetSelection()+1)
		rate=getSynth().rate
		self.rateSlider.SetValue(rate)
		pitch=getSynth().pitch
		self.pitchSlider.SetValue(pitch)
		volume=getSynth().volume
		self.volumeSlider.SetValue(volume)

	def onVariantChange(self,evt):
		val=evt.GetSelection()
		getSynth().variant=getSynth().getVariantIdentifier(val)

	def onRateChange(self,evt):
		val=evt.GetSelection()
		getSynth().rate=val

	def onPitchChange(self,evt):
		val=evt.GetSelection()
		getSynth().pitch=val

	def onInflectionChange(self,evt):
		val=evt.GetSelection()
		getSynth().inflection=val

	def onVolumeChange(self,evt):
		val=evt.GetSelection()
		getSynth().volume=val

	def onCancel(self,evt):
		if getSynth().hasVoice:
			changeVoice(getSynth(),config.conf["speech"][getSynth().name]["voice"])
		if getSynth().hasVariant:
			getSynth().variant=config.conf["speech"][getSynth().name]["variant"]
		if getSynth().hasRate:
			getSynth().rate=config.conf["speech"][getSynth().name]["rate"]
		if getSynth().hasPitch:
			getSynth().pitch=config.conf["speech"][getSynth().name]["pitch"]
		if getSynth().hasInflection:
			getSynth().inflection=config.conf["speech"][getSynth().name]["inflection"]
		if getSynth().hasVolume:
			getSynth().volume=config.conf["speech"][getSynth().name]["volume"]
		super(VoiceSettingsDialog, self).onCancel(evt)

	def onOk(self,evt):
		if getSynth().hasVoice:
			config.conf["speech"][getSynth().name]["voice"]=self.voiceList.GetSelection()+1
		if getSynth().hasVariant:
			config.conf["speech"][getSynth().name]["variant"]=getSynth().getVariantIdentifier(self.variantList.GetSelection())
		if getSynth().hasRate:
			config.conf["speech"][getSynth().name]["rate"]=self.rateSlider.GetValue()
		if getSynth().hasPitch:
			config.conf["speech"][getSynth().name]["pitch"]=self.pitchSlider.GetValue()
		if getSynth().hasInflection:
			config.conf["speech"][getSynth().name]["inflection"]=self.inflectionSlider.GetValue()
		if getSynth().hasVolume:
			config.conf["speech"][getSynth().name]["volume"]=self.volumeSlider.GetValue()
		config.conf["speech"]["speakPunctuation"]=self.punctuationCheckBox.IsChecked()
		config.conf["speech"][getSynth().name]["raisePitchForCapitals"]=self.raisePitchForCapsCheckBox.IsChecked()
		config.conf["speech"][getSynth().name]["sayCapForCapitals"]=self.sayCapForCapsCheckBox.IsChecked()
		config.conf["speech"][getSynth().name]["beepForCapitals"]=self.beepForCapsCheckBox.IsChecked()
		super(VoiceSettingsDialog, self).onOk(evt)

class KeyboardSettingsDialog(SettingsDialog):
	title = _("Keyboard Settings")

	def makeSettings(self, settingsSizer):
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
		self.capsAsNVDAModifierCheckBox.SetFocus()

	def onOk(self,evt):
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
		self.objectCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &object under mouse"))
		self.objectCheckBox.SetValue(config.conf["mouse"]["reportObjectUnderMouse"])
		settingsSizer.Add(self.objectCheckBox,border=10,flag=wx.BOTTOM)
		self.audioCheckBox=wx.CheckBox(self,wx.NewId(),label=_("play audio coordinates when mouse moves"))
		self.audioCheckBox.SetValue(config.conf["mouse"]["audioCoordinatesOnMouseMove"])
		settingsSizer.Add(self.audioCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.shapeCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["mouse"]["reportMouseShapeChanges"]=self.shapeCheckBox.IsChecked()
		config.conf["mouse"]["reportObjectUnderMouse"]=self.objectCheckBox.IsChecked()
		config.conf["mouse"]["audioCoordinatesOnMouseMove"]=self.audioCheckBox.IsChecked()
		super(MouseSettingsDialog, self).onOk(evt)

class ObjectPresentationDialog(SettingsDialog):
	title = _("Object presentation")

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
		self.stateFirstCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Say object &state first"))
		self.stateFirstCheckBox.SetValue(config.conf["presentation"]["sayStateFirst"])
		settingsSizer.Add(self.stateFirstCheckBox,border=10,flag=wx.BOTTOM)
		self.progressBeepCheckBox=wx.CheckBox(self,wx.NewId(),label=_("&Beep on progress bar updates"))
		self.progressBeepCheckBox.SetValue(config.conf["presentation"]["beepOnProgressBarUpdates"])
		settingsSizer.Add(self.progressBeepCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.tooltipCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["presentation"]["reportTooltips"]=self.tooltipCheckBox.IsChecked()
		config.conf["presentation"]["reportHelpBalloons"]=self.balloonCheckBox.IsChecked()
		config.conf["presentation"]["reportKeyboardShortcuts"]=self.shortcutCheckBox.IsChecked()
		config.conf["presentation"]["reportObjectPositionInformation"]=self.positionInfoCheckBox.IsChecked()
		config.conf["presentation"]["reportObjectDescriptions"]=self.descriptionCheckBox.IsChecked()
		config.conf["presentation"]["sayStateFirst"]=self.stateFirstCheckBox.IsChecked()
		config.conf["presentation"]["beepOnProgressBarUpdates"]=self.progressBeepCheckBox.IsChecked()
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

		self.presentationfocusCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &virtual presentation on focus changes"))
		self.presentationfocusCheckBox.SetValue(config.conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"])
		settingsSizer.Add(self.presentationfocusCheckBox,border=10,flag=wx.BOTTOM)
		self.updateCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Update the content &dynamically"))
		self.updateCheckBox.SetValue(config.conf["virtualBuffers"]["updateContentDynamically"])
		settingsSizer.Add(self.updateCheckBox,border=10,flag=wx.BOTTOM)
		self.linksCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report lin&ks"))
		self.linksCheckBox.SetValue(config.conf["virtualBuffers"]["reportLinks"])
		settingsSizer.Add(self.linksCheckBox,border=10,flag=wx.BOTTOM)
		self.listsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &lists"))
		self.listsCheckBox.SetValue(config.conf["virtualBuffers"]["reportLists"])
		settingsSizer.Add(self.listsCheckBox,border=10,flag=wx.BOTTOM)
		self.listItemsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report list &items"))
		self.listItemsCheckBox.SetValue(config.conf["virtualBuffers"]["reportListItems"])
		settingsSizer.Add(self.listItemsCheckBox,border=10,flag=wx.BOTTOM)
		self.headingsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &headings"))
		self.headingsCheckBox.SetValue(config.conf["virtualBuffers"]["reportHeadings"])
		settingsSizer.Add(self.headingsCheckBox,border=10,flag=wx.BOTTOM)
		self.tablesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &tables"))
		self.tablesCheckBox.SetValue(config.conf["virtualBuffers"]["reportTables"])
		settingsSizer.Add(self.tablesCheckBox,border=10,flag=wx.BOTTOM)
		self.graphicsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &graphics"))
		self.graphicsCheckBox.SetValue(config.conf["virtualBuffers"]["reportGraphics"])
		settingsSizer.Add(self.graphicsCheckBox,border=10,flag=wx.BOTTOM)
		self.formsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report f&orms"))
		self.formsCheckBox.SetValue(config.conf["virtualBuffers"]["reportForms"])
		settingsSizer.Add(self.formsCheckBox,border=10,flag=wx.BOTTOM)
		self.formFieldsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report form &fields"))
		self.formFieldsCheckBox.SetValue(config.conf["virtualBuffers"]["reportFormFields"])
		settingsSizer.Add(self.formFieldsCheckBox,border=10,flag=wx.BOTTOM)
		self.blockQuotesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report block &quotes"))
		self.blockQuotesCheckBox.SetValue(config.conf["virtualBuffers"]["reportBlockQuotes"])
		settingsSizer.Add(self.blockQuotesCheckBox,border=10,flag=wx.BOTTOM)
		self.paragraphsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &paragraphs"))
		self.paragraphsCheckBox.SetValue(config.conf["virtualBuffers"]["reportParagraphs"])
		settingsSizer.Add(self.paragraphsCheckBox,border=10,flag=wx.BOTTOM)
		self.framesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report f&rames"))
		self.framesCheckBox.SetValue(config.conf["virtualBuffers"]["reportFrames"])
		settingsSizer.Add(self.framesCheckBox,border=10,flag=wx.BOTTOM)

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
		config.conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"]=self.presentationfocusCheckBox.IsChecked()
		config.conf["virtualBuffers"]["updateContentDynamically"]=self.updateCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportLinks"]=self.linksCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportLists"]=self.listsCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportListItems"]=self.listItemsCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportHeadings"]=self.headingsCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportTables"]=self.tablesCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportGraphics"]=self.graphicsCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportForms"]=self.formsCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportFormFields"]=self.formFieldsCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportBlockQuotes"]=self.blockQuotesCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportParagraphs"]=self.paragraphsCheckBox.IsChecked()
		config.conf["virtualBuffers"]["reportFrames"]=self.framesCheckBox.IsChecked()
		speech.updateUserDisabledRoles()
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
		self.styleCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report st&yle"))
		self.styleCheckBox.SetValue(config.conf["documentFormatting"]["reportStyle"])
		settingsSizer.Add(self.styleCheckBox,border=10,flag=wx.BOTTOM)
		self.pageCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &pages"))
		self.pageCheckBox.SetValue(config.conf["documentFormatting"]["reportPage"])
		settingsSizer.Add(self.pageCheckBox,border=10,flag=wx.BOTTOM)
		self.lineNumberCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &line numbers"))
		self.lineNumberCheckBox.SetValue(config.conf["documentFormatting"]["reportLineNumber"])
		settingsSizer.Add(self.lineNumberCheckBox,border=10,flag=wx.BOTTOM)
		self.tablesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &tables"))
		self.tablesCheckBox.SetValue(config.conf["documentFormatting"]["reportTables"])
		settingsSizer.Add(self.tablesCheckBox,border=10,flag=wx.BOTTOM)
		self.alignmentCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report &alignment"))
		self.alignmentCheckBox.SetValue(config.conf["documentFormatting"]["reportAlignment"])
		settingsSizer.Add(self.alignmentCheckBox,border=10,flag=wx.BOTTOM)

	def postInit(self):
		self.detectFormatAfterCursorCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["documentFormatting"]["detectFormatAfterCursor"]=self.detectFormatAfterCursorCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontName"]=self.fontNameCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontSize"]=self.fontSizeCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontAttributes"]=self.fontAttrsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportStyle"]=self.styleCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportPage"]=self.pageCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLineNumber"]=self.lineNumberCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportTables"]=self.tablesCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportAlignment"]=self.alignmentCheckBox.IsChecked()
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
