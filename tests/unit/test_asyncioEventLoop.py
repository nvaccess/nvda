# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Bram Duvigneau, Dot Incorporated
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Unit tests for asyncioEventLoop module."""

import asyncio
import unittest

import asyncioEventLoop


class TestRunCoroutineSync(unittest.TestCase):
	"""Tests for runCoroutineSync function."""

	@classmethod
	def setUpClass(cls):
		"""Initialize the asyncio event loop before tests."""
		asyncioEventLoop.initialize()

	@classmethod
	def tearDownClass(cls):
		"""Terminate the asyncio event loop after tests."""
		asyncioEventLoop.terminate()

	def test_returnsResult(self):
		"""Test that runCoroutineSync returns the coroutine's result."""

		async def simpleCoroutine():
			return 42

		result = asyncioEventLoop.runCoroutineSync(simpleCoroutine())
		self.assertEqual(result, 42)

	def test_returnsComplexResult(self):
		"""Test that runCoroutineSync returns complex objects."""

		async def complexCoroutine():
			await asyncio.sleep(0.01)
			return {"key": "value", "number": 123}

		result = asyncioEventLoop.runCoroutineSync(complexCoroutine())
		self.assertEqual(result, {"key": "value", "number": 123})

	def test_raisesException(self):
		"""Test that runCoroutineSync raises exceptions from the coroutine."""

		async def failingCoroutine():
			await asyncio.sleep(0.01)
			raise ValueError("Test error message")

		with self.assertRaises(ValueError) as cm:
			asyncioEventLoop.runCoroutineSync(failingCoroutine())
		self.assertEqual(str(cm.exception), "Test error message")

	def test_timeoutRaisesTimeoutError(self):
		"""Test that runCoroutineSync raises TimeoutError when timeout is exceeded."""

		async def slowCoroutine():
			await asyncio.sleep(10)
			return "Should not reach here"

		with self.assertRaises(TimeoutError) as cm:
			asyncioEventLoop.runCoroutineSync(slowCoroutine(), timeout=0.1)
		self.assertIn("timed out", str(cm.exception).lower())

	def test_noTimeoutWaitsIndefinitely(self):
		"""Test that runCoroutineSync waits indefinitely when no timeout is specified."""

		async def delayedCoroutine():
			await asyncio.sleep(0.1)
			return "completed"

		# This should complete successfully even though it takes some time
		result = asyncioEventLoop.runCoroutineSync(delayedCoroutine())
		self.assertEqual(result, "completed")

	def test_raisesRuntimeErrorWhenEventLoopNotRunning(self):
		"""Test that runCoroutineSync raises RuntimeError when event loop is not running."""
		# Save original thread reference
		originalThread = asyncioEventLoop.asyncioThread

		# Temporarily set to None to simulate not running
		asyncioEventLoop.asyncioThread = None

		async def anyCoroutine():
			return "test"

		with self.assertRaises(RuntimeError) as cm:
			asyncioEventLoop.runCoroutineSync(anyCoroutine())
		self.assertIn("not running", str(cm.exception).lower())

		# Restore original thread
		asyncioEventLoop.asyncioThread = originalThread
