#watchdog.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2011 NV Access Inc
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

#settings
#: How often to check whether the core is alive
CHECK_INTERVAL=0.1
#: How long to wait for the core to be alive under normal circumstances
NORMAL_CORE_ALIVE_TIMEOUT=10
#: The minimum time to wait for the core to be alive
MIN_CORE_ALIVE_TIMEOUT=0.5
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

_coreAliveEvent = threading.Event()
_resumeEvent = threading.Event()
_coreThreadID=windll.kernel32.GetCurrentThreadId()
_watcherThread=None

class CallCancelled(Exception):
	"""Raised when a call is cancelled.
	"""

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
		if log.isEnabledFor(log.DEBUGWARNING) and not _coreAliveEvent.isSet():
			log.debugWarning("Trying to recover from freeze, core stack:\n%s"%
				"".join(traceback.format_stack(sys._current_frames()[_coreThreadID])))
		lastTime=time.time()
		while not _coreAliveEvent.isSet():
			curTime=time.time()
			if curTime-lastTime>FROZEN_WARNING_TIMEOUT:
				lastTime=curTime
				log.warning("Core frozen in stack:\n%s"%
					"".join(traceback.format_stack(sys._current_frames()[_coreThreadID])))
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
		oledll.ole32.CoCancelCall(_coreThreadID,0)
	except:
		pass
	import NVDAHelper
	NVDAHelper.localLib.cancelSendMessage()

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
			log.info("Writing minidump")
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
	import core
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
	global _watcherThread, isRunning
	if isRunning:
		raise RuntimeError("already running") 
	isRunning=True
	# Catch application crashes.
	windll.kernel32.SetUnhandledExceptionFilter(_crashHandler)
	oledll.ole32.CoEnableCallCancellation(None)
	# Handle cancelled SendMessage calls.
	import NVDAHelper
	NVDAHelper._setDllFuncPointer(NVDAHelper.localLib, "_notifySendMessageCancelled", _notifySendMessageCancelled)
	# Monkey patch comtypes to specially handle cancelled COM calls.
	comtypes.COMError.__init__ = _COMError_init
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
	comtypes.COMError.__init__ = _orig_COMError_init
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

		if pumpMessages:
			waitHandles = (ctypes.wintypes.HANDLE * 1)(self._executionDoneEvent)
			waitIndex = ctypes.wintypes.DWORD()
		timeout = int(1000 * CHECK_INTERVAL)
		while True:
			if pumpMessages:
				try:
					oledll.ole32.CoWaitForMultipleHandles(0, timeout, 1, waitHandles, ctypes.byref(waitIndex))
					break
				except WindowsError:
					pass
			else:
				if windll.kernel32.WaitForSingleObject(self._executionDoneEvent, timeout) != winKernel.WAIT_TIMEOUT:
					break
			if isAttemptingRecovery:
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
	if not isRunning or not _resumeEvent.isSet() or not isinstance(threading.currentThread(), threading._MainThread):
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
	import NVDAHelper
	result = ctypes.wintypes.DWORD()
	NVDAHelper.localLib.cancellableSendMessageTimeout(hwnd, msg, wParam, lParam, flags, timeout, ctypes.byref(result))
	return result.value
