#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

#Monkey patch comtypes to support byref in variants
from comtypes.automation import VARIANT, VT_BYREF
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
