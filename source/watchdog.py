# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2024 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sys
import os
import time
from time import perf_counter as _timer
import threading
from typing import (
	Any,
)
import inspect
from ctypes import windll, oledll
import ctypes.wintypes
import msvcrt
import comtypes
import winUser
import winKernel
from logHandler import log
import logHandler
import globalVars
import core
import exceptions
import NVDAHelper
import NVDAState


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "getFormattedStacksForAllThreads" and NVDAState._allowDeprecatedAPI():
		log.warning(
			"Importing getFormattedStacksForAllThreads from here is deprecated. "
			"getFormattedStacksForAllThreads should be imported from logHandler instead.",
			stack_info=True,
		)
		return logHandler.getFormattedStacksForAllThreads
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


MIN_CORE_ALIVE_TIMEOUT = 0.5
"""The minimum time (seconds) to wait for the core to be alive.
"""
NORMAL_CORE_ALIVE_TIMEOUT = 10
""" Seconds to wait for the core to be alive under normal circumstances.
"""
RECOVER_ATTEMPT_INTERVAL = 0.05
""" Seconds to wait between recovery attempts
"""
FROZEN_WARNING_TIMEOUT = 15
""" Seconds before the core should be considered severely frozen and a warning logged.
"""

safeWindowClassSet = {
	'Internet Explorer_Server',
	'_WwG',
	'EXCEL7',
}

isRunning=False
isAttemptingRecovery: bool = False
_coreIsAsleep = False

_coreDeadTimer = windll.kernel32.CreateWaitableTimerW(None, True, None)
_suspended = False
_watcherThread=None
_cancelCallEvent = None


def alive():
	"""Inform the watchdog that the core is alive.
	"""
	global _coreIsAsleep
	_coreIsAsleep = False
	# Stop cancelling calls.
	windll.kernel32.ResetEvent(_cancelCallEvent)
	# Set the timer so the watcher will take action in MIN_CORE_ALIVE_TIMEOUT
	# if this function or asleep() isn't called.
	SECOND_TO_100_NANOSECOND = 10 ** 7  # nanosecond is 10^9, 10^7 is hundreds of nanoseconds
	windll.kernel32.SetWaitableTimer(
		_coreDeadTimer,
		ctypes.byref(ctypes.wintypes.LARGE_INTEGER(
			# The time after which the state of the timer is to be set to signaled,
			# in 100 nanosecond intervals.
			# Use the format described by the FILETIME structure.
			# Positive values indicate absolute time.
			# Be sure to use a UTC-based absolute time, as the system uses UTC-based time internally.
			# Negative values indicate relative time.
			# The actual timer accuracy depends on the capability of your hardware.
			# For more information about UTC-based time, see System Time.
			-int(SECOND_TO_100_NANOSECOND * MIN_CORE_ALIVE_TIMEOUT)
		)),
		0, None, None, False)


def asleep():
	"""Inform the watchdog that the core is going to sleep.
	"""
	global _coreIsAsleep
# #5189: Reset in case the core was treated as dead.
	alive()
	# CancelWaitableTimer does not reset the signaled state; if it was signaled, it remains signaled.
	# However, alive() calls SetWaitableTimer, which resets the timer to unsignaled.
	windll.kernel32.CancelWaitableTimer(_coreDeadTimer)
	_coreIsAsleep = True


def isCoreAsleep():
	"""
	Finds out if the core is currently asleep (I.e. not in a core cycle).
	Note that if the core is actually frozen, this function will return false
	as it is frozen in a core cycle while awake.
	"""
	return _coreIsAsleep


def _isAlive():
	# #5189: If the watchdog has been terminated, treat the core as being alive.
	# This will stop recovery if it has started and allow the watcher to terminate.
	return not isRunning or winKernel.waitForSingleObject(_coreDeadTimer, 0) != 0


