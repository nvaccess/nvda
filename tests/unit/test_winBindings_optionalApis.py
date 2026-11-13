# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Akash Kakkar
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
import importlib.util
import sys
import unittest
from ctypes.wintypes import BOOL, DWORD, HANDLE
from types import ModuleType
from unittest import mock

import winBindings
from winBindings import bthprops, magnification, winusb


def _loadModuleCopy(module: ModuleType, name: str) -> ModuleType:
	if module.__file__ is None:
		raise RuntimeError(f"No file for {module.__name__}")
	spec = importlib.util.spec_from_file_location(name, module.__file__)
	if spec is None or spec.loader is None:
		raise RuntimeError(f"Could not load {name}")
	copy = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(copy)
	return copy


def _loadUnavailable(module: ModuleType, libraryName: str, error: Exception) -> ModuleType:
	class UnavailableWindll:
		def __getitem__(self, name: str) -> None:
			if name != libraryName:
				raise AssertionError(f"Unexpected library: {name}")
			raise error

		def __getattr__(self, name: str) -> None:
			if name != libraryName:
				raise AssertionError(f"Unexpected library: {name}")
			raise error

	with mock.patch.object(ctypes, "windll", UnavailableWindll()):
		return _loadModuleCopy(module, f"winBindings._test_{module.__name__.rsplit('.', 1)[-1]}")


class TestOptionalApiBindings(unittest.TestCase):
	def test_availableBindingsRemainCtypesFunctions(self):
		for module, availableName, functionName in (
			(bthprops, "BLUETOOTH_AVAILABLE", "BluetoothGetDeviceInfo"),
			(magnification, "MAGNIFICATION_AVAILABLE", "MagInitialize"),
			(winusb, "WINUSB_AVAILABLE", "WinUsb_Initialize"),
		):
			with self.subTest(module=module.__name__):
				if getattr(module, availableName):
					self.assertIsInstance(getattr(module, functionName), ctypes._CFuncPtr)

	def test_missingLibrariesExposeNamedBindingsAndPreserveLoadError(self):
		for module, libraryName, availableName, errorName, functionName, message in (
			(
				bthprops,
				"bthprops.cpl",
				"BLUETOOTH_AVAILABLE",
				"BLUETOOTH_LOAD_ERROR",
				"BluetoothGetDeviceInfo",
				"Bluetooth API is not available",
			),
			(
				magnification,
				"Magnification",
				"MAGNIFICATION_AVAILABLE",
				"MAGNIFICATION_LOAD_ERROR",
				"MagInitialize",
				"Magnification API is not available",
			),
			(
				winusb,
				"winusb",
				"WINUSB_AVAILABLE",
				"WINUSB_LOAD_ERROR",
				"WinUsb_Initialize",
				"WinUSB is not available",
			),
		):
			for error in (OSError("missing library"), AttributeError("missing library")):
				with self.subTest(library=libraryName, error=type(error).__name__):
					unavailable = _loadUnavailable(module, libraryName, error)
					self.assertFalse(getattr(unavailable, availableName))
					self.assertIs(getattr(unavailable, errorName), error)
					binding = getattr(unavailable, functionName)
					self.assertEqual(binding.__name__, functionName)
					with self.assertRaisesRegex(OSError, message) as raised:
						binding(argument=True)
					self.assertIs(raised.exception.__cause__, error)

	def test_unavailableBindingsRetainIndependentMetadata(self):
		bluetooth = _loadUnavailable(bthprops, "bthprops.cpl", OSError("missing"))
		self.assertEqual(
			bluetooth.BluetoothGetDeviceInfo.argtypes, (HANDLE, bluetooth.BLUETOOTH_DEVICE_INFO_P)
		)
		self.assertIs(bluetooth.BluetoothGetDeviceInfo.restype, DWORD)

		magnifier = _loadUnavailable(magnification, "Magnification", OSError("missing"))
		self.assertIsNot(magnifier.MagInitialize, magnifier.MagShowSystemCursor)
		self.assertEqual(magnifier.MagShowSystemCursor.argtypes, (BOOL,))
		self.assertIs(magnifier.MagShowSystemCursor.restype, BOOL)
		self.assertIs(magnifier.MagInitialize.errcheck, magnifier._errCheck)

		usb = _loadUnavailable(winusb, "winusb", OSError("missing"))
		self.assertIsNot(usb.WinUsb_Initialize, usb.WinUsb_Free)
		self.assertEqual(usb.WinUsb_Initialize.argtypes, (HANDLE, usb.PWINUSB_INTERFACE_HANDLE))
		self.assertEqual(usb.WinUsb_Free.argtypes, (usb.WINUSB_INTERFACE_HANDLE,))
		self.assertIs(usb.WinUsb_Initialize.restype, BOOL)

	def test_magnifierCommandsImportWithoutMagnification(self):
		import _magnifier.commands as commandsModule
		import _magnifier.fullscreenMagnifier as fullscreenModule

		unavailable = _loadUnavailable(magnification, "Magnification", OSError("missing"))
		with (
			mock.patch.object(winBindings, "magnification", unavailable),
			mock.patch.dict(sys.modules, {"winBindings.magnification": unavailable}),
		):
			fullscreen = _loadModuleCopy(fullscreenModule, "_magnifier._test_fullscreenMagnifier")
			with mock.patch.dict(sys.modules, {"_magnifier.fullscreenMagnifier": fullscreen}):
				commands = _loadModuleCopy(commandsModule, "_magnifier._test_commands")
		self.assertIs(commands.FullScreenMagnifier, fullscreen.FullScreenMagnifier)
