# typelib <unable to determine filename>
_lcid = 0 # change this if required
from ctypes import *
import comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from comtypes import CoClass
from comtypes import BSTR
from ctypes import HRESULT
from comtypes.automation import VARIANT_BOOL
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid


class VTxtAuto(CoClass):
    u'VoiceText Automation Class'
    _reg_clsid_ = GUID('{FF2C7A52-78F9-11CE-B762-00AA004CD65C}')
    _idlflags_ = ['appobject']
    _reg_typelib_ = ('{FF2C7A51-78F9-11CE-B762-00AA004CD65C}', 1, 0)
class IVTxtAuto(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'Text object for the VoiceText application.'
    _iid_ = GUID('{FF2C7A50-78F9-11CE-B762-00AA004CD65C}')
    _idlflags_ = ['dual', 'oleautomation']
VTxtAuto._com_interfaces_ = [IVTxtAuto, comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch]


# values for enumeration 'SPEAKFLAGS'
vtxtst_STATEMENT = 1
vtxtst_QUESTION = 2
vtxtst_COMMAND = 4
vtxtst_WARNING = 8
vtxtst_READING = 16
vtxtst_NUMBERS = 32
vtxtst_SPREADSHEET = 64
vtxtsp_VERYHIGH = 128
vtxtsp_HIGH = 256
vtxtsp_NORMAL = 512
SPEAKFLAGS = c_int # enum
IVTxtAuto._methods_ = [
    COMMETHOD([dispid(1610743808), helpstring(u'Register application with Voice Text.')], HRESULT, 'Register',
              ( ['in'], BSTR, 'pszSite' ),
              ( ['in'], BSTR, 'pszApp' )),
    COMMETHOD([dispid(1610743809), helpstring(u'Speak the text.')], HRESULT, 'Speak',
              ( ['in'], BSTR, 'pszBuffer' ),
              ( ['in'], c_int, 'dwFlags' )),
    COMMETHOD([dispid(1610743810), helpstring(u'Stop speaking the text.')], HRESULT, 'StopSpeaking'),
    COMMETHOD([dispid(1610743811), helpstring(u'Pause speaking the text.')], HRESULT, 'AudioPause'),
    COMMETHOD([dispid(1610743812), helpstring(u'Resume speaking the text.')], HRESULT, 'AudioResume'),
    COMMETHOD([dispid(1610743813), helpstring(u'Rewind the text.')], HRESULT, 'AudioRewind'),
    COMMETHOD([dispid(1610743814), helpstring(u'Fast forward the text.')], HRESULT, 'AudioFastForward'),
    COMMETHOD([dispid(1610743815), helpstring(u'Sets the Automation Server PROGID containing callbacks.'), 'propput'], HRESULT, 'Callback',
              ( ['in'], BSTR, 'rhs' )),
    COMMETHOD([dispid(1610743816), helpstring(u'Set the TTS speed.'), 'propput'], HRESULT, 'Speed',
              ( ['in'], c_int, 'pdwSpeed' )),
    COMMETHOD([dispid(1610743816), helpstring(u'Set the TTS speed.'), 'propget'], HRESULT, 'Speed',
              ( ['retval', 'out'], POINTER(c_int), 'pdwSpeed' )),
    COMMETHOD([dispid(1610743818), helpstring(u'Set the Enabled/Disabled state.'), 'propput'], HRESULT, 'Enabled',
              ( ['in'], c_int, 'pdwEnabled' )),
    COMMETHOD([dispid(1610743818), helpstring(u'Set the Enabled/Disabled state.'), 'propget'], HRESULT, 'Enabled',
              ( ['retval', 'out'], POINTER(c_int), 'pdwEnabled' )),
    COMMETHOD([dispid(1610743820), helpstring(u'Get the speaking state.'), 'propget'], HRESULT, 'IsSpeaking',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pbSpeaking' )),
]
