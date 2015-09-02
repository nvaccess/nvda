import os
import sys
import _winreg
import msvcrt
import winKernel
import config

from ctypes import *
from ctypes.wintypes import *
from comtypes import BSTR
import winUser
import eventHandler
import queueHandler
import api
import globalVars
from logHandler import log
import time
import globalVars

_remoteLib=None
_remoteLoader64=None
localLib=None
generateBeep=None
VBuf_getTextInRange=None
lastInputLanguageName=None
lastInputMethodName=None

#utility function to point an exported function pointer in a dll  to a ctypes wrapped python function
def _setDllFuncPointer(dll,name,cfunc):
	cast(getattr(dll,name),POINTER(c_void_p)).contents.value=cast(cfunc,c_void_p).value

#Implementation of nvdaController methods
@WINFUNCTYPE(c_long,c_wchar_p)
def nvdaController_speakText(text):
	focus=api.getFocusObject()
	if focus.sleepMode==focus.SLEEP_FULL:
		return -1
	import queueHandler
	import speech
	queueHandler.queueFunction(queueHandler.eventQueue,speech.speakText,text)
	return 0

@WINFUNCTYPE(c_long)
def nvdaController_cancelSpeech():
	focus=api.getFocusObject()
	if focus.sleepMode==focus.SLEEP_FULL:
		return -1
	import queueHandler
	import speech
	queueHandler.queueFunction(queueHandler.eventQueue,speech.cancelSpeech)
	return 0

@WINFUNCTYPE(c_long,c_wchar_p)
def nvdaController_brailleMessage(text):
	focus=api.getFocusObject()
	if focus.sleepMode==focus.SLEEP_FULL:
		return -1
	import queueHandler
	import braille
	queueHandler.queueFunction(queueHandler.eventQueue,braille.handler.message,text)
	return 0

