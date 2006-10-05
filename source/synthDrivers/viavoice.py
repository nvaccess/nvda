import os
import ctypes
import debug

#Constants

#Synth parameters
eciSynthMode=0
eciNumDeviceBlocks=13
eciSizeDeviceBlocks=14
#voice parameters
eciGender=0
eciHeadSize=1
eciPitchBaseline=2
eciPitchFluctuation=3
eciRoughness=4
eciBreathiness=5
eciSpeed=6
eciVolume=7

viavoicePath=r'C:\Program Files\ViaVoiceTTS'


class synthDriver(object):

	def __init__(self):
		oldDir=os.getcwd()
		os.chdir(viavoicePath)
		self.dll=ctypes.windll.LoadLibrary('ibmeci50.dll')
		os.chdir(oldDir)
		self.handle=self.dll.eciNew()

	def getRate(self):
		return self.dll.eciGetVoiceParam(self.handle,0,eciSpeed)

	def getPitch(self):
			return self.dll.eciGetVoiceParam(self.handle,0,eciPitchBaseline)

	def getVolume(self):
		return self.dll.eciGetVoiceParam(self.handle,0,eciVolume)

	def getVoice(self):
		return curVoice

	def setRate(self,value):
		self.dll.eciSetVoiceParam(self.handle,0,eciSpeed,value)

	def setPitch(self,value):
		self.dll.eciSetVoiceParam(self.handle,0,eciPitchBaseline,value)

	def setVolume(self,value):
		self.dll.eciSetVoiceParam(self.handle,0,eciVolume,value)

	def setVoice(self,value):
		self.dll.eciCopyVoice(self.handle,value,0)
		curVoice=value

	def speakText(self,text,wait=False):
		try:
			text=text.encode("iso-8859-1","ignore")
		except:
			return
		self.dll.eciAddText(self.handle,text)
		self.dll.eciSynthesize(self.handle)
		if wait:
			self.dll.eciSynchronize(self.handle)

	def cancel(self):
		if self.dll.eciSpeaking(self.handle):
			self.dll.eciStop(self.handle)
