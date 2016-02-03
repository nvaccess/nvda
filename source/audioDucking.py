#audioDucking.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited 
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import threading
from ctypes import *
import time
import config
from logHandler import log

class AutoEvent(wintypes.HANDLE):

	def __init__(self):
		e=windll.kernel32.CreateEventW(None,True,False,None)
		super(AutoEvent,self).__init__(e)

	def __del__(self):
		if self:
			windll.kernel32.CloseHandle(self)

WAIT_TIMEOUT=0x102
AUDIODUCKINGMODE_NONE=0
AUDIODUCKINGMODE_OUTPUTTING=1
AUDIODUCKINGMODE_ALWAYS=2

audioDuckingModes=[
	# Translators: An audio ducking mode which specifies how NVDA affects the volume of other applications.
	# See the Audio Ducking Mode section of the User Guide for details.
	_("No ducking"),
	# Translators: An audio ducking mode which specifies how NVDA affects the volume of other applications.
	# See the Audio Ducking Mode section of the User Guide for details.
	_("Duck when outputting speech and sounds"),
	# Translators: An audio ducking mode which specifies how NVDA affects the volume of other applications.
	# See the Audio Ducking Mode section of the User Guide for details.
	_("Always duck"),
]

ANRUS_ducking_AUDIO_ACTIVE=4
ANRUS_ducking_AUDIO_ACTIVE_NODUCK=8

INITIAL_DUCKING_DELAY=0.15

_audioDuckingMode=0
_duckingRefCount=0
_duckingRefCountLock = threading.RLock()
_modeChangeEvent=None
_lastDuckedTime=0

def _setDuckingState(switch):
	global _lastDuckedTime
	with _duckingRefCountLock:
		import gui
		ATWindow=gui.mainFrame.GetHandle()
		if switch:
			oledll.oleacc.AccSetRunningUtilityState(ATWindow,ANRUS_ducking_AUDIO_ACTIVE|ANRUS_ducking_AUDIO_ACTIVE_NODUCK,ANRUS_ducking_AUDIO_ACTIVE|ANRUS_ducking_AUDIO_ACTIVE_NODUCK)
			_lastDuckedTime=time.time()
		else:
			oledll.oleacc.AccSetRunningUtilityState(ATWindow,ANRUS_ducking_AUDIO_ACTIVE|ANRUS_ducking_AUDIO_ACTIVE_NODUCK,ANRUS_ducking_AUDIO_ACTIVE_NODUCK)

def _ensureDucked():
	global _duckingRefCount
	with _duckingRefCountLock:
		_duckingRefCount+=1
		log.debug("Increased ref count, _duckingRefCount=%d"%_duckingRefCount)
		if _duckingRefCount==1  and _audioDuckingMode!=AUDIODUCKINGMODE_NONE:
			_setDuckingState(True)
			delta=0
		else:
			delta=time.time()-_lastDuckedTime
		return delta,_modeChangeEvent

def _unensureDucked(delay=True):
	global _duckingRefCount
	if delay:
		import core
		log.debug("Queuing _unensureDucked")
		core.callLater(1000,_unensureDucked,False)
		return
	with _duckingRefCountLock:
		_duckingRefCount-=1
		log.debug("Decreased  ref count, _duckingRefCount=%d"%_duckingRefCount)
		if _duckingRefCount==0 and _audioDuckingMode!=AUDIODUCKINGMODE_NONE:
			_setDuckingState(False)

