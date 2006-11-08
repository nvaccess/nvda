import winsound
import ctypes
import comtypes.automation
import comtypesClient
import time
import difflib
import struct
import re
import debug
import NVDAThreads
import winUser
import winKernel
import audio
from keyboardHandler import key, sendKey
from constants import *
from config import conf
import dictionaries
import api
import MSAAHandler
import virtualBuffer
import globalVars

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
	return getNVDAObjectClass(winUser.getClassName(MSAAHandler.windowFromAccessibleObject(ia)),MSAAHandler.accRole(ia,child))(ia,child)

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

	def event_show(self):
		if self.getRole()==ROLE_SYSTEM_MENUPOPUP:
			self.event_menuStart()

	def updateMenuMode(self):
		if self.getRole() not in [ROLE_SYSTEM_MENUBAR,ROLE_SYSTEM_MENUPOPUP,ROLE_SYSTEM_MENUITEM]:
			api.setMenuMode(False)
		if self.getRole()==ROLE_SYSTEM_MENUITEM:
			audio.cancel()

	def event_gainFocus(self):
		self.updateMenuMode()
		if self.hasFocus() and not (not api.getMenuMode() and (self.getRole()==ROLE_SYSTEM_MENUITEM)):
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

	def event_valueChange(self):
		if self.hasFocus():
			audio.speakObjectProperties(value=self.getValue())

	def event_nameChange(self):
		if self.hasFocus():
			audio.speakObjectProperties(name=self.getName())

	def event_stateChange(self):
		states=self.getStates()
		if states is None or not self.hasFocus():
			return None
		states_on=states-(states&self.lastStates)
		audio.speakObjectProperties(stateText=getStateNames(self.filterStates(states_on)))
		states_off=self.lastStates-(states&self.lastStates)
		audio.speakObjectProperties(stateText=getStateNames(self.filterStates(states_off),opposite=True))
		self.lastStates=states

	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

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

	def event_gainFocus(self):
		pass

