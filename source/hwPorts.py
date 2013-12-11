#hwPorts.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 NV Access Limited

"""Support for devices connected via hardware connection ports.
"""

import collections

#: This port should only be probed when explicitly requested by the user.
#: This is usually used for ports such as serial ports which might not be exclusively associated with the device
#: and the only way to determine this is to send a query to the port,
#: which might cause unexpected behaviour for some devices.
PROBE_MANUAL = "manual"
#: This port can be safely probed automatically at regular intervals.
#: This is usually used for interfaces such as Bluetooth which don't notify the system
#: when a device becomes available.
PROBE_POLL = "poll"
#: This port should be probed when the system notifies that a device was added/removed.
#: This is usually used for interfaces such as USB which notify the system
#: when a device is connected.
PROBE_NOTIFY = "notify"

class HardwarePort(
	collections.namedtuple("HardwarePort", ("name", "description", "probeType"))
):
	"""A port for connecting to a braille display.
	"""

	def __new__(cls, name, description, probeType=PROBE_MANUAL):
		"""Constructor.
		@param name: The internal name of the port as passed to the driver.
		@type port: unicode
		@param description: The description of the port as shown to the user.
		@type description: unicode
		@param probeType: How the port should be probed for a device;
			one of the C{PROBE_*} constants.
		"""
		return super(HardwarePort, cls).__new__(cls, name, description, probeType)

#: A port for connecting via USB.
USB_PORT = HardwarePort("USB", "USB", PROBE_NOTIFY)
#: A port for connecting via Bluetooth.
BLUETOOTH_PORT = HardwarePort("bluetooth", "Bluetooth", PROBE_POLL)
#: Generally only used in the GUI; drivers should not use.
# Translators: An option in a list of ports for connecting to a device such as a braille display
# which indicates that the correct port should be determined automatically.
AUTO_PORT = HardwarePort("auto", _("Automatic"))

def getSerialPorts():
	"""Get all available serial ports for use in device port lists.
	@return: All available serial ports.
	@rtype: iterable of L{HardwarePort} instances
	"""
	import hwPortUtils
	for portInfo in hwPortUtils.listComPorts(onlyAvailable=True):
		yield HardwarePort(portInfo["port"],
			# Translators: Name of a serial communications port.
			# {portName} will be replaced with the name of the port.
			_("Serial: {portName}").format(portName=portInfo["friendlyName"]),
			PROBE_MANUAL)

def getUiPorts(ports):
	"""Get the ports that should be presented to the user.
	If there are ports which can be probed automatically,
	an automatic port will be included at the start.
	This should only be used by user interface code, not by drivers.
	"""
	if not isinstance(ports, list):
		ports = list(ports)
	if len(ports) == 1:
		return ports
	addAuto = False
	for port in ports:
		if port.probeType != PROBE_MANUAL:
			addAuto = True
	if addAuto:
		ports.insert(0, AUTO_PORT)
	return ports

def getAutoPorts(ports):
	"""Get the ports that can be probed automatically.
	This should not be used by drivers.
	"""
	for port in ports:
		if port.name == AUTO_PORT.name:
			# This is for compatibility with old drivers.
			yield port
			return
		if port.probeType != PROBE_MANUAL:
			yield port
