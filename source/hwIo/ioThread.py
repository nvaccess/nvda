# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2016-2023 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
# Leonard de Ruijter

import ctypes
import ctypes.wintypes
import threading
import winKernel
import typing
from logHandler import log
from serial.win32 import OVERLAPPED, LPOVERLAPPED
from extensionPoints.util import AnnotatableWeakref, BoundMethodWeakref
from inspect import ismethod
from logHandler import getFormattedStacksForAllThreads


LPOVERLAPPED_COMPLETION_ROUTINE = ctypes.WINFUNCTYPE(
	None,
	ctypes.wintypes.DWORD,
	ctypes.wintypes.DWORD,
	LPOVERLAPPED,
)
ApcT = typing.Callable[[int], None]
ApcIdT = int
OverlappedStructAddressT = int
CompletionRoutineT = typing.Callable[[int, int, LPOVERLAPPED], None]
ApcStoreT = typing.Dict[
	ApcIdT,
	typing.Tuple[
		typing.Union[ApcT, BoundMethodWeakref[ApcT], AnnotatableWeakref[ApcT]],
		ApcIdT,
	],
]
CompletionRoutineStoreTypeT = typing.Dict[
	OverlappedStructAddressT,
	typing.Tuple[
		typing.Union[BoundMethodWeakref[CompletionRoutineT], AnnotatableWeakref[CompletionRoutineT]],
		OVERLAPPED,
	],
]


def _generateApcParams() -> typing.Generator[ApcIdT, None, None]:
	"""Generator of APC params for internal use.
	Params generated using this generator are passed to our internal APC to lookup Python functions.
	A parameter passed to an APC is of type ULONG_PTR, which has a size of 4 bytes.
	Therefore, we use a counter which starts at 0, counts up to 0xffffffff,
	wraps back to 0 and continues cycling.
	"""
	while True:
		for param in range(0x100000000):
			yield param


