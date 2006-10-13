import ctypes
import comtypes.client
import comtypes.client.dynamic
import time
import difflib
import thread
import struct
import re
import debug
import winUser
import winKernel
import audio
from keyboardHandler import key, sendKey
from constants import *
from config import conf
import dictionaries
import api
import MSAAHandler

#Some api functions specific to NVDAObjects

def getNVDAObjectClass(windowClass,objectRole):
	if dynamicMap.has_key((windowClass,objectRole)):
		return dynamicMap[(windowClass,objectRole)]
	elif dynamicMap.has_key((windowClass,None)):
		return dynamicMap[(windowClass,None)]
	elif dynamicMap.has_key((None,objectRole)):
		return dynamicMap[(None,objectRole)]
	elif staticMap.has_key((windowClass,objectRole)):
		return staticMap[(windowClass,objectRole)]
	elif staticMap.has_key((windowClass,None)):
		return staticMap[(windowClass,None)]
	elif staticMap.has_key((None,objectRole)):
		return staticMap[(None,objectRole)]
	else:
		return NVDAObject

def getNVDAObjectByAccessibleObject(ia,child):
	try:
		return getNVDAObjectClass(winUser.getClassName(MSAAHandler.windowFromAccessibleObject(ia)),MSAAHandler.accRole(ia,child))(ia,child)
	except:
		debug.writeException("NVDAObjects.getNVDAObjectByAccessibleObject")
		return None

def getNVDAObjectByLocator(window,objectID,childID):
	res=MSAAHandler.accessibleObjectFromEvent(window,objectID,childID)
	if res:
		return getNVDAObjectByAccessibleObject(res[0],res[1])

def getNVDAObjectByPoint(x,y):
	res=MSAAHandler.accessibleObjectFromPoint(x,y)
	if res:
		return getNVDAObjectByAccessibleObject(res[0],res[1])

def registerNVDAObjectClass(windowClass,objectRole,cls):
	dynamicMap[(windowClass,objectRole)]=cls

def unregisterNVDAObjectClass(windowClass,objectRole):
	del dynamicMap[(windowClass,objectRole)]

def getRoleName(role):
	dictRole=dictionaries.roleNames.get(role,None)
	if dictRole:
		return dictRole
	elif isinstance(role,int):
		return MSAAHandler.getRoleText(role)
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
	dictState=dictionaries.stateNames.get(state,None)
	if dictState:
		newState=dictstate
	elif isinstance(state,int):
		newState=MSAAHandler.getStateText(state)
	else:
		newState=state
	if opposite:
		newState="not %s"%newState
	return newState


#The classes

