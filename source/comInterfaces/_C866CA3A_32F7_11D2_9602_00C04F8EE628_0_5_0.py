# typelib C:\Program Files\Common Files\Microsoft Shared\Speech\sapi.dll
_lcid = 0 # change this if required
from ctypes import *
import comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from ctypes import HRESULT
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes.automation import VARIANT_BOOL
from comtypes.automation import VARIANT
from comtypes import BSTR
from comtypes import IUnknown
from comtypes import CoClass
WSTRING = c_wchar_p
LONG_PTR = c_int
from comtypes import wireHWND
UINT_PTR = c_ulong
from comtypes import DISPMETHOD, DISPPROPERTY, helpstring


SpeechRegistryLocalMachineRoot = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech' # Constant BSTR
SpeechVoiceSkipTypeSentence = u'Sentence' # Constant BSTR

# values for enumeration 'DISPIDSPTSI'
DISPIDSPTSI_ActiveOffset = 1
DISPIDSPTSI_ActiveLength = 2
DISPIDSPTSI_SelectionOffset = 3
DISPIDSPTSI_SelectionLength = 4
DISPIDSPTSI = c_int # enum

# values for enumeration 'DISPID_SpeechGrammarRuleState'
DISPID_SGRSRule = 1
DISPID_SGRSTransitions = 2
DISPID_SGRSAddWordTransition = 3
DISPID_SGRSAddRuleTransition = 4
DISPID_SGRSAddSpecialTransition = 5
DISPID_SpeechGrammarRuleState = c_int # enum

# values for enumeration 'SPEVENTENUM'
SPEI_UNDEFINED = 0
SPEI_START_INPUT_STREAM = 1
SPEI_END_INPUT_STREAM = 2
SPEI_VOICE_CHANGE = 3
SPEI_TTS_BOOKMARK = 4
SPEI_WORD_BOUNDARY = 5
SPEI_PHONEME = 6
SPEI_SENTENCE_BOUNDARY = 7
SPEI_VISEME = 8
SPEI_TTS_AUDIO_LEVEL = 9
SPEI_TTS_PRIVATE = 15
SPEI_MIN_TTS = 1
SPEI_MAX_TTS = 15
SPEI_END_SR_STREAM = 34
SPEI_SOUND_START = 35
SPEI_SOUND_END = 36
SPEI_PHRASE_START = 37
SPEI_RECOGNITION = 38
SPEI_HYPOTHESIS = 39
SPEI_SR_BOOKMARK = 40
SPEI_PROPERTY_NUM_CHANGE = 41
SPEI_PROPERTY_STRING_CHANGE = 42
SPEI_FALSE_RECOGNITION = 43
SPEI_INTERFERENCE = 44
SPEI_REQUEST_UI = 45
SPEI_RECO_STATE_CHANGE = 46
SPEI_ADAPTATION = 47
SPEI_START_SR_STREAM = 48
SPEI_RECO_OTHER_CONTEXT = 49
SPEI_SR_AUDIO_LEVEL = 50
SPEI_SR_PRIVATE = 52
SPEI_MIN_SR = 34
SPEI_MAX_SR = 52
SPEI_RESERVED1 = 30
SPEI_RESERVED2 = 33
SPEI_RESERVED3 = 63
SPEVENTENUM = c_int # enum

# values for enumeration 'DISPID_SpeechPhoneConverter'
DISPID_SPCLangId = 1
DISPID_SPCPhoneToId = 2
DISPID_SPCIdToPhone = 3
DISPID_SpeechPhoneConverter = c_int # enum
SpeechGrammarTagUnlimitedDictation = u'*+' # Constant BSTR

# values for enumeration '_SPAUDIOSTATE'
SPAS_CLOSED = 0
SPAS_STOP = 1
SPAS_PAUSE = 2
SPAS_RUN = 3
_SPAUDIOSTATE = c_int # enum
class ISequentialStream(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0C733A30-2A1C-11CE-ADE5-00AA0044773D}')
    _idlflags_ = []
class IStream(ISequentialStream):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000C-0000-0000-C000-000000000046}')
    _idlflags_ = []
ISequentialStream._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteRead',
              ( ['out'], POINTER(c_ubyte), 'pv' ),
              ( ['in'], c_ulong, 'cb' ),
              ( ['out'], POINTER(c_ulong), 'pcbRead' )),
    COMMETHOD([], HRESULT, 'RemoteWrite',
              ( ['in'], POINTER(c_ubyte), 'pv' ),
              ( ['in'], c_ulong, 'cb' ),
              ( ['out'], POINTER(c_ulong), 'pcbWritten' )),
]
class _LARGE_INTEGER(Structure):
    pass
_LARGE_INTEGER._fields_ = [
    ('QuadPart', c_longlong),
]
assert sizeof(_LARGE_INTEGER) == 8, sizeof(_LARGE_INTEGER)
assert alignment(_LARGE_INTEGER) == 8, alignment(_LARGE_INTEGER)
class _ULARGE_INTEGER(Structure):
    pass
_ULARGE_INTEGER._fields_ = [
    ('QuadPart', c_ulonglong),
]
assert sizeof(_ULARGE_INTEGER) == 8, sizeof(_ULARGE_INTEGER)
assert alignment(_ULARGE_INTEGER) == 8, alignment(_ULARGE_INTEGER)
class tagSTATSTG(Structure):
    pass
