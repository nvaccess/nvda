import re
import winsound
import time
import struct
import difflib
import ctypes
import comtypes.automation
import comtypesClient
import debug
from keyboardHandler import sendKey, key 
import MSAAHandler
import winUser
import winKernel
import audio
import api
from config import conf
from constants import *
import window
import textBuffer
import ITextDocument

def getNVDAObjectFromEvent(hwnd,objectID,childID):
	accHandle=MSAAHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=NVDAObject_MSAA(pacc,child,origEventLocator=(hwnd,objectID,childID))
	return obj

def getNVDAObjectFromPoint(x,y):
	accHandle=MSAAHandler.accessibleObjectFromPoint(x,y)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=NVDAObject_MSAA(pacc,child)
	return obj

def registerNVDAObjectClass(processID,windowClass,objectRole,cls):
	_dynamicMap[(processID,windowClass,objectRole)]=cls

def unregisterNVDAObjectClass(windowClass,objectRole):
	del _dynamicMap[(processID,windowClass,objectRole)]

class NVDAObject_MSAA(window.NVDAObject_window):
	"""
the NVDAObject for MSAA
@ivar MSAAChildID: the MSAA object's child ID
@type MSAAChildID: int
@ivar MSAAOrigEventLocator: The origional window,objectID,childID from an MSAA event that caused this object to be created. If these are all None then the object was created by some form of navigation from another object.
@type MSAAOrigEventLocator: tuple
"""

	def __new__(cls,pacc,child,origEventLocator=(None,None,None)):
		"""
Checks the window class and IAccessible role against a map of NVDAObject_MSAA sub-types, and if a match is found, returns that rather than just NVDAObject_MSAA.
"""  
		oldCls=cls
		hwnd=MSAAHandler.windowFromAccessibleObject(pacc)
		windowClass=winUser.getClassName(hwnd)
		processID=winUser.getWindowThreadProcessID(hwnd)
		objectRole=MSAAHandler.accRole(pacc,child)
		if _dynamicMap.has_key((processID,windowClass,objectRole)):
			cls=_dynamicMap[(processID,windowClass,objectRole)]
		elif _dynamicMap.has_key((processID,windowClass,None)):
			cls=_dynamicMap[(processID,windowClass,None)]
		elif _dynamicMap.has_key((processID,None,objectRole)):
			cls=_dynamicMap[(processID,None,objectRole)]
		elif _staticMap.has_key((windowClass,objectRole)):
			cls=_staticMap[(windowClass,objectRole)]
		elif _staticMap.has_key((windowClass,None)):
			cls=_staticMap[(windowClass,None)]
		elif _staticMap.has_key((None,objectRole)):
			cls=_staticMap[(None,objectRole)]
		else:
			cls=NVDAObject_MSAA
		obj=window.NVDAObject_window.__new__(cls,hwnd)
		#Python will not call __init__ on the object if the class given to __new__ is different from the actual class its instanciating from 
		if cls!=oldCls:
			obj.__init__(pacc,child,origEventLocator=origEventLocator)
		return obj

	def __init__(self,pacc,child,origEventLocator=(None,None,None)):
		"""
@param pacc: a pointer to an IAccessible object
@type pacc: ctypes.POINTER(IAccessible)
@param child: A child ID that will be used on all methods of the IAccessible pointer
@type child: int
@param origEventLocator: a tuple of the origional MSAA event locator values (window,objectID,childID).
@type origEventLocator: tuple
"""
		self._pacc=pacc
		self._accChild=child
		self.MSAAOrigEventLocator=origEventLocator
		window.NVDAObject_window.__init__(self,MSAAHandler.windowFromAccessibleObject(self._pacc))
		self.allowedPositiveStates=STATE_SYSTEM_UNAVAILABLE|STATE_SYSTEM_SELECTED|STATE_SYSTEM_PRESSED|STATE_SYSTEM_CHECKED|STATE_SYSTEM_MIXED|STATE_SYSTEM_EXPANDED|STATE_SYSTEM_COLLAPSED|STATE_SYSTEM_BUSY|STATE_SYSTEM_HASPOPUP
		self._lastPositiveStates=self.calculatePositiveStates()
		self._lastNegativeStates=self.calculateNegativeStates()
		#Calculate the hash
		l=self._hashLimit
		p=self._hashPrime
		h=self._cachedHash
		h=(h+(hash(self.MSAAOrigEventLocator)*p))%l
		h=(h+(hash(self.MSAAChildID)*p))%l
		self._cachedHash=h


	def _get_name(self):
		res=MSAAHandler.accName(self._pacc,self._accChild)
		if isinstance(res,basestring):
			return res
		else:
			return ""

	def _get_value(self):
		res=MSAAHandler.accValue(self._pacc,self._accChild)
		if isinstance(res,basestring):
			return res
		else:
			return ""

	def _get_role(self):
		return MSAAHandler.accRole(self._pacc,self._accChild)

	def _get_typeString(self):
		role=self.role
		if role==ROLE_SYSTEM_CLIENT:
			role=ROLE_SYSTEM_WINDOW
		if conf["presentation"]["reportClassOfClientObjects"] and (role==ROLE_SYSTEM_WINDOW):
			typeString=self.windowClassName
		else:
			typeString=""
		return typeString+" %s"%MSAAHandler.getRoleName(role)

	def _get_states(self):
		return MSAAHandler.accState(self._pacc,self._accChild)

	def getStateName(self,state,opposite=False):
		if isinstance(state,int):
			newState=MSAAHandler.getStateText(state)
		else:
			newState=state
		if opposite:
			newState=_("not")+" "+newState
		return newState

	def _get_description(self):
		res=MSAAHandler.accDescription(self._pacc,self._accChild)
		if isinstance(res,basestring):
			return res
		else:
			return ""

	def _get_keyboardShortcut(self):
		res=MSAAHandler.accKeyboardShortcut(self._pacc,self._accChild)
		if isinstance(res,basestring):
			return res
		else:
			return ""

	def _get_MSAAChildID(self):
		return self._accChild

	def _get_childCount(self):
		count=MSAAHandler.accChildCount(self._pacc,self._accChild)
		return count

	def _get_location(self):
		location=MSAAHandler.accLocation(self._pacc,self._accChild)
		return location

	def _get_parent(self):
		res=MSAAHandler.accParent(self._pacc,self._accChild)
		if res:
			(ia,child)=res
		else:
			return None
		obj=NVDAObject_MSAA(ia,child)
		if obj and (obj.role==ROLE_SYSTEM_WINDOW):
			return obj.parent
		else:
			return obj

	def _get_next(self):
		res=MSAAHandler.accParent(self._pacc,self._accChild)
		if res:
			parentObject=NVDAObject_MSAA(res[0],res[1])
			parentRole=parentObject.role
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=MSAAHandler.accNavigate(obj._pacc,obj._accChild,NAVDIR_NEXT)
		if res:
			nextObject=NVDAObject_MSAA(res[0],res[1])
			if nextObject and (nextObject.role==ROLE_SYSTEM_WINDOW):
				nextObject=getNVDAObjectFromEvent(nextObject.windowHandle,-4,0)
			if nextObject!=self:
				return nextObject
			else:
				return None

	def _get_previous(self):
		res=MSAAHandler.accParent(self._pacc,self._accChild)
		if res:
			parentObject=NVDAObject_MSAA(res[0],res[1])
			parentRole=parentObject.role
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=MSAAHandler.accNavigate(obj._pacc,obj._accChild,NAVDIR_PREVIOUS)
		if res:
			previousObject=NVDAObject_MSAA(res[0],res[1])
			if previousObject and (previousObject.role==ROLE_SYSTEM_WINDOW):
				previousObject=getNVDAObjectFromEvent(previousObject.windowHandle,-4,0)
			if previousObject!=self:
				return previousObject
			else:
				return None

	def _get_firstChild(self):
		res=MSAAHandler.accNavigate(self._pacc,self._accChild,NAVDIR_FIRSTCHILD)
		if res:
			obj=NVDAObject_MSAA(res[0],res[1])
		else:
			return None
		if obj and (obj.role==ROLE_SYSTEM_WINDOW):
			return getNVDAObjectFromEvent(obj.windowHandle,OBJID_CLIENT,0)
		else:
			return obj

	def doDefaultAction(self):
		MSAAHandler.accDoDefaultAction(self._pacc,self._accChild)

	def _get_activeChild(self):
		res=MSAAHandler.accFocus(self._pacc)
		if res:
			return NVDAObject_MSAA(res[0],res[1])

	def hasFocus(self):
		states=0
		states=self.states
		if (states&STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		MSAAHandler.accFocus(self._pacc)

	def _get_positionString(self):
		position=""
		childID=self.MSAAChildID
		if childID>0:
			parent=self.parent
			if parent:
				parentChildCount=parent.childCount
				if parentChildCount>=childID:
					position="%s of %s"%(childID,parentChildCount)
		return position

	def event_show(self):
		if self.role==ROLE_SYSTEM_MENUPOPUP:
			self.event_menuStart()

	def updateMenuMode(self):
		if self.role not in [ROLE_SYSTEM_MENUBAR,ROLE_SYSTEM_MENUPOPUP,ROLE_SYSTEM_MENUITEM]:
			api.setMenuMode(False)
		if self.role==ROLE_SYSTEM_MENUITEM:
			audio.cancel()

	def event_mouseMove(self,x,y,oldX,oldY):
		location=self.location
		if not location or (len(location)!=4):
			return
		(left,top,width,height)=location
		right=left+width
		bottom=top+height
		if (oldX<left) or (oldX>right) or (oldY<top) or (oldY>bottom):
			audio.cancel()
			self.speakObject()

	def _get_groupName(self):
		curLocation=self.location
		groupObj=self
		while groupObj and (groupObj.role!=ROLE_SYSTEM_GROUPING):
			groupObj=groupObj.previous
		if groupObj and groupObj.role==ROLE_SYSTEM_GROUPING:
			groupLocation=groupObj.location
			if curLocation and groupLocation and (curLocation[0]>=groupLocation[0]) and (curLocation[1]>=groupLocation[1]) and ((curLocation[0]+curLocation[2])<=(groupLocation[0]+groupLocation[2])) and ((curLocation[1]+curLocation[3])<=(groupLocation[1]+groupLocation[3])):
				return groupObj.name
		return ""

	def event_gainFocus(self):
		self.updateMenuMode()
		if not (not api.getMenuMode() and (self.role==ROLE_SYSTEM_MENUITEM)):
			if conf["presentation"]["reportObjectGroupNames"] and api.getForegroundObject() and (api.getForegroundObject().role==ROLE_SYSTEM_DIALOG) and (self.MSAAChildID==0): 
				groupName=self.groupName
				if groupName:
					audio.speakMessage("%s %s"%(groupName,MSAAHandler.getRoleName(ROLE_SYSTEM_GROUPING)))
			window.NVDAObject_window.event_gainFocus(self)

	def event_menuStart(self):
		if self.role not in [ROLE_SYSTEM_MENUBAR,ROLE_SYSTEM_MENUPOPUP,ROLE_SYSTEM_MENUITEM]:
			return
		if not api.getMenuMode():
			audio.cancel()
			api.setMenuMode(True)
			self.speakObject()
			for child in self.children:
				if child.hasFocus():
					child.speakObject()
					break

	def event_valueChange(self):
		if self.hasFocus():
			audio.speakObjectProperties(value=self.value)

	def event_nameChange(self):
		if self.hasFocus():
			audio.speakObjectProperties(name=self.name)

	def event_stateChange(self):
		positiveStates=self.calculatePositiveStates()
		newPositiveStates=positiveStates-(positiveStates&self._lastPositiveStates)
		negativeStates=self.calculateNegativeStates()
		newNegativeStates=negativeStates-(negativeStates&self._lastNegativeStates)
		if self.hasFocus():
			if newPositiveStates:
				audio.speakObjectProperties(stateText=self.getStateNames(newPositiveStates))
			if newNegativeStates:
				audio.speakObjectProperties(stateText=self.getStateNames(newNegativeStates,opposite=True))
		self._lastPositiveStates=positiveStates
		self._lastNegativeStates=negativeStates

	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

class NVDAObject_dialog(NVDAObject_MSAA):
	"""
	Based on NVDAObject but on foreground events, the dialog contents gets read.
	"""

	def _get_value(self):
		return ""

	def event_foreground(self):
		super(NVDAObject_dialog,self).event_foreground()
		for child in self.children:
			states=child.states
			if (not states&STATE_SYSTEM_OFFSCREEN) and (not states&STATE_SYSTEM_INVISIBLE) and (not states&STATE_SYSTEM_UNAVAILABLE):
				child.speakObject()
				if child.states&STATE_SYSTEM_FOCUSED:
					audio.speakObjectProperties(stateText=child.getStateName(STATE_SYSTEM_FOCUSED))
				if child.states&STATE_SYSTEM_DEFAULT:
					audio.speakObjectProperties(stateText=child.getStateName(STATE_SYSTEM_DEFAULT))
			if child.role==ROLE_SYSTEM_PROPERTYPAGE:
				for grandChild in child.children:
					states=grandChild.states
					if (not states&STATE_SYSTEM_OFFSCREEN) and (not states&STATE_SYSTEM_INVISIBLE) and (not states&STATE_SYSTEM_UNAVAILABLE):
						grandChild.speakObject()
						if grandChild.states&STATE_SYSTEM_FOCUSED:
							audio.speakObjectProperties(stateText=grandChild.getStateName(STATE_SYSTEM_FOCUSED))
						if grandChild.states&STATE_SYSTEM_DEFAULT:
							audio.speakObjectProperties(stateText=grandChild.getStateName(STATE_SYSTEM_DEFAULT))

class NVDAObject_TrayClockWClass(NVDAObject_MSAA):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def _get_role(self):
		return ROLE_SYSTEM_CLOCK

class NVDAObject_Shell_TrayWnd_client(NVDAObject_MSAA):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows start button and taskbar.
	"""
 
	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.speakOnForeground=False
		self.speakOnGainFocus=False

class NVDAObject_Progman_client(NVDAObject_MSAA):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows desktop.
	"""

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.speakOnForeground=False
		self.speakOnGainFocus=False

class NVDAObject_staticText(textBuffer.NVDAObject_textBuffer,NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		textBuffer.NVDAObject_textBuffer.__init__(self,*args)

	def _get_text(self):
		#return self.windowText
		return self.value

	def _get_name(self):
		return ""

	def _get_value(self):
		return super(NVDAObject_staticText,self).name

class NVDAObject_edit(textBuffer.NVDAObject_editableTextBuffer,NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)

	def _get_text(self):
		return self.windowText

	def _get_typeString(self):
		typeString=super(NVDAObject_edit,self).typeString
		if self.states&STATE_SYSTEM_PROTECTED:
			typeString=MSAAHandler.getStateName(STATE_SYSTEM_PROTECTED)+" "+typeString
		return typeString

	def _get_value(self):
		return self.currentLine

	def _get_caretRange(self):
		long=winUser.sendMessage(self.windowHandle,EM_GETSEL,0,0)
		start=winUser.LOWORD(long)
		end=winUser.HIWORD(long)
		return (start,end)

	def _get_caretPosition(self):
		long=winUser.sendMessage(self.windowHandle,EM_GETSEL,0,0)
		pos=winUser.LOWORD(long)
		return pos

	def _set_caretPosition(self,pos):
		winUser.sendMessage(self.windowHandle,EM_SETSEL,pos,pos)

	def _get_lineCount(self):
		lineCount=winUser.sendMessage(self.windowHandle,EM_GETLINECOUNT,0,0)
		if lineCount<0:
			return None
		return lineCount

	def getLineNumber(self,pos):
		return winUser.sendMessage(self.windowHandle,EM_LINEFROMCHAR,pos,0)

	def getPositionFromLineNumber(self,lineNum):
		return winUser.sendMessage(self.windowHandle,EM_LINEINDEX,lineNum,0)

	def getLineStart(self,pos):
		lineNum=self.getLineNumber(pos)
		return winUser.sendMessage(self.windowHandle,EM_LINEINDEX,lineNum,0)

	def getLineLength(self,pos):
		lineLength=winUser.sendMessage(self.windowHandle,EM_LINELENGTH,pos,0)
		if lineLength<0:
			return None
		return lineLength

	def getLine(self,pos):
		lineNum=self.getLineNumber(pos)
		lineLength=self.getLineLength(pos)
		if not lineLength:
			return None
		sizeData=struct.pack('h',lineLength)
		buf=ctypes.create_unicode_buffer(sizeData,size=lineLength+4)
		res=winUser.sendMessage(self.windowHandle,EM_GETLINE,lineNum,buf)
		return buf.value

	def nextLine(self,pos):
		lineNum=self.getLineNumber(pos)
		if lineNum+1<self.lineCount:
			return self.getPositionFromLineNumber(lineNum+1)

	def previousLine(self,pos):
		lineNum=self.getLineNumber(pos)
		if lineNum-1>=0:
			return self.getPositionFromLineNumber(lineNum-1)

	def event_caret(self):
		self.reviewPosition=self.caretPosition

	def event_valueChange(self):
		pass


class NVDAObject_checkBox(NVDAObject_MSAA):
	"""
	Based on NVDAObject, but filterStates removes the pressed state for checkboxes.
	"""

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.allowedPositiveStates=self.allowedPositiveStates-(self.allowedPositiveStates&STATE_SYSTEM_PRESSED)
		self.allowedNegativeStates=self.allowedNegativeStates|STATE_SYSTEM_CHECKED
		self._lastPositiveStates=self.calculatePositiveStates()
		self._lastNegativeStates=self.calculateNegativeStates()

class NVDAObject_outlineItem(NVDAObject_MSAA):

	def _get_level(self):
		val=super(NVDAObject_outlineItem,self).value
		try:
			return int(val)
		except:
			return None

	def _get_value(self):
		val=super(NVDAObject_outlineItem,self).value
		try:
			int(val)
		except:
			return val

class NVDAObject_tooltip(NVDAObject_MSAA):

	def _get_name(self):
		name=super(NVDAObject_tooltip,self).name
		value=super(NVDAObject_tooltip,self).value
		if name and not value:
			return ""
		else:
			return name

	def _get_value(self):
		name=super(NVDAObject_tooltip,self).name
		value=super(NVDAObject_tooltip,self).value
		if name and not value:
			return name
		else:
			return ""

	def event_toolTip(self):
		if (conf["presentation"]["reportTooltips"] and (self.role==ROLE_SYSTEM_TOOLTIP)) or (conf["presentation"]["reportHelpBalloons"] and (self.role==ROLE_SYSTEM_HELPBALLOON)):
			self.speakObject()

class NVDAObject_consoleWindowClass(NVDAObject_MSAA):

	def event_nameChange(self):
		pass

class NVDAObject_consoleWindowClassClient(textBuffer.NVDAObject_editableTextBuffer,NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)
		self.sayAllGenerator=None

	def consoleEventHook(self,handle,eventID,window,objectID,childID,threadID,timestamp):
		self.reviewPosition=self.caretPosition
		newLines=self.visibleLines
		if eventID!=EVENT_CONSOLE_UPDATE_SIMPLE:
			self.speakNewText(newLines,self.oldLines)
		self.oldLines=newLines
		num=winKernel.getConsoleProcessList((ctypes.c_int*2)(),2)
		if num<2:
			winKernel.freeConsole()

	def getConsoleVerticalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return info.consoleSize.y

	def getConsoleHorizontalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return info.consoleSize.x

	def _get_visibleRange(self):
		if not hasattr(self,"consoleHandle"):
			return (0,0) 
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		top=self.getPositionFromCoord(0,info.windowRect.top)
		bottom=self.getPositionFromCoord(0,info.windowRect.bottom+1)
		return (top,bottom)

	def _get_caretPosition(self):
		if not hasattr(self,"consoleHandle"):
			return 0
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		y=info.cursorPosition.y
		x=info.cursorPosition.x
		return self.getPositionFromCoord(x,y)

	def _get_endPosition(self):
		if not hasattr(self,"consoleHandle"):
			return 0
		return self.getConsoleVerticalLength()*self.getConsoleHorizontalLength()

	def getPositionFromCoord(self,x,y):
		if not hasattr(self,"consoleHandle"):
			return 0
		return (y*self.getConsoleHorizontalLength())+x

	def getLineStart(self,pos):
		if not hasattr(self,"consoleHandle"):
			return 0
		return pos-(pos%self.getConsoleHorizontalLength())

	def getLineNumber(self,pos):
		if not hasattr(self,"consoleHandle"):
			return 0
		return pos/self.getConsoleHorizontalLength()

	def getLine(self,pos):
		if not hasattr(self,"consoleHandle"):
			return "\0"
		maxLen=self.getConsoleHorizontalLength()
		lineNum=self.getLineNumber(pos)
		line=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,0,lineNum)
		if line.isspace():
			line=None
		else:
			line=line.rstrip()
		return line

	def _get_lineCount(self):
		if not hasattr(self,"consoleHandle"):
			return 0
		return self.getConsoleVerticalLength()

	def getLineLength(self,pos):
		if not hasattr(self,"consoleHandle"):
			return 0
		return self.getConsoleHorizontalLength()

	def _get_text(self):
		if not hasattr(self,"consoleHandle"):
			return "\0"
		maxLen=self.endPosition
		text=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,0,0)
		return text

	def _get_visibleLines(self):
		if not hasattr(self,"consoleHandle"):
			return []
		visibleRange=self.visibleRange
		visibleRange=(self.getLineNumber(visibleRange[0]),self.getLineNumber(visibleRange[1]))
		lines=[]
		for lineNum in range(visibleRange[0],visibleRange[1]+1):
			line=self.getLine(self.getPositionFromCoord(0,lineNum))
			if line:
				lines.append(line)
		return lines

	def _get_value(self):
		return ""

	def event_gainFocus(self):
		processID=self.windowProcessID[0]
		try:
			winKernel.freeConsole()
		except:
			debug.writeException("freeConsole")
			pass
		winKernel.attachConsole(processID)
		res=winKernel.getStdHandle(STD_OUTPUT_HANDLE)
		if not res:
			raise OSError("NVDAObject_consoleWindowClassClient: could not get console std handle") 
		self.consoleHandle=res
		self.consoleEventHookHandles=[]
		self.oldLines=self.visibleLines
		NVDAObject_MSAA.event_gainFocus(self)
		self.cConsoleEventHook=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(self.consoleEventHook)
		for eventID in [EVENT_CONSOLE_CARET,EVENT_CONSOLE_UPDATE_REGION,EVENT_CONSOLE_UPDATE_SIMPLE,EVENT_CONSOLE_UPDATE_SCROLL]:
			handle=winUser.setWinEventHook(eventID,eventID,0,self.cConsoleEventHook,0,0,0)
			if handle:
				self.consoleEventHookHandles.append(handle)
			else:
				raise OSError('Could not register console event %s'%eventID)
		for line in self.visibleLines:
			audio.speakText(line)

	def event_looseFocus(self):
		for handle in self.consoleEventHookHandles:
			winUser.unhookWinEvent(handle)
		del self.consoleHandle
		try:
			winKernel.freeConsole()
		except:
			pass

	def event_nameChange(self):
		pass

	def event_valueChange(self):
		pass

	def speakNewText(self,newLines,oldLines):
		diffLines=filter(lambda x: x[0]!="?",list(difflib.ndiff(oldLines,newLines)))
		for lineNum in range(len(diffLines)):
			if (diffLines[lineNum][0]=="+") and (len(diffLines[lineNum])>=3):
				if (lineNum>0) and (diffLines[lineNum-1][0]=="-") and (len(diffLines[lineNum-1])>=3):
					newText=""
					block=""
					diffChars=list(difflib.ndiff(diffLines[lineNum-1][2:],diffLines[lineNum][2:]))
					for charNum in range(len(diffChars)):
						if (diffChars[charNum][0]=="+"):
							block+=diffChars[charNum][2]
						elif block:
							audio.speakText(block)
							block=""
					if block:
						audio.speakText(block)
				else:
					audio.speakText(diffLines[lineNum][2:])

