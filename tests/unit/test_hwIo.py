# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, Leonard de Ruijter

"""Unit tests for the hwIo module."""

import unittest
import hwIo
import threading


class TestBgThreadApc(unittest.TestCase):
	"""Tests whether an APC on the hwIo background thread executes correctly."""

	def setUp(self):
		"""Set up an event to be used in subsequent tests."""
		hwIo.initialize()
		self.event = threading.Event()

	def tearDown(self):
		hwIo.terminate()

	def test_apc(self):
		"""Test queuing an APC that executes correctly.
		As the param provided to the internal APC differs from the param passed to the Python function,
		This test also ensures that the expected param is propagated correctly.
		"""
		# Initially, our event isn't set
		self.assertFalse(self.event.is_set())

		class Container:
			param: int

		paramContainer = Container()

		# Queue a function as APC that sets the event
		def apc(param: int) -> None:
			paramContainer.param = param
			self.event.set()

		hwIo.bgThread.queueAsApc(apc, 42)
		# Wait for atmost 2 seconds for the event to be set
		self.assertTrue(self.event.wait(2))
		self.assertEqual(paramContainer.param, 42)
