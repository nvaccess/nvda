import wx
import synthDriverHandler
import debug
import config

class voiceSettingsDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		message=wx.StaticText(self,-1,label=_("Set the voice, rate, pitch and volume that you prefer."))
		mainSizer.Add(message)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		voiceListSizer=wx.BoxSizer(wx.HORIZONTAL)
		voiceListLabel=wx.StaticText(self,-1,label=_("Voice"))
		voiceListID=wx.NewId()
		voiceList=wx.Choice(self,voiceListID,name="Voice:",choices=synthDriverHandler.driverVoiceNames)
		voiceList.SetSelection(synthDriverHandler.getVoice()-1)
		wx.EVT_CHOICE(self,voiceListID,self.onVoiceChange)
		voiceListSizer.Add(voiceListLabel)
		voiceListSizer.Add(voiceList)
		settingsSizer.Add(voiceListSizer)
		rateSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		rateSliderLabel=wx.StaticText(self,-1,label=_("Rate"))
		rateSliderID=wx.NewId()
		rateSlider=wx.Slider(self,rateSliderID,value=synthDriverHandler.getRate(),minValue=0,maxValue=100,name="Rate:")
		wx.EVT_SLIDER(self,rateSliderID,self.onRateChange)
		rateSliderSizer.Add(rateSliderLabel)
		rateSliderSizer.Add(rateSlider)
		settingsSizer.Add(rateSliderSizer)
		pitchSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		pitchSliderLabel=wx.StaticText(self,-1,label=_("Pitch"))
		pitchSliderID=wx.NewId()
		pitchSlider=wx.Slider(self,pitchSliderID,value=synthDriverHandler.getPitch(),minValue=0,maxValue=100)
		wx.EVT_SLIDER(self,pitchSliderID,self.onPitchChange)
		pitchSliderSizer.Add(pitchSliderLabel)
		pitchSliderSizer.Add(pitchSlider)
		settingsSizer.Add(pitchSliderSizer)
		volumeSliderSizer=wx.BoxSizer(wx.HORIZONTAL)
		volumeSliderLabel=wx.StaticText(self,-1,label=_("Volume"))
		volumeSliderID=wx.NewId()
		volumeSlider=wx.Slider(self,volumeSliderID,value=synthDriverHandler.getVolume(),minValue=0,maxValue=100)
		wx.EVT_SLIDER(self,volumeSliderID,self.onVolumeChange)
		volumeSliderSizer.Add(volumeSliderLabel)
		volumeSliderSizer.Add(volumeSlider)
		settingsSizer.Add(volumeSliderSizer)
		punctuationCheckBoxID=wx.NewId()
		punctuationCheckBox=wx.CheckBox(self,punctuationCheckBoxID,label=_("Speak all punctuation"))
		punctuationCheckBox.SetValue(config.conf["speech"]["speakPunctuation"])
		wx.EVT_CHECKBOX(self,punctuationCheckBoxID,self.onPunctuationChange)
		settingsSizer.Add(punctuationCheckBox)
		capsCheckBoxID=wx.NewId()
		capsCheckBox=wx.CheckBox(self,capsCheckBoxID,label=_("Say cap before capitals"))
		capsCheckBox.SetValue(config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"])
		wx.EVT_CHECKBOX(self,capsCheckBoxID,self.onCapsChange)
		settingsSizer.Add(capsCheckBox)
		mainSizer.Add(settingsSizer)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer)
		self.SetSizer(mainSizer)

	def onVoiceChange(self,evt):
		synthDriverHandler.setVoice(evt.GetSelection()+1)

	def onRateChange(self,evt):
		synthDriverHandler.setRate(evt.GetSelection())

	def onPitchChange(self,evt):
		synthDriverHandler.setPitch(evt.GetSelection())

	def onVolumeChange(self,evt):
		synthDriverHandler.setVolume(evt.GetSelection())

	def onPunctuationChange(self,evt):
		config.conf["speech"]["speakPunctuation"]=evt.IsChecked()
		debug.writeMessage("checK %s"%evt.IsChecked())

	def onCapsChange(self,evt):
		config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]=evt.IsChecked()

class keyboardEchoDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.HORIZONTAL)
		message=wx.StaticText(self,-1,label=_("Choose whether to echo any of typed characters, words, or command keys."))
		mainSizer.Add(message)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		charsCheckBoxID=wx.NewId()
		charsCheckBox=wx.CheckBox(self,charsCheckBoxID,label=_("Speak typed characters"))
		charsCheckBox.SetValue(config.conf["keyboard"]["speakTypedCharacters"])
		wx.EVT_CHECKBOX(self,charsCheckBoxID,self.onCharsChange)
		settingsSizer.Add(charsCheckBox)
		wordsCheckBoxID=wx.NewId()
		wordsCheckBox=wx.CheckBox(self,wordsCheckBoxID,label=_("Speak typed words"))
		wordsCheckBox.SetValue(config.conf["keyboard"]["speakTypedWords"])
		wx.EVT_CHECKBOX(self,wordsCheckBoxID,self.onWordsChange)
		settingsSizer.Add(wordsCheckBox)
		commandKeysCheckBoxID=wx.NewId()
		commandKeysCheckBox=wx.CheckBox(self,commandKeysCheckBoxID,label=_("Speak command keys"))
		commandKeysCheckBox.SetValue(config.conf["keyboard"]["speakCommandKeys"])
		wx.EVT_CHECKBOX(self,commandKeysCheckBoxID,self.onCommandKeysChange)
		settingsSizer.Add(commandKeysCheckBox)
		mainSizer.Add(settingsSizer)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer)
		self.SetSizer(mainSizer)

	def onCharsChange(self,evt):
		config.conf["keyboard"]["speakTypedCharacters"]=evt.IsChecked()

	def onWordsChange(self,evt):
		config.conf["keyboard"]["speakTypedWords"]=evt.IsChecked()

	def onCommandKeysChange(self,evt):
		config.conf["keyboard"]["speakCommandKeys"]=evt.IsChecked()

