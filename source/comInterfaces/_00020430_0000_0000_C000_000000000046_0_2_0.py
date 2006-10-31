# typelib C:\WINDOWS\system32\stdole2.tlb
_lcid = 0 # change this if required
from ctypes import *
from comtypes.automation import VARIANT_BOOL
FONTBOLD = VARIANT_BOOL
from comtypes import GUID
from comtypes import IUnknown
from comtypes import BSTR
from ctypes import HRESULT
OLE_HANDLE = c_int
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes.automation import IDispatch
from comtypes import DISPMETHOD, DISPPROPERTY, helpstring
from comtypes.automation import EXCEPINFO
FONTITALIC = VARIANT_BOOL
FONTNAME = BSTR
OLE_ENABLEDEFAULTBOOL = VARIANT_BOOL
OLE_OPTEXCLUSIVE = VARIANT_BOOL
from comtypes.automation import IEnumVARIANT
OLE_YPOS_CONTAINER = c_float
OLE_YSIZE_HIMETRIC = c_int
OLE_YPOS_HIMETRIC = c_int
OLE_YSIZE_PIXELS = c_int
OLE_YPOS_PIXELS = c_int
OLE_XSIZE_HIMETRIC = c_int
OLE_XPOS_HIMETRIC = c_int
OLE_YSIZE_CONTAINER = c_float
from comtypes import CoClass
FONTSIZE = c_float
OLE_XPOS_PIXELS = c_int
OLE_COLOR = c_ulong
FONTSTRIKETHROUGH = VARIANT_BOOL
FONTUNDERSCORE = VARIANT_BOOL
OLE_CANCELBOOL = VARIANT_BOOL
OLE_XSIZE_CONTAINER = c_float
OLE_XPOS_CONTAINER = c_float
OLE_XSIZE_PIXELS = c_int
from comtypes.automation import DISPPARAMS
from comtypes import GUID


class IFont(IUnknown):
    _case_insensitive_ = True
    u'Font Object'
    _iid_ = GUID('{BEF6E002-A874-101A-8BBA-00AA00300CAB}')
    _idlflags_ = ['hidden']
