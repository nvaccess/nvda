#audioDucking.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited 
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import threading
from ctypes import *
import time
import wx
import config

AUDIODUCKINGMODE_NONE=0
AUDIODUCKINGMODE_OUTPUTTING=1
AUDIODUCKINGMODE_ALWAYS=2

audioDuckingModes=[
	# Translators: an audio ducking mode for Windows 8 and up
	_("No ducking"),
	# Translators: an audio ducking mode for Windows 8 and up
	_("Duck when outputting speech and sounds"),
	# Translators: an audio ducking mode for Windows 8 and up
	_("Always duck"),
]

ANRUS_ducking_AUDIO_ACTIVE=4
ANRUS_ducking_AUDIO_ACTIVE_NODUCK=8

_audioDuckingMode=0
_duckingRefCount=0
_duckingRefCountLock = threading.RLock()

def _setDuckingState(switch):
	with _duckingRefCountLock:
		import gui
		ATWindow=gui.mainFrame.GetHandle()
		if switch:
			oledll.oleacc.AccSetRunningUtilityState(ATWindow,ANRUS_ducking_AUDIO_ACTIVE|ANRUS_ducking_AUDIO_ACTIVE_NODUCK,ANRUS_ducking_AUDIO_ACTIVE|ANRUS_ducking_AUDIO_ACTIVE_NODUCK)
		else:
			oledll.oleacc.AccSetRunningUtilityState(ATWindow,ANRUS_ducking_AUDIO_ACTIVE|ANRUS_ducking_AUDIO_ACTIVE_NODUCK,ANRUS_ducking_AUDIO_ACTIVE_NODUCK)

def _unduckRequestHelper():
		global _duckingRefCount
		with _duckingRefCountLock:
			_duckingRefCount-=1
			if _duckingRefCount==0 and _audioDuckingMode!=AUDIODUCKINGMODE_NONE:
				_setDuckingState(False)

def _requestDucking(switch):
	global _duckingRefCount
	with _duckingRefCountLock:
		if switch:
			_duckingRefCount+=1
			if _duckingRefCount==1 and _audioDuckingMode!=AUDIODUCKINGMODE_NONE:
				_setDuckingState(True)
				time.sleep(0.15)
		else:
			wx.CallLater(1000,_unduckRequestHelper)

def setAudioDuckingMode(mode):
	global _audioDuckingMode, _duckingRefCount
	if not isAudioDuckingSupported():
		raise RuntimeError("audio ducking not supported")
	if mode<0 or mode>=len(audioDuckingModes):
		raise ValueError("%s is not an audio ducking mode")
	with _duckingRefCountLock:
		oldMode=_audioDuckingMode
		_audioDuckingMode=mode
		if oldMode==AUDIODUCKINGMODE_NONE and mode!=AUDIODUCKINGMODE_NONE and _duckingRefCount>0:
			_setDuckingState(True)
		elif oldMode!=AUDIODUCKINGMODE_NONE and mode==AUDIODUCKINGMODE_NONE and _duckingRefCount>0:
			_setDuckingState(False)
		if oldMode!=AUDIODUCKINGMODE_ALWAYS and mode==AUDIODUCKINGMODE_ALWAYS:
			_duckingRefCount+=1
			_setDuckingState(True)
		elif oldMode==AUDIODUCKINGMODE_ALWAYS and mode!=AUDIODUCKINGMODE_ALWAYS and _duckingRefCount>0: 
			_duckingRefCount-=1
			_setDuckingState(False)

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
	""" Create one of these objects to duck background audio.
	While one or more instances of this class exist, background audio is kept ducked, as long as NVDA's audio ducking mode is set to AUDIODUCKINGMODE_OUTPUT.
	When an  instance is created and it is the only one, instance creation will block for a short time to ensure that Windows has faded background audio enough before allowing audio from NVDA.
	When an instance is deleted, goes out of scope or is garbage collected, and it is the only instance remaining, audio will stay ducked for an extra amount of time before raising to normal volume so that quick duck requests (e.g. short speech) does not make the volume bounce up and down unnecessarily. 
	It is also possible to temporarily disable than AudioDucker instance by setting its disabled property to True. This is useful for such things as pausing speech.
	"""

	def __init__(self):
		if not isAudioDuckingSupported():
			raise RuntimeError("audio ducking not supported")
		_requestDucking(True)

	def __del__(self):
		if not self._disabled:
			_requestDucking(False)

	_disabled=False

	@property
	def disabled(self):
		"""If true, ducking is disabled, False it is enabled. """
		return self._disabled

	@disabled.setter
	def disabled(self,val):
		if val!=self._disabled:
			_requestDucking(not val)
			self._disabled=val