IStream._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteSeek',
              ( ['in'], _LARGE_INTEGER, 'dlibMove' ),
              ( ['in'], c_ulong, 'dwOrigin' ),
              ( ['out'], POINTER(_ULARGE_INTEGER), 'plibNewPosition' )),
    COMMETHOD([], HRESULT, 'SetSize',
              ( ['in'], _ULARGE_INTEGER, 'libNewSize' )),
    COMMETHOD([], HRESULT, 'RemoteCopyTo',
              ( ['in'], POINTER(IStream), 'pstm' ),
              ( ['in'], _ULARGE_INTEGER, 'cb' ),
              ( ['out'], POINTER(_ULARGE_INTEGER), 'pcbRead' ),
              ( ['out'], POINTER(_ULARGE_INTEGER), 'pcbWritten' )),
    COMMETHOD([], HRESULT, 'Commit',
              ( ['in'], c_ulong, 'grfCommitFlags' )),
    COMMETHOD([], HRESULT, 'Revert'),
    COMMETHOD([], HRESULT, 'LockRegion',
              ( ['in'], _ULARGE_INTEGER, 'libOffset' ),
              ( ['in'], _ULARGE_INTEGER, 'cb' ),
              ( ['in'], c_ulong, 'dwLockType' )),
    COMMETHOD([], HRESULT, 'UnlockRegion',
              ( ['in'], _ULARGE_INTEGER, 'libOffset' ),
              ( ['in'], _ULARGE_INTEGER, 'cb' ),
              ( ['in'], c_ulong, 'dwLockType' )),
    COMMETHOD([], HRESULT, 'Stat',
              ( ['out'], POINTER(tagSTATSTG), 'pstatstg' ),
              ( ['in'], c_ulong, 'grfStatFlag' )),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IStream)), 'ppstm' )),
]
class ISpeechRecognizer(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechRecognizer Interface'
    _iid_ = GUID('{2D5F1C0C-BD75-4B08-9478-3B11FEA2586C}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechObjectToken(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechObjectToken Interface'
    _iid_ = GUID('{C74A3ADC-B727-4500-A84A-B526721C8B8C}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechBaseStream(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechBaseStream Interface'
    _iid_ = GUID('{6450336F-7D49-4CED-8097-49D6DEE37294}')
    _idlflags_ = ['dual', 'oleautomation']

# values for enumeration 'SpeechRecognizerState'
SRSInactive = 0
SRSActive = 1
SRSActiveAlways = 2
SRSInactiveWithPurge = 3
SpeechRecognizerState = c_int # enum
class ISpeechRecognizerStatus(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechRecognizerStatus Interface'
    _iid_ = GUID('{BFF9E781-53EC-484E-BB8A-0E1B5551E35C}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechRecoContext(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechRecoContext Interface'
    _iid_ = GUID('{580AA49D-7E1E-4809-B8E2-57DA806104B8}')
    _idlflags_ = ['dual', 'oleautomation']

# values for enumeration 'SpeechFormatType'
SFTInput = 0
SFTSREngine = 1
SpeechFormatType = c_int # enum
class ISpeechAudioFormat(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechAudioFormat Interface'
    _iid_ = GUID('{E6E9C590-3E18-40E3-8299-061F98BDE7C7}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechObjectTokens(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechObjectTokens Interface'
    _iid_ = GUID('{9285B776-2E7B-4BC0-B53E-580EB6FA967F}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechRecognizer._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Recognizer'), 'propputref'], HRESULT, 'Recognizer',
              ( ['in'], POINTER(ISpeechObjectToken), 'Recognizer' )),
    COMMETHOD([dispid(1), helpstring(u'Recognizer'), 'propget'], HRESULT, 'Recognizer',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectToken)), 'Recognizer' )),
    COMMETHOD([dispid(2), helpstring(u'AllowAudioInputFormatChangesOnNextSet'), 'hidden', 'propput'], HRESULT, 'AllowAudioInputFormatChangesOnNextSet',
              ( ['in'], VARIANT_BOOL, 'Allow' )),
    COMMETHOD([dispid(2), helpstring(u'AllowAudioInputFormatChangesOnNextSet'), 'hidden', 'propget'], HRESULT, 'AllowAudioInputFormatChangesOnNextSet',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Allow' )),
    COMMETHOD([dispid(3), helpstring(u'AudioInput'), 'propputref'], HRESULT, 'AudioInput',
              ( ['in', 'optional'], POINTER(ISpeechObjectToken), 'AudioInput', 0 )),
    COMMETHOD([dispid(3), helpstring(u'AudioInput'), 'propget'], HRESULT, 'AudioInput',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectToken)), 'AudioInput' )),
    COMMETHOD([dispid(4), helpstring(u'AudioInputStream'), 'propputref'], HRESULT, 'AudioInputStream',
              ( ['in', 'optional'], POINTER(ISpeechBaseStream), 'AudioInputStream', 0 )),
    COMMETHOD([dispid(4), helpstring(u'AudioInputStream'), 'propget'], HRESULT, 'AudioInputStream',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechBaseStream)), 'AudioInputStream' )),
    COMMETHOD([dispid(5), helpstring(u'IsShared'), 'propget'], HRESULT, 'IsShared',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Shared' )),
    COMMETHOD([dispid(6), helpstring(u'State'), 'propput'], HRESULT, 'State',
              ( ['in'], SpeechRecognizerState, 'State' )),
    COMMETHOD([dispid(6), helpstring(u'State'), 'propget'], HRESULT, 'State',
              ( ['retval', 'out'], POINTER(SpeechRecognizerState), 'State' )),
    COMMETHOD([dispid(7), helpstring(u'Status'), 'propget'], HRESULT, 'Status',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecognizerStatus)), 'Status' )),
    COMMETHOD([dispid(8), helpstring(u'Profile'), 'propputref'], HRESULT, 'Profile',
              ( ['in', 'optional'], POINTER(ISpeechObjectToken), 'Profile', 0 )),
    COMMETHOD([dispid(8), helpstring(u'Profile'), 'propget'], HRESULT, 'Profile',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectToken)), 'Profile' )),
    COMMETHOD([dispid(9), helpstring(u'EmulateRecognition')], HRESULT, 'EmulateRecognition',
              ( ['in'], VARIANT, 'TextElements' ),
              ( ['in', 'optional'], POINTER(VARIANT), 'ElementDisplayAttributes', u'' ),
              ( ['in', 'optional'], c_int, 'LanguageId', 0 )),
    COMMETHOD([dispid(10), helpstring(u'CreateRecoContext')], HRESULT, 'CreateRecoContext',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecoContext)), 'NewContext' )),
    COMMETHOD([dispid(11), helpstring(u'GetFormat')], HRESULT, 'GetFormat',
              ( ['in'], SpeechFormatType, 'Type' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioFormat)), 'Format' )),
    COMMETHOD([dispid(12), helpstring(u'SetPropertyNumber'), 'hidden'], HRESULT, 'SetPropertyNumber',
              ( ['in'], BSTR, 'Name' ),
              ( ['in'], c_int, 'Value' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Supported' )),
    COMMETHOD([dispid(13), helpstring(u'GetPropertyNumber'), 'hidden'], HRESULT, 'GetPropertyNumber',
              ( ['in'], BSTR, 'Name' ),
              ( ['in', 'out'], POINTER(c_int), 'Value' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Supported' )),
    COMMETHOD([dispid(14), helpstring(u'SetPropertyString'), 'hidden'], HRESULT, 'SetPropertyString',
              ( ['in'], BSTR, 'Name' ),
              ( ['in'], BSTR, 'Value' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Supported' )),
    COMMETHOD([dispid(15), helpstring(u'GetPropertyString'), 'hidden'], HRESULT, 'GetPropertyString',
              ( ['in'], BSTR, 'Name' ),
              ( ['in', 'out'], POINTER(BSTR), 'Value' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Supported' )),
    COMMETHOD([dispid(16), helpstring(u'IsUISupported')], HRESULT, 'IsUISupported',
              ( ['in'], BSTR, 'TypeOfUI' ),
              ( ['in', 'optional'], POINTER(VARIANT), 'ExtraData', u'' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Supported' )),
    COMMETHOD([dispid(17), helpstring(u'DisplayUI')], HRESULT, 'DisplayUI',
              ( ['in'], c_int, 'hWndParent' ),
              ( ['in'], BSTR, 'Title' ),
              ( ['in'], BSTR, 'TypeOfUI' ),
              ( ['in', 'optional'], POINTER(VARIANT), 'ExtraData', u'' )),
    COMMETHOD([dispid(18), helpstring(u'GetRecognizers')], HRESULT, 'GetRecognizers',
              ( ['in', 'optional'], BSTR, 'RequiredAttributes', u'' ),
              ( ['in', 'optional'], BSTR, 'OptionalAttributes', u'' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectTokens)), 'ObjectTokens' )),
    COMMETHOD([dispid(19), helpstring(u'GetAudioInputs')], HRESULT, 'GetAudioInputs',
              ( ['in', 'optional'], BSTR, 'RequiredAttributes', u'' ),
              ( ['in', 'optional'], BSTR, 'OptionalAttributes', u'' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectTokens)), 'ObjectTokens' )),
    COMMETHOD([dispid(20), helpstring(u'GetProfiles')], HRESULT, 'GetProfiles',
              ( ['in', 'optional'], BSTR, 'RequiredAttributes', u'' ),
              ( ['in', 'optional'], BSTR, 'OptionalAttributes', u'' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectTokens)), 'ObjectTokens' )),
]
class ISpeechFileStream(ISpeechBaseStream):
    _case_insensitive_ = True
    u'ISpeechFileStream Interface'
    _iid_ = GUID('{AF67F125-AB39-4E93-B4A2-CC2E66E182A7}')
    _idlflags_ = ['dual', 'oleautomation']

# values for enumeration 'SpeechStreamSeekPositionType'
SSSPTRelativeToStart = 0
SSSPTRelativeToCurrentPosition = 1
SSSPTRelativeToEnd = 2
SpeechStreamSeekPositionType = c_int # enum
ISpeechBaseStream._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Format'), 'propget'], HRESULT, 'Format',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioFormat)), 'AudioFormat' )),
    COMMETHOD([dispid(1), helpstring(u'Format'), 'propputref'], HRESULT, 'Format',
              ( ['in'], POINTER(ISpeechAudioFormat), 'AudioFormat' )),
    COMMETHOD([dispid(2), helpstring(u'Read')], HRESULT, 'Read',
              ( ['out'], POINTER(VARIANT), 'Buffer' ),
              ( ['in'], c_int, 'NumberOfBytes' ),
              ( ['retval', 'out'], POINTER(c_int), 'BytesRead' )),
    COMMETHOD([dispid(3), helpstring(u'Write')], HRESULT, 'Write',
              ( ['in'], VARIANT, 'Buffer' ),
              ( ['retval', 'out'], POINTER(c_int), 'BytesWritten' )),
    COMMETHOD([dispid(4), helpstring(u'Seek')], HRESULT, 'Seek',
              ( ['in'], VARIANT, 'Position' ),
              ( ['in', 'optional'], SpeechStreamSeekPositionType, 'Origin', 0 ),
              ( ['retval', 'out'], POINTER(VARIANT), 'NewPosition' )),
]

# values for enumeration 'SpeechStreamFileMode'
SSFMOpenForRead = 0
SSFMOpenReadWrite = 1
SSFMCreate = 2
SSFMCreateForWrite = 3
SpeechStreamFileMode = c_int # enum
ISpeechFileStream._methods_ = [
    COMMETHOD([dispid(100), helpstring(u'Open')], HRESULT, 'Open',
              ( ['in'], BSTR, 'FileName' ),
              ( ['in', 'optional'], SpeechStreamFileMode, 'FileMode', 0 ),
              ( ['in', 'optional'], VARIANT_BOOL, 'DoEvents', False )),
    COMMETHOD([dispid(101), helpstring(u'Close')], HRESULT, 'Close'),
]

# values for enumeration 'DISPID_SpeechCustomStream'
DISPID_SCSBaseStream = 100
DISPID_SpeechCustomStream = c_int # enum
class SPWORDLIST(Structure):
    pass
class SPWORD(Structure):
    pass
SPWORDLIST._fields_ = [
    ('ulSize', c_ulong),
    ('pvBuffer', POINTER(c_ubyte)),
    ('pFirstWord', POINTER(SPWORD)),
]
assert sizeof(SPWORDLIST) == 12, sizeof(SPWORDLIST)
assert alignment(SPWORDLIST) == 4, alignment(SPWORDLIST)

# values for enumeration 'DISPID_SpeechGrammarRule'
DISPID_SGRAttributes = 1
DISPID_SGRInitialState = 2
DISPID_SGRName = 3
DISPID_SGRId = 4
DISPID_SGRClear = 5
DISPID_SGRAddResource = 6
DISPID_SGRAddState = 7
DISPID_SpeechGrammarRule = c_int # enum
Speech_StreamPos_RealTime = -1 # Constant c_int
SpeechAddRemoveWord = u'AddRemoveWord' # Constant BSTR
class ISpNotifySink(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpNotifySink Interface'
    _iid_ = GUID('{259684DC-37C3-11D2-9603-00C04F8EE628}')
    _idlflags_ = ['restricted']
ISpNotifySink._methods_ = [
    COMMETHOD([], HRESULT, 'Notify'),
]
class SPWORDPRONUNCIATIONLIST(Structure):
    pass
class SPWORDPRONUNCIATION(Structure):
    pass
SPWORDPRONUNCIATIONLIST._fields_ = [
    ('ulSize', c_ulong),
    ('pvBuffer', POINTER(c_ubyte)),
    ('pFirstWordPronunciation', POINTER(SPWORDPRONUNCIATION)),
]
assert sizeof(SPWORDPRONUNCIATIONLIST) == 12, sizeof(SPWORDPRONUNCIATIONLIST)
assert alignment(SPWORDPRONUNCIATIONLIST) == 4, alignment(SPWORDPRONUNCIATIONLIST)

# values for enumeration 'DISPID_SpeechPhraseAlternates'
DISPID_SPAsCount = 1
DISPID_SPAsItem = 0
DISPID_SPAs_NewEnum = -4
DISPID_SpeechPhraseAlternates = c_int # enum

# values for enumeration 'SpeechDataKeyLocation'
SDKLDefaultLocation = 0
SDKLCurrentUser = 1
SDKLLocalMachine = 2
SDKLCurrentConfig = 5
SpeechDataKeyLocation = c_int # enum

# values for enumeration 'DISPID_SpeechPhraseInfo'
DISPID_SPILanguageId = 1
DISPID_SPIGrammarId = 2
DISPID_SPIStartTime = 3
DISPID_SPIAudioStreamPosition = 4
DISPID_SPIAudioSizeBytes = 5
DISPID_SPIRetainedSizeBytes = 6
DISPID_SPIAudioSizeTime = 7
DISPID_SPIRule = 8
DISPID_SPIProperties = 9
DISPID_SPIElements = 10
DISPID_SPIReplacements = 11
DISPID_SPIEngineId = 12
DISPID_SPIEnginePrivateData = 13
DISPID_SPISaveToMemory = 14
DISPID_SPIGetText = 15
DISPID_SPIGetDisplayAttributes = 16
DISPID_SpeechPhraseInfo = c_int # enum
class ISpeechPhraseAlternates(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseAlternates Interface'
    _iid_ = GUID('{B238B6D5-F276-4C3D-A6C1-2974801C3CC2}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechPhraseAlternate(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseAlternate Interface'
    _iid_ = GUID('{27864A2A-2B9F-4CB8-92D3-0D2722FD1E73}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechPhraseAlternates._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseAlternate)), 'PhraseAlternate' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the alternates'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]

# values for enumeration 'SPGRAMMARWORDTYPE'
SPWT_DISPLAY = 0
SPWT_LEXICAL = 1
SPWT_PRONUNCIATION = 2
SPGRAMMARWORDTYPE = c_int # enum

# values for enumeration 'DISPID_SpeechRecoResultTimes'
DISPID_SRRTStreamTime = 1
DISPID_SRRTLength = 2
DISPID_SRRTTickCount = 3
DISPID_SRRTOffsetFromStart = 4
DISPID_SpeechRecoResultTimes = c_int # enum
class WaveFormatEx(Structure):
    pass
WaveFormatEx._fields_ = [
    ('wFormatTag', c_ushort),
    ('nChannels', c_ushort),
    ('nSamplesPerSec', c_ulong),
    ('nAvgBytesPerSec', c_ulong),
    ('nBlockAlign', c_ushort),
    ('wBitsPerSample', c_ushort),
    ('cbSize', c_ushort),
]
assert sizeof(WaveFormatEx) == 20, sizeof(WaveFormatEx)
assert alignment(WaveFormatEx) == 4, alignment(WaveFormatEx)
class SpNotifyTranslator(CoClass):
    u'SpNotify'
    _reg_clsid_ = GUID('{E2AE5372-5D40-11D2-960E-00C04F8EE628}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpNotifyTranslator(ISpNotifySink):
    _case_insensitive_ = True
    u'ISpNotifyTranslator Interface'
    _iid_ = GUID('{ACA16614-5D3D-11D2-960E-00C04F8EE628}')
    _idlflags_ = ['restricted']
SpNotifyTranslator._com_interfaces_ = [ISpNotifyTranslator]

class ISpPhrase(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpPhrase Interface'
    _iid_ = GUID('{1A5C0354-B621-4B5A-8791-D306ED379E53}')
    _idlflags_ = ['restricted']
class ISpRecoResult(ISpPhrase):
    _case_insensitive_ = True
    u'ISpRecoResult Interface'
    _iid_ = GUID('{20B053BE-E235-43CD-9A2A-8D17A48B7842}')
    _idlflags_ = ['restricted']
class SPPHRASE(Structure):
    pass
class SPSERIALIZEDPHRASE(Structure):
    pass
ISpPhrase._methods_ = [
    COMMETHOD([], HRESULT, 'GetPhrase',
              ( ['out'], POINTER(POINTER(SPPHRASE)), 'ppCoMemPhrase' )),
    COMMETHOD([], HRESULT, 'GetSerializedPhrase',
              ( ['out'], POINTER(POINTER(SPSERIALIZEDPHRASE)), 'ppCoMemPhrase' )),
    COMMETHOD([], HRESULT, 'GetText',
              ( ['in'], c_ulong, 'ulStart' ),
              ( ['in'], c_ulong, 'ulCount' ),
              ( ['in'], c_int, 'fUseTextReplacements' ),
              ( ['out'], POINTER(POINTER(c_ushort)), 'ppszCoMemText' ),
              ( ['out'], POINTER(c_ubyte), 'pbDisplayAttributes' )),
    COMMETHOD([], HRESULT, 'Discard',
              ( ['in'], c_ulong, 'dwValueTypes' )),
]
class SPRECORESULTTIMES(Structure):
    pass
class ISpPhraseAlt(ISpPhrase):
    _case_insensitive_ = True
    u'ISpPhraseAlt Interface'
    _iid_ = GUID('{8FCEBC98-4E49-4067-9C6C-D86A0E092E3D}')
    _idlflags_ = ['restricted']
class ISpStreamFormat(IStream):
    _case_insensitive_ = True
    u'ISpStreamFormat Interface'
    _iid_ = GUID('{BED530BE-2606-4F4D-A1C0-54C5CDA5566F}')
    _idlflags_ = ['restricted']
class SPSERIALIZEDRESULT(Structure):
    pass
class ISpNotifySource(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpNotifySource Interface'
    _iid_ = GUID('{5EFF4AEF-8487-11D2-961C-00C04F8EE628}')
    _idlflags_ = ['restricted']
class ISpEventSource(ISpNotifySource):
    _case_insensitive_ = True
    u'ISpEventSource Interface'
    _iid_ = GUID('{BE7A9CCE-5F9E-11D2-960F-00C04F8EE628}')
    _idlflags_ = ['restricted']
class ISpRecoContext(ISpEventSource):
    _case_insensitive_ = True
    u'ISpRecoContext Interface'
    _iid_ = GUID('{F740A62F-7C15-489E-8234-940A33D9272D}')
    _idlflags_ = ['restricted']
ISpRecoResult._methods_ = [
    COMMETHOD([], HRESULT, 'GetResultTimes',
              ( ['out'], POINTER(SPRECORESULTTIMES), 'pTimes' )),
    COMMETHOD([], HRESULT, 'GetAlternates',
              ( ['in'], c_ulong, 'ulStartElement' ),
              ( ['in'], c_ulong, 'cElements' ),
              ( ['in'], c_ulong, 'ulRequestCount' ),
              ( ['out'], POINTER(POINTER(ISpPhraseAlt)), 'ppPhrases' ),
              ( ['out'], POINTER(c_ulong), 'pcPhrasesReturned' )),
    COMMETHOD([], HRESULT, 'GetAudio',
              ( ['in'], c_ulong, 'ulStartElement' ),
              ( ['in'], c_ulong, 'cElements' ),
              ( ['out'], POINTER(POINTER(ISpStreamFormat)), 'ppStream' )),
    COMMETHOD([], HRESULT, 'SpeakAudio',
              ( ['in'], c_ulong, 'ulStartElement' ),
              ( ['in'], c_ulong, 'cElements' ),
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['out'], POINTER(c_ulong), 'pulStreamNumber' )),
    COMMETHOD([], HRESULT, 'Serialize',
              ( ['out'], POINTER(POINTER(SPSERIALIZEDRESULT)), 'ppCoMemSerializedResult' )),
    COMMETHOD([], HRESULT, 'ScaleAudio',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pAudioFormatId' ),
              ( ['in'], POINTER(WaveFormatEx), 'pWaveFormatEx' )),
    COMMETHOD([], HRESULT, 'GetRecoContext',
              ( ['out'], POINTER(POINTER(ISpRecoContext)), 'ppRecoContext' )),
]
SpeechTokenKeyUI = u'UI' # Constant BSTR

# values for enumeration 'DISPID_SpeechPhraseReplacements'
DISPID_SPRsCount = 1
DISPID_SPRsItem = 0
DISPID_SPRs_NewEnum = -4
DISPID_SpeechPhraseReplacements = c_int # enum

# values for enumeration 'SPRULESTATE'
SPRS_INACTIVE = 0
SPRS_ACTIVE = 1
SPRS_ACTIVE_WITH_AUTO_PAUSE = 3
SPRULESTATE = c_int # enum
class ISpStream(ISpStreamFormat):
    _case_insensitive_ = True
    u'ISpStream Interface'
    _iid_ = GUID('{12E3CCA9-7518-44C5-A5E7-BA5A79CB929E}')
    _idlflags_ = ['restricted']
ISpStreamFormat._methods_ = [
    COMMETHOD([], HRESULT, 'GetFormat',
              ( [], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pguidFormatId' ),
              ( [], POINTER(POINTER(WaveFormatEx)), 'ppCoMemWaveFormatEx' )),
]

# values for enumeration 'SPFILEMODE'
SPFM_OPEN_READONLY = 0
SPFM_OPEN_READWRITE = 1
SPFM_CREATE = 2
SPFM_CREATE_ALWAYS = 3
SPFM_NUM_MODES = 4
SPFILEMODE = c_int # enum
ISpStream._methods_ = [
    COMMETHOD([], HRESULT, 'SetBaseStream',
              ( [], POINTER(IStream), 'pStream' ),
              ( [], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'rguidFormat' ),
              ( [], POINTER(WaveFormatEx), 'pWaveFormatEx' )),
    COMMETHOD([], HRESULT, 'GetBaseStream',
              ( [], POINTER(POINTER(IStream)), 'ppStream' )),
    COMMETHOD([], HRESULT, 'BindToFile',
              ( [], POINTER(c_ushort), 'pszFileName' ),
              ( [], SPFILEMODE, 'eMode' ),
              ( [], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pFormatId' ),
              ( [], POINTER(WaveFormatEx), 'pWaveFormatEx' ),
              ( [], c_ulonglong, 'ullEventInterest' )),
    COMMETHOD([], HRESULT, 'Close'),
]

# values for enumeration 'SpeechWordPronounceable'
SWPUnknownWordUnpronounceable = 0
SWPUnknownWordPronounceable = 1
SWPKnownWordPronounceable = 2
SpeechWordPronounceable = c_int # enum
class ISpeechLexiconWords(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechLexiconWords Interface'
    _iid_ = GUID('{8D199862-415E-47D5-AC4F-FAA608B424E6}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechLexiconWord(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechLexiconWord Interface'
    _iid_ = GUID('{4E5B933C-C9BE-48ED-8842-1EE51BB1D4FF}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechLexiconWords._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechLexiconWord)), 'Word' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the tokens'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]
class ISpDataKey(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpDataKey Interface'
    _iid_ = GUID('{14056581-E16C-11D2-BB90-00C04F8EE6C0}')
    _idlflags_ = ['restricted']
class ISpObjectTokenCategory(ISpDataKey):
    _case_insensitive_ = True
    u'ISpObjectTokenCategory'
    _iid_ = GUID('{2D3D3845-39AF-4850-BBF9-40B49780011D}')
    _idlflags_ = ['restricted']
ISpDataKey._methods_ = [
    COMMETHOD([], HRESULT, 'SetData',
              ( [], POINTER(c_ushort), 'pszValueName' ),
              ( [], c_ulong, 'cbData' ),
              ( [], POINTER(c_ubyte), 'pData' )),
    COMMETHOD([], HRESULT, 'GetData',
              ( [], POINTER(c_ushort), 'pszValueName' ),
              ( [], POINTER(c_ulong), 'pcbData' ),
              ( [], POINTER(c_ubyte), 'pData' )),
    COMMETHOD([], HRESULT, 'SetStringValue',
              ( [], POINTER(c_ushort), 'pszValueName' ),
              ( [], POINTER(c_ushort), 'pszValue' )),
    COMMETHOD([], HRESULT, 'GetStringValue',
              ( [], POINTER(c_ushort), 'pszValueName' ),
              ( [], POINTER(POINTER(c_ushort)), 'ppszValue' )),
    COMMETHOD([], HRESULT, 'SetDWORD',
              ( [], POINTER(c_ushort), 'pszValueName' ),
              ( [], c_ulong, 'dwValue' )),
    COMMETHOD([], HRESULT, 'GetDWORD',
              ( [], POINTER(c_ushort), 'pszValueName' ),
              ( [], POINTER(c_ulong), 'pdwValue' )),
    COMMETHOD([], HRESULT, 'OpenKey',
              ( [], POINTER(c_ushort), 'pszSubKeyName' ),
              ( [], POINTER(POINTER(ISpDataKey)), 'ppSubKey' )),
    COMMETHOD([], HRESULT, 'CreateKey',
              ( [], POINTER(c_ushort), 'pszSubKey' ),
              ( [], POINTER(POINTER(ISpDataKey)), 'ppSubKey' )),
    COMMETHOD([], HRESULT, 'DeleteKey',
              ( [], POINTER(c_ushort), 'pszSubKey' )),
    COMMETHOD([], HRESULT, 'DeleteValue',
              ( [], POINTER(c_ushort), 'pszValueName' )),
    COMMETHOD([], HRESULT, 'EnumKeys',
              ( [], c_ulong, 'Index' ),
              ( [], POINTER(POINTER(c_ushort)), 'ppszSubKeyName' )),
    COMMETHOD([], HRESULT, 'EnumValues',
              ( [], c_ulong, 'Index' ),
              ( [], POINTER(POINTER(c_ushort)), 'ppszValueName' )),
]

# values for enumeration 'SPDATAKEYLOCATION'
SPDKL_DefaultLocation = 0
SPDKL_CurrentUser = 1
SPDKL_LocalMachine = 2
SPDKL_CurrentConfig = 5
SPDATAKEYLOCATION = c_int # enum
class IEnumSpObjectTokens(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'IEnumSpObjectTokens Interface'
    _iid_ = GUID('{06B64F9E-7FDA-11D2-B4F2-00C04F797396}')
    _idlflags_ = ['restricted']
    def __iter__(self):
        return self

    def next(self):
        item, fetched = self.Next(1)
        if fetched:
            return item
        raise StopIteration

    def __getitem__(self, index):
        self.Reset()
        self.Skip(index)
        item, fetched = self.Next(1)
        if fetched:
            return item
        raise IndexError, index

ISpObjectTokenCategory._methods_ = [
    COMMETHOD([], HRESULT, 'SetId',
              ( ['in'], POINTER(c_ushort), 'pszCategoryId' ),
              ( [], c_int, 'fCreateIfNotExist' )),
    COMMETHOD([], HRESULT, 'GetId',
              ( ['out'], POINTER(POINTER(c_ushort)), 'ppszCoMemCategoryId' )),
    COMMETHOD([], HRESULT, 'GetDataKey',
              ( [], SPDATAKEYLOCATION, 'spdkl' ),
              ( [], POINTER(POINTER(ISpDataKey)), 'ppDataKey' )),
    COMMETHOD([], HRESULT, 'EnumTokens',
              ( ['in'], WSTRING, 'pzsReqAttribs' ),
              ( ['in'], WSTRING, 'pszOptAttribs' ),
              ( ['out'], POINTER(POINTER(IEnumSpObjectTokens)), 'ppEnum' )),
    COMMETHOD([], HRESULT, 'SetDefaultTokenId',
              ( ['in'], POINTER(c_ushort), 'pszTokenId' )),
    COMMETHOD([], HRESULT, 'GetDefaultTokenId',
              ( ['out'], POINTER(POINTER(c_ushort)), 'ppszCoMemTokenId' )),
]

# values for enumeration 'SpeechRecoEvents'
SREStreamEnd = 1
SRESoundStart = 2
SRESoundEnd = 4
SREPhraseStart = 8
SRERecognition = 16
SREHypothesis = 32
SREBookmark = 64
SREPropertyNumChange = 128
SREPropertyStringChange = 256
SREFalseRecognition = 512
SREInterference = 1024
SRERequestUI = 2048
SREStateChange = 4096
SREAdaptation = 8192
SREStreamStart = 16384
SRERecoOtherContext = 32768
SREAudioLevel = 65536
SREPrivate = 262144
SREAllEvents = 393215
SpeechRecoEvents = c_int # enum

# values for enumeration 'DISPID_SpeechObjectTokenCategory'
DISPID_SOTCId = 1
DISPID_SOTCDefault = 2
DISPID_SOTCSetId = 3
DISPID_SOTCGetDataKey = 4
DISPID_SOTCEnumerateTokens = 5
DISPID_SpeechObjectTokenCategory = c_int # enum
class ISpeechPhraseElements(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseElements Interface'
    _iid_ = GUID('{0626B328-3478-467D-A0B3-D0853B93DDA3}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechPhraseElement(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseElement Interface'
    _iid_ = GUID('{E6176F96-E373-4801-B223-3B62C068C0B4}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechPhraseElements._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseElement)), 'Element' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the tokens'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]

# values for enumeration 'SpeechGrammarWordType'
SGDisplay = 0
SGLexical = 1
SGPronounciation = 2
SpeechGrammarWordType = c_int # enum

# values for enumeration 'DISPID_SpeechBaseStream'
DISPID_SBSFormat = 1
DISPID_SBSRead = 2
DISPID_SBSWrite = 3
DISPID_SBSSeek = 4
DISPID_SpeechBaseStream = c_int # enum

# values for enumeration 'DISPID_SpeechLexiconProns'
DISPID_SLPsCount = 1
DISPID_SLPsItem = 0
DISPID_SLPs_NewEnum = -4
DISPID_SpeechLexiconProns = c_int # enum

# values for enumeration 'DISPID_SpeechDataKey'
DISPID_SDKSetBinaryValue = 1
DISPID_SDKGetBinaryValue = 2
DISPID_SDKSetStringValue = 3
DISPID_SDKGetStringValue = 4
DISPID_SDKSetLongValue = 5
DISPID_SDKGetlongValue = 6
DISPID_SDKOpenKey = 7
DISPID_SDKCreateKey = 8
DISPID_SDKDeleteKey = 9
DISPID_SDKDeleteValue = 10
DISPID_SDKEnumKeys = 11
DISPID_SDKEnumValues = 12
DISPID_SpeechDataKey = c_int # enum
SpeechAudioFormatGUIDWave = u'{C31ADBAE-527F-4ff5-A230-F62BB61FF70C}' # Constant BSTR
SpeechMicTraining = u'MicTraining' # Constant BSTR
class SPAUDIOSTATUS(Structure):
    pass
SPAUDIOSTATUS._fields_ = [
    ('cbFreeBuffSpace', c_int),
    ('cbNonBlockingIO', c_ulong),
    ('State', _SPAUDIOSTATE),
    ('CurSeekPos', c_ulonglong),
    ('CurDevicePos', c_ulonglong),
    ('dwReserved1', c_ulong),
    ('dwReserved2', c_ulong),
]
assert sizeof(SPAUDIOSTATUS) == 40, sizeof(SPAUDIOSTATUS)
assert alignment(SPAUDIOSTATUS) == 8, alignment(SPAUDIOSTATUS)

# values for enumeration 'SpeechRuleAttributes'
SRATopLevel = 1
SRADefaultToActive = 2
SRAExport = 4
SRAImport = 8
SRAInterpreter = 16
SRADynamic = 32
SpeechRuleAttributes = c_int # enum
class ISpObjectWithToken(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpObjectWithToken Interface'
    _iid_ = GUID('{5B559F40-E952-11D2-BB91-00C04F8EE6C0}')
    _idlflags_ = ['restricted']
class ISpObjectToken(ISpDataKey):
    _case_insensitive_ = True
    u'ISpObjectToken Interface'
    _iid_ = GUID('{14056589-E16C-11D2-BB90-00C04F8EE6C0}')
    _idlflags_ = ['restricted']
ISpObjectWithToken._methods_ = [
    COMMETHOD([], HRESULT, 'SetObjectToken',
              ( [], POINTER(ISpObjectToken), 'pToken' )),
    COMMETHOD([], HRESULT, 'GetObjectToken',
              ( [], POINTER(POINTER(ISpObjectToken)), 'ppToken' )),
]
class ISpeechPhraseProperties(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseProperties Interface'
    _iid_ = GUID('{08166B47-102E-4B23-A599-BDB98DBFD1F4}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechPhraseProperty(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseProperty Interface'
    _iid_ = GUID('{CE563D48-961E-4732-A2E1-378A42B430BE}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechPhraseProperties._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseProperty)), 'Property' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the alternates'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]

# values for enumeration 'SPVPRIORITY'
SPVPRI_NORMAL = 0
SPVPRI_ALERT = 1
SPVPRI_OVER = 2
SPVPRIORITY = c_int # enum
class ISpeechCustomStream(ISpeechBaseStream):
    _case_insensitive_ = True
    u'ISpeechCustomStream Interface'
    _iid_ = GUID('{1A9E9F4F-104F-4DB8-A115-EFD7FD0C97AE}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechCustomStream._methods_ = [
    COMMETHOD([dispid(100), helpstring(u'BaseStream'), 'propget'], HRESULT, 'BaseStream',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'ppUnkStream' )),
    COMMETHOD([dispid(100), helpstring(u'BaseStream'), 'propputref'], HRESULT, 'BaseStream',
              ( ['in'], POINTER(IUnknown), 'ppUnkStream' )),
]

# values for enumeration 'DISPID_SpeechPhraseReplacement'
DISPID_SPRDisplayAttributes = 1
DISPID_SPRText = 2
DISPID_SPRFirstElement = 3
DISPID_SPRNumberOfElements = 4
DISPID_SpeechPhraseReplacement = c_int # enum
SpeechPropertyLowConfidenceThreshold = u'LowConfidenceThreshold' # Constant BSTR
class SPRECOGNIZERSTATUS(Structure):
    pass
SPRECOGNIZERSTATUS._fields_ = [
    ('AudioStatus', SPAUDIOSTATUS),
    ('ullRecognitionStreamPos', c_ulonglong),
    ('ulStreamNumber', c_ulong),
    ('ulNumActive', c_ulong),
    ('ClsidEngine', comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
    ('cLangIDs', c_ulong),
    ('aLangID', c_ushort * 20),
    ('dwReserved1', c_ulong),
    ('dwReserved2', c_ulong),
]
assert sizeof(SPRECOGNIZERSTATUS) == 128, sizeof(SPRECOGNIZERSTATUS)
assert alignment(SPRECOGNIZERSTATUS) == 8, alignment(SPRECOGNIZERSTATUS)
class SpStreamFormatConverter(CoClass):
    u'FormatConverter Class'
    _reg_clsid_ = GUID('{7013943A-E2EC-11D2-A086-00C04F8EF9B5}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpStreamFormatConverter(ISpStreamFormat):
    _case_insensitive_ = True
    u'ISpStreamFormatConverter Interface'
    _iid_ = GUID('{678A932C-EA71-4446-9B41-78FDA6280A29}')
    _idlflags_ = ['restricted']
SpStreamFormatConverter._com_interfaces_ = [ISpStreamFormatConverter]

class ISpLexicon(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpLexicon Interface'
    _iid_ = GUID('{DA41A7C2-5383-4DB2-916B-6C1719E3DB58}')
    _idlflags_ = ['restricted']

# values for enumeration 'SPPARTOFSPEECH'
SPPS_NotOverriden = -1
SPPS_Unknown = 0
SPPS_Noun = 4096
SPPS_Verb = 8192
SPPS_Modifier = 12288
SPPS_Function = 16384
SPPS_Interjection = 20480
SPPARTOFSPEECH = c_int # enum
ISpLexicon._methods_ = [
    COMMETHOD([], HRESULT, 'GetPronunciations',
              ( ['in'], POINTER(c_ushort), 'pszWord' ),
              ( ['in'], c_ushort, 'LangId' ),
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['in', 'out'], POINTER(SPWORDPRONUNCIATIONLIST), 'pWordPronunciationList' )),
    COMMETHOD([], HRESULT, 'AddPronunciation',
              ( ['in'], POINTER(c_ushort), 'pszWord' ),
              ( ['in'], c_ushort, 'LangId' ),
              ( ['in'], SPPARTOFSPEECH, 'ePartOfSpeech' ),
              ( ['in'], POINTER(c_ushort), 'pszPronunciation' )),
    COMMETHOD([], HRESULT, 'RemovePronunciation',
              ( ['in'], POINTER(c_ushort), 'pszWord' ),
              ( ['in'], c_ushort, 'LangId' ),
              ( ['in'], SPPARTOFSPEECH, 'ePartOfSpeech' ),
              ( ['in'], POINTER(c_ushort), 'pszPronunciation' )),
    COMMETHOD([], HRESULT, 'GetGeneration',
              ( [], POINTER(c_ulong), 'pdwGeneration' )),
    COMMETHOD([], HRESULT, 'GetGenerationChange',
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['in', 'out'], POINTER(c_ulong), 'pdwGeneration' ),
              ( ['in', 'out'], POINTER(SPWORDLIST), 'pWordList' )),
    COMMETHOD([], HRESULT, 'GetWords',
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['in', 'out'], POINTER(c_ulong), 'pdwGeneration' ),
              ( ['in', 'out'], POINTER(c_ulong), 'pdwCookie' ),
              ( ['in', 'out'], POINTER(SPWORDLIST), 'pWordList' )),
]

# values for enumeration 'SPRECOSTATE'
SPRST_INACTIVE = 0
SPRST_ACTIVE = 1
SPRST_ACTIVE_ALWAYS = 2
SPRST_INACTIVE_WITH_PURGE = 3
SPRST_NUM_STATES = 4
SPRECOSTATE = c_int # enum

# values for enumeration 'SPGRAMMARSTATE'
SPGS_DISABLED = 0
SPGS_ENABLED = 1
SPGS_EXCLUSIVE = 3
SPGRAMMARSTATE = c_int # enum
ISpPhraseAlt._methods_ = [
    COMMETHOD([], HRESULT, 'GetAltInfo',
              ( [], POINTER(POINTER(ISpPhrase)), 'ppParent' ),
              ( [], POINTER(c_ulong), 'pulStartElementInParent' ),
              ( [], POINTER(c_ulong), 'pcElementsInParent' ),
              ( [], POINTER(c_ulong), 'pcElementsInAlt' )),
    COMMETHOD([], HRESULT, 'Commit'),
]
class _FILETIME(Structure):
    pass
_FILETIME._fields_ = [
    ('dwLowDateTime', c_ulong),
    ('dwHighDateTime', c_ulong),
]
assert sizeof(_FILETIME) == 8, sizeof(_FILETIME)
assert alignment(_FILETIME) == 4, alignment(_FILETIME)
SPRECORESULTTIMES._fields_ = [
    ('ftStreamTime', _FILETIME),
    ('ullLength', c_ulonglong),
    ('dwTickCount', c_ulong),
    ('ullStart', c_ulonglong),
]
assert sizeof(SPRECORESULTTIMES) == 32, sizeof(SPRECORESULTTIMES)
assert alignment(SPRECORESULTTIMES) == 8, alignment(SPRECORESULTTIMES)
class SpObjectTokenCategory(CoClass):
    u'SpObjectTokenCategory Class'
    _reg_clsid_ = GUID('{A910187F-0C7A-45AC-92CC-59EDAFB77B53}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpeechObjectTokenCategory(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechObjectTokenCategory Interface'
    _iid_ = GUID('{CA7EAC50-2D01-4145-86D4-5AE7D70F4469}')
    _idlflags_ = ['dual', 'oleautomation']
SpObjectTokenCategory._com_interfaces_ = [ISpeechObjectTokenCategory, ISpObjectTokenCategory]

class SpInProcRecoContext(CoClass):
    u'SpInProcRecoContext Class'
    _reg_clsid_ = GUID('{73AD6842-ACE0-45E8-A4DD-8795881A2C2A}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class _ISpeechRecoContextEvents(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{7B8FCB42-0E9D-4F00-A048-7B04D6179D3D}')
    _idlflags_ = []
    _methods_ = []
SpInProcRecoContext._com_interfaces_ = [ISpeechRecoContext, ISpRecoContext]
SpInProcRecoContext._outgoing_interfaces_ = [_ISpeechRecoContextEvents]

SpeechCategoryAudioOut = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\AudioOutput' # Constant BSTR

# values for enumeration 'DISPID_SpeechWaveFormatEx'
DISPID_SWFEFormatTag = 1
DISPID_SWFEChannels = 2
DISPID_SWFESamplesPerSec = 3
DISPID_SWFEAvgBytesPerSec = 4
DISPID_SWFEBlockAlign = 5
DISPID_SWFEBitsPerSample = 6
DISPID_SWFEExtraData = 7
DISPID_SpeechWaveFormatEx = c_int # enum
SpeechGrammarTagDictation = u'*' # Constant BSTR
SpeechTokenValueCLSID = u'CLSID' # Constant BSTR

# values for enumeration 'DISPID_SpeechLexiconPronunciation'
DISPID_SLPType = 1
DISPID_SLPLangId = 2
DISPID_SLPPartOfSpeech = 3
DISPID_SLPPhoneIds = 4
DISPID_SLPSymbolic = 5
DISPID_SpeechLexiconPronunciation = c_int # enum
class ISpGrammarBuilder(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpGrammarBuilder Interface'
    _iid_ = GUID('{8137828F-591A-4A42-BE58-49EA7EBAAC68}')
    _idlflags_ = ['restricted']
class ISpRecoGrammar(ISpGrammarBuilder):
    _case_insensitive_ = True
    u'ISpRecoGrammar Interface'
    _iid_ = GUID('{2177DB29-7F45-47D0-8554-067E91C80502}')
    _idlflags_ = ['restricted']
class tagSPPROPERTYINFO(Structure):
    pass
SPPROPERTYINFO = tagSPPROPERTYINFO
ISpGrammarBuilder._methods_ = [
    COMMETHOD([], HRESULT, 'ResetGrammar',
              ( ['in'], c_ushort, 'NewLanguage' )),
    COMMETHOD([], HRESULT, 'GetRule',
              ( ['in'], POINTER(c_ushort), 'pszRuleName' ),
              ( ['in'], c_ulong, 'dwRuleId' ),
              ( ['in'], c_ulong, 'dwAttributes' ),
              ( ['in'], c_int, 'fCreateIfNotExist' ),
              ( ['out'], POINTER(c_void_p), 'phInitialState' )),
    COMMETHOD([], HRESULT, 'ClearRule',
              ( [], c_void_p, 'hState' )),
    COMMETHOD([], HRESULT, 'CreateNewState',
              ( [], c_void_p, 'hState' ),
              ( [], POINTER(c_void_p), 'phState' )),
    COMMETHOD([], HRESULT, 'AddWordTransition',
              ( [], c_void_p, 'hFromState' ),
              ( [], c_void_p, 'hToState' ),
              ( [], POINTER(c_ushort), 'psz' ),
              ( [], POINTER(c_ushort), 'pszSeparators' ),
              ( [], SPGRAMMARWORDTYPE, 'eWordType' ),
              ( [], c_float, 'Weight' ),
              ( [], POINTER(SPPROPERTYINFO), 'pPropInfo' )),
    COMMETHOD([], HRESULT, 'AddRuleTransition',
              ( [], c_void_p, 'hFromState' ),
              ( [], c_void_p, 'hToState' ),
              ( [], c_void_p, 'hRule' ),
              ( [], c_float, 'Weight' ),
              ( [], POINTER(SPPROPERTYINFO), 'pPropInfo' )),
    COMMETHOD([], HRESULT, 'AddResource',
              ( ['in'], c_void_p, 'hRuleState' ),
              ( ['in'], POINTER(c_ushort), 'pszResourceName' ),
              ( ['in'], POINTER(c_ushort), 'pszResourceValue' )),
    COMMETHOD([], HRESULT, 'Commit',
              ( [], c_ulong, 'dwReserved' )),
]

# values for enumeration 'SPLOADOPTIONS'
SPLO_STATIC = 0
SPLO_DYNAMIC = 1
SPLOADOPTIONS = c_int # enum
class SPBINARYGRAMMAR(Structure):
    pass
class tagSPTEXTSELECTIONINFO(Structure):
    pass
SPTEXTSELECTIONINFO = tagSPTEXTSELECTIONINFO

# values for enumeration 'SPWORDPRONOUNCEABLE'
SPWP_UNKNOWN_WORD_UNPRONOUNCEABLE = 0
SPWP_UNKNOWN_WORD_PRONOUNCEABLE = 1
SPWP_KNOWN_WORD_PRONOUNCEABLE = 2
SPWORDPRONOUNCEABLE = c_int # enum
ISpRecoGrammar._methods_ = [
    COMMETHOD([], HRESULT, 'GetGrammarId',
              ( ['out'], POINTER(c_ulonglong), 'pullGrammarId' )),
    COMMETHOD([], HRESULT, 'GetRecoContext',
              ( ['out'], POINTER(POINTER(ISpRecoContext)), 'ppRecoCtxt' )),
    COMMETHOD([], HRESULT, 'LoadCmdFromFile',
              ( ['in'], WSTRING, 'pszFileName' ),
              ( ['in'], SPLOADOPTIONS, 'Options' )),
    COMMETHOD([], HRESULT, 'LoadCmdFromObject',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'rcid' ),
              ( ['in'], WSTRING, 'pszGrammarName' ),
              ( ['in'], SPLOADOPTIONS, 'Options' )),
    COMMETHOD([], HRESULT, 'LoadCmdFromResource',
              ( ['in'], c_void_p, 'hModule' ),
              ( ['in'], WSTRING, 'pszResourceName' ),
              ( ['in'], WSTRING, 'pszResourceType' ),
              ( ['in'], c_ushort, 'wLanguage' ),
              ( ['in'], SPLOADOPTIONS, 'Options' )),
    COMMETHOD([], HRESULT, 'LoadCmdFromMemory',
              ( ['in'], POINTER(SPBINARYGRAMMAR), 'pGrammar' ),
              ( ['in'], SPLOADOPTIONS, 'Options' )),
    COMMETHOD([], HRESULT, 'LoadCmdFromProprietaryGrammar',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'rguidParam' ),
              ( ['in'], WSTRING, 'pszStringParam' ),
              ( ['in'], c_void_p, 'pvDataPrarm' ),
              ( ['in'], c_ulong, 'cbDataSize' ),
              ( ['in'], SPLOADOPTIONS, 'Options' )),
    COMMETHOD([], HRESULT, 'SetRuleState',
              ( ['in'], WSTRING, 'pszName' ),
              ( [], c_void_p, 'pReserved' ),
              ( ['in'], SPRULESTATE, 'NewState' )),
    COMMETHOD([], HRESULT, 'SetRuleIdState',
              ( ['in'], c_ulong, 'ulRuleId' ),
              ( ['in'], SPRULESTATE, 'NewState' )),
    COMMETHOD([], HRESULT, 'LoadDictation',
              ( ['in'], WSTRING, 'pszTopicName' ),
              ( ['in'], SPLOADOPTIONS, 'Options' )),
    COMMETHOD([], HRESULT, 'UnloadDictation'),
    COMMETHOD([], HRESULT, 'SetDictationState',
              ( ['in'], SPRULESTATE, 'NewState' )),
    COMMETHOD([], HRESULT, 'SetWordSequenceData',
              ( ['in'], POINTER(c_ushort), 'pText' ),
              ( ['in'], c_ulong, 'cchText' ),
              ( ['in'], POINTER(SPTEXTSELECTIONINFO), 'pInfo' )),
    COMMETHOD([], HRESULT, 'SetTextSelection',
              ( ['in'], POINTER(SPTEXTSELECTIONINFO), 'pInfo' )),
    COMMETHOD([], HRESULT, 'IsPronounceable',
              ( ['in'], WSTRING, 'pszWord' ),
              ( ['out'], POINTER(SPWORDPRONOUNCEABLE), 'pWordPronounceable' )),
    COMMETHOD([], HRESULT, 'SetGrammarState',
              ( ['in'], SPGRAMMARSTATE, 'eGrammarState' )),
    COMMETHOD([], HRESULT, 'SaveCmd',
              ( ['in'], POINTER(IStream), 'pStream' ),
              ( ['out', 'optional'], POINTER(POINTER(c_ushort)), 'ppszCoMemErrorText' )),
    COMMETHOD([], HRESULT, 'GetGrammarState',
              ( ['out'], POINTER(SPGRAMMARSTATE), 'peGrammarState' )),
]
class ISpeechVoice(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechVoice Interface'
    _iid_ = GUID('{269316D8-57BD-11D2-9EEE-00C04F797396}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechVoiceStatus(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechVoiceStatus Interface'
    _iid_ = GUID('{8BE47B07-57F6-11D2-9EEE-00C04F797396}')
    _idlflags_ = ['dual', 'oleautomation']

# values for enumeration 'SpeechVoiceEvents'
SVEStartInputStream = 2
SVEEndInputStream = 4
SVEVoiceChange = 8
SVEBookmark = 16
SVEWordBoundary = 32
SVEPhoneme = 64
SVESentenceBoundary = 128
SVEViseme = 256
SVEAudioLevel = 512
SVEPrivate = 32768
SVEAllEvents = 33790
SpeechVoiceEvents = c_int # enum

# values for enumeration 'SpeechVoicePriority'
SVPNormal = 0
SVPAlert = 1
SVPOver = 2
SpeechVoicePriority = c_int # enum

# values for enumeration 'SpeechVoiceSpeakFlags'
SVSFDefault = 0
SVSFlagsAsync = 1
SVSFPurgeBeforeSpeak = 2
SVSFIsFilename = 4
SVSFIsXML = 8
SVSFIsNotXML = 16
SVSFPersistXML = 32
SVSFNLPSpeakPunc = 64
SVSFNLPMask = 64
SVSFVoiceMask = 127
SVSFUnusedFlags = -128
SpeechVoiceSpeakFlags = c_int # enum
ISpeechVoice._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Status'), 'propget'], HRESULT, 'Status',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechVoiceStatus)), 'Status' )),
    COMMETHOD([dispid(2), helpstring(u'Voice'), 'propget'], HRESULT, 'Voice',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectToken)), 'Voice' )),
    COMMETHOD([dispid(2), helpstring(u'Voice'), 'propputref'], HRESULT, 'Voice',
              ( ['in'], POINTER(ISpeechObjectToken), 'Voice' )),
    COMMETHOD([dispid(3), helpstring(u'Gets the audio output object'), 'propget'], HRESULT, 'AudioOutput',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectToken)), 'AudioOutput' )),
    COMMETHOD([dispid(3), helpstring(u'Gets the audio output object'), 'propputref'], HRESULT, 'AudioOutput',
              ( ['in'], POINTER(ISpeechObjectToken), 'AudioOutput' )),
    COMMETHOD([dispid(4), helpstring(u'Gets the audio output stream'), 'propget'], HRESULT, 'AudioOutputStream',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechBaseStream)), 'AudioOutputStream' )),
    COMMETHOD([dispid(4), helpstring(u'Gets the audio output stream'), 'propputref'], HRESULT, 'AudioOutputStream',
              ( ['in'], POINTER(ISpeechBaseStream), 'AudioOutputStream' )),
    COMMETHOD([dispid(5), helpstring(u'Rate'), 'propget'], HRESULT, 'Rate',
              ( ['retval', 'out'], POINTER(c_int), 'Rate' )),
    COMMETHOD([dispid(5), helpstring(u'Rate'), 'propput'], HRESULT, 'Rate',
              ( ['in'], c_int, 'Rate' )),
    COMMETHOD([dispid(6), helpstring(u'Volume'), 'propget'], HRESULT, 'Volume',
              ( ['retval', 'out'], POINTER(c_int), 'Volume' )),
    COMMETHOD([dispid(6), helpstring(u'Volume'), 'propput'], HRESULT, 'Volume',
              ( ['in'], c_int, 'Volume' )),
    COMMETHOD([dispid(7), helpstring(u'AllowAudioOutputFormatChangesOnNextSet'), 'hidden', 'propput'], HRESULT, 'AllowAudioOutputFormatChangesOnNextSet',
              ( ['in'], VARIANT_BOOL, 'Allow' )),
    COMMETHOD([dispid(7), helpstring(u'AllowAudioOutputFormatChangesOnNextSet'), 'hidden', 'propget'], HRESULT, 'AllowAudioOutputFormatChangesOnNextSet',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Allow' )),
    COMMETHOD([dispid(8), helpstring(u'EventInterests'), 'propget'], HRESULT, 'EventInterests',
              ( ['retval', 'out'], POINTER(SpeechVoiceEvents), 'EventInterestFlags' )),
    COMMETHOD([dispid(8), helpstring(u'EventInterests'), 'propput'], HRESULT, 'EventInterests',
              ( ['in'], SpeechVoiceEvents, 'EventInterestFlags' )),
    COMMETHOD([dispid(9), helpstring(u'Priority'), 'propput'], HRESULT, 'Priority',
              ( ['in'], SpeechVoicePriority, 'Priority' )),
    COMMETHOD([dispid(9), helpstring(u'Priority'), 'propget'], HRESULT, 'Priority',
              ( ['retval', 'out'], POINTER(SpeechVoicePriority), 'Priority' )),
    COMMETHOD([dispid(10), helpstring(u'AlertBoundary'), 'propput'], HRESULT, 'AlertBoundary',
              ( ['in'], SpeechVoiceEvents, 'Boundary' )),
    COMMETHOD([dispid(10), helpstring(u'AlertBoundary'), 'propget'], HRESULT, 'AlertBoundary',
              ( ['retval', 'out'], POINTER(SpeechVoiceEvents), 'Boundary' )),
    COMMETHOD([dispid(11), helpstring(u'SyncSpeakTimeout'), 'propput'], HRESULT, 'SynchronousSpeakTimeout',
              ( ['in'], c_int, 'msTimeout' )),
    COMMETHOD([dispid(11), helpstring(u'SyncSpeakTimeout'), 'propget'], HRESULT, 'SynchronousSpeakTimeout',
              ( ['retval', 'out'], POINTER(c_int), 'msTimeout' )),
    COMMETHOD([dispid(12), helpstring(u'Speak')], HRESULT, 'Speak',
              ( ['in'], BSTR, 'Text' ),
              ( ['in', 'optional'], SpeechVoiceSpeakFlags, 'Flags', 0 ),
              ( ['retval', 'out'], POINTER(c_int), 'StreamNumber' )),
    COMMETHOD([dispid(13), helpstring(u'SpeakStream')], HRESULT, 'SpeakStream',
              ( ['in'], POINTER(ISpeechBaseStream), 'Stream' ),
              ( ['in', 'optional'], SpeechVoiceSpeakFlags, 'Flags', 0 ),
              ( ['retval', 'out'], POINTER(c_int), 'StreamNumber' )),
    COMMETHOD([dispid(14), helpstring(u'Pauses the voices rendering.')], HRESULT, 'Pause'),
    COMMETHOD([dispid(15), helpstring(u'Resumes the voices rendering.')], HRESULT, 'Resume'),
    COMMETHOD([dispid(16), helpstring(u'Skips rendering the specified number of items.')], HRESULT, 'Skip',
              ( ['in'], BSTR, 'Type' ),
              ( ['in'], c_int, 'NumItems' ),
              ( ['retval', 'out'], POINTER(c_int), 'NumSkipped' )),
    COMMETHOD([dispid(17), helpstring(u'GetVoices')], HRESULT, 'GetVoices',
              ( ['in', 'optional'], BSTR, 'RequiredAttributes', u'' ),
              ( ['in', 'optional'], BSTR, 'OptionalAttributes', u'' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectTokens)), 'ObjectTokens' )),
    COMMETHOD([dispid(18), helpstring(u'GetAudioOutputs')], HRESULT, 'GetAudioOutputs',
              ( ['in', 'optional'], BSTR, 'RequiredAttributes', u'' ),
              ( ['in', 'optional'], BSTR, 'OptionalAttributes', u'' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectTokens)), 'ObjectTokens' )),
    COMMETHOD([dispid(19), helpstring(u'WaitUntilDone')], HRESULT, 'WaitUntilDone',
              ( ['in'], c_int, 'msTimeout' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Done' )),
    COMMETHOD([dispid(20), helpstring(u'SpeakCompleteEvent'), 'hidden'], HRESULT, 'SpeakCompleteEvent',
              ( ['retval', 'out'], POINTER(c_int), 'Handle' )),
    COMMETHOD([dispid(21), helpstring(u'IsUISupported')], HRESULT, 'IsUISupported',
              ( ['in'], BSTR, 'TypeOfUI' ),
              ( ['in', 'optional'], POINTER(VARIANT), 'ExtraData', u'' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Supported' )),
    COMMETHOD([dispid(22), helpstring(u'DisplayUI')], HRESULT, 'DisplayUI',
              ( ['in'], c_int, 'hWndParent' ),
              ( ['in'], BSTR, 'Title' ),
              ( ['in'], BSTR, 'TypeOfUI' ),
              ( ['in', 'optional'], POINTER(VARIANT), 'ExtraData', u'' )),
]
SPAUDIOSTATE = _SPAUDIOSTATE
class ISpeechGrammarRuleStateTransitions(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechGrammarRuleStateTransitions Interface'
    _iid_ = GUID('{EABCE657-75BC-44A2-AA7F-C56476742963}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechGrammarRuleStateTransition(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechGrammarRuleStateTransition Interface'
    _iid_ = GUID('{CAFD1DB1-41D1-4A06-9863-E2E81DA17A9A}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechGrammarRuleStateTransitions._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRuleStateTransition)), 'Transition' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the transitions'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]
class SpUnCompressedLexicon(CoClass):
    u'SpUnCompressedLexicon Class'
    _reg_clsid_ = GUID('{C9E37C15-DF92-4727-85D6-72E5EEB6995A}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpeechLexicon(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechLexicon Interface'
    _iid_ = GUID('{3DA7627A-C7AE-4B23-8708-638C50362C25}')
    _idlflags_ = ['dual', 'oleautomation']
SpUnCompressedLexicon._com_interfaces_ = [ISpeechLexicon, ISpLexicon, ISpObjectWithToken]

class ISpeechRecoResultTimes(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechRecoResultTimes Interface'
    _iid_ = GUID('{62B3B8FB-F6E7-41BE-BDCB-056B1C29EFC0}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechRecoResultTimes._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'StreamTime'), 'propget'], HRESULT, 'StreamTime',
              ( ['retval', 'out'], POINTER(VARIANT), 'Time' )),
    COMMETHOD([dispid(2), helpstring(u'Length'), 'propget'], HRESULT, 'Length',
              ( ['retval', 'out'], POINTER(VARIANT), 'Length' )),
    COMMETHOD([dispid(3), helpstring(u'TickCount'), 'propget'], HRESULT, 'TickCount',
              ( ['retval', 'out'], POINTER(c_int), 'TickCount' )),
    COMMETHOD([dispid(4), helpstring(u'Start'), 'propget'], HRESULT, 'OffsetFromStart',
              ( ['retval', 'out'], POINTER(VARIANT), 'OffsetFromStart' )),
]

# values for enumeration 'SPWORDTYPE'
eWORDTYPE_ADDED = 1
eWORDTYPE_DELETED = 2
SPWORDTYPE = c_int # enum
Speech_Max_Word_Length = 128 # Constant c_int

# values for enumeration 'DISPID_SpeechAudioBufferInfo'
DISPID_SABIMinNotification = 1
DISPID_SABIBufferSize = 2
DISPID_SABIEventBias = 3
DISPID_SpeechAudioBufferInfo = c_int # enum
class SpMMAudioOut(CoClass):
    u'SpMMAudioOut Class'
    _reg_clsid_ = GUID('{A8C680EB-3D32-11D2-9EE7-00C04F797396}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpeechAudio(ISpeechBaseStream):
    _case_insensitive_ = True
    u'ISpeechAudio Interface'
    _iid_ = GUID('{CFF8E175-019E-11D3-A08E-00C04F8EF9B5}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechMMSysAudio(ISpeechAudio):
    _case_insensitive_ = True
    u'ISpeechMMSysAudio Interface'
    _iid_ = GUID('{3C76AF6D-1FD7-4831-81D1-3B71D5A13C44}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpEventSink(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpEventSink Interface'
    _iid_ = GUID('{BE7A9CC9-5F9E-11D2-960F-00C04F8EE628}')
    _idlflags_ = ['restricted']
class ISpAudio(ISpStreamFormat):
    _case_insensitive_ = True
    u'ISpAudio Interface'
    _iid_ = GUID('{C05C768F-FAE8-4EC2-8E07-338321C12452}')
    _idlflags_ = ['restricted']
class ISpMMSysAudio(ISpAudio):
    _case_insensitive_ = True
    u'ISpMMSysAudio Interface'
    _iid_ = GUID('{15806F6E-1D70-4B48-98E6-3B1A007509AB}')
    _idlflags_ = ['restricted']
SpMMAudioOut._com_interfaces_ = [ISpeechMMSysAudio, ISpEventSource, ISpEventSink, ISpObjectWithToken, ISpMMSysAudio]


# values for enumeration 'SPLEXICONTYPE'
eLEXTYPE_USER = 1
eLEXTYPE_APP = 2
eLEXTYPE_RESERVED1 = 4
eLEXTYPE_RESERVED2 = 8
eLEXTYPE_RESERVED3 = 16
eLEXTYPE_RESERVED4 = 32
eLEXTYPE_RESERVED5 = 64
eLEXTYPE_RESERVED6 = 128
eLEXTYPE_RESERVED7 = 256
eLEXTYPE_RESERVED8 = 512
eLEXTYPE_RESERVED9 = 1024
eLEXTYPE_RESERVED10 = 2048
eLEXTYPE_PRIVATE1 = 4096
eLEXTYPE_PRIVATE2 = 8192
eLEXTYPE_PRIVATE3 = 16384
eLEXTYPE_PRIVATE4 = 32768
eLEXTYPE_PRIVATE5 = 65536
eLEXTYPE_PRIVATE6 = 131072
eLEXTYPE_PRIVATE7 = 262144
eLEXTYPE_PRIVATE8 = 524288
eLEXTYPE_PRIVATE9 = 1048576
eLEXTYPE_PRIVATE10 = 2097152
eLEXTYPE_PRIVATE11 = 4194304
eLEXTYPE_PRIVATE12 = 8388608
eLEXTYPE_PRIVATE13 = 16777216
eLEXTYPE_PRIVATE14 = 33554432
eLEXTYPE_PRIVATE15 = 67108864
eLEXTYPE_PRIVATE16 = 134217728
eLEXTYPE_PRIVATE17 = 268435456
eLEXTYPE_PRIVATE18 = 536870912
eLEXTYPE_PRIVATE19 = 1073741824
eLEXTYPE_PRIVATE20 = -2147483648
SPLEXICONTYPE = c_int # enum

# values for enumeration 'DISPID_SpeechPhraseElement'
DISPID_SPEAudioTimeOffset = 1
DISPID_SPEAudioSizeTime = 2
DISPID_SPEAudioStreamOffset = 3
DISPID_SPEAudioSizeBytes = 4
DISPID_SPERetainedStreamOffset = 5
DISPID_SPERetainedSizeBytes = 6
DISPID_SPEDisplayText = 7
DISPID_SPELexicalForm = 8
DISPID_SPEPronunciation = 9
DISPID_SPEDisplayAttributes = 10
DISPID_SPERequiredConfidence = 11
DISPID_SPEActualConfidence = 12
DISPID_SPEEngineConfidence = 13
DISPID_SpeechPhraseElement = c_int # enum
class SpNullPhoneConverter(CoClass):
    u'SpNullPhoneConverter Class'
    _reg_clsid_ = GUID('{455F24E9-7396-4A16-9715-7C0FDBE3EFE3}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpPhoneConverter(ISpObjectWithToken):
    _case_insensitive_ = True
    u'ISpPhoneConverter Interface'
    _iid_ = GUID('{8445C581-0CAC-4A38-ABFE-9B2CE2826455}')
    _idlflags_ = ['restricted']
SpNullPhoneConverter._com_interfaces_ = [ISpPhoneConverter]

class SpPhoneConverter(CoClass):
    u'SpPhoneConverter Class'
    _reg_clsid_ = GUID('{9185F743-1143-4C28-86B5-BFF14F20E5C8}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpeechPhoneConverter(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhoneConverter Interface'
    _iid_ = GUID('{C3E4F353-433F-43D6-89A1-6A62A7054C3D}')
    _idlflags_ = ['dual', 'oleautomation']
SpPhoneConverter._com_interfaces_ = [ISpeechPhoneConverter, ISpPhoneConverter]

class ISpeechPhraseReplacements(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseReplacements Interface'
    _iid_ = GUID('{38BC662F-2257-4525-959E-2069D2596C05}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechPhraseReplacement(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseReplacement Interface'
    _iid_ = GUID('{2890A410-53A7-4FB5-94EC-06D4998E3D02}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechPhraseReplacements._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseReplacement)), 'Reps' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the tokens'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]
class SpFileStream(CoClass):
    u'SpFileStream Class'
    _reg_clsid_ = GUID('{947812B3-2AE1-4644-BA86-9E90DED7EC91}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpFileStream._com_interfaces_ = [ISpeechFileStream, ISpStream]

SpeechPropertyHighConfidenceThreshold = u'HighConfidenceThreshold' # Constant BSTR

# values for enumeration 'DISPID_SpeechAudio'
DISPID_SAStatus = 200
DISPID_SABufferInfo = 201
DISPID_SADefaultFormat = 202
DISPID_SAVolume = 203
DISPID_SABufferNotifySize = 204
DISPID_SAEventHandle = 205
DISPID_SASetState = 206
DISPID_SpeechAudio = c_int # enum
SpeechPropertyResponseSpeed = u'ResponseSpeed' # Constant BSTR
class SpRecPlayAudio(CoClass):
    u'SpRecPlayAudio Class'
    _reg_clsid_ = GUID('{FEE225FC-7AFD-45E9-95D0-5A318079D911}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpRecPlayAudio._com_interfaces_ = [ISpObjectWithToken, ISpAudio]


# values for enumeration 'SpeechGrammarRuleStateTransitionType'
SGRSTTEpsilon = 0
SGRSTTWord = 1
SGRSTTRule = 2
SGRSTTDictation = 3
SGRSTTWildcard = 4
SGRSTTTextBuffer = 5
SpeechGrammarRuleStateTransitionType = c_int # enum

# values for enumeration 'SpeechEngineConfidence'
SECLowConfidence = -1
SECNormalConfidence = 0
SECHighConfidence = 1
SpeechEngineConfidence = c_int # enum
ISpeechPhraseProperty._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Name'), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'Name' )),
    COMMETHOD([dispid(2), helpstring(u'Id'), 'propget'], HRESULT, 'Id',
              ( ['retval', 'out'], POINTER(c_int), 'Id' )),
    COMMETHOD([dispid(3), helpstring(u'Value'), 'propget'], HRESULT, 'Value',
              ( ['retval', 'out'], POINTER(VARIANT), 'Value' )),
    COMMETHOD([dispid(4), helpstring(u'FirstElement'), 'propget'], HRESULT, 'FirstElement',
              ( ['retval', 'out'], POINTER(c_int), 'FirstElement' )),
    COMMETHOD([dispid(5), helpstring(u'NumberOfElements'), 'propget'], HRESULT, 'NumberOfElements',
              ( ['retval', 'out'], POINTER(c_int), 'NumberOfElements' )),
    COMMETHOD([dispid(6), helpstring(u'EngineConfidence'), 'propget'], HRESULT, 'EngineConfidence',
              ( ['retval', 'out'], POINTER(c_float), 'Confidence' )),
    COMMETHOD([dispid(7), helpstring(u'Confidence'), 'propget'], HRESULT, 'Confidence',
              ( ['retval', 'out'], POINTER(SpeechEngineConfidence), 'Confidence' )),
    COMMETHOD([dispid(8), helpstring(u'Parent'), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseProperty)), 'ParentProperty' )),
    COMMETHOD([dispid(9), helpstring(u'Children'), 'propget'], HRESULT, 'Children',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseProperties)), 'Children' )),
]
SpeechTokenKeyFiles = u'Files' # Constant BSTR

# values for enumeration 'DISPID_SpeechRecoContext'
DISPID_SRCRecognizer = 1
DISPID_SRCAudioInInterferenceStatus = 2
DISPID_SRCRequestedUIType = 3
DISPID_SRCVoice = 4
DISPID_SRAllowVoiceFormatMatchingOnNextSet = 5
DISPID_SRCVoicePurgeEvent = 6
DISPID_SRCEventInterests = 7
DISPID_SRCCmdMaxAlternates = 8
DISPID_SRCState = 9
DISPID_SRCRetainedAudio = 10
DISPID_SRCRetainedAudioFormat = 11
DISPID_SRCPause = 12
DISPID_SRCResume = 13
DISPID_SRCCreateGrammar = 14
DISPID_SRCCreateResultFromMemory = 15
DISPID_SRCBookmark = 16
DISPID_SRCSetAdaptationData = 17
DISPID_SpeechRecoContext = c_int # enum
SpeechCategoryAudioIn = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\AudioInput' # Constant BSTR
class ISpeechGrammarRule(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechGrammarRule Interface'
    _iid_ = GUID('{AFE719CF-5DD1-44F2-999C-7A399F1CFCCC}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechGrammarRuleState(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechGrammarRuleState Interface'
    _iid_ = GUID('{D4286F2C-EE67-45AE-B928-28D695362EDA}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechGrammarRuleStateTransition._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Type'), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(SpeechGrammarRuleStateTransitionType), 'Type' )),
    COMMETHOD([dispid(2), helpstring(u'Text'), 'propget'], HRESULT, 'Text',
              ( ['retval', 'out'], POINTER(BSTR), 'Text' )),
    COMMETHOD([dispid(3), helpstring(u'Rule'), 'propget'], HRESULT, 'Rule',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRule)), 'Rule' )),
    COMMETHOD([dispid(4), helpstring(u'Weight'), 'propget'], HRESULT, 'Weight',
              ( ['retval', 'out'], POINTER(VARIANT), 'Weight' )),
    COMMETHOD([dispid(5), helpstring(u'PropertyName'), 'propget'], HRESULT, 'PropertyName',
              ( ['retval', 'out'], POINTER(BSTR), 'PropertyName' )),
    COMMETHOD([dispid(6), helpstring(u'PropertyId'), 'propget'], HRESULT, 'PropertyId',
              ( ['retval', 'out'], POINTER(c_int), 'PropertyId' )),
    COMMETHOD([dispid(7), helpstring(u'PropertyValue'), 'propget'], HRESULT, 'PropertyValue',
              ( ['retval', 'out'], POINTER(VARIANT), 'PropertyValue' )),
    COMMETHOD([dispid(8), helpstring(u'NextState'), 'propget'], HRESULT, 'NextState',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRuleState)), 'NextState' )),
]

# values for enumeration 'SPVISEMES'
SP_VISEME_0 = 0
SP_VISEME_1 = 1
SP_VISEME_2 = 2
SP_VISEME_3 = 3
SP_VISEME_4 = 4
SP_VISEME_5 = 5
SP_VISEME_6 = 6
SP_VISEME_7 = 7
SP_VISEME_8 = 8
SP_VISEME_9 = 9
SP_VISEME_10 = 10
SP_VISEME_11 = 11
SP_VISEME_12 = 12
SP_VISEME_13 = 13
SP_VISEME_14 = 14
SP_VISEME_15 = 15
SP_VISEME_16 = 16
SP_VISEME_17 = 17
SP_VISEME_18 = 18
SP_VISEME_19 = 19
SP_VISEME_20 = 20
SP_VISEME_21 = 21
SPVISEMES = c_int # enum
ISpObjectToken._methods_ = [
    COMMETHOD([], HRESULT, 'SetId',
              ( [], POINTER(c_ushort), 'pszCategoryId' ),
              ( [], POINTER(c_ushort), 'pszTokenId' ),
              ( [], c_int, 'fCreateIfNotExist' )),
    COMMETHOD([], HRESULT, 'GetId',
              ( [], POINTER(POINTER(c_ushort)), 'ppszCoMemTokenId' )),
    COMMETHOD([], HRESULT, 'GetCategory',
              ( [], POINTER(POINTER(ISpObjectTokenCategory)), 'ppTokenCategory' )),
    COMMETHOD([], HRESULT, 'CreateInstance',
              ( ['in'], POINTER(IUnknown), 'pUnkOuter' ),
              ( ['in'], c_ulong, 'dwClsContext' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'riid' ),
              ( ['out'], POINTER(c_void_p), 'ppvObject' )),
    COMMETHOD([], HRESULT, 'GetStorageFileName',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'clsidCaller' ),
              ( ['in'], POINTER(c_ushort), 'pszValueName' ),
              ( ['in'], POINTER(c_ushort), 'pszFileNameSpecifier' ),
              ( ['in'], c_ulong, 'nFolder' ),
              ( ['out'], POINTER(POINTER(c_ushort)), 'ppszFilePath' )),
    COMMETHOD([], HRESULT, 'RemoveStorageFileName',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'clsidCaller' ),
              ( ['in'], POINTER(c_ushort), 'pszKeyName' ),
              ( ['in'], c_int, 'fDeleteFile' )),
    COMMETHOD([], HRESULT, 'Remove',
              ( [], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pclsidCaller' )),
    COMMETHOD([], HRESULT, 'IsUISupported',
              ( ['in'], POINTER(c_ushort), 'pszTypeOfUI' ),
              ( ['in'], c_void_p, 'pvExtraData' ),
              ( ['in'], c_ulong, 'cbExtraData' ),
              ( ['in'], POINTER(IUnknown), 'punkObject' ),
              ( ['out'], POINTER(c_int), 'pfSupported' )),
    COMMETHOD([], HRESULT, 'DisplayUI',
              ( ['in'], wireHWND, 'hWndParent' ),
              ( ['in'], POINTER(c_ushort), 'pszTitle' ),
              ( ['in'], POINTER(c_ushort), 'pszTypeOfUI' ),
              ( ['in'], c_void_p, 'pvExtraData' ),
              ( ['in'], c_ulong, 'cbExtraData' ),
              ( ['in'], POINTER(IUnknown), 'punkObject' )),
    COMMETHOD([], HRESULT, 'MatchesAttributes',
              ( ['in'], POINTER(c_ushort), 'pszAttributes' ),
              ( ['out'], POINTER(c_int), 'pfMatches' )),
]

# values for enumeration 'SpeechAudioFormatType'
SAFTDefault = -1
SAFTNoAssignedFormat = 0
SAFTText = 1
SAFTNonStandardFormat = 2
SAFTExtendedAudioFormat = 3
SAFT8kHz8BitMono = 4
SAFT8kHz8BitStereo = 5
SAFT8kHz16BitMono = 6
SAFT8kHz16BitStereo = 7
SAFT11kHz8BitMono = 8
SAFT11kHz8BitStereo = 9
SAFT11kHz16BitMono = 10
SAFT11kHz16BitStereo = 11
SAFT12kHz8BitMono = 12
SAFT12kHz8BitStereo = 13
SAFT12kHz16BitMono = 14
SAFT12kHz16BitStereo = 15
SAFT16kHz8BitMono = 16
SAFT16kHz8BitStereo = 17
SAFT16kHz16BitMono = 18
SAFT16kHz16BitStereo = 19
SAFT22kHz8BitMono = 20
SAFT22kHz8BitStereo = 21
SAFT22kHz16BitMono = 22
SAFT22kHz16BitStereo = 23
SAFT24kHz8BitMono = 24
SAFT24kHz8BitStereo = 25
SAFT24kHz16BitMono = 26
SAFT24kHz16BitStereo = 27
SAFT32kHz8BitMono = 28
SAFT32kHz8BitStereo = 29
SAFT32kHz16BitMono = 30
SAFT32kHz16BitStereo = 31
SAFT44kHz8BitMono = 32
SAFT44kHz8BitStereo = 33
SAFT44kHz16BitMono = 34
SAFT44kHz16BitStereo = 35
SAFT48kHz8BitMono = 36
SAFT48kHz8BitStereo = 37
SAFT48kHz16BitMono = 38
SAFT48kHz16BitStereo = 39
SAFTTrueSpeech_8kHz1BitMono = 40
SAFTCCITT_ALaw_8kHzMono = 41
SAFTCCITT_ALaw_8kHzStereo = 42
SAFTCCITT_ALaw_11kHzMono = 43
SAFTCCITT_ALaw_11kHzStereo = 44
SAFTCCITT_ALaw_22kHzMono = 45
SAFTCCITT_ALaw_22kHzStereo = 46
SAFTCCITT_ALaw_44kHzMono = 47
SAFTCCITT_ALaw_44kHzStereo = 48
SAFTCCITT_uLaw_8kHzMono = 49
SAFTCCITT_uLaw_8kHzStereo = 50
SAFTCCITT_uLaw_11kHzMono = 51
SAFTCCITT_uLaw_11kHzStereo = 52
SAFTCCITT_uLaw_22kHzMono = 53
SAFTCCITT_uLaw_22kHzStereo = 54
SAFTCCITT_uLaw_44kHzMono = 55
SAFTCCITT_uLaw_44kHzStereo = 56
SAFTADPCM_8kHzMono = 57
SAFTADPCM_8kHzStereo = 58
SAFTADPCM_11kHzMono = 59
SAFTADPCM_11kHzStereo = 60
SAFTADPCM_22kHzMono = 61
SAFTADPCM_22kHzStereo = 62
SAFTADPCM_44kHzMono = 63
SAFTADPCM_44kHzStereo = 64
SAFTGSM610_8kHzMono = 65
SAFTGSM610_11kHzMono = 66
SAFTGSM610_22kHzMono = 67
SAFTGSM610_44kHzMono = 68
SpeechAudioFormatType = c_int # enum
class ISpeechWaveFormatEx(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechWaveFormatEx Interface'
    _iid_ = GUID('{7A1EF0D5-1581-4741-88E4-209A49F11A10}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechAudioFormat._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Type'), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(SpeechAudioFormatType), 'AudioFormat' )),
    COMMETHOD([dispid(1), helpstring(u'Type'), 'propput'], HRESULT, 'Type',
              ( ['in'], SpeechAudioFormatType, 'AudioFormat' )),
    COMMETHOD([dispid(2), helpstring(u'Guid'), 'hidden', 'propget'], HRESULT, 'Guid',
              ( ['retval', 'out'], POINTER(BSTR), 'Guid' )),
    COMMETHOD([dispid(2), helpstring(u'Guid'), 'hidden', 'propput'], HRESULT, 'Guid',
              ( ['in'], BSTR, 'Guid' )),
    COMMETHOD([dispid(3), helpstring(u'GetWaveFormatEx'), 'hidden'], HRESULT, 'GetWaveFormatEx',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechWaveFormatEx)), 'WaveFormatEx' )),
    COMMETHOD([dispid(4), helpstring(u'SetWaveFormatEx'), 'hidden'], HRESULT, 'SetWaveFormatEx',
              ( ['in'], POINTER(ISpeechWaveFormatEx), 'WaveFormatEx' )),
]
class SPPHRASERULE(Structure):
    pass
SPPHRASERULE._fields_ = [
    ('pszName', POINTER(c_ushort)),
    ('ulId', c_ulong),
    ('ulFirstElement', c_ulong),
    ('ulCountOfElements', c_ulong),
    ('pNextSibling', POINTER(SPPHRASERULE)),
    ('pFirstChild', POINTER(SPPHRASERULE)),
    ('SREngineConfidence', c_float),
    ('Confidence', c_char),
]
assert sizeof(SPPHRASERULE) == 32, sizeof(SPPHRASERULE)
assert alignment(SPPHRASERULE) == 4, alignment(SPPHRASERULE)
class SPPHRASEPROPERTY(Structure):
    pass
class SPPHRASEELEMENT(Structure):
    pass
class SPPHRASEREPLACEMENT(Structure):
    pass
SPPHRASE._fields_ = [
    ('cbSize', c_ulong),
    ('LangId', c_ushort),
    ('wReserved', c_ushort),
    ('ullGrammarID', c_ulonglong),
    ('ftStartTime', c_ulonglong),
    ('ullAudioStreamPosition', c_ulonglong),
    ('ulAudioSizeBytes', c_ulong),
    ('ulRetainedSizeBytes', c_ulong),
    ('ulAudioSizeTime', c_ulong),
    ('Rule', SPPHRASERULE),
    ('pProperties', POINTER(SPPHRASEPROPERTY)),
    ('pElements', POINTER(SPPHRASEELEMENT)),
    ('cReplacements', c_ulong),
    ('pReplacements', POINTER(SPPHRASEREPLACEMENT)),
    ('SREngineID', comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
    ('ulSREnginePrivateDataSize', c_ulong),
    ('pSREnginePrivateData', POINTER(c_ubyte)),
]
assert sizeof(SPPHRASE) == 120, sizeof(SPPHRASE)
assert alignment(SPPHRASE) == 8, alignment(SPPHRASE)
class SPAUDIOBUFFERINFO(Structure):
    pass
SPAUDIOBUFFERINFO._fields_ = [
    ('ulMsMinNotification', c_ulong),
    ('ulMsBufferSize', c_ulong),
    ('ulMsEventBias', c_ulong),
]
assert sizeof(SPAUDIOBUFFERINFO) == 12, sizeof(SPAUDIOBUFFERINFO)
assert alignment(SPAUDIOBUFFERINFO) == 4, alignment(SPAUDIOBUFFERINFO)
class ISpProperties(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    u'ISpProperties Interface'
    _iid_ = GUID('{5B4FB971-B115-4DE1-AD97-E482E3BF6EE4}')
    _idlflags_ = ['restricted']
ISpProperties._methods_ = [
    COMMETHOD([], HRESULT, 'SetPropertyNum',
              ( ['in'], POINTER(c_ushort), 'pName' ),
              ( ['in'], c_int, 'lValue' )),
    COMMETHOD([], HRESULT, 'GetPropertyNum',
              ( ['in'], POINTER(c_ushort), 'pName' ),
              ( ['out'], POINTER(c_int), 'plValue' )),
    COMMETHOD([], HRESULT, 'SetPropertyString',
              ( ['in'], POINTER(c_ushort), 'pName' ),
              ( ['in'], POINTER(c_ushort), 'pValue' )),
    COMMETHOD([], HRESULT, 'GetPropertyString',
              ( ['in'], POINTER(c_ushort), 'pName' ),
              ( ['out'], POINTER(POINTER(c_ushort)), 'ppCoMemValue' )),
]
class IServiceProvider(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{6D5140C1-7436-11CE-8034-00AA006009FA}')
    _idlflags_ = []
class ISpResourceManager(IServiceProvider):
    _case_insensitive_ = True
    u'ISpResourceManager Interface'
    _iid_ = GUID('{93384E18-5014-43D5-ADBB-A78E055926BD}')
    _idlflags_ = ['restricted']
IServiceProvider._methods_ = [
    COMMETHOD([], HRESULT, 'RemoteQueryService',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'guidService' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'riid' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppvObject' )),
]
ISpResourceManager._methods_ = [
    COMMETHOD([], HRESULT, 'SetObject',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'guidServiceId' ),
              ( ['in'], POINTER(IUnknown), 'punkObject' )),
    COMMETHOD([], HRESULT, 'GetObject',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'guidServiceId' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'ObjectCLSID' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'ObjectIID' ),
              ( ['in'], c_int, 'fReleaseWhenLastExternalRefReleased' ),
              ( ['out'], POINTER(c_void_p), 'ppObject' )),
]

# values for enumeration 'DISPID_SpeechRecognizerStatus'
DISPID_SRSAudioStatus = 1
DISPID_SRSCurrentStreamPosition = 2
DISPID_SRSCurrentStreamNumber = 3
DISPID_SRSNumberOfActiveRules = 4
DISPID_SRSClsidEngine = 5
DISPID_SRSSupportedLanguages = 6
DISPID_SpeechRecognizerStatus = c_int # enum
class SpSharedRecognizer(CoClass):
    u'SpSharedRecognizer Class'
    _reg_clsid_ = GUID('{3BEE4890-4FE9-4A37-8C1E-5E7E12791C1F}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpRecognizer(ISpProperties):
    _case_insensitive_ = True
    u'ISpRecognizer Interface'
    _iid_ = GUID('{C2B5F241-DAA0-4507-9E16-5A1EAA2B7A5C}')
    _idlflags_ = ['restricted']
SpSharedRecognizer._com_interfaces_ = [ISpeechRecognizer, ISpRecognizer]


# values for enumeration 'SPAUDIOOPTIONS'
SPAO_NONE = 0
SPAO_RETAIN_AUDIO = 1
SPAUDIOOPTIONS = c_int # enum
IEnumSpObjectTokens._methods_ = [
    COMMETHOD([], HRESULT, 'Next',
              ( ['in'], c_ulong, 'celt' ),
              ( ['out'], POINTER(POINTER(ISpObjectToken)), 'pelt' ),
              ( ['out'], POINTER(c_ulong), 'pceltFetched' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], c_ulong, 'celt' )),
    COMMETHOD([], HRESULT, 'Reset'),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out'], POINTER(POINTER(IEnumSpObjectTokens)), 'ppEnum' )),
    COMMETHOD([], HRESULT, 'Item',
              ( ['in'], c_ulong, 'Index' ),
              ( ['out'], POINTER(POINTER(ISpObjectToken)), 'ppToken' )),
    COMMETHOD([], HRESULT, 'GetCount',
              ( ['out'], POINTER(c_ulong), 'pCount' )),
]

# values for enumeration 'SpeechDisplayAttributes'
SDA_No_Trailing_Space = 0
SDA_One_Trailing_Space = 2
SDA_Two_Trailing_Spaces = 4
SDA_Consume_Leading_Spaces = 8
SpeechDisplayAttributes = c_int # enum
class ISpeechAudioStatus(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechAudioStatus Interface'
    _iid_ = GUID('{C62D9C91-7458-47F6-862D-1EF86FB0B278}')
    _idlflags_ = ['dual', 'oleautomation']

# values for enumeration 'SpeechAudioState'
SASClosed = 0
SASStop = 1
SASPause = 2
SASRun = 3
SpeechAudioState = c_int # enum
ISpeechAudioStatus._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'FreeBufferSpace'), 'propget'], HRESULT, 'FreeBufferSpace',
              ( ['retval', 'out'], POINTER(c_int), 'FreeBufferSpace' )),
    COMMETHOD([dispid(2), helpstring(u'NonBlockingIO'), 'propget'], HRESULT, 'NonBlockingIO',
              ( ['retval', 'out'], POINTER(c_int), 'NonBlockingIO' )),
    COMMETHOD([dispid(3), helpstring(u'State'), 'propget'], HRESULT, 'State',
              ( ['retval', 'out'], POINTER(SpeechAudioState), 'State' )),
    COMMETHOD([dispid(4), helpstring(u'CurrentSeekPosition'), 'propget'], HRESULT, 'CurrentSeekPosition',
              ( ['retval', 'out'], POINTER(VARIANT), 'CurrentSeekPosition' )),
    COMMETHOD([dispid(5), helpstring(u'CurrentDevicePosition'), 'propget'], HRESULT, 'CurrentDevicePosition',
              ( ['retval', 'out'], POINTER(VARIANT), 'CurrentDevicePosition' )),
]
SpeechUserTraining = u'UserTraining' # Constant BSTR
SPSERIALIZEDPHRASE._fields_ = [
    ('ulSerializedSize', c_ulong),
]
assert sizeof(SPSERIALIZEDPHRASE) == 4, sizeof(SPSERIALIZEDPHRASE)
assert alignment(SPSERIALIZEDPHRASE) == 4, alignment(SPSERIALIZEDPHRASE)

# values for enumeration 'DISPID_SpeechGrammarRuleStateTransitions'
DISPID_SGRSTsCount = 1
DISPID_SGRSTsItem = 0
DISPID_SGRSTs_NewEnum = -4
DISPID_SpeechGrammarRuleStateTransitions = c_int # enum

# values for enumeration 'SpeechInterference'
SINone = 0
SINoise = 1
SINoSignal = 2
SITooLoud = 3
SITooQuiet = 4
SITooFast = 5
SITooSlow = 6
SpeechInterference = c_int # enum
class ISpeechRecoResult(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechRecoResult Interface'
    _iid_ = GUID('{ED2879CF-CED9-4EE6-A534-DE0191D5468D}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechPhraseInfo(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseInfo Interface'
    _iid_ = GUID('{961559CF-4E67-4662-8BF0-D93F1FCD61B3}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechPhraseAlternate._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'RecoResult'), 'propget'], HRESULT, 'RecoResult',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecoResult)), 'RecoResult' )),
    COMMETHOD([dispid(2), helpstring(u'StartElementInResult'), 'propget'], HRESULT, 'StartElementInResult',
              ( ['retval', 'out'], POINTER(c_int), 'StartElement' )),
    COMMETHOD([dispid(3), helpstring(u'NumberOfElementsInResult'), 'propget'], HRESULT, 'NumberOfElementsInResult',
              ( ['retval', 'out'], POINTER(c_int), 'NumberOfElements' )),
    COMMETHOD([dispid(4), helpstring(u'Phrase'), 'propget'], HRESULT, 'PhraseInfo',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseInfo)), 'PhraseInfo' )),
    COMMETHOD([dispid(5), helpstring(u'Commit')], HRESULT, 'Commit'),
]
ISpeechGrammarRule._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'RuleAttributes'), 'propget'], HRESULT, 'Attributes',
              ( ['retval', 'out'], POINTER(SpeechRuleAttributes), 'Attributes' )),
    COMMETHOD([dispid(2), helpstring(u'InitialState'), 'propget'], HRESULT, 'InitialState',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRuleState)), 'State' )),
    COMMETHOD([dispid(3), helpstring(u'Name'), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'Name' )),
    COMMETHOD([dispid(4), helpstring(u'Id'), 'propget'], HRESULT, 'Id',
              ( ['retval', 'out'], POINTER(c_int), 'Id' )),
    COMMETHOD([dispid(5), helpstring(u'Clear')], HRESULT, 'Clear'),
    COMMETHOD([dispid(6), helpstring(u'AddResource')], HRESULT, 'AddResource',
              ( ['in'], BSTR, 'ResourceName' ),
              ( ['in'], BSTR, 'ResourceValue' )),
    COMMETHOD([dispid(7), helpstring(u'AddState')], HRESULT, 'AddState',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRuleState)), 'State' )),
]
SpeechPropertyComplexResponseSpeed = u'ComplexResponseSpeed' # Constant BSTR
SpeechEngineProperties = u'EngineProperties' # Constant BSTR
SPPHRASEREPLACEMENT._fields_ = [
    ('bDisplayAttributes', c_ubyte),
    ('pszReplacementText', POINTER(c_ushort)),
    ('ulFirstElement', c_ulong),
    ('ulCountOfElements', c_ulong),
]
assert sizeof(SPPHRASEREPLACEMENT) == 16, sizeof(SPPHRASEREPLACEMENT)
assert alignment(SPPHRASEREPLACEMENT) == 4, alignment(SPPHRASEREPLACEMENT)
class SPEVENT(Structure):
    pass