class NVDAObject_richEdit(ITextDocument.NVDAObject_ITextDocument,NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		ITextDocument.NVDAObject_ITextDocument.__init__(self,*args)

	def _get_typeString(self):
		return "rich "+super(NVDAObject_richEdit,self).typeString

	def _get_value(self):
		return self.getLine(self.caretPosition)

	def getDocumentObjectModel(self):
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		res=ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,OBJID_NATIVEOM,ctypes.byref(domPointer._iid_),ctypes.byref(domPointer))
		if res==0:
			return comtypesClient.wrap(domPointer)
		else:
			raise OSError("No ITextDocument interface")

	def _duplicateDocumentRange(self,rangeObj):
		return rangeObj.Duplicate

class NVDAObject_mozillaUIWindowClass(NVDAObject_MSAA):
	"""
	Based on NVDAObject, but on focus events, actions are performed whether or not the object really has focus.
	mozillaUIWindowClass objects sometimes do not set their focusable state properly.
	"""

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.needsFocusState=False

class NVDAObject_mozillaUIWindowClass_application(NVDAObject_mozillaUIWindowClass):
	"""
	Based on NVDAObject_mozillaUIWindowClass, but:
	*Value is always empty because otherwise it is a long url to a .shul file that generated the mozilla application.
	*firstChild is the first child that is not a tooltip or a menu popup since these don't seem to allow getNext etc.
	*On focus events, the object is not spoken automatically since focus is given to this object when moving from one object to another.
	"""

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.speakOnGainFocus=False

	def _get_value(self):
		return ""

	def _get_firstChild(self):
		try:
			children=self._pacc.accChildren()
		except:
			return None
		for child in children:
			try:
				role=child.role
				if role not in [ROLE_SYSTEM_TOOLTIP,ROLE_SYSTEM_MENUPOPUP]:
					return getNVDAObjectByAccessibleObject(child)
			except:
				pass

