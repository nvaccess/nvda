import re
import win32gui
import win32process
import win32console
import debug
from constants import *
import api
import audio
from config import conf
from NVDAObjects import getStateNames

re_multiSpacing=re.compile(r' +')

class virtualBuffer(object):

	def __new__(cls,window):
		className=win32gui.GetClassName(window)
		if classMap.has_key(className):
			return object.__new__(classMap[className],window)
		else:
			return object.__new__(cls,window)

	def __init__(self,window):
		self.virtualBuffer=[]
		self.window=window
		if window==api.getForegroundWindow():
			self.appendObject(window,-2,0)
			self.appendObject(window,-3,0)
		self.appendObject(window,OBJID_CLIENT,0)

	def getWindowHandle(self):
		return self.window
 
	def getRootObject(self):
		if len(self.virtualBuffer)>=1:
			return self.virtualBuffer[0][1]
		else:
			return None

	def handleEvent(self,name,window,objectID,childID):
		self.refreshObject(window,objectID,childID)

	def generateObjectBuffer(self,thisObj):
		if thisObj.getWindowHandle()!=self.getWindowHandle():
			return []
		lines=[]
		children=thisObj.getChildren()
		startText=""
		if conf["presentation"]["reportKeyboardShortcuts"]:
			startText+=" %s"%thisObj.getKeyboardShortcut()
		startText+=" %s"%thisObj.getName()
		startText+=" %s"%thisObj.getTypeString()
		startText+=" %s"%thisObj.getValue()
		startText+=" %s"%getStateNames(thisObj.filterStates(thisObj.getStates()))
		startText=startText.strip()
		startText=re_multiSpacing.sub(" ",startText)
		startLine=(startText,thisObj,1)
		for child in children:
			childBuffer=self.generateObjectBuffer(child)
			lines+=childBuffer
		if len(lines)>1:
			endText="end of %s %s"%(thisObj.getName(),thisObj.getTypeString())
			lines.append((endText,thisObj,None))
			startLine=("%s (contains %d items):"%(startLine[0],len(children)),startLine[1],len(lines)+1)
		elif len(lines)==1:
			startLine=("%s:"%startLine[0],startLine[1],len(lines)+1)
		lines.insert(0,startLine)
		return lines

	def appendObject(self,window,objectID,childID):
		obj=api.getNVDAObjectByLocator(window,objectID,childID)
		if obj:
			self.virtualBuffer+=self.generateObjectBuffer(obj)

	def getObjectLineRange(self,obj):
		for line in enumerate(self.virtualBuffer):
			if line[1][1]==obj:
				return (line[0],line[0]+line[1][2])
		return None

	def refreshObject(self,window,objectID,childID):
		obj=api.getNVDAObjectByLocator(window,objectID,childID)
		if not obj:
			return
		lineRange=self.getObjectLineRange(obj)
		if not lineRange or (lineRange[0]>=len(self.virtualBuffer)) or (lineRange[1]>=len(self.virtualBuffer)):
			return
		for lineNum in range(lineRange[0],lineRange[1]):
			del self.virtualBuffer[lineRange[0]]
		for line in enumerate(self.generateObjectBuffer(obj)):
			self.virtualBuffer.insert(lineRange[0]+line[0],line[1])

	def getIndexByLocator(self,window,objectID,childID):
		obj=api.getNVDAObjectByLocator(window,objectID,childID)
		if not obj:
			return None
		for line in enumerate(self.virtualBuffer):
			if line[1][1]==obj:
				return [line[0],0]
		return None

	def getCaretIndex(self):
		obj=apply(api.getNVDAObjectByLocator,api.getFocusLocator())
		lineRange=self.getObjectLineRange(obj)
		if not lineRange:
			return [0,0]
		index=[lineRange[0],0]
		if not index:
			index=[0,0]
		return index

	def activateIndex(self,index=None):
		if not index:
			index=self.getCaretIndex()
		obj=self.virtualBuffer[index[0]][1]
		obj.doDefaultAction()

	def getNextCharacterIndex(self,index,crossLines=True):
		lineLength=self.getLineLength(index=index)
		lineCount=self.getLineCount()
		if index[1]==lineLength:
			if (index[0]==lineCount-1) or not crossLines:
				return None
			else:
				newIndex=[index[0]+1,0]
		else:
			newIndex=[index[0],index[1]+1]
		return newIndex

	def getPreviousCharacterIndex(self,index,crossLines=True):
		lineLength=self.getLineLength(index=index)
		lineCount=self.getLineCount()
		if index[1]==0:
			if (index[0]==0) or not crossLines:
				return None
			else:
				newIndex=[index[0]-1,self.getLineLength(self.getPreviousLineIndex(index))-1]
		else:
			newIndex=[index[0],index[1]-1]
		return newIndex

	def getWordEndIndex(self,index):
		whitespace=['\n','\r','\t',' ','\0']
		if not index:
			raise TypeError("function takes a character index as its ownly argument")
		curIndex=index
		while self.getCharacter(index=curIndex) not in whitespace:
			prevIndex=curIndex
			curIndex=self.getNextCharacterIndex(curIndex,crossLines=False)
			if not curIndex:
				return prevIndex
		return curIndex

	def getPreviousWordIndex(self,index):
		whitespace=['\n','\r','\t',' ','\0']
		if not index:
			raise TypeError("function takes a character index as its ownly argument")
		curIndex=index
		while curIndex and self.getCharacter(index=curIndex) not in whitespace:
			curIndex=self.getPreviousCharacterIndex(curIndex,crossLines=False)
		if not curIndex:
			return None
		curIndex = self.getPreviousCharacterIndex(curIndex, crossLines = False)
		while curIndex and self.getCharacter(index=curIndex) not in whitespace:
			curIndex=self.getPreviousCharacterIndex(curIndex,crossLines=False)
		if not curIndex:
			return None
		return self.getNextCharacterIndex(curIndex, crossLines = False)

	def getNextLineIndex(self,index):
		lineCount=self.getLineCount()
		if index[0]>=lineCount-1:
			return None
		else:
			return [index[0]+1,0]

	def getPreviousLineIndex(self,index):
		lineCount=self.getLineCount()
		if index[0]<=0:
			return None
		else:
			return [index[0]-1,0]
 
	def getLineCount(self):
		return len(self.virtualBuffer)

	def getLineLength(self,index=None):
		if index is None:
			index=getCaretIndex()
		return len(self.virtualBuffer[index[0]][0])

	def getLine(self,index=None):
		if index is None:
			index=self.getCaretIndex()
		return self.virtualBuffer[index[0]][0]

	def getCharacter(self,index=None):
		if index is None:
			index=self.getCaretIndex()
		if index[1]>=self.getLineLength(index=index):
			return None
		return self.getLine(index=index)[index[1]]

	def getWord(self,index=None):
		if not index:
			index=self.getCaretIndex()
		end=self.getWordEndIndex(index)
		if not end or (end==index):
			text=self.getCharacter(index=index)
		else:
			text=self.getTextRange(index,end)
		return text

	def getTextRange(self,start,end):
		if start[0]==end[0]:
			if start[1]>end[1]:
				raise TypeError("Start and end indexes are invalid (%s, %s)"%(start,end))
			line=self.getLine(index=start)
			if not line:
				return None
			return line[start[1]:end[1]]
		else:
			if start[0]>end[0]:
				raise TypeError("Start and end indexes are invalid (%s, %s)"%(start,end))
			lines=[]
			for lineNum in range(end[0])[start[1]+1:]:
				lines.append(self.getLine(index=[lineNum,0]))
			lines.insert(0,self.getLine(index=start)[start[1]:])
			endLine=self.getLine(index=end)
			if endLine:
				lines.append(self.getLine(index=end)[:end[1]])
			text=""
			for line in lines:
				text+="%s "%line
			return text

	def getText(self):
		text=""
		index=[0,0]
		while index:
			text+="%s "%self.getLine(index=index)
			index=self.getNextLineIndex(index)
		return text

