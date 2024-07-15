# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from logHandler import log
from pycaw.api.audiopolicy import IAudioSessionManager2
from pycaw.callbacks import AudioSessionNotification, AudioSessionEvents
from pycaw.utils import AudioSession, AudioUtilities
from dataclasses import dataclass, field
from comtypes import COMError
from threading import Lock
from pycaw.api.audiopolicy import IAudioSessionControl2
import weakref
import globalVars
import os


_audioSessionManager: IAudioSessionManager2 | None = None


def initialize() -> None:
	global _audioSessionManager
	try:
		_audioSessionManager = AudioUtilities.GetAudioSessionManager()
	except COMError:
		log.exception("Could not initialize audio session manager")
		return


def terminate():
	global _audioSessionManager
	_audioSessionManager = None


class _AudioSessionEventsListener(AudioSessionEvents):
	"""
	This class is a listener for audio session termination event. It is registered in WASAPI by
	`_AudioSessionNotificationListener.on_session_created()` method. It calls custom logic defined in
	`AudioSessionCallback.onSessionTerminated()` implementation and allows customers to restore audio volume.
	"""

	callback: "weakref.ReferenceType[AudioSessionCallback]"
	pid: int
	audioSession: AudioSession

	def __init__(self, callback: "AudioSessionCallback", pid: int, audioSession: AudioSession):
		self.callback = weakref.ref(callback)
		self.pid = pid
		self.audioSession = audioSession

	def on_state_changed(self, new_state: str, new_state_id: int):
		if new_state == "Expired":
			self.onSessionTerminated()

	def onSessionTerminated(self):
		log.debug(f"Audio session for pid {self.pid} terminated")
		try:
			self.callback().onSessionTerminated(self.audioSession)
		finally:
			self.unregister()
		with self.callback()._lock:
			self.callback()._audioSessionEventListeners.remove(self)

	def unregister(self):
		try:
			self.audioSession.unregister_notification()
		except Exception:
			log.exception(f"Cannot unregister audio session for process {self.pid}")


class _AudioSessionNotificationListener(AudioSessionNotification):
	"""
	This class is a handler for existing and newly created audio sessions. Its method `on_session_created`
	will be called from `AudioSessionCallback.register()` for all existing audio sessions; and, additionally,
	it will be notified by WASAPI for every new audio session created.
	It sets up a callback for session termination - an instance of `_AudioSessionEventsListener` class;
	then it calls custom logic provided in `AudioSessionCallback.onSessionUpdate()` implementation.
	"""

	callback: "weakref.ReferenceType[AudioSessionCallback]"

	def __init__(self, callback: "AudioSessionCallback"):
		self.callback = weakref.ref(callback)

	def on_session_created(self, new_session: AudioSession):
		pid = new_session.ProcessId
		if pid != globalVars.appPid:
			process = new_session.Process
			if process is not None:
				exe = os.path.basename(process.exe())
				isNvda = exe.lower() == "nvda.exe"
				if isNvda:
					# This process must be NVDA running on secure screen.
					# We shouldn't change volume of such process.
					return
		audioSessionEventsListener = _AudioSessionEventsListener(self.callback(), pid, new_session)
		new_session.register_notification(audioSessionEventsListener)
		with self.callback()._lock:
			self.callback()._audioSessionEventListeners.add(audioSessionEventsListener)
		self.callback().onSessionUpdate(new_session)


class DummyAudioSessionCallback:
	def register(self, applyToFuture: bool = True):
		pass

	def unregister(self, runTerminators: bool = True):
		pass


@dataclass(unsafe_hash=True)
class AudioSessionCallback(DummyAudioSessionCallback):
	"""
	This is an abstract class that allows implementing custom logic, that will be applied to all WASAPI
	audio sessions. Consumers are expected to implement functions:
	* def onSessionUpdate(self, session: AudioSession):
		It will be called once for every existing audio session and also will be scheduled to be called
		for every new audio session.
	* def onSessionTerminated(self, session: AudioSession):
		It will be called when an audio session is terminated or when unregister() is called, which
		typically happens when NVDA quits.
	"""

	_lock: Lock = Lock()
	_audioSessionNotification: AudioSessionNotification | None = None
	_audioSessionEventListeners: set[_AudioSessionEventsListener] = field(default_factory=set)

	def onSessionUpdate(self, session: AudioSession) -> None:
		"""
		Callback function to be implemented by the customer.
		Will be called for all existing sessions and newly created sessions.
		"""
		pass

	def onSessionTerminated(self, session: AudioSession) -> None:
		"""
		Callback function to be implemented by the customer.
		Will be called when each session is terminated or when unregister() method is called.
		"""
		pass

	def register(self, applyToFuture: bool = True):
		"""
		Registers this callback.
		This will internally call onSessionUpdate() for all current audio sessions.
		Additionally if applyToFuture is True, it will also call onSessionUpdate() for all newly created sessions
		until this callback is unregistered.
		"""
		_applyToAllAudioSessions(self, applyToFuture)

	def unregister(self, runTerminators: bool = True):
		"""
		Unregisters this callback.
		If runTerminators is True, it will also trigger onSessionTerminated for all current audio sessions.
		"""
		if self._audioSessionNotification is not None:
			_audioSessionManager.UnregisterSessionNotification(self._audioSessionNotification)
		with self._lock:
			listenersCopy = list(self._audioSessionEventListeners)
		for audioSessionEventListener in listenersCopy:
			if runTerminators:
				audioSessionEventListener.on_state_changed("Expired", 0)
			else:
				audioSessionEventListener.audioSession.unregister_notification()


def _applyToAllAudioSessions(
	callback: AudioSessionCallback,
	applyToFuture: bool = True,
) -> None:
	"""
	Executes provided callback function on all active audio sessions.
	Additionally, if applyToFuture is True, then it will register a notification with audio session manager,
	which will execute the same callback for all future sessions as they are created.
	"""
	listener = _AudioSessionNotificationListener(callback)
	if applyToFuture:
		_audioSessionManager.RegisterSessionNotification(listener)
		callback._audioSessionNotification = listener
	sessionEnumerator = _audioSessionManager.GetSessionEnumerator()
	count = sessionEnumerator.GetCount()
	for i in range(count):
		ctl = sessionEnumerator.GetSession(i)
		if ctl is None:
			continue
		ctl2 = ctl.QueryInterface(IAudioSessionControl2)
		if ctl2 is not None:
			audioSession = AudioSession(ctl2)
			listener.on_session_created(audioSession)