class NVDAObject_mozillaDocument(NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.needsFocusState=False


	def _get_value(self):
		return ""

	def _get_typeString(self):
		if self.states&STATE_SYSTEM_READONLY:
			return "Mozilla "+MSAAHandler.getRoleName(ROLE_SYSTEM_DOCUMENT)
		else:
			return _("not supported")
 
class NVDAObject_mozillaListItem(NVDAObject_MSAA):

	def _get_name(self):
		child=super(NVDAObject_mozillaListItem,self).firstChild
		if child and (child.role in [ROLE_SYSTEM_STATICTEXT,"bullet"]):
 			return child.name
		else:
			return ""

	def _get_firstChild(self):
		child=super(NVDAObject_mozillaListItem,self).firstChild
		if child and (child.role in [ROLE_SYSTEM_STATICTEXT,"bullet"]):
			child=child.next
		return child

class NVDAObject_link(NVDAObject_MSAA):
	"""
	Based on NVDAObject_MSAA, but:
	*Value is always empty otherwise it would be the full url.
	*typeString is link, visited link, or same page link depending on certain states.
	*getChildren does not include any text objects, since text objects are where the name of the link comes from.
	"""

	def _get_value(self):
		return ""

	def _get_typeString(self):
		states=self.states
		typeString=""
		if states&STATE_SYSTEM_TRAVERSED:
			typeString+="visited "
		if states&STATE_SYSTEM_SELECTABLE:
			typeString+="same page "
		typeString+=super(NVDAObject_link,self).typeString
		return typeString

class NVDAObject_mozillaText(textBuffer.NVDAObject_editableTextBuffer,NVDAObject_MSAA):
	"""
	Based on NVDAObject_mozillaContentWindowClass but:
	*If the object has a name but no value, the name is used as the value and no name is provided.
	*the role is changed to static text if it has the read only state set.
	"""

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)

	def _get_name(self):
		name=super(NVDAObject_mozillaText,self).name
		value=super(NVDAObject_mozillaText,self).value
		if (self.role==ROLE_SYSTEM_STATICTEXT):
			return ""
		else:
			return name

	def _get_role(self):
		if super(NVDAObject_mozillaText,self).states&STATE_SYSTEM_READONLY:
			return ROLE_SYSTEM_STATICTEXT
		else:
			return super(NVDAObject_mozillaText,self).role
 
	def _get_value(self):
		name=super(NVDAObject_mozillaText,self).name
		value=super(NVDAObject_mozillaText,self).value
		if (self.role==ROLE_SYSTEM_STATICTEXT):
			return name
		else:
			return value


	def _get_text(self):
		return self.value

