# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2009-2019 NV Access Limited, Babbage B.V.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Warning: no comtypes modules can be imported at the module level
# since we need to replace ctypes.WINFUNCTYPE with our custom version.

import ctypes
import _ctypes
from ctypes import cast, c_void_p
from _ctypes import _Pointer
import importlib
import sys
import exceptions
import RPCConstants


def new_WINFUNCTYPE(restype,*argtypes,**kwargs):
	"""A version of ctypes.WINFUNCTYPE
	that produces a WinFunctionType class
	whose instance will convert COMError into a CallCancelled exception when called as a function."""
	cls = ctypes.WINFUNCTYPE_orig(restype, *argtypes, **kwargs)
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
				if e.args[0] == RPCConstants.RPC.E_CALL_CANCELED:
					# As this is a cancelled COM call,
					# raise CallCancelled instead of the original COMError.
					# Also raising from None gives a cleaner traceback,
					# Hiding the fact we were already in an except block.
					raise exceptions.CallCancelled("COM call cancelled") from None
				# Otherwise, just continue the original COMError exception up the stack.
				raise
	return WinFunctionType


def replace_WINFUNCTYPE() -> None:
	# While importing comtypes,
	# Replace WINFUNCTYPE in ctypes with our own version,
	# So that comtypes will use this in all its COM method calls.
	# As comtypes imports WINFUNCTYPE from ctypes by name,
	# We only need to replace it for the duration of importing comtypes,
	# as it will then have it for ever.
	ctypes.WINFUNCTYPE_orig = ctypes.WINFUNCTYPE
	ctypes.WINFUNCTYPE = new_WINFUNCTYPE
	try:
		import comtypes
		if comtypes.WINFUNCTYPE != new_WINFUNCTYPE:
			raise RuntimeError("Failed to replace WINFUNCTYPE with the custom version")
	finally:
		ctypes.WINFUNCTYPE = ctypes.WINFUNCTYPE_orig


def newVARIANT_value_fset(self,value):
	from comtypes.automation import VARIANT
	realValue=value
	if isinstance(value,_Pointer):
		try:
			value=value.contents
		except (NameError,AttributeError):
			pass
	VARIANT.VALUE_FSEWT_ORIG(self, value)
	if realValue is not value:
		from comtypes.automation import VT_BYREF
		self.vt|=VT_BYREF
		self._.c_void_p=cast(realValue,c_void_p)


def support_byref_in_variants() -> None:
	# Monkey patch comtypes to support byref in variants
	from comtypes.automation import VARIANT
	VARIANT.VALUE_FSEWT_ORIG = VARIANT.value.fset
	VARIANT.value = property(VARIANT.value.fget, newVARIANT_value_fset, VARIANT.value.fdel)


def new__getattr__(self,name):
	import comtypes.client.lazybind
	try:
		return comtypes.client.lazybind.Dispatch.__getattr__orig(self, name)
	except (NameError, AttributeError):
		return getattr(comtypes.client.dynamic._Dispatch(self._comobj),name)


def lazybind_dynamic_to_basic() -> None:
	# Monkeypatch comtypes lazybind dynamic IDispatch support
	# to fallback to the more basic dynamic IDispatch support if the former does not work
	# Example: ITypeComp.bind gives back a vardesc, which comtypes does not yet support
	import comtypes.client.lazybind
	comtypes.client.lazybind.Dispatch.__getattr__orig = comtypes.client.lazybind.Dispatch.__getattr__
	comtypes.client.lazybind.Dispatch.__getattr__ = new__getattr__


def new__call__(self,*args,**kwargs):
	import comtypes.client
	return comtypes.client.dynamic.MethodCaller(0,self)(*args,**kwargs)


def support_invoke_zero() -> None:
	# Monkeypatch comtypes to allow its basic dynamic Dispatch support
	# to support invoke 0 (calling the actual IDispatch object itself)
	import comtypes.client
	comtypes.client.dynamic._Dispatch.__call__ = new__call__


def newCpbDel(self):
	# __del__ may be called while Python is exiting.
	# In this state, global symbols may be set to None
	# Therefore avoid calling into garbageHandler or log,
	# unless isFinalizing is checked first to ensure they are still available
	# Using local variables or calling other methods on this class is still okay.
	isFinalizingFunc = getattr(sys, 'is_finalizing', lambda: True)
	isFinalizing = isFinalizingFunc()
	if hasattr(self, "_deleted"):
		# Don't allow this to be called more than once.
		if not isFinalizing:
			from logHandler import log
			log.debugWarning("COM pointer %r already deleted" % self)
		return
	if not isFinalizing:
		import garbageHandler
		garbageHandler.notifyObjectDeletion(self)
	self._oldCpbDel()
	self._deleted = True
