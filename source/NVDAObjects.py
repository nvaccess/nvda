import ctypes
import comtypes.client
import time
import difflib
import thread
import struct
import re
import win32api
import win32com
import win32con
import win32console
import win32gui
import win32process
import pyAA
import debug
import audio
from keyEventHandler import key, sendKey
from constants import *
from config import conf
import dictionaries
import api

#Some api functions specific to NVDAObjects

def getNVDAObjectClass(windowClass,objectRole):
	if dynamicMap.has_key((windowClass,objectRole)):
		return dynamicMap[(windowClass,objectRole)]
	elif dynamicMap.has_key((windowClass,None)):
		return dynamicMap[(windowClass,None)]
	elif staticMap.has_key((windowClass,objectRole)):
		return staticMap[(windowClass,objectRole)]
	elif staticMap.has_key((windowClass,None)):
		return staticMap[(windowClass,None)]
	else:
		return NVDAObject

def getNVDAObjectByAccessibleObject(accObject):
	try:
		return getNVDAObjectClass(win32gui.GetClassName(accObject.Window),accObject.Role)(accObject)
	except:
		debug.writeException("NVDAObjects.getNVDAObjectByAccessibleObject")
		return None

def getNVDAObjectByLocator(window,objectID,childID):
	try:
		obj=pyAA.AccessibleObjectFromEvent(window,objectID,childID)
		if obj.GetRole()>0:
			return getNVDAObjectByAccessibleObject(obj)
	except:
		return None

def getNVDAObjectByPoint(x,y):
	try:
		obj=pyAA.AccessibleObjectFromPoint(x,y)
		return getNVDAObjectByAccessibleObject(obj)
	except:
		return None

def registerNVDAObjectClass(windowClass,objectRole,cls):
	dynamicMap[(windowClass,objectRole)]=cls

def unregisterNVDAObjectClass(windowClass,objectRole):
	del dynamicMap[(windowClass,objectRole)]

def getRoleName(role):
	if dictionaries.roleNames.has_key(role) is True:
		return dictionaries.roleNames[role]
	else:
		return role

def createStateList(stateBits):
	stateList=[]
	for bitPos in range(32):
		bitVal=1<<bitPos
		if stateBits&bitVal:
			stateList+=[bitVal]
	return stateList

def getStateNames(states,opposite=False):
	str=""
	for state in createStateList(states):
		str="%s %s"%(str,getStateName(state,opposite=opposite))
	return str

def getStateName(state,opposite=False):
	if dictionaries.stateNames.has_key(state):
		name=dictionaries.stateNames[state]
	else:
		name=state
	if opposite is True:
		name="not %s"%name
	return name

#The classes

