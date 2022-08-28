# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, Burman's Computer and Education Ltd.

import ctypes
import serial

from ctypes import byref
from ctypes.wintypes import DWORD
from logHandler import log
from serial.win32 import (
	ERROR_IO_PENDING,
	EV_RXCHAR,
	GetLastError,
	SetCommMask
)
from threading import (
	Event,
	Timer,
	Thread
)
from typing import Callable

from brailleDisplayDrivers.albatross.constants import KC_INTERVAL


# Controls most of read operations and tries to reconnect when needed
# Suspended most of time.
class ReadThread(Thread):
	def __init__(
			self,
			readFunction: Callable,
			disableFunction: Callable,
			event: Event,
			dev: serial.Serial,
			*args,
			**kwargs
	):
		super().__init__(*args, **kwargs)
		self._readFunction = readFunction
		self._disableFunction = disableFunction
		self._event = event
		self._dev = dev

	def run(self):
		data = dwEvtMask = DWORD()
		log.debug(f"{self.name} started")
		while not self._event.isSet():
			# Try to reconnect if port is not open
			if not self._dev.is_open:
				log.debug(
					f"Calling {self._readFunction.__name__}, port {self._dev.name} not open"
				)
				self._readFunction()
				if not self._dev.is_open:
					log.debug(
						f"Sleepin {KC_INTERVAL} seconds, port {self._dev.name} not open"
					)
					self._event.wait(KC_INTERVAL)
					continue
			# If any of I/O function fails, it should not crash the thread.
			try:
				if not SetCommMask(self._dev._port_handle, EV_RXCHAR):
					# Exiting
					if self._event.isSet():
						break
					self._disableFunction()
					log.debug("SetCommMask failed")
					continue
				result = ctypes.windll.kernel32.WaitCommEvent(
					self._dev._port_handle,
					byref(dwEvtMask),
					byref(self._dev._overlapped_read)
				)
				if not result and GetLastError() != ERROR_IO_PENDING:
					if self._event.isSet():
						break
					self._disableFunction()
					log.debug("WaitCommEvent failed")
					continue
				result = ctypes.windll.kernel32.GetOverlappedResult(
					self._dev._port_handle,
					byref(self._dev._overlapped_read),
					byref(data), True
				)
				if result:
					log.debug(f"Calling function {self._readFunction.__name__} for read")
					self._readFunction()
				else:
					if self._event.isSet():
						break
					self._disableFunction()
					log.debug("GetOverLappedResult failed")
			# See comment in _somethingToRead
			except (OSError, AttributeError):
				if self._event.isSet():
					break
				else:
					self._disableFunction()
					log.debug("", exc_info=True)
		log.debug(f"Exiting {self.name}")


# Timer is used to send BOTH_BYTES regularly to keep connection
# (copied from
# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds)
class RepeatedTimer(object):
	def __init__(
			self,
			interval: float,
			function: Callable,
			*args,
			**kwargs
	):
		self.interval = interval
		self._timer = Timer(self.interval, self._run)
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False
