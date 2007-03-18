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
		self.hideInterfaceCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Hide user interface on startup"))
		self.hideInterfaceCheckBox.SetValue(config.conf["general"]["hideInterfaceOnStartup"])
		settingsSizer.Add(self.hideInterfaceCheckBox,border=10,flag=wx.BOTTOM)
		self.saveOnExitCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Save configuration on exit"))
		self.saveOnExitCheckBox.SetValue(config.conf["general"]["saveConfigurationOnExit"])
		settingsSizer.Add(self.saveOnExitCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		languageList.SetFocus()

	def onLanguageChange(self,evt):
		lang=evt.GetString()
		languageHandler.setLanguage(lang)
		config.conf["general"]["language"]=lang

	def onCancel(self,evt):
		languageHandler.setLanguage(self.oldLanguage)
		self.Destroy()

	def onOk(self,evt):
		config.conf["general"]["hideInterfaceOnStartup"]=self.hideInterfaceCheckBox.IsChecked()
		config.conf["general"]["saveConfigurationOnExit"]=self.saveOnExitCheckBox.IsChecked()
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
		self.punctuationCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Speak all punctuation"))
		self.punctuationCheckBox.SetValue(config.conf["speech"]["speakPunctuation"])
		settingsSizer.Add(self.punctuationCheckBox,border=10,flag=wx.BOTTOM)
		self.capsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Say cap before capitals"))
		self.capsCheckBox.SetValue(config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"])
		settingsSizer.Add(self.capsCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		voiceList.SetFocus()

	def onVoiceChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVoice,evt.GetSelection()+1)

	def onRateChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setRate,evt.GetSelection())

	def onPitchChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setPitch,evt.GetSelection())

	def onVolumeChange(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVolume,evt.GetSelection())

	def onCancel(self,evt):
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVoice,self.oldVoice)
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setRate,self.oldRate)
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setPitch,self.oldPitch)
		queueHandler.queueFunction(queueHandler.ID_INTERACTIVE,synthDriverHandler.setVolume,self.oldVolume)
		self.Destroy()

	def onOk(self,evt):
		config.conf["speech"]["speakPunctuation"]=self.punctuationCheckBox.IsChecked()
		config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]=self.capsCheckBox.IsChecked()
		self.Destroy()

class keyboardEchoDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		self.charsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Speak typed characters"))
		self.charsCheckBox.SetValue(config.conf["keyboard"]["speakTypedCharacters"])
		settingsSizer.Add(self.charsCheckBox,border=10,flag=wx.BOTTOM)
		self.wordsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Speak typed words"))
		self.wordsCheckBox.SetValue(config.conf["keyboard"]["speakTypedWords"])
		settingsSizer.Add(self.wordsCheckBox,border=10,flag=wx.BOTTOM)
		self.commandKeysCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Speak command keys"))
		self.commandKeysCheckBox.SetValue(config.conf["keyboard"]["speakCommandKeys"])
		settingsSizer.Add(self.commandKeysCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.charsCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["keyboard"]["speakTypedCharacters"]=self.charsCheckBox.IsChecked()
		config.conf["keyboard"]["speakTypedWords"]=self.wordsCheckBox.IsChecked()
		config.conf["keyboard"]["speakCommandKeys"]=self.commandKeysCheckBox.IsChecked()
		self.Destroy()

class mouseSettingsDialog(wx.Dialog):

 	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		self.shapeCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report mouse shape changes"))
		self.shapeCheckBox.SetValue(config.conf["mouse"]["reportMouseShapeChanges"])
		settingsSizer.Add(self.shapeCheckBox,border=10,flag=wx.BOTTOM)
		self.objectCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report object under mouse"))
		self.objectCheckBox.SetValue(config.conf["mouse"]["reportObjectUnderMouse"])
		settingsSizer.Add(self.objectCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.shapeCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["mouse"]["reportMouseShapeChanges"]=self.shapeCheckBox.IsChecked()
		config.conf["mouse"]["reportObjectUnderMouse"]=self.objectCheckBox.IsChecked()
		self.Destroy()

class objectPresentationDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		self.tooltipCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report tooltips"))
		self.tooltipCheckBox.SetValue(config.conf["presentation"]["reportTooltips"])
		settingsSizer.Add(self.tooltipCheckBox,border=10,flag=wx.BOTTOM)
		self.balloonCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report help balloons"))
		self.balloonCheckBox.SetValue(config.conf["presentation"]["reportHelpBalloons"])
		settingsSizer.Add(self.balloonCheckBox,border=10,flag=wx.BOTTOM)
		self.shortcutCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report object shortcut keys"))
		self.shortcutCheckBox.SetValue(config.conf["presentation"]["reportKeyboardShortcuts"])
		settingsSizer.Add(self.shortcutCheckBox,border=10,flag=wx.BOTTOM)
		self.groupCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report object group names"))
		self.groupCheckBox.SetValue(config.conf["presentation"]["reportObjectGroupNames"])
		settingsSizer.Add(self.groupCheckBox,border=10,flag=wx.BOTTOM)
		self.stateFirstCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Say object state first"))
		self.stateFirstCheckBox.SetValue(config.conf["presentation"]["sayStateFirst"])
		settingsSizer.Add(self.stateFirstCheckBox,border=10,flag=wx.BOTTOM)
		self.progressBeepCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Beep on progress bar updates"))
		self.progressBeepCheckBox.SetValue(config.conf["presentation"]["beepOnProgressBarUpdates"])
		settingsSizer.Add(self.progressBeepCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.tooltipCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["presentation"]["reportTooltips"]=self.tooltipCheckBox.IsChecked()
		config.conf["presentation"]["reportHelpBalloons"]=self.balloonCheckBox.IsChecked()
		config.conf["presentation"]["reportKeyboardShortcuts"]=self.shortcutCheckBox.IsChecked()
		config.conf["presentation"]["reportObjectGroupNames"]=self.groupCheckBox.IsChecked()
		config.conf["presentation"]["sayStateFirst"]=self.stateFirstCheckBox.IsChecked()
		config.conf["presentation"]["beepOnProgressBarUpdates"]=self.progressBeepCheckBox.IsChecked()
		self.Destroy()

class virtualBuffersDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		maxLengthLabel=wx.StaticText(self,-1,label=_("Maximum number of characters on one line"))
		settingsSizer.Add(maxLengthLabel)
		self.maxLengthEdit=wx.TextCtrl(self,wx.NewId())
		self.maxLengthEdit.SetValue(str(config.conf["virtualBuffers"]["maxLineLength"]))
		settingsSizer.Add(self.maxLengthEdit,border=10,flag=wx.BOTTOM)
		pageLinesLabel=wx.StaticText(self,-1,label=_("Number of lines per page"))
		settingsSizer.Add(pageLinesLabel)
		self.pageLinesEdit=wx.TextCtrl(self,wx.NewId())
		self.pageLinesEdit.SetValue(str(config.conf["virtualBuffers"]["linesPerPage"]))
		settingsSizer.Add(self.pageLinesEdit,border=10,flag=wx.BOTTOM)
		self.presentationfocusCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report virtual presentation on focus changes"))
		self.presentationfocusCheckBox.SetValue(config.conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"])
		settingsSizer.Add(self.presentationfocusCheckBox,border=10,flag=wx.BOTTOM)
		self.updateCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Update the content dynamically"))
		self.updateCheckBox.SetValue(config.conf["virtualBuffers"]["updateContentDynamically"])
		settingsSizer.Add(self.updateCheckBox,border=10,flag=wx.BOTTOM)
		self.linksCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report links"))
		self.linksCheckBox.SetValue(config.conf["virtualBuffers"]["reportLinks"])
		settingsSizer.Add(self.linksCheckBox,border=10,flag=wx.BOTTOM)
		self.listsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report lists"))
		self.listsCheckBox.SetValue(config.conf["virtualBuffers"]["reportLists"])
		settingsSizer.Add(self.listsCheckBox,border=10,flag=wx.BOTTOM)
		self.listItemsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report list items"))
		self.listItemsCheckBox.SetValue(config.conf["virtualBuffers"]["reportListItems"])
		settingsSizer.Add(self.listItemsCheckBox,border=10,flag=wx.BOTTOM)
		self.headingsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report headings"))
		self.headingsCheckBox.SetValue(config.conf["virtualBuffers"]["reportHeadings"])
		settingsSizer.Add(self.headingsCheckBox,border=10,flag=wx.BOTTOM)
		self.tablesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report tables"))
		self.tablesCheckBox.SetValue(config.conf["virtualBuffers"]["reportTables"])
		settingsSizer.Add(self.tablesCheckBox,border=10,flag=wx.BOTTOM)
		self.graphicsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report graphics"))
		self.graphicsCheckBox.SetValue(config.conf["virtualBuffers"]["reportGraphics"])
		settingsSizer.Add(self.graphicsCheckBox,border=10,flag=wx.BOTTOM)
		self.formsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report forms"))
		self.formsCheckBox.SetValue(config.conf["virtualBuffers"]["reportForms"])
		settingsSizer.Add(self.formsCheckBox,border=10,flag=wx.BOTTOM)
		self.formFieldsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report form fields"))
		self.formFieldsCheckBox.SetValue(config.conf["virtualBuffers"]["reportFormFields"])
		settingsSizer.Add(self.formFieldsCheckBox,border=10,flag=wx.BOTTOM)
		self.blockQuotesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report block quotes"))
		self.blockQuotesCheckBox.SetValue(config.conf["virtualBuffers"]["reportBlockQuotes"])
		settingsSizer.Add(self.blockQuotesCheckBox,border=10,flag=wx.BOTTOM)
		self.paragraphsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report paragraphs"))
		self.paragraphsCheckBox.SetValue(config.conf["virtualBuffers"]["reportParagraphs"])
		settingsSizer.Add(self.paragraphsCheckBox,border=10,flag=wx.BOTTOM)
		self.framesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report frames"))
		self.framesCheckBox.SetValue(config.conf["virtualBuffers"]["reportFrames"])
		settingsSizer.Add(self.framesCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
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
		self.Destroy()

class documentFormattingDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		self.fontNameCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report font name"))
		self.fontNameCheckBox.SetValue(config.conf["documentFormatting"]["reportFontName"])
		settingsSizer.Add(self.fontNameCheckBox,border=10,flag=wx.BOTTOM)
		self.fontSizeCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report font size"))
		self.fontSizeCheckBox.SetValue(config.conf["documentFormatting"]["reportFontSize"])
		settingsSizer.Add(self.fontSizeCheckBox,border=10,flag=wx.BOTTOM)
		self.fontAttrsCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report font attributes"))
		self.fontAttrsCheckBox.SetValue(config.conf["documentFormatting"]["reportFontAttributes"])
		settingsSizer.Add(self.fontAttrsCheckBox,border=10,flag=wx.BOTTOM)
		self.styleCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report style"))
		self.styleCheckBox.SetValue(config.conf["documentFormatting"]["reportStyle"])
		settingsSizer.Add(self.styleCheckBox,border=10,flag=wx.BOTTOM)
		self.pageCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report pages"))
		self.pageCheckBox.SetValue(config.conf["documentFormatting"]["reportPage"])
		settingsSizer.Add(self.pageCheckBox,border=10,flag=wx.BOTTOM)
		self.lineNumberCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report line numbers"))
		self.lineNumberCheckBox.SetValue(config.conf["documentFormatting"]["reportLineNumber"])
		settingsSizer.Add(self.lineNumberCheckBox,border=10,flag=wx.BOTTOM)
		self.tablesCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report tables"))
		self.tablesCheckBox.SetValue(config.conf["documentFormatting"]["reportTables"])
		settingsSizer.Add(self.tablesCheckBox,border=10,flag=wx.BOTTOM)
		self.alignmentCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Report alignment"))
		self.alignmentCheckBox.SetValue(config.conf["documentFormatting"]["reportAlignment"])
		settingsSizer.Add(self.alignmentCheckBox,border=10,flag=wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.fontNameCheckBox.SetFocus()

	def onOk(self,evt):
		config.conf["documentFormatting"]["reportFontName"]=self.fontNameCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontSize"]=self.fontSizeCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportFontAttributes"]=self.fontAttrsCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportStyle"]=self.styleCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportPage"]=self.pageCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportLineNumber"]=self.lineNumberCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportTables"]=self.tablesCheckBox.IsChecked()
		config.conf["documentFormatting"]["reportAlignment"]=self.alignmentCheckBox.IsChecked()
		self.Destroy()
