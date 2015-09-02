#watchdog.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import sys
import os
import traceback
import time
import threading
import inspect
from ctypes import windll, oledll
import ctypes.wintypes
import msvcrt
import comtypes
import winUser
import winKernel
from logHandler import log
import globalVars
import core
import NVDAHelper

#settings
#: The minimum time to wait for the core to be alive.
MIN_CORE_ALIVE_TIMEOUT=0.5
#: How long to wait for the core to be alive under normal circumstances.
#: This must be a multiple of MIN_CORE_ALIVE_TIMEOUT.
NORMAL_CORE_ALIVE_TIMEOUT=10
#: How long to wait between recovery attempts
RECOVER_ATTEMPT_INTERVAL = 0.05
#: The amount of time before the core should be considered severely frozen and a warning logged.
FROZEN_WARNING_TIMEOUT = 15

safeWindowClassSet=set([
	'Internet Explorer_Server',
	'_WwG',
	'EXCEL7',
])

isRunning=False
isAttemptingRecovery = False

_coreDeadTimer = windll.kernel32.CreateWaitableTimerW(None, True, None)
_suspended = False
_watcherThread=None
_cancelCallEvent = None

class CallCancelled(Exception):
	"""Raised when a call is cancelled.
	"""

def alive():
	"""Inform the watchdog that the core is alive.
	"""
	# Stop cancelling calls.
	windll.kernel32.ResetEvent(_cancelCallEvent)
	# Set the timer so the watcher will take action in MIN_CORE_ALIVE_TIMEOUT
	# if this function or asleep() isn't called.
	windll.kernel32.SetWaitableTimer(_coreDeadTimer,
		ctypes.byref(ctypes.wintypes.LARGE_INTEGER(-int(10000000 * MIN_CORE_ALIVE_TIMEOUT))),
		0, None, None, False)

def asleep():
	"""Inform the watchdog that the core is going to sleep.
	"""
	# #5189: Reset in case the core was treated as dead.
	alive()
	# CancelWaitableTimer does not reset the signaled state; if it was signaled, it remains signaled.
	# However, alive() calls SetWaitableTimer, which resets the timer to unsignaled.
	windll.kernel32.CancelWaitableTimer(_coreDeadTimer)

def _isAlive():
	# #5189: If the watchdog has been terminated, treat the core as being alive.
	# This will stop recovery if it has started and allow the watcher to terminate.
	return not isRunning or winKernel.waitForSingleObject(_coreDeadTimer, 0) != 0

def _watcher():
	global isAttemptingRecovery
	while True:
		# Wait for the core to die.
		winKernel.waitForSingleObject(_coreDeadTimer, winKernel.INFINITE)
		if not isRunning:
			return
		# The core hasn't reported alive for MIN_CORE_ALIVE_TIMEOUT.
		waited = MIN_CORE_ALIVE_TIMEOUT
		while not _isAlive() and not _shouldRecoverAfterMinTimeout():
			# The core is still dead and fast recovery doesn't apply.
			# Wait up to NORMAL_ALIVE_TIMEOUT.
			time.sleep(MIN_CORE_ALIVE_TIMEOUT)
			waited += MIN_CORE_ALIVE_TIMEOUT
			if waited >= NORMAL_CORE_ALIVE_TIMEOUT:
				break
		if _isAlive():
			continue
		if log.isEnabledFor(log.DEBUGWARNING):
			log.debugWarning("Trying to recover from freeze, core stack:\n%s"%
				"".join(traceback.format_stack(sys._current_frames()[core.mainThreadId])))
		lastTime=time.time()
		isAttemptingRecovery = True
		# Cancel calls until the core is alive.
		# This event will be reset by alive().
		windll.kernel32.SetEvent(_cancelCallEvent)
		# Some calls have to be killed individually.
		while True:
			curTime=time.time()
			if curTime-lastTime>FROZEN_WARNING_TIMEOUT:
				lastTime=curTime
				log.warning("Core frozen in stack:\n%s"%
					"".join(traceback.format_stack(sys._current_frames()[core.mainThreadId])))
			_recoverAttempt()
			time.sleep(RECOVER_ATTEMPT_INTERVAL)
			if _isAlive():
				break
		isAttemptingRecovery = False