SPEVENT._fields_ = [
    ('eEventId', c_ushort),
    ('elParamType', c_ushort),
    ('ulStreamNum', c_ulong),
    ('ullAudioStreamOffset', c_ulonglong),
    ('wParam', UINT_PTR),
    ('lParam', LONG_PTR),
]
assert sizeof(SPEVENT) == 24, sizeof(SPEVENT)
assert alignment(SPEVENT) == 8, alignment(SPEVENT)
Speech_StreamPos_Asap = 0 # Constant c_int

# values for enumeration 'DISPIDSPRG'
DISPID_SRGId = 1
DISPID_SRGRecoContext = 2
DISPID_SRGState = 3
DISPID_SRGRules = 4
DISPID_SRGReset = 5
DISPID_SRGCommit = 6
DISPID_SRGCmdLoadFromFile = 7
DISPID_SRGCmdLoadFromObject = 8
DISPID_SRGCmdLoadFromResource = 9
DISPID_SRGCmdLoadFromMemory = 10
DISPID_SRGCmdLoadFromProprietaryGrammar = 11
DISPID_SRGCmdSetRuleState = 12
DISPID_SRGCmdSetRuleIdState = 13
DISPID_SRGDictationLoad = 14
DISPID_SRGDictationUnload = 15
DISPID_SRGDictationSetState = 16
DISPID_SRGSetWordSequenceData = 17
DISPID_SRGSetTextSelection = 18
DISPID_SRGIsPronounceable = 19
DISPIDSPRG = c_int # enum
ISpNotifyTranslator._methods_ = [
    COMMETHOD([], HRESULT, 'InitWindowMessage',
              ( ['in'], wireHWND, 'hWnd' ),
              ( ['in'], c_uint, 'Msg' ),
              ( ['in'], UINT_PTR, 'wParam' ),
              ( ['in'], LONG_PTR, 'lParam' )),
    COMMETHOD([], HRESULT, 'InitCallback',
              ( ['in'], POINTER(c_void_p), 'pfnCallback' ),
              ( ['in'], UINT_PTR, 'wParam' ),
              ( ['in'], LONG_PTR, 'lParam' )),
    COMMETHOD([], HRESULT, 'InitSpNotifyCallback',
              ( ['in'], POINTER(c_void_p), 'pSpCallback' ),
              ( ['in'], UINT_PTR, 'wParam' ),
              ( ['in'], LONG_PTR, 'lParam' )),
    COMMETHOD([], HRESULT, 'InitWin32Event',
              ( [], c_void_p, 'hEvent' ),
              ( [], c_int, 'fCloseHandleOnRelease' )),
    COMMETHOD([], HRESULT, 'Wait',
              ( ['in'], c_ulong, 'dwMilliseconds' )),
    COMMETHOD([], c_void_p, 'GetEventHandle'),
]
class SpTextSelectionInformation(CoClass):
    u'SpTextSelectionInformation Class'
    _reg_clsid_ = GUID('{0F92030A-CBFD-4AB8-A164-FF5985547FF6}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class ISpeechTextSelectionInformation(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechTextSelectionInformation Interface'
    _iid_ = GUID('{3B9C7E7A-6EEE-4DED-9092-11657279ADBE}')
    _idlflags_ = ['dual', 'oleautomation']
SpTextSelectionInformation._com_interfaces_ = [ISpeechTextSelectionInformation]

SpeechCategoryVoices = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices' # Constant BSTR
class SPEVENTSOURCEINFO(Structure):
    pass
SPEVENTSOURCEINFO._fields_ = [
    ('ullEventInterest', c_ulonglong),
    ('ullQueuedInterest', c_ulonglong),
    ('ulCount', c_ulong),
]
assert sizeof(SPEVENTSOURCEINFO) == 24, sizeof(SPEVENTSOURCEINFO)
assert alignment(SPEVENTSOURCEINFO) == 8, alignment(SPEVENTSOURCEINFO)
class SpAudioFormat(CoClass):
    u'SpAudioFormat Class'
    _reg_clsid_ = GUID('{9EF96870-E160-4792-820D-48CF0649E4EC}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpAudioFormat._com_interfaces_ = [ISpeechAudioFormat]


# values for enumeration 'SpeechRecognitionType'
SRTStandard = 0
SRTAutopause = 1
SRTEmulated = 2
SpeechRecognitionType = c_int # enum

# values for enumeration 'DISPID_SpeechVoice'
DISPID_SVStatus = 1
DISPID_SVVoice = 2
DISPID_SVAudioOutput = 3
DISPID_SVAudioOutputStream = 4
DISPID_SVRate = 5
DISPID_SVVolume = 6
DISPID_SVAllowAudioOuputFormatChangesOnNextSet = 7
DISPID_SVEventInterests = 8
DISPID_SVPriority = 9
DISPID_SVAlertBoundary = 10
DISPID_SVSyncronousSpeakTimeout = 11
DISPID_SVSpeak = 12
DISPID_SVSpeakStream = 13
DISPID_SVPause = 14
DISPID_SVResume = 15
DISPID_SVSkip = 16
DISPID_SVGetVoices = 17
DISPID_SVGetAudioOutputs = 18
DISPID_SVWaitUntilDone = 19
DISPID_SVSpeakCompleteEvent = 20
DISPID_SVIsUISupported = 21
DISPID_SVDisplayUI = 22
DISPID_SpeechVoice = c_int # enum
class SpSharedRecoContext(CoClass):
    u'SpSharedRecoContext Class'
    _reg_clsid_ = GUID('{47206204-5ECA-11D2-960F-00C04F8EE628}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpSharedRecoContext._com_interfaces_ = [ISpeechRecoContext, ISpRecoContext]
SpSharedRecoContext._outgoing_interfaces_ = [_ISpeechRecoContextEvents]


# values for enumeration 'SPBOOKMARKOPTIONS'
SPBO_NONE = 0
SPBO_PAUSE = 1
SPBOOKMARKOPTIONS = c_int # enum

# values for enumeration 'SpeechGrammarState'
SGSEnabled = 1
SGSDisabled = 0
SGSExclusive = 3
SpeechGrammarState = c_int # enum
class SpLexicon(CoClass):
    u'SpLexicon Class'
    _reg_clsid_ = GUID('{0655E396-25D0-11D3-9C26-00C04F8EF87C}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpLexicon._com_interfaces_ = [ISpeechLexicon, ISpLexicon]

SPPHRASEELEMENT._fields_ = [
    ('ulAudioTimeOffset', c_ulong),
    ('ulAudioSizeTime', c_ulong),
    ('ulAudioStreamOffset', c_ulong),
    ('ulAudioSizeBytes', c_ulong),
    ('ulRetainedStreamOffset', c_ulong),
    ('ulRetainedSizeBytes', c_ulong),
    ('pszDisplayText', POINTER(c_ushort)),
    ('pszLexicalForm', POINTER(c_ushort)),
    ('pszPronunciation', POINTER(c_ushort)),
    ('bDisplayAttributes', c_ubyte),
    ('RequiredConfidence', c_char),
    ('ActualConfidence', c_char),
    ('reserved', c_ubyte),
    ('SREngineConfidence', c_float),
]
assert sizeof(SPPHRASEELEMENT) == 44, sizeof(SPPHRASEELEMENT)
assert alignment(SPPHRASEELEMENT) == 4, alignment(SPPHRASEELEMENT)
class ISpeechDataKey(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechDataKey Interface'
    _iid_ = GUID('{CE17C09B-4EFA-44D5-A4C9-59D9585AB0CD}')
    _idlflags_ = ['dual', 'oleautomation']

# values for enumeration 'SpeechTokenContext'
STCInprocServer = 1
STCInprocHandler = 2
STCLocalServer = 4
STCRemoteServer = 16
STCAll = 23
SpeechTokenContext = c_int # enum

# values for enumeration 'SpeechTokenShellFolder'
STSF_AppData = 26
STSF_LocalAppData = 28
STSF_CommonAppData = 35
STSF_FlagCreate = 32768
SpeechTokenShellFolder = c_int # enum
ISpeechObjectToken._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Id'), 'propget'], HRESULT, 'Id',
              ( ['retval', 'out'], POINTER(BSTR), 'ObjectId' )),
    COMMETHOD([dispid(2), helpstring(u'DataKey'), 'hidden', 'propget'], HRESULT, 'DataKey',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechDataKey)), 'DataKey' )),
    COMMETHOD([dispid(3), helpstring(u'Category'), 'propget'], HRESULT, 'Category',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectTokenCategory)), 'Category' )),
    COMMETHOD([dispid(4), helpstring(u'GetDescription')], HRESULT, 'GetDescription',
              ( ['in', 'optional'], c_int, 'Locale', 0 ),
              ( ['retval', 'out'], POINTER(BSTR), 'Description' )),
    COMMETHOD([dispid(5), helpstring(u'SetId'), 'hidden'], HRESULT, 'SetId',
              ( ['in'], BSTR, 'Id' ),
              ( ['in', 'optional'], BSTR, 'CategoryID', u'' ),
              ( ['in', 'optional'], VARIANT_BOOL, 'CreateIfNotExist', False )),
    COMMETHOD([dispid(6), helpstring(u'GetAttribute')], HRESULT, 'GetAttribute',
              ( ['in'], BSTR, 'AttributeName' ),
              ( ['retval', 'out'], POINTER(BSTR), 'AttributeValue' )),
    COMMETHOD([dispid(7), helpstring(u'CreateInstance')], HRESULT, 'CreateInstance',
              ( ['in', 'optional'], POINTER(IUnknown), 'pUnkOuter' ),
              ( ['in', 'optional'], SpeechTokenContext, 'ClsContext', 23 ),
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'Object' )),
    COMMETHOD([dispid(8), helpstring(u'Remove'), 'hidden'], HRESULT, 'Remove',
              ( ['in'], BSTR, 'ObjectStorageCLSID' )),
    COMMETHOD([dispid(9), helpstring(u'GetStorageFileName'), 'hidden'], HRESULT, 'GetStorageFileName',
              ( ['in'], BSTR, 'ObjectStorageCLSID' ),
              ( ['in'], BSTR, 'KeyName' ),
              ( ['in'], BSTR, 'FileName' ),
              ( ['in'], SpeechTokenShellFolder, 'Folder' ),
              ( ['retval', 'out'], POINTER(BSTR), 'FilePath' )),
    COMMETHOD([dispid(10), helpstring(u'RemoveStorageFileName'), 'hidden'], HRESULT, 'RemoveStorageFileName',
              ( ['in'], BSTR, 'ObjectStorageCLSID' ),
              ( ['in'], BSTR, 'KeyName' ),
              ( ['in'], VARIANT_BOOL, 'DeleteFile' )),
    COMMETHOD([dispid(11), helpstring(u'IsUISupported'), 'hidden'], HRESULT, 'IsUISupported',
              ( ['in'], BSTR, 'TypeOfUI' ),
              ( ['in', 'optional'], POINTER(VARIANT), 'ExtraData', u'' ),
              ( ['in', 'optional'], POINTER(IUnknown), 'Object' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Supported' )),
    COMMETHOD([dispid(12), helpstring(u'DisplayUI'), 'hidden'], HRESULT, 'DisplayUI',
              ( ['in'], c_int, 'hWnd' ),
              ( ['in'], BSTR, 'Title' ),
              ( ['in'], BSTR, 'TypeOfUI' ),
              ( ['in', 'optional'], POINTER(VARIANT), 'ExtraData', u'' ),
              ( ['in', 'optional'], POINTER(IUnknown), 'Object' )),
    COMMETHOD([dispid(13), helpstring(u'MatchesAttributes')], HRESULT, 'MatchesAttributes',
              ( ['in'], BSTR, 'Attributes' ),
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Matches' )),
]

# values for enumeration 'SPWAVEFORMATTYPE'
SPWF_INPUT = 0
SPWF_SRENGINE = 1
SPWAVEFORMATTYPE = c_int # enum
SPSTREAMFORMATTYPE = SPWAVEFORMATTYPE

# values for enumeration 'DISPID_SpeechPhraseProperties'
DISPID_SPPsCount = 1
DISPID_SPPsItem = 0
DISPID_SPPs_NewEnum = -4
DISPID_SpeechPhraseProperties = c_int # enum

# values for enumeration 'DISPID_SpeechRecognizer'
DISPID_SRRecognizer = 1
DISPID_SRAllowAudioInputFormatChangesOnNextSet = 2
DISPID_SRAudioInput = 3
DISPID_SRAudioInputStream = 4
DISPID_SRIsShared = 5
DISPID_SRState = 6
DISPID_SRStatus = 7
DISPID_SRProfile = 8
DISPID_SREmulateRecognition = 9
DISPID_SRCreateRecoContext = 10
DISPID_SRGetFormat = 11
DISPID_SRSetPropertyNumber = 12
DISPID_SRGetPropertyNumber = 13
DISPID_SRSetPropertyString = 14
DISPID_SRGetPropertyString = 15
DISPID_SRIsUISupported = 16
DISPID_SRDisplayUI = 17
DISPID_SRGetRecognizers = 18
DISPID_SVGetAudioInputs = 19
DISPID_SVGetProfiles = 20
DISPID_SpeechRecognizer = c_int # enum
class SPRECOCONTEXTSTATUS(Structure):
    pass

# values for enumeration 'SPINTERFERENCE'
SPINTERFERENCE_NONE = 0
SPINTERFERENCE_NOISE = 1
SPINTERFERENCE_NOSIGNAL = 2
SPINTERFERENCE_TOOLOUD = 3
SPINTERFERENCE_TOOQUIET = 4
SPINTERFERENCE_TOOFAST = 5
SPINTERFERENCE_TOOSLOW = 6
SPINTERFERENCE = c_int # enum
SPRECOCONTEXTSTATUS._fields_ = [
    ('eInterference', SPINTERFERENCE),
    ('szRequestTypeOfUI', c_ushort * 255),
    ('dwReserved1', c_ulong),
    ('dwReserved2', c_ulong),
]
assert sizeof(SPRECOCONTEXTSTATUS) == 524, sizeof(SPRECOCONTEXTSTATUS)
assert alignment(SPRECOCONTEXTSTATUS) == 4, alignment(SPRECOCONTEXTSTATUS)
SPBINARYGRAMMAR._fields_ = [
    ('ulTotalSerializedSize', c_ulong),
]
assert sizeof(SPBINARYGRAMMAR) == 4, sizeof(SPBINARYGRAMMAR)
assert alignment(SPBINARYGRAMMAR) == 4, alignment(SPBINARYGRAMMAR)

# values for enumeration 'DISPID_SpeechObjectTokens'
DISPID_SOTsCount = 1
DISPID_SOTsItem = 0
DISPID_SOTs_NewEnum = -4
DISPID_SpeechObjectTokens = c_int # enum

# values for enumeration 'SpeechRunState'
SRSEDone = 1
SRSEIsSpeaking = 2
SpeechRunState = c_int # enum
ISpeechVoiceStatus._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'CurrentStreamNumber'), 'propget'], HRESULT, 'CurrentStreamNumber',
              ( ['retval', 'out'], POINTER(c_int), 'StreamNumber' )),
    COMMETHOD([dispid(2), helpstring(u'LastStreamNumberQueued'), 'propget'], HRESULT, 'LastStreamNumberQueued',
              ( ['retval', 'out'], POINTER(c_int), 'StreamNumber' )),
    COMMETHOD([dispid(3), helpstring(u'LastHResult'), 'propget'], HRESULT, 'LastHResult',
              ( ['retval', 'out'], POINTER(c_int), 'HResult' )),
    COMMETHOD([dispid(4), helpstring(u'RunningState'), 'propget'], HRESULT, 'RunningState',
              ( ['retval', 'out'], POINTER(SpeechRunState), 'State' )),
    COMMETHOD([dispid(5), helpstring(u'InputWordPosition'), 'propget'], HRESULT, 'InputWordPosition',
              ( ['retval', 'out'], POINTER(c_int), 'Position' )),
    COMMETHOD([dispid(6), helpstring(u'InputWordLength'), 'propget'], HRESULT, 'InputWordLength',
              ( ['retval', 'out'], POINTER(c_int), 'Length' )),
    COMMETHOD([dispid(7), helpstring(u'InputSentencePosition'), 'propget'], HRESULT, 'InputSentencePosition',
              ( ['retval', 'out'], POINTER(c_int), 'Position' )),
    COMMETHOD([dispid(8), helpstring(u'InputSentenceLength'), 'propget'], HRESULT, 'InputSentenceLength',
              ( ['retval', 'out'], POINTER(c_int), 'Length' )),
    COMMETHOD([dispid(9), helpstring(u'LastBookmark'), 'propget'], HRESULT, 'LastBookmark',
              ( ['retval', 'out'], POINTER(BSTR), 'Bookmark' )),
    COMMETHOD([dispid(10), helpstring(u'LastBookmarkId'), 'hidden', 'propget'], HRESULT, 'LastBookmarkId',
              ( ['retval', 'out'], POINTER(c_int), 'BookmarkId' )),
    COMMETHOD([dispid(11), helpstring(u'PhonemeId'), 'propget'], HRESULT, 'PhonemeId',
              ( ['retval', 'out'], POINTER(c_short), 'PhoneId' )),
    COMMETHOD([dispid(12), helpstring(u'VisemeId'), 'propget'], HRESULT, 'VisemeId',
              ( ['retval', 'out'], POINTER(c_short), 'VisemeId' )),
]
SpeechCategoryRecognizers = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Recognizers' # Constant BSTR
SPWORD._fields_ = [
    ('pNextWord', POINTER(SPWORD)),
    ('LangId', c_ushort),
    ('wReserved', c_ushort),
    ('eWordType', SPWORDTYPE),
    ('pszWord', POINTER(c_ushort)),
    ('pFirstWordPronunciation', POINTER(SPWORDPRONUNCIATION)),
]
assert sizeof(SPWORD) == 20, sizeof(SPWORD)
assert alignment(SPWORD) == 4, alignment(SPWORD)

