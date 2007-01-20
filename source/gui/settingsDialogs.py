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
		settingsSizer=wx.GridSizer()
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
		mainSizer.Add(settingsSizer)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer)

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
