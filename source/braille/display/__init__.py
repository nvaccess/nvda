# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import pkgutil
import typing
from locale import strxfrm
from typing import (
	Any,
	Callable,
	Generator,
	List,
	NamedTuple,
	Optional,
	Tuple,
	Type,
)

import brailleDisplayDrivers
import hwPortUtils
from logHandler import log

from .driver import BrailleDisplayDriver, _getDisplayDriver


class DisplayDimensions(NamedTuple):
	numRows: int
	numCols: int

	@property
	def displaySize(self) -> int:
		return self.numCols * self.numRows


def getDisplayList(excludeNegativeChecks=True) -> List[Tuple[str, str]]:
	"""Gets a list of available display driver names with their descriptions.
	@param excludeNegativeChecks: excludes all drivers for which the check method returns C{False}.
	@type excludeNegativeChecks: bool
	@return: list of tuples with driver names and descriptions.
	"""
	displayList = []
	# The display that should be placed at the end of the list.
	lastDisplay = None
	for display in getDisplayDrivers():
		try:
			if not excludeNegativeChecks or display.check():
				if display.name == "noBraille":
					lastDisplay = (display.name, display.description)
				else:
					displayList.append((display.name, display.description))
			else:
				log.debugWarning(f"Braille display driver {display.name} reports as unavailable, excluding")
		except:  # noqa: E722
			log.error("", exc_info=True)
	displayList.sort(key=lambda d: strxfrm(d[1]))
	if lastDisplay:
		displayList.append(lastDisplay)
	return displayList


# Maps old braille display driver names to new drivers that supersede old drivers.
# Ensure that if a user has set a preferred driver which has changed name, the new
# user preference is retained.
RENAMED_DRIVERS = {
	# "oldDriverName": "newDriverName"
	"syncBraille": "hims",
	"alvaBC6": "alva",
	"hid": "hidBrailleStandard",
}


def getSerialPorts(filterFunc=None) -> typing.Iterator[typing.Tuple[str, str]]:
	"""Get available serial ports in a format suitable for L{BrailleDisplayDriver.getManualPorts}.
	@param filterFunc: a function executed on every dictionary retrieved using L{hwPortUtils.listComPorts}.
		For example, this can be used to filter by USB or Bluetooth com ports.
	@type filterFunc: callable
	"""
	if filterFunc and not callable(filterFunc):
		raise TypeError("The provided filterFunc is not callable")
	for info in hwPortUtils.listComPorts():
		if filterFunc and not filterFunc(info):
			continue
		if "bluetoothName" in info:
			yield (
				info["port"],
				# Translators: Name of a Bluetooth serial communications port.
				_("Bluetooth Serial: {port} ({deviceName})").format(
					port=info["port"],
					deviceName=info["bluetoothName"],
				),
			)
		else:
			yield (
				info["port"],
				# Translators: Name of a serial communications port.
				_("Serial: {portName}").format(portName=info["friendlyName"]),
			)


def getDisplayDrivers(
	filterFunc: Optional[Callable[[Type[BrailleDisplayDriver]], bool]] = None,
) -> Generator[Type[BrailleDisplayDriver], Any, Any]:
	"""Gets an iterator of braille display drivers meeting the given filter callable.
	@param filterFunc: an optional callable that receives a driver as its only argument and returns
		either True or False.
	@return: Iterator of braille display drivers.
	"""
	for loader, name, isPkg in pkgutil.iter_modules(brailleDisplayDrivers.__path__):
		if name.startswith("_"):
			continue
		try:
			display = _getDisplayDriver(name)
		except Exception:
			log.error(
				f"Error while importing braille display driver {name}",
				exc_info=True,
			)
			continue
		if not filterFunc or filterFunc(display):
			yield display
