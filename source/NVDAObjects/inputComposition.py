import eventHandler
import queueHandler
import controlTypes
import characterProcessing
import speech
import config
from NVDAObjects.window import Window
from behaviors import EditableTextWithAutoSelectDetection, CandidateItem as CandidateItemBehavior 
from textInfos.offsets import OffsetsTextInfo

def calculateInsertedChars(oldComp,newComp):
	oldLen=len(oldComp)
	newLen=len(newComp)
	minLen=min(oldLen,newLen)
	print "oldLen %d, newLen %d, minLen %d"%(oldLen,newLen,minLen)
	diffStart=0
	diffEnd=newLen
	for index in xrange(minLen):
		print "checking start: index %d, new %c, old %c"%(index,newComp[index],oldComp[index])
		if newComp[index]!=oldComp[index]:
			break
		diffStart=index+1
	for index in xrange(minLen,0,-1):
		backIndex=index-minLen-1
		print "checking end: index %d, backIndex %d, new %c, old %c"%(index,backIndex,newComp[backIndex],oldComp[backIndex])
		if newComp[backIndex]!=oldComp[backIndex]:
			break
		diffEnd=newLen+backIndex
	diffEnd=max(diffEnd,diffStart+(newLen-oldLen))
	print "diffStart %d, diffEnd %d"%(diffStart,diffEnd)
	return newComp[diffStart:diffEnd]

class InputCompositionTextInfo(OffsetsTextInfo):

	def _getSelectionOffsets(self):
		return self.obj.readingSelectionOffsets if self.obj.isReading else self.obj.compositionSelectionOffsets

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _getStoryText(self):
		return self.obj.readingString if self.obj.isReading else self.obj.compositionString

	def _getStoryLength(self):
		return len(self._getStoryText())

class InputComposition(EditableTextWithAutoSelectDetection,Window):

	TextInfo=InputCompositionTextInfo
	# Translators: The label for a 'composition' Window that appears when the user is typing one or more east-Asian characters into a document. 
	name=_("Composition")
	role=controlTypes.ROLE_EDITABLETEXT
	next=None
	previous=None
	firstChild=None
	lastChild=None
	states=set()
	location=None
	compositionString=""
	readingString=""
	compositionSelectionOffsets=(0,0)
	readingSelectionOffsets=(0,0)
	isReading=False

	def __init__(self,parent=None):
		self.parent=parent
		super(InputComposition,self).__init__(windowHandle=parent.windowHandle)

	def findOverlayClasses(self,clsList):
		clsList.append(InputComposition)
		clsList.append(InputComposition)
		return clsList

	def reportNewText(self,oldString,newString):
		if (config.conf["keyboard"]["speakTypedCharacters"] or config.conf["keyboard"]["speakTypedWords"]):
			newText=calculateInsertedChars(oldString.strip(u'\u3000'),newString.strip(u'\u3000'))
			if newText:
				queueHandler.queueFunction(queueHandler.eventQueue,speech.speakText,newText,symbolLevel=characterProcessing.SYMLVL_ALL)

	def compositionUpdate(self,compositionString,selectionStart,selectionEnd,isReading):
		if isReading and not config.conf["inputComposition"]["reportReadingStringChanges"]: return
		if not isReading and not config.conf["inputComposition"]["reportCompositionStringChanges"]: return
		self.reportNewText((self.readingString if isReading else self.compositionString),compositionString)
		hasChanged=False
		if isReading:
			self.readingString=compositionString
			self.readingSelectionOffsets=(selectionStart,selectionEnd)
			self.isReading=True
			hasChanged=True
		elif compositionString!=self.compositionString or (selectionStart,selectionEnd)!=self.compositionSelectionOffsets:
			self.readingString=""
			self.readingSelectionOffsets=(0,0)
			self.isReading=False
			self.compositionString=compositionString
			self.compositionSelectionOffsets=(selectionStart,selectionEnd)
			hasChanged=True
		if hasChanged:
			eventHandler.queueEvent("valueChange",self)
			eventHandler.queueEvent("caret",self)

	def reportFocus(self):
		pass

class CandidateList(Window):

	# Translators: The label for a 'candidate' list that shows a choice of symbols a user can choose from when typing east-Asian characters into a document.
	name=_("Candidate")
	role=controlTypes.ROLE_LIST
	next=None
	previous=None
	firstChild=None
	lastChild=None
	states=set()

	def __init__(self,parent=None):
		self.parent=parent
		super(CandidateList,self).__init__(windowHandle=parent.windowHandle)

	def findOverlayClasses(self,clsList):
		clsList.append(CandidateList)
		return clsList

class CandidateItem(CandidateItemBehavior,Window):

	role=controlTypes.ROLE_LISTITEM
	firstChild=None
	lastChild=None
	states=set()

	def __init__(self,parent=None,candidateStrings=[],candidateIndex=0):
		self.parent=parent
		self.candidateStrings=candidateStrings
		self.candidateIndex=candidateIndex
		super(CandidateItem,self).__init__(windowHandle=parent.windowHandle)

	def findOverlayClasses(self,clsList):
		clsList.append(CandidateItem)
		return clsList

	def _get_name(self):
		number=self.candidateIndex+1
		candidate=self.candidateStrings[self.candidateIndex]
		return self.getFormattedCandidateName(number,candidate)

	def _get_basicText(self):
		return self.candidateStrings[self.candidateIndex]

	def _get_description(self):
		candidate=self.candidateStrings[self.candidateIndex]
		return self.getFormattedCandidateDescription(candidate)

	def _get_next(self):
		if self.candidateIndex<(len(self.candidateStrings)-1):
			return CandidateItem(parent=self.parent,candidateStrings=self.candidateStrings,candidateIndex=self.candidateIndex+1)

	def _get_previous(self):
		if self.candidateIndex>0:
			return CandidateItem(parent=self.parent,candidateStrings=self.candidateStrings,candidateIndex=self.candidateIndex-1)
