import debug
import languageHandler
import _espeak
import Queue
import threading
import silence

class SynthDriver(silence.SynthDriver):
	name = "espeak"
	description = "eSpeak"

	def _paramToPercent(self, current, min, max):
		return int(round(float(current - min) / (max - min) * 100))

	def _percentToParam(self, percent, min, max):
		return int(round(float(percent) / 100 * (max - min) + min))

	def initialize(self):
		_espeak.initialize()
		_espeak.setParameter(_espeak.espeakRATE,230,0)
		lang=languageHandler.getLanguage()
		_espeak.setVoiceByLanguage(lang)
		self._voiceList=_espeak.getVoiceList()

	def speakText(self,text,wait=False,index=None):
		_espeak.speak(text, index=index, wait=wait)

	def cancel(self):
		_espeak.stop()

	def _get_rate(self):
		val=_espeak.getParameter(_espeak.espeakRATE,1)
		return self._paramToPercent(val,_espeak.minRate,_espeak.maxRate)

	def _set_rate(self,rate):
		val=self._percentToParam(rate, _espeak.minRate, _espeak.maxRate)
		_espeak.setParameter(_espeak.espeakRATE,val,0)

	def _get_pitch(self):
		val=_espeak.getParameter(_espeak.espeakPITCH,1)
		return self._paramToPercent(val,_espeak.minPitch,_espeak.maxPitch)

	def _set_pitch(self,pitch):
		val=self._percentToParam(pitch, _espeak.minPitch, _espeak.maxPitch)
		_espeak.setParameter(_espeak.espeakPITCH,val,0)

	def _get_volume(self):
		return _espeak.getParameter(_espeak.espeakVOLUME,1)

	def _set_volume(self,volume):
		_espeak.setParameter(_espeak.espeakVOLUME,volume,0)

	def _get_voice(self):
		curVoice = _espeak.getCurrentVoice()
		if not curVoice:
			return 0
		for index, voice in enumerate(self._voiceList):
			if voice == curVoice:
				return index + 1
		return 0

	def _set_voice(self, index):
		if index == 0:
			return
		_espeak.setVoice(self._voiceList[index - 1])

	def _get_voiceCount(self):
		return len(self._voiceList)

	def getVoiceName(self,num):
		num=num-1
		return "%s (%s)"%(self._voiceList[num].name,self._voiceList[num].identifier)

	def _get_lastIndex(self):
		return _espeak.lastIndex

	def terminate(self):
		_espeak.terminate()