def _lookupKeyboardLayoutNameWithHexString(layoutString):
	buf=create_unicode_buffer(1024)
	bufSize=c_int(2048)
	key=HKEY()
	if windll.advapi32.RegOpenKeyExW(_winreg.HKEY_LOCAL_MACHINE,u"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\"+ layoutString,0,_winreg.KEY_QUERY_VALUE,byref(key))==0:
		try:
			if windll.advapi32.RegQueryValueExW(key,u"Layout Display Name",0,None,buf,byref(bufSize))==0:
				windll.shlwapi.SHLoadIndirectString(buf.value,buf,1023,None)
				return buf.value
			if windll.advapi32.RegQueryValueExW(key,u"Layout Text",0,None,buf,byref(bufSize))==0:
				return buf.value
		finally:
			windll.advapi32.RegCloseKey(key)

@WINFUNCTYPE(c_long,c_wchar_p)
def nvdaControllerInternal_requestRegistration(uuidString):
	pid=c_long()
	windll.rpcrt4.I_RpcBindingInqLocalClientPID(None,byref(pid))
	pid=pid.value
	if not pid:
		log.error("Could not get process ID for RPC call")
		return -1;
	bindingHandle=c_long()
	bindingHandle.value=localLib.createRemoteBindingHandle(uuidString)
	if not bindingHandle: 
		log.error("Could not bind to inproc rpc server for pid %d"%pid)
		return -1
	registrationHandle=c_long()
	res=localLib.nvdaInProcUtils_registerNVDAProcess(bindingHandle,byref(registrationHandle))
	if res!=0 or not registrationHandle:
		log.error("Could not register NVDA with inproc rpc server for pid %d, res %d, registrationHandle %s"%(pid,res,registrationHandle))
		windll.rpcrt4.RpcBindingFree(byref(bindingHandle))
		return -1
	import appModuleHandler
	queueHandler.queueFunction(queueHandler.eventQueue,appModuleHandler.update,pid,helperLocalBindingHandle=bindingHandle,inprocRegistrationHandle=registrationHandle)
	return 0

@WINFUNCTYPE(c_long,c_long,c_long,c_long,c_long,c_long)
def nvdaControllerInternal_displayModelTextChangeNotify(hwnd, left, top, right, bottom):
	import displayModel
	displayModel.textChangeNotify(hwnd, left, top, right, bottom)
	return 0

@WINFUNCTYPE(c_long,c_long,c_long,c_long,c_long,c_long)
def nvdaControllerInternal_drawFocusRectNotify(hwnd, left, top, right, bottom):
	import eventHandler
	from NVDAObjects.window import Window
	focus=api.getFocusObject()
	if isinstance(focus,Window) and hwnd==focus.windowHandle:
		eventHandler.queueEvent("displayModel_drawFocusRectNotify",focus,rect=(left,top,right,bottom))
	return 0;

@WINFUNCTYPE(c_long,c_long,c_long,c_wchar_p)
def nvdaControllerInternal_logMessage(level,pid,message):
	if not log.isEnabledFor(level):
		return 0
	if pid:
		from appModuleHandler import getAppNameFromProcessID
		codepath="RPC process %s (%s)"%(pid,getAppNameFromProcessID(pid,includeExt=True))
	else:
		codepath="NVDAHelperLocal"
	log._log(level,message,[],codepath=codepath)
	return 0

def handleInputCompositionEnd(result):
	import speech
	import characterProcessing
	from NVDAObjects.inputComposition import InputComposition
	from NVDAObjects.behaviors import CandidateItem
	focus=api.getFocusObject()
	result=result.lstrip(u'\u3000 ')
	curInputComposition=None
	if isinstance(focus,InputComposition):
		curInputComposition=focus
		oldSpeechMode=speech.speechMode
		speech.speechMode=speech.speechMode_off
		eventHandler.executeEvent("gainFocus",focus.parent)
		speech.speechMode=oldSpeechMode
	elif isinstance(focus.parent,InputComposition):
		#Candidate list is still up
		curInputComposition=focus.parent
		focus.parent=focus.parent.parent
	if curInputComposition and not result:
		result=curInputComposition.compositionString.lstrip(u'\u3000 ')
	if result:
		speech.speakText(result,symbolLevel=characterProcessing.SYMLVL_ALL)

def handleInputCompositionStart(compositionString,selectionStart,selectionEnd,isReading):
	import speech
	from NVDAObjects.inputComposition import InputComposition
	from NVDAObjects.behaviors import CandidateItem
	focus=api.getFocusObject()
	if focus.parent and isinstance(focus.parent,InputComposition):
		#Candidates infront of existing composition string
		announce=not config.conf["inputComposition"]["announceSelectedCandidate"]
		focus.parent.compositionUpdate(compositionString,selectionStart,selectionEnd,isReading,announce=announce)
		return 0
	#IME keeps updating input composition while the candidate list is open
	#Therefore ignore new composition updates if candidate selections are configured for speaking.
	if config.conf["inputComposition"]["announceSelectedCandidate"] and isinstance(focus,CandidateItem):
		return 0
	if not isinstance(focus,InputComposition):
		parent=api.getDesktopObject().objectWithFocus()
		curInputComposition=InputComposition(parent=parent)
		oldSpeechMode=speech.speechMode
		speech.speechMode=speech.speechMode_off
		eventHandler.executeEvent("gainFocus",curInputComposition)
		focus=curInputComposition
		speech.speechMode=oldSpeechMode
	focus.compositionUpdate(compositionString,selectionStart,selectionEnd,isReading)

@WINFUNCTYPE(c_long,c_wchar_p,c_int,c_int,c_int)
def nvdaControllerInternal_inputCompositionUpdate(compositionString,selectionStart,selectionEnd,isReading):
	from NVDAObjects.inputComposition import InputComposition
	if selectionStart==-1:
		queueHandler.queueFunction(queueHandler.eventQueue,handleInputCompositionEnd,compositionString)
		return 0
	focus=api.getFocusObject()
	if isinstance(focus,InputComposition):
		focus.compositionUpdate(compositionString,selectionStart,selectionEnd,isReading)
	else:
		queueHandler.queueFunction(queueHandler.eventQueue,handleInputCompositionStart,compositionString,selectionStart,selectionEnd,isReading)
	return 0

def handleInputCandidateListUpdate(candidatesString,selectionIndex,inputMethod):
	candidateStrings=candidatesString.split('\n')
	import speech
	from NVDAObjects.inputComposition import InputComposition, CandidateList, CandidateItem
	focus=api.getFocusObject()
	if not (0<=selectionIndex<len(candidateStrings)):
		if isinstance(focus,CandidateItem):
			oldSpeechMode=speech.speechMode
			speech.speechMode=speech.speechMode_off
			eventHandler.executeEvent("gainFocus",focus.parent)
			speech.speechMode=oldSpeechMode
		return
	oldCandidateItemsText=None
	if isinstance(focus,CandidateItem):
		oldCandidateItemsText=focus.visibleCandidateItemsText
		parent=focus.parent
		wasCandidate=True
	else:
		parent=focus
		wasCandidate=False
	item=CandidateItem(parent=parent,candidateStrings=candidateStrings,candidateIndex=selectionIndex,inputMethod=inputMethod)
	if wasCandidate and focus.windowHandle==item.windowHandle and focus.candidateIndex==item.candidateIndex and focus.name==item.name:
		return
	if config.conf["inputComposition"]["autoReportAllCandidates"] and item.visibleCandidateItemsText!=oldCandidateItemsText:
		import ui
		ui.message(item.visibleCandidateItemsText)
	eventHandler.executeEvent("gainFocus",item)

@WINFUNCTYPE(c_long,c_wchar_p,c_long,c_wchar_p)
def nvdaControllerInternal_inputCandidateListUpdate(candidatesString,selectionIndex,inputMethod):
	queueHandler.queueFunction(queueHandler.eventQueue,handleInputCandidateListUpdate,candidatesString,selectionIndex,inputMethod)
	return 0

inputConversionModeMessages={
	1:(
		# Translators: A mode  that allows typing in the actual 'native' characters for an east-Asian input method language currently selected, rather than alpha numeric (Roman/English) characters. 
		_("Native input"),
		# Translators: a mode that lets you type in alpha numeric (roman/english) characters, rather than 'native' characters for the east-Asian input method  language currently selected.
		_("Alpha numeric input")
	),
	8:(
		# Translators: for East-Asian input methods, a mode that allows typing in full-shaped (full double-byte) characters, rather than the smaller half-shaped ones.
		_("Full shaped mode"),
		# Translators: for East-Asian input methods, a mode that allows typing in half-shaped (single-byte) characters, rather than the larger full-shaped (double-byte) ones.
		_("Half shaped mode")
	),
}

JapaneseInputConversionModeMessages= {
	# Translators: For Japanese character input: half-shaped (single-byte) alpha numeric (roman/english) mode.
	0: _("half alphanumeric"),
	# Translators: For Japanese character input: half-shaped (single-byte) Katacana input mode.
	3: _("half katakana"),
	# Translators: For Japanese character input: alpha numeric (roman/english) mode.
	8: _("alphanumeric"),
	# Translators: For Japanese character input: Hiragana input mode.
	9: _("hiragana"),
	# Translators: For Japanese character input: Katacana input mode.
	11: _("katakana"),
	# Translators: For Japanese character input: half-shaped (single-byte) alpha numeric (roman/english) mode.
	16: _("half alphanumeric"),
	# Translators: For Japanese character input: half katakana roman input mode.
	19: _("half katakana roman"),
	# Translators: For Japanese character input: alpha numeric (roman/english) mode.
	24: _("alphanumeric"),
	# Translators: For Japanese character input: Hiragana Roman input mode.
	25: _("hiragana roman"),
	# Translators: For Japanese character input: Katacana Roman input mode.
	27: _("katakana roman"),
} 

def handleInputConversionModeUpdate(oldFlags,newFlags,lcid):
	import speech
	textList=[]
	if newFlags!=oldFlags and lcid&0xff==0x11: #Japanese
		msg=JapaneseInputConversionModeMessages.get(newFlags)
		if msg:
			textList.append(msg)
	else:
		for x in xrange(32):
			x=2**x
			msgs=inputConversionModeMessages.get(x)
			if not msgs: continue
			newOn=bool(newFlags&x)
			oldOn=bool(oldFlags&x)
			if newOn!=oldOn: 
				textList.append(msgs[0] if newOn else msgs[1])
	if len(textList)>0:
		queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage," ".join(textList))

