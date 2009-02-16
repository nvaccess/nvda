import time
import threading
from ctypes import *
import queueHandler
import winUser
import api

#settings
#: How often to check whether the core is alive
CHECK_INTERVAL=0.3
#: How long to wait for the core to be alive
CORE_ALIVE_TIMEOUT=0.01

isRunning=False

_coreAliveEvent=threading.Event()
_coreGeneratorID=None
_coreThreadID=windll.kernel32.GetCurrentThreadId()
_lastFocusProcessID=0
_watcherThread=None

def _coreGenerator():
	global _lastFocusProcessID
	while True:
		_lastFocusProcessID=api.getFocusObject().processID
		_coreAliveEvent.set()
		yield
		yield

def _watcher():
	while isRunning:
		_coreAliveEvent.wait(CORE_ALIVE_TIMEOUT)
		if _coreAliveEvent.isSet():
			_coreAliveEvent.clear()
			time.sleep(CHECK_INTERVAL)
		elif winUser.getWindowThreadProcessID(winUser.getForegroundWindow())[0]!=_lastFocusProcessID:
			try:
				oledll.ole32.CoCancelCall(_coreThreadID,0)
			except:
				pass

def start():
	"""Enables COM call cancellation and monitors NVDA's main thread so it can cancel overly long blocking COM calls.""" 
	global _watcherThread, _coreGeneratorID, isRunning
	if isRunning:
		raise RuntimeError("already running") 
	isRunning=True
	oledll.ole32.CoEnableCallCancellation(None)
	_coreAliveEvent.set()
	_coreGeneratorID=queueHandler.registerGeneratorObject(_coreGenerator())
	_watcherThread=threading.Thread(target=_watcher)
	_watcherThread.start()

def stop():
	"""Disables COM call cancellation and cleans up the monitor thread."""
	global isRunning
	if not isRunning:
		return
	isRunning=False
	oledll.ole32.CoDisableCallCancellation(None)
	_watcherThread.join()
	queueHandler.cancelGeneratorObject(_coreGeneratorID)

class CancellationDisabler(object):
	"""A class that can be used with the Python 'with' keyword, to temporarily disable COM call cancellation for its containing code, if cancellation was enabled.""" 

	def __enter__(self):
		stop()

	def __exit__(self,*args):
		start()