class IoThread(threading.Thread):
	"""A thread used for background writes and raw I/O, e.g. for braille displays."""

	exit: bool = False
	_apcParamCounter = _generateApcParams()
	#: Store of Python functions to be called as APC.
	#: This allows us to have a single APC function in the class rather than on
	#: each instance, which prevents reference cycles.
	_apcStore: ApcStoreT = {}
	#: Store of Python functions to be called as Overlapped Completion Routine.
	#: This allows us to have a single completion routine in the class rather than on
	#: each instance, which prevents reference cycles.
	#: Note that we use the address of the OVERLAPPED structure as key in this store,
	#: eventhough the structure is also stored in the value.
	#: The OVERLAPPED structure can't be used as key because ctypes does not have OOR (original object return),
	#: it constructs a new, equivalent object each time you retrieve the contents of a LPOVERLAPPED.
	_completionRoutineStore: CompletionRoutineStoreTypeT = {}

	def __init__(self):
		super().__init__(
			name=f"{self.__class__.__module__}.{self.__class__.__qualname__}",
			daemon=True,
		)

	@winKernel.PAPCFUNC
	def _internalApc(param: ApcIdT):
		threadinst = threading.current_thread()
		if not isinstance(threadinst, IoThread):
			log.error("Internal APC called from unknown thread")
			return

		(reference, actualParam) = IoThread._apcStore.pop(param, (None, 0))
		if reference is None:
			log.error(f"Internal APC called with param {param}, but no such apcId in store")
			return
		if isinstance(reference, (BoundMethodWeakref, AnnotatableWeakref)):
			function = reference()
			if not function:
				log.debugWarning(
					f"Not executing queued APC {param}:{reference.funcName} with param {actualParam} because reference died",
				)
				return
		else:
			function = reference

		try:
			function(actualParam)
		except Exception:
			log.error(
				f"Error in APC function {function!r} with apcId {param} queued to IoThread",
				exc_info=True,
			)

	@LPOVERLAPPED_COMPLETION_ROUTINE
	def _internalCompletionRoutine(
		error: int,
		numberOfBytes: int,
		overlapped: LPOVERLAPPED,
	):
		threadinst = threading.current_thread()
		if not isinstance(threadinst, IoThread):
			log.error("Internal APC called from unknown thread")
			return

		ptr = ctypes.cast(overlapped, ctypes.c_void_p).value
		(reference, cachedOverlapped) = IoThread._completionRoutineStore.pop(ptr, (None, None))
		if reference is None:
			log.error(
				f"Internal completion routine called with pointer 0x{ptr:x}, but no such address in store",
			)
			return

		function = reference()
		if not function:
			log.debugWarning(
				f"Not executing queued completion routine 0x{ptr:x}:{reference.funcName} because reference died",
			)
			return

		try:
			function(error, numberOfBytes, overlapped)
		except Exception:
			log.error(f"Error in overlapped completion routine {function!r}", exc_info=True)

	def start(self):
		super().start()
		self.handle = ctypes.windll.kernel32.OpenThread(winKernel.THREAD_SET_CONTEXT, False, self.ident)

	def _registerToCallAsApc(
		self,
		func: ApcT,
		param: int = 0,
	) -> ApcIdT:
		"""Internal method to store a python function to be called in an Asynchronous Procedure Call (APC).
		The function and param are saved in a store on the IoThread instance.
		When our internal APC executes the function, the entry be popped from the store.
		This method does not queue the APC itself.
		The saved python function will be weakly referenced,
		therefore the caller should keep a reference to the python function.
		@param func: The function to be called in an APC.
		@param param: The parameter passed to the APC when called.
		@returns: The internal param to pass to the internal APC.
		"""
		if not self.is_alive():
			raise RuntimeError("Thread is not running")

		# generate a number to identify the function in the store.
		internalParam = next(self._apcParamCounter)
		# Generate a weak reference to the function
		reference = BoundMethodWeakref(func) if ismethod(func) else AnnotatableWeakref(func)
		reference.funcName = repr(func)

		self._apcStore[internalParam] = (reference, param)
		return internalParam

	def queueAsApc(
		self,
		func: ApcT,
		param: int = 0,
	):
		"""safely queues a Python function call as an Asynchronous Procedure Call (APC).
		The function and param are saved in a store on the IoThread instance.
		When our internal APC executes the function, the entry will be popped from the store.
		The queued python function will be weakly referenced,
		therefore the caller should keep a reference to the python function.
		@param func: The function to be called in an APC.
		@param param: The parameter passed to the APC when called.
		"""
		internalParam = self._registerToCallAsApc(func, param)
		ctypes.windll.kernel32.QueueUserAPC(self._internalApc, self.handle, internalParam)

	def setWaitableTimer(
		self,
		handle: typing.Union[int, ctypes.wintypes.HANDLE],
		dueTime: int,
		func: ApcT,
		param: int = 0,
	):
		""" "Safe wrapper around winKernel.setWaitableTimer that uses an internal APC.
		A weak reference to the function and its param are saved in a store on the IoThread instance.
		When our internal APC executes the function, the entry will be popped from the store.
		Note that as the python function is weakly referenced, the caller should
		keep a reference to the python function.
		@param handle: A handle to the timer object.
		@param dueTime: Relative time (in miliseconds).
		@param func: The function to be executed when the timer elapses.
		@param param: The parameter passed to the APC when called.
		"""
		internalParam = self._registerToCallAsApc(func, param)
		winKernel.setWaitableTimer(
			handle,
			dueTime,
			completionRoutine=self._internalApc,
			arg=internalParam,
		)

	def queueAsCompletionRoutine(
		self,
		func: CompletionRoutineT,
		overlapped: OVERLAPPED,
	):
		"""safely queues a Python function call as an overlapped completion routine.
		A weak reference to the Python function is saved in a store on the IoThread instance
		When our internal completion routine executes the function, it will be popped from the store.
		The wrapped python function is weakly referenced, therefore the caller should
		keep a reference to the python function (not the completion routine itself).
		@param func: The function to be wrapped in a completion routine.
		@param overlapped: The overlapped structure
		@returns: The completion routine.
		"""
		if not self.is_alive():
			raise RuntimeError("Thread is not running")

		addr = ctypes.addressof(overlapped)
		if addr in self._completionRoutineStore:
			raise RuntimeError(
				f"Overlapped structure with address 0x{addr:x} has a completion routine queued already. "
				"Only one completion routine for one overlapped structure can be queued at a time.",
			)

		# Generate a weak reference to the function
		reference = BoundMethodWeakref(func) if ismethod(func) else AnnotatableWeakref(func)
		reference.funcName = repr(func)

		self._completionRoutineStore[addr] = (reference, overlapped)
		return self._internalCompletionRoutine

	def stop(self, timeout: typing.Optional[float] = None):
		if not self.is_alive():
			raise RuntimeError("Thread is not running")
		self.exit = True
		# Wake up the thread. It will exit when it sees exit is True.
		# We do this by queuing a fake lambda that does nothing.
		# L{queueAsApc} will ensure that the APC exits early when the thread is about to exit.

		def fakeApc(param):
			return None

		self.queueAsApc(fakeApc)
		self.join(timeout)
		self.exit = False
		winKernel.closeHandle(self.handle)
		self.handle = None

	def run(self):
		try:
			while True:
				ctypes.windll.kernel32.SleepEx(winKernel.INFINITE, True)
				if self.exit:
					break
		except Exception:
			log.critical("Exception in IoThread function", exc_info=True)
			stacks = getFormattedStacksForAllThreads()
			log.info(f"Listing stacks for Python threads after IoThread crash:\n{stacks}")