@WINFUNCTYPE(c_long,c_long,c_long,c_ulong)
def nvdaControllerInternal_inputConversionModeUpdate(oldFlags,newFlags,lcid):
	queueHandler.queueFunction(queueHandler.eventQueue,handleInputConversionModeUpdate,oldFlags,newFlags,lcid)
	return 0

@WINFUNCTYPE(c_long,c_long)
def nvdaControllerInternal_IMEOpenStatusUpdate(opened):
	if opened:
		# Translators: a message when the IME open status changes to opened
		message=_("IME opened")
	else:
		# Translators: a message when the IME open status changes to closed
		message=_("IME closed")
	import ui
	queueHandler.queueFunction(queueHandler.eventQueue,ui.message,message)
	return 0

@WINFUNCTYPE(c_long,c_long,c_ulong,c_wchar_p)
def nvdaControllerInternal_inputLangChangeNotify(threadID,hkl,layoutString):
	global lastInputMethodName, lastInputLanguageName
	focus=api.getFocusObject()
	#This callback can be called before NVDa is fully initialized
	#So also handle focus object being None as well as checking for sleepMode
	if not focus or focus.sleepMode:
		return 0
	import NVDAObjects.window
	#Generally we should not allow input lang changes from threads that are not focused.
	#But threadIDs for console windows are always wrong so don't ignore for those.
	if not isinstance(focus,NVDAObjects.window.Window) or (threadID!=focus.windowThreadID and focus.windowClassName!="ConsoleWindowClass"):
		return 0
	import sayAllHandler
	#Never announce changes while in sayAll (#1676)
	if sayAllHandler.isRunning():
		return 0
	import queueHandler
	import ui
	languageID=hkl&0xffff
	buf=create_unicode_buffer(1024)
	res=windll.kernel32.GetLocaleInfoW(languageID,2,buf,1024)
	# Translators: the label for an unknown language when switching input methods.
	inputLanguageName=buf.value if res else _("unknown language")
	layoutStringCodes=[]
	inputMethodName=None
	#layoutString can either be a real input method name, a hex string for an input method name in the registry, or an empty string.
	#If its a real input method name its used as is.
	#If its a hex string or its empty, then the method name is looked up by trying:
	#The full hex string, the hkl as a hex string, the low word of the hex string or hkl, the high word of the hex string or hkl.
	if layoutString:
		try:
			int(layoutString,16)
			layoutStringCodes.append(layoutString)
		except ValueError:
			inputMethodName=layoutString
	if not inputMethodName:
		layoutStringCodes.insert(0,hex(hkl)[2:].rstrip('L').upper().rjust(8,'0'))
		for stringCode in list(layoutStringCodes):
			layoutStringCodes.append(stringCode[4:].rjust(8,'0'))
			if stringCode[0]<'D':
				layoutStringCodes.append(stringCode[0:4].rjust(8,'0'))
		for stringCode in layoutStringCodes:
			inputMethodName=_lookupKeyboardLayoutNameWithHexString(stringCode)
			if inputMethodName: break
	if not inputMethodName:
		log.debugWarning("Could not find layout name for keyboard layout, reporting as unknown") 
		# Translators: The label for an unknown input method when switching input methods. 
		inputMethodName=_("unknown input method")
	if ' - ' in inputMethodName:
		inputMethodName="".join(inputMethodName.split(' - ')[1:])
	if inputLanguageName!=lastInputLanguageName:
		lastInputLanguageName=inputLanguageName
		# Translators: the message announcing the language and keyboard layout when it changes
		inputMethodName=_("{language} - {layout}").format(language=inputLanguageName,layout=inputMethodName)
	if inputMethodName!=lastInputMethodName:
		lastInputMethodName=inputMethodName
		queueHandler.queueFunction(queueHandler.eventQueue,ui.message,inputMethodName)
	return 0