def _shouldRecoverAfterMinTimeout():
	info=winUser.getGUIThreadInfo(0)
	if not info.hwndFocus:
		# The foreground thread is frozen or there is no foreground thread (probably due to a freeze elsewhere).
		return True
	# Import late to avoid circular import.
	import api
	#If a system menu has been activated but NVDA's focus is not yet in the menu then use min timeout
	if info.flags&winUser.GUI_SYSTEMMENUMODE and info.hwndMenuOwner and api.getFocusObject().windowClassName!='#32768':
		return True 
	if winUser.getClassName(info.hwndFocus) in safeWindowClassSet:
		return False
	if not winUser.isDescendantWindow(info.hwndActive, api.getFocusObject().windowHandle):
		# The foreground window has changed.
		return True
	newHwnd=info.hwndFocus
	newThreadID=winUser.getWindowThreadProcessID(newHwnd)[1]
	return newThreadID!=api.getFocusObject().windowThreadID

def _recoverAttempt():
	try:
		oledll.ole32.CoCancelCall(core.mainThreadId,0)
	except:
		pass

class MINIDUMP_EXCEPTION_INFORMATION(ctypes.Structure):
	_fields_ = (
		("ThreadId", ctypes.wintypes.DWORD),
		("ExceptionPointers", ctypes.c_void_p),
		("ClientPointers", ctypes.wintypes.BOOL),
	)

@ctypes.WINFUNCTYPE(ctypes.wintypes.LONG, ctypes.c_void_p)
def _crashHandler(exceptionInfo):
	threadId = ctypes.windll.kernel32.GetCurrentThreadId()
	# An exception might have been set for this thread.
	# Clear it so that it doesn't get raised in this function.
	ctypes.pythonapi.PyThreadState_SetAsyncExc(threadId, None)

	# Write a minidump.
	dumpPath = os.path.abspath(os.path.join(globalVars.appArgs.logFileName, "..", "nvda_crash.dmp"))
	try:
		with file(dumpPath, "w") as mdf:
			mdExc = MINIDUMP_EXCEPTION_INFORMATION(ThreadId=threadId,
				ExceptionPointers=exceptionInfo, ClientPointers=False)
			if not ctypes.windll.DbgHelp.MiniDumpWriteDump(
				ctypes.windll.kernel32.GetCurrentProcess(),
				os.getpid(),
				msvcrt.get_osfhandle(mdf.fileno()),
				0, # MiniDumpNormal
				ctypes.byref(mdExc),
				None,
				None
			):
				raise ctypes.WinError()
	except:
		log.critical("NVDA crashed! Error writing minidump", exc_info=True)
	else:
		log.critical("NVDA crashed! Minidump written to %s" % dumpPath)

	log.info("Restarting due to crash")
	core.restart()
	return 1 # EXCEPTION_EXECUTE_HANDLER

@ctypes.WINFUNCTYPE(None)
def _notifySendMessageCancelled():
	caller = inspect.currentframe().f_back
	if not caller:
		return
	# Set a profile function which will raise an exception when returning from the calling frame.
	def sendMessageCallCanceller(frame, event, arg):
		if frame == caller:
			# Raising an exception will also cause the profile function to be deactivated.
			raise CallCancelled
	sys.setprofile(sendMessageCallCanceller)

RPC_E_CALL_CANCELED = -2147418110
_orig_COMError_init = comtypes.COMError.__init__
def _COMError_init(self, hresult, text, details):
	if hresult == RPC_E_CALL_CANCELED:
		raise CallCancelled
	_orig_COMError_init(self, hresult, text, details)

def initialize():
	"""Initialize the watchdog.
	"""
	global _watcherThread, isRunning, _cancelCallEvent
	if isRunning:
		raise RuntimeError("already running") 
	isRunning=True
	# Catch application crashes.
	windll.kernel32.SetUnhandledExceptionFilter(_crashHandler)
	oledll.ole32.CoEnableCallCancellation(None)
	# Cache cancelCallEvent.
	_cancelCallEvent = ctypes.wintypes.HANDLE.in_dll(NVDAHelper.localLib,
		"cancelCallEvent")
	# Handle cancelled SendMessage calls.
	NVDAHelper._setDllFuncPointer(NVDAHelper.localLib, "_notifySendMessageCancelled", _notifySendMessageCancelled)
	# Monkey patch comtypes to specially handle cancelled COM calls.
	comtypes.COMError.__init__ = _COMError_init
	_watcherThread=threading.Thread(target=_watcher)
	alive()
	_watcherThread.start()

