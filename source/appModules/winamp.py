#appModules/winamp.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
import winKernel
import winUser
from scriptHandler import isScriptWaiting
from NVDAObjects.IAccessible import IAccessible 
import _default
import speech
import locale
import controlTypes
import api

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
	return winUser.sendMessage(hwndWinamp,WM_WA_IPC,0,IPC_GET_SHUFFLE)

def getRepeat():
	global hwndWinamp
	return winUser.sendMessage(hwndWinamp,WM_WA_IPC,0,IPC_GET_REPEAT)

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		global hwndWinamp
		hwndWinamp=windll.user32.FindWindowA("Winamp v1.x",None)
		if obj.windowClassName=="Winamp PE":
			obj.__class__=winampPlaylistEditor
		elif obj.windowClassName=="Winamp v1.x":
			obj.__class__=winampMainWindow

class winampMainWindow(IAccessible):

	def event_nameChange(self):
		pass

	def script_shuffleToggle(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			if getShuffle():
				onOff=_("on")
			else:
				onOff=_("off")
			speech.speakMessage(onOff)

	def script_repeatToggle(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			if getRepeat():
				onOff=_("on")
			else:
				onOff=_("off")
			speech.speakMessage(onOff)

class winampPlaylistEditor(winampMainWindow):

	def _get_name(self):
		curIndex=winUser.sendMessage(hwndWinamp,WM_WA_IPC,-1,IPC_PLAYLIST_GET_NEXT_SELECTED)
		if curIndex <0:
			return None
		info=fileinfo2()
		info.fileindex=curIndex
		internalInfo=winKernel.virtualAllocEx(self.processHandle,None,sizeof(info),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winKernel.writeProcessMemory(self.processHandle,internalInfo,byref(info),sizeof(info),None)
		winUser.sendMessage(self.windowHandle,WM_WA_IPC,IPC_PE_GETINDEXTITLE,internalInfo)
		winKernel.readProcessMemory(self.processHandle,internalInfo,byref(info),sizeof(info),None)
		winKernel.virtualFreeEx(self.processHandle,internalInfo,0,winKernel.MEM_RELEASE)
		return unicode("%d.\t%s\t%s"%(curIndex+1,info.filetitle,info.filelength), errors="replace", encoding=locale.getlocale()[1])

	def _get_role(self):
		return controlTypes.ROLE_LISTITEM

	def script_changeItem(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			speech.speakObject(self,reason=speech.REASON_FOCUS)

	def event_nameChange(self):
		return super(winampMainWindow,self).event_nameChange()

[winampMainWindow.bindKey(keyName,scriptName) for keyName,scriptName in [
	("s","shuffleToggle"),
	("r","repeatToggle"),
]]

[winampPlaylistEditor.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","changeItem"),
	("ExtendedDown","changeItem"),
	("extendedPrior","changeItem"),
	("extendedNext","changeItem"),
]]
