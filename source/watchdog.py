import time
import threading
from ctypes import *
import winUser
import api

#settings
#: How often to check whether the core is alive
CHECK_INTERVAL=0.1
#: How long to wait for the core to be alive under normal circumstances
NORMAL_CORE_ALIVE_TIMEOUT=10
#: The minimum time to wait for the core to be alive
MIN_CORE_ALIVE_TIMEOUT=0.3
#: How long to wait between recovery attempts
RECOVER_ATTEMPT_INTERVAL = 0.05

safeWindowClassSet=set([
	'Internet Explorer_Server',
	'_WwG',
])

isRunning=False
isAttemptingRecovery = False

_coreAliveEvent = threading.Event()
_resumeEvent = threading.Event()
_coreThreadID=windll.kernel32.GetCurrentThreadId()
_watcherThread=None

def alive():
	"""Inform the watchdog that the core is alive.
	"""
	global _coreAliveEvent
	_coreAliveEvent.set()

def _watcher():
	global isAttemptingRecovery
	while isRunning:
		# If the watchdog is suspended, wait until it is resumed.
		_resumeEvent.wait()

		# Wait for the core to be alive.
		# Wait a maximum of NORMAL_CORE_ALIVE_TIMEOUT, but shorten this to a minimum of MIN_CORE_ALIVE_TIMEOUT under special circumstances.
		waited = 0
		while True:
			# Wait MIN_CORE_ALIVE_TIMEOUT, unless there is less than that time remaining for NORMAL_CORE_ALIVE_TIMEOUT.
			timeout = min(MIN_CORE_ALIVE_TIMEOUT, NORMAL_CORE_ALIVE_TIMEOUT - waited)
			if timeout <= 0:
				# Timeout elapsed.
				break
			_coreAliveEvent.wait(timeout)
			waited += timeout
			if _coreAliveEvent.isSet() or _shouldRecoverAfterMinTimeout():
				break

		while not _coreAliveEvent.isSet():
			# The core is dead, so attempt recovery.
			isAttemptingRecovery = True
			_recoverAttempt()
			_coreAliveEvent.wait(RECOVER_ATTEMPT_INTERVAL)
		isAttemptingRecovery = False

		# At this point, the core is alive.
		_coreAliveEvent.clear()
		# Wait a bit to avoid excessive resource consumption.
		time.sleep(CHECK_INTERVAL)

def _shouldRecoverAfterMinTimeout():
	info=winUser.getGUIThreadInfo(0)
	if winUser.getClassName(info.hwndFocus) in safeWindowClassSet:
		return False
	if not winUser.isDescendantWindow(info.hwndActive, api.getFocusObject().windowHandle):
		# The foreground window has changed.
		return True
	newHwnd=info.hwndFocus if info.hwndFocus else info.hwndActive
	newThreadID=winUser.getWindowThreadProcessID(newHwnd)[1]
	return newThreadID!=api.getFocusObject().windowThreadID

def _recoverAttempt():
	try:
		oledll.ole32.CoCancelCall(_coreThreadID,0)
	except:
		pass

def initialize():
	"""Initialize the watchdog.
	"""
	global _watcherThread, isRunning
	if isRunning:
		raise RuntimeError("already running") 
	isRunning=True
	oledll.ole32.CoEnableCallCancellation(None)
	_coreAliveEvent.set()
	_resumeEvent.set()
	_watcherThread=threading.Thread(target=_watcher)
	_watcherThread.start()

def terminate():
	"""Terminate the watchdog.
	"""
	global isRunning
	if not isRunning:
		return
	isRunning=False
	oledll.ole32.CoDisableCallCancellation(None)
	_resumeEvent.set()
	_coreAliveEvent.set()
	_watcherThread.join()

class Suspender(object):
	"""A context manager to temporarily suspend the watchdog for a block of code.
	"""

	def __enter__(self):
		_resumeEvent.clear()

	def __exit__(self,*args):
		_resumeEvent.set()
