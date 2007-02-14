#settingsDialogs.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import wx
import synthDriverHandler
import debug
import config
import core
import audio

class interfaceSettingsDialog(wx.Dialog):

 	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		languageSizer=wx.BoxSizer(wx.HORIZONTAL)
		languageLabel=wx.StaticText(self,-1,label=_("Language (requires restart to fully take affect)"))
		languageSizer.Add(languageLabel)
		languageListID=wx.NewId()
		languages=[x for x in os.listdir('locale') if not x.startswith('.')]
		languageList=wx.Choice(self,languageListID,name=_("Language"),choices=languages)
		try:
			index=languages.index(config.conf["general"]["language"])
			languageList.SetSelection(index)
		except:
			pass
		languageList.Bind(wx.EVT_CHOICE,self.onLanguageChange)
		languageSizer.Add(languageList)
		settingsSizer.Add(languageSizer,border=10,flag=wx.BOTTOM)
		hideInterfaceCheckBoxID=wx.NewId()
		hideInterfaceCheckBox=wx.CheckBox(self,hideInterfaceCheckBoxID,label=_("Hide user interface on startup"))
		hideInterfaceCheckBox.SetValue(config.conf["general"]["hideInterfaceOnStartup"])
		hideInterfaceCheckBox.Bind(wx.EVT_CHECKBOX,self.onHideInterfaceChange)
		settingsSizer.Add(hideInterfaceCheckBox,border=10,flag=wx.BOTTOM)
		saveOnExitCheckBoxID=wx.NewId()
		saveOnExitCheckBox=wx.CheckBox(self,saveOnExitCheckBoxID,label=_("Save configuration on exit"))
		saveOnExitCheckBox.SetValue(config.conf["general"]["saveConfigurationOnExit"])
		saveOnExitCheckBox.Bind(wx.EVT_CHECKBOX,self.onSaveOnExitChange)
		settingsSizer.Add(saveOnExitCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		languageList.SetFocus()

	def onLanguageChange(self,evt):
		lang=evt.GetString()
		core.setLanguage(lang)
		config.conf["general"]["language"]=lang

	def onHideInterfaceChange(self,evt):
		config.conf["general"]["hideInterfaceOnStartup"]=evt.IsChecked()

	def onSaveOnExitChange(self,evt):
		config.conf["general"]["saveConfigurationOnExit"]=evt.IsChecked()

class voiceSettingsDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		voiceListSizer=wx.BoxSizer(wx.HORIZONTAL)
		voiceListLabel=wx.StaticText(self,-1,label=_("Voice"))
		voiceListID=wx.NewId()
		voiceList=wx.Choice(self,voiceListID,name="Voice:",choices=synthDriverHandler.driverVoiceNames)
		try:
			voiceIndex=synthDriverHandler.getVoice()-1
			if voiceIndex>=0 and voiceIndex<len(synthDriverHandler.driverVoiceNames):
				voiceList.SetSelection(voiceIndex)
		except:
			pass
		voiceList.Bind(wx.EVT_CHOICE,self.onVoiceChange)
		voiceListSizer.Add(voiceListLabel)
		voiceListSizer.Add(voiceList)
		settingsSizer.Add(voiceListSizer,border=10,flag=wx.BOTTOM)
		rateSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		rateSliderLabel=wx.StaticText(self,-1,label=_("Rate"))
		rateSliderID=wx.NewId()
		rateSlider=wx.Slider(self,rateSliderID,value=synthDriverHandler.getRate(),minValue=0,maxValue=100,name="Rate:")
		rateSlider.Bind(wx.EVT_SLIDER,self.onRateChange)
		rateSliderSizer.Add(rateSliderLabel)
		rateSliderSizer.Add(rateSlider)
		settingsSizer.Add(rateSliderSizer,border=10,flag=wx.BOTTOM)
		pitchSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		pitchSliderLabel=wx.StaticText(self,-1,label=_("Pitch"))
		pitchSliderID=wx.NewId()
		pitchSlider=wx.Slider(self,pitchSliderID,value=synthDriverHandler.getPitch(),minValue=0,maxValue=100)
		pitchSlider.Bind(wx.EVT_SLIDER,self.onPitchChange)
		pitchSliderSizer.Add(pitchSliderLabel)
		pitchSliderSizer.Add(pitchSlider)
		settingsSizer.Add(pitchSliderSizer,border=10,flag=wx.BOTTOM)
		volumeSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		volumeSliderLabel=wx.StaticText(self,-1,label=_("Volume"))
		volumeSliderID=wx.NewId()
		volumeSlider=wx.Slider(self,volumeSliderID,value=synthDriverHandler.getVolume(),minValue=0,maxValue=100)
		volumeSlider.Bind(wx.EVT_SLIDER,self.onVolumeChange)
		volumeSliderSizer.Add(volumeSliderLabel)
		volumeSliderSizer.Add(volumeSlider)
		settingsSizer.Add(volumeSliderSizer,border=10,flag=wx.BOTTOM)
		punctuationCheckBoxID=wx.NewId()
		punctuationCheckBox=wx.CheckBox(self,punctuationCheckBoxID,label=_("Speak all punctuation"))
		punctuationCheckBox.SetValue(config.conf["speech"]["speakPunctuation"])
		punctuationCheckBox.Bind(wx.EVT_CHECKBOX,self.onPunctuationChange)
		settingsSizer.Add(punctuationCheckBox,border=10,flag=wx.BOTTOM)
		capsCheckBoxID=wx.NewId()
		capsCheckBox=wx.CheckBox(self,capsCheckBoxID,label=_("Say cap before capitals"))
		capsCheckBox.SetValue(config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"])
		capsCheckBox.Bind(wx.EVT_CHECKBOX,self.onCapsChange)
		settingsSizer.Add(capsCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		voiceList.SetFocus()

	def onVoiceChange(self,evt):
		core.executeFunction(core.EXEC_SPEECH,synthDriverHandler.setVoice,evt.GetSelection()+1)

	def onRateChange(self,evt):
		core.executeFunction(core.EXEC_SPEECH,synthDriverHandler.setRate,evt.GetSelection())

	def onPitchChange(self,evt):
		core.executeFunction(core.EXEC_SPEECH,synthDriverHandler.setPitch,evt.GetSelection())

	def onVolumeChange(self,evt):
		core.executeFunction(core.EXEC_SPEECH,synthDriverHandler.setVolume,evt.GetSelection())

	def onPunctuationChange(self,evt):
		config.conf["speech"]["speakPunctuation"]=evt.IsChecked()
		debug.writeMessage("checK %s"%evt.IsChecked())

	def onCapsChange(self,evt):
		config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]=evt.IsChecked()

class keyboardEchoDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		charsCheckBoxID=wx.NewId()
		charsCheckBox=wx.CheckBox(self,charsCheckBoxID,label=_("Speak typed characters"))
		charsCheckBox.SetValue(config.conf["keyboard"]["speakTypedCharacters"])
		wx.EVT_CHECKBOX(self,charsCheckBoxID,self.onCharsChange)
		settingsSizer.Add(charsCheckBox,border=10,flag=wx.BOTTOM)
		wordsCheckBoxID=wx.NewId()
		wordsCheckBox=wx.CheckBox(self,wordsCheckBoxID,label=_("Speak typed words"))
		wordsCheckBox.SetValue(config.conf["keyboard"]["speakTypedWords"])
		wx.EVT_CHECKBOX(self,wordsCheckBoxID,self.onWordsChange)
		settingsSizer.Add(wordsCheckBox,border=10,flag=wx.BOTTOM)
		commandKeysCheckBoxID=wx.NewId()
		commandKeysCheckBox=wx.CheckBox(self,commandKeysCheckBoxID,label=_("Speak command keys"))
		commandKeysCheckBox.SetValue(config.conf["keyboard"]["speakCommandKeys"])
		wx.EVT_CHECKBOX(self,commandKeysCheckBoxID,self.onCommandKeysChange)
		settingsSizer.Add(commandKeysCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		charsCheckBox.SetFocus()

	def onCharsChange(self,evt):
		config.conf["keyboard"]["speakTypedCharacters"]=evt.IsChecked()

	def onWordsChange(self,evt):
		config.conf["keyboard"]["speakTypedWords"]=evt.IsChecked()

	def onCommandKeysChange(self,evt):
		config.conf["keyboard"]["speakCommandKeys"]=evt.IsChecked()

class mouseSettingsDialog(wx.Dialog):

 	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		shapeCheckBoxID=wx.NewId()
		shapeCheckBox=wx.CheckBox(self,shapeCheckBoxID,label=_("Report mouse shape changes"))
		shapeCheckBox.SetValue(config.conf["mouse"]["reportMouseShapeChanges"])
		wx.EVT_CHECKBOX(self,shapeCheckBoxID,self.onShapeChange)
		settingsSizer.Add(shapeCheckBox,border=10,flag=wx.BOTTOM)
		objectCheckBoxID=wx.NewId()
		objectCheckBox=wx.CheckBox(self,objectCheckBoxID,label=_("Report object under mouse"))
		objectCheckBox.SetValue(config.conf["mouse"]["reportObjectUnderMouse"])
		wx.EVT_CHECKBOX(self,objectCheckBoxID,self.onObjectChange)
		settingsSizer.Add(objectCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		shapeCheckBox.SetFocus()

	def onShapeChange(self,evt):
		config.conf["mouse"]["reportMouseShapeChanges"]=evt.IsChecked()

	def onObjectChange(self,evt):
		config.conf["mouse"]["reportObjectUnderMouse"]=evt.IsChecked()

class objectPresentationDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		tooltipCheckBoxID=wx.NewId()
		tooltipCheckBox=wx.CheckBox(self,tooltipCheckBoxID,label=_("Report tooltips"))
		tooltipCheckBox.SetValue(config.conf["presentation"]["reportTooltips"])
		wx.EVT_CHECKBOX(self,tooltipCheckBoxID,self.onTooltipChange)
		settingsSizer.Add(tooltipCheckBox,border=10,flag=wx.BOTTOM)
		balloonCheckBoxID=wx.NewId()
		balloonCheckBox=wx.CheckBox(self,balloonCheckBoxID,label=_("Report help balloons"))
		balloonCheckBox.SetValue(config.conf["presentation"]["reportHelpBalloons"])
		wx.EVT_CHECKBOX(self,balloonCheckBoxID,self.onBalloonChange)
		settingsSizer.Add(balloonCheckBox,border=10,flag=wx.BOTTOM)
		shortcutCheckBoxID=wx.NewId()
		shortcutCheckBox=wx.CheckBox(self,shortcutCheckBoxID,label=_("Report object shortcut keys"))
		shortcutCheckBox.SetValue(config.conf["presentation"]["reportKeyboardShortcuts"])
		wx.EVT_CHECKBOX(self,shortcutCheckBoxID,self.onShortcutChange)
		settingsSizer.Add(shortcutCheckBox,border=10,flag=wx.BOTTOM)
		groupCheckBoxID=wx.NewId()
		groupCheckBox=wx.CheckBox(self,groupCheckBoxID,label=_("Report object group names"))
		groupCheckBox.SetValue(config.conf["presentation"]["reportObjectGroupNames"])
		wx.EVT_CHECKBOX(self,groupCheckBoxID,self.onGroupChange)
		settingsSizer.Add(groupCheckBox,border=10,flag=wx.BOTTOM)
		stateFirstCheckBoxID=wx.NewId()
		stateFirstCheckBox=wx.CheckBox(self,stateFirstCheckBoxID,label=_("Say object state first"))
		stateFirstCheckBox.SetValue(config.conf["presentation"]["sayStateFirst"])
		wx.EVT_CHECKBOX(self,stateFirstCheckBoxID,self.onStateFirstChange)
		settingsSizer.Add(stateFirstCheckBox,border=10,flag=wx.BOTTOM)
		progressBeepCheckBoxID=wx.NewId()
		progressBeepCheckBox=wx.CheckBox(self,progressBeepCheckBoxID,label=_("Beep on progress bar updates"))
		progressBeepCheckBox.SetValue(config.conf["presentation"]["beepOnProgressBarUpdates"])
		wx.EVT_CHECKBOX(self,progressBeepCheckBoxID,self.onProgressBeepChange)
		settingsSizer.Add(progressBeepCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		tooltipCheckBox.SetFocus()

	def onTooltipChange(self,evt):
		config.conf["presentation"]["reportTooltips"]=evt.IsChecked()

	def onBalloonChange(self,evt):
		config.conf["presentation"]["reportHelpBalloons"]=evt.IsChecked()

	def onShortcutChange(self,evt):
		config.conf["presentation"]["reportKeyboardShortcuts"]=evt.IsChecked()

	def onGroupChange(self,evt):
		config.conf["presentation"]["reportObjectGroupNames"]=evt.IsChecked()

	def onStateFirstChange(self,evt):
		config.conf["presentation"]["sayStateFirst"]=evt.IsChecked()

	def onProgressBeepChange(self,evt):
		config.conf["presentation"]["beepOnProgressBarUpdates"]=evt.IsChecked()
