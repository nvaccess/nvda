# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/ecoBraille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014-2015 ONCE-CIDAT <cidat.id@once.es>
from typing import List, Tuple

import inputCore
import braille
import hwPortUtils
from hwIo import intToByte
from collections import OrderedDict
from logHandler import log
import serial
import struct
import wx

ECO_KEY_F1 = 0x01
ECO_KEY_F2 = 0x02
ECO_KEY_F3 = 0x04
ECO_KEY_F4 = 0x08
ECO_KEY_F5 = 0x10
ECO_KEY_F6 = 0x20
ECO_KEY_F7 = 0x40
ECO_KEY_F8 = 0x80
ECO_KEY_F9 = 0x0100
ECO_KEY_A = 0x0200
ECO_KEY_F0 = 0x0400
ECO_KEY_S = 0x4000
ECO_KEY_DOWN = 0x10000
ECO_KEY_RIGHT = 0x20000
ECO_KEY_POINT = 0x40000
ECO_KEY_LEFT = 0x80000
ECO_KEY_UP = 0x100000
ECO_START_ROUTING = 0x80000000
ECO_END_ROUTING = 0xD0000000
ECO_KEY_STATUS1 = 0xD5000000
ECO_KEY_STATUS2 = 0xD6000000
ECO_KEY_STATUS3 = 0xD0000000
ECO_KEY_STATUS4 = 0xD1000000

READ_INTERVAL = 50
TIMEOUT = 0.1

keyNames = {
	ECO_KEY_F1: "F1",
	ECO_KEY_F2: "F2",
	ECO_KEY_F3: "F3",
	ECO_KEY_F4: "F4",
	ECO_KEY_F5: "F5",
	ECO_KEY_F6: "F6",
	ECO_KEY_F7: "F7",
	ECO_KEY_F8: "F8",
	ECO_KEY_F9: "F9",
	ECO_KEY_F0: "F0",
	ECO_KEY_A: "A",
	ECO_KEY_S: "S",
	ECO_KEY_UP: "T1",
	ECO_KEY_DOWN: "T5",
	ECO_KEY_RIGHT: "T4",
	ECO_KEY_POINT: "T3",
	ECO_KEY_LEFT: "T2"
}

class ecoTypes:
	TECO_NO_DISPLAY = 0
	TECO_20 = 20
	TECO_40 = 40
	TECO_80 = 80

def eco_in_init(dev: serial.Serial) -> int:
	msg: bytes = dev.read(9)
	if len(msg) < 9:
		return ecoTypes.TECO_80 # Needed to restart NVDA with Ecoplus
	# Command message from EcoBraille is something like that:
	# 0x10 0x02 TT AA BB CC DD 0x10 0x03
	# where TT can be 0xF1 (identification message) or 0x88 (command pressed in the line)
	# If TT = 0xF1, then the next byte (AA) give us the type of EcoBraille line (ECO 80, 40 or 20)
	if (
		(msg[0] == 0x10)
		and (msg[1] == 0x02)
		and (msg[7] == 0x10)
		and (msg[8] == 0x03)
	):
		if msg[2] == 0xf1:  # Initial message
			if msg[3] == 0x80:
				return ecoTypes.TECO_80
			if msg[3] == 0x40:
				return ecoTypes.TECO_40
			if msg[3] == 0x20:
				return ecoTypes.TECO_20
	return ecoTypes.TECO_80 # Needed for changing Braille Settings with Ecoplus

def eco_in(dev: serial.Serial) -> int:
	try:
		msg: bytes = dev.read(9)
	except:
		log.debug("unpacking error", exc_info=True)
		return 0
	# Command message from EcoBraille is something like that:
	# 0x10 0x02 TT AA BB CC DD 0x10 0x03
	# where TT can be 0xF1 (identification message) or 0x88 (command pressed in the line)
	# If TT = 0x88 then AA, BB, CC and DD give us the command pressed in the braille line
	if(
			(msg[0] == 0x10)
			and (msg[1] == 0x02)
			and (msg[7] == 0x10)
			and (msg[8] == 0x03)
			and (msg[2] == 0x88)  # command pressed message
	):
		return (msg[3] << 24) | (msg[4] << 16) | (msg[5] << 8) | msg[6]
	return 0


