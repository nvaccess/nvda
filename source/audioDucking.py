# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from enum import IntEnum
from utils.displayString import DisplayStringIntEnum
import threading
from typing import Dict
from ctypes import oledll, wintypes, windll
import time
import config
from logHandler import log
import systemUtils


def _isDebug():
	return config.conf["debugLog"]["audioDucking"]


class AutoEvent(wintypes.HANDLE):

	def __init__(self):
		e=windll.kernel32.CreateEventW(None,True,False,None)
		super(AutoEvent,self).__init__(e)

	def __del__(self):
		if self:
			windll.kernel32.CloseHandle(self)

WAIT_TIMEOUT=0x102


class AudioDuckingMode(DisplayStringIntEnum):
	NONE = 0
	OUTPUTTING = 1
	ALWAYS = 2

	@property
	def _displayStringLabels(self) -> Dict[IntEnum, str]:
		return {
			# Translators: An audio ducking mode which specifies how NVDA affects the volume of other applications.
			# See the Audio Ducking Mode section of the User Guide for details.
			AudioDuckingMode.NONE: _("No ducking"),
			# Translators: An audio ducking mode which specifies how NVDA affects the volume of other applications.
			# See the Audio Ducking Mode section of the User Guide for details.
			AudioDuckingMode.OUTPUTTING: _("Duck when outputting speech and sounds"),
			# Translators: An audio ducking mode which specifies how NVDA affects the volume of other applications.
			# See the Audio Ducking Mode section of the User Guide for details.
			AudioDuckingMode.ALWAYS: _("Always duck"),
		}


class ANRUSDucking(IntEnum):
	# https://docs.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accsetrunningutilitystate#anrus_priority_audio_active_noduck
	AUDIO_ACTIVE = 4
	AUDIO_ACTIVE_NODUCK = 8


INITIAL_DUCKING_DELAY=0.15

_audioDuckingMode=0
_duckingRefCount=0
_duckingRefCountLock = threading.RLock()
_modeChangeEvent=None
_lastDuckedTime=0


def _setDuckingState(switch):
	global _lastDuckedTime
	with _duckingRefCountLock:
		try:
			import gui
			ATWindow=gui.mainFrame.GetHandle()
			if switch:
				oledll.oleacc.AccSetRunningUtilityState(
					ATWindow,
					ANRUSDucking.AUDIO_ACTIVE | ANRUSDucking.AUDIO_ACTIVE_NODUCK,
					ANRUSDucking.AUDIO_ACTIVE | ANRUSDucking.AUDIO_ACTIVE_NODUCK
				)
				_lastDuckedTime=time.time()
			else:
				oledll.oleacc.AccSetRunningUtilityState(
					ATWindow,
					ANRUSDucking.AUDIO_ACTIVE | ANRUSDucking.AUDIO_ACTIVE_NODUCK,
					ANRUSDucking.AUDIO_ACTIVE_NODUCK
				)
		except WindowsError as e:
			# When the NVDA build is not signed, audio ducking fails with access denied.
			# A developer built launcher is unlikely to be signed. Catching this error stops developers from looking into
			# "expected" errors.
			# ERROR_ACCESS_DENIED is 0x5
			# https://docs.microsoft.com/en-us/windows/desktop/debug/system-error-codes--0-499-
			ERROR_ACCESS_DENIED = 0x80070005
			errorCode = e.winerror & 0xFFFFFFFF  # we only care about the first 8 hex values.
			if errorCode == ERROR_ACCESS_DENIED:
				log.warning("Unable to set ducking state: ERROR_ACCESS_DENIED.")
			else:
				# we want developers to hear the "error sound", and to halt, so still raise the exception.
				log.error(
					"Unknown error when setting ducking state:  Error number: {:#010X}".format(errorCode),
					exc_info=True
				)
				raise e


def _ensureDucked():
	global _duckingRefCount
	with _duckingRefCountLock:
		_duckingRefCount+=1
		if _isDebug():
			log.debug("Increased ref count, _duckingRefCount=%d"%_duckingRefCount)
		if _duckingRefCount == 1 and _audioDuckingMode != AudioDuckingMode.NONE:
			_setDuckingState(True)
			delta=0
		else:
			delta=time.time()-_lastDuckedTime
		return delta,_modeChangeEvent


