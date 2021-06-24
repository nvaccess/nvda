# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2020 NV Access Limited, Leonard de Ruijter

"""Unit tests for braille display drivers.
"""

from brailleDisplayDrivers.seikantk import BrailleDisplayDriver as SeikaNotetakerDriver, SEIKA_INFO

import unittest
import braille


class TestSeikaNotetakerDriver(unittest.TestCase):
	def test_onReceive(self):
		""" Tests how the Seika Notetaker driver handles receiving data via `_onReceive`.
		Simulates sending a sample message from the device, which should result in our driver processing a
		command via `_processCommand`. Without knowing the specifications of the device, this simulation may
		be inaccurate or uncomprehensive.
		"""
		sampleCommand = SEIKA_INFO
		sampleArgument = b"test"
		sampleArgLen = bytes([len(sampleArgument)])
		sampleMessage = sampleCommand + sampleArgLen + sampleArgument + b"\0\0\0"

		class FakeSeikaNotetakerDriver(SeikaNotetakerDriver):
			def __init__(self):
				"""Sets the variables necessary to test _onReceive without a braille device connected.
				"""
				self._hidBuffer = b""
				self._command = None
				self._argsLen = None

			def _processCommand(self, command, arg):
				"""Intercept processCommand to confirm _onReceive processes a message correctly.
				"""
				self._finalCommand = command
				self._finalArg = arg
		
		seikaTestDriver = FakeSeikaNotetakerDriver()
		for byteToSend in sampleMessage:
			# the middle byte is the only one used, padded by a byte on either side.
			seikaTestDriver._onReceive(b"\0" + bytes([byteToSend]) + b"\0")

		self.assertEqual(sampleCommand, seikaTestDriver._finalCommand)
		self.assertEqual(sampleArgLen + sampleArgument, seikaTestDriver._finalArg)


class TestGestureMap(unittest.TestCase):
	"""Tests the integrity of braille display driver gesture maps."""

	def test_identifiers(self):
		"""Checks whether all defined braille display gestures contain valid braille display key identifiers."""
		for name, description in braille.getDisplayList(excludeNegativeChecks=False):
			driver=braille._getDisplayDriver(name)
			gmap=driver.gestureMap
			if not gmap:
				continue
			for cls, gesture, scriptName in gmap.getScriptsForAllGestures():
				if gesture.startswith("br"):
					self.assertRegexpMatches(gesture, braille.BrailleDisplayGesture.ID_PARTS_REGEX)


class TestBRLTTY(unittest.TestCase):
	"""Tests the integrity of the bundled brlapi module."""

	def test_brlapi(self):
		try:
			# SUpress Flake8 F401 imported but unused, as we're testing the import
			import brlapi  # noqa: F401
		except Exception:
			self.fail("Couldn't import the brlapi module")
