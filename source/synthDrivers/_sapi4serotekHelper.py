#sapi4helper.py
# Contributed by Serotek Corporation under the GPL
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.


from ctypes import *
from ctypes.wintypes import *
from comtypes import *
import traceback
import config

###comtypes class definitions

SVFN_LEN = 262
LANG_LEN = 64
TTSDATAFLAG_TAGGED = 1
TTSI_NAMELEN = SVFN_LEN
TTSI_STYLELEN = SVFN_LEN
TTSATTR_MINPITCH = 0
TTSATTR_MAXPITCH = 0xffff
TTSATTR_MINSPEED = 0
TTSATTR_MAXSPEED = 0xffffffff

LANGID = WORD
QWORD = c_ulonglong

class VOICECHARSET(c_int):
    CHARSET_TEXT = 0
    CHARSET_IPAPHONETIC = 1
    CHARSET_ENGINEPHONETIC = 2

class FILETIME(Structure):
    _fields_ = [("dwLowDateTime", DWORD), ("dwHighDateTime", DWORD)]

class LANGUAGEW(Structure):
    _fields_ = [("LanguageID", LANGID),
                ("szDialect", c_wchar * LANG_LEN)]
LANGUAGE = LANGUAGEW

class TTSMODEINFOW(Structure):
    _fields_ = [("gEngine", GUID),
                ("szMfgName", c_wchar * TTSI_NAMELEN),
                ("szProductName", c_wchar * TTSI_NAMELEN),
                ("gModeID", GUID),
                ("szModeName", c_wchar * TTSI_NAMELEN),
                ("language", LANGUAGEW),
                ("szSpeaker", c_wchar * TTSI_NAMELEN),
                ("szStyle", c_wchar * TTSI_STYLELEN),
                ("wGender", WORD),
                ("wAge", WORD),
                ("dwFeatures", DWORD),
                ("dwInterfaces", DWORD),
                ("dwEngineFeatures", DWORD)]
TTSMODEINFO = TTSMODEINFOW

class SDATA(Structure):
    _fields_ = [("pData", c_void_p), ("dwSize", DWORD)]

class TTSMOUTH(Structure):
    _fields_ = [("bMouthHeight", BYTE), ("bMouthWidth", BYTE),
                ("bMouthUpturn", BYTE), ("bJawOpen", BYTE),
                ("bTeethUpperVisible", BYTE), ("bTeethLowerVisible", BYTE),
                ("bTonguePosn", BYTE), ("bLipTension", BYTE)]

def TextSDATA(text):
    d = SDATA()
    d.pData = cast(c_wchar_p(text), c_void_p)
    d.dwSize = (len(text) * sizeof(c_wchar)) + 1
    return d

class ITTSAttributesW(IUnknown):
    _iid_ = GUID("{1287A280-4A47-101B-931A-00AA0047BA4F}")

ITTSAttributesW._methods_ = [
    STDMETHOD(HRESULT, "PitchGet", [POINTER(WORD)]),
    STDMETHOD(HRESULT, "PitchSet", [WORD]),
    STDMETHOD(HRESULT, "RealTimeGet", [POINTER(DWORD)]),
    STDMETHOD(HRESULT, "RealTimeSet", [DWORD]),
    STDMETHOD(HRESULT, "SpeedGet", [POINTER(DWORD)]),
    STDMETHOD(HRESULT, "SpeedSet", [DWORD]),
    STDMETHOD(HRESULT, "VolumeGet", [POINTER(DWORD)]),
    STDMETHOD(HRESULT, "VolumeSet", [DWORD])
]

ITTSAttributes = ITTSAttributesW

class ITTSBufNotifySink(IUnknown):
    _iid_ = GUID("{E4963D40-C743-11cd-80E5-00AA003E4B50}")

