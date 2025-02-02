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
- register_url_handler(): Registers the NVDARemote URL protocol in the Windows Registry
- unregister_url_handler(): Removes the NVDARemote URL protocol registration
- url_handler_path(): Returns the path to the URL handler executable
"""

import os
import sys
import winreg

try:
	from logHandler import log
except ImportError:
	from logging import getLogger

	log = getLogger("url_handler")


def _createRegistryStructure(key_handle, data: dict):
	"""Creates a nested registry structure from a dictionary.

	:param key_handle: A handle to an open registry key
	:param data: Dictionary containing the registry structure to create
	:raises OSError: If creating registry keys or setting values fails
	"""
	for name, value in data.items():
		if isinstance(value, dict):
			# Create and recursively populate subkey
			try:
				subkey = winreg.CreateKey(key_handle, name)
				try:
					_createRegistryStructure(subkey, value)
				finally:
					winreg.CloseKey(subkey)
			except WindowsError as e:
				raise OSError(f"Failed to create registry subkey {name}: {e}")
		else:
			# Set value
			try:
				winreg.SetValueEx(key_handle, name, 0, winreg.REG_SZ, str(value))
			except WindowsError as e:
				raise OSError(f"Failed to set registry value {name}: {e}")


def _deleteRegistryKeyRecursive(base_key, subkey_path: str):
	"""Recursively deletes a registry key and all its subkeys.

	:param base_key: One of the HKEY_* constants from winreg
	:param subkey_path: Full registry path to the key to delete
	:raises OSError: If deletion fails for reasons other than key not found
	"""
	try:
		# Try to delete directly first
		winreg.DeleteKey(base_key, subkey_path)
	except WindowsError:
		# If that fails, need to do recursive deletion
		try:
			with winreg.OpenKey(base_key, subkey_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
				# Enumerate and delete all subkeys
				while True:
					try:
						subkey_name = winreg.EnumKey(key, 0)
						full_path = f"{subkey_path}\\{subkey_name}"
						_deleteRegistryKeyRecursive(base_key, full_path)
					except WindowsError:
						break
			# Now delete the key itself
			winreg.DeleteKey(base_key, subkey_path)
		except WindowsError as e:
			if e.winerror != 2:  # ERROR_FILE_NOT_FOUND
				raise OSError(f"Failed to delete registry key {subkey_path}: {e}")


def registerURLHandler():
	"""Registers the nvdaremote:// URL protocol handler in the Windows Registry.

	:raises OSError: If registration in the registry fails
	"""
	try:
		keyPath = r"SOFTWARE\Classes\nvdaremote"
		with winreg.CreateKey(winreg.HKEY_CURRENT_USER, keyPath) as key:
			_createRegistryStructure(key, URL_HANDLER_REGISTRY)
	except OSError as e:
		raise OSError(f"Failed to register URL handler: {e}")


def unregisterURLHandler():
	"""Unregisters the nvdaremote:// URL protocol handler from the Windows Registry.

	:raises OSError: If unregistration from the registry fails
	"""
	try:
		_deleteRegistryKeyRecursive(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\nvdaremote")
	except OSError as e:
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
