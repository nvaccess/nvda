# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
URL Handler Module for NVDARemote
This module provides functionality for launching NVDARemote connections via custom 'nvdaremote://' URLs.

Key Components:
- URL registration and unregistration utilities for Windows registry
- Parsing and handling of NVDARemote connection URLs

Main Functions:

-:func:`registerURLHandler`:
	Registers the NVDARemote URL protocol in the Windows Registry
:func:`unregisterURLHandler`:
	Removes the NVDARemote URL protocol registration
:func:`URLHandlerPath`:
	Returns the path to the URL handler executable
"""

import os
import sys
import winreg

from config.registry import RegistryKey, _deleteKeyAndSubkeys


def _createRegistryStructure(keyHandle: winreg.HKEYType, data: dict):
	"""Creates a nested registry structure from a dictionary.

	:param keyHandle: A handle to an open registry key
	:param data: Dictionary containing the registry structure to create
	:raises OSError: If creating registry keys or setting values fails
	"""
	for name, value in data.items():
		if isinstance(value, dict):
			# Create and recursively populate subkey
			try:
				subkey = winreg.CreateKey(keyHandle, name)
				try:
					_createRegistryStructure(subkey, value)
				finally:
					subkey.Close()
			except WindowsError as e:
				raise OSError(f"Failed to create registry subkey {name}: {e}")
		else:
			# Set value
			try:
				winreg.SetValueEx(keyHandle, name, 0, winreg.REG_SZ, str(value))
			except WindowsError as e:
				raise OSError(f"Failed to set registry value {name}: {e}")


def registerURLHandler():
	"""Registers the nvdaremote:// URL protocol handler in the Windows Registry.

	:raises OSError: If registration in the registry fails
	"""
	try:
		with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RegistryKey.REMOTE_URL_HANDLER.value) as key:
			_createRegistryStructure(key, URL_HANDLER_REGISTRY)
	except OSError as e:
		raise OSError(f"Failed to register URL handler: {e}")


def unregisterURLHandler():
	"""Unregisters the nvdaremote:// URL protocol handler from the Windows Registry.

	:raises OSError: If unregistration from the registry fails
	"""
	try:
		_deleteKeyAndSubkeys(
			winreg.HKEY_CURRENT_USER,
			RegistryKey.REMOTE_URL_HANDLER.value,
		)
	except WindowsError as e:
		raise OSError(f"Failed to unregister URL handler: {e}")


def URLHandlerPath():
	"""Returns the absolute path to the URL handler executable.

	:return: Full path to url_handler.exe
	:rtype: str
	"""
	return os.path.join(os.path.split(os.path.abspath(__file__))[0], "url_handler.exe")


# Registry structure definition
URL_HANDLER_REGISTRY = {
	"URL Protocol": "",
	"shell": {
		"open": {
			"command": {
				"": '"{path}" handleRemoteURL %1'.format(path=os.path.join(sys.prefix, "nvda_slave.exe")),
			},
		},
	},
}