ITTSBufNotifySink._methods_ = [
    STDMETHOD(HRESULT, "TextDataDone", [QWORD, DWORD]),
    STDMETHOD(HRESULT, "TextDataStarted", [QWORD]),
    STDMETHOD(HRESULT, "BookMark", [QWORD, DWORD]),
    STDMETHOD(HRESULT, "WordPosition", [QWORD, DWORD])
]

class ITTSCentralW(IUnknown):
    _iid_ = GUID("{28016060-4A47-101B-931A-00AA0047BA4F}")

ITTSCentralW._methods_ = [
    STDMETHOD(HRESULT, "Inject", [LPCWSTR]),
    STDMETHOD(HRESULT, "ModeGet", [POINTER(TTSMODEINFOW)]),
    STDMETHOD(HRESULT, "Phoneme", [VOICECHARSET, DWORD, SDATA, POINTER(SDATA)]),
    STDMETHOD(HRESULT, "PosnGet", [POINTER(QWORD)]),
    STDMETHOD(HRESULT, "TextData", [VOICECHARSET, DWORD, SDATA, c_void_p, GUID]),
    STDMETHOD(HRESULT, "ToFileTime", [POINTER(QWORD), POINTER(FILETIME)]),
    STDMETHOD(HRESULT, "AudioPause"),
    STDMETHOD(HRESULT, "AudioResume"),
    STDMETHOD(HRESULT, "AudioReset"),
    STDMETHOD(HRESULT, "Register", [c_void_p, GUID, POINTER(DWORD)]),
    STDMETHOD(HRESULT, "UnRegister", [DWORD])
]

ITTSCentral = ITTSCentralW

class IAudioMultiMediaDevice(IUnknown):
    _iid_ = GUID("{B68AD320-C743-11cd-80E5-00AA003E4B50}")

IAudioMultiMediaDevice._methods_ = [
    STDMETHOD(HRESULT, "CustomMessage", [c_uint, SDATA]),
    STDMETHOD(HRESULT, "DeviceNumGet", [POINTER(DWORD)]),
    STDMETHOD(HRESULT, "DeviceNumSet", [DWORD])
]

class ITTSEnumW(IUnknown):
    _iid_ = GUID("{6B837B20-4A47-101B-931A-00AA0047BA4F}")

ITTSEnumW._methods_ = [
    STDMETHOD(HRESULT, "Next", [c_ulong, POINTER(TTSMODEINFOW),
                                POINTER(c_ulong)]),
    STDMETHOD(HRESULT, "Skip", [c_ulong]),
    STDMETHOD(HRESULT, "Reset"),
    STDMETHOD(HRESULT, "Clone", [POINTER(POINTER(ITTSEnumW))]),
    STDMETHOD(HRESULT, "Select", [GUID, POINTER(POINTER(ITTSCentralW)),
                                  POINTER(IUnknown)])
]

ITTSEnum = ITTSEnumW

class ITTSNotifySinkW(IUnknown):
    _iid_ = GUID("{C0FA8F40-4A46-101B-931A-00AA0047BA4F}")

ITTSNotifySinkW._methods_ = [
  STDMETHOD(HRESULT, "AttribChanged", [DWORD]),
  STDMETHOD(HRESULT, "AudioStart", [QWORD]),
  STDMETHOD(HRESULT, "AudioStop", [QWORD]),
  STDMETHOD(HRESULT, "Visual", [QWORD, c_wchar, c_wchar, DWORD,
                                POINTER(TTSMOUTH)])
]

ITTSNotifySink = ITTSNotifySinkW

CLSID_MMAudioDest = GUID("{CB96B400-C743-11cd-80E5-00AA003E4B50}")
CLSID_TTSEnumerator = GUID("{D67C0280-C743-11cd-80E5-00AA003E4B50}")

###Sapi4 wrapper class

_voiceDefault = None