output_dots_map: List[int] = [
	0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
	0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71,
	0x02, 0x12, 0x22, 0x32, 0x42, 0x52, 0x62, 0x72,
	0x03, 0x13, 0x23, 0x33, 0x43, 0x53, 0x63, 0x73,
	0x04, 0x14, 0x24, 0x34, 0x44, 0x54, 0x64, 0x74,
	0x05, 0x15, 0x25, 0x35, 0x45, 0x55, 0x65, 0x75,
	0x06, 0x16, 0x26, 0x36, 0x46, 0x56, 0x66, 0x76,
	0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77,
	0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0,
	0x81, 0x91, 0xA1, 0xB1, 0xC1, 0xD1, 0xE1, 0xF1,
	0x82, 0x92, 0xA2, 0xB2, 0xC2, 0xD2, 0xE2, 0xF2,
	0x83, 0x93, 0xA3, 0xB3, 0xC3, 0xD3, 0xE3, 0xF3,
	0x84, 0x94, 0xA4, 0xB4, 0xC4, 0xD4, 0xE4, 0xF4,
	0x85, 0x95, 0xA5, 0xB5, 0xC5, 0xD5, 0xE5, 0xF5,
	0x86, 0x96, 0xA6, 0xB6, 0xC6, 0xD6, 0xE6, 0xF6,
	0x87, 0x97, 0xA7, 0xB7, 0xC7, 0xD7, 0xE7, 0xF7,
	0x08, 0x18, 0x28, 0x38, 0x48, 0x58, 0x68, 0x78,
	0x09, 0x19, 0x29, 0x39, 0x49, 0x59, 0x69, 0x79,
	0x0A, 0x1A, 0x2A, 0x3A, 0x4A, 0x5A, 0x6A, 0x7A,
	0x0B, 0x1B, 0x2B, 0x3B, 0x4B, 0x5B, 0x6B, 0x7B,
	0x0C, 0x1C, 0x2C, 0x3C, 0x4C, 0x5C, 0x6C, 0x7C,
	0x0D, 0x1D, 0x2D, 0x3D, 0x4D, 0x5D, 0x6D, 0x7D,
	0x0E, 0x1E, 0x2E, 0x3E, 0x4E, 0x5E, 0x6E, 0x7E,
	0x0F, 0x1F, 0x2F, 0x3F, 0x4F, 0x5F, 0x6F, 0x7F,
	0x88, 0x98, 0xA8, 0xB8, 0xC8, 0xD8, 0xE8, 0xF8,
	0x89, 0x99, 0xA9, 0xB9, 0xC9, 0xD9, 0xE9, 0xF9,
	0x8A, 0x9A, 0xAA, 0xBA, 0xCA, 0xDA, 0xEA, 0xFA,
	0x8B, 0x9B, 0xAB, 0xBB, 0xCB, 0xDB, 0xEB, 0xFB,
	0x8C, 0x9C, 0xAC, 0xBC, 0xCC, 0xDC, 0xEC, 0xFC,
	0x8D, 0x9D, 0xAD, 0xBD, 0xCD, 0xDD, 0xED, 0xFD,
	0x8E, 0x9E, 0xAE, 0xBE, 0xCE, 0xDE, 0xEE, 0xFE,
	0x8F, 0x9F, 0xAF, 0xBF, 0xCF, 0xDF, 0xEF, 0xFF
]


