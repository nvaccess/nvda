from default import *
import comtypes.client
import comtypes.automation
import ctypes

#Word constants

#Indexing
wdFirstCharacterLineNumber=10
#Units
wdCharacter=1
wdWord=2
wdLine=5
wdStory=6
wdWindow=11
#GoTo - direction
wdGoToAbsolute=1
wdGoToNext=2
#GoTo - units
wdGoToLine=3

def event_moduleStart():
	NVDAObjects.registerNVDAObjectClass("_WwG",ROLE_SYSTEM_CLIENT,NVDAObject_wordDocument)

def event_moduleEnd():
	NVDAObjects.unregisterNVDAObjectClass("_WwG",ROLE_SYSTEM_CLIENT)

class NVDAObject_wordDocument(NVDAObjects.NVDAObject_edit):

	def __init__(self,accObject):
		NVDAObjects.NVDAObject_edit.__init__(self,accObject)
		ptr=ctypes.c_void_p()
		ctypes.windll.oleacc.AccessibleObjectFromWindow(self.getWindowHandle(),-16,ctypes.byref(comtypes.automation.IUnknown._iid_),ctypes.byref(ptr))
		ptr=ctypes.cast(ptr,ctypes.POINTER(comtypes.automation.IUnknown))
		self.documentWindow=comtypes.client.wrap(ptr).ActivePane
		self.keyMap.update({
key("insert+f"):self.script_fontInfo,
})

	def getRole(self):
		return ROLE_SYSTEM_TEXT

	def getCaretRange(self):
		start=self.documentWindow.Selection.Start
		end=self.documentWindow.Selection.End
		if start!=end:
			return (start,end)
		else:
			return None

	def getCaretPosition(self):
		return self.documentWindow.Selection.Start

	def getVisibleLineRange(self):
		range=self.documentWindow.Selection.Range
		range.Expand(wdWindow)
		return (self.getLineNumber(range.Start),self.getLineNumber(range.End))

	def getStartPosition(self):
		return 0

	def getEndPosition(self):
		range=self.documentWindow.Selection.Range
		range.Expand(wdStory)
		return range.End

	def getLineNumber(self,pos):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=0
		range.Move(wdCharacter,pos)
		return range.Information(wdFirstCharacterLineNumber)-1

	def getLineStart(self,lineNum):
		range=self.documentWindow.Selection.Range
		range=range.GoTo(wdGoToLine,wdGoToAbsolute,lineNum+1)
		return range.Start

	def getLine(self,lineNum):
		start=self.getLineStart(lineNum)
		range=self.documentWindow.Selection.Range
		range.Start=range.End=start
		newRange=range.GoTo(wdGoToLine,wdGoToNext)
		range.End=newRange.Start-1
		text=range.Text
		if text!='\r':
			return text
		else:
			return None

	def getLineCount(self):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=0
		range.Expand(wdStory)
		return self.getLineNumber(range.End)

	def nextWord(self,pos):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=pos
		delta=range.Move(wdWord,1)
		if delta:
			return range.Start
		else:
			return None

	def previousWord(self,pos):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=pos
		delta=range.Move(wdWord,-1)
		if delta:
			return range.Start
		else:
			return None

	def getTextRange(self,start,end):
		range=self.documentWindow.Selection.Range
		range.Start=start
		range.End=end
		return range.Text

	def getFontName(self,pos):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=pos
		return range.Font.Name

	def getCurrentFontName(self):
		return self.getFontName(self.getCaretPosition())

	def getFontSize(self,pos):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=pos
		return "%d"%range.Font.Size

	def getCurrentFontSize(self):
		return self.getFontSize(self.getCaretPosition())

	def script_fontInfo(self,keyPress):
		audio.speakMessage("Font: %s, %s pt"%(self.getCurrentFontName(),self.getCurrentFontSize()))

	def getFontName(self,pos):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=pos
		return range.Font.Name

	def getCurrentFontName(self):
		return self.getFontName(self.getCaretPosition())

	def getFontSize(self,pos):
		range=self.documentWindow.Selection.Range
		range.Start=range.End=pos
		return "%d"%range.Font.Size

	def getCurrentFontSize(self):
		return self.getFontSize(self.getCaretPosition())

	def script_fontInfo(self,keyPress):
		audio.speakMessage("Font: %s, %s pt"%(self.getCurrentFontName(),self.getCurrentFontSize()))
