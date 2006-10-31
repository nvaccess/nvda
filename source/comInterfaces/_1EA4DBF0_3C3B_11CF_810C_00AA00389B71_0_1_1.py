# typelib oleacc.dll
_lcid = 0 # change this if required
from ctypes import *
import comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from ctypes import HRESULT
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes import wireHWND
from comtypes import CoClass
from comtypes.automation import IDispatch
from comtypes.automation import VARIANT
from comtypes import BSTR
WSTRING = c_wchar_p


class IAccessibleHandler(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{03022430-ABC4-11D0-BDE2-00AA001A1953}')
    _idlflags_ = ['oleautomation', 'hidden']
class IAccessible(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{618736E0-3C3D-11CF-810C-00AA00389B71}')
    _idlflags_ = ['dual', 'oleautomation', 'hidden']
IAccessibleHandler._methods_ = [
    COMMETHOD([], HRESULT, 'AccessibleObjectFromID',
              ( ['in'], c_int, 'hwnd' ),
              ( ['in'], c_int, 'lObjectID' ),
              ( ['out'], POINTER(POINTER(IAccessible)), 'pIAccessible' )),
]
class __MIDL_IWinTypes_0009(Union):
    pass
__MIDL_IWinTypes_0009._fields_ = [
    ('hInproc', c_int),
    ('hRemote', c_int),
]
assert sizeof(__MIDL_IWinTypes_0009) == 4, sizeof(__MIDL_IWinTypes_0009)
assert alignment(__MIDL_IWinTypes_0009) == 4, alignment(__MIDL_IWinTypes_0009)
class CAccPropServices(CoClass):
    _reg_clsid_ = GUID('{B5F8350B-0548-48B1-A6EE-88BD00B4A5E7}')
    _idlflags_ = []
    _reg_typelib_ = ('{1EA4DBF0-3C3B-11CF-810C-00AA00389B71}', 1, 1)
class IAccPropServices(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{6E26E776-04F0-495D-80E4-3330352E3169}')
    _idlflags_ = []
CAccPropServices._com_interfaces_ = [IAccPropServices]

class IAccIdentity(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{7852B78D-1CFD-41C1-A615-9C0C85960B5F}')
    _idlflags_ = []
IAccIdentity._methods_ = [
    COMMETHOD([], HRESULT, 'GetIdentityString',
              ( ['in'], c_ulong, 'dwIDChild' ),
              ( ['out'], POINTER(POINTER(c_ubyte)), 'ppIDString' ),
              ( ['out'], POINTER(c_ulong), 'pdwIDStringLen' )),
]
IAccessible._methods_ = [
    COMMETHOD([dispid(-5000), 'hidden', 'propget'], HRESULT, 'accParent',
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'ppdispParent' )),
    COMMETHOD([dispid(-5001), 'hidden', 'propget'], HRESULT, 'accChildCount',
              ( ['retval', 'out'], POINTER(c_int), 'pcountChildren' )),
    COMMETHOD([dispid(-5002), 'hidden', 'propget'], HRESULT, 'accChild',
              ( ['in'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(POINTER(IDispatch)), 'ppdispChild' )),
    COMMETHOD([dispid(-5003), 'hidden', 'propget'], HRESULT, 'accName',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszName' )),
    COMMETHOD([dispid(-5004), 'hidden', 'propget'], HRESULT, 'accValue',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszValue' )),
    COMMETHOD([dispid(-5005), 'hidden', 'propget'], HRESULT, 'accDescription',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszDescription' )),
    COMMETHOD([dispid(-5006), 'hidden', 'propget'], HRESULT, 'accRole',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarRole' )),
    COMMETHOD([dispid(-5007), 'hidden', 'propget'], HRESULT, 'accState',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarState' )),
    COMMETHOD([dispid(-5008), 'hidden', 'propget'], HRESULT, 'accHelp',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszHelp' )),
    COMMETHOD([dispid(-5009), 'hidden', 'propget'], HRESULT, 'accHelpTopic',
              ( ['out'], POINTER(BSTR), 'pszHelpFile' ),
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(c_int), 'pidTopic' )),
    COMMETHOD([dispid(-5010), 'hidden', 'propget'], HRESULT, 'accKeyboardShortcut',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszKeyboardShortcut' )),
    COMMETHOD([dispid(-5011), 'hidden', 'propget'], HRESULT, 'accFocus',
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarChild' )),
    COMMETHOD([dispid(-5012), 'hidden', 'propget'], HRESULT, 'accSelection',
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarChildren' )),
    COMMETHOD([dispid(-5013), 'hidden', 'propget'], HRESULT, 'accDefaultAction',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['retval', 'out'], POINTER(BSTR), 'pszDefaultAction' )),
    COMMETHOD([dispid(-5014), 'hidden'], HRESULT, 'accSelect',
              ( ['in'], c_int, 'flagsSelect' ),
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5015), 'hidden'], HRESULT, 'accLocation',
              ( ['out'], POINTER(c_int), 'pxLeft' ),
              ( ['out'], POINTER(c_int), 'pyTop' ),
              ( ['out'], POINTER(c_int), 'pcxWidth' ),
              ( ['out'], POINTER(c_int), 'pcyHeight' ),
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5016), 'hidden'], HRESULT, 'accNavigate',
              ( ['in'], c_int, 'navDir' ),
              ( ['in', 'optional'], VARIANT, 'varStart' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarEndUpAt' )),
    COMMETHOD([dispid(-5017), 'hidden'], HRESULT, 'accHitTest',
              ( ['in'], c_int, 'xLeft' ),
              ( ['in'], c_int, 'yTop' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'pvarChild' )),
    COMMETHOD([dispid(-5018), 'hidden'], HRESULT, 'accDoDefaultAction',
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5003), 'hidden', 'propput'], HRESULT, 'accName',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['in'], BSTR, 'pszName' )),
    COMMETHOD([dispid(-5004), 'hidden', 'propput'], HRESULT, 'accValue',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['in'], BSTR, 'pszValue' )),
]
class _RemotableHandle(Structure):
    pass
_RemotableHandle._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0009),
]
assert sizeof(_RemotableHandle) == 8, sizeof(_RemotableHandle)
assert alignment(_RemotableHandle) == 4, alignment(_RemotableHandle)
wireHMENU = POINTER(_RemotableHandle)
class IAccPropServer(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{76C0DBBB-15E0-4E7B-B61B-20EEEA2001E0}')
    _idlflags_ = []

# values for enumeration 'AnnoScope'
ANNO_THIS = 0
ANNO_CONTAINER = 1
AnnoScope = c_int # enum
IAccPropServices._methods_ = [
    COMMETHOD([], HRESULT, 'SetPropValue',
              ( ['in'], POINTER(c_ubyte), 'pIDString' ),
              ( ['in'], c_ulong, 'dwIDStringLen' ),
              ( ['in'], comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID, 'idProp' ),
              ( ['in'], VARIANT, 'var' )),
    COMMETHOD([], HRESULT, 'SetPropServer',
              ( ['in'], POINTER(c_ubyte), 'pIDString' ),
              ( ['in'], c_ulong, 'dwIDStringLen' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'paProps' ),
              ( ['in'], c_int, 'cProps' ),
              ( ['in'], POINTER(IAccPropServer), 'pServer' ),
              ( ['in'], AnnoScope, 'AnnoScope' )),
    COMMETHOD([], HRESULT, 'ClearProps',
              ( ['in'], POINTER(c_ubyte), 'pIDString' ),
              ( ['in'], c_ulong, 'dwIDStringLen' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'paProps' ),
              ( ['in'], c_int, 'cProps' )),
    COMMETHOD([], HRESULT, 'SetHwndProp',
              ( ['in'], wireHWND, 'hwnd' ),
              ( ['in'], c_ulong, 'idObject' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID, 'idProp' ),
              ( ['in'], VARIANT, 'var' )),
    COMMETHOD([], HRESULT, 'SetHwndPropStr',
              ( ['in'], wireHWND, 'hwnd' ),
              ( ['in'], c_ulong, 'idObject' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID, 'idProp' ),
              ( ['in'], WSTRING, 'str' )),
    COMMETHOD([], HRESULT, 'SetHwndPropServer',
              ( ['in'], wireHWND, 'hwnd' ),
              ( ['in'], c_ulong, 'idObject' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'paProps' ),
              ( ['in'], c_int, 'cProps' ),
              ( ['in'], POINTER(IAccPropServer), 'pServer' ),
              ( ['in'], AnnoScope, 'AnnoScope' )),
    COMMETHOD([], HRESULT, 'ClearHwndProps',
              ( ['in'], wireHWND, 'hwnd' ),
              ( ['in'], c_ulong, 'idObject' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'paProps' ),
              ( ['in'], c_int, 'cProps' )),
    COMMETHOD([], HRESULT, 'ComposeHwndIdentityString',
              ( ['in'], wireHWND, 'hwnd' ),
              ( ['in'], c_ulong, 'idObject' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['out'], POINTER(POINTER(c_ubyte)), 'ppIDString' ),
              ( ['out'], POINTER(c_ulong), 'pdwIDStringLen' )),
    COMMETHOD([], HRESULT, 'DecomposeHwndIdentityString',
              ( ['in'], POINTER(c_ubyte), 'pIDString' ),
              ( ['in'], c_ulong, 'dwIDStringLen' ),
              ( ['out'], POINTER(wireHWND), 'phwnd' ),
              ( ['out'], POINTER(c_ulong), 'pidObject' ),
              ( ['out'], POINTER(c_ulong), 'pidChild' )),
    COMMETHOD([], HRESULT, 'SetHmenuProp',
              ( ['in'], wireHMENU, 'hmenu' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID, 'idProp' ),
              ( ['in'], VARIANT, 'var' )),
    COMMETHOD([], HRESULT, 'SetHmenuPropStr',
              ( ['in'], wireHMENU, 'hmenu' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID, 'idProp' ),
              ( ['in'], WSTRING, 'str' )),
    COMMETHOD([], HRESULT, 'SetHmenuPropServer',
              ( ['in'], wireHMENU, 'hmenu' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'paProps' ),
              ( ['in'], c_int, 'cProps' ),
              ( ['in'], POINTER(IAccPropServer), 'pServer' ),
              ( ['in'], AnnoScope, 'AnnoScope' )),
    COMMETHOD([], HRESULT, 'ClearHmenuProps',
              ( ['in'], wireHMENU, 'hmenu' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'paProps' ),
              ( ['in'], c_int, 'cProps' )),
    COMMETHOD([], HRESULT, 'ComposeHmenuIdentityString',
              ( ['in'], wireHMENU, 'hmenu' ),
              ( ['in'], c_ulong, 'idChild' ),
              ( ['out'], POINTER(POINTER(c_ubyte)), 'ppIDString' ),
              ( ['out'], POINTER(c_ulong), 'pdwIDStringLen' )),
    COMMETHOD([], HRESULT, 'DecomposeHmenuIdentityString',
              ( ['in'], POINTER(c_ubyte), 'pIDString' ),
              ( ['in'], c_ulong, 'dwIDStringLen' ),
              ( ['out'], POINTER(wireHMENU), 'phmenu' ),
              ( ['out'], POINTER(c_ulong), 'pidChild' )),
]
IAccPropServer._methods_ = [
    COMMETHOD([], HRESULT, 'GetPropValue',
              ( ['in'], POINTER(c_ubyte), 'pIDString' ),
              ( ['in'], c_ulong, 'dwIDStringLen' ),
              ( ['in'], comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID, 'idProp' ),
              ( ['out'], POINTER(VARIANT), 'pvarValue' ),
              ( ['out'], POINTER(c_int), 'pfHasProp' )),
]