class Sink(COMObject):
    _com_interfaces_ = [ITTSNotifySinkW]

    def __init__(self, wrapper):
        self._wrapper = wrapper
        super(Sink, self).__init__()

    def ITTSNotifySinkW_AttribChanged(self, *args):
        return S_OK

    def ITTSNotifySinkW_AudioStart(self, *args):
        self._wrapper.onAudioStart()
        return S_OK

    def ITTSNotifySinkW_AudioStop(self, *args):
        self._wrapper.onAudioStop()
        return S_OK

    def ITTSNotifySinkW_Visual(self, *args):
        return S_OK

class BufSink(COMObject):
    _com_interfaces_ = [ITTSBufNotifySink]

    def __init__(self, wrapper):
        self._wrapper = wrapper
        super(BufSink, self).__init__()

    def ITTSBufNotifySink_BookMark(self, this, qTimeStamp, dwMarkNum):
        self._wrapper.onIndexMark(dwMarkNum)
        return S_OK

    def ITTSBufNotifySink_TextDataDone(self, this, qTimeStamp, dwFlags):
        return S_OK

    def ITTSBufNotifySink_TextDataStarted(self, this, qTimeStamp):
        return S_OK

    def ITTSBufNotifySink_WordPosition(self, this, qTimeStamp, dwByteOffset):
        return S_OK