IFont._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'pname' )),
    COMMETHOD(['propput'], HRESULT, 'Name',
              ( ['in'], BSTR, 'pname' )),
    COMMETHOD(['propget'], HRESULT, 'Size',
              ( ['retval', 'out'], POINTER(c_float), 'psize' )),
    COMMETHOD(['propput'], HRESULT, 'Size',
              ( ['in'], c_float, 'psize' )),
    COMMETHOD(['propget'], HRESULT, 'Bold',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pbold' )),
    COMMETHOD(['propput'], HRESULT, 'Bold',
              ( ['in'], VARIANT_BOOL, 'pbold' )),
    COMMETHOD(['propget'], HRESULT, 'Italic',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pitalic' )),
    COMMETHOD(['propput'], HRESULT, 'Italic',
              ( ['in'], VARIANT_BOOL, 'pitalic' )),
    COMMETHOD(['propget'], HRESULT, 'Underline',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'punderline' )),
    COMMETHOD(['propput'], HRESULT, 'Underline',
              ( ['in'], VARIANT_BOOL, 'punderline' )),
    COMMETHOD(['propget'], HRESULT, 'Strikethrough',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pstrikethrough' )),
    COMMETHOD(['propput'], HRESULT, 'Strikethrough',
              ( ['in'], VARIANT_BOOL, 'pstrikethrough' )),
    COMMETHOD(['propget'], HRESULT, 'Weight',
              ( ['retval', 'out'], POINTER(c_short), 'pweight' )),
    COMMETHOD(['propput'], HRESULT, 'Weight',
              ( ['in'], c_short, 'pweight' )),
    COMMETHOD(['propget'], HRESULT, 'Charset',
              ( ['retval', 'out'], POINTER(c_short), 'pcharset' )),
    COMMETHOD(['propput'], HRESULT, 'Charset',
              ( ['in'], c_short, 'pcharset' )),
    COMMETHOD(['propget'], HRESULT, 'hFont',
              ( ['retval', 'out'], POINTER(OLE_HANDLE), 'phfont' )),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IFont)), 'ppfont' )),
    COMMETHOD([], HRESULT, 'IsEqual',
              ( ['in'], POINTER(IFont), 'pfontOther' )),
    COMMETHOD([], HRESULT, 'SetRatio',
              ( ['in'], c_int, 'cyLogical' ),
              ( ['in'], c_int, 'cyHimetric' )),
    COMMETHOD([], HRESULT, 'AddRefHfont',
              ( ['in'], OLE_HANDLE, 'hFont' )),
    COMMETHOD([], HRESULT, 'ReleaseHfont',
              ( ['in'], OLE_HANDLE, 'hFont' )),
]
class Font(IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{BEF6E003-A874-101A-8BBA-00AA00300CAB}')
    _idlflags_ = []
    _methods_ = []
Font._disp_methods_ = [
    DISPPROPERTY([dispid(0)], BSTR, 'Name'),
    DISPPROPERTY([dispid(2)], c_float, 'Size'),
    DISPPROPERTY([dispid(3)], VARIANT_BOOL, 'Bold'),
    DISPPROPERTY([dispid(4)], VARIANT_BOOL, 'Italic'),
    DISPPROPERTY([dispid(5)], VARIANT_BOOL, 'Underline'),
    DISPPROPERTY([dispid(6)], VARIANT_BOOL, 'Strikethrough'),
    DISPPROPERTY([dispid(7)], c_short, 'Weight'),
    DISPPROPERTY([dispid(8)], c_short, 'Charset'),
]

# values for enumeration 'OLE_TRISTATE'
Unchecked = 0
Checked = 1
Gray = 2
OLE_TRISTATE = c_int # enum
class FontEvents(IDispatch):
    _case_insensitive_ = True
    'Event interface for the Font object'
    _iid_ = GUID('{4EF6100A-AF88-11D0-9846-00C04FC29993}')
    _idlflags_ = ['hidden']
    _methods_ = []
FontEvents._disp_methods_ = [
    DISPMETHOD([dispid(9)], None, 'FontChanged',
               ( ['in'], BSTR, 'PropertyName' )),
]
class Picture(IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{7BF80981-BF32-101A-8BBB-00AA00300CAB}')
    _idlflags_ = []
    _methods_ = []
Picture._disp_methods_ = [
    DISPPROPERTY([dispid(0), 'readonly'], OLE_HANDLE, 'Handle'),
    DISPPROPERTY([dispid(2)], OLE_HANDLE, 'hPal'),
    DISPPROPERTY([dispid(3), 'readonly'], c_short, 'Type'),
    DISPPROPERTY([dispid(4), 'readonly'], OLE_XSIZE_HIMETRIC, 'Width'),
    DISPPROPERTY([dispid(5), 'readonly'], OLE_YSIZE_HIMETRIC, 'Height'),
    DISPMETHOD([dispid(6)], None, 'Render',
               ( [], c_int, 'hdc' ),
               ( [], c_int, 'x' ),
               ( [], c_int, 'y' ),
               ( [], c_int, 'cx' ),
               ( [], c_int, 'cy' ),
               ( [], OLE_XPOS_HIMETRIC, 'xSrc' ),
               ( [], OLE_YPOS_HIMETRIC, 'ySrc' ),
               ( [], OLE_XSIZE_HIMETRIC, 'cxSrc' ),
               ( [], OLE_YSIZE_HIMETRIC, 'cySrc' ),
               ( [], c_void_p, 'prcWBounds' )),
]
IPictureDisp = Picture
class StdFont(CoClass):
    _reg_clsid_ = GUID('{0BE35203-8F91-11CE-9DE3-00AA004BB851}')
    _idlflags_ = []
    _reg_typelib_ = ('{00020430-0000-0000-C000-000000000046}', 2, 0)
StdFont._com_interfaces_ = [Font, IFont]
StdFont._outgoing_interfaces_ = [FontEvents]

class IPicture(IUnknown):
    _case_insensitive_ = True
    u'Picture Object'
    _iid_ = GUID('{7BF80980-BF32-101A-8BBB-00AA00300CAB}')
    _idlflags_ = ['hidden']
IPicture._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'Handle',
              ( ['retval', 'out'], POINTER(OLE_HANDLE), 'phandle' )),
    COMMETHOD(['propget'], HRESULT, 'hPal',
              ( ['retval', 'out'], POINTER(OLE_HANDLE), 'phpal' )),
    COMMETHOD(['propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(c_short), 'ptype' )),
    COMMETHOD(['propget'], HRESULT, 'Width',
              ( ['retval', 'out'], POINTER(OLE_XSIZE_HIMETRIC), 'pwidth' )),
    COMMETHOD(['propget'], HRESULT, 'Height',
              ( ['retval', 'out'], POINTER(OLE_YSIZE_HIMETRIC), 'pheight' )),
    COMMETHOD([], HRESULT, 'Render',
              ( ['in'], c_int, 'hdc' ),
              ( ['in'], c_int, 'x' ),
              ( ['in'], c_int, 'y' ),
              ( ['in'], c_int, 'cx' ),
              ( ['in'], c_int, 'cy' ),
              ( ['in'], OLE_XPOS_HIMETRIC, 'xSrc' ),
              ( ['in'], OLE_YPOS_HIMETRIC, 'ySrc' ),
              ( ['in'], OLE_XSIZE_HIMETRIC, 'cxSrc' ),
              ( ['in'], OLE_YSIZE_HIMETRIC, 'cySrc' ),
              ( ['in'], c_void_p, 'prcWBounds' )),
    COMMETHOD(['propput'], HRESULT, 'hPal',
              ( ['in'], OLE_HANDLE, 'phpal' )),
    COMMETHOD(['propget'], HRESULT, 'CurDC',
              ( ['retval', 'out'], POINTER(c_int), 'phdcOut' )),
    COMMETHOD([], HRESULT, 'SelectPicture',
              ( ['in'], c_int, 'hdcIn' ),
              ( ['out'], POINTER(c_int), 'phdcOut' ),
              ( ['out'], POINTER(OLE_HANDLE), 'phbmpOut' )),
    COMMETHOD(['propget'], HRESULT, 'KeepOriginalFormat',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pfkeep' )),
    COMMETHOD(['propput'], HRESULT, 'KeepOriginalFormat',
              ( ['in'], VARIANT_BOOL, 'pfkeep' )),
    COMMETHOD([], HRESULT, 'PictureChanged'),
    COMMETHOD([], HRESULT, 'SaveAsFile',
              ( ['in'], c_void_p, 'pstm' ),
              ( ['in'], VARIANT_BOOL, 'fSaveMemCopy' ),
              ( ['out'], POINTER(c_int), 'pcbSize' )),
    COMMETHOD(['propget'], HRESULT, 'Attributes',
              ( ['retval', 'out'], POINTER(c_int), 'pdwAttr' )),
    COMMETHOD([], HRESULT, 'SetHdc',
              ( ['in'], OLE_HANDLE, 'hdc' )),
]
class StdPicture(CoClass):
    _reg_clsid_ = GUID('{0BE35204-8F91-11CE-9DE3-00AA004BB851}')
    _idlflags_ = []
    _reg_typelib_ = ('{00020430-0000-0000-C000-000000000046}', 2, 0)
StdPicture._com_interfaces_ = [Picture, IPicture]

IFontDisp = Font

# values for enumeration 'LoadPictureConstants'
Default = 0
Monochrome = 1
VgaColor = 2
Color = 4
LoadPictureConstants = c_int # enum
IFontEventsDisp = FontEvents
