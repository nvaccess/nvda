import time
import re
import win32gui
import win32process
import win32console
import debug
from constants import *
import api
import audio
from config import conf
import NVDAObjects

re_multiSpacing=re.compile(r' +')

def makeVirtualBuffer(window):
	className=win32gui.GetClassName(window)
	if classMap.has_key(className):
		return classMap[className](window)
	else:
		return virtualBuffer(window)

class virtualBuffer(object):

	def __init__(self,window):
		self.virtualBuffer=[]
		self.objects={}
		self.window=window
		self.virtualBuffer=[("None",None)]
		#self.appendObject(window,OBJID_CLIENT,0)

	def getWindowHandle(self):
		return self.window
 
	def getRootObject(self):
		if len(self.virtualBuffer)>=1:
			return self.virtualBuffer[0][1]
		else:
			return None

	def handleEvent(self,name,window,objectID,childID):
		if name not in ["focusObject","foreground"]:
			self.refreshObject(window,objectID,childID)

	def generateObjectBuffer(self,thisObj):
		if thisObj.getWindowHandle()!=self.getWindowHandle():
			return None
		lines=[]
		objList={}
		children=thisObj.getChildren()
		for child in children:
			res=self.generateObjectBuffer(child)
			if res and (len(res)==2):
				for key in res[1]:
					value=(res[1][key][0]+len(lines)+1,res[1][key][1]+len(lines)+1)
					objList[key]=value
				lines+=res[0]
		startText=""
		if conf["presentation"]["reportKeyboardShortcuts"]:
			startText+=" %s"%thisObj.getKeyboardShortcut()
		startText+=" %s"%thisObj.getName()
		startText+=" %s"%thisObj.getTypeString()
		startText+=" %s"%thisObj.getValue()
		startText+=" %s"%NVDAObjects.getStateNames(thisObj.filterStates(thisObj.getStates()))
		startText=startText.strip()
		startText=re_multiSpacing.sub(" ",startText)
		if len(lines)>0:
			startText+=" (has %d items):"%len(children)
			endText="end of %s %s"%(thisObj.getName(),thisObj.getTypeString())
			lines.append((endText,thisObj))
		lines.insert(0,(startText,thisObj))
		objList[thisObj]=(0,len(lines))
		return (lines,objList)


	def appendObject(self,window,objectID,childID):
		obj=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
		if obj:
			res=self.generateObjectBuffer(obj)
			if not res:
				return
			lines,objList=res
			for key in objList:
				value=(objList[key][0]+len(self.virtualBuffer),objList[key][1]+len(self.virtualBuffer))
				self.objects[key]=value
			self.virtualBuffer+=lines

	def refreshObject(self,window,objectID,childID):
		obj=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
		if not obj:
			return
		r=self.getObjectRange(obj)
		if not r:
			return
		for lineNum in range(r[0],r[1]):
			if self.objects.has_key(self.virtualBuffer[r[0]][1]):
				del self.objects[self.virtualBuffer[r[0]][1]]
			del self.virtualBuffer[r[0]]
		res=self.generateObjectBuffer(obj)
		if not res:
			return
		lines,objList=res
		for key in objList:
			value=(objList[key][0]+r[0],objList[key][1]+r[0])
			self.objects[key]=value
		for line in enumerate(lines):
			self.virtualBuffer.insert(r[0]+line[0],line[1])

	def getObjectRange(self,obj):
		return self.objects.get(obj,None)

	def getPositionByLocator(self,window,objectID,childID):
		obj=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
		if not obj:
			return None
		if self.objects.has_key(obj):
			return [self.objects[obj][0],0]
		return None

	def getCaretPosition(self):
		pos=apply(self.getPositionByLocator,api.getFocusLocator())
		if not pos:
			pos=[0,0]
		return pos

	def getEndPosition(self):
		endLineNum=self.getLineCount()-1
		endLineLength=self.getLineLength(endLineNum)
		endLineStart=self.getLineStart(endLineNum)
		pos=[endLineNum,endLineStart[1]+endLineLength]
		return pos

 	def getLineNumber(self,pos):
		return pos[0]

	def getLineStart(self,lineNum):
		return [lineNum,0]

	def activatePosition(self,pos):
		obj=self.virtualBuffer[self.getLineNumber(pos)][1]
		obj.doDefaultAction()

	def nextCharacter(self,pos):
		lineNum=self.getLineNumber(pos)
		lineCount=self.getLineCount()
		if pos[1]==self.getLineLength(lineNum)-1:
			if lineNum==lineCount-1:
				return None
			else:
				return [lineNum+1,0]
		else:
			return [lineNum,pos[1]+1]

	def previousCharacter(self,pos):
		lineNum=self.getLineNumber(pos)
		lineCount=self.getLineCount()
		if pos[1]==0:
			if lineNum==0:
				return None
			else:
				return [lineNum-1,self.getLineLength(lineNum-1)-1]
		else:
			return [lineNum,pos[1]-1]

	def nextWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		curPos=pos
		while curPos and (self.getLineNumber(pos)==self.getLineNumber(curPos)) and (self.getCharacter(curPos) not in whitespace):
			curPos=self.nextCharacter(curPos)
		while curPos and (self.getLineNumber(pos)==self.getLineNumber(curPos)) and (self.getCharacter(curPos) in whitespace):
			curPos=self.nextCharacter(curPos)
		return curPos

	def previousWord(self,pos):
		whitespace=['\n','\r','\t',' ','\0']
		curPos=pos
		while curPos and (self.getLineNumber(pos)==self.getLineNumber(curPos)) and (self.getCharacter(curPos) not in whitespace):
			curPos=self.previousCharacter(curPos)
		pos=curPos
		while curPos and (self.getLineNumber(pos)==self.getLineNumber(curPos)) and (self.getCharacter(curPos) in whitespace):
			curPos=self.previousCharacter(curPos)
		pos=curPos
		while curPos and (self.getLineNumber(pos)==self.getLineNumber(curPos)) and (self.getCharacter(curPos) not in whitespace):
			curPos=self.previousCharacter(curPos)
		if curPos:
			curPos=self.nextCharacter(curPos)
		return curPos

	def getLineCount(self):
		return len(self.virtualBuffer)

	def getLineLength(self,lineNum):
		return len(self.virtualBuffer[lineNum][0])

	def getLine(self,lineNum):
		return self.virtualBuffer[lineNum][0]

	def getText(self):
		text=""
		for line in self.virtualBuffer:
			text+="%s "%line[0]
		return text

	def getTextRange(self,start,end):
		if start[0]==end[0]:
			if start[1]>end[1]:
				return None
			line=self.getLine(start[0])
			if not line:
				return None
			return line[start[1]:end[1]]
		else:
			if start[0]>end[0]:
				return None
			lines=[]
			for lineNum in range(start[0]+1,end[0]):
				lines.append(self.getLine(lineNum))
			lines.insert(0,self.getLine(start[0])[start[1]:])
			endLine=self.getLine(end[0])
			if endLine:
				lines.append(endLine[:end[1]])
			text=""
			for line in lines:
				text+="%s"%line
			return text

	def getCharacter(self,pos):
		return self.getTextRange(pos,self.nextCharacter(pos))

	def getWord(self,pos):
		nextWord=self.nextWord(pos)
		if nextWord:
			return self.getTextRange(pos,nextWord)
		else:
			return self.getTextRange(pos,self.getEndPosition())

