import os
import time
import pythoncom
import comtypesClient
import win32com.client
import _winreg
import debug
import queueHandler
import baseObject

name="sapi4"
description="Microsoft Speech API 4 (ActiveVoice.ActiveVoice)"

COM_CLASS = "ActiveVoice.ActiveVoice"

def check():
	try:
		r=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,COM_CLASS)
		r.Close()
		return True
	except:
		pass
	return registerDll()

def registerDll():
	try:
		ret = os.system(r"regsvr32 /s %SystemRoot%\speech\xvoice.dll")
		return ret == 0
	except:
		pass
		return False

class synthDriver(baseObject.autoPropertyObject):

	def __init__(self):
		registerDll()
		self.tts=comtypesClient.CreateObject(COM_CLASS,sink=self)
		self.tts.Speak("")
		self.tts.CallBacksEnabled=1
		self.tts.Tagged=1
		self._lastIndex=None
		self.voiceNames=[]
		try:
			for num in xrange(1,self.tts.CountEngines+1):
				self.voiceNames.append(self.tts.modeName(num))
		except:
			pass
 
	def _paramToPercent(self, current, min, max):
		return float(current - min) / (max - min) * 100

	def _percentToParam(self, percent, min, max):
		return int(float(percent) / 100 * (max - min) + min)

	#Events

	def BookMark(self,x,y,z,markNum):
		self._lastIndex=markNum-1

	def _get_rate(self):
		return self._paramToPercent(self.tts.speed,self.tts.minSpeed,self.tts.maxSpeed)

	def _get_pitch(self):
		return self._paramToPercent(self.tts.pitch,self.tts.minPitch,self.tts.maxPitch)

	def _get_volume(self):
		return self._paramToPercent(self.tts.volumeLeft,self.tts.minVolumeLeft,self.tts.maxVolumeLeft)

	def _get_voice(self):
		return self.tts.currentMode

	def _get_lastIndex(self):
		return self._lastIndex

	def _set_rate(self,rate):
		# ViaVoice doesn't seem to like the speed being set to maximum.
		self.tts.speed=min(self._percentToParam(rate, self.tts.minSpeed, self.tts.maxSpeed), self.tts.maxSpeed - 1)
		self.tts.speak("")

	def _set_pitch(self,value):
		self.tts.pitch=self._percentToParam(value, self.tts.minPitch, self.tts.maxPitch)

	def _set_volume(self,value):
		self.tts.volumeLeft = self.tts.VolumeRight = self._percentToParam(value, self.tts.minVolumeLeft, self.tts.maxVolumeLeft)
		self.tts.speak("")

	def _set_voice(self,value):
		try:
			self.tts.select(value)
		except:
			pass
		self.tts.speak("")

	def speakText(self,text,wait=False,index=None):
		text=text.replace("\\","\\\\")
		if isinstance(index,int) and index>=0:
			text="".join(["\\mrk=%d\\"%(index+1),text])
		self.tts.speak(text)
		if wait:
			while self.tts.speaking:
				pythoncom.PumpWaitingMessages()
				time.sleep(0.01)

	def cancel(self):
		self.tts.audioReset()
