import time
import struct
import difflib
import ctypes
import comtypes.automation
import comtypesClient
import debug
import lang
import MSAAHandler
import winUser
import winKernel
import audio
import api
from config import conf
from constants import *
import window
import textBuffer
import manager
import ITextDocument
import virtualBuffer

class NVDAObject_MSAA(window.NVDAObject_window):

	def __init__(self,*args):
		self.ia=args[0]
		self.child=args[1]
		window.NVDAObject_window.__init__(self,MSAAHandler.windowFromAccessibleObject(self.ia))
		self._lastStates=self.states

	def __hash__(self):
		l=10000000
		p=17
		h=window.NVDAObject_window.__hash__(self)
		role=self.role
		if isinstance(role,basestring):
			role=hash(role)
		if isinstance(role,int):
			h=(h+(role*p))%l
		childID=self.childID
		if isinstance(childID,int):
			h=(h+(childID*p))%l
		location=self.location
		if location and (len(location)==4):
			left,top,width,height=location
			h=(h+(left*p))%l
			h=(h+(top*p))%l
			h=(h+(width*p))%l
			h=(h+(height*p))%l
		return h

	def getName(self):
		return MSAAHandler.accName(self.ia,self.child)
	name=property(fget=getName)

	def getValue(self):
		return MSAAHandler.accValue(self.ia,self.child)
	value=property(fget=getValue)

	def getRole(self):
		return MSAAHandler.accRole(self.ia,self.child)
	role=property(fget=getRole)

	def getTypeString(self):
		role=self.role
		if conf["presentation"]["reportClassOfAllObjects"] or (conf["presentation"]["reportClassOfClientObjects"] and (role==ROLE_SYSTEM_CLIENT)):
			typeString=self.className
		else:
			typeString=""
		return typeString+" %s"%MSAAHandler.getRoleName(self.role)
	typeString=property(fget=getTypeString)

	def getStates(self):
		return MSAAHandler.accState(self.ia,self.child)
	states=property(fget=getStates)

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

	def getStateName(self,state,opposite=False):
		dictState=lang.stateNames.get(state,None)
		if dictState:
			newState=dictstate
		elif isinstance(state,int):
			newState=MSAAHandler.getStateText(state)
		else:
			newState=state
		if opposite:
			newState=lang.messages["not"]+" "+newState
		return newState

	def getDescription(self):
		try:
			return self.ia.accDescription(self.child)
		except:
			return ""
	description=property(fget=getDescription)

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
	keyboardShortcut=property(fget=getKeyboardShortcut)

	def getChildID(self):
		try:
			return self.child
		except:
			return None
	childID=property(fget=getChildID)

	def getChildCount(self):
		count=MSAAHandler.accChildCount(self.ia,self.child)
		return count
	childCount=property(fget=getChildCount)

	def getLocation(self):
		location=MSAAHandler.accLocation(self.ia,self.child)
		return location
	location=property(fget=getLocation)

	def getParent(self):
		res=MSAAHandler.accParent(self.ia,self.child)
		if res:
			(ia,child)=res
		else:
			return None
		obj=manager.getNVDAObjectByAccessibleObject(ia,child)
		if obj and (obj.getRole()==ROLE_SYSTEM_WINDOW):
			return obj.getParent()
		else:
			return obj
	parent=property(fget=getParent)

	def getNext(self):
		res=MSAAHandler.accParent(self.ia,self.child)
		if res:
			parentObject=manager.getNVDAObjectByAccessibleObject(res[0],res[1])
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
			nextObject=manager.getNVDAObjectByAccessibleObject(res[0],res[1])
			if nextObject and (nextObject.getRole()==ROLE_SYSTEM_WINDOW):
				nextObject=manager.getNVDAObjectByLocator(nextObject.hwnd,-4,0)
			if nextObject!=self:
				return nextObject
			else:
				return None
	next=property(fget=getNext)

	def getPrevious(self):
		res=MSAAHandler.accParent(self.ia,self.child)
		if res:
			parentObject=manager.getNVDAObjectByAccessibleObject(res[0],res[1])
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
			previousObject=manager.getNVDAObjectByAccessibleObject(res[0],res[1])
			if previousObject and (previousObject.getRole()==ROLE_SYSTEM_WINDOW):
				previousObject=manager.getNVDAObjectByLocator(previousObject.hwnd,-4,0)
			if previousObject!=self:
				return previousObject
			else:
				return None
	previous=property(fget=getPrevious)

	def getFirstChild(self):
		res=MSAAHandler.accNavigate(self.ia,self.child,NAVDIR_FIRSTCHILD)
		if res:
			obj=manager.getNVDAObjectByAccessibleObject(res[0],res[1])
		else:
			return None
		if obj and (obj.getRole()==ROLE_SYSTEM_WINDOW):
			return manager.getNVDAObjectByLocator(obj.hwnd,OBJID_CLIENT,0)
		else:
			return obj
	firstChild=property(fget=getFirstChild)

	def doDefaultAction(self):
		MSAAHandler.accDoDefaultAction(self.ia,self.child)

	def getChildren(self):
		children=[]
		obj=self.getFirstChild()
		while obj:
			children.append(obj)
			obj=obj.getNext()
		return children
	children=property(fget=getChildren)

	def getActiveChild(self):
		res=MSAAHandler.accFocus()
		if res:
			return manager.getNVDAObjectByAccessibleObject(res[0],res[1])
	activeChild=property(fget=getActiveChild)

	def hasFocus(self):
		states=0
		states=self.states
		if (states&STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		self.ia.SetFocus()

	def getPositionString(self):
		position=""
		childID=self.childID
		if childID>0:
			parent=self.parent
			if parent:
				parentChildCount=parent.childCount
				if parentChildCount>=childID:
					position="%s of %s"%(childID,parentChildCount)
		return position
	positionString=property(fget=getPositionString)

	def event_foreground(self):
		audio.cancel()
		self.speakObject()

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

	def event_gainFocus(self):
		self.updateMenuMode()
		if self.hasFocus() and not (not api.getMenuMode() and (self.role==ROLE_SYSTEM_MENUITEM)) and not ((self.hwnd==winUser.getForegroundWindow()) and (self.role==ROLE_SYSTEM_CLIENT)):
			self.speakObject()

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
		states=self.states
		if states is None or not self.hasFocus():
			return None
		states_on=states-(states&self._lastStates)
		audio.speakObjectProperties(stateText=MSAAHandler.getStateNames(self.filterStates(states_on)))
		states_off=self._lastStates-(states&self._lastStates)
		audio.speakObjectProperties(stateText=MSAAHandler.getStateNames(self.filterStates(states_off),opposite=True))
		self._lastStates=states

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

	def event_foreground(self):
		self.speakObject()
		for child in self.children:
			states=child.states
			if (not states&STATE_SYSTEM_OFFSCREEN) and (not states&STATE_SYSTEM_INVISIBLE) and (not states&STATE_SYSTEM_UNAVAILABLE):
				child.speakObject()
			if child.role==ROLE_SYSTEM_PROPERTYPAGE:
				for grandChild in child.children:
					states=grandChild.states
					if (not states&STATE_SYSTEM_OFFSCREEN) and (not states&STATE_SYSTEM_INVISIBLE) and (not states&STATE_SYSTEM_UNAVAILABLE):
						grandChild.speakObject()

class NVDAObject_TrayClockWClass(NVDAObject_MSAA):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def getRole(self):
		return ROLE_SYSTEM_CLOCK
	role=property(fget=getRole)

class NVDAObject_Shell_TrayWnd(NVDAObject_MSAA):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows start button and taskbar.
	"""
 
	def event_foreground(self):
		pass

	def event_gainFocus(self):
		pass

class NVDAObject_Progman(NVDAObject_MSAA):
	"""
	Based on NVDAObject but on foreground events nothing gets spoken.
	This is the window which holds the windows desktop.
	"""

	def event_foreground(self):
		pass

	def event_gainFocus(self):
		pass

class NVDAObject_staticText(textBuffer.NVDAObject_textBuffer,NVDAObject_MSAA):

	def __init__(self,*args):
		NVDAObject_MSAA.__init__(self,*args)
		textBuffer.NVDAObject_textBuffer.__init__(self,*args)

class NVDAObject_edit(textBuffer.NVDAObject_editableTextBuffer,NVDAObject_MSAA):

	def __init__(self,*args):
		NVDAObject_MSAA.__init__(self,*args)
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)

	def getValue(self):
		return self.getCurrentLine()
	value=property(fget=getValue)

	def getCaretRange(self):
		long=winUser.sendMessage(self.hwnd,EM_GETSEL,0,0)
		start=winUser.LOWORD(long)
		end=winUser.HIWORD(long)
		return (start,end)
	caretRange=property(fget=getCaretRange)

	def getCaretPosition(self):
		long=winUser.sendMessage(self.hwnd,EM_GETSEL,0,0)
		pos=winUser.LOWORD(long)
		return pos

	def setCaretPosition(self,pos):
		winUser.sendMessage(self.hwnd,EM_SETSEL,pos,pos)

	caretPosition=property(fget=getCaretPosition,fset=setCaretPosition)

	def getLineCount(self):
		lineCount=winUser.sendMessage(self.hwnd,EM_GETLINECOUNT,0,0)
		if lineCount<0:
			return None
		return lineCount

	def getLineNumber(self,pos):
		return winUser.sendMessage(self.hwnd,EM_LINEFROMCHAR,pos,0)

	def getPositionFromLineNumber(self,lineNum):
		return winUser.sendMessage(self.hwnd,EM_LINEINDEX,lineNum,0)

	def getLineStart(self,pos):
		lineNum=self.getLineNumber(pos)
		return winUser.sendMessage(self.hwnd,EM_LINEINDEX,lineNum,0)

	def getLineLength(self,pos):
		lineLength=winUser.sendMessage(self.hwnd,EM_LINELENGTH,pos,0)
		if lineLength<0:
			return None
		return lineLength

	def getLine(self,pos):
		lineNum=self.getLineNumber(pos)
		lineLength=self.getLineLength(pos)
		if not lineLength:
			return None
		sizeData=struct.pack('h',lineLength)
		buf=ctypes.create_unicode_buffer(sizeData,size=lineLength)
		res=winUser.sendMessage(self.hwnd,EM_GETLINE,lineNum,buf)
		return buf.value

	def nextLine(self,pos):
		lineNum=self.getLineNumber(pos)
		if lineNum+1<self.getLineCount():
			return self.getPositionFromLineNumber(lineNum+1)

	def previousLine(self,pos):
		lineNum=self.getLineNumber(pos)
		if lineNum-1>=0:
			return self.getPositionFromLineNumber(lineNum-1)

	def event_caret(self):
		self._reviewCursor=self.caretPosition

	def event_valueChange(self):
		pass


class NVDAObject_checkBox(NVDAObject_MSAA):
	"""
	Based on NVDAObject, but filterStates removes the pressed state for checkboxes.
	"""

	def filterStates(self,states):
		states=NVDAObject_MSAA.filterStates(self,states)
		states-=states&STATE_SYSTEM_PRESSED
		return states

class NVDAObject_outlineItem(NVDAObject_MSAA):

	def getValue(self):
		return "level %s"%NVDAObject_MSAA.getValue(self)
	value=property(fget=getValue)

class NVDAObject_tooltip(NVDAObject_MSAA):

	def getName(self):
		name=NVDAObject_MSAA.getName(self)
		value=NVDAObject_MSAA.getValue(self)
		if name and not value:
			return ""
		else:
			return name
	name=property(fget=getName)

	def getValue(self):
		name=NVDAObject_MSAA.getName(self)
		value=NVDAObject_MSAA.getValue(self)
		if name and not value:
			return name
		else:
			return ""
	value=property(fget=getValue)

	def event_toolTip(self):
		if conf["presentation"]["reportTooltips"]:
			self.speakObject()

class NVDAObject_consoleWindowClass(NVDAObject_MSAA):

	def event_nameChange(self):
		pass

class NVDAObject_consoleWindowClassClient(textBuffer.NVDAObject_editableTextBuffer,NVDAObject_MSAA):

	def __init__(self,*args):
		NVDAObject_MSAA.__init__(self,*args)
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
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)

	def __del__(self):
		try:
			winKernel.freeConsole()
		except:
			debug.writeException("freeConsole")
		NVDAObject_edit.__del__(self)

	def consoleEventHook(self,handle,eventID,window,objectID,childID,threadID,timestamp):
		self._reviewCursor=self.caretPosition
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
	visibleRange=property(fget=getVisibleRange)

	def getCaretPosition(self):
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		y=info.cursorPosition.y
		x=info.cursorPosition.x
		return self.getPositionFromCoord(x,y)
	caretPosition=property(fget=getCaretPosition)

	def getEndPosition(self):
		return self.getConsoleVerticalLength()*self.getConsoleHorizontalLength()
	endPosition=property(fget=getEndPosition)

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
	text=property(fget=getText)

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
	value=property(fget=getValue)

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

class NVDAObject_richEdit(ITextDocument.NVDAObject_ITextDocument,NVDAObject_MSAA):

	def __init__(self,*args):
		NVDAObject_MSAA.__init__(self,*args)
		ITextDocument.NVDAObject_ITextDocument.__init__(self,*args)
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)

	def getDocumentObjectModel(self):
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		res=ctypes.windll.oleacc.AccessibleObjectFromWindow(self.hwnd,OBJID_NATIVEOM,ctypes.byref(domPointer._iid_),ctypes.byref(domPointer))
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
	value=property(fget=getValue)

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

class NVDAObject_mozillaContentWindowClass(NVDAObject_MSAA):
	pass

class NVDAObject_mozillaContentWindowClass_document(NVDAObject_mozillaContentWindowClass):

	def getValue(self):
		return ""
	value=property(fget=getValue)

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
	value=property(fget=getValue)

	def filterStates(self,states):
		states=NVDAObject_mozillaContentWindowClass.filterStates(self,states)
		states-=(states&STATE_SYSTEM_LINKED)
		states-=(states&STATE_SYSTEM_TRAVERSED)
		return states

	def getTypeString(self):
		states=self.states
		typeString=""
		if states&STATE_SYSTEM_TRAVERSED:
			typeString+="visited "
		if states&STATE_SYSTEM_SELECTED:
			typeString+="same page "
		typeString+=NVDAObject_MSAA.getTypeString(self)
		return typeString
	typeString=property(fget=getTypeString)

	def getChildren(self):
		children=NVDAObject_MSAA.getChildren(self)
		newChildren=[]
		for child in children:
			if child.getRole()!=ROLE_SYSTEM_STATICTEXT:
				newChildren.append(child)
		return newChildren
	children=property(fget=getChildren)

class NVDAObject_mozillaContentWindowClass_listItem(NVDAObject_mozillaContentWindowClass):
	"""
	Based on NVDAObject_mozillaContentWindowClass, but:
	*Name is the bullet or counter for the list item which is found in the text object which is the first child of this object.
	*getChildren ignores the first child wich is the text object that contains the bullet or counter for the list item.
	"""

	def getName(self):
		child=self.getFirstChild()
		if child and self.role==ROLE_SYSTEM_STATICTEXT:
			name=child.getName()
		else:
			name=""
		return name
	name=property(fget=getName)

	def getChildren(self):
		children=NVDAObject_MSAA.getChildren(self)
		if (len(children)>=1) and (NVDAObject_MSAA.getRole(children[0])==ROLE_SYSTEM_STATICTEXT):
			del children[0]
		return children
	children=property(fget=getChildren)

class NVDAObject_mozillaContentWindowClass_text(NVDAObject_mozillaContentWindowClass):
	"""
	Based on NVDAObject_mozillaContentWindowClass but:
	*If the object has a name but no value, the name is used as the value and no name is provided.
	*the role is changed to static text if it has the read only state set.
	"""

	def getName(self):
		name=NVDAObject_MSAA.getName(self)
		value=NVDAObject_MSAA.getValue(self)
		if name and not value:
			return ""
		else:
			return name
	name=property(fget=getName)

	def getRole(self):
		if NVDAObject_MSAA.getStates(self)&STATE_SYSTEM_READONLY:
			return ROLE_SYSTEM_STATICTEXT
		else:
			return NVDAObject_MSAA.getRole(self)
	role=property(fget=getRole)

	def getValue(self):
		name=NVDAObject_MSAA.getName(self)
		value=NVDAObject_MSAA.getValue(self)
		if name and not value:
			return name
		else:
			return ""
	value=property(fget=getValue)

class NVDAObject_internetExplorerServer(virtualBuffer.NVDAObject_virtualBuffer,NVDAObject_MSAA):

	def __init__(self,*args):
		NVDAObject_MSAA.__init__(self,*args)
		virtualBuffer.NVDAObject_virtualBuffer.__init__(self,*args)

	def event_gainFocus(self):
		if self.role not in [ROLE_SYSTEM_DOCUMENT,ROLE_SYSTEM_PANE]:
			NVDAObject_MSAA.event_gainFocus(self)