@WINFUNCTYPE(c_long,c_long,c_wchar)
def nvdaControllerInternal_typedCharacterNotify(threadID,ch):
	focus=api.getFocusObject()
	if focus.windowClassName!="ConsoleWindowClass":
		eventHandler.queueEvent("typedCharacter",focus,ch=ch)
	return 0

@WINFUNCTYPE(c_long, c_int, c_int)
def nvdaControllerInternal_vbufChangeNotify(rootDocHandle, rootID):
	import virtualBuffers
	virtualBuffers.VirtualBuffer.changeNotify(rootDocHandle, rootID)
	return 0

@WINFUNCTYPE(c_long, c_wchar_p)
def nvdaControllerInternal_installAddonPackageFromPath(addonPath):
	import wx
	from gui import addonGui
	log.debug("Requesting installation of add-on from %s", addonPath)
	wx.CallAfter(addonGui.AddonsDialog.handleRemoteAddonInstall, addonPath)
	return 0

class RemoteLoader64(object):

	def __init__(self):
		# Create a pipe so we can write to stdin of the loader process.
		pipeReadOrig, self._pipeWrite = winKernel.CreatePipe(None, 0)
		# Make the read end of the pipe inheritable.
		pipeRead = self._duplicateAsInheritable(pipeReadOrig)
		winKernel.closeHandle(pipeReadOrig)
		# stdout/stderr of the loader process should go to nul.
		with file("nul", "w") as nul:
			nulHandle = self._duplicateAsInheritable(msvcrt.get_osfhandle(nul.fileno()))
		# Set the process to start with the appropriate std* handles.
		si = winKernel.STARTUPINFO(dwFlags=winKernel.STARTF_USESTDHANDLES, hSTDInput=pipeRead, hSTDOutput=nulHandle, hSTDError=nulHandle)
		pi = winKernel.PROCESS_INFORMATION()
		# Even if we have uiAccess privileges, they will not be inherited by default.
		# Therefore, explicitly specify our own process token, which causes them to be inherited.
		token = winKernel.OpenProcessToken(winKernel.GetCurrentProcess(), winKernel.MAXIMUM_ALLOWED)
		try:
			winKernel.CreateProcessAsUser(token, None, u"lib64/nvdaHelperRemoteLoader.exe", None, None, True, None, None, None, si, pi)
			# We don't need the thread handle.
			winKernel.closeHandle(pi.hThread)
			self._process = pi.hProcess
		except:
			winKernel.closeHandle(self._pipeWrite)
			raise
		finally:
			winKernel.closeHandle(pipeRead)
			winKernel.closeHandle(token)

	def _duplicateAsInheritable(self, handle):
		curProc = winKernel.GetCurrentProcess()
		return winKernel.DuplicateHandle(curProc, handle, curProc, 0, True, winKernel.DUPLICATE_SAME_ACCESS)

	def terminate(self):
		# Closing the write end of the pipe will cause EOF for the waiting loader process, which will then exit gracefully.
		winKernel.closeHandle(self._pipeWrite)
		# Wait until it's dead.
		winKernel.waitForSingleObject(self._process, winKernel.INFINITE)
		winKernel.closeHandle(self._process)

