import eventHandler
import queueHandler
import controlTypes
import speech
import config
from NVDAObjects.window import Window
from behaviors import EditableTextWithAutoSelectDetection 
from textInfos.offsets import OffsetsTextInfo

class InputCompositionTextInfo(OffsetsTextInfo):

	def _getSelectionOffsets(self):
		return self.obj.compositionSelectionOffsets

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _getStoryLength(self):
		return len(self.obj.compositionString) if self.obj.compositionString else 0

	def _getStoryText(self):
		return self.obj.compositionString if self.obj.compositionString else u""

class InputComposition(EditableTextWithAutoSelectDetection,Window):

	TextInfo=InputCompositionTextInfo
	name=_("Composition")
	role=controlTypes.ROLE_EDITABLETEXT
	next=None
	previous=None
	firstChild=None
	lastChild=None
	states=set()
	location=None
	compositionString=""
	compositionSelectionOffsets=(0,0)

	def __init__(self,parent=None):
		self.parent=parent
		super(InputComposition,self).__init__(windowHandle=parent.windowHandle)

	def findOverlayClasses(self,clsList):
		clsList.append(InputComposition)
		clsList.append(InputComposition)
		return clsList

	def compositionUpdate(self,compositionString,selectionStart,selectionEnd,newText):
		if (config.conf["keyboard"]["speakTypedCharacters"] or config.conf["keyboard"]["speakTypedWords"]) and newText and not newText.isspace() and compositionString!=self.compositionString:
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakText,newText)
		self.compositionString=compositionString
		self.compositionSelectionOffsets=(selectionStart,selectionEnd)
		eventHandler.queueEvent("valueChange",self)
		eventHandler.queueEvent("caret",self)
