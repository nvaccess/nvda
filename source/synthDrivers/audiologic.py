#synthDrivers/audiologic.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _audiologic
import synthDriverHandler
import _winreg

class SynthDriver(synthDriverHandler.SynthDriver):

	hasVoice=True
	hasPitch=True
	hasRate=True
	hasVolume=True
	hasVariant=False
	hasInflection=True
	inflectionMinStep=10
	volumeMinStep=2
	pitchMinStep=5

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


	def _paramToPercent(self, current, min, max):
		return int(round(float(current - min) / (max - min) * 100))

	def _percentToParam(self, percent, min, max):
		return int(round(float(percent) / 100 * (max - min) + min))

	def initialize(self):
		try:
			_audiologic.TtsOpen()
			return True 
		except:
			return False 

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

	def _get_voice(self):
		return 1

	def _get_voiceCount(self):
		return 1

	def getVoiceName(self,num):
		return "Tts3"

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
