import time
import thread
import ctypes
import os
import ctypes
import debug

#Constants

#Synth parameters
eciSynthMode=0
eciDictionary=3
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
#Index types
eciIndexReply=2
#Callback return values
eciDataNotProcessed=0
eciDataProcessed=1
eciDataAbort=2

viavoicePath=r'C:\Program Files\ViaVoiceTTS'

class synthDriver(object):

	def __init__(self):
		oldDir=os.getcwd()
		os.chdir(viavoicePath)
		self.dll=ctypes.windll.LoadLibrary('ibmeci50.dll')
		os.chdir(oldDir)
		self.handle=self.dll.eciNew()
		self.dll.eciSetParam(self.handle,eciSynthMode,1)
		self.dll.eciSetParam(self.handle,eciDictionary,1)
		#self.keepWatching=True
		#thread.start_new_thread(self.indexWatcher,())

	def __del__(self):
		self.dll.eciDelete(self.handle)

	def getLastIndex(self):
		self.dll.eciSpeaking(self.handle)
		return self.dll.eciGetIndex(self.handle)

	def indexWatcher(self):
		try:
			while self.keepWatching:
				self.dll.eciSpeaking(self.handle)
				index=self.dll.eciGetIndex(self.handle)
				if index and callable(self.spokenTextCallback):
					debug.writeMessage("synthDriver viavoice indexWatcher index %s"%index)
					self.spokenTextCallback(index)
				time.sleep(0.01)
		except:
			debug.writeException("synth driver viavoice indexWatcher")

	def getRate(self):
		return self.dll.eciGetVoiceParam(self.handle,0,eciSpeed)

	def getPitch(self):
			return self.dll.eciGetVoiceParam(self.handle,0,eciPitchBaseline)

	def getVolume(self):
		return self.dll.eciGetVoiceParam(self.handle,0,eciVolume)

	def getVoice(self):
		return curVoice

	def getLastIndex(self):
		self.dll.eciSpeaking(self.handle)
		return self.dll.eciGetIndex(self.handle)

	def setRate(self,value):
		self.dll.eciSetVoiceParam(self.handle,0,eciSpeed,value)

	def setPitch(self,value):
		self.dll.eciSetVoiceParam(self.handle,0,eciPitchBaseline,value)

	def setVolume(self,value):
		self.dll.eciSetVoiceParam(self.handle,0,eciVolume,value)

	def setVoice(self,value):
		self.dll.eciCopyVoice(self.handle,value,0)
		curVoice=value

	def speakText(self,text,wait=False,index=None):
		try:
			text=text.encode("iso-8859-1","ignore")
		except:
			return
		self.dll.eciAddText(self.handle,text)
		if index is not None:
			res=self.dll.eciInsertIndex(self.handle,index)
			debug.writeMessage("synthDriver viavoice addText index %s, res %s"%(index,res))
		self.dll.eciAddText(self.handle,"")
		self.dll.eciSynthesize(self.handle)
		if wait:
			self.dll.eciSynchronize(self.handle)

	def cancel(self):
		if self.dll.eciSpeaking(self.handle):
			self.dll.eciStop(self.handle)