class mouseSettingsDialog(wx.Dialog):

 	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.HORIZONTAL)
		message=wx.StaticText(self,-1,label=_("Choose what information about the mouse should be reported"))
		mainSizer.Add(message)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		shapeCheckBoxID=wx.NewId()
		shapeCheckBox=wx.CheckBox(self,shapeCheckBoxID,label=_("Report mouse shape changes"))
		shapeCheckBox.SetValue(config.conf["mouse"]["reportMouseShapeChanges"])
		wx.EVT_CHECKBOX(self,shapeCheckBoxID,self.onShapeChange)
		settingsSizer.Add(shapeCheckBox)
		objectCheckBoxID=wx.NewId()
		objectCheckBox=wx.CheckBox(self,objectCheckBoxID,label=_("Report object under mouse"))
		objectCheckBox.SetValue(config.conf["mouse"]["reportObjectUnderMouse"])
		wx.EVT_CHECKBOX(self,objectCheckBoxID,self.onObjectChange)
		settingsSizer.Add(objectCheckBox)
		mainSizer.Add(settingsSizer)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer)
		self.SetSizer(mainSizer)

	def onShapeChange(self,evt):
		config.conf["mouse"]["reportMouseShapeChanges"]=evt.IsChecked()

	def onObjectChange(self,evt):
		config.conf["mouse"]["reportObjectUnderMouse"]=evt.IsChecked()

class objectPresentationDialog(wx.Dialog):

	def __init__(self,parent,ID,title):
		wx.Dialog.__init__(self,parent,ID,title)
		mainSizer=wx.BoxSizer(wx.HORIZONTAL)
		message=wx.StaticText(self,-1,label=_("Choose what information objects should report, and whether to be notified of things such as tooltips and help balloons."))
		mainSizer.Add(message)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		tooltipCheckBoxID=wx.NewId()
		tooltipCheckBox=wx.CheckBox(self,tooltipCheckBoxID,label=_("Report tooltips"))
		tooltipCheckBox.SetValue(config.conf["presentation"]["reportTooltips"])
		wx.EVT_CHECKBOX(self,tooltipCheckBoxID,self.onTooltipChange)
		settingsSizer.Add(tooltipCheckBox)
		balloonCheckBoxID=wx.NewId()
		balloonCheckBox=wx.CheckBox(self,balloonCheckBoxID,label=_("Report help balloons"))
		balloonCheckBox.SetValue(config.conf["presentation"]["reportHelpBalloons"])
		wx.EVT_CHECKBOX(self,balloonCheckBoxID,self.onBalloonChange)
		settingsSizer.Add(balloonCheckBox)
		shortcutCheckBoxID=wx.NewId()
		shortcutCheckBox=wx.CheckBox(self,shortcutCheckBoxID,label=_("Report object shortcut keys"))
		shortcutCheckBox.SetValue(config.conf["presentation"]["reportKeyboardShortcuts"])
		wx.EVT_CHECKBOX(self,shortcutCheckBoxID,self.onShortcutChange)
		settingsSizer.Add(shortcutCheckBox)
		groupCheckBoxID=wx.NewId()
		groupCheckBox=wx.CheckBox(self,groupCheckBoxID,label=_("Report object group names"))
		groupCheckBox.SetValue(config.conf["presentation"]["reportObjectGroupNames"])
		wx.EVT_CHECKBOX(self,groupCheckBoxID,self.onGroupChange)
		settingsSizer.Add(groupCheckBox)
		stateFirstCheckBoxID=wx.NewId()
		stateFirstCheckBox=wx.CheckBox(self,stateFirstCheckBoxID,label=_("Say object state first"))
		stateFirstCheckBox.SetValue(config.conf["presentation"]["sayStateFirst"])
		wx.EVT_CHECKBOX(self,stateFirstCheckBoxID,self.onStateFirstChange)
		settingsSizer.Add(stateFirstCheckBox)
		progressBeepCheckBoxID=wx.NewId()
		progressBeepCheckBox=wx.CheckBox(self,progressBeepCheckBoxID,label=_("Beep on progress bar updates"))
		progressBeepCheckBox.SetValue(config.conf["presentation"]["beepOnProgressBarUpdates"])
		wx.EVT_CHECKBOX(self,progressBeepCheckBoxID,self.onProgressBeepChange)
		settingsSizer.Add(progressBeepCheckBox)
		mainSizer.Add(settingsSizer)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer)
		self.SetSizer(mainSizer)

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