def setAudioDuckingMode(mode):
	global _audioDuckingMode, _modeChangeEvent
	if not isAudioDuckingSupported():
		raise RuntimeError("audio ducking not supported")
	if mode<0 or mode>=len(audioDuckingModes):
		raise ValueError("%s is not an audio ducking mode")
	with _duckingRefCountLock:
		oldMode=_audioDuckingMode
		_audioDuckingMode=mode
		if _modeChangeEvent: windll.kernel32.SetEvent(_modeChangeEvent)
		_modeChangeEvent=AutoEvent()
		log.debug("Switched modes from %s, to %s"%(oldMode,mode))
		if oldMode==AUDIODUCKINGMODE_NONE and mode!=AUDIODUCKINGMODE_NONE and _duckingRefCount>0:
			_setDuckingState(True)
		elif oldMode!=AUDIODUCKINGMODE_NONE and mode==AUDIODUCKINGMODE_NONE and _duckingRefCount>0:
			_setDuckingState(False)
		if oldMode!=AUDIODUCKINGMODE_ALWAYS and mode==AUDIODUCKINGMODE_ALWAYS:
			_ensureDucked()
		elif oldMode==AUDIODUCKINGMODE_ALWAYS and mode!=AUDIODUCKINGMODE_ALWAYS:
			_unensureDucked(delay=False)

def initialize():
	if not isAudioDuckingSupported():
		return
	_setDuckingState(False)
	setAudioDuckingMode(config.conf['audio']['audioDuckingMode'])

_isAudioDuckingSupported=None
def isAudioDuckingSupported():
	global _isAudioDuckingSupported
	if _isAudioDuckingSupported is None:
		_isAudioDuckingSupported=config.isInstalledCopy() and hasattr(oledll.oleacc,'AccSetRunningUtilityState')
	return _isAudioDuckingSupported

def handleConfigProfileSwitch():
	if isAudioDuckingSupported():
		setAudioDuckingMode(config.conf['audio']['audioDuckingMode'])

class AudioDucker(object):
	""" Create one of these objects to manage ducking of background audio. 
	Use the enable and disable methods on this object to denote when you require audio to be ducked.  
	If this object is deleted while ducking is still enabled, the object will automatically disable ducking first.
	"""

	def __init__(self):
		if not isAudioDuckingSupported():
			raise RuntimeError("audio ducking not supported")
		self._enabled=False
		self._lock=threading.Lock()

	def __del__(self):
		if self._enabled:
			self.disable()

	def enable(self):
		"""Tells NVDA that you require that background audio be ducked from now until you call disable.
		This method may block for a short time while background audio ducks to a suitable level.
		It is safe to call this method more than once.
		@ returns: True if ducking was enabled, false if ducking was subsiquently disabled while waiting for the background audio to drop.
		"""
		with self._lock:
			if self._enabled:
				log.debug("ignoring duplicate enable")
				return True
			self._enabled=True
			log.debug("enabling")
			whenWasDucked,modeChangeEvent=_ensureDucked()
			deltaMS=int((INITIAL_DUCKING_DELAY-whenWasDucked)*1000)
			disableEvent=self._disabledEvent=AutoEvent()
			log.debug("whenWasDucked %s, deltaMS %s"%(whenWasDucked,deltaMS))
			if deltaMS<=0 or _audioDuckingMode==AUDIODUCKINGMODE_NONE:
				return True
		import NVDAHelper
		if not NVDAHelper.localLib.audioDucking_shouldDelay():
			log.debug("No background audio, not delaying")
			return True
		log.debug("waiting %s ms or mode change"%deltaMS)
		wasCanceled=windll.kernel32.WaitForMultipleObjects(2,(wintypes.HANDLE*2)(disableEvent,modeChangeEvent),False,deltaMS)!=WAIT_TIMEOUT
		log.debug("Wait canceled" if wasCanceled else "timeout exceeded")
		return not wasCanceled

	def disable(self):
		"""Tells NVDA that you no longer require audio to be ducked.
		while other AudioDucker objects are still enabled, audio will remain ducked.
		It is safe to call this method more than once.
		"""
		with self._lock:
			if not self._enabled:
				log.debug("Ignoring duplicate disable")
				return True
			self._enabled=False
			log.debug("disabling")
			_unensureDucked()
			windll.kernel32.SetEvent(self._disabledEvent)
			return True
