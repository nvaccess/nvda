#touchDeviceDrivers/synaptics.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 Aleksey Sadovoy <lex@progger.ru>

import threading
from comtypes.client import CreateObject, GetEvents
import pythoncom #until comtypes.client.PumpEvents gets fixed
import comtypes.gen.SYNCTRLLib as synlib
import touchReview

class TouchDeviceDriver(touchReview.TouchDeviceDriver):
	"""Synaptics touchpad driver.
	"""
	name="synaptics"
	#: Synaptics API object instance
	#: @type: L{synlib.SynAPICtrl}
	api=None

	@classmethod
	def check(cls):
		try:
			cls.api=CreateObject('SynCtrl.SynAPICtrl')
		except WindowsError:
			return False
		cls.api.initialize()
		return cls.api.FindDevice(synlib.SE_ConnectionAny, synlib.SE_DeviceTouchPad, -1)>=0

	def __init__(self):
		self.acquired=False
		self.pad=CreateObject('SynCtrl.SynDeviceCtrl')
		self.pad.select(0)

	def acquire(self):
		self.pad.activate()
		self.pad.acquire(0)

	def unacquire(self):
		self.pad.unacquire()
		self.pad.deactivate()
