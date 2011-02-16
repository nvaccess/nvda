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
import inputCore

"""Touch review support.
"""

class TouchGesture(inputCore.InputGesture):
	"""The base class for touch gestures.
	Every touch gesture should contain position in relative coordinates, representing the place where the gesture was initiated.
	By definition, the point (0,0) is situated at the upper left corner of the touch surface; x increases to the right and y increases to the bottom.
	The Largest possible values for x and y are determined by L{TouchDeviceDriver.dimensions} property.
	"""
	#: identifier of the gesture e.g. 'tap'
	#: @type: str
	id=""
	#: L{TouchRegion} this gesture coresponds to, if any
	#: @type: L{TouchRegion} or C{None}
	region=None

	shouldReportAsCommand=False

	def __init__(self, x,y):
		"""Creates a new touch gesture.
		@param x: x component of the gesture in relative coordinates.
		@type x: int
		@param y: y component of the gesture in relative coordinates.
		@type y: int
		"""
		super(TouchGesture,self).__init__()
		self.x=x
		self.y=y

	def _get_identifiers(self):
		region="(%s)"%self.region.name if self.region is not None else ""
		return ("touch%s:%s"%(region,self.id),)

	def _get_scriptableObject(self):
		if self.region is not None:
			return self.region
		else:
			return manager


class FingerContactGesture(TouchGesture):
	"""Represents a moderate contact of a finger with a touch surface.
	It indicates finger presence on the device with middle presure (not a tap) or) soft finger movement.
	"""
	id="fingercontact"
	displayName=_("finger contact")


class FingerTapGesture(TouchGesture):
	"""Represents a single tap on the surface.
	"""
	id="fingertap"
	displayName=_("finger tap")


class DoubleFingerTapGesture(TouchGesture):
	"""Represents a double tap on the surface.
	"""
	id="doublefingertap"
	displayName=_("double finger tap")


class TouchRegion(baseObject.ScriptableObject):
	"""Represents an active zone on touch surface.
	An example of the touch region can be a rectangle that affects gestures performed  within its bounds.
	L{TouchReviewManager} calls L{shouldAcceptGesture} on every instantiated gesture for every registered region, in the defined order. On C{True}, it marks the gesture appropriately, i.a. sets the gesture's region property.
	"""
	#: an unique name of the region
	#: @type: str
	name=""

	def _get_weight(self):
		"""The "weight" of this region. 
		Regions are tested in order of their weights. For example, it can be an area of a rectangle.
		@rtype: int
		"""
		raise NonImplementedError

	def shouldAcceptGesture(self, gesture):
		"""Checks if the gesture is affected by this region.
		@param gesture: the gesture to check
		@type gesture: L{TouchGesture}
		@returns: whether the gesture is accepted
		@rtype: bool
		"""
		raise NonImplementedError


class TouchReviewManager(baseObject.ScriptableObject):
	"""Manages touch review in NVDA.
	it implements touch review commands, handles touch regions and manages touch device drivers.
	"""

	def __init__(self):
		super(TouchReviewManager,self).__init__()
		#: The device receiving input from
		#: @type: L{TouchDeviceDriver}
		self.device=None
		#: whether touch review is curently active
		#: @type: bool
		self.isActive=False
		#: The list of registered touch regions.
		#: @type: list
		self.touchRegions=[]

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

	def addRegion(self, region):
		"""Adds a new region to the list of registered regions.
		@param region: The region to add
		@type region: L{TouchRegion}
		"""
		self.touchRegions.append(region)
		self.touchRegions.sort(key=lambda r: r.weight)

	def removeRegion(self,region):
		"""Removes a specified region from the list of registered regions.
		@param region: The region to remove.
		@type region: L{TouchRegion}
		"""
		self.touchRegions.remove(region)

	def executeGesture(self, gesture):
		"""Processes the gesture with touch regions and passes it to the input core.
		touch device drivers should call this when they have a gesture to execute instead of L{inputCore.InputManager.executeGesture}.
		@param gesture: the gesture to execute
		@type gesture: L{TouchGesture}
		"""
		for region in self.touchRegions:
			if region.shouldAcceptGesture(gesture):
				gesture.region=region
				break
		inputCore.manager.executeGesture(gesture)


#: The singleton touch review manager instance.
#: @type: L{TouchReviewManager}
manager = None


class TouchDeviceDriver(baseObject.AutoPropertyObject):
	"""An abstract touch device driver.
	Each touch device driver should be a separate Python module in the root touchDrivers directory containing a TouchDeviceDriver class which inherits from this base class.
	Touch device drivers are responsive for handling input from the sensor-enabled devices and translating it to the NVDA gestures.
	each driver supports devices of the particular manufacturer, there can be more than one device connected of one manufacturer.
	At the very least, subclasses must overwrite L{check} and L{_get_dimensions}.
	"""

	#: the name of the driver
	#: @type: str
	name=""

	@classmethod
	def check(cls):
		"""Checks if this driver can be used e.g. the device is present and appropriate manufacturer drivers are functioning.
		"""
		raise NotImplementedError

	def __init__(self, deviceID="default"):
		"""Initializes the driver and specified device.
		Postcondition: the device is ready to be acquired.
		@param deviceID: The driver-specific identifier  of the device to use or 'default'
		@type deviceID: str
		"""

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
		@rtype: collections.OrderedDict
		"""
		return collections.OrderedDict()

	def _get_dimensions(self):
		"""The size of the device i.e. the range in which device reports touch gestures.
		@returns:  tuple consisting of (with, height)
		@rtype: tuple(int,int)
		"""
		raise NotImplementedError

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
