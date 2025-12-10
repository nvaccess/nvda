# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
from _bridge.components.proxies.synthDriver import SynthDriverProxy
from .launcher import createSynthDriverHost32, isSynthDriverHost32RuntimeAvailable

class SynthDriverProxy32(SynthDriverProxy):
	""" A SynthDriver proxy class that loads a synthDriver using  the 32 bit SynthDriver host. """ 
	synthDriver32Path: str
	synthDriver32Name: str

	@classmethod
	def check(cls):
		return isSynthDriverHost32RuntimeAvailable()

	def __init__(self):
		self._host = createSynthDriverHost32()
		self._host.registerSynthDriversPath(self.synthDriver32Path)
		remoteDriver = self._host.SynthDriver(self.synthDriver32Name)
		super().__init__(remoteDriver)
