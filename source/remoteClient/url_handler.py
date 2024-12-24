"""
URL Handler Module for NVDARemote
This module provides functionality for launching NVDARemote connections via custom 'nvdaremote://' URLs.

Key Components:
- URLHandlerWindow: A custom window class that intercepts and processes NVDARemote URLs
- URL registration and unregistration utilities for Windows registry
- Parsing and handling of NVDARemote connection URLs

Main Functions:
- register_url_handler(): Registers the NVDARemote URL protocol in the Windows Registry
- unregister_url_handler(): Removes the NVDARemote URL protocol registration
- url_handler_path(): Returns the path to the URL handler executable
"""

import os
import winreg

try:
	from logHandler import log
except ImportError:
	from logging import getLogger

	log = getLogger("url_handler")

import ctypes
import ctypes.wintypes

import gui  # provided by NVDA
import windowUtils
import wx
from winUser import WM_COPYDATA  # provided by NVDA

from . import connection_info


class COPYDATASTRUCT(ctypes.Structure):
	"""Windows COPYDATASTRUCT for inter-process communication.

	This structure is used by Windows to pass data between processes using
	the WM_COPYDATA message. It contains fields for:
	- Custom data value (dwData)
	- Size of data being passed (cbData)
	- Pointer to the actual data (lpData)
	"""

	_fields_ = [
		("dwData", ctypes.wintypes.LPARAM),
		("cbData", ctypes.wintypes.DWORD),
		("lpData", ctypes.c_void_p),
	]


PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)

MSGFLT_ALLOW = 1


class URLHandlerWindow(windowUtils.CustomWindow):
	"""Window class that receives and processes nvdaremote:// URLs.

	This window registers itself to receive WM_COPYDATA messages containing
	URLs. When a URL is received, it:
	1. Parses the URL into connection parameters
	2. Validates the URL format
	3. Calls the provided callback with the connection info

	The window automatically handles UAC elevation by allowing messages
	from lower privilege processes.
	"""

	className = "NVDARemoteURLHandler"

	def __init__(self, callback=None, *args, **kwargs):
		"""Initialize URL handler window.

		Args:
			callback (callable, optional): Function to call with parsed ConnectionInfo
				when a valid URL is received. Defaults to None.
			*args: Additional arguments passed to CustomWindow
			**kwargs: Additional keyword arguments passed to CustomWindow
		"""
		super().__init__(*args, **kwargs)
		self.callback = callback
		try:
			ctypes.windll.user32.ChangeWindowMessageFilterEx(
				self.handle,
				WM_COPYDATA,
				MSGFLT_ALLOW,
				None,
			)
		except AttributeError:
			pass

	def windowProc(self, hwnd, msg, wParam, lParam):
		"""Windows message procedure for handling received URLs.

		Processes WM_COPYDATA messages containing nvdaremote:// URLs.
		Parses the URL and calls the callback if one was provided.

		Args:
			hwnd: Window handle
			msg: Message type
			wParam: Source window handle
			lParam: Pointer to COPYDATASTRUCT containing the URL

		Raises:
			URLParsingError: If the received URL is malformed or invalid
		"""
		if msg != WM_COPYDATA:
			return
		struct_pointer = lParam
		message_data = ctypes.cast(struct_pointer, PCOPYDATASTRUCT)
		url = ctypes.wstring_at(message_data.contents.lpData)
		log.info("Received url: %s" % url)
		try:
			con_info = connection_info.ConnectionInfo.fromURL(url)
		except connection_info.URLParsingError:
			wx.CallLater(
				50,
				gui.messageBox,
				parent=gui.mainFrame,
				# Translators: Title of a message box shown when an invalid URL has been provided.
				caption=_("Invalid URL"),
				# Translators: Message shown when an invalid URL has been provided.
				message=_('Unable to parse url "%s"') % url,
				style=wx.OK | wx.ICON_ERROR,
			)
			log.exception("unable to parse nvdaremote:// url %s" % url)
			raise
		log.info("Connection info: %r" % con_info)
		if callable(self.callback):
			wx.CallLater(50, self.callback, con_info)


def _create_registry_structure(key_handle, data):
	"""Creates a nested registry structure from a dictionary.

	Args:
	    key_handle: A handle to an open registry key
	    data: Dictionary containing the registry structure to create
	"""
	for name, value in data.items():
		if isinstance(value, dict):
			# Create and recursively populate subkey
			try:
				subkey = winreg.CreateKey(key_handle, name)
				try:
					_create_registry_structure(subkey, value)
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


def _delete_registry_key_recursive(base_key, subkey_path):
	"""Recursively deletes a registry key and all its subkeys.

	Args:
	    base_key: One of the HKEY_* constants
	    subkey_path: Path to the key to delete
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
						_delete_registry_key_recursive(base_key, full_path)
					except WindowsError:
						break
			# Now delete the key itself
			winreg.DeleteKey(base_key, subkey_path)
		except WindowsError as e:
			if e.winerror != 2:  # ERROR_FILE_NOT_FOUND
				raise OSError(f"Failed to delete registry key {subkey_path}: {e}")


def register_url_handler():
	"""Registers the URL handler in the Windows Registry."""
	try:
		key_path = r"SOFTWARE\Classes\nvdaremote"
		with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
			_create_registry_structure(key, URL_HANDLER_REGISTRY)
	except OSError as e:
		raise OSError(f"Failed to register URL handler: {e}")


def unregister_url_handler():
	"""Unregisters the URL handler from the Windows Registry."""
	try:
		_delete_registry_key_recursive(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\nvdaremote")
	except OSError as e:
		raise OSError(f"Failed to unregister URL handler: {e}")


def url_handler_path():
	"""Returns the path to the URL handler executable."""
	return os.path.join(os.path.split(os.path.abspath(__file__))[0], "url_handler.exe")


# Registry structure definition
URL_HANDLER_REGISTRY = {
	"URL Protocol": "",
	"shell": {
		"open": {
			"command": {
				"": '"{path}" %1'.format(path=url_handler_path()),
			},
		},
	},
}