# values for enumeration 'SpeechBookmarkOptions'
SBONone = 0
SBOPause = 1
SpeechBookmarkOptions = c_int # enum
_ISpeechRecoContextEvents._disp_methods_ = [
    DISPMETHOD([dispid(1), helpstring(u'StartStream')], None, 'StartStream',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(2), helpstring(u'EndStream')], None, 'EndStream',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], VARIANT_BOOL, 'StreamReleased' )),
    DISPMETHOD([dispid(3), helpstring(u'Bookmark')], None, 'Bookmark',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], VARIANT, 'BookmarkId' ),
               ( ['in'], SpeechBookmarkOptions, 'Options' )),
    DISPMETHOD([dispid(4), helpstring(u'SoundStart')], None, 'SoundStart',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(5), helpstring(u'SoundEnd')], None, 'SoundEnd',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(6), helpstring(u'PhraseStart')], None, 'PhraseStart',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(7), helpstring(u'Recognition')], None, 'Recognition',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], SpeechRecognitionType, 'RecognitionType' ),
               ( ['in'], POINTER(ISpeechRecoResult), 'Result' )),
    DISPMETHOD([dispid(8), helpstring(u'Hypothesis')], None, 'Hypothesis',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], POINTER(ISpeechRecoResult), 'Result' )),
    DISPMETHOD([dispid(9), helpstring(u'PropertyNumberChange')], None, 'PropertyNumberChange',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], BSTR, 'PropertyName' ),
               ( ['in'], c_int, 'NewNumberValue' )),
    DISPMETHOD([dispid(10), helpstring(u'PropertyStringChange')], None, 'PropertyStringChange',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], BSTR, 'PropertyName' ),
               ( ['in'], BSTR, 'NewStringValue' )),
    DISPMETHOD([dispid(11), helpstring(u'FalseRecognition')], None, 'FalseRecognition',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], POINTER(ISpeechRecoResult), 'Result' )),
    DISPMETHOD([dispid(12), helpstring(u'Interference')], None, 'Interference',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], SpeechInterference, 'Interference' )),
    DISPMETHOD([dispid(13), helpstring(u'RequestUI')], None, 'RequestUI',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], BSTR, 'UIType' )),
    DISPMETHOD([dispid(14), helpstring(u'RecognizerStateChange')], None, 'RecognizerStateChange',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], SpeechRecognizerState, 'NewState' )),
    DISPMETHOD([dispid(15), helpstring(u'Adaptation')], None, 'Adaptation',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(16), helpstring(u'RecognitionForOtherContext')], None, 'RecognitionForOtherContext',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(17), helpstring(u'AudioLevel')], None, 'AudioLevel',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], c_int, 'AudioLevel' )),
    DISPMETHOD([dispid(18), helpstring(u'EnginePrivate')], None, 'EnginePrivate',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], VARIANT, 'EngineData' )),
]

