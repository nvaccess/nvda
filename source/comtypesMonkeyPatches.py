# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2019 NV Access Limited, Babbage B.V.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Warning: no comtypes modules can be imported until ctypes.WINFUNCTYPE has been replaced further down.

import ctypes
import _ctypes
import importlib


# A version of ctypes.WINFUNCTYPE 
# that produces a WinFunctionType class whose instance will convert COMError into a CallCancelled exception when called as a function.
old_WINFUNCTYPE=ctypes.WINFUNCTYPE
def new_WINFUNCTYPE(restype,*argtypes,**kwargs):
	cls=old_WINFUNCTYPE(restype,*argtypes,**kwargs)
	class WinFunctionType(cls):
		# We must manually pull the mandatory class variables from the super class,
		# as the metaclass of _ctypes.CFuncPtr seems to expect these on the outermost subclass.
		_argtypes_=cls._argtypes_
		_restype_=cls._restype_
		_flags_=cls._flags_
		def __call__(self,*args,**kwargs):
			try:
				return super().__call__(*args,**kwargs)
			except _ctypes.COMError as e:
				from core import CallCancelled, RPC_E_CALL_CANCELED
				if e.args[0]==RPC_E_CALL_CANCELED:
					# As this is a cancelled COM call,
					# raise CallCancelled instead of the original COMError.
					# Also raising from None gives a cleaner traceback,
					# Hiding the fact we were already in an except block.
					raise CallCancelled("COM call cancelled") from None
				# Otherwise, just continue the original COMError exception up the stack.
				raise
	return WinFunctionType

# While importing comtypes,
# Replace WINFUNCTYPE in ctypes with our own version,
# So that comtypes will use this in all its COM method calls. 
# As comtypes imports WINFUNCTYPE from ctypes by name,
# We only need to replace it for the duration of importing comtypes, 
# as it will then have it for ever.
ctypes.WINFUNCTYPE=new_WINFUNCTYPE
try:
	import comtypes
finally:
	ctypes.WINFUNCTYPE=old_WINFUNCTYPE

# It is safe to import any comtypes modules from here on down.

from logHandler import log

from comtypes import COMError
from comtypes.hresult import *

#Monkey patch comtypes to support byref in variants
from comtypes.automation import VARIANT, VT_BYREF, IDispatch
from ctypes import cast, c_void_p
from _ctypes import _Pointer
oldVARIANT_value_fset=VARIANT.value.fset
def newVARIANT_value_fset(self,value):
	realValue=value
	if isinstance(value,_Pointer):
		try:
			value=value.contents
		except (NameError,AttributeError):
			pass
	oldVARIANT_value_fset(self,value)
	if realValue is not value:
		self.vt|=VT_BYREF
		self._.c_void_p=cast(realValue,c_void_p)
VARIANT.value=property(VARIANT.value.fget,newVARIANT_value_fset,VARIANT.value.fdel)

#Monkeypatch comtypes lazybind dynamic IDispatch support to fallback to the more basic dynamic IDispatch support if the former does not work
#Example: ITypeComp.bind gives back a vardesc, which comtypes does not yet support
import comtypes.client.lazybind
old__getattr__=comtypes.client.lazybind.Dispatch.__getattr__
def new__getattr__(self,name):
	try:
		return old__getattr__(self,name)
	except (NameError, AttributeError):
		return getattr(comtypes.client.dynamic._Dispatch(self._comobj),name)
comtypes.client.lazybind.Dispatch.__getattr__=new__getattr__

#Monkeypatch comtypes to allow its basic dynamic Dispatch support to  support invoke 0 (calling the actual IDispatch object itself)
def new__call__(self,*args,**kwargs):
	return comtypes.client.dynamic.MethodCaller(0,self)(*args,**kwargs)
comtypes.client.dynamic._Dispatch.__call__=new__call__

# Work around an issue with comtypes where __del__ seems to be called twice on COM pointers.
# This causes Release() to be called more than it should, which is very nasty and will eventually cause us to access pointers which have been freed.
from comtypes import _compointer_base
_cpbDel = _compointer_base.__del__
def newCpbDel(self):
	if hasattr(self, "_deleted"):
		# Don't allow this to be called more than once.
		log.debugWarning("COM pointer %r already deleted" % self)
		return
	_cpbDel(self)
	self._deleted = True
newCpbDel.__name__ = "__del__"
_compointer_base.__del__ = newCpbDel
del _compointer_base

#Monkey patch to force dynamic Dispatch on all vt_dispatch variant values.
#Certainly needed for comtypes COM servers, but currently very fiddly to do just for that case 
oldVARIANT_value_fget=VARIANT.value.fget
def newVARIANT_value_fget(self):
	return self._get_value(dynamic=True)
VARIANT.value=property(newVARIANT_value_fget,VARIANT.value.fset,VARIANT.value.fdel)

# #4258: monkeypatch to better handle error where IDispatch's GetTypeInfo can return a NULL pointer. Affects QT5
oldGetTypeInfo=IDispatch._GetTypeInfo
def newGetTypeInfo(self,index,lcid=0):
	res=oldGetTypeInfo(self,index,lcid)
	if not res:
		raise COMError(E_NOTIMPL,None,None)
	return res
IDispatch._GetTypeInfo=newGetTypeInfo

# Windows updates often include newer versions of dlls/typelibs we use.
# The typelib being newer than the comtypes generated module doesn't hurt us,
# so kill the "Typelib newer than module" ImportError.
# comtypes doesn't let us disable this when running from source, so we need to monkey patch.
# This is just the code from the original comtypes._check_version excluding the time check.
import comtypes
def _check_version(actual):
	from comtypes.tools.codegenerator import version as required
	if actual != required:
		raise ImportError("Wrong version")
comtypes._check_version = _check_version


# Monkeypatch comtypes to clear the importlib cache when importing a new module

# We must import comtypes.client._generate here as it must be done after other monkeypatching
import comtypes.client._generate  # noqa: E402

old_my_import = comtypes.client._generate._my_import


def new_my_import(fullname):
	importlib.invalidate_caches()
	return old_my_import(fullname)


comtypes.client._generate._my_import = new_my_import