def terminate():
	"""Terminate the watchdog.
	"""
	global isRunning
	if not isRunning:
		return
	isRunning=False
	oledll.ole32.CoDisableCallCancellation(None)
	comtypes.COMError.__init__ = _orig_COMError_init
	# Wake up the watcher so it knows to finish.
	windll.kernel32.SetWaitableTimer(_coreDeadTimer,
		ctypes.byref(ctypes.wintypes.LARGE_INTEGER(0)),
		0, None, None, False)
	_watcherThread.join()

class Suspender(object):
	"""A context manager to temporarily suspend the watchdog for a block of code.
	"""

	def __enter__(self):
		global _suspended
		_suspended = True
		asleep()

	def __exit__(self,*args):
		global _suspended
		_suspended = False
		alive()

class CancellableCallThread(threading.Thread):
	"""A worker thread used to execute a call which must be made cancellable.
	If the call is cancelled, this thread must be abandoned.
	"""

	def __init__(self):
		super(CancellableCallThread, self).__init__()
		self.daemon = True
		self._executeEvent = threading.Event()
		self._executionDoneEvent = ctypes.windll.kernel32.CreateEventW(None, False, False, None)
		self.isUsable = True

	def execute(self, func, args, kwargs, pumpMessages=True):
		# Don't even bother making the call if the core is already dead.
		if isAttemptingRecovery:
			raise CallCancelled

		self._func = func
		self._args = args
		self._kwargs = kwargs
		self._result = None
		self._exc_info = None
		self._executeEvent.set()

		waitHandles = (ctypes.wintypes.HANDLE * 2)(
			self._executionDoneEvent, _cancelCallEvent)
		waitIndex = ctypes.wintypes.DWORD()
		if pumpMessages:
			oledll.ole32.CoWaitForMultipleHandles(0, winKernel.INFINITE, 2, waitHandles, ctypes.byref(waitIndex))
		else:
			waitIndex.value = windll.kernel32.WaitForMultipleObjects(2, waitHandles, False, winKernel.INFINITE)
		if waitIndex.value == 1:
			# Cancelled.
			self.isUsable = False
			raise CallCancelled

		exc = self._exc_info
		if exc:
			raise exc[0], exc[1], exc[2]
		return self._result

	def run(self):
		comtypes.CoInitializeEx(comtypes.COINIT_MULTITHREADED)
		while self.isUsable:
			self._executeEvent.wait()
			self._executeEvent.clear()
			try:
				self._result = self._func(*self._args, **self._kwargs)
			except:
				self._exc_info = sys.exc_info()
			ctypes.windll.kernel32.SetEvent(self._executionDoneEvent)
		ctypes.windll.kernel32.CloseHandle(self._executionDoneEvent)

cancellableCallThread = None
def cancellableExecute(func, *args, **kwargs):
	"""Execute a function in the main thread, making it cancellable.
	@param func: The function to execute.
	@type func: callable
	@param ccPumpMessages: Whether to pump messages while waiting.
	@type ccPumpMessages: bool
	@param args: Positional arguments for the function.
	@param kwargs: Keyword arguments for the function.
	@raise CallCancelled: If the call was cancelled.
	"""
	global cancellableCallThread
	pumpMessages = kwargs.pop("ccPumpMessages", True)
	if not isRunning or _suspended or not isinstance(threading.currentThread(), threading._MainThread):
		# Watchdog is not running or this is a background thread,
		# so just execute the call.
		return func(*args, **kwargs)
	if not cancellableCallThread or not cancellableCallThread.isUsable:
		# The thread hasn't yet been created or is not usable.
		# Create a new one.
		cancellableCallThread = CancellableCallThread()
		cancellableCallThread.start()
	return cancellableCallThread.execute(func, args, kwargs, pumpMessages=pumpMessages)

def cancellableSendMessage(hwnd, msg, wParam, lParam, flags=0, timeout=60000):
	"""Send a window message, making the call cancellable.
	The C{timeout} and C{flags} arguments should usually be left at their default values.
	The call will still be cancelled if appropriate even if the specified timeout has not yet been reached.
	@raise CallCancelled: If the call was cancelled.
	"""
	result = ctypes.wintypes.DWORD()
	NVDAHelper.localLib.cancellableSendMessageTimeout(hwnd, msg, wParam, lParam, flags, timeout, ctypes.byref(result))
	return result.value