# values for enumeration 'SpeechLexiconType'
SLTUser = 1
SLTApp = 2
SpeechLexiconType = c_int # enum

# values for enumeration 'DISPID_SpeechLexiconWord'
DISPID_SLWLangId = 1
DISPID_SLWType = 2
DISPID_SLWWord = 3
DISPID_SLWPronunciations = 4
DISPID_SpeechLexiconWord = c_int # enum
class ISpeechPhraseInfoBuilder(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseInfoBuilder Interface'
    _iid_ = GUID('{3B151836-DF3A-4E0A-846C-D2ADC9334333}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechPhraseInfoBuilder._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'RestorePhraseFromMemory')], HRESULT, 'RestorePhraseFromMemory',
              ( ['in'], POINTER(VARIANT), 'PhraseInMemory' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseInfo)), 'PhraseInfo' )),
]
SpeechPropertyAdaptationOn = u'AdaptationOn' # Constant BSTR

# values for enumeration 'SpeechWordType'
SWTAdded = 1
SWTDeleted = 2
SpeechWordType = c_int # enum

# values for enumeration 'SpeechPartOfSpeech'
SPSNotOverriden = -1
SPSUnknown = 0
SPSNoun = 4096
SPSVerb = 8192
SPSModifier = 12288
SPSFunction = 16384
SPSInterjection = 20480
SpeechPartOfSpeech = c_int # enum
class ISpeechLexiconPronunciations(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechLexiconPronunciations Interface'
    _iid_ = GUID('{72829128-5682-4704-A0D4-3E2BB6F2EAD3}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechLexicon._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'GenerationId'), 'hidden', 'propget'], HRESULT, 'GenerationId',
              ( ['retval', 'out'], POINTER(c_int), 'GenerationId' )),
    COMMETHOD([dispid(2), helpstring(u'GetWords')], HRESULT, 'GetWords',
              ( ['in', 'optional'], SpeechLexiconType, 'Flags', 3 ),
              ( ['out', 'optional'], POINTER(c_int), 'GenerationId', 0 ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechLexiconWords)), 'Words' )),
    COMMETHOD([dispid(3), helpstring(u'AddPronunciation')], HRESULT, 'AddPronunciation',
              ( ['in'], BSTR, 'bstrWord' ),
              ( ['in'], c_int, 'LangId' ),
              ( ['in', 'optional'], SpeechPartOfSpeech, 'PartOfSpeech', 0 ),
              ( ['in', 'optional'], BSTR, 'bstrPronunciation', u'' )),
    COMMETHOD([dispid(4), helpstring(u'AddPronunciationByPhoneIds'), 'hidden'], HRESULT, 'AddPronunciationByPhoneIds',
              ( ['in'], BSTR, 'bstrWord' ),
              ( ['in'], c_int, 'LangId' ),
              ( ['in', 'optional'], SpeechPartOfSpeech, 'PartOfSpeech', 0 ),
              ( ['in', 'optional'], POINTER(VARIANT), 'PhoneIds', u'' )),
    COMMETHOD([dispid(5), helpstring(u'RemovePronunciation')], HRESULT, 'RemovePronunciation',
              ( ['in'], BSTR, 'bstrWord' ),
              ( ['in'], c_int, 'LangId' ),
              ( ['in', 'optional'], SpeechPartOfSpeech, 'PartOfSpeech', 0 ),
              ( ['in', 'optional'], BSTR, 'bstrPronunciation', u'' )),
    COMMETHOD([dispid(6), helpstring(u'RemovePronunciationByPhoneIds'), 'hidden'], HRESULT, 'RemovePronunciationByPhoneIds',
              ( ['in'], BSTR, 'bstrWord' ),
              ( ['in'], c_int, 'LangId' ),
              ( ['in', 'optional'], SpeechPartOfSpeech, 'PartOfSpeech', 0 ),
              ( ['in', 'optional'], POINTER(VARIANT), 'PhoneIds', u'' )),
    COMMETHOD([dispid(7), helpstring(u'GetPronunciations')], HRESULT, 'GetPronunciations',
              ( ['in'], BSTR, 'bstrWord' ),
              ( ['in', 'optional'], c_int, 'LangId', 0 ),
              ( ['in', 'optional'], SpeechLexiconType, 'TypeFlags', 3 ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechLexiconPronunciations)), 'ppPronunciations' )),
    COMMETHOD([dispid(8), helpstring(u'GetGenerationChange'), 'hidden'], HRESULT, 'GetGenerationChange',
              ( ['in', 'out'], POINTER(c_int), 'GenerationId' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechLexiconWords)), 'ppWords' )),
]
class SpObjectToken(CoClass):
    u'SpObjectToken Class'
    _reg_clsid_ = GUID('{EF411752-3736-4CB4-9C8C-8EF4CCB58EFE}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpObjectToken._com_interfaces_ = [ISpeechObjectToken, ISpObjectToken]

SpeechTokenKeyAttributes = u'Attributes' # Constant BSTR
ISpeechObjectTokens._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectToken)), 'Token' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the tokens'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'ppEnumVARIANT' )),
]
SpeechAllElements = -1 # Constant c_int

# values for enumeration 'DISPID_SpeechGrammarRules'
DISPID_SGRsCount = 1
DISPID_SGRsDynamic = 2
DISPID_SGRsAdd = 3
DISPID_SGRsCommit = 4
DISPID_SGRsCommitAndSave = 5
DISPID_SGRsFindRule = 6
DISPID_SGRsItem = 0
DISPID_SGRs_NewEnum = -4
DISPID_SpeechGrammarRules = c_int # enum
class SpCustomStream(CoClass):
    u'SpCustomStream Class'
    _reg_clsid_ = GUID('{8DBEF13F-1948-4AA8-8CF0-048EEBED95D8}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpCustomStream._com_interfaces_ = [ISpeechCustomStream, ISpStream]

ISpeechPhraseElement._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'AudioTimeOffset'), 'propget'], HRESULT, 'AudioTimeOffset',
              ( ['retval', 'out'], POINTER(c_int), 'AudioTimeOffset' )),
    COMMETHOD([dispid(2), helpstring(u'AudioSizeTime'), 'propget'], HRESULT, 'AudioSizeTime',
              ( ['retval', 'out'], POINTER(c_int), 'AudioSizeTime' )),
    COMMETHOD([dispid(3), helpstring(u'AudioStreamOffset'), 'propget'], HRESULT, 'AudioStreamOffset',
              ( ['retval', 'out'], POINTER(c_int), 'AudioStreamOffset' )),
    COMMETHOD([dispid(4), helpstring(u'AudioSizeBytes'), 'propget'], HRESULT, 'AudioSizeBytes',
              ( ['retval', 'out'], POINTER(c_int), 'AudioSizeBytes' )),
    COMMETHOD([dispid(5), helpstring(u'RetainedStreamOffset'), 'propget'], HRESULT, 'RetainedStreamOffset',
              ( ['retval', 'out'], POINTER(c_int), 'RetainedStreamOffset' )),
    COMMETHOD([dispid(6), helpstring(u'RetainedSizeBytes'), 'propget'], HRESULT, 'RetainedSizeBytes',
              ( ['retval', 'out'], POINTER(c_int), 'RetainedSizeBytes' )),
    COMMETHOD([dispid(7), helpstring(u'DisplayText'), 'propget'], HRESULT, 'DisplayText',
              ( ['retval', 'out'], POINTER(BSTR), 'DisplayText' )),
    COMMETHOD([dispid(8), helpstring(u'LexicalForm'), 'propget'], HRESULT, 'LexicalForm',
              ( ['retval', 'out'], POINTER(BSTR), 'LexicalForm' )),
    COMMETHOD([dispid(9), helpstring(u'Pronunciation'), 'propget'], HRESULT, 'Pronunciation',
              ( ['retval', 'out'], POINTER(VARIANT), 'Pronunciation' )),
    COMMETHOD([dispid(10), helpstring(u'DisplayAttributes'), 'propget'], HRESULT, 'DisplayAttributes',
              ( ['retval', 'out'], POINTER(SpeechDisplayAttributes), 'DisplayAttributes' )),
    COMMETHOD([dispid(11), helpstring(u'RequiredConfidence'), 'propget'], HRESULT, 'RequiredConfidence',
              ( ['retval', 'out'], POINTER(SpeechEngineConfidence), 'RequiredConfidence' )),
    COMMETHOD([dispid(12), helpstring(u'ActualConfidence'), 'propget'], HRESULT, 'ActualConfidence',
              ( ['retval', 'out'], POINTER(SpeechEngineConfidence), 'ActualConfidence' )),
    COMMETHOD([dispid(13), helpstring(u'EngineConfidence'), 'propget'], HRESULT, 'EngineConfidence',
              ( ['retval', 'out'], POINTER(c_float), 'EngineConfidence' )),
]
class ISpeechAudioBufferInfo(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechAudioBufferInfo Interface'
    _iid_ = GUID('{11B103D8-1142-4EDF-A093-82FB3915F8CC}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechAudioBufferInfo._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'MinNotification'), 'propget'], HRESULT, 'MinNotification',
              ( ['retval', 'out'], POINTER(c_int), 'MinNotification' )),
    COMMETHOD([dispid(1), helpstring(u'MinNotification'), 'propput'], HRESULT, 'MinNotification',
              ( ['in'], c_int, 'MinNotification' )),
    COMMETHOD([dispid(2), helpstring(u'BufferSize'), 'propget'], HRESULT, 'BufferSize',
              ( ['retval', 'out'], POINTER(c_int), 'BufferSize' )),
    COMMETHOD([dispid(2), helpstring(u'BufferSize'), 'propput'], HRESULT, 'BufferSize',
              ( ['in'], c_int, 'BufferSize' )),
    COMMETHOD([dispid(3), helpstring(u'EventBias'), 'propget'], HRESULT, 'EventBias',
              ( ['retval', 'out'], POINTER(c_int), 'EventBias' )),
    COMMETHOD([dispid(3), helpstring(u'EventBias'), 'propput'], HRESULT, 'EventBias',
              ( ['in'], c_int, 'EventBias' )),
]
Speech_Default_Weight = 1065353216.0 # Constant c_float

