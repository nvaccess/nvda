#touchDeviceDrivers/synaptics.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 Aleksey Sadovoy <lex@progger.ru>

import collections
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
		self.acquired=True

	def unacquire(self):
		self.pad.unacquire()
		self.pad.deactivate()
		self.acquired=False

	def _get_device(self):
		return self.pad.GetStringProperty(synlib.SP_ShortName)

	def _set_device(self, id):
		handle=-1
		currHandle=self.pad.GetLongProperty(synlib.SP_Handle)
		#The device may change, so unacquire it first
		acquired=self.acquired
		if acquired:
			self.unacquire()
		try:
			while True:
				handle=self.api.FindDevice(synlib.SE_ConnectionAny, synlib.SE_DeviceTouchPad, handle)
				if handle==-1:
					raise LookupError("device '%d' not found"%id)
				self.pad.select(handle)
				if id==self.pad.GetStringProperty(synlib.SP_ShortName):
					currHandle=handle
					break
		finally:
			self.pad.select(currHandle)
			if acquired:
				self.acquire()

	def _get_availableDevices(self):
		currHandle=self.pad.GetLongProperty(synlib.SP_Handle)
		#The device may change, so unacquire it first
		acquired=self.acquired
		if acquired:
			self.unacquire()
		devices=collections.OrderedDict()
		handle=-1
		try:
			while True:
				handle=self.api.FindDevice(synlib.SE_ConnectionAny, synlib.SE_DeviceTouchPad, handle)
				if handle==-1:
					return devices
				self.pad.select(handle)
				devices[self.pad.GetStringProperty(synlib.SP_ShortName)]=self.pad.GetStringProperty(synlib.SP_ModelString)
		finally:
			self.pad.select(currHandle)
			if acquired:
				self.acquire()