class SAPI4(object):
    rateStep = 20
    averagePitchStep = 10
    _noticeAudioStop = False
    newEngineOnVoiceChange = True

    def __init__(self, voice=None):
        global _voiceDefault
        self._doneCallbacks = []
        self._enum = CoCreateInstance(CLSID_TTSEnumerator, ITTSEnumW)
        self._audio = self._tts = self._ttsAttrs = None
        self.text = ""
        self.interrupted = False
        self.voices = []
        self.voiceModes = {}
        setDefault = False
        for mode in self._enumerate():
            if not _voiceDefault:
                try:
                    self._selectMode(mode)
                    _voiceDefault = self.voice
                    setDefault = True
                except:
                    traceback.print_exc()
                    continue
            guid = str(mode.gModeID)
            name = mode.szModeName
            self.voices.append((guid, name))
            self.voiceModes[guid] = mode
        if not self.voices:
            raise RuntimeError, "SAPI 4 not available"
        self.voiceDefault = _voiceDefault
        if voice:
            self.voice = voice
        elif not setDefault:
            self.voice = _voiceDefault
        self.indexMarks = {}
        self.nextIndexMarkID = 0
        self._sink = None
        self._sinkID = None
        self._bufSink = None
        self.say(" ")

    def _enumerate(self):
        self._enum.Reset()
        while True:
            mode = TTSMODEINFOW()
            fetched = ULONG(0)
            self._enum.Next(1, byref(mode), byref(fetched))
            if not mode.szModeName:
                break
            else:
                yield mode

    def _selectMode(self, mode):
        modeID = mode.gModeID
        if self._ttsAttrs:
            oldRate = self.rate
        else:
            oldRate = None
        self._noticeAudioStop = False
        self._sink = None
        self._sinkID = None
        self._bufSink = None
        self._tts = POINTER(ITTSCentralW)()
        self._audio = CoCreateInstance(CLSID_MMAudioDest,
                                       IAudioMultiMediaDevice)
        self._audio.DeviceNumSet(config.conf["speech"]["outputDevice"])
        self._enum.Select(modeID, byref(self._tts), self._audio)
        self._ttsAttrs = self._tts.QueryInterface(ITTSAttributesW)
        self.averagePitchDefault = self.averagePitch
        self.averagePitch = TTSATTR_MINPITCH
        self.averagePitchMin = self.averagePitch
        self.averagePitch = TTSATTR_MAXPITCH
        self.averagePitchMax = self.averagePitch
        self.averagePitch = self.averagePitchDefault
        self.rateDefault = self.rate
        self.rate = TTSATTR_MINSPEED
        self.rateMin = self.rate
        self.rate = TTSATTR_MAXSPEED
        self.rateMax = self.rate
        self.rate = self.rateDefault
        if oldRate is not None:
            try:
                self.rate = oldRate
            except:
                pass

    def say(self, text, raw=False):
        self.addText(text, raw=raw)
        self.speak()

    def sayCharacter(self, ch):
        if ch.isupper():
            newPitch = self.averagePitch + 30
            self.addText("\\pit=%d\\" % newPitch, raw=True)
        self.addText(ch)
        self.addText("\\pit=%d\\" % self.averagePitch, raw=True)
        self.speak()

    def _getRate(self):
        dwSpeed = DWORD()
        self._ttsAttrs.SpeedGet(byref(dwSpeed))
        return dwSpeed.value

    def _setRate(self, rate):
        self._ttsAttrs.SpeedSet(rate)

    def _getAveragePitch(self):
        wPitch = WORD()
        self._ttsAttrs.PitchGet(byref(wPitch))
        return wPitch.value

    def _setAveragePitch(self, pitch):
        self._ttsAttrs.PitchSet(pitch)

    def speak(self):
        if self.text:
            self._sink = Sink(self)
            self._sinkID = DWORD()
            sinkPtr = self._sink._com_pointers_[ITTSNotifySinkW._iid_]
            self._tts.Register(sinkPtr,
                               ITTSNotifySinkW._iid_, byref(self._sinkID))
            self._bufSink = BufSink(self)
            bufSinkPtr = self._bufSink._com_pointers_[ITTSBufNotifySink._iid_]
            self._tts.TextData(VOICECHARSET.CHARSET_TEXT, TTSDATAFLAG_TAGGED,
                               TextSDATA(self.text),
                               bufSinkPtr,
                               ITTSBufNotifySink._iid_)
            self.text = ""

    def stop(self):
        self.text = ""
        self.indexMarks.clear()
        del self._doneCallbacks[:]
        self._sink = None
        if self._sinkID:
            self._tts.UnRegister(self._sinkID)
            self._sinkID = None
        self._bufSink = None
        self._noticeAudioStop = False
        self._tts.AudioReset()
        mode = self.voiceModes[self.voice]
        self._selectMode(mode)

    def addText(self, text, raw=False):
        if text:
            if not raw:
                text = text.replace("\\", "\\\\")
            self.text += text

    def callWhenDone(self, func):
        self._doneCallbacks.append(func)

    def addIndexMark(self, func, args, kw):
        self.addText("\\mrk=%d\\" % self.nextIndexMarkID, raw=True)
        self.indexMarks[self.nextIndexMarkID] = (func, args, kw)
        self.nextIndexMarkID += 1

    def onIndexMark(self, markID):
        cb = self.indexMarks.get(markID)
        if cb:
            del self.indexMarks[markID]
            func, args, kw = cb
            func(*args, **kw)

    def _getVoice(self):
        mode = TTSMODEINFOW()
        self._tts.ModeGet(byref(mode))
        return str(mode.gModeID)

    def _setVoice(self, voice):
        mode = self.voiceModes[voice]
        self._selectMode(mode)

    def _getVoiceDescription(self):
        mode = TTSMODEINFOW()
        self._tts.ModeGet(byref(mode))
        return mode.szModeName

    def onAudioStart(self):
        self._noticeAudioStop = True

    def onAudioStop(self):
        if not self._noticeAudioStop:
            return
        for func in self._doneCallbacks[:]:
            try:
                func()
            except:
                traceback.print_exc()
        del self._doneCallbacks[:]
        self._noticeAudioStop = False
        self._sink = None
        if self._sinkID:
            self._tts.UnRegister(self._sinkID)
            self._sinkID = None
        self._bufSink = None

    rate = property(_getRate, _setRate)
    averagePitch = property(_getAveragePitch, _setAveragePitch)
    voice = property(_getVoice, _setVoice)
    voiceDescription = property(_getVoiceDescription)