# values for enumeration 'DISPID_SpeechRecoContextEvents'
DISPID_SRCEStartStream = 1
DISPID_SRCEEndStream = 2
DISPID_SRCEBookmark = 3
DISPID_SRCESoundStart = 4
DISPID_SRCESoundEnd = 5
DISPID_SRCEPhraseStart = 6
DISPID_SRCERecognition = 7
DISPID_SRCEHypothesis = 8
DISPID_SRCEPropertyNumberChange = 9
DISPID_SRCEPropertyStringChange = 10
DISPID_SRCEFalseRecognition = 11
DISPID_SRCEInterference = 12
DISPID_SRCERequestUI = 13
DISPID_SRCERecognizerStateChange = 14
DISPID_SRCEAdaptation = 15
DISPID_SRCERecognitionForOtherContext = 16
DISPID_SRCEAudioLevel = 17
DISPID_SRCEEnginePrivate = 18
DISPID_SpeechRecoContextEvents = c_int # enum

# values for enumeration 'DISPID_SpeechLexiconWords'
DISPID_SLWsCount = 1
DISPID_SLWsItem = 0
DISPID_SLWs_NewEnum = -4
DISPID_SpeechLexiconWords = c_int # enum
ISpeechPhraseReplacement._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'DisplayAttributes'), 'propget'], HRESULT, 'DisplayAttributes',
              ( ['retval', 'out'], POINTER(SpeechDisplayAttributes), 'DisplayAttributes' )),
    COMMETHOD([dispid(2), helpstring(u'Text'), 'propget'], HRESULT, 'Text',
              ( ['retval', 'out'], POINTER(BSTR), 'Text' )),
    COMMETHOD([dispid(3), helpstring(u'FirstElement'), 'propget'], HRESULT, 'FirstElement',
              ( ['retval', 'out'], POINTER(c_int), 'FirstElement' )),
    COMMETHOD([dispid(4), helpstring(u'NumElements'), 'propget'], HRESULT, 'NumberOfElements',
              ( ['retval', 'out'], POINTER(c_int), 'NumberOfElements' )),
]
ISpNotifySource._methods_ = [
    COMMETHOD([], HRESULT, 'SetNotifySink',
              ( ['in'], POINTER(ISpNotifySink), 'pNotifySink' )),
    COMMETHOD([], HRESULT, 'SetNotifyWindowMessage',
              ( ['in'], wireHWND, 'hWnd' ),
              ( ['in'], c_uint, 'Msg' ),
              ( ['in'], UINT_PTR, 'wParam' ),
              ( ['in'], LONG_PTR, 'lParam' )),
    COMMETHOD([], HRESULT, 'SetNotifyCallbackFunction',
              ( ['in'], POINTER(c_void_p), 'pfnCallback' ),
              ( ['in'], UINT_PTR, 'wParam' ),
              ( ['in'], LONG_PTR, 'lParam' )),
    COMMETHOD([], HRESULT, 'SetNotifyCallbackInterface',
              ( ['in'], POINTER(c_void_p), 'pSpCallback' ),
              ( ['in'], UINT_PTR, 'wParam' ),
              ( ['in'], LONG_PTR, 'lParam' )),
    COMMETHOD([], HRESULT, 'SetNotifyWin32Event'),
    COMMETHOD([], HRESULT, 'WaitForNotifyEvent',
              ( ['in'], c_ulong, 'dwMilliseconds' )),
    COMMETHOD([], c_void_p, 'GetNotifyEventHandle'),
]

# values for enumeration 'DISPID_SpeechObjectToken'
DISPID_SOTId = 1
DISPID_SOTDataKey = 2
DISPID_SOTCategory = 3
DISPID_SOTGetDescription = 4
DISPID_SOTSetId = 5
DISPID_SOTGetAttribute = 6
DISPID_SOTCreateInstance = 7
DISPID_SOTRemove = 8
DISPID_SOTGetStorageFileName = 9
DISPID_SOTRemoveStorageFileName = 10
DISPID_SOTIsUISupported = 11
DISPID_SOTDisplayUI = 12
DISPID_SOTMatchesAttributes = 13
DISPID_SpeechObjectToken = c_int # enum

# values for enumeration 'SpeechRecoContextState'
SRCS_Disabled = 0
SRCS_Enabled = 1
SpeechRecoContextState = c_int # enum

# values for enumeration 'SpeechRetainedAudioOptions'
SRAONone = 0
SRAORetainAudio = 1
SpeechRetainedAudioOptions = c_int # enum
class ISpeechRecoGrammar(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechRecoGrammar Interface'
    _iid_ = GUID('{B6D6F79F-2158-4E50-B5BC-9A9CCD852A09}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechRecoContext._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Recognizer'), 'propget'], HRESULT, 'Recognizer',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecognizer)), 'Recognizer' )),
    COMMETHOD([dispid(2), helpstring(u'AudioInInterferenceStatus'), 'propget'], HRESULT, 'AudioInputInterferenceStatus',
              ( ['retval', 'out'], POINTER(SpeechInterference), 'Interference' )),
    COMMETHOD([dispid(3), helpstring(u'RequestedUIType'), 'propget'], HRESULT, 'RequestedUIType',
              ( ['retval', 'out'], POINTER(BSTR), 'UIType' )),
    COMMETHOD([dispid(4), helpstring(u'Voice'), 'propputref'], HRESULT, 'Voice',
              ( ['in'], POINTER(ISpeechVoice), 'Voice' )),
    COMMETHOD([dispid(4), helpstring(u'Voice'), 'propget'], HRESULT, 'Voice',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechVoice)), 'Voice' )),
    COMMETHOD([dispid(5), helpstring(u'AllowVoiceFormatMatchingOnNextSet'), 'hidden', 'propput'], HRESULT, 'AllowVoiceFormatMatchingOnNextSet',
              ( ['in'], VARIANT_BOOL, 'pAllow' )),
    COMMETHOD([dispid(5), helpstring(u'AllowVoiceFormatMatchingOnNextSet'), 'hidden', 'propget'], HRESULT, 'AllowVoiceFormatMatchingOnNextSet',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'pAllow' )),
    COMMETHOD([dispid(6), helpstring(u'VoicePurgeEvent'), 'propput'], HRESULT, 'VoicePurgeEvent',
              ( ['in'], SpeechRecoEvents, 'EventInterest' )),
    COMMETHOD([dispid(6), helpstring(u'VoicePurgeEvent'), 'propget'], HRESULT, 'VoicePurgeEvent',
              ( ['retval', 'out'], POINTER(SpeechRecoEvents), 'EventInterest' )),
    COMMETHOD([dispid(7), helpstring(u'EventInterests'), 'propput'], HRESULT, 'EventInterests',
              ( ['in'], SpeechRecoEvents, 'EventInterest' )),
    COMMETHOD([dispid(7), helpstring(u'EventInterests'), 'propget'], HRESULT, 'EventInterests',
              ( ['retval', 'out'], POINTER(SpeechRecoEvents), 'EventInterest' )),
    COMMETHOD([dispid(8), helpstring(u'CmdMaxAlternates'), 'propput'], HRESULT, 'CmdMaxAlternates',
              ( ['in'], c_int, 'MaxAlternates' )),
    COMMETHOD([dispid(8), helpstring(u'CmdMaxAlternates'), 'propget'], HRESULT, 'CmdMaxAlternates',
              ( ['retval', 'out'], POINTER(c_int), 'MaxAlternates' )),
    COMMETHOD([dispid(9), helpstring(u'State'), 'propput'], HRESULT, 'State',
              ( ['in'], SpeechRecoContextState, 'State' )),
    COMMETHOD([dispid(9), helpstring(u'State'), 'propget'], HRESULT, 'State',
              ( ['retval', 'out'], POINTER(SpeechRecoContextState), 'State' )),
    COMMETHOD([dispid(10), helpstring(u'RetainedAudio'), 'propput'], HRESULT, 'RetainedAudio',
              ( ['in'], SpeechRetainedAudioOptions, 'Option' )),
    COMMETHOD([dispid(10), helpstring(u'RetainedAudio'), 'propget'], HRESULT, 'RetainedAudio',
              ( ['retval', 'out'], POINTER(SpeechRetainedAudioOptions), 'Option' )),
    COMMETHOD([dispid(11), helpstring(u'RetainedAudioFormat'), 'propputref'], HRESULT, 'RetainedAudioFormat',
              ( ['in'], POINTER(ISpeechAudioFormat), 'Format' )),
    COMMETHOD([dispid(11), helpstring(u'RetainedAudioFormat'), 'propget'], HRESULT, 'RetainedAudioFormat',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioFormat)), 'Format' )),
    COMMETHOD([dispid(12), helpstring(u'Pause')], HRESULT, 'Pause'),
    COMMETHOD([dispid(13), helpstring(u'Resume')], HRESULT, 'Resume'),
    COMMETHOD([dispid(14), helpstring(u'CreateGrammar')], HRESULT, 'CreateGrammar',
              ( ['in', 'optional'], VARIANT, 'GrammarId', 0 ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecoGrammar)), 'Grammar' )),
    COMMETHOD([dispid(15), helpstring(u'CreateResultFromMemory')], HRESULT, 'CreateResultFromMemory',
              ( ['in'], POINTER(VARIANT), 'ResultBlock' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecoResult)), 'Result' )),
    COMMETHOD([dispid(16), helpstring(u'Bookmark')], HRESULT, 'Bookmark',
              ( ['in'], SpeechBookmarkOptions, 'Options' ),
              ( ['in'], VARIANT, 'StreamPos' ),
              ( ['in'], VARIANT, 'BookmarkId' )),
    COMMETHOD([dispid(17), helpstring(u'SetAdaptationData')], HRESULT, 'SetAdaptationData',
              ( ['in'], BSTR, 'AdaptationString' )),
]
class ISpVoice(ISpEventSource):
    _case_insensitive_ = True
    u'ISpVoice Interface'
    _iid_ = GUID('{6C44DF74-72B9-4992-A1EC-EF996E0422D4}')
    _idlflags_ = ['restricted']
ISpEventSource._methods_ = [
    COMMETHOD([], HRESULT, 'SetInterest',
              ( ['in'], c_ulonglong, 'ullEventInterest' ),
              ( ['in'], c_ulonglong, 'ullQueuedInterest' )),
    COMMETHOD([], HRESULT, 'GetEvents',
              ( ['in'], c_ulong, 'ulCount' ),
              ( ['out'], POINTER(SPEVENT), 'pEventArray' ),
              ( ['out'], POINTER(c_ulong), 'pulFetched' )),
    COMMETHOD([], HRESULT, 'GetInfo',
              ( ['out'], POINTER(SPEVENTSOURCEINFO), 'pInfo' )),
]
class SPVOICESTATUS(Structure):
    pass
ISpVoice._methods_ = [
    COMMETHOD([], HRESULT, 'SetOutput',
              ( ['in'], POINTER(IUnknown), 'pUnkOutput' ),
              ( ['in'], c_int, 'fAllowFormatChanges' )),
    COMMETHOD([], HRESULT, 'GetOutputObjectToken',
              ( ['out'], POINTER(POINTER(ISpObjectToken)), 'ppObjectToken' )),
    COMMETHOD([], HRESULT, 'GetOutputStream',
              ( ['out'], POINTER(POINTER(ISpStreamFormat)), 'ppStream' )),
    COMMETHOD([], HRESULT, 'Pause'),
    COMMETHOD([], HRESULT, 'Resume'),
    COMMETHOD([], HRESULT, 'SetVoice',
              ( ['in'], POINTER(ISpObjectToken), 'pToken' )),
    COMMETHOD([], HRESULT, 'GetVoice',
              ( ['out'], POINTER(POINTER(ISpObjectToken)), 'ppToken' )),
    COMMETHOD([], HRESULT, 'Speak',
              ( ['in'], WSTRING, 'pwcs' ),
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['out'], POINTER(c_ulong), 'pulStreamNumber' )),
    COMMETHOD([], HRESULT, 'SpeakStream',
              ( ['in'], POINTER(IStream), 'pStream' ),
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['out'], POINTER(c_ulong), 'pulStreamNumber' )),
    COMMETHOD([], HRESULT, 'GetStatus',
              ( ['out'], POINTER(SPVOICESTATUS), 'pStatus' ),
              ( ['out'], POINTER(WSTRING), 'ppszLastBookmark' )),
    COMMETHOD([], HRESULT, 'Skip',
              ( ['in'], WSTRING, 'pItemType' ),
              ( ['in'], c_int, 'lNumItems' ),
              ( ['out'], POINTER(c_ulong), 'pulNumSkipped' )),
    COMMETHOD([], HRESULT, 'SetPriority',
              ( ['in'], SPVPRIORITY, 'ePriority' )),
    COMMETHOD([], HRESULT, 'GetPriority',
              ( ['out'], POINTER(SPVPRIORITY), 'pePriority' )),
    COMMETHOD([], HRESULT, 'SetAlertBoundary',
              ( ['in'], SPEVENTENUM, 'eBoundary' )),
    COMMETHOD([], HRESULT, 'GetAlertBoundary',
              ( ['out'], POINTER(SPEVENTENUM), 'peBoundary' )),
    COMMETHOD([], HRESULT, 'SetRate',
              ( ['in'], c_int, 'RateAdjust' )),
    COMMETHOD([], HRESULT, 'GetRate',
              ( ['out'], POINTER(c_int), 'pRateAdjust' )),
    COMMETHOD([], HRESULT, 'SetVolume',
              ( ['in'], c_ushort, 'usVolume' )),
    COMMETHOD([], HRESULT, 'GetVolume',
              ( ['out'], POINTER(c_ushort), 'pusVolume' )),
    COMMETHOD([], HRESULT, 'WaitUntilDone',
              ( ['in'], c_ulong, 'msTimeout' )),
    COMMETHOD([], HRESULT, 'SetSyncSpeakTimeout',
              ( ['in'], c_ulong, 'msTimeout' )),
    COMMETHOD([], HRESULT, 'GetSyncSpeakTimeout',
              ( ['out'], POINTER(c_ulong), 'pmsTimeout' )),
    COMMETHOD([], c_void_p, 'SpeakCompleteEvent'),
    COMMETHOD([], HRESULT, 'IsUISupported',
              ( ['in'], POINTER(c_ushort), 'pszTypeOfUI' ),
              ( ['in'], c_void_p, 'pvExtraData' ),
              ( ['in'], c_ulong, 'cbExtraData' ),
              ( ['out'], POINTER(c_int), 'pfSupported' )),
    COMMETHOD([], HRESULT, 'DisplayUI',
              ( ['in'], wireHWND, 'hWndParent' ),
              ( ['in'], POINTER(c_ushort), 'pszTitle' ),
              ( ['in'], POINTER(c_ushort), 'pszTypeOfUI' ),
              ( ['in'], c_void_p, 'pvExtraData' ),
              ( ['in'], c_ulong, 'cbExtraData' )),
]

# values for enumeration 'SPCONTEXTSTATE'
SPCS_DISABLED = 0
SPCS_ENABLED = 1
SPCONTEXTSTATE = c_int # enum
Speech_Max_Pron_Length = 384 # Constant c_int
class SpVoice(CoClass):
    u'SpVoice Class'
    _reg_clsid_ = GUID('{96749377-3391-11D2-9EE3-00C04F797396}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
class _ISpeechVoiceEvents(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{A372ACD1-3BEF-4BBD-8FFB-CB3E2B416AF8}')
    _idlflags_ = []
    _methods_ = []
SpVoice._com_interfaces_ = [ISpeechVoice, ISpVoice]
SpVoice._outgoing_interfaces_ = [_ISpeechVoiceEvents]

class ISpeechMemoryStream(ISpeechBaseStream):
    _case_insensitive_ = True
    u'ISpeechMemoryStream Interface'
    _iid_ = GUID('{EEB14B68-808B-4ABE-A5EA-B51DA7588008}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechMemoryStream._methods_ = [
    COMMETHOD([dispid(100), helpstring(u'SetData')], HRESULT, 'SetData',
              ( ['in'], VARIANT, 'Data' )),
    COMMETHOD([dispid(101), helpstring(u'GetData')], HRESULT, 'GetData',
              ( ['retval', 'out'], POINTER(VARIANT), 'pData' )),
]
class _RemotableHandle(Structure):
    pass
class __MIDL_IWinTypes_0009(Union):
    pass
__MIDL_IWinTypes_0009._fields_ = [
    ('hInproc', c_int),
    ('hRemote', c_int),
]
assert sizeof(__MIDL_IWinTypes_0009) == 4, sizeof(__MIDL_IWinTypes_0009)
assert alignment(__MIDL_IWinTypes_0009) == 4, alignment(__MIDL_IWinTypes_0009)
_RemotableHandle._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0009),
]
assert sizeof(_RemotableHandle) == 8, sizeof(_RemotableHandle)
assert alignment(_RemotableHandle) == 4, alignment(_RemotableHandle)
SpeechDictationTopicSpelling = u'Spelling' # Constant BSTR
ISpRecoContext._methods_ = [
    COMMETHOD([], HRESULT, 'GetRecognizer',
              ( ['out'], POINTER(POINTER(ISpRecognizer)), 'ppRecognizer' )),
    COMMETHOD([], HRESULT, 'CreateGrammar',
              ( ['in'], c_ulonglong, 'ullGrammarID' ),
              ( ['out'], POINTER(POINTER(ISpRecoGrammar)), 'ppGrammar' )),
    COMMETHOD([], HRESULT, 'GetStatus',
              ( ['out'], POINTER(SPRECOCONTEXTSTATUS), 'pStatus' )),
    COMMETHOD([], HRESULT, 'GetMaxAlternates',
              ( ['in'], POINTER(c_ulong), 'pcAlternates' )),
    COMMETHOD([], HRESULT, 'SetMaxAlternates',
              ( ['in'], c_ulong, 'cAlternates' )),
    COMMETHOD([], HRESULT, 'SetAudioOptions',
              ( ['in'], SPAUDIOOPTIONS, 'Options' ),
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pAudioFormatId' ),
              ( ['in'], POINTER(WaveFormatEx), 'pWaveFormatEx' )),
    COMMETHOD([], HRESULT, 'GetAudioOptions',
              ( ['in'], POINTER(SPAUDIOOPTIONS), 'pOptions' ),
              ( ['out'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pAudioFormatId' ),
              ( ['out'], POINTER(POINTER(WaveFormatEx)), 'ppCoMemWFEX' )),
    COMMETHOD([], HRESULT, 'DeserializeResult',
              ( ['in'], POINTER(SPSERIALIZEDRESULT), 'pSerializedResult' ),
              ( ['out'], POINTER(POINTER(ISpRecoResult)), 'ppResult' )),
    COMMETHOD([], HRESULT, 'Bookmark',
              ( ['in'], SPBOOKMARKOPTIONS, 'Options' ),
              ( ['in'], c_ulonglong, 'ullStreamPosition' ),
              ( ['in'], LONG_PTR, 'lparamEvent' )),
    COMMETHOD([], HRESULT, 'SetAdaptationData',
              ( ['in'], WSTRING, 'pAdaptationData' ),
              ( ['in'], c_ulong, 'cch' )),
    COMMETHOD([], HRESULT, 'Pause',
              ( [], c_ulong, 'dwReserved' )),
    COMMETHOD([], HRESULT, 'Resume',
              ( [], c_ulong, 'dwReserved' )),
    COMMETHOD([], HRESULT, 'SetVoice',
              ( ['in'], POINTER(ISpVoice), 'pVoice' ),
              ( ['in'], c_int, 'fAllowFormatChanges' )),
    COMMETHOD([], HRESULT, 'GetVoice',
              ( ['out'], POINTER(POINTER(ISpVoice)), 'ppVoice' )),
    COMMETHOD([], HRESULT, 'SetVoicePurgeEvent',
              ( ['in'], c_ulonglong, 'ullEventInterest' )),
    COMMETHOD([], HRESULT, 'GetVoicePurgeEvent',
              ( ['out'], POINTER(c_ulonglong), 'pullEventInterest' )),
    COMMETHOD([], HRESULT, 'SetContextState',
              ( ['in'], SPCONTEXTSTATE, 'eContextState' )),
    COMMETHOD([], HRESULT, 'GetContextState',
              ( ['in'], POINTER(SPCONTEXTSTATE), 'peContextState' )),
]

# values for enumeration 'SpeechSpecialTransitionType'
SSTTWildcard = 1
SSTTDictation = 2
SSTTTextBuffer = 3
SpeechSpecialTransitionType = c_int # enum
ISpeechGrammarRuleState._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Rule'), 'propget'], HRESULT, 'Rule',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRule)), 'Rule' )),
    COMMETHOD([dispid(2), helpstring(u'Transitions'), 'propget'], HRESULT, 'Transitions',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRuleStateTransitions)), 'Transitions' )),
    COMMETHOD([dispid(3), helpstring(u'AddWordTransition')], HRESULT, 'AddWordTransition',
              ( ['in'], POINTER(ISpeechGrammarRuleState), 'DestState' ),
              ( ['in'], BSTR, 'Words' ),
              ( ['in', 'optional'], BSTR, 'Separators', u' ' ),
              ( ['in', 'optional'], SpeechGrammarWordType, 'Type', 1 ),
              ( ['in', 'optional'], BSTR, 'PropertyName', u'' ),
              ( ['in', 'optional'], c_int, 'PropertyId', 0 ),
              ( ['in', 'optional'], POINTER(VARIANT), 'PropertyValue', u'' ),
              ( ['in', 'optional'], c_float, 'Weight', 1.0 )),
    COMMETHOD([dispid(4), helpstring(u'AddRuleTransition')], HRESULT, 'AddRuleTransition',
              ( ['in'], POINTER(ISpeechGrammarRuleState), 'DestinationState' ),
              ( ['in'], POINTER(ISpeechGrammarRule), 'Rule' ),
              ( ['in', 'optional'], BSTR, 'PropertyName', u'' ),
              ( ['in', 'optional'], c_int, 'PropertyId', 0 ),
              ( ['in', 'optional'], POINTER(VARIANT), 'PropertyValue', u'' ),
              ( ['in', 'optional'], c_float, 'Weight', 1.0 )),
    COMMETHOD([dispid(5), helpstring(u'AddSpecialTransition')], HRESULT, 'AddSpecialTransition',
              ( ['in'], POINTER(ISpeechGrammarRuleState), 'DestinationState' ),
              ( ['in'], SpeechSpecialTransitionType, 'Type' ),
              ( ['in', 'optional'], BSTR, 'PropertyName', u'' ),
              ( ['in', 'optional'], c_int, 'PropertyId', 0 ),
              ( ['in', 'optional'], POINTER(VARIANT), 'PropertyValue', u'' ),
              ( ['in', 'optional'], c_float, 'Weight', 1.0 )),
]
class SpResourceManager(CoClass):
    u'SpResourceManger'
    _reg_clsid_ = GUID('{96749373-3391-11D2-9EE3-00C04F797396}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpResourceManager._com_interfaces_ = [ISpResourceManager]


# values for enumeration 'DISPID_SpeechMMSysAudio'
DISPID_SMSADeviceId = 300
DISPID_SMSALineId = 301
DISPID_SMSAMMHandle = 302
DISPID_SpeechMMSysAudio = c_int # enum
SpeechVoiceCategoryTTSRate = u'DefaultTTSRate' # Constant BSTR

# values for enumeration 'SpeechRuleState'
SGDSInactive = 0
SGDSActive = 1
SGDSActiveWithAutoPause = 3
SpeechRuleState = c_int # enum
SPPHRASEPROPERTY._fields_ = [
    ('pszName', POINTER(c_ushort)),
    ('ulId', c_ulong),
    ('pszValue', POINTER(c_ushort)),
    ('vValue', VARIANT),
    ('ulFirstElement', c_ulong),
    ('ulCountOfElements', c_ulong),
    ('pNextSibling', POINTER(SPPHRASEPROPERTY)),
    ('pFirstChild', POINTER(SPPHRASEPROPERTY)),
    ('SREngineConfidence', c_float),
    ('Confidence', c_char),
]
assert sizeof(SPPHRASEPROPERTY) == 56, sizeof(SPPHRASEPROPERTY)
assert alignment(SPPHRASEPROPERTY) == 8, alignment(SPPHRASEPROPERTY)
class SpMemoryStream(CoClass):
    u'SpMemoryStream Class'
    _reg_clsid_ = GUID('{5FB7EF7D-DFF4-468A-B6B7-2FCBD188F994}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpMemoryStream._com_interfaces_ = [ISpeechMemoryStream, ISpStream]

class SpMMAudioIn(CoClass):
    u'SpMMAudioIn Class'
    _reg_clsid_ = GUID('{CF3D2E50-53F2-11D2-960C-00C04F8EE628}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpMMAudioIn._com_interfaces_ = [ISpeechMMSysAudio, ISpEventSource, ISpEventSink, ISpObjectWithToken, ISpMMSysAudio]


# values for enumeration 'DISPID_SpeechPhraseRules'
DISPID_SPRulesCount = 1
DISPID_SPRulesItem = 0
DISPID_SPRules_NewEnum = -4
DISPID_SpeechPhraseRules = c_int # enum
class ISpeechPhraseRules(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseRules Interface'
    _iid_ = GUID('{9047D593-01DD-4B72-81A3-E4A0CA69F407}')
    _idlflags_ = ['dual', 'oleautomation']
class ISpeechPhraseRule(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechPhraseRule Interface'
    _iid_ = GUID('{A7BFE112-A4A0-48D9-B602-C313843F6964}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechPhraseRules._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseRule)), 'Rule' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the Rules'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]
tagSPPROPERTYINFO._fields_ = [
    ('pszName', POINTER(c_ushort)),
    ('ulId', c_ulong),
    ('pszValue', POINTER(c_ushort)),
    ('vValue', VARIANT),
]
assert sizeof(tagSPPROPERTYINFO) == 32, sizeof(tagSPPROPERTYINFO)
assert alignment(tagSPPROPERTYINFO) == 8, alignment(tagSPPROPERTYINFO)

# values for enumeration 'SpeechDiscardType'
SDTProperty = 1
SDTReplacement = 2
SDTRule = 4
SDTDisplayText = 8
SDTLexicalForm = 16
SDTPronunciation = 32
SDTAudio = 64
SDTAlternates = 128
SDTAll = 255
SpeechDiscardType = c_int # enum
SPSERIALIZEDRESULT._fields_ = [
    ('ulSerializedSize', c_ulong),
]
assert sizeof(SPSERIALIZEDRESULT) == 4, sizeof(SPSERIALIZEDRESULT)
assert alignment(SPSERIALIZEDRESULT) == 4, alignment(SPSERIALIZEDRESULT)
class SpMMAudioEnum(CoClass):
    u'SpMMAudioEnum Class'
    _reg_clsid_ = GUID('{AB1890A0-E91F-11D2-BB91-00C04F8EE6C0}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpMMAudioEnum._com_interfaces_ = [IEnumSpObjectTokens]


# values for enumeration 'DISPID_SpeechPhraseElements'
DISPID_SPEsCount = 1
DISPID_SPEsItem = 0
DISPID_SPEs_NewEnum = -4
DISPID_SpeechPhraseElements = c_int # enum
class ISpeechGrammarRules(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechGrammarRules Interface'
    _iid_ = GUID('{6FFA3B44-FC2D-40D1-8AFC-32911C7F1AD1}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechGrammarRules._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(6), helpstring(u'FindRule')], HRESULT, 'FindRule',
              ( ['in'], VARIANT, 'RuleNameOrId' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRule)), 'Rule' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRule)), 'Rule' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the alternates'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
    COMMETHOD([dispid(2), helpstring(u'Dynamic'), 'propget'], HRESULT, 'Dynamic',
              ( ['retval', 'out'], POINTER(VARIANT_BOOL), 'Dynamic' )),
    COMMETHOD([dispid(3), helpstring(u'Add')], HRESULT, 'Add',
              ( ['in'], BSTR, 'RuleName' ),
              ( ['in'], SpeechRuleAttributes, 'Attributes' ),
              ( ['in', 'optional'], c_int, 'RuleId', 0 ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRule)), 'Rule' )),
    COMMETHOD([dispid(4), helpstring(u'Commit')], HRESULT, 'Commit'),
    COMMETHOD([dispid(5), helpstring(u'CommitAndSave')], HRESULT, 'CommitAndSave',
              ( ['out'], POINTER(BSTR), 'ErrorText' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'SaveStream' )),
]

# values for enumeration 'DISPID_SpeechVoiceStatus'
DISPID_SVSCurrentStreamNumber = 1
DISPID_SVSLastStreamNumberQueued = 2
DISPID_SVSLastResult = 3
DISPID_SVSRunningState = 4
DISPID_SVSInputWordPosition = 5
DISPID_SVSInputWordLength = 6
DISPID_SVSInputSentencePosition = 7
DISPID_SVSInputSentenceLength = 8
DISPID_SVSLastBookmark = 9
DISPID_SVSLastBookmarkId = 10
DISPID_SVSPhonemeId = 11
DISPID_SVSVisemeId = 12
DISPID_SpeechVoiceStatus = c_int # enum

# values for enumeration 'SpeechVisemeFeature'
SVF_None = 0
SVF_Stressed = 1
SVF_Emphasis = 2
SpeechVisemeFeature = c_int # enum
ISpeechRecoResult._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'RecoContext'), 'propget'], HRESULT, 'RecoContext',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecoContext)), 'RecoContext' )),
    COMMETHOD([dispid(2), helpstring(u'Times'), 'propget'], HRESULT, 'Times',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecoResultTimes)), 'Times' )),
    COMMETHOD([dispid(3), helpstring(u'AudioFormat'), 'propputref'], HRESULT, 'AudioFormat',
              ( ['in'], POINTER(ISpeechAudioFormat), 'Format' )),
    COMMETHOD([dispid(3), helpstring(u'AudioFormat'), 'propget'], HRESULT, 'AudioFormat',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioFormat)), 'Format' )),
    COMMETHOD([dispid(4), helpstring(u'PhraseInfo'), 'propget'], HRESULT, 'PhraseInfo',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseInfo)), 'PhraseInfo' )),
    COMMETHOD([dispid(5), helpstring(u'Alternates')], HRESULT, 'Alternates',
              ( ['in'], c_int, 'RequestCount' ),
              ( ['in', 'optional'], c_int, 'StartElement', 0 ),
              ( ['in', 'optional'], c_int, 'Elements', -1 ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseAlternates)), 'Alternates' )),
    COMMETHOD([dispid(6), helpstring(u'Audio')], HRESULT, 'Audio',
              ( ['in', 'optional'], c_int, 'StartElement', 0 ),
              ( ['in', 'optional'], c_int, 'Elements', -1 ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechMemoryStream)), 'Stream' )),
    COMMETHOD([dispid(7), helpstring(u'SpeakAudio')], HRESULT, 'SpeakAudio',
              ( ['in', 'optional'], c_int, 'StartElement', 0 ),
              ( ['in', 'optional'], c_int, 'Elements', -1 ),
              ( ['in', 'optional'], SpeechVoiceSpeakFlags, 'Flags', 0 ),
              ( ['retval', 'out'], POINTER(c_int), 'StreamNumber' )),
    COMMETHOD([dispid(8), helpstring(u'SaveToMemory')], HRESULT, 'SaveToMemory',
              ( ['retval', 'out'], POINTER(VARIANT), 'ResultBlock' )),
    COMMETHOD([dispid(9), helpstring(u'DiscardResultInfo')], HRESULT, 'DiscardResultInfo',
              ( ['in'], SpeechDiscardType, 'ValueTypes' )),
]
SpeechCategoryPhoneConverters = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\PhoneConverters' # Constant BSTR

