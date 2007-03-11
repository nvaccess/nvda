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
import queueHandler
import languageHandler
import audio
from wx.lib.masked import textctrl

class interfaceSettingsDialog(wx.Dialog):

 	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		languageSizer=wx.BoxSizer(wx.HORIZONTAL)
		languageLabel=wx.StaticText(self,-1,label=_("Language (requires restart to fully take affect)"))
		languageSizer.Add(languageLabel)
		languageListID=wx.NewId()
		languages=languageHandler.getAvailableLanguages()
		languageList=wx.Choice(self,languageListID,name=_("Language"),choices=languages)
		try:
			self.oldLanguage=config.conf["general"]["language"]
			index=languages.index(self.oldLanguage)
			languageList.SetSelection(index)
		except:
			pass
		languageList.Bind(wx.EVT_CHOICE,self.onLanguageChange)
		languageSizer.Add(languageList)
		settingsSizer.Add(languageSizer,border=10,flag=wx.BOTTOM)
		hideInterfaceCheckBoxID=wx.NewId()
		hideInterfaceCheckBox=wx.CheckBox(self,hideInterfaceCheckBoxID,label=_("Hide user interface on startup"))
		self.oldHideInterface=config.conf["general"]["hideInterfaceOnStartup"]
		hideInterfaceCheckBox.SetValue(self.oldHideInterface)
		hideInterfaceCheckBox.Bind(wx.EVT_CHECKBOX,self.onHideInterfaceChange)
		settingsSizer.Add(hideInterfaceCheckBox,border=10,flag=wx.BOTTOM)
		saveOnExitCheckBoxID=wx.NewId()
		saveOnExitCheckBox=wx.CheckBox(self,saveOnExitCheckBoxID,label=_("Save configuration on exit"))
		self.oldSaveOnExit=config.conf["general"]["saveConfigurationOnExit"]
		saveOnExitCheckBox.SetValue(self.oldSaveOnExit)
		saveOnExitCheckBox.Bind(wx.EVT_CHECKBOX,self.onSaveOnExitChange)
		settingsSizer.Add(saveOnExitCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		languageList.SetFocus()

	def onLanguageChange(self,evt):
		lang=evt.GetString()
		languageHandler.setLanguage(lang)
		config.conf["general"]["language"]=lang

	def onHideInterfaceChange(self,evt):
		config.conf["general"]["hideInterfaceOnStartup"]=evt.IsChecked()

	def onSaveOnExitChange(self,evt):
		config.conf["general"]["saveConfigurationOnExit"]=evt.IsChecked()

	def onCancel(self,evt):
		languageHandler.setLanguage(self.oldLanguage)
		config.conf["general"]["hideInterfaceOnStartup"]=self.oldHideInterface
		config.conf["general"]["saveConfigurationOnExit"]=self.oldSaveOnExit
		self.Destroy()

class synthesizerDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		synthListSizer=wx.BoxSizer(wx.HORIZONTAL)
		synthListLabel=wx.StaticText(self,-1,label=_("Synthesizer"))
		synthListID=wx.NewId()
		driverList=synthDriverHandler.getDriverList()
		self.synthNames=[x[0] for x in driverList]
		options=['%s, %s'%x for x in driverList]
		self.synthList=wx.Choice(self,synthListID,choices=options)
		try:
			index=self.synthNames.index(synthDriverHandler.driverName)
			self.synthList.SetSelection(index)
		except:
			pass
		synthListSizer.Add(synthListLabel)
		synthListSizer.Add(self.synthList)
		settingsSizer.Add(synthListSizer,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.synthList.SetFocus()

	def onOk(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setDriver,self.synthNames[self.synthList.GetSelection()])
		self.Destroy()

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
			voiceIndex=self.oldVoice=synthDriverHandler.getVoice()
			voiceIndex-=1
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
		self.oldRate=synthDriverHandler.getRate()
		rateSlider=wx.Slider(self,rateSliderID,value=self.oldRate,minValue=0,maxValue=100,name="Rate:")
		rateSlider.Bind(wx.EVT_SLIDER,self.onRateChange)
		rateSliderSizer.Add(rateSliderLabel)
		rateSliderSizer.Add(rateSlider)
		settingsSizer.Add(rateSliderSizer,border=10,flag=wx.BOTTOM)
		pitchSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		pitchSliderLabel=wx.StaticText(self,-1,label=_("Pitch"))
		pitchSliderID=wx.NewId()
		self.oldPitch=synthDriverHandler.getPitch()
		pitchSlider=wx.Slider(self,pitchSliderID,value=self.oldPitch,minValue=0,maxValue=100)
		pitchSlider.Bind(wx.EVT_SLIDER,self.onPitchChange)
		pitchSliderSizer.Add(pitchSliderLabel)
		pitchSliderSizer.Add(pitchSlider)
		settingsSizer.Add(pitchSliderSizer,border=10,flag=wx.BOTTOM)
		volumeSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		volumeSliderLabel=wx.StaticText(self,-1,label=_("Volume"))
		volumeSliderID=wx.NewId()
		self.oldVolume=synthDriverHandler.getVolume()
		volumeSlider=wx.Slider(self,volumeSliderID,value=self.oldVolume,minValue=0,maxValue=100)
		volumeSlider.Bind(wx.EVT_SLIDER,self.onVolumeChange)
		volumeSliderSizer.Add(volumeSliderLabel)
		volumeSliderSizer.Add(volumeSlider)
		settingsSizer.Add(volumeSliderSizer,border=10,flag=wx.BOTTOM)
		punctuationCheckBoxID=wx.NewId()
		punctuationCheckBox=wx.CheckBox(self,punctuationCheckBoxID,label=_("Speak all punctuation"))
		self.oldPunctuation=config.conf["speech"]["speakPunctuation"]
		punctuationCheckBox.SetValue(self.oldPunctuation)
		punctuationCheckBox.Bind(wx.EVT_CHECKBOX,self.onPunctuationChange)
		settingsSizer.Add(punctuationCheckBox,border=10,flag=wx.BOTTOM)
		capsCheckBoxID=wx.NewId()
		capsCheckBox=wx.CheckBox(self,capsCheckBoxID,label=_("Say cap before capitals"))
		self.oldCaps=config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]
		capsCheckBox.SetValue(self.oldCaps)
		capsCheckBox.Bind(wx.EVT_CHECKBOX,self.onCapsChange)
		settingsSizer.Add(capsCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		voiceList.SetFocus()

	def onVoiceChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVoice,evt.GetSelection()+1)

	def onRateChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setRate,evt.GetSelection())

	def onPitchChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setPitch,evt.GetSelection())

	def onVolumeChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVolume,evt.GetSelection())

	def onPunctuationChange(self,evt):
		config.conf["speech"]["speakPunctuation"]=evt.IsChecked()
		debug.writeMessage("checK %s"%evt.IsChecked())

	def onCapsChange(self,evt):
		config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]=evt.IsChecked()

	def onCancel(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVoice,self.oldVoice)
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setRate,self.oldRate)
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setPitch,self.oldPitch)
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVolume,self.oldVolume)
		config.conf["speech"]["speakPunctuation"]=self.oldPunctuation
		config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]=self.oldCaps
		self.Destroy()

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

class virtualBuffersDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		presentationfocusCheckBoxID=wx.NewId()
		presentationfocusCheckBox=wx.CheckBox(self,presentationfocusCheckBoxID,label=_("Report virtual presentation on focus changes"))
		presentationfocusCheckBox.SetValue(config.conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"])
#		wx.EVT_CHECKBOX(self,presentationfocusCheckBoxID,self.onPresentationfocusChange)
#		settingsSizer.Add(presentationfocusCheckBox,border=10,flag=wx.BOTTOM)
		updateCheckBoxID=wx.NewId()
		updateCheckBox=wx.CheckBox(self,updateCheckBoxID,label=_("Update the content dynamically"))
		updateCheckBox.SetValue(config.conf["virtualBuffers"]["updateContentDynamically"])
		wx.EVT_CHECKBOX(self,updateCheckBoxID,self.onUpdateChange)
		settingsSizer.Add(updateCheckBox,border=10,flag=wx.BOTTOM)
		linksCheckBoxID=wx.NewId()
		linksCheckBox=wx.CheckBox(self,linksCheckBoxID,label=_("Report links"))
		linksCheckBox.SetValue(config.conf["virtualBuffers"]["reportLinks"])
		wx.EVT_CHECKBOX(self,linksCheckBoxID,self.onLinksChange)
		settingsSizer.Add(linksCheckBox,border=10,flag=wx.BOTTOM)
		listsCheckBoxID=wx.NewId()
		listsCheckBox=wx.CheckBox(self,listsCheckBoxID,label=_("Report lists"))
		listsCheckBox.SetValue(config.conf["virtualBuffers"]["reportLists"])
		wx.EVT_CHECKBOX(self,listsCheckBoxID,self.onListsChange)
		settingsSizer.Add(listsCheckBox,border=10,flag=wx.BOTTOM)
		listItemsCheckBoxID=wx.NewId()
		listItemsCheckBox=wx.CheckBox(self,listItemsCheckBoxID,label=_("Report list items"))
		listItemsCheckBox.SetValue(config.conf["virtualBuffers"]["reportListItems"])
		wx.EVT_CHECKBOX(self,listItemsCheckBoxID,self.onListItemsChange)
		settingsSizer.Add(listItemsCheckBox,border=10,flag=wx.BOTTOM)
		headingsCheckBoxID=wx.NewId()
		headingsCheckBox=wx.CheckBox(self,headingsCheckBoxID,label=_("Report headings"))
		headingsCheckBox.SetValue(config.conf["virtualBuffers"]["reportHeadings"])
		wx.EVT_CHECKBOX(self,headingsCheckBoxID,self.onHeadingsChange)
		settingsSizer.Add(headingsCheckBox,border=10,flag=wx.BOTTOM)
		tablesCheckBoxID=wx.NewId()
		tablesCheckBox=wx.CheckBox(self,tablesCheckBoxID,label=_("Report tables"))
		tablesCheckBox.SetValue(config.conf["virtualBuffers"]["reportTables"])
		wx.EVT_CHECKBOX(self,tablesCheckBoxID,self.onTablesChange)
		settingsSizer.Add(tablesCheckBox,border=10,flag=wx.BOTTOM)
		graphicsCheckBoxID=wx.NewId()
		graphicsCheckBox=wx.CheckBox(self,graphicsCheckBoxID,label=_("Report graphics"))
		graphicsCheckBox.SetValue(config.conf["virtualBuffers"]["reportGraphics"])
		wx.EVT_CHECKBOX(self,graphicsCheckBoxID,self.onGraphicsChange)
		settingsSizer.Add(graphicsCheckBox,border=10,flag=wx.BOTTOM)
		formsCheckBoxID=wx.NewId()
		formsCheckBox=wx.CheckBox(self,formsCheckBoxID,label=_("Report forms"))
		formsCheckBox.SetValue(config.conf["virtualBuffers"]["reportForms"])
		wx.EVT_CHECKBOX(self,formsCheckBoxID,self.onFormsChange)
		settingsSizer.Add(formsCheckBox,border=10,flag=wx.BOTTOM)
		formFieldsCheckBoxID=wx.NewId()
		formFieldsCheckBox=wx.CheckBox(self,formFieldsCheckBoxID,label=_("Report form fields"))
		formFieldsCheckBox.SetValue(config.conf["virtualBuffers"]["reportFormFields"])
		wx.EVT_CHECKBOX(self,formFieldsCheckBoxID,self.onFormFieldsChange)
		settingsSizer.Add(formFieldsCheckBox,border=10,flag=wx.BOTTOM)
		blockQuotesCheckBoxID=wx.NewId()
		blockQuotesCheckBox=wx.CheckBox(self,blockQuotesCheckBoxID,label=_("Report block quotes"))
		blockQuotesCheckBox.SetValue(config.conf["virtualBuffers"]["reportBlockQuotes"])
		wx.EVT_CHECKBOX(self,blockQuotesCheckBoxID,self.onBlockQuotesChange)
		settingsSizer.Add(blockQuotesCheckBox,border=10,flag=wx.BOTTOM)
		paragraphsCheckBoxID=wx.NewId()
		paragraphsCheckBox=wx.CheckBox(self,paragraphsCheckBoxID,label=_("Report paragraphs"))
		paragraphsCheckBox.SetValue(config.conf["virtualBuffers"]["reportParagraphs"])
		wx.EVT_CHECKBOX(self,paragraphsCheckBoxID,self.onParagraphsChange)
		settingsSizer.Add(paragraphsCheckBox,border=10,flag=wx.BOTTOM)
		framesCheckBoxID=wx.NewId()
		framesCheckBox=wx.CheckBox(self,framesCheckBoxID,label=_("Report frames"))
		framesCheckBox.SetValue(config.conf["virtualBuffers"]["reportFrames"])
		wx.EVT_CHECKBOX(self,framesCheckBoxID,self.onFramesChange)
		settingsSizer.Add(framesCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		presentationfocusCheckBox.SetFocus()

	def onPresentationfocusChange(self,evt):
		config.conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"]=evt.IsChecked()

	def onUpdateChange(self,evt):
		config.conf["virtualBuffers"]["updateContentDynamically"]=evt.IsChecked()

	def onLinksChange(self,evt):
		config.conf["virtualBuffers"]["reportLinks"]=evt.IsChecked()

	def onListsChange(self,evt):
		config.conf["virtualBuffers"]["reportLists"]=evt.IsChecked()

	def onListItemsChange(self,evt):
		config.conf["virtualBuffers"]["reportListItems"]=evt.IsChecked()

	def onHeadingsChange(self,evt):
		config.conf["virtualBuffers"]["reportHeadings"]=evt.IsChecked()

	def onTablesChange(self,evt):
		config.conf["virtualBuffers"]["reportTables"]=evt.IsChecked()

	def onGraphicsChange(self,evt):
		config.conf["virtualBuffers"]["reportGraphics"]=evt.IsChecked()

	def onFormsChange(self,evt):
		config.conf["virtualBuffers"]["reportForms"]=evt.IsChecked()

	def onFormFieldsChange(self,evt):
		config.conf["virtualBuffers"]["reportFormFields"]=evt.IsChecked()

	def onBlockQuotesChange(self,evt):
		config.conf["virtualBuffers"]["reportBlockQuotes"]=evt.IsChecked()

	def onParagraphsChange(self,evt):
		config.conf["virtualBuffers"]["reportParagraphs"]=evt.IsChecked()

	def onFramesChange(self,evt):
		config.conf["virtualBuffers"]["reportFrames"]=evt.IsChecked()
