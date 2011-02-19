#touchDeviceDrivers/synaptics.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 Aleksey Sadovoy <lex@progger.ru>

import collections
import math
from comtypes.client import CreateObject, GetEvents
import comtypes.gen.SYNCTRLLib as synlib
import config
from logHandler import log
import touchReview
import tones
import speech

class TouchDeviceDriver(touchReview.TouchDeviceDriver):
	"""Synaptics touchpad driver.
	"""
	name="synaptics"
	#: Synaptics API object instance
	#: @type: L{synlib.SynAPICtrl}
	api=None
	#TODO: determine it programatically
	dimensions=(160, 120)

	@classmethod
	def check(cls):
		try:
			cls.api=CreateObject('SynCtrl.SynAPICtrl')
		except WindowsError:
			return False
		cls.api.initialize()
		return cls.api.FindDevice(synlib.SE_ConnectionAny, synlib.SE_DeviceTouchPad, -1)>=0

	def __init__(self, device="default"):
		self.isAcquired=False
		self._lastKnownCoords=(0,0)
		self._lastContactCoords=(0,0)
		self._lastContactTimestamp=0
		self._lastTapTimestamp=0
		self.pad=CreateObject('SynCtrl.SynDeviceCtrl')
		self.deviceHandle=None
		self.packet=CreateObject('SynCtrl.SynPacketCtrl')
		self.conn=GetEvents(self.pad, self)
		log.info(self.api.GetStringProperty(synlib.SP_VersionString))
		self._set_device(device)
		#We do not need events until the device is acquired
		self.pad.deactivate()

	def configureDevice(self):
		"""Configures the device as required by this driver.
		"""
		#We don't need gestures besides tap, so disable all others to simplify packet recognition.
		self._oldGestures=self.pad.GetLongProperty(synlib.SP_Gestures)
		self.pad.SetLongProperty(synlib.SP_Gestures, synlib.SF_GestureTap)
		#Set report rate to low, for touchpad not to anoy NVDA too often
		self._oldReportRate=self.pad.GetLongProperty(synlib.SP_ReportRate)
		self.pad.SetLongProperty(synlib.SP_ReportRate, 0)
		#enable the device if it is disabled by user.
		self._oldDisableState=self.pad.GetLongProperty(synlib.SP_DisableState)
		self.pad.SetLongProperty(synlib.SP_DisableState, 0)

	def revertDeviceConfiguration(self):
		"""Reverts the device configuration to the saved state.
		"""
		self.pad.SetLongProperty(synlib.SP_Gestures, self._oldGestures)
		self.pad.SetLongProperty(synlib.SP_ReportRate, self._oldReportRate)
		self.pad.SetLongProperty(synlib.SP_DisableState, self._oldDisableState)

	def terminate(self):
		if self.isAcquired:
			self.unacquire()
		del self.conn

	def acquire(self):
		self.configureDevice()
		#receive events from the device
		self.pad.activate()
		#Get an exclussive access to the device
		self.pad.acquire(synlib.SF_AcquireAll)
		self.isAcquired=True

	def unacquire(self):
		#Release the device to be usable by others, esp. to control mouse
		self.pad.unacquire()
		#unsubscribe from packet events
		self.pad.deactivate()
		self.isAcquired=False
		self.revertDeviceConfiguration()

	def _get_device(self):
		return self.pad.GetStringProperty(synlib.SP_ShortName)

	def retrieveDeviceBorders(self):
		"""Requests and saves the lowest and highest values that can be reported by the device.
		"""
		self.xLoBorder=self.pad.GetLongProperty(synlib.SP_XLoRim)
		self.xHiBorder=self.pad.GetLongProperty(synlib.SP_XHiRim)
		self.yLoBorder=self.pad.GetLongProperty(synlib.SP_YLoRim)
		self.yHiBorder=self.pad.GetLongProperty(synlib.SP_YHiRim)

	def _set_device(self, id):
		handle=-1
		#The device may change, so unacquire it first
		isAcquired=self.isAcquired
		if isAcquired:
			self.unacquire()
		try:
			while True:
				handle=self.api.FindDevice(synlib.SE_ConnectionAny, synlib.SE_DeviceTouchPad, handle)
				if handle==-1:
					raise LookupError("device '%d' not found"%id)
				self.pad.select(handle)
				if id=="default" or id==self.pad.GetStringProperty(synlib.SP_ShortName):
					self.deviceHandle=handle
					break
		finally:
			if self.deviceHandle is not None:
				self.pad.select(self.deviceHandle)
				self.retrieveDeviceBorders()
			if isAcquired:
				self.acquire()

	def _get_availableDevices(self):
		currHandle=self.pad.GetLongProperty(synlib.SP_Handle)
		#The device may change, so unacquire it first
		isAcquired=self.isAcquired
		if isAcquired:
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
			if isAcquired:
				self.acquire()

	def calibrate(self, x, y):
		"""Calibrates the borders of the device.
		Borders received by L{receiveBorders} may be not precise, so it is better to adjust them at runtime.
		TODO: cache calibration results in the config
		"""
		self.xLoBorder=min(x, self.xLoBorder)
		self.yLoBorder=min(y, self.yLoBorder)
		self.xHiBorder=max(x, self.xHiBorder)
		self.yHiBorder=max(y, self.yHiBorder)

	def translateDeviceCoords(self, x,y):
		"""Converts device-specific coordinates to relative coordinates used by NVDA.
		@returns: the tuple of relative coordinates
		@rtype: tuple(int,int)
		""" 
		#[loBorder..hiBorder] is a closed range, that is, both ends are included. So, actually, we get hiBorder-loBorder+1 possible values
		relX=int((float(x-self.xLoBorder))/(self.xHiBorder-self.xLoBorder+1)*self.dimensions[0])
		#Synaptics y coordinate increases from bottom to top, so invert it appropriately
		relY=self.dimensions[1]-1 -int((float(y-self.yLoBorder))/(self.yHiBorder-self.yLoBorder+1)*self.dimensions[1] )
		return relX,relY

	def OnPacket(self):
		self.pad.LoadPacket(self.packet)
		x=self.packet.x
		y=self.packet.y
		fingerState=self.packet.FingerState
		timestamp=self.packet.TimeStamp
		if fingerState&synlib.SF_FingerPresent:
			#save finger coordinates (used for taps and other gestures where coordinates don't come with the gesture itself)
			self._lastKnownCoords=(x,y)
			self.calibrate(x,y)
		#detect finger contact
		if fingerState&synlib.SF_FingerPresent and not fingerState&synlib.SF_FingerPossTap and timestamp-self._lastContactTimestamp>=50: 
			if self.distance_sq(self._lastContactCoords, (x, y))>625: #eliminate call to math.sqrt
				#speech.speakMessage('%d, %d'%(self.translateDeviceCoords(x, y)))
				touchReview.manager.executeGesture(touchReview.FingerContactGesture(*self.translateDeviceCoords(x,y)))
				self._lastContactCoords=(x, y)
				self._lastContactTimestamp=timestamp
		if fingerState&synlib.SF_FingerTap and timestamp-self._lastTapTimestamp>=175:
			touchReview.manager.executeGesture(touchReview.FingerTapGesture(*self.translateDeviceCoords(*self._lastKnownCoords)))
			self._lastTapTimestamp=timestamp

	@staticmethod
	def distance_sq(a,b):
		return (b[0]-a[0])**2+(b[1]-a[1])**2
