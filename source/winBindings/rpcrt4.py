# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by rpcrt4.dll, and supporting data structures and enumerations."""

from ctypes import (
	c_long,
	c_ulong,
	c_void_p,
	POINTER,
	windll,
)


dll = windll.rpcrt4

RPC_STATUS = c_ulong
RPC_BINDING_HANDLE = c_void_p


I_RpcBindingInqLocalClientPID = dll.I_RpcBindingInqLocalClientPID
"""
Obtains the process identifier (PID) of the local client process that made the remote procedure call.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/rpcdcep/nf-rpcdcep-i_rpcbindinginqlocalclientpid
"""
I_RpcBindingInqLocalClientPID.restype = RPC_STATUS
I_RpcBindingInqLocalClientPID.argtypes = (
	RPC_BINDING_HANDLE,  # Binding: RPC binding handle (can be None)
	POINTER(c_long),  # ClientPID: Pointer to receive the client process ID
)

RpcBindingFree = dll.RpcBindingFree
"""
Releases binding handle resources.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindingfree
"""
RpcBindingFree.restype = RPC_STATUS
RpcBindingFree.argtypes = (
	POINTER(RPC_BINDING_HANDLE),  # Binding: Pointer to the binding handle to free
)

RpcSsDestroyClientContext = dll.RpcSsDestroyClientContext
"""
Destroys a client context handle and releases associated resources.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/rpcndr/nf-rpcndr-rpcssdestroyclientcontext
"""
RpcSsDestroyClientContext.restype = None  # void
RpcSsDestroyClientContext.argtypes = (
	POINTER(c_void_p),  # ContextHandle: Pointer to the context handle to destroy
)
