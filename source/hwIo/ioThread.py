# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2016-2022 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
# Leonard de Ruijter

import ctypes
import ctypes.wintypes
import threading
import winKernel
import typing
from logHandler import log
import serial.win32
import uuid
from contextlib import contextmanager
from extensionPoints.util import AnnotatableWeakref, BoundMethodWeakref
from inspect import ismethod
from buildVersion import version_year
import NVDAState

LPOVERLAPPED_COMPLETION_ROUTINE = ctypes.WINFUNCTYPE(
	None,
	ctypes.wintypes.DWORD,
	ctypes.wintypes.DWORD,
	serial.win32.LPOVERLAPPED
)
apcsWillBeStronglyReferenced = version_year < 2024 and NVDAState._allowDeprecatedAPI()
"""
Starting from NVDA 2024.1, we will weakly reference functions wrapped in an APC.
This will ensure that objects from which APCs have been queuedwon't be scattering around
when the APC is never executed.
Wrapped methods are now strongly referenced due to an oversight in NVDA 2023.1.
"""


class IoThread(threading.Thread):
	"""A thread used for background writes and raw I/O, e.g. for braille displays.
	"""

	exit: bool = False
	_apcReferences: typing.Dict[uuid.UUID, winKernel.PAPCFUNC]

	def __init__(self):
		super().__init__(
			name=f"{self.__class__.__module__}.{self.__class__.__qualname__}",
			daemon=True
		)
		self._apcReferences = dict()

	def start(self):
		super().start()
		self.handle = ctypes.windll.kernel32.OpenThread(winKernel.THREAD_SET_CONTEXT, False, self.ident)

	@contextmanager
	def autoDeleteApcReference(self, apcUuid: uuid.UUID):
		try:
			yield
		finally:
			del self._apcReferences[apcUuid]

	def _getApc(
			self,
			func: typing.Callable[[int], None],
			param: int = 0,
			_alwaysReferenceWeakly: bool = True
	) -> winKernel.PAPCFUNC:
		"""Internal method to safely wrap a python function in an Asynchronous Procedure Call (APC).
		The generated APC is saved in a cache on the IoThread instance
		and automatically cleaned when the call is complete.
		Note that starting from NVDA 2024.1, the wrapped python function will be weakly referenced,
		therefore the caller should keep a reference to the python function (not the APC itself).
		@param func: The function to be wrapped in an APC.
		@param param: The parameter passed to the APC when called.
		@returns: The wrapped APC.
		"""
		if not self.is_alive():
			raise RuntimeError("Thread is not running")

		# generate an UUID that will be used to cleanup the APC when it is finished
		apcUuid = uuid.uuid4()
		useWeak = _alwaysReferenceWeakly or not apcsWillBeStronglyReferenced
		if useWeak:
			# Generate a weak reference to the function
			reference = BoundMethodWeakref(func) if ismethod(func) else AnnotatableWeakref(func)
			reference.funcName = repr(func)

		@winKernel.PAPCFUNC
		def apc(param: int):
			with self.autoDeleteApcReference(apcUuid):
				if self.exit:
					return
				if useWeak:
					function = reference()
					if not function:
						log.debugWarning(f"Not executing queued APC {reference.funcName} because reference died")
						return
				else:
					function = func

				try:
					function(param)
				except Exception:
					log.error(f"Error in APC function {function!r} queued to IoThread", exc_info=True)

		self._apcReferences[apcUuid] = apc
		return apc

	def queueAsApc(
			self,
			func: typing.Callable[[int], None],
			param: int = 0
	):
		"""safely queues an Asynchronous Procedure Call (APC) created from a python function.
		The generated APC is saved in a cache on the IoThread instance
		and automatically cleaned when the call is complete.
		Note that starting from NVDA 2024.1, the wrapped python function will be weakly referenced,
		therefore the caller should keep a reference to the python function.
		@param func: The function to be wrapped in an APC.
		@param param: The parameter passed to the APC when called.
		"""
		apc = self._getApc(func, param, _alwaysReferenceWeakly=False)
		ctypes.windll.kernel32.QueueUserAPC(apc, self.handle, param)

	def setWaitableTimer(
			self,
			handle: typing.Union[int, ctypes.wintypes.HANDLE],
			dueTime: int,
			func: typing.Callable[[int], None],
			param: int = 0
	):
		""""Safe wrapper around winKernel.setWaitableTimer to ensure that the queued APC
		is available when called.
		The generated APC is saved in a cache on the IoThread instance
		and automatically cleaned when the call is complete.
		The wrapped python function is weakly referenced, therefore the caller should
		keep a reference to the python function.
		@param handle: A handle to the timer object.
		@param dueTime: Relative time (in miliseconds).
		@param func: The function to be executed when the timer elapses.
		@param param: The parameter passed to the APC when called.
		"""
		apc = self._getApc(func, param)
		winKernel.setWaitableTimer(handle, dueTime, completionRoutine=apc, arg=param)

	def getCompletionRoutine(
			self,
			func: typing.Callable[[int, int, serial.win32.LPOVERLAPPED], None],
	):
		"""Safely wraps a python function in an overlapped completion routine.
		The generated routine is saved in a cache on the IoThread instance
		and automatically cleaned when the call is complete.
		The wrapped python function is weakly referenced, therefore the caller should
		keep a reference to the python function (not the completion routine itself).
		@param func: The function to be wrapped in a completion routine.
		@returns: The wrapped completion routine.
		"""
		if not self.is_alive():
			raise RuntimeError("Thread is not running")

		# generate an UUID that will be used to cleanup the func when it is finished
		ocrUuid = uuid.uuid4()
		# Generate a weak reference to the function
		reference = BoundMethodWeakref(func) if ismethod(func) else AnnotatableWeakref(func)
		reference.funcName = repr(func)

		@LPOVERLAPPED_COMPLETION_ROUTINE
		def overlappedCompletionRoutine(error: int, numberOfBytes: int, overlapped: serial.win32.LPOVERLAPPED):
			with self.autoDeleteApcReference(ocrUuid):
				if self.exit:
					return
				function = reference()
				if not function:
					log.debugWarning(f"Not executing completion routine {reference.funcName} because reference died")
					return
				try:
					function(error, numberOfBytes, overlapped)
				except Exception:
					log.error(f"Error in overlapped completion routine {func!r}", exc_info=True)

		self._apcReferences[ocrUuid] = overlappedCompletionRoutine
		return overlappedCompletionRoutine

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
		while True:
			ctypes.windll.kernel32.SleepEx(winKernel.INFINITE, True)
			if self.exit:
				break