class virtualBuffer_mozillaContentWindowClass(virtualBuffer):

	def __init__(self,window):
		audio.cancel()
		audio.speakMessage("Loading document...")
		virtualBuffer.__init__(self,window)
		time.sleep(0.1)
		audio.cancel()
		audio.speakText(self.getText())

	def refreshObject(self,window,objectID,childID):
		obj=NVDAObjects.getNVDAObjectByLocator(window,objectID,childID)
		if obj and (obj.getRole()==ROLE_SYSTEM_DOCUMENT):
			audio.cancel()
			audio.speakMessage("Loading document...")
			if obj.getStates()&STATE_SYSTEM_BUSY:
				return
		virtualBuffer.refreshObject(self,window,objectID,childID)
		if obj and (obj.getRole()==ROLE_SYSTEM_DOCUMENT):
			time.sleep(0.1)
			audio.cancel()
			audio.speakText(self.getText())

class virtualBuffer_mozillaUIWindowClass(virtualBuffer):

	def generateObjectBuffer(self,obj):
		return ([("%s %s"%(obj.getName(),obj.getTypeString()),obj)],{})

class virtualBuffer_cursorBufferWindow(object):

	def __init__(self,window):
		self.window=window

	def handleEvent(self,name,window,objectID,childID):
		pass

	def getWindowHandle(self):
		return self.window

	def getCaretPosition(self):
		obj=api.getFocusObject()
		return obj.getCaretPosition()

	def getLineNumber(self,pos):
		obj=api.getFocusObject()
		return obj.getLineNumber(pos)-obj.getVisibleLineRange()[0]

	def getLineStart(self,lineNum):
		obj=api.getFocusObject()
		lineNum=lineNum+obj.getVisibleLineRange()[0]
		return obj.getLineStart(lineNum)

	def getLine(self,lineNum):
		obj=api.getFocusObject()
		lineNum=lineNum+obj.getVisibleLineRange()[0]
		return obj.getLine(lineNum)

	def getLineCount(self):
		obj=api.getFocusObject()
		v=obj.getVisibleLineRange()
		return (v[1]-v[0])+1
		return obj.getLineCount()

	def nextCharacter(self,pos):
		obj=api.getFocusObject()
		return obj.nextCharacter(pos)

	def previousCharacter(self,pos):
		obj=api.getFocusObject()
		return obj.previousCharacter(pos)

	def nextWord(self,pos):
		obj=api.getFocusObject()
		return obj.nextWord(pos)

	def previousWord(self,pos):
		obj=api.getFocusObject()
		return obj.previousWord(pos)

	def getCharacter(self,pos):
		obj=api.getFocusObject()
		return obj.getCharacter(pos)

	def getWord(self,pos):
		obj=api.getFocusObject()
		return obj.getWord(pos)

classMap={
"MozillaContentWindowClass":virtualBuffer_mozillaContentWindowClass,
"MozillaUIWindowClass":virtualBuffer_mozillaUIWindowClass,
"Edit":virtualBuffer_cursorBufferWindow,
"RICHEDIT50W":virtualBuffer_cursorBufferWindow,
"ConsoleWindowClass":virtualBuffer_cursorBufferWindow,
}
