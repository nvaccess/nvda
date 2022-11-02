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
import extensionPoints
import uuid

pre_IoThreadStop = extensionPoints.Action()
"""
Executed when the i/o thread is to be stopped.
This allows components and add-ons to clean up or reset state before background thread shut down.
Handlers are called with one argument.
@param ioThread: The thread to shut down
@type ioThread: IoThread
"""


class IoThread:
	"""A thread used for background writes and raw I/O, e.g. for braille displays.
	"""

	thread: typing.Optional[threading.Thread] = None
	exit: bool = False
	_apcReferences: typing.Dict[uuid.UUID, winKernel.PAPCFUNC]

	def __init__(self):
		self._apcReferences = dict()

	def start(self):
		if self.thread:
			return
		thread = self.thread = threading.Thread(
			name=f"{self.__class__.__module__}.{self.__class__.__qualname__}",
			target=self.func
		)
		thread.daemon = True
		thread.start()
		self.handle = ctypes.windll.kernel32.OpenThread(winKernel.THREAD_SET_CONTEXT, False, thread.ident)

	def queueAsApc(
			self,
			func: typing.Callable[[int], None],
			param: int = 0
	):
		if not self.handle:
			raise RuntimeError("IoThread not running")

		# generate an UUID that will be used to cleanup the APC when it is finished
		apcUuid = uuid.uuid4()

		@winKernel.PAPCFUNC
		def apc(param: int):
			try:
				if self.exit:
					return
				func(param)
			except Exception:
				log.error("Error in APC function queued to IoThread", exc_info=True)
			finally:
				del self._apcReferences[apcUuid]

		self._apcReferences[apcUuid] = apc
		ctypes.windll.kernel32.QueueUserAPC(apc, self.handle, param)

	def stop(self, timeout: typing.Optional[float] = None):
		if not self.thread:
			return
		self.exit = True
		# Wake up the thread. It will exit when it sees exit is True.
		# We do this by queuing a fake lambda that does nothing.
		# L{queueAsApc} will ensure that the APC exits early when the thread is about to exit.
		self.queueAsApc(lambda param: None)
		self.thread.join(timeout)
		self.exit = False
		winKernel.closeHandle(self.handle)
		self.handle = None
		self.thread = None

	def func(self):
		while True:
			ctypes.windll.kernel32.SleepEx(winKernel.INFINITE, True)
			if self.exit:
				break