def _waitUntilNormalCoreAliveTimeout(waitedSince: float):
	logged = False
	while (
		_timer() - waitedSince < NORMAL_CORE_ALIVE_TIMEOUT
		and not _isAlive()
		and not _shouldRecoverAfterMinTimeout()
	):
		if not logged:
			logged = True
			log.debug(f"Potential freeze, waiting up to {NORMAL_CORE_ALIVE_TIMEOUT} seconds.")
		# The core is still dead and fast recovery doesn't apply.
		# Wait up to NORMAL_ALIVE_TIMEOUT in increments of MIN_CORE_ALIVE_TIMEOUT
		time.sleep(MIN_CORE_ALIVE_TIMEOUT)

	if logged and _isAlive():
		log.debug(f"Recovered from potential freeze after {_timer() - waitedSince} seconds.")


def _watcher():
	global isAttemptingRecovery
	while True:
		# Wait for the core to die.
		winKernel.waitForSingleObject(_coreDeadTimer, winKernel.INFINITE)

		if not isRunning:
			# NVDA has shutdown, exit the watcher.
			return

		# The core hasn't reported alive for MIN_CORE_ALIVE_TIMEOUT.
		waitedSince = _timer() - MIN_CORE_ALIVE_TIMEOUT  # already waiting this long via _coreDeadTimer
		_waitUntilNormalCoreAliveTimeout(waitedSince)
		if _isAlive():
			continue
		else:
			isAttemptingRecovery = True
			waitForFreezeRecovery(waitedSince)
			isAttemptingRecovery = False


def waitForFreezeRecovery(waitedSince: float):
	log.info(f"Starting freeze recovery after {_timer() - waitedSince} seconds.")
	if log.isEnabledFor(log.DEBUGWARNING):
		stacks = logHandler.getFormattedStacksForAllThreads()
		log.debugWarning(
			f"Listing stacks for Python threads:\n{stacks}"
		)

	# After every FROZEN_WARNING_TIMEOUT seconds have elapsed
	# log each threads stack trace
	lastTime = _timer()

	# Cancel calls until the core is alive.
	# This event will be reset by alive().
	windll.kernel32.SetEvent(_cancelCallEvent)

	# Some calls have to be killed individually.
	while not _isAlive():
		curTime = _timer()
		if curTime - lastTime > FROZEN_WARNING_TIMEOUT:
			lastTime = curTime
			# Core is completely frozen.
			# Collect formatted stacks for all Python threads.
			log.error(f"Core frozen in stack! ({curTime - waitedSince} seconds)")
			stacks = logHandler.getFormattedStacksForAllThreads()
			log.info(f"Listing stacks for Python threads:\n{stacks}")
		_recoverAttempt()
		time.sleep(RECOVER_ATTEMPT_INTERVAL)

	log.info(
		f"Recovered from freeze after {_timer() - waitedSince} seconds."
	)

def _shouldRecoverAfterMinTimeout():
	info=winUser.getGUIThreadInfo(0)
	if not info.hwndFocus:
		# The foreground thread is frozen or there is no foreground thread (probably due to a freeze elsewhere).
		return True
	# Import late to avoid circular import.
	import api
	from NVDAObjects.window import Window
	#If a system menu has been activated but NVDA's focus is not yet in the menu then use min timeout
	if info.flags&winUser.GUI_SYSTEMMENUMODE and info.hwndMenuOwner and api.getFocusObject().windowClassName!='#32768':
		return True 
	if winUser.getClassName(info.hwndFocus) in safeWindowClassSet:
		return False
	focus = api.getFocusObject()
	if (not isinstance(focus, Window)) or (not winUser.isDescendantWindow(info.hwndActive, focus.windowHandle)):
		# The foreground window has changed.
		return True
	newHwnd=info.hwndFocus
	newThreadID=winUser.getWindowThreadProcessID(newHwnd)[1]
	return newThreadID != focus.windowThreadID

