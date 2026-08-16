# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from unittest import mock

import NVDAHelper


class TestTryStartRemoteLoader(unittest.TestCase):
	def test_loaderFailureIsLoggedAndIgnored(self):
		with (
			mock.patch.object(NVDAHelper, "_RemoteLoader", side_effect=OSError),
			mock.patch.object(NVDAHelper.log, "error") as logError,
		):
			loader = NVDAHelper._tryStartRemoteLoader("loaderPath")

		self.assertIsNone(loader)
		logError.assert_called_once_with(
			"Unable to start remote loader from loaderPath",
			exc_info=True,
		)


class TestRemoteLoaderHandles(unittest.TestCase):
	def test_handlesAreClosedWhenSetupFails(self):
		with (
			mock.patch.object(NVDAHelper.winKernel, "CreatePipe", return_value=(10, 11)),
			mock.patch.object(
				NVDAHelper._RemoteLoader,
				"_duplicateAsInheritable",
				side_effect=OSError,
			),
			mock.patch.object(NVDAHelper.winKernel, "closeHandle") as closeHandle,
			self.assertRaises(OSError),
		):
			NVDAHelper._RemoteLoader("loaderPath")

		self.assertEqual([mock.call(11), mock.call(10)], closeHandle.call_args_list)

	def test_parentHandlesAreClosedAfterStartup(self):
		def createProcess(*args):
			processInformation = args[-1]
			processInformation.hProcess = 16
			processInformation.hThread = 17

		with (
			mock.patch.object(NVDAHelper.winKernel, "CreatePipe", return_value=(10, 11)),
			mock.patch.object(
				NVDAHelper._RemoteLoader,
				"_duplicateAsInheritable",
				side_effect=(12, 13),
			),
			mock.patch.object(NVDAHelper.msvcrt, "get_osfhandle", return_value=14),
			mock.patch.object(NVDAHelper.winKernel, "OpenProcessToken", return_value=15),
			mock.patch.object(NVDAHelper.winKernel, "CreateProcessAsUser", side_effect=createProcess),
			mock.patch.object(NVDAHelper.winKernel, "closeHandle") as closeHandle,
			mock.patch("builtins.open", mock.mock_open()),
		):
			loader = NVDAHelper._RemoteLoader("loaderPath")

		self.assertEqual(11, loader._pipeWrite)
		self.assertEqual(16, loader._process)
		self.assertEqual(
			[mock.call(10), mock.call(12), mock.call(13), mock.call(15), mock.call(17)],
			closeHandle.call_args_list,
		)
