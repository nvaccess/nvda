# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
import winKernel
import winUser
from scriptHandler import isScriptWaiting
from NVDAObjects.IAccessible import IAccessible 
import appModuleHandler
import speech
import controlTypes
import api
import watchdog
import braille
import ui
import textUtils

# message used to sent many messages to winamp's main window. 
# most all of the IPC_* messages involve sending the message in the form of:
#   result = SendMessage(hwnd_winamp,WM_WA_IPC,(parameter),IPC_*);

WM_WA_IPC=winUser.WM_USER

# winamp window
IPC_GET_SHUFFLE=250
IPC_GET_REPEAT=251

# playlist editor
IPC_PLAYLIST_GET_NEXT_SELECTED=3029
IPC_PE_GETCURINDEX=100
IPC_PE_GETINDEXTOTAL=101
# in_process ONLY
IPC_PE_GETINDEXTITLE=200 #  lParam = pointer to fileinfo2 structure

class fileinfo2(Structure):
	_fields_=[
		('fileindex',c_int),
		('filetitle',c_char*256),
		('filelength',c_char*16),
	]

hwndWinamp=0

def getShuffle():
	global hwndWinamp
	return watchdog.cancellableSendMessage(hwndWinamp,WM_WA_IPC,0,IPC_GET_SHUFFLE)

def getRepeat():
	global hwndWinamp
	return watchdog.cancellableSendMessage(hwndWinamp,WM_WA_IPC,0,IPC_GET_REPEAT)

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		global hwndWinamp
		hwndWinamp = winUser.FindWindow("Winamp v1.x", None)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		if windowClass == "Winamp PE":
			clsList.insert(0, winampPlaylistEditor)
		elif windowClass == "Winamp v1.x":
			clsList.insert(0, winampMainWindow)

class winampMainWindow(IAccessible):

	def event_nameChange(self):
		pass

	def script_shuffleToggle(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			if getShuffle():
				# Translators: the user has pressed the shuffle tracks toggle in winamp, shuffle is now on.
				onOff=pgettext("shuffle", "on")
			else:
				# Translators: the user has pressed the shuffle tracks toggle in winamp, shuffle is now off.
				onOff=pgettext("shuffle", "off")
			ui.message(onOff)

	def script_repeatToggle(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			if getRepeat():
				# Translators: the user has pressed the repeat track toggle in winamp, repeat is now on.
				onOff=pgettext("repeat", "on")
			else:
				# Translators: the user has pressed the repeat track toggle in winamp, repeat is now off.
				onOff=pgettext("repeat", "off")
			ui.message(onOff)

	__gestures = {
		"kb:s": "shuffleToggle",
		"kb:r": "repeatToggle",
	}

class winampPlaylistEditor(winampMainWindow):

	def _get_name(self):
		curIndex=watchdog.cancellableSendMessage(hwndWinamp,WM_WA_IPC,-1,IPC_PLAYLIST_GET_NEXT_SELECTED)
		if curIndex <0:
			return None
		info=fileinfo2()
		info.fileindex=curIndex
		internalInfo=winKernel.virtualAllocEx(self.processHandle,None,sizeof(info),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			winKernel.writeProcessMemory(self.processHandle,internalInfo,byref(info),sizeof(info),None)
			watchdog.cancellableSendMessage(self.windowHandle,WM_WA_IPC,IPC_PE_GETINDEXTITLE,internalInfo)
			winKernel.readProcessMemory(self.processHandle,internalInfo,byref(info),sizeof(info),None)
		finally:
			winKernel.virtualFreeEx(self.processHandle,internalInfo,0,winKernel.MEM_RELEASE)
		# file title is fetched in the current locale encoding.
		# We need to decode it to unicode first. 
		encoding = textUtils.USER_ANSI_CODE_PAGE
		fileTitle=info.filetitle.decode(encoding,errors="replace")
		return "%d.\t%s\t%s"%(curIndex+1,fileTitle,info.filelength)

	def _get_role(self):
		return controlTypes.Role.LISTITEM

	def script_changeItem(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS)
			braille.handler.handleGainFocus(self)

	def event_nameChange(self):
		return super(winampMainWindow,self).event_nameChange()

	__changeItemGestures = (
		"kb:upArrow",
		"kb:downArrow",
		"kb:pageUp",
		"kb:pageDown",
	)

	def initOverlayClass(self):
		for gesture in self.__changeItemGestures:
			self.bindGesture(gesture, "changeItem")
