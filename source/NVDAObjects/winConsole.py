import ctypes
import difflib
import winKernel
import winUser
import audio
from autoPropertyType import autoPropertyType

class NVDAObjectExt_console:

	__metaclass__=autoPropertyType

	text_caretSayAllGenerator=None

	def consoleEventHook(self,handle,eventID,window,objectID,childID,threadID,timestamp):
		self.text_reviewOffset=self.text_caretOffset
		newLines=self.consoleVisibleLines
		if eventID!=winUser.EVENT_CONSOLE_UPDATE_SIMPLE:
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

	def _get_text_reviewOffsetLimits(self):
		if not hasattr(self,"consoleHandle"):
			return (0,0) 
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		top=self.getOffsetFromConsoleCoord(0,info.windowRect.top)
		bottom=self.getOffsetFromConsoleCoord(self.getConsoleHorizontalLength(),info.windowRect.bottom)
		return (top,bottom)

	def _get_text_caretOffset(self):
		if not hasattr(self,"consoleHandle"):
			return 0
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		y=info.cursorPosition.y
		x=info.cursorPosition.x
		return self.getOffsetFromConsoleCoord(x,y)

	def getOffsetFromConsoleCoord(self,x,y):
		if not hasattr(self,"consoleHandle"):
			return 0
		return (y*self.getConsoleHorizontalLength())+x

	def getConsoleCoordFromOffset(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		return (offset%self.getConsoleHorizontalLength(),offset/self.getConsoleHorizontalLength())

	def text_getLineOffsets(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		start=offset-(offset%self.getConsoleHorizontalLength())
		end=start+self.getConsoleHorizontalLength()
		return (start,end)

	def text_getNextLineOffsets(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		(x,y)=self.getConsoleCoordFromOffset(offset)
		x=0
		y+=1
		newOffset=self.getOffsetFromConsoleCoord(x,y)
		if newOffset<self.text_characterCount:
			return self.text_getLineOffsets(newOffset)
		else:
			return None

	def text_getPrevLineOffsets(self,offset):
		if not hasattr(self,"consoleHandle"):
			return (0,0)
		(x,y)=self.getConsoleCoordFromOffset(offset)
		x=0
		if y<=0:
			return None
		y-=1
		newOffset=self.getOffsetFromConsoleCoord(x,y)
		if newOffset>=0:
			return self.text_getLineOffsets(newOffset)
		else:
			return None

	def _get_text_characterCount(self):
		return self.getOffsetFromConsoleCoord(self.getConsoleHorizontalLength(),self.getConsoleVerticalLength()-1)

	def text_getText(self,start=None,end=None):
		if not hasattr(self,"consoleHandle"):
			return "\0"
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else len(self.value)
		(x,y)=self.getConsoleCoordFromOffset(start)
		maxLen=end-start
		text=winKernel.readConsoleOutputCharacter(self.consoleHandle,maxLen,x,y)
		return text

	def _get_consoleVisibleLines(self):
		if not hasattr(self,"consoleHandle"):
			return []
		info=winKernel.getConsoleScreenBufferInfo(self.consoleHandle)
		top=info.windowRect.top
		bottom=info.windowRect.bottom
		lines=[]
		for lineNum in range(top,bottom+1):
			line=winKernel.readConsoleOutputCharacter(self.consoleHandle,self.getConsoleHorizontalLength(),0,lineNum)
			if line and not line.isspace():
				lines.append(line)
		return lines

	def event_gainFocus(self):
		processID=self.windowProcessID[0]
		try:
			winKernel.freeConsole()
		except:
			debug.writeException("freeConsole")
			pass
		winKernel.attachConsole(processID)
		res=winKernel.getStdHandle(winKernel.STD_OUTPUT_HANDLE)
		if not res:
			raise OSError("NVDAObject_consoleWindowClassClient: could not get console std handle") 
		self.consoleHandle=res
		self.consoleEventHookHandles=[]
		self.oldLines=self.consoleVisibleLines
		super(NVDAObjectExt_console,self).event_gainFocus()
		self.cConsoleEventHook=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(self.consoleEventHook)
		for eventID in [winUser.EVENT_CONSOLE_CARET,winUser.EVENT_CONSOLE_UPDATE_REGION,winUser.EVENT_CONSOLE_UPDATE_SIMPLE,winUser.EVENT_CONSOLE_UPDATE_SCROLL]:
			handle=winUser.setWinEventHook(eventID,eventID,0,self.cConsoleEventHook,0,0,0)
			if handle:
				self.consoleEventHookHandles.append(handle)
			else:
				raise OSError('Could not register console event %s'%eventID)
		self.text_reviewOffset=self.text_caretOffset
		for line in self.consoleVisibleLines:
			audio.speakText(line)

	def event_looseFocus(self):
		for handle in self.consoleEventHookHandles:
			winUser.unhookWinEvent(handle)
		del self.consoleHandle
		try:
			winKernel.freeConsole()
		except:
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
