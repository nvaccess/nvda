#synthDrivers/audiologic.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _audiologic
from synthDriverHandler import SynthDriver
import _winreg
from copy import copy

class SynthDriver(SynthDriver):
	Volume=copy(SynthDriver.Volume)
	Volume.data=2
	Inflection=copy(SynthDriver.Inflection)
	Inflection.data=10
	_supportedSettings=[SynthDriver.Rate,SynthDriver.Pitch,Volume,Inflection]

	description="Tts3"
	name="audiologic"


	@classmethod
	def check(cls):
		try:
			r=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Audiologic\Sintesi Audiologic")
			r.Close()
			return True
		except:
			return False

	def __init__(self):
		_audiologic.TtsOpen()

	def terminate(self):
		_audiologic.TtsClose()

	def speakText(self,text,index=None):
		if isinstance(index,int) and index>=0:
			text="[:BMK=%d]%s"%(index,text)
		_audiologic.TtsSpeak(text)

	def _get_lastIndex(self):
		return _audiologic.LastIndex
 
	def cancel(self):
		_audiologic.TtsStop()

	def _getAvailableVoices(self):
		return [synthDriverHandler.VoiceInfo("", "Tts3")]

	def _get_voice(self):
		return ""

	def _set_voice(self, voice):
		pass

	def _get_rate(self):
		return self._paramToPercent(_audiologic.TtsGetProsody('Speed') ,_audiologic.minRate, _audiologic.maxRate) 

	def _set_rate(self,value):
		_audiologic.TtsSetParam(_audiologic.ttsRate, self._percentToParam(value, _audiologic.minRate, _audiologic.maxRate), 0)

	def _get_pitch(self):
		return self._paramToPercent(_audiologic.TtsGetProsody('Pitch'),_audiologic.minPitch, _audiologic.maxPitch) 

	def _set_pitch(self,value):
		_audiologic.TtsSetParam(_audiologic.ttsPitch,self._percentToParam(value, _audiologic.minPitch, _audiologic.maxPitch), 0)

	def _get_volume(self):
		return self._paramToPercent(_audiologic.TtsGetProsody('Vol'),_audiologic.minVol, _audiologic.maxVol) 

	def _set_volume(self,value):
		_audiologic.TtsSetParam(_audiologic.ttsVol,self._percentToParam(value, _audiologic.minVol, _audiologic.maxVol), 0)

	def _get_inflection(self):
		return _audiologic.TtsGetProsody('Expression') *10

	def _set_inflection(self,value):
		_audiologic.TtsSetParam(_audiologic.ttsExpression,int(value/10), 0)

	def pause(self,switch):
		if switch: 
			_audiologic.TtsPause()
		else:
			_audiologic.TtsRestart()