class virtualBuffer_mozillaContentWindowClass(virtualBuffer):

	def handleEvent(self,name,window,objectID,childID):
		obj=api.getNVDAObjectByLocator(window,objectID,childID)
		if not obj:
			return
		if not ((obj.getRole()==ROLE_SYSTEM_DOCUMENT) and not (name=="objectReorder")):
			virtualBuffer.handleEvent(self,name,window,objectID,childID)

	def generateObjectBuffer(self,obj):
		lines=[]
		if not conf["virtualBuffer"]["includeTableStructure"] and (obj.getRole() in [ROLE_SYSTEM_CELL,ROLE_SYSTEM_TABLE,"tbody","thead"]):
			for child in obj.getChildren():
				lines+=self.generateObjectBuffer(child)
		else:
			lines+=virtualBuffer.generateObjectBuffer(self,obj)
		return lines

class virtualBuffer_mozillaUIWindowClass(virtualBuffer):

	def generateObjectBuffer(self,obj):
		if obj.getRole()==ROLE_SYSTEM_DOCUMENT:
			return [("%s %s"%(obj.getName(),obj.getTypeString()),obj,1)]
		return virtualBuffer.generateObjectBuffer(self,obj)

class virtualBuffer_cursorBufferWindow(virtualBuffer):

	def getCaretIndex(self):
		index=api.getFocusObject().getCaretIndex()
		visibleLineRange=api.getFocusObject().getVisibleLineRange()
		index[0]=index[0]-visibleLineRange[0]
		return index

	def getLine(self,index=None):
		if index:
			visibleLineRange=api.getFocusObject().getVisibleLineRange()
			index=[index[0]+visibleLineRange[0],index[1]]
		return api.getFocusObject().getLine(index=index)

	def getLineLength(self,index=None):
		return api.getFocusObject().getLineLength(index=index)

	def getLineCount(self):
		visibleLineRange=api.getFocusObject().getVisibleLineRange()
		return (visibleLineRange[1]-visibleLineRange[0])

classMap={
"MozillaContentWindowClass":virtualBuffer_mozillaContentWindowClass,
"MozillaUIWindowClass":virtualBuffer_mozillaUIWindowClass,
"Edit":virtualBuffer_cursorBufferWindow,
"RICHEDIT50W":virtualBuffer_cursorBufferWindow,
"ConsoleWindowClass":virtualBuffer_cursorBufferWindow,
}