def initialize():
	global _remoteLib, _remoteLoader64, localLib, generateBeep,VBuf_getTextInRange
	localLib=cdll.LoadLibrary('lib/nvdaHelperLocal.dll')
	for name,func in [
		("nvdaController_speakText",nvdaController_speakText),
		("nvdaController_cancelSpeech",nvdaController_cancelSpeech),
		("nvdaController_brailleMessage",nvdaController_brailleMessage),
		("nvdaControllerInternal_requestRegistration",nvdaControllerInternal_requestRegistration),
		("nvdaControllerInternal_inputLangChangeNotify",nvdaControllerInternal_inputLangChangeNotify),
		("nvdaControllerInternal_typedCharacterNotify",nvdaControllerInternal_typedCharacterNotify),
		("nvdaControllerInternal_displayModelTextChangeNotify",nvdaControllerInternal_displayModelTextChangeNotify),
		("nvdaControllerInternal_logMessage",nvdaControllerInternal_logMessage),
		("nvdaControllerInternal_inputCompositionUpdate",nvdaControllerInternal_inputCompositionUpdate),
		("nvdaControllerInternal_inputCandidateListUpdate",nvdaControllerInternal_inputCandidateListUpdate),
		("nvdaControllerInternal_IMEOpenStatusUpdate",nvdaControllerInternal_IMEOpenStatusUpdate),
		("nvdaControllerInternal_inputConversionModeUpdate",nvdaControllerInternal_inputConversionModeUpdate),
		("nvdaControllerInternal_vbufChangeNotify",nvdaControllerInternal_vbufChangeNotify),
		("nvdaControllerInternal_installAddonPackageFromPath",nvdaControllerInternal_installAddonPackageFromPath),
		("nvdaControllerInternal_drawFocusRectNotify",nvdaControllerInternal_drawFocusRectNotify),
	]:
		try:
			_setDllFuncPointer(localLib,"_%s"%name,func)
		except AttributeError as e:
			log.error("nvdaHelperLocal function pointer for %s could not be found, possibly old nvdaHelperLocal dll"%name,exc_info=True)
			raise e
	localLib.nvdaHelperLocal_initialize()
	generateBeep=localLib.generateBeep
	generateBeep.argtypes=[c_char_p,c_float,c_int,c_int,c_int]
	generateBeep.restype=c_int
	# Handle VBuf_getTextInRange's BSTR out parameter so that the BSTR will be freed automatically.
	VBuf_getTextInRange = CFUNCTYPE(c_int, c_int, c_int, c_int, POINTER(BSTR), c_int)(
		("VBuf_getTextInRange", localLib),
		((1,), (1,), (1,), (2,), (1,)))
	#Load nvdaHelperRemote.dll but with an altered search path so it can pick up other dlls in lib
	h=windll.kernel32.LoadLibraryExW(os.path.abspath(ur"lib\nvdaHelperRemote.dll"),0,0x8)
	if not h:
		log.critical("Error loading nvdaHelperRemote.dll: %s" % WinError())
		return
	_remoteLib=CDLL("nvdaHelperRemote",handle=h)
	if _remoteLib.injection_initialize(globalVars.appArgs.secure) == 0:
		raise RuntimeError("Error initializing NVDAHelperRemote")
	if not _remoteLib.installIA2Support():
		log.error("Error installing IA2 support")
	#Manually start the in-process manager thread for this NVDA main thread now, as a slow system can cause this action to confuse WX
	_remoteLib.initInprocManagerThreadIfNeeded()
	if os.environ.get('PROCESSOR_ARCHITEW6432')=='AMD64':
		_remoteLoader64=RemoteLoader64()

def terminate():
	global _remoteLib, _remoteLoader64, localLib, generateBeep, VBuf_getTextInRange
	if not _remoteLib.uninstallIA2Support():
		log.debugWarning("Error uninstalling IA2 support")
	if _remoteLib.injection_terminate() == 0:
		raise RuntimeError("Error terminating NVDAHelperRemote")
	_remoteLib=None
	if _remoteLoader64:
		_remoteLoader64.terminate()
		_remoteLoader64=None
	generateBeep=None
	VBuf_getTextInRange=None
	localLib.nvdaHelperLocal_terminate()
	localLib=None