class NVDAObject(object):

	def __init__(self,*args):
		if len(args)!=2:
			raise TypeError("args should be a 2-typle of IAccWrapper object and int")
		if not isinstance(args[0],MSAAHandler.IAccWrapper):
			raise TypeError("arg[0] must be an IAccWrapper object, not %s"%type(args[0]))
		self.ia=args[0]
		if not isinstance(args[1],int):
			raise TypeError("arg[1] must be an int, not %s"%type(args[1]))
		self.child=args[1]
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
		return MSAAHandler.windowFromAccessibleObject(self.ia)

	def getName(self):
		return MSAAHandler.accName(self.ia,self.child)

	def getValue(self):
		return MSAAHandler.accValue(self.ia,self.child)

	def getRole(self):
		return MSAAHandler.accRole(self.ia,self.child)

	def getTypeString(self):
		role=self.getRole()
		if conf["presentation"]["reportClassOfAllObjects"] or (conf["presentation"]["reportClassOfClientObjects"] and (role==ROLE_SYSTEM_CLIENT)):
			typeString=winUser.getClassName(self.getWindowHandle())
		else:
			typeString=""
		return typeString+" %s"%getRoleName(self.getRole())

	def getStates(self):
		return MSAAHandler.accState(self.ia,self.child)

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
			return self.ia.accDescription(self.child)
		except:
			return ""

	def getHelp(self):
		try:
			return self.ia.accHelp(self.child)
		except:
			return ""

	def getKeyboardShortcut(self):
		keyboardShortcut=None
		try:
			keyboardShortcut=self.ia.accKeyboardShortcut(self.child)
		except:
			return ""
		if not keyboardShortcut:
			return ""
		else:
			return keyboardShortcut

	def getChildID(self):
		try:
			return self.child
		except:
			return None

	def getChildCount(self):
		count=MSAAHandler.accChildCount(self.ia,self.child)
		return count

	def getProcessID(self):
		return winUser.getWindowThreadProcessID(self.getWindowHandle())
 

	def getLocation(self):
		return MSAAHandler.accLocation(self.ia,self.child)

	def getParent(self):
		res=MSAAHandler.accParent(self.ia,self.child)
		if res:
			(ia,child)=res
		else:
			return None
		obj=getNVDAObjectByAccessibleObject(ia,child)
		if obj and (obj.getRole()==ROLE_SYSTEM_WINDOW):
			return obj.getParent()
		else:
			return obj

	def getNext(self):
		res=MSAAHandler.accParent(self.ia,self.child)
		if res:
			parentObject=getNVDAObjectByAccessibleObject(res[0],res[1])
			parentRole=parentObject.getRole()
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=MSAAHandler.accNavigate(obj.ia,obj.child,NAVDIR_NEXT)
		if res:
			nextObject=getNVDAObjectByAccessibleObject(res[0],res[1])
			if nextObject and (nextObject.getRole()==ROLE_SYSTEM_WINDOW):
				nextObject=getNVDAObjectByLocator(nextObject.getWindowHandle(),-4,0)
			if nextObject!=self:
				return nextObject
			else:
				return None

	def getPrevious(self):
		res=MSAAHandler.accParent(self.ia,self.child)
		if res:
			parentObject=getNVDAObjectByAccessibleObject(res[0],res[1])
			parentRole=parentObject.getRole()
		else:
			parentObject=None
			parentRole=None
		if parentObject and (parentRole==ROLE_SYSTEM_WINDOW):
			obj=parentObject
		else:
			obj=self
		res=MSAAHandler.accNavigate(obj.ia,obj.child,NAVDIR_PREVIOUS)
		if res:
			previousObject=getNVDAObjectByAccessibleObject(res[0],res[1])
			if previousObject and (previousObject.getRole()==ROLE_SYSTEM_WINDOW):
				previousObject=getNVDAObjectByLocator(previousObject.getWindowHandle(),-4,0)
			if previousObject!=self:
				return previousObject
			else:
				return None

	def getFirstChild(self):
		res=MSAAHandler.accNavigate(self.ia,self.child,NAVDIR_FIRSTCHILD)
		if res:
			obj=getNVDAObjectByAccessibleObject(res[0],res[1])
		else:
			return None
		if obj and (obj.getRole()==ROLE_SYSTEM_WINDOW):
			return getNVDAObjectByLocator(obj.getWindowHandle(),OBJID_CLIENT,0)
		else:
			return obj


	def doDefaultAction(self):
		MSAAHandler.accDoDefaultAction(self.ia,self.child)

	def getChildren(self):
		children=[]
		obj=self.getFirstChild()
		while obj:
			children.append(obj)
			obj=obj.getNext()
		return children

	def getActiveChild(self):
		res=MSAAHandler.accFocus()
		if res:
			return getNVDAObjectByAccessibleObject(res[0],res[1])

	def hasFocus(self):
		states=0
		states=self.getStates()
		if (states&STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		self.ia.SetFocus()

	def event_foreground(self):
		audio.cancel()
		self.speakObject()

	def oupdateVirtualBuffer(self):
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

	def __init__(self,*args):
		NVDAObject.__init__(self,*args)
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
		word=winUser.sendMessage(self.getWindowHandle(),EM_GETSEL,0,0)
		if word<0:
			return None
		start=winUser.LOWORD(word)
		end=winUser.HIWORD(word)
		return (start,end)

	def getCaretPosition(self):
		word=winUser.sendMessage(self.getWindowHandle(),EM_GETSEL,0,0)
		if word<0:
			return None
		pos=winUser.LOWORD(word)
		return pos

	def getStartPosition(self):
		return 0

	def getEndPosition(self):
		return self.getTextLength()

	def getLineCount(self):
		lineCount=winUser.sendMessage(self.getWindowHandle(),EM_GETLINECOUNT,0,0)
		if lineCount<0:
			return None
		return lineCount

	def getLineNumber(self,pos):
		return winUser.sendMessage(self.getWindowHandle(),EM_LINEFROMCHAR,pos,0)

	def getLineStart(self,lineNum):
		return winUser.sendMessage(self.getWindowHandle(),EM_LINEINDEX,lineNum,0)

	def getLineLength(self,lineNum):
		lineStart=self.getLineStart(lineNum)
		lineLength=winUser.sendMessage(self.getWindowHandle(),EM_LINELENGTH,lineStart,0)
		if lineLength<0:
			return None
		return lineLength

	def getLine(self,lineNum):
		lineLength=self.getLineLength(lineNum)
		if not lineLength:
			return None
		buf=ctypes.create_unicode_buffer(lineLength+1)
		buf.value=struct.pack('i',lineLength+1)
		res=winUser.sendMessage(self.getWindowHandle(),EM_GETLINE,lineNum,buf)
		return buf.value

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
		return winUser.sendMessage(self.getWindowHandle(),WM_GETTEXTLENGTH,0,0)

	def getText(self):
		textLength=self.getTextLength()
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		winUser.sendMessage(self.getWindowHandle(),WM_GETTEXT,textLength+1,textBuf)
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
		states-=states&STATE_SYSTEM_PRESSED
		return states

class NVDAObject_outlineItem(NVDAObject):

	def getValue(self):
		return "level %s"%NVDAObject.getValue(self)

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
			children=self.ia.accChildren()
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

	def __init__(self,*args):
		NVDAObject_edit.__init__(self,*args)
		processID=self.getProcessID()[0]
		try:
			winKernel.freeConsole()
		except:
			debug.writeException("freeConsole")
			pass
		winKernel.attachConsole(processID)
		self.consoleHandle=winKernel.getStdHandle(STD_OUTPUT_HANDLE)
		self.oldLines=self.getVisibleLines()
		self.cConsoleEventHook=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(self.consoleEventHook)
		self.consoleEventHookHandles=[]

	def __del__(self):
		for handle in self.consoleEventHookHandles:
			winUser.unhookWinEventHook(handle)
		NVDAObject_edit.__del__(self)

	def consoleEventHook(self,handle,eventID,window,objectID,childID,threadID,timestamp):
		if self.hasFocus():
			api.setVirtualBufferCursor(api.getVirtualBuffer().getCaretPosition())
			newLines=self.getVisibleLines()
			if newLines!=self.oldLines:
				if eventID in [EVENT_CONSOLE_UPDATE_REGION,EVENT_CONSOLE_UPDATE_SCROLL]:
					self.speakNewText(newLines,self.oldLines)
				self.oldLines=newLines

	def getConsoleVerticalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return info.consoleSize.y

	def getConsoleHorizontalLength(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		return info.consoleSize.x

	def getVisibleLineRange(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		topLineNum=info.windowRect.top
		bottomLineNum=info.windowRect.bottom
		#audio.speakMessage("top %s, bottom %s"%(topLineNum,bottomLineNum))
		return (topLineNum,bottomLineNum)

	def getCaretPosition(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		y=info.cursorPosition.y
		x=info.cursorPosition.x
		return self.getLineStart(y)+x

	def getEndPosition(self):
		return self.getConsoleVerticalLength()*self.getConsoleHorizontalLength()

	def getLineStart(self,lineNum):
		return lineNum*self.getConsoleHorizontalLength()

	def getLineNumber(self,pos):
		return pos/self.getConsoleHorizontalLength()

	def getLine(self,lineNum):
		maxLen=self.getConsoleHorizontalLength()
		line=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,0,lineNum)
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
		text=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,0,0)
		return text

	def getVisibleLines(self):
		visibleRange=self.getVisibleLineRange()
		lines=[]
		for lineNum in range(visibleRange[0],visibleRange[1]+1):
			line=self.getLine(lineNum)
			if line:
				lines.append(line)
		return lines

	def getValue(self):
		return ""

	def event_focusObject(self):
		if self.doneFocus:
			return
		self.doneFocus=True
		audio.speakObjectProperties(typeString="console")
		for line in self.getVisibleLines():
			audio.speakText(line)
		for eventID in [EVENT_CONSOLE_UPDATE_REGION,EVENT_CONSOLE_UPDATE_SIMPLE,EVENT_CONSOLE_UPDATE_SCROLL]:
			handle=winUser.setWinEventHook(eventID,eventID,0,self.cConsoleEventHook,0,0,0)
			if handle:
				self.consoleEventHookHandles.append(handle)

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

	class constants:
		#Units
		tomCharacter=1
		tomWord=2
		tomParagraph=4
		tomLine=5
		tomStory=6
		tomWindow=11
		#Paragraph alignment
		tomAlignLeft=0
		tomAlignCenter=1
		tomAlignRight=2
		tomAlignJustify=3

	def __init__(self,*args):
		NVDAObject_edit.__init__(self,*args)
		self.dom=self.getDocumentObjectModel()
		self.lastFontName=self.lastFontSize=self.lastBold=self.lastItalic=self.lastUnderline=self.lastParagraphAlignment=None
		self.keyMap.update({
key("insert+f"):self.script_formatInfo,
})

	def __del__(self):
		self.destroyObjectModel(self.dom)
		NVDAObject_edit.__del__(self)

	def getDocumentObjectModel(self):
		ptr=ctypes.POINTER(comtypes.automation.IDispatch)()
		res=ctypes.windll.oleacc.AccessibleObjectFromWindow(self.getWindowHandle(),OBJID_NATIVEOM,ctypes.byref(comtypes.automation.IDispatch._iid_),ctypes.byref(ptr))
		if res==0:
			return comtypes.client.dynamic.Dispatch(ptr)
		else:
			raise OSError("No IDispatch interface")

	def destroyObjectModel(self,om):
		pass



	def _duplicateDocumentRange(self,rangeObj):
		return rangeObj.Duplicate

	def getCaretRange(self):
		start=self.dom.Selection.Start
		end=self.dom.Selection.End
		if start!=end:
			return (start,end)
		else:
			return None

	def getCaretPosition(self):
		return self.dom.Selection.Start

	def getVisibleLineRange(self):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Expand(self.constants.tomWindow)
		return (self.getLineNumber(rangeObj.Start),self.getLineNumber(rangeObj.End))

	def getStartPosition(self):
		return 0

	def getEndPosition(self):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Expand(self.constants.tomStory)
		return rangeObj.End

	def getLineNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=0
		rangeObj.Move(self.constants.tomCharacter,pos)
		return rangeObj.GetIndex(self.constants.tomLine)-1

	def getLineStart(self,lineNum):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=0
		rangeObj.Move(self.constants.tomLine,lineNum)
		return rangeObj.Start

	def getLine(self,lineNum):
		start=self.getLineStart(lineNum)
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=start
		rangeObj.Expand(self.constants.tomLine)
		text=rangeObj.Text
		if text!='\r':
			return text
		else:
			return None

	def getLineCount(self):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=0
		rangeObj.Expand(self.constants.tomStory)
		return self.getLineNumber(rangeObj.End)

	def nextWord(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		delta=rangeObj.Move(self.constants.tomWord,1)
		if delta:
			return rangeObj.Start
		else:
			return None

	def previousWord(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		delta=rangeObj.Move(self.constants.tomWord,-1)
		if delta:
			return rangeObj.Start
		else:
			return None

	def getParagraph(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(self.constants.tomParagraph)
		return self.getTextRange(rangeObj.Start,rangeObj.End)

	def getCurrentParagraph(self):
		return self.getParagraph(self.getCaretPosition())

	def getTextRange(self,start,end):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=start
		rangeObj.End=end
		return rangeObj.Text

	def getFontName(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Name

	def getCurrentFontName(self):
		return self.getFontName(self.getCaretPosition())

	def getFontSize(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return int(rangeObj.Font.Size)

	def getCurrentFontSize(self):
		return self.getFontSize(self.getCaretPosition())

	def getParagraphAlignment(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		align=rangeObj.Para.Alignment
		if align==self.constants.tomAlignLeft:
			return "left"
		elif align==self.constants.tomAlignCenter:
			return "centered"
		elif align==self.constants.tomAlignRight:
			return "right"
		elif align>=self.constants.tomAlignJustify:
			return "justified"

	def getCurrentParagraphAlignment(self):
		return self.getParagraphAlignment(self.getCaretPosition())

	def isBold(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Bold

	def isCurrentBold(self):
		return self.isBold(self.getCaretPosition())

	def isItalic(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Italic

	def isCurrentItalic(self):
		return self.isItalic(self.getCaretPosition())

	def isUnderline(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Underline

	def isCurrentUnderline(self):
		return self.isUnderline(self.getCaretPosition())

	def reportChanges(self):
		if conf["documentFormatting"]["reportFontChanges"]:
			fontName=self.getCurrentFontName()
			if fontName!=self.lastFontName:
				audio.speakMessage("%s font"%fontName)
				self.lastFontName=fontName
		if conf["documentFormatting"]["reportFontSizeChanges"]:
			fontSize=self.getCurrentFontSize()
			if fontSize!=self.lastFontSize:
				audio.speakMessage("%s point"%fontSize)
				self.lastFontSize=fontSize
		if conf["documentFormatting"]["reportFontAttributeChanges"]:
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
		if conf["documentFormatting"]["reportAlignmentChanges"]:
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
("Shell_TrayWnd",ROLE_SYSTEM_CLIENT):NVDAObject_Shell_TrayWnd,
("tooltips_class32",None):NVDAObject_tooltip,
("Progman",ROLE_SYSTEM_CLIENT):NVDAObject_Progman,
("#32770",ROLE_SYSTEM_DIALOG):NVDAObject_dialog,
("TrayClockWClass",ROLE_SYSTEM_CLIENT):NVDAObject_TrayClockWClass,
("Edit",ROLE_SYSTEM_TEXT):NVDAObject_edit,
("RichEdit20W",ROLE_SYSTEM_TEXT):NVDAObject_ITextDocument,
("RICHEDIT50W",ROLE_SYSTEM_TEXT):NVDAObject_ITextDocument,
(None,ROLE_SYSTEM_CHECKBUTTON):NVDAObject_checkBox,
(None,ROLE_SYSTEM_OUTLINEITEM):NVDAObject_outlineItem,
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

