# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest import mock

import NVDAHelper


class TestTryStartRemoteLoader(unittest.TestCase):
	def test_loaderFailureIsLoggedAndIgnored(self):
		with (
			mock.patch.object(NVDAHelper, "_RemoteLoader", side_effect=OSError),
			mock.patch.object(NVDAHelper.log, "exception") as logException,
		):
			loader = NVDAHelper._tryStartRemoteLoader("loaderPath")

		self.assertIsNone(loader)
		logException.assert_called_once_with("Unable to start remote loader from %s", "loaderPath")


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

	def test_handlesAreClosedWhenLaterSetupStepsFail(self):
		for failedStep, expectedClosed in (
			("nul", [10, 11, 12]),
			("token", [10, 11, 12, 13]),
			("process", [10, 11, 12, 13, 15]),
		):
			with (
				self.subTest(failedStep=failedStep),
				mock.patch.object(NVDAHelper.winKernel, "CreatePipe", return_value=(10, 11)),
				mock.patch.object(
					NVDAHelper._RemoteLoader,
					"_duplicateAsInheritable",
					side_effect=(12, OSError()) if failedStep == "nul" else (12, 13),
				),
				mock.patch.object(NVDAHelper.msvcrt, "get_osfhandle", return_value=14),
				mock.patch.object(
					NVDAHelper.winKernel,
					"OpenProcessToken",
					side_effect=OSError() if failedStep == "token" else None,
					return_value=15,
				),
				mock.patch.object(
					NVDAHelper.winKernel,
					"CreateProcessAsUser",
					side_effect=OSError() if failedStep == "process" else None,
				),
				mock.patch.object(NVDAHelper.winKernel, "closeHandle") as closeHandle,
				mock.patch("builtins.open", mock.mock_open()),
				self.assertRaises(OSError),
			):
				NVDAHelper._RemoteLoader("loaderPath")

			self.assertEqual([mock.call(handle) for handle in expectedClosed], closeHandle.call_args_list)

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
