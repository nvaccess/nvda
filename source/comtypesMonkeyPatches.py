#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

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