# values for enumeration 'DISPID_SpeechVoiceEvent'
DISPID_SVEStreamStart = 1
DISPID_SVEStreamEnd = 2
DISPID_SVEVoiceChange = 3
DISPID_SVEBookmark = 4
DISPID_SVEWord = 5
DISPID_SVEPhoneme = 6
DISPID_SVESentenceBoundary = 7
DISPID_SVEViseme = 8
DISPID_SVEAudioLevel = 9
DISPID_SVEEnginePrivate = 10
DISPID_SpeechVoiceEvent = c_int # enum
class ISpeechLexiconPronunciation(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    u'ISpeechLexiconPronunciation Interface'
    _iid_ = GUID('{95252C5D-9E43-4F4A-9899-48EE73352F9F}')
    _idlflags_ = ['dual', 'oleautomation']
ISpeechLexiconPronunciation._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Type'), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(SpeechLexiconType), 'LexiconType' )),
    COMMETHOD([dispid(2), helpstring(u'LangId'), 'propget'], HRESULT, 'LangId',
              ( ['retval', 'out'], POINTER(c_int), 'LangId' )),
    COMMETHOD([dispid(3), helpstring(u'PartOfSpeech'), 'propget'], HRESULT, 'PartOfSpeech',
              ( ['retval', 'out'], POINTER(SpeechPartOfSpeech), 'PartOfSpeech' )),
    COMMETHOD([dispid(4), helpstring(u'PhoneIds'), 'propget'], HRESULT, 'PhoneIds',
              ( ['retval', 'out'], POINTER(VARIANT), 'PhoneIds' )),
    COMMETHOD([dispid(5), helpstring(u'Symbolic'), 'propget'], HRESULT, 'Symbolic',
              ( ['retval', 'out'], POINTER(BSTR), 'Symbolic' )),
]
ISpeechLexiconPronunciations._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Count'), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'Count' )),
    COMMETHOD([dispid(0), helpstring(u'Item')], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechLexiconPronunciation)), 'Pronunciation' )),
    COMMETHOD([dispid(-4), helpstring(u'Enumerates the tokens'), 'restricted', 'propget'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'EnumVARIANT' )),
]
ISpeechAudio._methods_ = [
    COMMETHOD([dispid(200), helpstring(u'Status'), 'propget'], HRESULT, 'Status',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioStatus)), 'Status' )),
    COMMETHOD([dispid(201), helpstring(u'BufferInfo'), 'propget'], HRESULT, 'BufferInfo',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioBufferInfo)), 'BufferInfo' )),
    COMMETHOD([dispid(202), helpstring(u'DefaultFormat'), 'propget'], HRESULT, 'DefaultFormat',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioFormat)), 'StreamFormat' )),
    COMMETHOD([dispid(203), helpstring(u'Volume'), 'propget'], HRESULT, 'Volume',
              ( ['retval', 'out'], POINTER(c_int), 'Volume' )),
    COMMETHOD([dispid(203), helpstring(u'Volume'), 'propput'], HRESULT, 'Volume',
              ( ['in'], c_int, 'Volume' )),
    COMMETHOD([dispid(204), helpstring(u'BufferNotifySize'), 'propget'], HRESULT, 'BufferNotifySize',
              ( ['retval', 'out'], POINTER(c_int), 'BufferNotifySize' )),
    COMMETHOD([dispid(204), helpstring(u'BufferNotifySize'), 'propput'], HRESULT, 'BufferNotifySize',
              ( ['in'], c_int, 'BufferNotifySize' )),
    COMMETHOD([dispid(205), helpstring(u'EventHandle'), 'hidden', 'propget'], HRESULT, 'EventHandle',
              ( ['retval', 'out'], POINTER(c_int), 'EventHandle' )),
    COMMETHOD([dispid(206), helpstring(u'SetState'), 'hidden'], HRESULT, 'SetState',
              ( ['in'], SpeechAudioState, 'State' )),
]
SpeechAudioProperties = u'AudioProperties' # Constant BSTR
class SpCompressedLexicon(CoClass):
    u'SpCompressedLexicon Class'
    _reg_clsid_ = GUID('{90903716-2F42-11D3-9C26-00C04F8EF87C}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpCompressedLexicon._com_interfaces_ = [ISpLexicon, ISpObjectWithToken]


# values for enumeration 'DISPID_SpeechPhraseBuilder'
DISPID_SPPBRestorePhraseFromMemory = 1
DISPID_SpeechPhraseBuilder = c_int # enum

# values for enumeration 'SpeechLoadOption'
SLOStatic = 0
SLODynamic = 1
SpeechLoadOption = c_int # enum
ISpeechRecoGrammar._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Id'), 'propget'], HRESULT, 'Id',
              ( ['retval', 'out'], POINTER(VARIANT), 'Id' )),
    COMMETHOD([dispid(2), helpstring(u'RecoContext'), 'propget'], HRESULT, 'RecoContext',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechRecoContext)), 'RecoContext' )),
    COMMETHOD([dispid(3), helpstring(u'State'), 'propput'], HRESULT, 'State',
              ( ['in'], SpeechGrammarState, 'State' )),
    COMMETHOD([dispid(3), helpstring(u'State'), 'propget'], HRESULT, 'State',
              ( ['retval', 'out'], POINTER(SpeechGrammarState), 'State' )),
    COMMETHOD([dispid(4), helpstring(u'Rules'), 'propget'], HRESULT, 'Rules',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechGrammarRules)), 'Rules' )),
    COMMETHOD([dispid(5), helpstring(u'Reset')], HRESULT, 'Reset',
              ( ['in', 'optional'], c_int, 'NewLanguage', 0 )),
    COMMETHOD([dispid(7), helpstring(u'CmdLoadFromFile')], HRESULT, 'CmdLoadFromFile',
              ( ['in'], BSTR, 'FileName' ),
              ( ['in', 'optional'], SpeechLoadOption, 'LoadOption', 0 )),
    COMMETHOD([dispid(8), helpstring(u'CmdLoadFromObject')], HRESULT, 'CmdLoadFromObject',
              ( ['in'], BSTR, 'ClassId' ),
              ( ['in'], BSTR, 'GrammarName' ),
              ( ['in', 'optional'], SpeechLoadOption, 'LoadOption', 0 )),
    COMMETHOD([dispid(9), helpstring(u'CmdLoadFromResource')], HRESULT, 'CmdLoadFromResource',
              ( ['in'], c_int, 'hModule' ),
              ( ['in'], VARIANT, 'ResourceName' ),
              ( ['in'], VARIANT, 'ResourceType' ),
              ( ['in'], c_int, 'LanguageId' ),
              ( ['in', 'optional'], SpeechLoadOption, 'LoadOption', 0 )),
    COMMETHOD([dispid(10), helpstring(u'CmdLoadFromMemory')], HRESULT, 'CmdLoadFromMemory',
              ( ['in'], VARIANT, 'GrammarData' ),
              ( ['in', 'optional'], SpeechLoadOption, 'LoadOption', 0 )),
    COMMETHOD([dispid(11), helpstring(u'CmdLoadFromProprietaryGrammar')], HRESULT, 'CmdLoadFromProprietaryGrammar',
              ( ['in'], BSTR, 'ProprietaryGuid' ),
              ( ['in'], BSTR, 'ProprietaryString' ),
              ( ['in'], VARIANT, 'ProprietaryData' ),
              ( ['in', 'optional'], SpeechLoadOption, 'LoadOption', 0 )),
    COMMETHOD([dispid(12), helpstring(u'CmdSetRuleState')], HRESULT, 'CmdSetRuleState',
              ( ['in'], BSTR, 'Name' ),
              ( ['in'], SpeechRuleState, 'State' )),
    COMMETHOD([dispid(13), helpstring(u'CmdSetRuleIdState')], HRESULT, 'CmdSetRuleIdState',
              ( ['in'], c_int, 'RuleId' ),
              ( ['in'], SpeechRuleState, 'State' )),
    COMMETHOD([dispid(14), helpstring(u'DictationLoad')], HRESULT, 'DictationLoad',
              ( ['in', 'optional'], BSTR, 'TopicName', u'' ),
              ( ['in', 'optional'], SpeechLoadOption, 'LoadOption', 0 )),
    COMMETHOD([dispid(15), helpstring(u'DictationUnload')], HRESULT, 'DictationUnload'),
    COMMETHOD([dispid(16), helpstring(u'DictationSetState')], HRESULT, 'DictationSetState',
              ( ['in'], SpeechRuleState, 'State' )),
    COMMETHOD([dispid(17), helpstring(u'SetWordSequenceData')], HRESULT, 'SetWordSequenceData',
              ( ['in'], BSTR, 'Text' ),
              ( ['in'], c_int, 'TextLength' ),
              ( ['in'], POINTER(ISpeechTextSelectionInformation), 'Info' )),
    COMMETHOD([dispid(18), helpstring(u'SetTextSelection')], HRESULT, 'SetTextSelection',
              ( ['in'], POINTER(ISpeechTextSelectionInformation), 'Info' )),
    COMMETHOD([dispid(19), helpstring(u'IsPronounceable')], HRESULT, 'IsPronounceable',
              ( ['in'], BSTR, 'Word' ),
              ( ['retval', 'out'], POINTER(SpeechWordPronounceable), 'WordPronounceable' )),
]
ISpeechObjectTokenCategory._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Id'), 'propget'], HRESULT, 'Id',
              ( ['retval', 'out'], POINTER(BSTR), 'Id' )),
    COMMETHOD([dispid(2), helpstring(u'Default'), 'propput'], HRESULT, 'Default',
              ( ['in'], BSTR, 'TokenId' )),
    COMMETHOD([dispid(2), helpstring(u'Default'), 'propget'], HRESULT, 'Default',
              ( ['retval', 'out'], POINTER(BSTR), 'TokenId' )),
    COMMETHOD([dispid(3), helpstring(u'SetId')], HRESULT, 'SetId',
              ( ['in'], BSTR, 'Id' ),
              ( ['in', 'optional'], VARIANT_BOOL, 'CreateIfNotExist', False )),
    COMMETHOD([dispid(4), helpstring(u'GetDataKey'), 'hidden'], HRESULT, 'GetDataKey',
              ( ['in', 'optional'], SpeechDataKeyLocation, 'Location', 0 ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechDataKey)), 'DataKey' )),
    COMMETHOD([dispid(5), helpstring(u'EnumerateTokens')], HRESULT, 'EnumerateTokens',
              ( ['in', 'optional'], BSTR, 'RequiredAttributes', u'' ),
              ( ['in', 'optional'], BSTR, 'OptionalAttributes', u'' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechObjectTokens)), 'Tokens' )),
]
SpeechGrammarTagWildcard = u'...' # Constant BSTR
SPWORDPRONUNCIATION._fields_ = [
    ('pNextWordPronunciation', POINTER(SPWORDPRONUNCIATION)),
    ('eLexiconType', SPLEXICONTYPE),
    ('LangId', c_ushort),
    ('wReserved', c_ushort),
    ('ePartOfSpeech', SPPARTOFSPEECH),
    ('szPronunciation', c_ushort * 1),
]
assert sizeof(SPWORDPRONUNCIATION) == 20, sizeof(SPWORDPRONUNCIATION)
assert alignment(SPWORDPRONUNCIATION) == 4, alignment(SPWORDPRONUNCIATION)

# values for enumeration 'DISPID_SpeechAudioStatus'
DISPID_SASFreeBufferSpace = 1
DISPID_SASNonBlockingIO = 2
DISPID_SASState = 3
DISPID_SASCurrentSeekPosition = 4
DISPID_SASCurrentDevicePosition = 5
DISPID_SpeechAudioStatus = c_int # enum
SpeechPropertyResourceUsage = u'ResourceUsage' # Constant BSTR

# values for enumeration 'DISPID_SpeechPhraseRule'
DISPID_SPRuleName = 1
DISPID_SPRuleId = 2
DISPID_SPRuleFirstElement = 3
DISPID_SPRuleNumberOfElements = 4
DISPID_SPRuleParent = 5
DISPID_SPRuleChildren = 6
DISPID_SPRuleConfidence = 7
DISPID_SPRuleEngineConfidence = 8
DISPID_SpeechPhraseRule = c_int # enum
ISpStreamFormatConverter._methods_ = [
    COMMETHOD([], HRESULT, 'SetBaseStream',
              ( ['in'], POINTER(ISpStreamFormat), 'pStream' ),
              ( ['in'], c_int, 'fSetFormatToBaseStreamFormat' ),
              ( ['in'], c_int, 'fWriteToBaseStream' )),
    COMMETHOD([], HRESULT, 'GetBaseStream',
              ( ['out'], POINTER(POINTER(ISpStreamFormat)), 'ppStream' )),
    COMMETHOD([], HRESULT, 'SetFormat',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'rguidFormatIdOfConvertedStream' ),
              ( ['in'], POINTER(WaveFormatEx), 'pWaveFormatExOfConvertedStream' )),
    COMMETHOD([], HRESULT, 'ResetSeekPosition'),
    COMMETHOD([], HRESULT, 'ScaleConvertedToBaseOffset',
              ( ['in'], c_ulonglong, 'ullOffsetConvertedStream' ),
              ( ['out'], POINTER(c_ulonglong), 'pullOffsetBaseStream' )),
    COMMETHOD([], HRESULT, 'ScaleBaseToConvertedOffset',
              ( ['in'], c_ulonglong, 'ullOffsetBaseStream' ),
              ( ['out'], POINTER(c_ulonglong), 'pullOffsetConvertedStream' )),
]
SpeechCategoryAppLexicons = u'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\AppLexicons' # Constant BSTR

# values for enumeration 'DISPID_SpeechGrammarRuleStateTransition'
DISPID_SGRSTType = 1
DISPID_SGRSTText = 2
DISPID_SGRSTRule = 3
DISPID_SGRSTWeight = 4
DISPID_SGRSTPropertyName = 5
DISPID_SGRSTPropertyId = 6
DISPID_SGRSTPropertyValue = 7
DISPID_SGRSTNextState = 8
DISPID_SpeechGrammarRuleStateTransition = c_int # enum
ISpeechLexiconWord._methods_ = [
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'LangId',
              ( ['retval', 'out'], POINTER(c_int), 'LangId' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(SpeechWordType), 'WordType' )),
    COMMETHOD([dispid(3), 'propget'], HRESULT, 'Word',
              ( ['retval', 'out'], POINTER(BSTR), 'Word' )),
    COMMETHOD([dispid(4), 'propget'], HRESULT, 'Pronunciations',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechLexiconPronunciations)), 'Pronunciations' )),
]
class SpWaveFormatEx(CoClass):
    u'SpWaveFormatEx Class'
    _reg_clsid_ = GUID('{C79A574C-63BE-44B9-801F-283F87F898BE}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpWaveFormatEx._com_interfaces_ = [ISpeechWaveFormatEx]

tagSTATSTG._fields_ = [
    ('pwcsName', WSTRING),
    ('Type', c_ulong),
    ('cbSize', _ULARGE_INTEGER),
    ('mtime', _FILETIME),
    ('ctime', _FILETIME),
    ('atime', _FILETIME),
    ('grfMode', c_ulong),
    ('grfLocksSupported', c_ulong),
    ('clsid', comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID),
    ('grfStateBits', c_ulong),
    ('reserved', c_ulong),
]
assert sizeof(tagSTATSTG) == 72, sizeof(tagSTATSTG)
assert alignment(tagSTATSTG) == 8, alignment(tagSTATSTG)
ISpAudio._methods_ = [
    COMMETHOD([], HRESULT, 'SetState',
              ( ['in'], SPAUDIOSTATE, 'NewState' ),
              ( ['in'], c_ulonglong, 'ullReserved' )),
    COMMETHOD([], HRESULT, 'SetFormat',
              ( ['in'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'rguidFmtId' ),
              ( ['in'], POINTER(WaveFormatEx), 'pWaveFormatEx' )),
    COMMETHOD([], HRESULT, 'GetStatus',
              ( ['out'], POINTER(SPAUDIOSTATUS), 'pStatus' )),
    COMMETHOD([], HRESULT, 'SetBufferInfo',
              ( ['in'], POINTER(SPAUDIOBUFFERINFO), 'pBuffInfo' )),
    COMMETHOD([], HRESULT, 'GetBufferInfo',
              ( ['out'], POINTER(SPAUDIOBUFFERINFO), 'pBuffInfo' )),
    COMMETHOD([], HRESULT, 'GetDefaultFormat',
              ( ['out'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pFormatId' ),
              ( ['out'], POINTER(POINTER(WaveFormatEx)), 'ppCoMemWaveFormatEx' )),
    COMMETHOD([], c_void_p, 'EventHandle'),
    COMMETHOD([], HRESULT, 'GetVolumeLevel',
              ( ['out'], POINTER(c_ulong), 'pLevel' )),
    COMMETHOD([], HRESULT, 'SetVolumeLevel',
              ( ['in'], c_ulong, 'Level' )),
    COMMETHOD([], HRESULT, 'GetBufferNotifySize',
              ( ['out'], POINTER(c_ulong), 'pcbSize' )),
    COMMETHOD([], HRESULT, 'SetBufferNotifySize',
              ( ['in'], c_ulong, 'cbSize' )),
]
ISpMMSysAudio._methods_ = [
    COMMETHOD([], HRESULT, 'GetDeviceId',
              ( ['out'], POINTER(c_uint), 'puDeviceId' )),
    COMMETHOD([], HRESULT, 'SetDeviceId',
              ( ['in'], c_uint, 'uDeviceId' )),
    COMMETHOD([], HRESULT, 'GetMMHandle',
              ( [], POINTER(c_void_p), 'pHandle' )),
    COMMETHOD([], HRESULT, 'GetLineId',
              ( ['out'], POINTER(c_uint), 'puLineId' )),
    COMMETHOD([], HRESULT, 'SetLineId',
              ( ['in'], c_uint, 'uLineId' )),
]
ISpEventSink._methods_ = [
    COMMETHOD([], HRESULT, 'AddEvents',
              ( ['in'], POINTER(SPEVENT), 'pEventArray' ),
              ( ['in'], c_ulong, 'ulCount' )),
    COMMETHOD([], HRESULT, 'GetEventInterest',
              ( ['out'], POINTER(c_ulonglong), 'pullEventInterest' )),
]
SpeechAudioVolume = u'AudioVolume' # Constant BSTR
ISpeechWaveFormatEx._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'FormatTag'), 'propget'], HRESULT, 'FormatTag',
              ( ['retval', 'out'], POINTER(c_short), 'FormatTag' )),
    COMMETHOD([dispid(1), helpstring(u'FormatTag'), 'propput'], HRESULT, 'FormatTag',
              ( ['in'], c_short, 'FormatTag' )),
    COMMETHOD([dispid(2), helpstring(u'Channels'), 'propget'], HRESULT, 'Channels',
              ( ['retval', 'out'], POINTER(c_short), 'Channels' )),
    COMMETHOD([dispid(2), helpstring(u'Channels'), 'propput'], HRESULT, 'Channels',
              ( ['in'], c_short, 'Channels' )),
    COMMETHOD([dispid(3), helpstring(u'SamplesPerSec'), 'propget'], HRESULT, 'SamplesPerSec',
              ( ['retval', 'out'], POINTER(c_int), 'SamplesPerSec' )),
    COMMETHOD([dispid(3), helpstring(u'SamplesPerSec'), 'propput'], HRESULT, 'SamplesPerSec',
              ( ['in'], c_int, 'SamplesPerSec' )),
    COMMETHOD([dispid(4), helpstring(u'AvgBytesPerSec'), 'propget'], HRESULT, 'AvgBytesPerSec',
              ( ['retval', 'out'], POINTER(c_int), 'AvgBytesPerSec' )),
    COMMETHOD([dispid(4), helpstring(u'AvgBytesPerSec'), 'propput'], HRESULT, 'AvgBytesPerSec',
              ( ['in'], c_int, 'AvgBytesPerSec' )),
    COMMETHOD([dispid(5), helpstring(u'BlockAlign'), 'propget'], HRESULT, 'BlockAlign',
              ( ['retval', 'out'], POINTER(c_short), 'BlockAlign' )),
    COMMETHOD([dispid(5), helpstring(u'BlockAlign'), 'propput'], HRESULT, 'BlockAlign',
              ( ['in'], c_short, 'BlockAlign' )),
    COMMETHOD([dispid(6), helpstring(u'BitsPerSample'), 'propget'], HRESULT, 'BitsPerSample',
              ( ['retval', 'out'], POINTER(c_short), 'BitsPerSample' )),
    COMMETHOD([dispid(6), helpstring(u'BitsPerSample'), 'propput'], HRESULT, 'BitsPerSample',
              ( ['in'], c_short, 'BitsPerSample' )),
    COMMETHOD([dispid(7), helpstring(u'ExtraData'), 'propget'], HRESULT, 'ExtraData',
              ( ['retval', 'out'], POINTER(VARIANT), 'ExtraData' )),
    COMMETHOD([dispid(7), helpstring(u'ExtraData'), 'propput'], HRESULT, 'ExtraData',
              ( ['in'], VARIANT, 'ExtraData' )),
]
SpeechRegistryUserRoot = u'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Speech' # Constant BSTR
SPVOICESTATUS._fields_ = [
    ('ulCurrentStream', c_ulong),
    ('ulLastStreamQueued', c_ulong),
    ('hrLastResult', HRESULT),
    ('dwRunningState', c_ulong),
    ('ulInputWordPos', c_ulong),
    ('ulInputWordLen', c_ulong),
    ('ulInputSentPos', c_ulong),
    ('ulInputSentLen', c_ulong),
    ('lBookmarkId', c_int),
    ('PhonemeId', c_ushort),
    ('VisemeId', SPVISEMES),
    ('dwReserved1', c_ulong),
    ('dwReserved2', c_ulong),
]
assert sizeof(SPVOICESTATUS) == 52, sizeof(SPVOICESTATUS)
assert alignment(SPVOICESTATUS) == 4, alignment(SPVOICESTATUS)
ISpeechRecognizerStatus._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'AudioStatus'), 'propget'], HRESULT, 'AudioStatus',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechAudioStatus)), 'AudioStatus' )),
    COMMETHOD([dispid(2), helpstring(u'CurrentStreamPosition'), 'propget'], HRESULT, 'CurrentStreamPosition',
              ( ['retval', 'out'], POINTER(VARIANT), 'pCurrentStreamPos' )),
    COMMETHOD([dispid(3), helpstring(u'CurrentStreamNumber'), 'propget'], HRESULT, 'CurrentStreamNumber',
              ( ['retval', 'out'], POINTER(c_int), 'StreamNumber' )),
    COMMETHOD([dispid(4), helpstring(u'NumberOfActiveRules'), 'propget'], HRESULT, 'NumberOfActiveRules',
              ( ['retval', 'out'], POINTER(c_int), 'NumberOfActiveRules' )),
    COMMETHOD([dispid(5), helpstring(u'ClsidEngine'), 'propget'], HRESULT, 'ClsidEngine',
              ( ['retval', 'out'], POINTER(BSTR), 'ClsidEngine' )),
    COMMETHOD([dispid(6), helpstring(u'SupportedLanguages'), 'propget'], HRESULT, 'SupportedLanguages',
              ( ['retval', 'out'], POINTER(VARIANT), 'SupportedLanguages' )),
]