newCpbDel.__name__ = "__del__"


def replace_cpb_del() -> None:
	# Work around an issue with comtypes where __del__ seems to be called twice on COM pointers.
	# This causes Release() to be called more than it should,
	# which is very nasty and will eventually cause us to access pointers which have been freed.
	from comtypes import _compointer_base
	_compointer_base._oldCpbDel = _compointer_base.__del__
	_compointer_base.__del__ = newCpbDel
	del _compointer_base


def newVARIANT_value_fget(self):
	return self._get_value(dynamic=True)


def replace_VARIAN_value_fget() -> None:
	# Monkey patch to force dynamic Dispatch on all vt_dispatch variant values.
	# Certainly needed for comtypes COM servers, but currently very fiddly to do just for that case
	from comtypes.automation import VARIANT
	VARIANT.value = property(newVARIANT_value_fget, VARIANT.value.fset, VARIANT.value.fdel)


def newGetTypeInfo(self,index,lcid=0):
	from comtypes.automation import IDispatch
	res = IDispatch._GetTypeInfo_orig(self, index, lcid)
	if not res:
		from comtypes import COMError
		from comtypes.hresult import E_NOTIMPL
		raise COMError(E_NOTIMPL,None,None)
	return res


def replace_idispatch_getTypeInfo() -> None:
	# #4258: monkeypatch to better handle error where IDispatch's GetTypeInfo can return a NULL pointer.
	# Affects QT5
	from comtypes.automation import IDispatch
	IDispatch._GetTypeInfo_orig = IDispatch._GetTypeInfo
	IDispatch._GetTypeInfo = newGetTypeInfo


def _check_version(actual, tlib_cached_mtime=None):
	from comtypes.tools.codegenerator import version as required
	if actual != required:
		raise ImportError("Wrong version")


def replace_check_version() -> None:
	# Windows updates often include newer versions of dlls/typelibs we use.
	# The typelib being newer than the comtypes generated module doesn't hurt us,
	# so kill the "Typelib newer than module" ImportError.
	# comtypes doesn't let us disable this when running from source, so we need to monkey patch.
	# This is just the code from the original comtypes._check_version excluding the time check.
	import comtypes
	comtypes._check_version = _check_version


def new_my_import(fullname):
	import comtypes.client._generate
	importlib.invalidate_caches()
	return comtypes.client._generate._my_import_orig(fullname)


def replace_my_import() -> None:
	# Monkeypatch comtypes to clear the importlib cache when importing a new module
	import comtypes.client._generate
	comtypes.client._generate._my_import_orig = comtypes.client._generate._my_import
	comtypes.client._generate._my_import = new_my_import


def vt_R8_to_c_double() -> None:
	# Correctly map VT_R8 to c_double.
	# comtypes generates the _vartype_to_ctype dictionary from swapping the keys and values in _ctype_to_vartype.
	# Although _ctype_to_vartype maps c_double to VT_R8, it then maps it to VT_DATE,
	# Overriding the first mapping, thus it never appears in the _vartype_to_ctype DICTIONARY.
	# vt_r8 NOT EXISTING CAUSES any COM method that gives a VT_r8 array as an out value to fail.
	# For example, the cellSize UIA custom property in Excel.
	from comtypes.automation import _vartype_to_ctype, VT_R8
	_vartype_to_ctype[VT_R8] = ctypes.c_double


def appendComInterfacesToGenSearchPath() -> None:
	# Initialise comtypes.client.gen_dir and the comtypes.gen search path
	# and append our comInterfaces directory to the comtypes.gen search path.
	import comtypes.client
	import comtypes.gen
	import comInterfaces
	comtypes.gen.__path__.append(comInterfaces.__path__[0])


def applyMonkeyPatches() -> None:
	# Ensure no comtypes modules were imported
	# before we had a chance to replace `ctypes.WINFUNCTYPE` with our custom version.
	if any(filter(lambda modName: modName.startswith("comtypes"), sys.modules.keys())):
		raise RuntimeError("Comtypes module imported before `ctypes.WINFUNCTYPE` has been replaced")
	replace_WINFUNCTYPE()
	support_byref_in_variants()
	lazybind_dynamic_to_basic()
	support_invoke_zero()
	replace_cpb_del()
	replace_VARIAN_value_fget()
	replace_idispatch_getTypeInfo()
	replace_check_version()
	replace_my_import()
	vt_R8_to_c_double()
	appendComInterfacesToGenSearchPath()
