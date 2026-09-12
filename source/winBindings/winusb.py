# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Selvas Healthcare
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by winusb.dll, and supporting data structures and enumerations.

When WinUSB is unavailable, function bindings raise :class:`OSError`.
"""

from ctypes import (  # noqa: I001
	WINFUNCTYPE,
	POINTER,
	Structure,
	c_int,
	c_ubyte,
	c_void_p,
	windll,
)
from ctypes.wintypes import BOOL, HANDLE, PULONG, ULONG, USHORT
from enum import IntEnum
from serial.win32 import LPOVERLAPPED
from typing import Any

try:
	dll = windll.winusb
except (AttributeError, OSError) as e:
	dll = None
	WINUSB_LOAD_ERROR: Exception | None = e
else:
	WINUSB_LOAD_ERROR = None

WINUSB_AVAILABLE: bool = dll is not None
"""True if WinUSB is available."""

WINUSB_INTERFACE_HANDLE = c_void_p
PWINUSB_INTERFACE_HANDLE = POINTER(c_void_p)


class USBD_PIPE_TYPE(IntEnum):
	"""Indicates the type of pipe, used in the ``PipeType`` member of ``WINUSB_PIPE_INFORMATION``.

	..seealso::
		https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/usb/ne-usb-_usbd_pipe_type
	"""

	CONTROL = 0
	ISOCHRONOUS = 1
	BULK = 2
	INTERRUPT = 3


class WINUSB_PIPE_POLICY(IntEnum):
	"""Policy type values for the ``PolicyType`` parameter of ``WinUsb_SetPipePolicy``.

	..seealso::
		https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/winusb-functions-for-pipe-policy-modification
	"""

	PIPE_TRANSFER_TIMEOUT = 0x03
	"""Waits for a time-out interval, in milliseconds, before canceling the request."""


class USB_INTERFACE_DESCRIPTOR(Structure):
	"""Describes a USB interface.

	..seealso::
		https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/usbspec/ns-usbspec-_usb_interface_descriptor
	"""

	_fields_ = (
		("bLength", c_ubyte),
		("bDescriptorType", c_ubyte),
		("bInterfaceNumber", c_ubyte),
		("bAlternateSetting", c_ubyte),
		("bNumEndpoints", c_ubyte),
		("bInterfaceClass", c_ubyte),
		("bInterfaceSubClass", c_ubyte),
		("bInterfaceProtocol", c_ubyte),
		("iInterface", c_ubyte),
	)


class WINUSB_PIPE_INFORMATION(Structure):
	"""Contains pipe information retrieved by `WinUsb_QueryPipe`.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/winusbio/ns-winusbio-winusb_pipe_information
	"""

	_fields_ = (
		("pipeType", c_int),  # USBD_PIPE_TYPE
		("pipeId", c_ubyte),
		("maximumPacketSize", USHORT),
		("interval", c_ubyte),
	)


def _unavailable(*args: Any, **kwargs: Any) -> None:
	raise OSError("WinUSB is not available")


def _bind(name: str, argtypes: tuple[Any, ...], restype: Any) -> Any:
	if dll is None:
		return _unavailable
	function = WINFUNCTYPE(None)((name, dll))
	function.argtypes = argtypes
	function.restype = restype
	return function


WinUsb_Initialize = _bind(
	"WinUsb_Initialize",
	(
		HANDLE,  # DeviceHandle
		PWINUSB_INTERFACE_HANDLE,  # InterfaceHandle
	),
	BOOL,
)
"""
Creates a WinUSB handle for the device specified by a file handle.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_initialize
"""

WinUsb_Free = _bind(
	"WinUsb_Free",
	(
		WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
	),
	BOOL,
)
"""
Frees the resources allocated by ``WinUsb_Initialize``.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_free
"""

WinUsb_QueryInterfaceSettings = _bind(
	"WinUsb_QueryInterfaceSettings",
	(
		WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
		c_ubyte,  # AlternateInterfaceNumber
		POINTER(USB_INTERFACE_DESCRIPTOR),  # UsbAltInterfaceDescriptor
	),
	BOOL,
)
"""
Retrieves the interface descriptor for the specified alternate interface settings for a particular interface handle.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_queryinterfacesettings
"""

WinUsb_QueryPipe = _bind(
	"WinUsb_QueryPipe",
	(
		WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
		c_ubyte,  # AlternateInterfaceNumber
		c_ubyte,  # PipeIndex
		POINTER(WINUSB_PIPE_INFORMATION),  # PipeInformation
	),
	BOOL,
)
"""
Retrieves information about a pipe that is associated with an interface.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_querypipe
"""

WinUsb_ReadPipe = _bind(
	"WinUsb_ReadPipe",
	(
		WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
		c_ubyte,  # PipeID
		c_void_p,  # Buffer
		ULONG,  # BufferLength
		PULONG,  # LengthTransferred
		LPOVERLAPPED,  # Overlapped
	),
	BOOL,
)
"""
Reads data from the specified pipe.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_readpipe
"""

WinUsb_WritePipe = _bind(
	"WinUsb_WritePipe",
	(
		WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
		c_ubyte,  # PipeID
		c_void_p,  # Buffer
		ULONG,  # BufferLength
		PULONG,  # LengthTransferred
		LPOVERLAPPED,  # Overlapped
	),
	BOOL,
)
"""
Writes data to a pipe.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_writepipe
"""

WinUsb_SetPipePolicy = _bind(
	"WinUsb_SetPipePolicy",
	(
		WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
		c_ubyte,  # PipeID
		ULONG,  # PolicyType
		ULONG,  # ValueLength
		c_void_p,  # Value
	),
	BOOL,
)
"""
Sets the policy for a specific pipe associated with an endpoint on the device.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_setpipepolicy
"""