def _unensureDucked(delay=True):
	global _duckingRefCount
	if delay:
		import core
		if _isDebug():
			log.debug("Queuing _unensureDucked")
		try:
			core.callLater(1000, _unensureDucked, False)
			return
		except core.NVDANotInitializedError:
			# If the wx.App has not been initialized, audio ducking callbacks
			# will fail as they rely on wx.CallLater/wx.CallAfter
			log.debugWarning("wx App not initialized, unducking immediately")
	with _duckingRefCountLock:
		_duckingRefCount-=1
		if _isDebug():
			log.debug("Decreased  ref count, _duckingRefCount=%d"%_duckingRefCount)
		if _duckingRefCount == 0 and _audioDuckingMode != AudioDuckingMode.NONE:
			_setDuckingState(False)


def setAudioDuckingMode(mode):
	global _audioDuckingMode, _modeChangeEvent
	if not isAudioDuckingSupported():
		raise RuntimeError("audio ducking not supported")
	if mode < 0 or mode >= len(AudioDuckingMode):
		raise ValueError("%s is not an audio ducking mode")
	with _duckingRefCountLock:
		oldMode=_audioDuckingMode
		_audioDuckingMode=mode
		if _modeChangeEvent: windll.kernel32.SetEvent(_modeChangeEvent)
		_modeChangeEvent=AutoEvent()
		if _isDebug():
			log.debug("Switched modes from %s, to %s"%(oldMode,mode))
		if oldMode == AudioDuckingMode.NONE and mode != AudioDuckingMode.NONE and _duckingRefCount > 0:
			_setDuckingState(True)
		elif oldMode != AudioDuckingMode.NONE and mode == AudioDuckingMode.NONE and _duckingRefCount > 0:
			_setDuckingState(False)
		if oldMode != AudioDuckingMode.ALWAYS and mode == AudioDuckingMode.ALWAYS:
			_ensureDucked()
		elif oldMode == AudioDuckingMode.ALWAYS and mode != AudioDuckingMode.ALWAYS:
			_unensureDucked(delay=False)


def initialize():
	if not isAudioDuckingSupported():
		return
	_setDuckingState(False)
	setAudioDuckingMode(config.conf['audio']['audioDuckingMode'])
	config.post_configProfileSwitch.register(handlePostConfigProfileSwitch)


_isAudioDuckingSupported=None


def isAudioDuckingSupported():
	global _isAudioDuckingSupported
	if _isAudioDuckingSupported is None:
		_isAudioDuckingSupported = (
			config.isInstalledCopy()
			or config.isAppX
		) and hasattr(oledll.oleacc, 'AccSetRunningUtilityState')
		_isAudioDuckingSupported &= systemUtils.hasUiAccess()
	return _isAudioDuckingSupported


def handlePostConfigProfileSwitch():
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
		@returns: True if ducking was enabled,
			false if ducking was subsiquently disabled while waiting for the background audio to drop.
		"""
		debug = _isDebug()
		with self._lock:
			if self._enabled:
				if debug:
					log.debug("ignoring duplicate enable")
				return True
			self._enabled=True
			if debug:
				log.debug("enabling")
			whenWasDucked,modeChangeEvent=_ensureDucked()
			deltaMS=int((INITIAL_DUCKING_DELAY-whenWasDucked)*1000)
			disableEvent=self._disabledEvent=AutoEvent()
			if debug:
				log.debug("whenWasDucked %s, deltaMS %s"%(whenWasDucked,deltaMS))
			if deltaMS <= 0 or _audioDuckingMode == AudioDuckingMode.NONE:
				return True
		import NVDAHelper
		if not NVDAHelper.localLib.audioDucking_shouldDelay():
			if debug:
				log.debug("No background audio, not delaying")
			return True
		if debug:
			log.debug("waiting %s ms or mode change"%deltaMS)
		wasCanceled=windll.kernel32.WaitForMultipleObjects(2,(wintypes.HANDLE*2)(disableEvent,modeChangeEvent),False,deltaMS)!=WAIT_TIMEOUT
		if debug:
			log.debug("Wait canceled" if wasCanceled else "timeout exceeded")
		return not wasCanceled

	def disable(self):
		"""Tells NVDA that you no longer require audio to be ducked.
		while other AudioDucker objects are still enabled, audio will remain ducked.
		It is safe to call this method more than once.
		"""
		with self._lock:
			if not self._enabled:
				if _isDebug():
					log.debug("Ignoring duplicate disable")
				return True
			self._enabled=False
			if _isDebug():
				log.debug("disabling")
			_unensureDucked()
			windll.kernel32.SetEvent(self._disabledEvent)
			return True