def _recoverAttempt():
	try:
		oledll.ole32.CoCancelCall(core.mainThreadId,0)
	except:  # noqa: E722
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
	dumpPath = os.path.join(globalVars.appArgs.logFileName, "..", "nvda_crash.dmp")
	try:
		# Though we aren't using pythonic functions to write to the dump file,
		# open it in binary mode as opening it in text mode (the default) doesn't make sense.
		with open(dumpPath, "wb") as mdf:
			mdExc = MINIDUMP_EXCEPTION_INFORMATION(ThreadId=threadId,
				ExceptionPointers=exceptionInfo, ClientPointers=False)
			if not ctypes.windll.DbgHelp.MiniDumpWriteDump(
				winKernel.kernel32.GetCurrentProcess(),
				globalVars.appPid,
				msvcrt.get_osfhandle(mdf.fileno()),
				0, # MiniDumpNormal
				ctypes.byref(mdExc),
				None,
				None
			):
				raise ctypes.WinError()
	except:  # noqa: E722
		log.critical("NVDA crashed! Error writing minidump", exc_info=True)
	else:
		log.critical("NVDA crashed! Minidump written to %s" % dumpPath)

	# Log Python stacks for every thread.
	stacks = logHandler.getFormattedStacksForAllThreads()
	log.info(f"Listing stacks for Python threads:\n{stacks}")

	log.info("Restarting due to crash")
	# if NVDA has crashed we cannot rely on the queue handler to start the new NVDA instance
	core.restartUnsafely()
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
			raise exceptions.CallCancelled
	sys.setprofile(sendMessageCallCanceller)

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
	_watcherThread = threading.Thread(
		name=__name__,
		target=_watcher,
		daemon=True,
	)
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

	def execute(self, func, *args, pumpMessages=True, **kwargs):
		fname = repr(func)
		self.name = f"{self.__class__.__module__}.{self.execute.__qualname__}({fname})"
		# Don't even bother making the call if the core is already dead.
		if isAttemptingRecovery:
			raise exceptions.CallCancelled

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
			raise exceptions.CallCancelled

		exc = self._exc_info
		if exc:
			# The execution of the function in the other thread caused an exception.
			# Re-raise it here.
			# Note that in Python3, the traceback (stack) is now part of the exception,
			# So the logged traceback will correctly show the stack for both this thread and the other thread. 
			raise exc
		return self._result

	def run(self):
		comtypes.CoInitializeEx(comtypes.COINIT_MULTITHREADED)
		while self.isUsable:
			self._executeEvent.wait()
			self._executeEvent.clear()
			try:
				self._result = self._func(*self._args, **self._kwargs)
			except Exception as e:
				self._exc_info = e
			ctypes.windll.kernel32.SetEvent(self._executionDoneEvent)
		ctypes.windll.kernel32.CloseHandle(self._executionDoneEvent)

cancellableCallThread = None
def cancellableExecute(func, *args, ccPumpMessages=True, **kwargs):
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
	if (
		not isRunning
		or _suspended
		or threading.current_thread() is not threading.main_thread()
	):
		# Watchdog is not running or this is a background thread,
		# so just execute the call.
		return func(*args, **kwargs)
	if not cancellableCallThread or not cancellableCallThread.isUsable:
		# The thread hasn't yet been created or is not usable.
		# Create a new one.
		cancellableCallThread = CancellableCallThread()
		cancellableCallThread.start()
	return cancellableCallThread.execute(func, *args, pumpMessages=ccPumpMessages, **kwargs)

def cancellableSendMessage(hwnd, msg, wParam, lParam, flags=0, timeout=60000):
	"""Send a window message, making the call cancellable.
	The C{timeout} and C{flags} arguments should usually be left at their default values.
	The call will still be cancelled if appropriate even if the specified timeout has not yet been reached.
	@raise CallCancelled: If the call was cancelled.
	"""
	result = ctypes.wintypes.DWORD()
	NVDAHelper.localLib.cancellableSendMessageTimeout(hwnd, msg, wParam, lParam, flags, timeout, ctypes.byref(result))
	return result.value


class WatchdogObserver:
	@property
	def isAttemptingRecovery(self) -> bool:
		global isAttemptingRecovery
		return isAttemptingRecovery
