# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ctypes
from ctypes import c_int, c_char_p, c_void_p
import os

from logHandler import log

# Load the native WinML library
try:
	_winMLLib = ctypes.cdll.LoadLibrary("nvdaHelperLocalWin10.dll")

	# Define function signatures
	_winMLLib.winML_initialize.argtypes = []
	_winMLLib.winML_initialize.restype = c_int

	_winMLLib.winML_createSession.argtypes = [c_char_p, c_int]
	_winMLLib.winML_createSession.restype = c_void_p

	_winMLLib.winML_destroySession.argtypes = [c_void_p]
	_winMLLib.winML_destroySession.restype = None

	_winMLLib.winML_getInputCount.argtypes = [c_void_p]
	_winMLLib.winML_getInputCount.restype = c_int

	_winMLLib.winML_getOutputCount.argtypes = [c_void_p]
	_winMLLib.winML_getOutputCount.restype = c_int

	_winMLLib.winML_terminate.argtypes = []
	_winMLLib.winML_terminate.restype = None

	_WINML_AVAILABLE = True
except Exception as e:
	log.error(f"Failed to load WinML native library: {e}")
	_WINML_AVAILABLE = False
	_winMLLib = None

_WINML_INSTANCE = None


class _WinML:
	"""Python wrapper for C++ WinML implementation."""

	def __new__(cls, *args, **kwargs):
		global _WINML_INSTANCE
		if _WINML_INSTANCE is None:
			_WINML_INSTANCE = super(_WinML, cls).__new__(cls, *args, **kwargs)
			_WINML_INSTANCE._initialized = False
		return _WINML_INSTANCE

	def __init__(self):
		if self._initialized:
			return

		if not _WINML_AVAILABLE:
			raise RuntimeError("WinML native library is not available")

		# Initialize WinML
		result = _winMLLib.winML_initialize()
		if result != 0:
			raise RuntimeError(f"Failed to initialize WinML (error code: {result})")

		self._initialized = True
		log.debug("WinML initialized successfully")

	def __del__(self):
		if self._initialized and _WINML_AVAILABLE:
			_winMLLib.winML_terminate()

	def createSession(self, modelPath: str, enableProfiling: bool = False) -> int:
		"""Create an ONNX Runtime session.

		Args:
			modelPath: Path to the ONNX model file.
			enableProfiling: Whether to enable profiling.

		Returns:
			Session handle (pointer), or 0 on failure.
		"""
		if not self._initialized:
			raise RuntimeError("WinML not initialized")

		modelPathBytes = modelPath.encode('utf-8')
		return _winMLLib.winML_createSession(modelPathBytes, 1 if enableProfiling else 0)

	def destroySession(self, session: int) -> None:
		"""Destroy an ONNX Runtime session.

		Args:
			session: Session handle to destroy.
		"""
		if session:
			_winMLLib.winML_destroySession(session)

	def getInputCount(self, session: int) -> int:
		"""Get the number of input tensors.

		Args:
			session: Session handle.

		Returns:
			Number of inputs.
		"""
		return _winMLLib.winML_getInputCount(session)

	def getOutputCount(self, session: int) -> int:
		"""Get the number of output tensors.

		Args:
			session: Session handle.

		Returns:
			Number of outputs.
		"""
		return _winMLLib.winML_getOutputCount(session)