def eco_out(cells: List[int]) -> bytes:
	# Messages sends to EcoBraille display are something like that:
	# 0x10 0x02 0xBC message 0x10 0x03
	ret = bytearray(b"\x10\x02\xBC")
	ret.extend(b"\00" * 5)
	# Leave status cells blank
	ret.extend(output_dots_map[c] for c in cells)
	ret.extend(b"\x10\x03")
	return bytes(ret)


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	""" EcoBraille display driver.
	"""
	name = "ecoBraille"
	# Translators: The name of a braille display.
	description = _("EcoBraille displays")

	@classmethod
	def check(cls):
		return True

	@classmethod
	def getPossiblePorts(cls):
		ports = OrderedDict()
		for p in hwPortUtils.listComPorts():
			# Translators: Name of a serial communications port.
			ports[p["port"]] = _("Serial: {portName}").format(portName=p["friendlyName"])
		return ports

	def __init__(self, port):
		super(BrailleDisplayDriver, self).__init__()
		self._port = port
		# Try to open port
		self._dev = serial.Serial(self._port, baudrate = 19200,  bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)
		# Use a longer timeout when waiting for initialisation.
		self._dev.timeout = self._dev.write_timeout = 2.7
		self._ecoType = eco_in_init(self._dev)
		# Use a shorter timeout hereafter.
		self._dev.timeout = self._dev.write_timeout = TIMEOUT
		# Always send the protocol answer.
		self._dev.write(b"\x61\x10\x02\xf1\x57\x57\x57\x10\x03")
		self._dev.write(b"\x10\x02\xbc\x00\x00\x00\x00\x00\x10\x03")
		# Start keyCheckTimer.
		self._readTimer = wx.PyTimer(self._handleResponses)
		self._readTimer.Start(READ_INTERVAL)

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		try:
			self._dev.write(b"\x61\x10\x02\xf1\x57\x57\x57\x10\x03")
			self._readTimer.Stop()
			self._readTimer = None
		finally:
			self._dev.close()
			self._dev = None

	def _get_numCells(self):
		return self._ecoType

	def display(self, cells: List[int]):
		try:
			self._dev.write(eco_out(cells))
		except:
			log.debug("error writing to the display", exc_info=True)

	def _handleResponses(self):
		if self._dev.in_waiting:
			command = eco_in(self._dev)
			if command:
				try:
					self._handleResponse(command)
				except KeyError:
					log.debug("error handling responses", exc_info=True)

	def _handleResponse(self, command: int):
		if command in (ECO_KEY_STATUS1, ECO_KEY_STATUS2, ECO_KEY_STATUS3, ECO_KEY_STATUS4):
			# Nothing to do with the status cells
			return 0
		if (command < ECO_END_ROUTING) and (command >= ECO_START_ROUTING):
			# Routing
			try:
				inputCore.manager.executeGesture(InputGestureRouting(((command - ECO_START_ROUTING) >> 24) + 1))
			except:
				log.debug("EcoBraille: No function associated with this routing key {key}".format(key=command))
		elif command > 0:
			# Button
			try:
				inputCore.manager.executeGesture(InputGestureKeys(command))
			except inputCore.NoInputGestureAction:
				log.debug("EcoBraille: No function associated with this Braille key {key}".format(key=command))
		return 0

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": "br(ecoBraille):routing",
			"braille_previousLine": "br(ecoBraille):T1",
			"braille_nextLine": "br(ecoBraille):T5",
			"braille_scrollBack": "br(ecoBraille):T2",
			"braille_scrollForward": "br(ecoBraille):T4",
			"review_activate": "br(ecoBraille):T3",
			"reviewMode_next": "br(ecoBraille):F1",
			"navigatorObject_parent": "br(ecoBraille):F2",
			"reviewMode_previous": "br(ecoBraille):F3",
			"navigatorObject_previous": "br(ecoBraille):F4",
			"navigatorObject_current": "br(ecoBraille):F5",
			"navigatorObject_next": "br(ecoBraille):F6",
			"navigatorObject_toFocus": "br(ecoBraille):F7",
			"navigatorObject_firstChild": "br(ecoBraille):F8",
			"navigatorObject_moveFocus": "br(ecoBraille):F9",
			"navigatorObject_currentDimensions": "br(ecoBraille):F0",
			"braille_toggleTether": "br(ecoBraille):A",
		}
	})


class InputGestureKeys(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, keys):
		super(InputGestureKeys, self).__init__()
		self.id = keyNames[keys]


class InputGestureRouting(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, index):
		super(InputGestureRouting, self).__init__()
		self.id = "routing"
		self.routingIndex = index-1
