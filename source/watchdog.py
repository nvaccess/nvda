import time
import threading
from ctypes import *

#settings
#: How often to check whether the core is alive
CHECK_INTERVAL=0.1
#: How long to wait for the core to be alive
CORE_ALIVE_TIMEOUT=0.4
#: How long to wait between recovery attempts
RECOVER_ATTEMPT_INTERVAL = 0.01

isRunning=False

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
	while isRunning:
		# If the watchdog is suspended, wait until it is resumed.
		_resumeEvent.wait()
		_coreAliveEvent.wait(CORE_ALIVE_TIMEOUT)
		while not _coreAliveEvent.isSet():
			# The core is dead, so attempt recovery.
			_recoverAttempt()
			_coreAliveEvent.wait(RECOVER_ATTEMPT_INTERVAL)
		# At this point, the core is alive.
		_coreAliveEvent.clear()
		# Wait a bit to avoid excessive resource consumption.
		time.sleep(CHECK_INTERVAL)

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
