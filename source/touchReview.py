#touchReview.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 Aleksey Sadovoy <lex@progger.ru>

import pkgutil
import collections
import baseObject
import config
from logHandler import log
import touchDeviceDrivers

"""Touch review support.
"""

class TouchReviewManager(baseObject.ScriptableObject):
	"""Manages touch review in NVDA.
	it implements touch review commands and manages touch device drivers.
	"""

	def __init__(self):
		#: The device receiving input from
		#: @type: L{TouchDeviceDriver}
		self.device=None
		#: whether touch review is curently active
		#: @type: bool
		self.isActive=False

	def terminate(self):
		if self.isActive:
			self.deactivate()
		self.device.terminate()
		self.device=None

	def activate(self):
		"""Activates touch review, acquiring the input device.
		"""
		if not self.isActive:
			self.device.acquire()
			self.isActive=True

	def deactivate(self):
		"""Deactivates touch review, releasing the input device.
		"""
		if self.isActive:
			self.device.unacquire()
			self.isActive=False

	def setDeviceByName(self, name):
		"""Sets the device by its name.
		name should consist of device driver name, , optionally followed by a dot and a driver-specific identifier.
		@param name: a name of the device or 'default' for the default one
		@type name: str
		"""
		drivers=self.getAvailableDrivers()
		if name=="default":
			#choose a first existing device that is not  dummy if possible
			try:
				driverName=[d.name for d in drivers if not d.name=="dummy"][0]
			except IndexError:
				driverName="dummy"
			deviceID=None
		else:
			lst=name.split('.', 1)
			driverName=lst[0]
			deviceID=lst[1] if len(lst)==2 else None
		for Driver in drivers:
			if Driver.name==driverName:
				if self.device:
					try:
						self.device.terminate()
					except:
						log.error("Error terminating touch device", exc_info=True)
				self.device=Driver()
				if deviceID is not None:
					self.device.device=deviceID
				return
		raise LookupError("touch device '%s' not found"%name)

	@staticmethod
	def getAvailableDrivers():
		"""Returns a list of touch device drivers which report availability.
		@rtype: list
		"""
		driverList = []
		for loader, name, isPkg in pkgutil.iter_modules(touchDeviceDrivers.__path__):
			if name.startswith('_'):
				continue
			try:
				Driver = __import__("touchDeviceDrivers.%s" % name, globals(), locals(), ("touchDeviceDrivers",)).TouchDeviceDriver
				if Driver.check():
					driverList.append(Driver)
				else:
					log.debugWarning("Touch device driver '%s' doesn't pass the check, excluding from list"%name)
			except:
					log.error("",exc_info=True)
		return driverList

#: The singleton touch review manager instance.
#: @type: L{TouchReviewManager}
manager = None

class TouchDeviceDriver(baseObject.AutoPropertyObject):
	"""An abstract touch device driver.
	Each touch device driver should be a separate Python module in the root touchDrivers directory containing a TouchDeviceDriver class which inherits from this base class.
	Touch device drivers are responsive for handling input from the sensor-enabled devices and translating it to the NVDA gestures.
	each driver supports devices of the particular manufacturer, there can be more than one device connected of one manufacturer.
	"""

	#: the name of the driver
	#: @type: str
	name=""

	@classmethod
	def check(cls):
		"""Checks if this driver can be used e.g. the device is present and appropriate manufacturer drivers are functioning.
		"""
		raise NotImplementedError

	def _set_device(self, ID):
		"""Sets the device to use.
		@param ID: the identifier of the device.
		@type ID: str
		"""
		pass

	def _get_device(self):
		"""Returns identifier of the device in use.
		@rtype: str
		"""
		return ""

	def _get_availableDevices(self):
		"""Returns list of the connected devices.
		It is an ordered dictionary where keys are identifiers and values are human-readable descriptions.
		Identifiers should include the driver name followed by a dot and the ID of the device.
		@rtype: collections.OrderedDict
		"""
		return collections.OrderedDict()

	def acquire(self):
		"""Start intercepting input from the device.
		Postcondition: the device may not perform its usual functions e.g. touchpad will stop control the mouse.
		"""
		pass

	def unacquire(self):
		"""Stop actively intercepting input from the device.
		postcondition: Device should return to its usual functioning e.g. touchpad will again control the mouse.
		"""
		pass

	def terminate(self):
		"""Terminates the driver, releasing all resources.
		"""
		pass

def initialize():
	"""Initializes touch review functionality.
	"""
	global manager
	config.addConfigDirsToPythonPackagePath(touchDeviceDrivers)
	manager=TouchReviewManager()
	manager.setDeviceByName(config.conf["touchReview"]["device"])
	log.info("Using touch device driver '%s'"%manager.device.name)
	if config.conf["touchReview"]["active"]:
		manager.activate()

def terminate():
	"""Terminates touch reviev functionality.
	"""
	global manager
	manager.terminate()
	manager=None