class NVDAObject_mozillaOutlineItem(NVDAObject_MSAA):

	_re_level=re.compile('.*L([0-9]+)')
	_re_position=re.compile('.*([0-9]+) of ([0-9]+)')
	_re_children=re.compile('.*with ([0-9]+)')

	def _get_description(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		if desc.startswith('Description: '):
			return desc[13:]
		else:
			return ""

	def _get_level(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		m=self._re_level.match(desc)
		try:
			return int(m.groups()[0])
		except:
			return None

	def _get_contains(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		m=self._re_children.match(desc)
		if len(m.groups()[0])>0 and (m.groups()[0]!='0'):
			return "%s %s"%(m.groups()[0],_("items"))
		else:
			return ""

	def _get_positionString(self):
		desc=super(NVDAObject_mozillaOutlineItem,self).description
		m=self._re_position.match(desc)
		if len(m.groups())==2:
			return "%s of %s"%(m.groups()[0],m.groups()[1])
		else:
			return ""



class NVDAObject_listItem(NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.allowedNegativeStates=self.allowedNegativeStates|STATE_SYSTEM_SELECTED
		self._lastNegativeStates=self.calculateNegativeStates()

class NVDAObject_SHELLDLL_DefView_client(NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args,**vars)
		self.speakOnGainFocus=False

class NVDAObject_list(NVDAObject_MSAA):

	def _get_name(self):
		name=super(NVDAObject_list,self).name
		if not name:
			name=super(NVDAObject_MSAA,self).name
		return name

	def event_gainFocus(self):
		NVDAObject_MSAA.event_gainFocus(self)
		child=self.activeChild
		if child and (child.role==ROLE_SYSTEM_LISTITEM):
			childID=child.MSAAChildID
			hwnd=self.windowHandle
			objectID=self.MSAAOrigEventLocator[1]
			child.MSAAOrigEventLocator=(hwnd,objectID,childID)
			api.setFocusObject(child)
			child.event_gainFocus()
		else:
			audio.speakMessage("%s %s"%(self.childCount,_("items")))

class NVDAObject_progressBar(NVDAObject_MSAA):

	def event_valueChange(self):
		if conf["presentation"]["beepOnProgressBarUpdates"]:
			baseFreq=440
			winsound.Beep(int(baseFreq*(1+(float(self.value[:-1])/100.0))),100)
		super(NVDAObject_progressBar,self).event_valueChange()

class NVDAObject_internetExplorerEdit(textBuffer.NVDAObject_editableTextBuffer,NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args)

	def _get_typeString(self):
		typeString=super(NVDAObject_internetExplorerEdit,self).typeString
		if self.states&STATE_SYSTEM_PROTECTED:
			typeString=MSAAHandler.getStateName(STATE_SYSTEM_PROTECTED)+" "+typeString
		return typeString

	def _get_text(self):
		if hasattr(self,"dom"):
			try:
				r=self.dom.activeElement.createTextRange()
				text=r.text
				if not text:
					text=""
				else:
					text=text.replace('\r\n','\n')
				return text+"\0"
			except:
				return self.value
		else:
			return self.value

	def _get_caretRange(self):
		if hasattr(self,"dom"):
			try:
				bookmark=self.dom.selection.createRange().getBookmark()
				if ord(bookmark[1])==3:
					return (ord(bookmark[2])-self.positionOffset,ord(bookmark[40])-self.positionOffset)
			except:
				return None
		return None

	def _get_caretPosition(self):
		if hasattr(self,"dom"):
			try:
				bookmark=self.dom.selection.createRange().getBookmark()
				return ord(bookmark[2])-self.positionOffset
			except:
				return 0
		else:
			return 0

	def _get_value(self):
		val=super(NVDAObject_internetExplorerEdit,self).value
		if val is None:
			return ""
		elif self.states&STATE_SYSTEM_PROTECTED:
			return "*"*len(val)
		else:
			return val

	def event_gainFocus(self):
		NVDAObject_MSAA.event_gainFocus(self)
		#Create a html document com pointer and point it to the com object we receive from the internet explorer_server window
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
		lresult=winUser.sendMessage(self.windowHandle,wm,0,0)
		res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
		self.dom=comtypesClient.wrap(domPointer)
		#Find out position offset
		oldBookmark=self.dom.selection.createRange().getBookmark()
		sendKey(key("control+extendedHome"))
		sendKey(key("extendedHome"))
		bookmark=self.dom.selection.createRange().getBookmark()
		self.dom.selection.createRange().moveToBookmark(oldBookmark)
		self.positionOffset=ord(bookmark[2])
		textBuffer.NVDAObject_editableTextBuffer.__init__(self)

	def event_looseFocus(self):
		if hasattr(self,"dom"):
			del self.dom

	def script_moveByLine(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		bookmark=self.dom.selection.createRange().getBookmark()
		sendKey(key("ExtendedEnd"))
		endRange=self.dom.selection.createRange()
		sendKey(key("ExtendedHome"))
		startRange=self.dom.selection.createRange()
		startRange.setEndPoint("EndToStart",endRange)
		del endRange
		text=startRange.text
		startRange.moveToBookmark(bookmark)
		audio.speakText(text)

class NVDAObject_internetExplorerClient(NVDAObject_MSAA):

	def _get_name(self):
		return ""

	def _get_typeString(self):
		return "HTML "+super(NVDAObject_internetExplorerClient,self).typeString

	def _get_description(self):
		return ""

class NVDAObject_internetExplorerPane(textBuffer.NVDAObject_editableTextBuffer,NVDAObject_MSAA):

	def __init__(self,*args,**vars):
		NVDAObject_MSAA.__init__(self,*args)
		self.allowedPositiveStates-=(self.allowedPositiveStates&STATE_SYSTEM_READONLY)

	def _get_typeString(self):
		if hasattr(self,"dom") and self.dom.body.isContentEditable is True:
			return "HTML "+MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)
		else:
			return "HTML "+MSAAHandler.getRoleName(ROLE_SYSTEM_PANE)

	def _get_value(self):
		return ""

	def _get_text(self):
		if hasattr(self,"dom"):
			try:
				text=self.dom.body.createTextRange().text
				if text is not None:
					return text
				else:
					return "\0"
			except:
				return "\0"
 
	def _get_caretRange(self):
		if hasattr(self,"dom"):
			try:
				bookmark=self.dom.selection.createRange().getBookmark()
				if ord(bookmark[1])==3:
					return (ord(bookmark[2])-self.positionOffset,ord(bookmark[40])-self.positionOffset)
				return None
			except:
				return None

	def _get_caretPosition(self):
		if hasattr(self,"dom"):
			try:
				bookmark=self.dom.selection.createRange().getBookmark()
				return ord(bookmark[2])-13
			except:
				return 0
		else:
			return 0

	def event_gainFocus(self):
		#Create a html document com pointer and point it to the com object we receive from the internet explorer_server window
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
		lresult=winUser.sendMessage(self.windowHandle,wm,0,0)
		res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
		self.dom=comtypesClient.wrap(domPointer)
		NVDAObject_MSAA.event_gainFocus(self)
		textBuffer.NVDAObject_editableTextBuffer.__init__(self)
		if (self.dom.body.isContentEditable is True):
			oldBookmark=self.dom.selection.createRange().getBookmark()
			sendKey(key("control+extendedHome"))
			sendKey(key("extendedHome"))
			bookmark=self.dom.selection.createRange().getBookmark()
			self.dom.selection.createRange().moveToBookmark(oldBookmark)
			self.positionOffset=ord(bookmark[2])
			if (not api.isVirtualBufferPassThrough()):
				api.toggleVirtualBufferPassThrough()
		else:
			del self.dom

	def event_looseFocus(self):
		if hasattr(self,"dom"):
			del self.dom

	def script_moveByLine(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		bookmark=self.dom.selection.createRange().getBookmark()
		sendKey(key("ExtendedEnd"))
		endRange=self.dom.selection.createRange()
		sendKey(key("ExtendedHome"))
		startRange=self.dom.selection.createRange()
		startRange.setEndPoint("EndToStart",endRange)
		del endRange
		text=startRange.text
		startRange.moveToBookmark(bookmark)
		audio.speakText(text)

	def script_moveByWord(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		startRange=self.dom.selection.createRange()
		bookmark=startRange.getBookmark()
		startRange.expand("word")
		text=startRange.text
		startRange.moveToBookmark(bookmark)
		audio.speakText(text)

	def script_moveByCharacter(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		startRange=self.dom.selection.createRange()
		bookmark=startRange.getBookmark()
		startRange.expand("character")
		text=startRange.text
		startRange.moveToBookmark(bookmark)
		audio.speakSymbol(text)

	def script_delete(self,keyPress):
		if not hasattr(self,'dom'):
			return
		sendKey(keyPress)
		startRange=self.dom.selection.createRange()
		bookmark=startRange.getBookmark()
		startRange.expand("character")
		text=startRange.text
		startRange.moveToBookmark(bookmark)
		audio.speakSymbol(text)

	def script_backspace(self,keyPress):
		if not hasattr(self,'dom'):
			return
		startRange=self.dom.selection.createRange()
		bookmark=startRange.getBookmark()
		startPos=ord(bookmark[2])
		startRange.move("character",-1)
		startRange.expand("character")
		text=startRange.text
		startRange.moveToBookmark(bookmark)
		sendKey(keyPress)
		if ord(self.dom.selection.createRange().getBookmark()[2])!=startPos:
			audio.speakSymbol(text)
		else:
			audio.speakText("")


class NVDAObject_statusBar(NVDAObject_MSAA):

	def _get_value(self):
		value=""
		for child in self.children:
			if child.name is not None:
				value+="  "+child.name
		return value

###class mappings

_dynamicMap={}

_staticMap={
("Shell_TrayWnd",ROLE_SYSTEM_CLIENT):NVDAObject_Shell_TrayWnd_client,
("tooltips_class32",ROLE_SYSTEM_TOOLTIP):NVDAObject_tooltip,
("tooltips_class32",ROLE_SYSTEM_HELPBALLOON):NVDAObject_tooltip,
("Progman",ROLE_SYSTEM_CLIENT):NVDAObject_Progman_client,
(None,ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("TrayClockWClass",ROLE_SYSTEM_CLIENT):NVDAObject_TrayClockWClass,
("Edit",ROLE_SYSTEM_TEXT):NVDAObject_edit,
("Static",ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("RichEdit20W",ROLE_SYSTEM_TEXT):NVDAObject_richEdit,
("RICHEDIT50W",ROLE_SYSTEM_TEXT):NVDAObject_richEdit,
(None,ROLE_SYSTEM_CHECKBUTTON):NVDAObject_checkBox,
(None,ROLE_SYSTEM_OUTLINEITEM):NVDAObject_outlineItem,
(None,ROLE_SYSTEM_LINK):NVDAObject_link,
("MozillaUIWindowClass",None):NVDAObject_mozillaUIWindowClass,
("MozillaUIWindowClass",ROLE_SYSTEM_APPLICATION):NVDAObject_mozillaUIWindowClass_application,
("MozillaDialogClass",ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaDialogClass",ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaUIWindowClass",ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaUIWindowClass",ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaWindowClass",ROLE_SYSTEM_ALERT):NVDAObject_dialog,
("MozillaWindowClass",ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("MozillaWindowClass",ROLE_SYSTEM_TEXT):NVDAObject_mozillaText,
("MozillaDialogClass",ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("MozillaWindowClass",ROLE_SYSTEM_STATICTEXT):NVDAObject_staticText,
("MozillaContentWindowClass",ROLE_SYSTEM_TEXT):NVDAObject_mozillaText,
("MozillaWindowClass",ROLE_SYSTEM_LISTITEM):NVDAObject_mozillaListItem,
("MozillaContentWindowClass",ROLE_SYSTEM_LISTITEM):NVDAObject_mozillaListItem,
("MozillaContentWindowClass",ROLE_SYSTEM_DOCUMENT):NVDAObject_mozillaDocument,
("MozillaWindowClass",ROLE_SYSTEM_DOCUMENT):NVDAObject_mozillaDocument,
("MozillaUIWindowClass",ROLE_SYSTEM_OUTLINEITEM):NVDAObject_mozillaOutlineItem,
("MozillaContentWindowClass",ROLE_SYSTEM_OUTLINEITEM):NVDAObject_mozillaOutlineItem,
("MozillaWindowClass",ROLE_SYSTEM_OUTLINEITEM):NVDAObject_mozillaDocument,
("ConsoleWindowClass",ROLE_SYSTEM_WINDOW):NVDAObject_consoleWindowClass,
("ConsoleWindowClass",ROLE_SYSTEM_CLIENT):NVDAObject_consoleWindowClassClient,
(None,ROLE_SYSTEM_LISTITEM):NVDAObject_listItem,
("Internet Explorer_Server",ROLE_SYSTEM_PANE):NVDAObject_internetExplorerPane,
("SHELLDLL_DefView",ROLE_SYSTEM_CLIENT):NVDAObject_SHELLDLL_DefView_client,
(None,ROLE_SYSTEM_LIST):NVDAObject_list,
("msctls_progress32",ROLE_SYSTEM_PROGRESSBAR):NVDAObject_progressBar,
("Internet Explorer_Server",ROLE_SYSTEM_TEXT):NVDAObject_internetExplorerEdit,
("Internet Explorer_Server",ROLE_SYSTEM_CLIENT):NVDAObject_internetExplorerClient,
("Internet Explorer_Server",ROLE_SYSTEM_PANE):NVDAObject_internetExplorerPane,
("msctls_statusbar32",ROLE_SYSTEM_STATUSBAR):NVDAObject_statusBar,
}
