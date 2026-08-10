# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Selvas Healthcare
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by winusb.dll, and supporting data structures and enumerations."""

from ctypes import (
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

dll = windll.winusb

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


WinUsb_Initialize = WINFUNCTYPE(None)(("WinUsb_Initialize", dll))
"""
Creates a WinUSB handle for the device specified by a file handle.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_initialize
"""
WinUsb_Initialize.argtypes = (
	HANDLE,  # DeviceHandle
	PWINUSB_INTERFACE_HANDLE,  # InterfaceHandle
)
WinUsb_Initialize.restype = BOOL

WinUsb_Free = WINFUNCTYPE(None)(("WinUsb_Free", dll))
"""
Frees the resources allocated by ``WinUsb_Initialize``.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_free
"""
WinUsb_Free.argtypes = (
	WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
)
WinUsb_Free.restype = BOOL

WinUsb_QueryInterfaceSettings = WINFUNCTYPE(None)(("WinUsb_QueryInterfaceSettings", dll))
"""
Retrieves the interface descriptor for the specified alternate interface settings for a particular interface handle.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_queryinterfacesettings
"""
WinUsb_QueryInterfaceSettings.argtypes = (
	WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
	c_ubyte,  # AlternateInterfaceNumber
	POINTER(USB_INTERFACE_DESCRIPTOR),  # UsbAltInterfaceDescriptor
)
WinUsb_QueryInterfaceSettings.restype = BOOL

WinUsb_QueryPipe = WINFUNCTYPE(None)(("WinUsb_QueryPipe", dll))
"""
Retrieves information about a pipe that is associated with an interface.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_querypipe
"""
WinUsb_QueryPipe.argtypes = (
	WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
	c_ubyte,  # AlternateInterfaceNumber
	c_ubyte,  # PipeIndex
	POINTER(WINUSB_PIPE_INFORMATION),  # PipeInformation
)
WinUsb_QueryPipe.restype = BOOL

WinUsb_ReadPipe = WINFUNCTYPE(None)(("WinUsb_ReadPipe", dll))
"""
Reads data from the specified pipe.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_readpipe
"""
WinUsb_ReadPipe.argtypes = (
	WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
	c_ubyte,  # PipeID
	c_void_p,  # Buffer
	ULONG,  # BufferLength
	PULONG,  # LengthTransferred
	LPOVERLAPPED,  # Overlapped
)
WinUsb_ReadPipe.restype = BOOL

WinUsb_WritePipe = WINFUNCTYPE(None)(("WinUsb_WritePipe", dll))
"""
Writes data to a pipe.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_writepipe
"""
WinUsb_WritePipe.argtypes = (
	WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
	c_ubyte,  # PipeID
	c_void_p,  # Buffer
	ULONG,  # BufferLength
	PULONG,  # LengthTransferred
	LPOVERLAPPED,  # Overlapped
)
WinUsb_WritePipe.restype = BOOL

WinUsb_SetPipePolicy = WINFUNCTYPE(None)(("WinUsb_SetPipePolicy", dll))
"""
Sets the policy for a specific pipe associated with an endpoint on the device.

..seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/winusb/nf-winusb-winusb_setpipepolicy
"""
WinUsb_SetPipePolicy.argtypes = (
	WINUSB_INTERFACE_HANDLE,  # InterfaceHandle
	c_ubyte,  # PipeID
	ULONG,  # PolicyType
	ULONG,  # ValueLength
	c_void_p,  # Value
)
WinUsb_SetPipePolicy.restype = BOOL