class NVDAObject_Progman(NVDAObject):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows desktop.
	"""

	def event_foreground(self):
		pass

	def event_gainFocus(self):
		pass

class NVDAObject_edit(NVDAObject):
	"""
	Based on NVDAObject, but speaks moving and editing with in the edit control.
	"""

	def __init__(self,*args):
		NVDAObject.__init__(self,*args)
		self.reviewCursor=0
		self.presentationTable=[]
		self.keyMap={
			key("insert+extendedDown"):self.script_sayAll,
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
			key("end"):self.script_review_previousCharacter,
			key("shift+end"):self.script_review_startOfLine,
			key("down"):self.script_review_currentCharacter,
			key("next"):self.script_review_nextCharacter,
			key("shift+next"):self.script_review_endOfLine,
			key("left"):self.script_review_previousWord,
			key("clear"):self.script_review_currentWord,
			key("right"):self.script_review_nextWord,
			key("home"):self.script_review_previousLine,
			key("shift+home"):self.script_review_top,
			key("up"):self.script_review_currentLine,
			key("prior"):self.script_review_nextLine,
			key("shift+prior"):self.script_review_bottom,
			key("insert+f"):self.script_formatInfo,
		}

	def getValue(self):
		return self.getCurrentLine()

	def getVisibleRange(self):
		return (self.getStartPosition(),self.getEndPosition())

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

	def setCaretPosition(self,pos):
		winUser.sendMessage(self.getWindowHandle(),EM_SETSEL,pos,pos)

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

	def getLineStart(self,pos):
		lineNum=self.getLineNumber(pos)
		return winUser.sendMessage(self.getWindowHandle(),EM_LINEINDEX,lineNum,0)

	def getLineLength(self,pos):
		lineLength=winUser.sendMessage(self.getWindowHandle(),EM_LINELENGTH,pos,0)
		if lineLength<0:
			return None
		return lineLength

	def getLine(self,pos):
		lineNum=self.getLineNumber(pos)
		lineLength=self.getLineLength(pos)
		if not lineLength:
			return None
		buf=ctypes.create_unicode_buffer(lineLength+10)
		buf.value=struct.pack('i',lineLength)
		res=winUser.sendMessage(self.getWindowHandle(),EM_GETLINE,lineNum,buf)
		return buf.value

	def getCurrentLine(self):
		return self.getLine(self.getCaretPosition())

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

	def inWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.getCharacter(pos) not in whitespace:
			return True
		else:
			return False

	def wordStart(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			while (pos is not None) and (self.getCharacter(pos) not in whitespace):
				oldPos=pos
				pos=self.previousCharacter(pos)
			if pos is None:
				pos=oldPos
			else:
				pos=self.nextCharacter(pos)
		return pos

	def wordEnd(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		while (pos is not None) and (self.getCharacter(pos) not in whitespace):
			oldPos=pos
			pos=self.nextCharacter(pos)
		if pos is not None:
			return pos
		else:
			return oldPos

	def nextWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			pos=self.wordEnd(pos)
		while (pos is not None) and (self.getCharacter(pos) in whitespace):
			pos=self.nextCharacter(pos)
		return pos

	def previousWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		if self.inWord(pos):
			pos=self.wordStart(pos)
			pos=self.previousCharacter(pos)
		while (pos is not None) and (self.getCharacter(pos) in whitespace):
			pos=self.previousCharacter(pos)
		if pos:
			pos=self.wordStart(pos)
		return pos

	def nextLine(self,pos):
		lineLength=self.getLineLength(pos)
		lineStart=self.getLineStart(pos)
		lineEnd=lineStart+lineLength
		newPos=lineEnd+1
		if newPos<self.getEndPosition():
			return newPos
		else:
			return None

	def previousLine(self,pos):
		lineStart=self.getLineStart(pos)
		pos=lineStart-1
		lineStart=self.getLineStart(pos)
		if lineStart>=self.getStartPosition():
			return lineStart
		else:
			return None

	def getTextLength(self):
		return winUser.sendMessage(self.getWindowHandle(),WM_GETTEXTLENGTH,0,0)

	def getText(self):
		textLength=self.getTextLength()
		textBuf=ctypes.create_unicode_buffer(textLength+2)
		winUser.sendMessage(self.getWindowHandle(),WM_GETTEXT,textLength+1,textBuf)
		return textBuf.value+u"\0"

	def getTextRange(self,start,end):
		text=self.getText()
		if (start>=end) or (end>len(text)):
			return None
		return text[start:end]

	def getCharacter(self,pos):
		if pos is not None:
			return self.getTextRange(pos,pos+1)

	def getCurrentCharacter(self):
		return self.getCharacter(self.getCaretPosition())

	def getWord(self,pos):
		wordStart=self.wordStart(pos)
		wordEnd=self.wordEnd(pos)
		return self.getTextRange(wordStart,wordEnd)

	def getCurrentWord(self):
		return self.getWord(self.getCaretPosition())

	def sayAllGenerator(self):
		#Setup the initial info (count, caret position, index etc)
		count=0 #Used to see when we need to start yielding
		startPos=endPos=curPos=self.getCaretPosition()
		index=lastIndex=None
		lastKeyCount=globalVars.keyCounter
		#A loop that runs while no key is pressed and while we are not at the end of the text
		while (curPos is not None) and (curPos<self.getEndPosition()):
			#Speak the current line (if its not blank) with an speech index of its position
			text=self.getLine(curPos)
			if text and (text not in ['\n','\r',""]):
				audio.speakText(text,index=curPos)
			#Move our current position down by one line
				endPos=curPos
			curPos=self.nextLine(curPos)
			#Grab the current speech index from the synth, and if different to last, move the caret there
			index=audio.getLastIndex()
			if (index!=lastIndex) and (index>=startPos) and (index<=endPos):
		 		self.setCaretPosition(index)
			lastIndex=index
			#We don't want to yield for the first 4 loops so the synth can get a good run up
			if count>4:
				yield None
			count+=1
			#If the current keyPress count has changed, we need to stop
			if lastKeyCount!=globalVars.keyCounter:
				break
		else: #We fell off the end of the loop (keyPress count didn't change)
			#We are at the end of the document, but the speech most likely isn't yet, so loop so it can catch up
			while (index<endPos):
				index=audio.getLastIndex()
				if (index!=lastIndex) and (index>=startPos) and (index<=endPos):
			 		self.setCaretPosition(index)
				lastIndex=index
				if count>4:
					yield None
				count+=1
				if lastKeyCount!=globalVars.keyCounter:
					break
		#If we did see a keyPress, then we still have to give the speech index a chance to catch up to our current location
		if lastKeyCount!=globalVars.keyCounter:
			for num in range(2):
				yield None
				index=audio.getLastIndex()
				if (index!=lastIndex) and (index>=startPos) and (index<=endPos):
			 		self.setCaretPosition(index)
			audio.cancel()


	def event_caret(self):
		self.reviewCursor=self.getCaretPosition()

	def event_gainFocus(self):
		self.speakObject()
		self.reportPresentation()
		self.reviewCursor=self.getCaretPosition()

	def event_valueChange(self):
		pass

	def reportPresentation(self):
		#The old values are at index 2
		pos=self.getCaretPosition()
		for ruleNum in range(len(self.presentationTable)):
			messageFunc=self.presentationTable[ruleNum][0]
			reportWhen=conf
			for item in self.presentationTable[ruleNum][1]:
				reportWhen=reportWhen.get(item,{})
			if reportWhen=="always":
				message=messageFunc(pos)
				if message is not None:
					audio.speakMessage(messageFunc(pos))
			elif reportWhen=="changes":
				message=messageFunc(pos)
				if (message is not None) and (message!=self.presentationTable[ruleNum][2]):
					audio.speakMessage(message)
				self.presentationTable[ruleNum][2]=message

	def reportReviewPresentation(self):
		#The old values are at index 3
		pos=self.reviewCursor
		for ruleNum in range(len(self.presentationTable)):
			messageFunc=self.presentationTable[ruleNum][0]
			reportWhen=conf
			for item in self.presentationTable[ruleNum][1]:
				reportWhen=reportWhen.get(item,{})
			if reportWhen=="always":
				message=messageFunc(pos)
				if message is not None:
					audio.speakMessage(messageFunc(pos))
			elif reportWhen=="changes":
				message=messageFunc(pos)
				if (message is not None) and (message!=self.presentationTable[ruleNum][3]):
					audio.speakMessage(message)
				self.presentationTable[ruleNum][3]=message

	def script_sayAll(self,keyPress):
		NVDAThreads.newThread(self.sayAllGenerator())


	def script_moveByLine(self,keyPress):
		"""Moves and then reads the current line"""
		debug.writeMessage("script_moveByCharacter: started")
		sendKey(keyPress)
		debug.writeMessage("script_moveByCharacter: done sendKey")
		self.reportPresentation()
		debug.writeMessage("script_moveByCharacter: done reportPresentation")
		audio.speakText(self.getCurrentLine())
		debug.writeMessage("script_moveByCharacter: done speakText")

	def script_moveByCharacter(self,keyPress):
		"""Moves and reads the current character"""
		sendKey(keyPress)
		self.reportPresentation()
		audio.speakSymbol(self.getCurrentCharacter())
		self.reviewCursor=self.getCaretPosition()

	def script_moveByWord(self,keyPress):
		"""Moves and reads the current word"""
		sendKey(keyPress)
		self.reportPresentation()
		audio.speakText(self.getCurrentWord())
		self.reviewCursor=self.getCaretPosition()

	def script_changeSelection(self,keyPress):
		"""Moves and reads the current selection"""
		selectionPoints=self.getCaretRange()
		sendKey(keyPress)
		newSelectionPoints=self.getCaretRange()
		if newSelectionPoints and not selectionPoints:
			audio.speakText("selected %s"%self.getTextRange(newSelectionPoints[0],newSelectionPoints[1]))
		elif not newSelectionPoints:
			audio.speakSymbol(self.getCharacter(self.getCaretPosition()))
		elif selectionPoints and newSelectionPoints: 
			if newSelectionPoints[1]>selectionPoints[1]:
				audio.speakText("selected %s"%self.getTextRange(selectionPoints[1],newSelectionPoints[1]))
			elif newSelectionPoints[0]>selectionPoints[0]:
				audio.speakText("unselected %s"%self.getTextRange(selectionPoints[0],newSelectionPoints[0]))
			elif newSelectionPoints[1]<selectionPoints[1]:
				audio.speakText("unselected %s"%self.getTextRange(newSelectionPoints[1],selectionPoints[1]))
			elif newSelectionPoints[0]<selectionPoints[0]:
				audio.speakText("selected %s"%self.getTextRange(newSelectionPoints[0],selectionPoints[0]))
		self.reviewCursor=self.getCaretPosition()

	def script_delete(self,keyPress):
		"""Deletes the character and reads the new current character"""
		sendKey(keyPress)
		self.reportPresentation()
		audio.speakSymbol(self.getCurrentCharacter())
		self.reviewCursor=self.getCaretPosition()

	def script_backspace(self,keyPress):
		"""Reads the character before the current character and then deletes it"""
		point=self.getCaretPosition()
		if not point==self.getStartPosition():
			delChar=self.getCharacter(self.previousCharacter(point))
			sendKey(keyPress)
			newPoint=self.getCaretPosition()
			if newPoint<point:
				audio.speakSymbol(delChar)
		else:
			sendKey(keyPress)
		self.reviewCursor=self.getCaretPosition()

	def script_formatInfo(self,keyPress):
		"""Reports the current formatting information"""
		pos=self.getCaretPosition()
		for rule in self.presentationTable:
			message=rule[0](pos)
			if message is not None:
				audio.speakMessage(message)

	def script_review_top(self,keyPress):
		"""Move the review cursor to the top and read the line"""
		self.reviewCursor=self.getVisibleRange()[0]
		self.reportReviewPresentation()
		line=self.getLine(self.reviewCursor)
		audio.speakText(line)

	def script_review_bottom(self,keyPress):
		"""Move the review cursor to the bottom and read the line"""
		self.reviewCursor=self.getVisibleRange()[1]-1
		self.reportReviewPresentation()
		line=self.getLine(self.reviewCursor)
		audio.speakText(line)

	def script_review_currentLine(self,keyPress):
		"""Reads the line at the review cursor position""" 
		self.reportReviewPresentation()
		line=self.getLine(self.reviewCursor)
		audio.speakText(line)

	def script_review_nextLine(self,keyPress):
		"""Moves the review cursor to the next line and reads it"""
		pos=self.reviewCursor
		nextPos=self.nextLine(pos)
		if (pos<self.getVisibleRange()[1]) and (nextPos is not None):
			self.reviewCursor=nextPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage("bottom")
		audio.speakText(self.getLine(self.reviewCursor))

	def script_review_previousLine(self,keyPress):
		"""Moves the review cursor to the previous line and reads it"""
		pos=self.reviewCursor
		prevPos=self.previousLine(pos)
		if (pos>self.getVisibleRange()[0]) and (prevPos is not None):
			self.reviewCursor=prevPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage("top")
		audio.speakText(self.getLine(self.reviewCursor))

	def script_review_startOfLine(self,keyPress):
		"""Move review cursor to start of line and read the current character"""
		self.reviewCursor=self.getLineStart(self.reviewCursor)
		self.reportReviewPresentation()
		character=self.getCharacter(self.reviewCursor)
		audio.speakText(character)

	def script_review_endOfLine(self,keyPress):
		"""Move review cursor to start of line and read the current character"""
		self.reviewCursor=self.getLineStart(self.reviewCursor)+self.getLineLength(self.reviewCursor)-1
		self.reportReviewPresentation()
		character=self.getCharacter(self.reviewCursor)
		audio.speakText(character)

	def script_review_currentWord(self,keyPress):
		"""Reads the word at the review cursor position"""
		self.reportReviewPresentation()
		word=self.getWord(self.reviewCursor)
		audio.speakText(word)

	def script_review_nextWord(self,keyPress):
		"""Moves the review cursor to the next word and reads it"""
		pos=self.reviewCursor
		nextPos=self.nextWord(pos)
		if (pos<self.getVisibleRange()[1]) and (nextPos is not None):
			self.reviewCursor=nextPos
			self.reportReviewPresentation()
			if self.getLineNumber(nextPos)!=self.getLineNumber(pos):
				winsound.Beep(440,20)
		else:
			audio.speakMessage("bottom")
		audio.speakText(self.getWord(self.reviewCursor))

	def script_review_previousWord(self,keyPress):
		"""Moves the review cursor to the previous word and reads it"""
		pos=self.reviewCursor
		prevPos=self.previousWord(pos)
		if (prevPos is not None) and (prevPos>=self.getVisibleRange()[0]):
			self.reviewCursor=prevPos
			self.reportReviewPresentation()
			if self.getLineNumber(prevPos)!=self.getLineNumber(pos):
				winsound.Beep(440,20)
		else:
			audio.speakMessage("top")
		audio.speakText(self.getWord(self.reviewCursor))

	def script_review_currentCharacter(self,keyPress):
		"""Reads the character at the review cursor position"""
		self.reportReviewPresentation()
		character=self.getCharacter(self.reviewCursor)
		audio.speakText(character)

	def script_review_nextCharacter(self,keyPress):
		"""Moves the review cursor to the next character and reads it"""
		pos=self.reviewCursor
		nextPos=self.nextCharacter(pos)
		lineStart=self.getLineStart(pos)
		lineEnd=lineStart+self.getLineLength(pos)
		if (nextPos<=lineEnd) and (nextPos is not None): 
			self.reviewCursor=nextPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage("right")
		audio.speakText(self.getCharacter(self.reviewCursor))

	def script_review_previousCharacter(self,keyPress):
		"""Moves the review cursor to the previous character and reads it"""
		pos=self.reviewCursor
		prevPos=self.previousCharacter(pos)
		lineStart=self.getLineStart(pos)
		if (prevPos>=lineStart) and (prevPos is not None):
			self.reviewCursor=prevPos
			self.reportReviewPresentation()
		else:
			audio.speakMessage("left")
		audio.speakText(self.getCharacter(self.reviewCursor))

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

	def event_gainFocus(self):
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

	def event_gainFocus(self):
		pass

class NVDAObject_mozillaContentWindowClass(NVDAObject):
	pass

class NVDAObject_mozillaContentWindowClass_document(NVDAObject_mozillaContentWindowClass):

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

class NVDAObject_consoleWindowClass(NVDAObject):

	def event_nameChange(self):
		pass

class NVDAObject_consoleWindowClassClient(NVDAObject_edit):

	def __init__(self,*args):
		NVDAObject_edit.__init__(self,*args)
		processID=self.getProcessID()[0]
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
		self.oldLines=self.getVisibleLines()

	def __del__(self):
		try:
			winKernel.freeConsole()
		except:
			debug.writeException("freeConsole")
		NVDAObject_edit.__del__(self)

	def consoleEventHook(self,handle,eventID,window,objectID,childID,threadID,timestamp):
		self.reviewCursor=self.getCaretPosition()
		newLines=self.getVisibleLines()
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

	def getVisibleRange(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		top=self.getPositionFromCoord(0,info.windowRect.top)
		bottom=self.getPositionFromCoord(0,info.windowRect.bottom+1)
		return (top,bottom)

	def getCaretPosition(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		y=info.cursorPosition.y
		x=info.cursorPosition.x
		return self.getPositionFromCoord(x,y)

	def getEndPosition(self):
		return self.getConsoleVerticalLength()*self.getConsoleHorizontalLength()

	def getPositionFromCoord(self,x,y):
		return (y*self.getConsoleHorizontalLength())+x

	def getLineStart(self,pos):
		return pos-(pos%self.getConsoleHorizontalLength())

	def getLineNumber(self,pos):
		return pos/self.getConsoleHorizontalLength()

	def getLine(self,pos):
		maxLen=self.getConsoleHorizontalLength()
		lineNum=self.getLineNumber(pos)
		line=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,0,lineNum)
		if line.isspace():
			line=None
		else:
			line=line.rstrip()
		return line

	def getLineCount(self):
		return self.getConsoleVerticalLength()

	def getLineLength(self,pos):
		return self.getConsoleHorizontalLength()

	def getText(self):
		maxLen=self.getEndPosition()
		text=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,0,0)
		return text

	def getVisibleLines(self):
		visibleRange=self.getVisibleRange()
		visibleRange=(self.getLineNumber(visibleRange[0]),self.getLineNumber(visibleRange[1]))
		lines=[]
		for lineNum in range(visibleRange[0],visibleRange[1]+1):
			line=self.getLine(self.getPositionFromCoord(0,lineNum))
			if line:
				lines.append(line)
		return lines

	def getValue(self):
		return ""

	def event_gainFocus(self):
		time.sleep(0.1)
		self.cConsoleEventHook=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(self.consoleEventHook)
		for eventID in [EVENT_CONSOLE_CARET,EVENT_CONSOLE_UPDATE_REGION,EVENT_CONSOLE_UPDATE_SIMPLE,EVENT_CONSOLE_UPDATE_SCROLL]:
			handle=winUser.setWinEventHook(eventID,eventID,0,self.cConsoleEventHook,0,0,0)
			if handle:
				debug.writeMessage("NVDAObject_consoleWindowClassClient: registered event: %s, handle %s"%(eventID,handle))
				self.consoleEventHookHandles.append(handle)
			else:
				raise OSError('Could not register console event %s'%eventID)
		audio.speakObjectProperties(typeString="console")
		for line in self.getVisibleLines():
			audio.speakText(line)

	def event_looseFocus(self):
		for handle in self.consoleEventHookHandles:
			winUser.unhookWinEvent(handle)

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
		self.presentationTable+=[
			[self.msgFontName,["documentFormatting","reportFontName"],None,None],
			[self.msgFontSize,["documentFormatting","reportFontSize"],None,None],
			[self.msgBold,["documentFormatting","reportFontAttributes"],None,None],
			[self.msgItalic,["documentFormatting","reportFontAttributes"],None,None],
			[self.msgUnderline,["documentFormatting","reportFontAttributes"],None,None],
			[self.msgParagraphAlignment,["documentFormatting","reportAlignment"],None,None],
		]

	def __del__(self):
		self.destroyObjectModel(self.dom)
		NVDAObject_edit.__del__(self)

	def getDocumentObjectModel(self):
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		res=ctypes.windll.oleacc.AccessibleObjectFromWindow(self.getWindowHandle(),OBJID_NATIVEOM,ctypes.byref(domPointer._iid_),ctypes.byref(domPointer))
		if res==0:
			return comtypesClient.wrap(domPointer)
		else:
			raise OSError("No ITextDocument interface")

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

	def setCaretPosition(self,pos):
		self.dom.Selection.Start=pos
		self.dom.Selection.End=pos

	def getVisibleRange(self):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Expand(self.constants.tomWindow)
		return (rangeObj.Start,rangeObj.End)

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

	def getLineStart(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(self.constants.tomLine)
		return rangeObj.Start

	def getLine(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
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

	def getWord(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(self.constants.tomWord)
		return self.getTextRange(rangeObj.Start,rangeObj.End)


	def getFontName(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Name

	def msgFontName(self,pos):
		return "font %s"%self.getFontName(pos)

	def getFontSize(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return int(rangeObj.Font.Size)

	def msgFontSize(self,pos):
		return "%s point"%self.getFontSize(pos)

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

	def msgParagraphAlignment(self,pos):
		return "alignment %s"%self.getParagraphAlignment(pos)

	def isBold(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Bold

	def msgBold(self,pos):
		if self.isBold(pos):
			bold="on"
		else:
			bold="off"
		return "bold %s"%bold

	def isItalic(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Italic

	def msgItalic(self,pos):
		if self.isItalic(pos):
			italic="on"
		else:
			italic="off"
		return "italic %s"%italic

	def isUnderline(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Underline

	def msgUnderline(self,pos):
		if self.isUnderline(pos):
			underline="on"
		else:
			underline="off"
		return "underline %s"%underline

class NVDAObject_virtualBuffer(NVDAObject_edit):

	def __init__(self,*args):
		NVDAObject_edit.__init__(self,*args)
		self.keyMap.update({
			key("insert+space"):self.script_toggleFocusInteractionMode,
			key("ExtendedRight"):self.script_rightArrow,
			key("ExtendedLeft"):self.script_leftArrow,
			key("ExtendedUp"):self.script_upArrow,
			key("ExtendedDown"):self.script_downArrow,
			key("extendedHome"):self.script_home,
			key("extendedEnd"):self.script_end,
			key("Control+ExtendedRight"):self.script_controlRightArrow,
			key("Control+ExtendedLeft"):self.script_controlLeftArrow,
			key("control+extendedHome"):self.script_controlHome,
			key("control+extendedEnd"):self.script_controlEnd,
			key("Return"):self.script_enter,
			key("Space"):self.script_space,
		})
		self.focusInteractionMode=False

	def getValue(self):
		return NVDAObject.getValue(self)

	def getCaretPosition(self):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getCaretPosition()

	def setCaretPosition(self,pos):
		virtualBuffer.getVirtualBuffer(self.getWindowHandle()).setCaretPosition(pos)

	def getLineCount(self):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getLineCount()

	def getLineNumber(self,pos):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getLineNumber(pos)

	def getLineStart(self,pos):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getLineStart(pos)

	def getLineLength(self,pos):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getLineLength(pos)

	def getLine(self,pos):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getLine(pos)

	def getTextLength(self):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getTextLength()

	def getText(self):
		return virtualBuffer.getVirtualBuffer(self.getWindowHandle()).getText()

	def script_toggleFocusInteractionMode(self,keyPress):
		"""Toggles focus interaction mode on and off"""
		if not self.focusInteractionMode:
			audio.speakMessage("Focus interaction mode on")
			self.focusInteractionMode=True
		else:
			audio.speakMessage("Focus interaction mode off")
			self.focusInteractionMode=False

	def script_rightArrow(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_nextCharacter(keyPress)

	def script_leftArrow(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_previousCharacter(keyPress)

	def script_upArrow(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_previousLine(keyPress)

	def script_downArrow(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_nextLine(keyPress)

	def script_controlRightArrow(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_nextWord(keyPress)

	def script_controlLeftArrow(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_previousWord(keyPress)

	def script_home(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_startOfLine(keyPress)

	def script_end(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_endOfLine(keyPress)

	def script_controlHome(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_top(keyPress)

	def script_controlEnd(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		self.script_review_bottom(keyPress)

	def script_enter(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		virtualBuffer.getVirtualBuffer(self.getWindowHandle()).activatePosition(self.reviewCursor)

	def script_space(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		virtualBuffer.getVirtualBuffer(self.getWindowHandle()).activatePosition(self.reviewCursor)

	def script_activatePosition(self,keyPress):
		virtualBuffer.getVirtualBuffer(self.getWindowHandle()).activatePosition(self.reviewCursor)

class NVDAObject_internetExplorerServer(NVDAObject_virtualBuffer):

	def event_gainFocus(self):
		if self.getRole() not in [ROLE_SYSTEM_DOCUMENT,ROLE_SYSTEM_PANE]:
			NVDAObject_virtualBuffer.event_gainFocus(self)
 
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
#("MozillaContentWindowClass",None):NVDAObject_virtualBuffer,
("ConsoleWindowClass",ROLE_SYSTEM_WINDOW):NVDAObject_consoleWindowClass,
("ConsoleWindowClass",ROLE_SYSTEM_CLIENT):NVDAObject_consoleWindowClassClient,
("Internet Explorer_Server",None):NVDAObject_internetExplorerServer,
}

dynamicMap={}