class NVDAObject(object):

	def __init__(self,accObject):
		self.accObject=accObject
		self.keyMap={}
		self.lastStates=self.getStates()
		self.doneFocus=False
		self.hash=self._makeHash()
	def _makeHash(self):
		l=10000000
		p=17
		h=0
		window=self.getWindowHandle()
		if isinstance(window,int):
			h=(h+(window*p))%l
		role=self.getRole()
		if isinstance(role,basestring):
			role=hash(role)
		if isinstance(role,int):
			h=(h+(role*p))%l
		childID=self.getChildID()
		if isinstance(childID,int):
			h=(h+(childID*p))%l
		location=self.getLocation()
		if location:
			left,top,right,bottom=location
			h=(h+(left*p))%l
			h=(h+(top*p))%l
			h=(h+(right*p))%l
			h=(h+(bottom*p))%l
		return h

	def __hash__(self):
		return self.hash

	def __eq__(self,other):
		if self and other and (self.getProcessID()==other.getProcessID()) and (self.getWindowHandle()==other.getWindowHandle()) and (self.getRole()==other.getRole()) and (self.getChildID()==other.getChildID()) and (self.getLocation()==other.getLocation()) and (self.getKeyboardShortcut()==other.getKeyboardShortcut()):
			return True
		else:
			return False

	def __ne__(self,other):
		if not other or (self.getProcessID()!=other.getProcessID()) or (self.getWindowHandle()!=other.getWindowHandle()) or (self.getRole()!=other.getRole()) or (self.getChildID()!=other.getChildID()) or (self.getLocation()!=other.getLocation()) or (self.getKeyboardShortcut()!=other.getKeyboardShortcut()):
			return True
		else:
			return False

	def speakObject(obj):
		window=obj.getWindowHandle()
		name=obj.getName()
		typeString=obj.getTypeString()
		stateNames=getStateNames(obj.filterStates(obj.getStates()))
		value=obj.getValue()
		description=obj.getDescription()
		if description==name:
			description=None
		help=obj.getHelp()
		if conf["presentation"]["reportKeyboardShortcuts"]:
			keyboardShortcut=obj.getKeyboardShortcut()
		else:
			keyboardShortcut=None
		position=None
		childID=obj.getChildID()
		if childID>0:
			parent=obj.getParent()
			if parent:
				parentChildCount=parent.getChildCount()
				if parentChildCount>=childID:
					position="%s of %s"%(childID,parentChildCount)
		#if role!=ROLE_SYSTEM_GROUPING:
		#	groupName=getObjectGroupName(accObject)
		#else:
		#	groupName=None
		groupName=None
		audio.speakObjectProperties(groupName=groupName,name=name,typeString=typeString,stateText=stateNames,value=value,description=description,help=help,keyboardShortcut=keyboardShortcut,position=position)

	def getWindowHandle(self):
		try:
			window=self.accObject.Window
		except:
			return None
		return window

	def getName(self):
		try:
			name=self.accObject.GetName()
		except:
			name=""
		if not name:
			window=self.getWindowHandle()
			if not window:
				return ""
			name=win32gui.GetWindowText(window)
		return name

	def getValue(self):
		value=None
		try:
			value=self.accObject.GetValue()
		except:
			pass
		if value:
			return value
		else:
			return ""

	def getRole(self):
		try:
			return self.accObject.GetRole()
		except:
			return ""

	def getTypeString(self):
		role=self.getRole()
		if conf["presentation"]["reportClassOfAllObjects"] or (conf["presentation"]["reportClassOfClientObjects"] and (role==ROLE_SYSTEM_CLIENT)):
			typeString=self.getClassName()
		else:
			typeString=""
		return typeString+" %s"%getRoleName(self.getRole())


	def getStates(self):
		states=0
		try:
			states=self.accObject.GetState()
		except:
			pass
		return states

	def filterStates(self,states):
		states-=(states&STATE_SYSTEM_FOCUSED)
		states-=(states&STATE_SYSTEM_FOCUSABLE)
		states-=(states&STATE_SYSTEM_SELECTABLE)
		states-=(states&STATE_SYSTEM_MULTISELECTABLE)
		states-=(states&STATE_SYSTEM_READONLY)
		states-=(states&STATE_SYSTEM_INVISIBLE)
		states-=(states&STATE_SYSTEM_HOTTRACKED)
		states-=(states&STATE_SYSTEM_OFFSCREEN)
		states-=(states&STATE_SYSTEM_DEFAULT)
		return states

	def getDescription(self):
		try:
			return self.accObject.GetDescription()
		except:
			return ""

	def getHelp(self):
		try:
			return self.accObject.GetHelp()
		except:
			return ""

	def getKeyboardShortcut(self):
		keyboardShortcut=None
		try:
			keyboardShortcut=self.accObject.GetKeyboardShortcut()
		except:
			return ""
		if not keyboardShortcut:
			return ""
		else:
			return keyboardShortcut

	def getChildID(self):
		try:
			return self.accObject.child
		except:
			return None

	def getChildCount(self):
		return len(self.getChildren())

	def getProcessID(self):
		try:
			return self.accObject.ProcessID
		except:
			return None

	def getLocation(self):
		try:
			return self.accObject.GetLocation()
		except:
			return None

	def getClassName(self):
		return win32gui.GetClassName(self.getWindowHandle())

	def getParent(self):
		try:
			accObject=self.accObject.GetParent()
		except:
			return None
		if accObject.GetRole()==pyAA.Constants.ROLE_SYSTEM_WINDOW:
			try:
				return getNVDAObjectByAccessibleObject(accObject.GetParent())
			except:
				return None
		else:
			return getNVDAObjectByAccessibleObject(accObject)

	def getNext(self):
		try:
			parentObject=getNVDAObjectByAccessibleObject(self.accObject.GetParent())
			parentRole=parentObject.getRole()
		except:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==ROLE_SYSTEM_WINDOW):
			try:
				next=parentObject.accObject.Navigate(pyAA.Constants.NAVDIR_NEXT)
				next=pyAA.AccessibleObjectFromWindow(next.Window,-4)
				nextObject=getNVDAObjectByAccessibleObject(next)
				if nextObject!=self:
					return nextObject
				else:
					return None
			except:
				return None
		else:
			try:
				next=self.accObject.Navigate(pyAA.Constants.NAVDIR_NEXT)
				nextObject=getNVDAObjectByAccessibleObject(next)
				if nextObject.getRole()==ROLE_SYSTEM_WINDOW:
					nextObject=api.getNVDAObjectByLocator(nextObject.getWindowHandle(),-4,0)
				if nextObject!=self:
					return nextObject
				else:
					return None
			except:
				return None

	def getPrevious(self):
		try:
			parentObject=getNVDAObjectByAccessibleObject(self.accObject.GetParent())
			parentRole=parentObject.getRole()
		except:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==ROLE_SYSTEM_WINDOW):
			try:
				prev=parentObject.accObject.Navigate(pyAA.Constants.NAVDIR_PREVIOUS)
				prev=pyAA.AccessibleObjectFromWindow(prev.Window,-4)
				prevObject=getNVDAObjectByAccessibleObject(prev)
				if prevObject!=self:
					return prevObject
				else:
					return None
			except:
				return None
		else:
			try:
				prev=self.accObject.Navigate(pyAA.Constants.NAVDIR_PREVIOUS)
				prevObject=getNVDAObjectByAccessibleObject(prev)
				if prevObject.getRole()==ROLE_SYSTEM_WINDOW:
					prevObject=api.getNVDAObjectByLocator(prevObject.getWindowHandle(),-4,0)
				if prevObject!=self:
					return prevObject
				else:
					return None
			except:
				return None

	def getFirstChild(self):
		try:
			child=self.accObject.Navigate(pyAA.Constants.NAVDIR_FIRSTCHILD)
			if child.GetRole()==pyAA.Constants.ROLE_SYSTEM_WINDOW:
				child=pyAA.AccessibleObjectFromWindow(child.Window,-4)
			childObject=getNVDAObjectByAccessibleObject(child)
			if childObject!=self:
				return childObject
			else:
				return None
		except:
			return None

	def doDefaultAction(self):
		try:
			self.accObject.DoDefaultAction()
		except:
			pass

	def getChildren(self):
		children=[]
		obj=self.getFirstChild()
		while obj:
			children.append(obj)
			obj=obj.getNext()
		return children

	def getActiveChild(self):
		try:
			child=self.accObject.GetFocus()
		except:
			return None
		return getNVDAObjectByAccessibleObject(child)

	def getSelectedChildren(self):
		try:
			accChildren=self.accObject.GetSelection()
		except:
			accChildren=[]
		children=[]
		for accChild in accChildren:
			children.append(getNVDAObjectByAccessibleObject(accChild))
		return children


	def hasFocus(self):
		states=0
		states=self.getStates()
		if (states&STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		try:
			self.accObject.SetFocus()
		except:
			pass

	def event_foreground(self):
		audio.cancel()
		self.speakObject()

	def updateVirtualBuffer(self):
		if api.getVirtualBuffer().getWindowHandle()!=self.getWindowHandle():
			api.setVirtualBuffer(self.getWindowHandle())
			audio.speakMessage("new buffer")
	def updateMenuMode(self):
		if self.getRole() not in [ROLE_SYSTEM_MENUBAR,ROLE_SYSTEM_MENUPOPUP,ROLE_SYSTEM_MENUITEM]:
			api.setMenuMode(False)

	def event_showObject(self):
		if self.getRole()==ROLE_SYSTEM_MENUPOPUP:
			self.event_menuStart()

	def event_focusObject(self):
		if self.doneFocus:
			return
		self.doneFocus=True
		self.updateMenuMode()
		if self.hasFocus() and not (not api.getMenuMode() and (self.getRole()==ROLE_SYSTEM_MENUITEM)):
			if self.getRole()==ROLE_SYSTEM_MENUITEM:
				audio.cancel()
			self.speakObject()

	def event_menuStart(self):
		if self.getRole() not in [ROLE_SYSTEM_MENUBAR,ROLE_SYSTEM_MENUPOPUP,ROLE_SYSTEM_MENUITEM]:
			return
		if not api.getMenuMode():
			audio.cancel()
			api.setMenuMode(True)
			self.speakObject()
			for child in self.getChildren():
				if child.hasFocus():
					child.speakObject()
					break

	def event_objectValueChange(self):
		if self.hasFocus():
			audio.speakObjectProperties(value=self.getValue())

	def event_objectStateChange(self):
		states=self.getStates()
		if states is None or not self.hasFocus():
			return None
		states_on=states-(states&self.lastStates)
		audio.speakObjectProperties(stateText=getStateNames(self.filterStates(states_on)))
		states_off=self.lastStates-(states&self.lastStates)
		audio.speakObjectProperties(stateText=getStateNames(self.filterStates(states_off),opposite=True))
		self.lastStates=states

	def event_objectSelection(self):
		return self.event_objectStateChange()

	def event_objectSelectionAdd(self):
		return self.event_objectStateChange()

	def event_objectSelectionRemove(self):
		return self.event_objectStateChange()

	def event_objectSelectionWithIn(self):
		return self.event_objectStateChange()

class NVDAObject_dialog(NVDAObject):
	"""
	Based on NVDAObject but on foreground events, the dialog contents gets read.
	"""

	def event_foreground(self):
		self.speakObject()
		for child in self.getChildren():
			states=child.getStates()
			if (not states&STATE_SYSTEM_OFFSCREEN) and (not states&STATE_SYSTEM_INVISIBLE) and (not states&STATE_SYSTEM_UNAVAILABLE):
				child.speakObject()
			if child.getRole()==ROLE_SYSTEM_PROPERTYPAGE:
				for grandChild in child.getChildren():
					states=grandChild.getStates()
					if (not states&STATE_SYSTEM_OFFSCREEN) and (not states&STATE_SYSTEM_INVISIBLE) and (not states&STATE_SYSTEM_UNAVAILABLE):
						grandChild.speakObject()


class NVDAObject_Shell_TrayWnd(NVDAObject):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows start button and taskbar.
	"""
 
	def event_foreground(self):
		pass

class NVDAObject_Progman(NVDAObject):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows desktop.
	"""

	def event_foreground(self):
		pass

class NVDAObject_edit(NVDAObject):
	"""
	Based on NVDAObject, but speaks moving and editing with in the edit control.
	"""

	def __init__(self,accObject):
		NVDAObject.__init__(self,accObject)
		self.keyMap={
			key("ExtendedUp"):self.script_moveByLine,
			key("ExtendedDown"):self.script_moveByLine,
			key("ExtendedLeft"):self.script_moveByCharacter,
			key("ExtendedRight"):self.script_moveByCharacter,
			key("Control+ExtendedLeft"):self.script_moveByWord,
			key("Control+ExtendedRight"):self.script_moveByWord,
			key("Shift+ExtendedRight"):self.script_changeSelection,
			key("Shift+ExtendedLeft"):self.script_changeSelection,
			key("Shift+ExtendedHome"):self.script_changeSelection,
			key("Shift+ExtendedEnd"):self.script_changeSelection,
			key("Shift+ExtendedUp"):self.script_changeSelection,
			key("Shift+ExtendedDown"):self.script_changeSelection,
			key("Control+Shift+ExtendedLeft"):self.script_changeSelection,
			key("Control+Shift+ExtendedRight"):self.script_changeSelection,
			key("ExtendedHome"):self.script_moveByCharacter,
			key("ExtendedEnd"):self.script_moveByCharacter,
			key("control+extendedHome"):self.script_moveByLine,
			key("control+extendedEnd"):self.script_moveByLine,
			key("control+shift+extendedHome"):self.script_changeSelection,
			key("control+shift+extendedEnd"):self.script_changeSelection,
			key("ExtendedDelete"):self.script_delete,
			key("Back"):self.script_backspace,
		}

	def getValue(self):
		return self.getCurrentLine()

	def getVisibleLineRange(self):
		return (self.getLineNumber(self.getStartPosition()),self.getLineNumber(self.getEndPosition()))

	def getCaretRange(self):
		word=win32gui.SendMessage(self.getWindowHandle(),win32con.EM_GETSEL,0,0)
		if word<0:
			return None
		start=win32api.LOWORD(word)
		end=win32api.HIWORD(word)
		return (start,end)

	def getCaretPosition(self):
		word=win32gui.SendMessage(self.getWindowHandle(),win32con.EM_GETSEL,0,0)
		if word<0:
			return None
		pos=win32api.LOWORD(word)
		return pos

	def getStartPosition(self):
		return 0

	def getEndPosition(self):
		return self.getTextLength()

	def getLineCount(self):
		lineCount=win32gui.SendMessage(self.getWindowHandle(),win32con.EM_GETLINECOUNT,0,0)
		if lineCount<0:
			return None
		return lineCount

	def getLineNumber(self,pos):
		return win32gui.SendMessage(self.getWindowHandle(),win32con.EM_LINEFROMCHAR,pos,0)

	def getLineStart(self,lineNum):
		return win32gui.SendMessage(self.getWindowHandle(),win32con.EM_LINEINDEX,lineNum,0)

	def getLineLength(self,lineNum):
		lineStart=self.getLineStart(lineNum)
		lineLength=win32gui.SendMessage(self.getWindowHandle(),win32con.EM_LINELENGTH,lineStart,0)
		if lineLength<0:
			return None
		return lineLength

	def getLine(self,lineNum):
		lineLength=self.getLineLength(lineNum)
		if not lineLength:
			return None
		lineBuf=struct.pack('i',lineLength+1)
		lineBuf=lineBuf+"".ljust(lineLength-2)
		res=win32gui.SendMessage(self.getWindowHandle(),win32con.EM_GETLINE,lineNum,lineBuf)
		line="%s"%lineBuf[0:lineLength]
		return line

	def getCurrentLine(self):
		return self.getLine(self.getLineNumber(self.getCaretPosition()))

	def nextCharacter(self,pos):
		if pos<self.getEndPosition():
			return pos+1
		else:
			return None

	def previousCharacter(self,pos):
		if pos>self.getStartPosition():
			return pos-1
		else:
			return None

	def nextWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		curPos=pos
		while curPos and (self.getCharacter(curPos) not in whitespace):
			curPos=self.nextCharacter(curPos)
		while curPos and (self.getCharacter(curPos) in whitespace):
			curPos=self.nextCharacter(curPos)
		return curPos

	def previousWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		curPos=pos
		while (curPos>0) and (self.getCharacter(curPos) not in whitespace):
			curPos=self.previousCharacter(curPos)
		while (curPos>0) and (self.getCharacter(curPos) in whitespace):
			curPos=self.previousCharacter(curPos)
		while (curPos>0) and (self.getCharacter(curPos) not in whitespace):
			curPos=self.previousCharacter(curPos)
		if curPos:
			return curPos
		else:
			return None

 
	def getTextLength(self):
		return ctypes.windll.user32.SendMessageW(self.getWindowHandle(),win32con.WM_GETTEXTLENGTH,0,0)

	def getText(self):
		textLength=self.getTextLength()
		textBuf=ctypes.create_unicode_buffer(textLength+1)
		ctypes.windll.user32.SendMessageW(self.getWindowHandle(),win32con.WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value+u""

	def getTextRange(self,start,end):
		text=self.getText()
		if (start>=end) or (end>len(text)):
			return None
		return text[start:end]

	def getCharacter(self,pos):
		return self.getTextRange(pos,pos+1)

	def getCurrentCharacter(self):
		return self.getCharacter(self.getCaretPosition())

	def getWord(self,pos):
		nextWord=self.nextWord(pos)
		if nextWord:
			return self.getTextRange(self.previousWord(nextWord),nextWord)
		else:
			return self.getTextRange(pos,self.getEndPosition())

	def getCurrentWord(self):
		return self.getWord(self.getCaretPosition())

	def event_caret(self):
		api.setVirtualBufferCursor(api.getVirtualBuffer().getCaretPosition())

	def script_moveByLine(self,keyPress):
		sendKey(keyPress)
		audio.speakText(self.getCurrentLine())

	def script_moveByCharacter(self,keyPress):
		sendKey(keyPress)
		audio.speakSymbol(self.getCurrentCharacter())

	def script_moveByWord(self,keyPress):
		sendKey(keyPress)
		audio.speakText(self.getCurrentWord())

	def script_changeSelection(self,keyPress):
		selectionPoints=self.getCaretRange()
		sendKey(keyPress)
		newSelectionPoints=self.getCaretRange()
		if newSelectionPoints and not selectionPoints:
			audio.speakText("selected %s"%self.getTextRange(newSelectionPoints[0],newSelectionPoints[1]))
		elif not newSelectionPoints:
			audio.speakSymbol(self.getCharacter())
		elif selectionPoints and newSelectionPoints: 
			if newSelectionPoints[1]>selectionPoints[1]:
				audio.speakText("selected %s"%self.getTextRange(selectionPoints[1],newSelectionPoints[1]))
			elif newSelectionPoints[0]>selectionPoints[0]:
				audio.speakText("unselected %s"%self.getTextRange(selectionPoints[0],newSelectionPoints[0]))
			elif newSelectionPoints[1]<selectionPoints[1]:
				audio.speakText("unselected %s"%self.getTextRange(newSelectionPoints[1],selectionPoints[1]))
			elif newSelectionPoints[0]<selectionPoints[0]:
				audio.speakText("selected %s"%self.getTextRange(newSelectionPoints[0],selectionPoints[0]))

	def script_delete(self,keyPress):
		sendKey(keyPress)
		audio.speakSymbol(self.getCurrentCharacter())

	def script_backspace(self,keyPress):
		point=self.getCaretPosition()

		if not point==self.getStartPosition():
			delChar=self.getCharacter(self.previousCharacter(point))
			sendKey(keyPress)
			newPoint=self.getCaretPosition()
			if newPoint<point:
				audio.speakSymbol(delChar)
		else:
			sendKey(keyPress)

	def event_objectValueChange(self):
		pass

class NVDAObject_checkBox(NVDAObject):
	"""
	Based on NVDAObject, but filterStates removes the pressed state for checkboxes.
	"""

	def filterStates(self,states):
		states=NVDAObject.filterStates(self,states)
		states-=states&pyAA.Constants.STATE_SYSTEM_PRESSED
		return states

class NVDAObject_mozillaUIWindowClass(NVDAObject):
	"""
	Based on NVDAObject, but on focus events, actions are performed whether or not the object really has focus.
	mozillaUIWindowClass objects sometimes do not set their focusable state properly.
	"""

	def event_focusObject(self):
		if api.getVirtualBuffer().getWindowHandle()!=api.getForegroundWindow():
			api.setVirtualBuffer(api.getForegroundWindow())
		api.setVirtualBufferCursor(api.getVirtualBuffer().getCaretPosition())
		self.speakObject()

class NVDAObject_mozillaUIWindowClass_application(NVDAObject_mozillaUIWindowClass):
	"""
	Based on NVDAObject_mozillaUIWindowClass, but:
	*Value is always empty because otherwise it is a long url to a .shul file that generated the mozilla application.
	*firstChild is the first child that is not a tooltip or a menu popup since these don't seem to allow getNext etc.
	*On focus events, the object is not spoken automatically since focus is given to this object when moving from one object to another.
	"""

	def getValue(self):
		return ""

	def event_focusObject(self):
		self.updateVirtualBuffer()

	def getFirstChild(self):
		try:
			children=self.accObject.GetChildren()
		except:
			return None
		for child in children:
			try:
				role=child.GetRole()
				if role not in [ROLE_SYSTEM_TOOLTIP,ROLE_SYSTEM_MENUPOPUP]:
					return getNVDAObjectByAccessibleObject(child)
			except:
				pass


class NVDAObject_mozillaContentWindowClass(NVDAObject):
	"""
	Based on NVDAObject, but updateVirtualBuffer only updates the cursor position, not the actual buffer since only the document object should do this. 
	"""

class NVDAObject_mozillaContentWindowClass_document(NVDAObject_mozillaContentWindowClass):
	"""
	Based on NVDAObject_mozillaContentWindowClass but:
	*Value is always empty because otherwise it is the URL of the document.
	*updateVirtualBuffer loads the document --- this window and its decendant objects in to the buffer if the busy state is not set, rather than the 	foreground window. It then speaks the contents.
	*event_objectStateChange reports that the document is loading if the busy state is turned on, but if it is turned off, it updates the virtualBuffer.
	"""

	def getValue(self):
		return ""

class NVDAObject_mozillaContentWindowClass_link(NVDAObject_mozillaContentWindowClass):
	"""
	Based on NVDAObject_mozillaContentWindowClass, but:
	*Value is always empty otherwise it would be the full url.
	*typeString is link, visited link, or same page link depending on certain states.
	*filterStates filters out linked and traversed since these don't need to be reported.
	*getChildren does not include any text objects, since text objects are where the name of the link comes from.
	"""

	def getValue(self):
		return ""

	def filterStates(self,states):
		states=NVDAObject_mozillaContentWindowClass.filterStates(self,states)
		states-=(states&STATE_SYSTEM_LINKED)
		states-=(states&STATE_SYSTEM_TRAVERSED)
		return states

	def getTypeString(self):
		states=self.getStates()
		typeString=""
		if states&STATE_SYSTEM_TRAVERSED:
			typeString+="visited "
		if states&STATE_SYSTEM_SELECTED:
			typeString+="same page "
		typeString+=NVDAObject.getTypeString(self)
		return typeString

	def getChildren(self):
		children=NVDAObject.getChildren(self)
		newChildren=[]
		for child in children:
			if child.getRole()!=ROLE_SYSTEM_STATICTEXT:
				newChildren.append(child)
		return newChildren

class NVDAObject_mozillaContentWindowClass_listItem(NVDAObject_mozillaContentWindowClass):
	"""
	Based on NVDAObject_mozillaContentWindowClass, but:
	*Name is the bullet or counter for the list item which is found in the text object which is the first child of this object.
	*getChildren ignores the first child wich is the text object that contains the bullet or counter for the list item.
	"""

	def getName(self):
		child=self.getFirstChild()
		if child and self.getRole()==ROLE_SYSTEM_STATICTEXT:
			name=child.getName()
		else:
			name=""
		return name

	def getChildren(self):
		children=NVDAObject.getChildren(self)
		if (len(children)>=1) and (NVDAObject.getRole(children[0])==ROLE_SYSTEM_STATICTEXT):
			del children[0]
		return children

class NVDAObject_mozillaContentWindowClass_text(NVDAObject_mozillaContentWindowClass):
	"""
	Based on NVDAObject_mozillaContentWindowClass but:
	*If the object has a name but no value, the name is used as the value and no name is provided.
	*the role is changed to static text if it has the read only state set.
	"""

	def getName(self):
		name=NVDAObject.getName(self)
		value=NVDAObject.getValue(self)
		if name and not value:
			return ""
		else:
			return name

	def getRole(self):
		if NVDAObject.getStates(self)&STATE_SYSTEM_READONLY:
			return ROLE_SYSTEM_STATICTEXT
		else:
			return NVDAObject.getRole(self)

	def getValue(self):
		name=NVDAObject.getName(self)
		value=NVDAObject.getValue(self)
		if name and not value:
			return name
		else:
			return ""

class NVDAObject_TrayClockWClass(NVDAObject):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def getRole(self):
		return ROLE_SYSTEM_CLOCK

class NVDAObject_consoleWindowClass(NVDAObject_edit):

	def __init__(self,accObject):
		NVDAObject_edit.__init__(self,accObject)
		processID=win32process.GetWindowThreadProcessId(self.getWindowHandle())[1]
		try:
			win32console.FreeConsole()
		except:
			pass
		win32console.AttachConsole(processID)
		self.consoleBuffer=win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
		debug.writeMessage("console settings: %s"%self.consoleBuffer.GetConsoleScreenBufferInfo())

	def __del__(self):
		self.keepUpdating=False
		time.sleep(0.1)
		NVDAObject_edit.__del__(self)

	def getConsoleVerticalLength(self):
		info=self.consoleBuffer.GetConsoleScreenBufferInfo()
		return info["Size"].Y

	def getConsoleHorizontalLength(self):
		info=self.consoleBuffer.GetConsoleScreenBufferInfo()
		return info["Size"].X

	def getVisibleLineRange(self):
		info=self.consoleBuffer.GetConsoleScreenBufferInfo()
		topLineNum=info["Window"].Top
		bottomLineNum=info["Window"].Bottom
		return (topLineNum,bottomLineNum)

	def getCaretPosition(self):
		info=self.consoleBuffer.GetConsoleScreenBufferInfo()
		y=info["CursorPosition"].Y
		x=info["CursorPosition"].X
		return self.getLineStart(y)+x

	def getEndPosition(self):
		return self.getConsoleVerticalLength()*self.getConsoleHorizontalLength()

	def getLineStart(self,lineNum):
		return lineNum*self.getConsoleHorizontalLength()

	def getLineNumber(self,pos):
		return pos/self.getConsoleHorizontalLength()

	def getLine(self,lineNum):
		maxLen=self.getConsoleHorizontalLength()
		line=self.consoleBuffer.ReadConsoleOutputCharacter(maxLen,win32console.PyCOORDType(0,lineNum))
		if line.isspace():
			line=None
		else:
			line=line.rstrip()
		return line

	def getLineCount(self):
		return self.getConsoleVerticalLength()

	def getLineLength(self,index=None):
		line=self.getLine()
		if line is None:
			return 0
		else:
			return len(line)

	def getText(self):
		maxLen=self.getEndPosition()
		text=self.consoleBuffer.ReadConsoleOutputCharacter(maxLen,win32console.PyCOORDType(0,0))
		return text

	def getVisibleLines(self):
		visibleRange=self.getVisibleLineRange()
		lines=[]
		for lineNum in range(visibleRange[0],visibleRange[1]+1):
			line=self.getLine(lineNum)
			if line:
				lines.append(line)
		return lines

	def event_focusObject(self):
		self.keepUpdating=True
		self._oldestLines=None
		self.thread=thread.start_new_thread(self._consoleUpdater,())
		self.updateVirtualBuffer()
		for line in self.getVisibleLines():
			audio.speakText(line)

	def _consoleUpdater(self):
		try:
			oldCaretPosition=api.getVirtualBuffer().getCaretPosition()
			oldLines=self.getVisibleLines()
			while self.keepUpdating and win32gui.IsWindow(self.getWindowHandle()):
				newCaretPosition=api.getVirtualBuffer().getCaretPosition()
				if newCaretPosition!=oldCaretPosition:
					api.setVirtualBufferCursor(newCaretPosition)
					oldCaretPosition=newCaretPosition
				newLines=self.getVisibleLines()
				if newLines!=oldLines:
					if not self._oldestLines:
						self._oldestLines=oldLines
					oldLines=newLines
				elif self._oldestLines:
					diffLines=filter(lambda x: x[0]!="?",list(difflib.ndiff(self._oldestLines,newLines)))
					self._oldestLines=None
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
				time.sleep(0.1)
		except:
			debug.writeException("NVDAObject_consoleWindowClass._consoleUpdater")

class NVDAObject_tooltip(NVDAObject):

	def getName(self):
		name=NVDAObject.getName(self)
		value=NVDAObject.getValue(self)
		if name and not value:
			return ""
		else:
			return name

	def getValue(self):
		name=NVDAObject.getName(self)
		value=NVDAObject.getValue(self)
		if name and not value:
			return name
		else:
			return ""

	def event_showObject(self):
		if conf["presentation"]["reportTooltips"]:
			self.speakObject()

class NVDAObject_ITextDocument(NVDAObject_edit):

	def __init__(self,accObject):
		NVDAObject_edit.__init__(self,accObject)
		self.msftedit=comtypes.client.GetModule('msftedit.dll')
		ptr=ctypes.c_void_p()
		ctypes.windll.oleacc.AccessibleObjectFromWindow(self.getWindowHandle(),-16,ctypes.byref(comtypes.automation.IUnknown._iid_),ctypes.byref(ptr))
		ptr=ctypes.cast(ptr,ctypes.POINTER(comtypes.automation.IUnknown))
		self.document=comtypes.client.wrap(ptr)
		self.lastFontName=self.lastFontSize=self.lastBold=self.lastItalic=self.lastUnderline=self.lastParagraphAlignment=None
		self.keyMap.update({
key("insert+f"):self.script_formatInfo,
})

	def _duplicateDocumentRange(self,range):
		return range.Duplicate

	def getCaretRange(self):
		start=self.document.Selection.Start
		end=self.document.Selection.End
		if start!=end:
			return (start,end)
		else:
			return None

	def getCaretPosition(self):
		return self.document.Selection.Start

	def getVisibleLineRange(self):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Expand(self.msftedit.tomWindow)
		return (self.getLineNumber(range.Start),self.getLineNumber(range.End))

	def getStartPosition(self):
		return 0

	def getEndPosition(self):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Expand(self.msftedit.tomStory)
		return range.End

	def getLineNumber(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=0
		range.Move(self.msftedit.tomCharacter,pos)
		return range.GetIndex(self.msftedit.tomLine)-1

	def getLineStart(self,lineNum):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=0
		range.Move(self.msftedit.tomLine,lineNum)
		return range.Start

	def getLine(self,lineNum):
		start=self.getLineStart(lineNum)
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=start
		range.Expand(self.msftedit.tomLine)
		text=range.Text
		if text!='\r':
			return text
		else:
			return None

	def getLineCount(self):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=0
		range.Expand(self.msftedit.tomStory)
		return self.getLineNumber(range.End)

	def nextWord(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		delta=range.Move(self.msftedit.tomWord,1)
		if delta:
			return range.Start
		else:
			return None

	def previousWord(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		delta=range.Move(self.msftedit.tomWord,-1)
		if delta:
			return range.Start
		else:
			return None

	def getTextRange(self,start,end):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=start
		range.End=end
		return range.Text

	def getFontName(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		return range.Font.Name

	def getCurrentFontName(self):
		return self.getFontName(self.getCaretPosition())

	def getFontSize(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		return "%d"%range.Font.Size

	def getCurrentFontSize(self):
		return self.getFontSize(self.getCaretPosition())

	def getParagraphAlignment(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		align=range.Para.Alignment
		if align==self.msftedit.tomAlignLeft:
			return "left"
		elif align==self.msftedit.tomAlignCenter:
			return "centered"
		elif align==self.msftedit.tomAlignRight:
			return "right"
		elif align>=self.msftedit.tomAlignJustify:
			return "justified"

	def getCurrentParagraphAlignment(self):
		return self.getParagraphAlignment(self.getCaretPosition())

	def isBold(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		return range.Font.Bold

	def isCurrentBold(self):
		return self.isBold(self.getCaretPosition())

	def isItalic(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		return range.Font.Italic

	def isCurrentItalic(self):
		return self.isItalic(self.getCaretPosition())

	def isUnderline(self,pos):
		range=self._duplicateDocumentRange(self.document.Selection)
		range.Start=range.End=pos
		return range.Font.Underline

	def isCurrentUnderline(self):
		return self.isUnderline(self.getCaretPosition())

	def reportChanges(self):
		if conf["documentFormat"]["reportFontChanges"]:
			fontName=self.getCurrentFontName()
			if fontName!=self.lastFontName:
				audio.speakMessage("%s font"%fontName)
				self.lastFontName=fontName
		if conf["documentFormat"]["reportFontSizeChanges"]:
			fontSize=self.getCurrentFontSize()
			if fontSize!=self.lastFontSize:
				audio.speakMessage("%s point"%fontSize)
				self.lastFontSize=fontSize
		if conf["documentFormat"]["reportFontAttributeChanges"]:
			bold=self.isCurrentBold()
			if bold!=self.lastBold:
				if bold:
					audio.speakMessage("bold")
				elif self.lastBold:
					audio.speakMessage("bold off")
				self.lastBold=bold
				self.lastFontSize=fontSize
			italic=self.isCurrentItalic()
			if italic!=self.lastItalic:
				if italic:
					audio.speakMessage("Italic")
				elif self.lastItalic:
					audio.speakMessage("italic off")
				self.lastItalic=italic
			underline=self.isCurrentUnderline()
			if underline!=self.lastUnderline:
				if underline:
					audio.speakMessage("underline")
				elif self.lastUnderline:
					audio.speakMessage("underline off")
				self.lastUnderline=underline
		if conf["documentFormat"]["reportAlignmentChanges"]:
			alignment=self.getCurrentParagraphAlignment()
			if alignment!=self.lastParagraphAlignment:
				audio.speakMessage("Aligned %s"%alignment)
				self.lastParagraphAlignment=alignment

	def script_moveByLine(self,keyPress):
		sendKey(keyPress)
		self.reportChanges()
		audio.speakText(self.getCurrentLine())

	def script_moveByCharacter(self,keyPress):
		sendKey(keyPress)
		self.reportChanges()
		audio.speakSymbol(self.getCurrentCharacter())

	def script_moveByWord(self,keyPress):
		sendKey(keyPress)
		self.reportChanges()
		audio.speakText(self.getCurrentWord())

	def script_delete(self,keyPress):
		sendKey(keyPress)
		self.reportChanges()
		audio.speakSymbol(self.getCurrentCharacter())

	def script_formatInfo(self,keyPress):
		audio.speakMessage("%s style"%self.getCurrentStyle())
		audio.speakMessage("%s font"%self.getCurrentFontName())
		audio.speakMessage("%d point"%self.getCurrentFontSize())
		if self.isCurrentBold():
			audio.speakMessage("bold")
		if self.isCurrentItalic():
			audio.speakMessage("Italic")
		if self.isCurrentUnderline():
			audio.speakMessage("underline")
		audio.speakMessage("align %s"%self.getCurrentParagraphAlignment())


staticMap={
("Shell_TrayWnd",None):NVDAObject_Shell_TrayWnd,
("tooltips_class32",None):NVDAObject_tooltip,
("Progman",None):NVDAObject_Progman,
("#32770",ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("TrayClockWClass",ROLE_SYSTEM_CLIENT):NVDAObject_TrayClockWClass,
("Edit",ROLE_SYSTEM_TEXT):NVDAObject_edit,
("RICHEDIT20W",ROLE_SYSTEM_TEXT):NVDAObject_ITextDocument,
("RICHEDIT50W",ROLE_SYSTEM_TEXT):NVDAObject_ITextDocument,
("Button",ROLE_SYSTEM_CHECKBUTTON):NVDAObject_checkBox,
("MozillaUIWindowClass",None):NVDAObject_mozillaUIWindowClass,
("MozillaUIWindowClass",ROLE_SYSTEM_APPLICATION):NVDAObject_mozillaUIWindowClass_application,
("MozillaContentWindowClass",None):NVDAObject_mozillaContentWindowClass,
("MozillaContentWindowClass",ROLE_SYSTEM_DOCUMENT):NVDAObject_mozillaContentWindowClass_document,
("MozillaContentWindowClass",ROLE_SYSTEM_LINK):NVDAObject_mozillaContentWindowClass_link,
("MozillaContentWindowClass",ROLE_SYSTEM_LISTITEM):NVDAObject_mozillaContentWindowClass_listItem,
("MozillaContentWindowClass",ROLE_SYSTEM_TEXT):NVDAObject_mozillaContentWindowClass_text,
("ConsoleWindowClass",ROLE_SYSTEM_CLIENT):NVDAObject_consoleWindowClass,
}

dynamicMap={}