# values for enumeration 'DISPID_SpeechPhraseProperty'
DISPID_SPPName = 1
DISPID_SPPId = 2
DISPID_SPPValue = 3
DISPID_SPPFirstElement = 4
DISPID_SPPNumberOfElements = 5
DISPID_SPPEngineConfidence = 6
DISPID_SPPConfidence = 7
DISPID_SPPParent = 8
DISPID_SPPChildren = 9
DISPID_SpeechPhraseProperty = c_int # enum

# values for enumeration 'DISPID_SpeechAudioFormat'
DISPID_SAFType = 1
DISPID_SAFGuid = 2
DISPID_SAFGetWaveFormatEx = 3
DISPID_SAFSetWaveFormatEx = 4
DISPID_SpeechAudioFormat = c_int # enum
ISpRecognizer._methods_ = [
    COMMETHOD([], HRESULT, 'SetRecognizer',
              ( ['in'], POINTER(ISpObjectToken), 'pRecognizer' )),
    COMMETHOD([], HRESULT, 'GetRecognizer',
              ( ['out'], POINTER(POINTER(ISpObjectToken)), 'ppRecognizer' )),
    COMMETHOD([], HRESULT, 'SetInput',
              ( ['in'], POINTER(IUnknown), 'pUnkInput' ),
              ( ['in'], c_int, 'fAllowFormatChanges' )),
    COMMETHOD([], HRESULT, 'GetInputObjectToken',
              ( ['out'], POINTER(POINTER(ISpObjectToken)), 'ppToken' )),
    COMMETHOD([], HRESULT, 'GetInputStream',
              ( ['out'], POINTER(POINTER(ISpStreamFormat)), 'ppStream' )),
    COMMETHOD([], HRESULT, 'CreateRecoContext',
              ( ['out'], POINTER(POINTER(ISpRecoContext)), 'ppNewCtxt' )),
    COMMETHOD([], HRESULT, 'GetRecoProfile',
              ( ['out'], POINTER(POINTER(ISpObjectToken)), 'ppToken' )),
    COMMETHOD([], HRESULT, 'SetRecoProfile',
              ( ['in'], POINTER(ISpObjectToken), 'pToken' )),
    COMMETHOD([], HRESULT, 'IsSharedInstance'),
    COMMETHOD([], HRESULT, 'GetRecoState',
              ( ['out'], POINTER(SPRECOSTATE), 'pState' )),
    COMMETHOD([], HRESULT, 'SetRecoState',
              ( ['in'], SPRECOSTATE, 'NewState' )),
    COMMETHOD([], HRESULT, 'GetStatus',
              ( ['out'], POINTER(SPRECOGNIZERSTATUS), 'pStatus' )),
    COMMETHOD([], HRESULT, 'GetFormat',
              ( ['in'], SPSTREAMFORMATTYPE, 'WaveFormatType' ),
              ( ['out'], POINTER(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'pFormatId' ),
              ( ['out'], POINTER(POINTER(WaveFormatEx)), 'ppCoMemWFEX' )),
    COMMETHOD([], HRESULT, 'IsUISupported',
              ( ['in'], POINTER(c_ushort), 'pszTypeOfUI' ),
              ( ['in'], c_void_p, 'pvExtraData' ),
              ( ['in'], c_ulong, 'cbExtraData' ),
              ( ['out'], POINTER(c_int), 'pfSupported' )),
    COMMETHOD([], HRESULT, 'DisplayUI',
              ( ['in'], wireHWND, 'hWndParent' ),
              ( ['in'], POINTER(c_ushort), 'pszTitle' ),
              ( ['in'], POINTER(c_ushort), 'pszTypeOfUI' ),
              ( ['in'], c_void_p, 'pvExtraData' ),
              ( ['in'], c_ulong, 'cbExtraData' )),
    COMMETHOD([], HRESULT, 'EmulateRecognition',
              ( ['in'], POINTER(ISpPhrase), 'pPhrase' )),
]
SpeechRecoProfileProperties = u'RecoProfileProperties' # Constant BSTR
SpeechPropertyNormalConfidenceThreshold = u'NormalConfidenceThreshold' # Constant BSTR

# values for enumeration 'DISPID_SpeechPhraseAlternate'
DISPID_SPARecoResult = 1
DISPID_SPAStartElementInResult = 2
DISPID_SPANumberOfElementsInResult = 3
DISPID_SPAPhraseInfo = 4
DISPID_SPACommit = 5
DISPID_SpeechPhraseAlternate = c_int # enum
ISpeechTextSelectionInformation._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'ActiveOffset'), 'propput'], HRESULT, 'ActiveOffset',
              ( ['in'], c_int, 'ActiveOffset' )),
    COMMETHOD([dispid(1), helpstring(u'ActiveOffset'), 'propget'], HRESULT, 'ActiveOffset',
              ( ['retval', 'out'], POINTER(c_int), 'ActiveOffset' )),
    COMMETHOD([dispid(2), helpstring(u'ActiveLength'), 'propput'], HRESULT, 'ActiveLength',
              ( ['in'], c_int, 'ActiveLength' )),
    COMMETHOD([dispid(2), helpstring(u'ActiveLength'), 'propget'], HRESULT, 'ActiveLength',
              ( ['retval', 'out'], POINTER(c_int), 'ActiveLength' )),
    COMMETHOD([dispid(3), helpstring(u'SelectionOffset'), 'propput'], HRESULT, 'SelectionOffset',
              ( ['in'], c_int, 'SelectionOffset' )),
    COMMETHOD([dispid(3), helpstring(u'SelectionOffset'), 'propget'], HRESULT, 'SelectionOffset',
              ( ['retval', 'out'], POINTER(c_int), 'SelectionOffset' )),
    COMMETHOD([dispid(4), helpstring(u'SelectionLength'), 'propput'], HRESULT, 'SelectionLength',
              ( ['in'], c_int, 'SelectionLength' )),
    COMMETHOD([dispid(4), helpstring(u'SelectionLength'), 'propget'], HRESULT, 'SelectionLength',
              ( ['retval', 'out'], POINTER(c_int), 'SelectionLength' )),
]
class SpInprocRecognizer(CoClass):
    u'SpInprocRecognizer Class'
    _reg_clsid_ = GUID('{41B89B6B-9399-11D2-9623-00C04F8EE628}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpInprocRecognizer._com_interfaces_ = [ISpeechRecognizer, ISpRecognizer]

class SpStream(CoClass):
    u'SpStream Class'
    _reg_clsid_ = GUID('{715D9C59-4442-11D2-9605-00C04F8EE628}')
    _idlflags_ = ['hidden', 'restricted']
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpStream._com_interfaces_ = [ISpStream]


# values for enumeration 'DISPID_SpeechFileStream'
DISPID_SFSOpen = 100
DISPID_SFSClose = 101
DISPID_SpeechFileStream = c_int # enum
ISpeechPhraseInfo._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'LanguageId'), 'propget'], HRESULT, 'LanguageId',
              ( ['retval', 'out'], POINTER(c_int), 'LanguageId' )),
    COMMETHOD([dispid(2), helpstring(u'GrammarId'), 'propget'], HRESULT, 'GrammarId',
              ( ['retval', 'out'], POINTER(VARIANT), 'GrammarId' )),
    COMMETHOD([dispid(3), helpstring(u'StartTime'), 'propget'], HRESULT, 'StartTime',
              ( ['retval', 'out'], POINTER(VARIANT), 'StartTime' )),
    COMMETHOD([dispid(4), helpstring(u'AudioStreamPosition'), 'propget'], HRESULT, 'AudioStreamPosition',
              ( ['retval', 'out'], POINTER(VARIANT), 'AudioStreamPosition' )),
    COMMETHOD([dispid(5), helpstring(u'AudioSizeBytes'), 'propget'], HRESULT, 'AudioSizeBytes',
              ( ['retval', 'out'], POINTER(c_int), 'pAudioSizeBytes' )),
    COMMETHOD([dispid(6), helpstring(u'RetainedSizeBytes'), 'propget'], HRESULT, 'RetainedSizeBytes',
              ( ['retval', 'out'], POINTER(c_int), 'RetainedSizeBytes' )),
    COMMETHOD([dispid(7), helpstring(u'AudioSizeTime'), 'propget'], HRESULT, 'AudioSizeTime',
              ( ['retval', 'out'], POINTER(c_int), 'AudioSizeTime' )),
    COMMETHOD([dispid(8), helpstring(u'Rule'), 'propget'], HRESULT, 'Rule',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseRule)), 'Rule' )),
    COMMETHOD([dispid(9), helpstring(u'Properties'), 'propget'], HRESULT, 'Properties',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseProperties)), 'Properties' )),
    COMMETHOD([dispid(10), helpstring(u'Elements'), 'propget'], HRESULT, 'Elements',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseElements)), 'Elements' )),
    COMMETHOD([dispid(11), helpstring(u'Replacements'), 'propget'], HRESULT, 'Replacements',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseReplacements)), 'Replacements' )),
    COMMETHOD([dispid(12), helpstring(u'EngineId'), 'propget'], HRESULT, 'EngineId',
              ( ['retval', 'out'], POINTER(BSTR), 'EngineIdGuid' )),
    COMMETHOD([dispid(13), helpstring(u'EnginePrivateData'), 'propget'], HRESULT, 'EnginePrivateData',
              ( ['retval', 'out'], POINTER(VARIANT), 'PrivateData' )),
    COMMETHOD([dispid(14), helpstring(u'SaveToMemory')], HRESULT, 'SaveToMemory',
              ( ['retval', 'out'], POINTER(VARIANT), 'PhraseBlock' )),
    COMMETHOD([dispid(15), helpstring(u'GetText')], HRESULT, 'GetText',
              ( ['in', 'optional'], c_int, 'StartElement', 0 ),
              ( ['in', 'optional'], c_int, 'Elements', -1 ),
              ( ['in', 'optional'], VARIANT_BOOL, 'UseReplacements', True ),
              ( ['retval', 'out'], POINTER(BSTR), 'Text' )),
    COMMETHOD([dispid(16), helpstring(u'DisplayAttributes')], HRESULT, 'GetDisplayAttributes',
              ( ['in', 'optional'], c_int, 'StartElement', 0 ),
              ( ['in', 'optional'], c_int, 'Elements', -1 ),
              ( ['in', 'optional'], VARIANT_BOOL, 'UseReplacements', True ),
              ( ['retval', 'out'], POINTER(SpeechDisplayAttributes), 'DisplayAttributes' )),
]
ISpeechPhoneConverter._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'LanguageId'), 'propget'], HRESULT, 'LanguageId',
              ( ['retval', 'out'], POINTER(c_int), 'LanguageId' )),
    COMMETHOD([dispid(1), helpstring(u'LanguageId'), 'propput'], HRESULT, 'LanguageId',
              ( ['in'], c_int, 'LanguageId' )),
    COMMETHOD([dispid(2), helpstring(u'PhoneToId')], HRESULT, 'PhoneToId',
              ( ['in'], BSTR, 'Phonemes' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'IdArray' )),
    COMMETHOD([dispid(3), helpstring(u'IdToPhone')], HRESULT, 'IdToPhone',
              ( ['in'], VARIANT, 'IdArray' ),
              ( ['retval', 'out'], POINTER(BSTR), 'Phonemes' )),
]

# values for enumeration 'DISPID_SpeechLexicon'
DISPID_SLGenerationId = 1
DISPID_SLGetWords = 2
DISPID_SLAddPronunciation = 3
DISPID_SLAddPronunciationByPhoneIds = 4
DISPID_SLRemovePronunciation = 5
DISPID_SLRemovePronunciationByPhoneIds = 6
DISPID_SLGetPronunciations = 7
DISPID_SLGetGenerationChange = 8
DISPID_SpeechLexicon = c_int # enum
ISpeechMMSysAudio._methods_ = [
    COMMETHOD([dispid(300), helpstring(u'DeviceId'), 'propget'], HRESULT, 'DeviceId',
              ( ['retval', 'out'], POINTER(c_int), 'DeviceId' )),
    COMMETHOD([dispid(300), helpstring(u'DeviceId'), 'propput'], HRESULT, 'DeviceId',
              ( ['in'], c_int, 'DeviceId' )),
    COMMETHOD([dispid(301), helpstring(u'LineId'), 'propget'], HRESULT, 'LineId',
              ( ['retval', 'out'], POINTER(c_int), 'LineId' )),
    COMMETHOD([dispid(301), helpstring(u'LineId'), 'propput'], HRESULT, 'LineId',
              ( ['in'], c_int, 'LineId' )),
    COMMETHOD([dispid(302), helpstring(u'MMHandle'), 'hidden', 'propget'], HRESULT, 'MMHandle',
              ( ['retval', 'out'], POINTER(c_int), 'Handle' )),
]
SpeechCategoryRecoProfiles = u'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Speech\\RecoProfiles' # Constant BSTR

# values for enumeration 'DISPID_SpeechRecoResult'
DISPID_SRRRecoContext = 1
DISPID_SRRTimes = 2
DISPID_SRRAudioFormat = 3
DISPID_SRRPhraseInfo = 4
DISPID_SRRAlternates = 5
DISPID_SRRAudio = 6
DISPID_SRRSpeakAudio = 7
DISPID_SRRSaveToMemory = 8
DISPID_SRRDiscardResultInfo = 9
DISPID_SpeechRecoResult = c_int # enum
ISpeechDataKey._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'SetBinaryValue')], HRESULT, 'SetBinaryValue',
              ( ['in'], BSTR, 'ValueName' ),
              ( ['in'], VARIANT, 'Value' )),
    COMMETHOD([dispid(2), helpstring(u'GetBinaryValue')], HRESULT, 'GetBinaryValue',
              ( ['in'], BSTR, 'ValueName' ),
              ( ['retval', 'out'], POINTER(VARIANT), 'Value' )),
    COMMETHOD([dispid(3), helpstring(u'SetStringValue')], HRESULT, 'SetStringValue',
              ( ['in'], BSTR, 'ValueName' ),
              ( ['in'], BSTR, 'Value' )),
    COMMETHOD([dispid(4), helpstring(u'GetStringValue')], HRESULT, 'GetStringValue',
              ( ['in'], BSTR, 'ValueName' ),
              ( ['retval', 'out'], POINTER(BSTR), 'Value' )),
    COMMETHOD([dispid(5), helpstring(u'SetLongValue')], HRESULT, 'SetLongValue',
              ( ['in'], BSTR, 'ValueName' ),
              ( ['in'], c_int, 'Value' )),
    COMMETHOD([dispid(6), helpstring(u'GetlongValue')], HRESULT, 'GetLongValue',
              ( ['in'], BSTR, 'ValueName' ),
              ( ['retval', 'out'], POINTER(c_int), 'Value' )),
    COMMETHOD([dispid(7), helpstring(u'OpenKey')], HRESULT, 'OpenKey',
              ( ['in'], BSTR, 'SubKeyName' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechDataKey)), 'SubKey' )),
    COMMETHOD([dispid(8), helpstring(u'CreateKey')], HRESULT, 'CreateKey',
              ( ['in'], BSTR, 'SubKeyName' ),
              ( ['retval', 'out'], POINTER(POINTER(ISpeechDataKey)), 'SubKey' )),
    COMMETHOD([dispid(9), helpstring(u'DeleteKey')], HRESULT, 'DeleteKey',
              ( ['in'], BSTR, 'SubKeyName' )),
    COMMETHOD([dispid(10), helpstring(u'DeleteValue')], HRESULT, 'DeleteValue',
              ( ['in'], BSTR, 'ValueName' )),
    COMMETHOD([dispid(11), helpstring(u'EnumKeys')], HRESULT, 'EnumKeys',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(BSTR), 'SubKeyName' )),
    COMMETHOD([dispid(12), helpstring(u'EnumValues')], HRESULT, 'EnumValues',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(BSTR), 'ValueName' )),
]
class SpPhraseInfoBuilder(CoClass):
    u'SpPhraseInfoBuilder Class'
    _reg_clsid_ = GUID('{C23FC28D-C55F-4720-8B32-91F73C2BD5D1}')
    _idlflags_ = []
    _reg_typelib_ = ('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 5, 0)
SpPhraseInfoBuilder._com_interfaces_ = [ISpeechPhraseInfoBuilder]

tagSPTEXTSELECTIONINFO._fields_ = [
    ('ulStartActiveOffset', c_ulong),
    ('cchActiveChars', c_ulong),
    ('ulStartSelection', c_ulong),
    ('cchSelection', c_ulong),
]
assert sizeof(tagSPTEXTSELECTIONINFO) == 16, sizeof(tagSPTEXTSELECTIONINFO)
assert alignment(tagSPTEXTSELECTIONINFO) == 4, alignment(tagSPTEXTSELECTIONINFO)

# values for enumeration 'SpeechVisemeType'
SVP_0 = 0
SVP_1 = 1
SVP_2 = 2
SVP_3 = 3
SVP_4 = 4
SVP_5 = 5
SVP_6 = 6
SVP_7 = 7
SVP_8 = 8
SVP_9 = 9
SVP_10 = 10
SVP_11 = 11
SVP_12 = 12
SVP_13 = 13
SVP_14 = 14
SVP_15 = 15
SVP_16 = 16
SVP_17 = 17
SVP_18 = 18
SVP_19 = 19
SVP_20 = 20
SVP_21 = 21
SpeechVisemeType = c_int # enum
_ISpeechVoiceEvents._disp_methods_ = [
    DISPMETHOD([dispid(1), helpstring(u'StartStream')], None, 'StartStream',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(2), helpstring(u'EndStream')], None, 'EndStream',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' )),
    DISPMETHOD([dispid(3), helpstring(u'VoiceChange')], None, 'VoiceChange',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], POINTER(ISpeechObjectToken), 'VoiceObjectToken' )),
    DISPMETHOD([dispid(4), helpstring(u'Bookmark')], None, 'Bookmark',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], BSTR, 'Bookmark' ),
               ( ['in'], c_int, 'BookmarkId' )),
    DISPMETHOD([dispid(5), helpstring(u'Word')], None, 'Word',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], c_int, 'CharacterPosition' ),
               ( ['in'], c_int, 'Length' )),
    DISPMETHOD([dispid(7), helpstring(u'Sentence')], None, 'Sentence',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], c_int, 'CharacterPosition' ),
               ( ['in'], c_int, 'Length' )),
    DISPMETHOD([dispid(6), helpstring(u'Phoneme')], None, 'Phoneme',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], c_int, 'Duration' ),
               ( ['in'], c_short, 'NextPhoneId' ),
               ( ['in'], SpeechVisemeFeature, 'Feature' ),
               ( ['in'], c_short, 'CurrentPhoneId' )),
    DISPMETHOD([dispid(8), helpstring(u'Viseme')], None, 'Viseme',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], c_int, 'Duration' ),
               ( ['in'], SpeechVisemeType, 'NextVisemeId' ),
               ( ['in'], SpeechVisemeFeature, 'Feature' ),
               ( ['in'], SpeechVisemeType, 'CurrentVisemeId' )),
    DISPMETHOD([dispid(9), helpstring(u'AudioLevel')], None, 'AudioLevel',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], VARIANT, 'StreamPosition' ),
               ( ['in'], c_int, 'AudioLevel' )),
    DISPMETHOD([dispid(10), helpstring(u'EnginePrivate')], None, 'EnginePrivate',
               ( ['in'], c_int, 'StreamNumber' ),
               ( ['in'], c_int, 'StreamPosition' ),
               ( ['in'], VARIANT, 'EngineData' )),
]
SpeechAudioFormatGUIDText = u'{7CEEF9F9-3D13-11d2-9EE7-00C04F797396}' # Constant BSTR

# values for enumeration 'DISPID_SpeechMemoryStream'
DISPID_SMSSetData = 100
DISPID_SMSGetData = 101
DISPID_SpeechMemoryStream = c_int # enum
SpeechTokenIdUserLexicon = u'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Speech\\CurrentUserLexicon' # Constant BSTR
ISpPhoneConverter._methods_ = [
    COMMETHOD([], HRESULT, 'PhoneToId',
              ( ['in'], POINTER(c_ushort), 'pszPhone' ),
              ( ['out'], POINTER(c_ushort), 'pId' )),
    COMMETHOD([], HRESULT, 'IdToPhone',
              ( ['in'], POINTER(c_ushort), 'pId' ),
              ( ['out'], POINTER(c_ushort), 'pszPhone' )),
]
ISpeechPhraseRule._methods_ = [
    COMMETHOD([dispid(1), helpstring(u'Name'), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'Name' )),
    COMMETHOD([dispid(2), helpstring(u'Id'), 'propget'], HRESULT, 'Id',
              ( ['retval', 'out'], POINTER(c_int), 'Id' )),
    COMMETHOD([dispid(3), helpstring(u'FirstElement'), 'propget'], HRESULT, 'FirstElement',
              ( ['retval', 'out'], POINTER(c_int), 'FirstElement' )),
    COMMETHOD([dispid(4), helpstring(u'NumElements'), 'propget'], HRESULT, 'NumberOfElements',
              ( ['retval', 'out'], POINTER(c_int), 'NumberOfElements' )),
    COMMETHOD([dispid(5), helpstring(u'Parent'), 'propget'], HRESULT, 'Parent',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseRule)), 'Parent' )),
    COMMETHOD([dispid(6), helpstring(u'Children'), 'propget'], HRESULT, 'Children',
              ( ['retval', 'out'], POINTER(POINTER(ISpeechPhraseRules)), 'Children' )),
    COMMETHOD([dispid(7), helpstring(u'Confidence'), 'propget'], HRESULT, 'Confidence',
              ( ['retval', 'out'], POINTER(SpeechEngineConfidence), 'ActualConfidence' )),
    COMMETHOD([dispid(8), helpstring(u'EngineConfidence'), 'propget'], HRESULT, 'EngineConfidence',
              ( ['retval', 'out'], POINTER(c_float), 'EngineConfidence' )),
]
