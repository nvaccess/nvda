#NVDAObjects/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module that contains the base NVDA object type"""
from new import instancemethod
import time
import baseObject
import debug
import speech
from keyUtils import key, sendKey, isKeyWaiting
import globalVars
import api
import textHandler
import config
import controlTypes
import baseObject

class NVDAObjectTextInfo(textHandler.TextInfo):

	def __eq__(self,other):
		if id(self)==id(other) or (isinstance(other,NVDAObjectTextInfo) and self._startOffset==other._startOffset and self._endOffset==other._endOffset):
			return True
		else:
			return False

	def _getStoryText(self):
		if not hasattr(self,'_storyText'):
			self._storyText=self.obj.basicText
		return self._storyText

	def _getStoryLength(self):
		if not hasattr(self,'_storyLength'):
			self._storyLength=len(self._getStoryText())
		return self._storyLength

	def _getTextLineLength(self):
		if not hasattr(self,'_textLineLength'):
			self._textLineLength=self.obj.basicTextLineLength
		return self._textLineLength

	def _getCaretOffset(self):
		return self.obj.basicCaretOffset

	def _setCaretOffset(self,offset):
		self.obj.basicCaretOffset=offset

	def _getSelectionOffsets(self):
		return self.obj.basicSelectionOffsets

	def _setSelectionOffsets(self):
		self.obj.basicSelectionOffsets=(self._startOffset,self._endOffset)

	def _getTextRange(self,start,end):
		if hasattr(self,'_text'):
			return self._text[start:end]
		else:
			self._text=self._getStoryText()
			return self._text[start:end]

	def _getCharacterOffsets(self,offset):
		return [offset,offset+1]

	def _getWordOffsets(self,offset):
		lineStart,lineEnd=self._getLineOffsets(offset)
		lineText=self._getTextRange(lineStart,lineEnd)
		start=textHandler.findStartOfWord(lineText,offset-lineStart)+lineStart
		end=textHandler.findEndOfWord(lineText,offset-lineStart)+lineStart
		return [start,end]

	def _getLineCount(self):
		lineLength=self._getTextLineLength()
		if lineLength:
			storyLength=self._getStoryLength()
			return storyLength/lineLength
		else:
			return -1

	def _getLineNumFromOffset(self,offset):
		lineLength=self._getTextLineLength()
		if lineLength:
			return offset/lineLength
		else:
			return -1

	def _getLineOffsets(self,offset):
		storyText=self._getStoryText()
		lineLength=self._getTextLineLength()
		start=textHandler.findStartOfLine(storyText,offset,lineLength=lineLength)
		end=textHandler.findEndOfLine(storyText,offset,lineLength=lineLength)
		return [start,end]

	def _getSentenceOffsets(self,offset):
		return self._getLineOffsets(offset)

	_getParagraphOffsets=_getLineOffsets

	def _getFormatAndOffsets(self,offset,includes=set(),excludes=set()):
		end=offset+1
		formats=[]
		if textHandler.isFormatEnabled(controlTypes.ROLE_LINE,includes=includes,excludes=excludes):
			lineNum=self._getLineNumFromOffset(offset)
			if lineNum>=0:
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_CHANGE,textHandler.Format(controlTypes.ROLE_LINE,value=str(lineNum+1)))
				formats.append(f)
				lineStart,end=self._getLineOffsets(offset)
		return (formats,offset,end)

	def _getReadingChunkOffsets(self,offset):
		return self._getSentenceOffsets(offset)

	def __init__(self,obj,position):
		super(NVDAObjectTextInfo,self).__init__(obj,position)
		if position==textHandler.POSITION_FIRST:
			self._startOffset=self._endOffset=0
		elif position==textHandler.POSITION_LAST:
			self._startOffset=self._endOffset=self._getStoryLength()-1
		elif position==textHandler.POSITION_CARET:
			self._startOffset=self._endOffset=self._getCaretOffset()
		elif position==textHandler.POSITION_SELECTION:
			(self._startOffset,self._endOffset)=self._getSelectionOffsets()
		elif position==textHandler.POSITION_ALL:
			self._startOffset=0
			self._endOffset=self._getStoryLength()
		elif isinstance(position,textHandler.Bookmark):
			if position.infoClass==self.__class__:
				(self._startOffset,self._endOffset)=position.data
			else:
				raise TypeError("Bookmark was for %s type, not for %s type"%(position.infoClass.__name__,self.__class__.__name__))
		else:
			raise NotImplementedError("position: %s not supported"%position)

	def _get_isCollapsed(self):
		if self._startOffset==self._endOffset:
			return True
		else:
			return False

	def collapse(self,end=False):
		if not end:
			self._endOffset=self._startOffset
		else:
			self._startOffset=self._endOffset

	def expand(self,unit):
		if unit==textHandler.UNIT_CHARACTER:
			(self._startOffset,self._endOffset)=self._getCharacterOffsets(self._startOffset)
		elif unit==textHandler.UNIT_WORD:
				(self._startOffset,self._endOffset)=self._getWordOffsets(self._startOffset)
		elif unit==textHandler.UNIT_LINE:
			(self._startOffset,self._endOffset)=self._getLineOffsets(self._startOffset)
		elif unit==textHandler.UNIT_SENTENCE:
			(self._startOffset,self._endOffset)=self._getSentenceOffsets(self._startOffset)
		elif unit==textHandler.UNIT_PARAGRAPH:
			(self._startOffset,self._endOffset)=self._getParagraphOffsets(self._startOffset)
		elif unit==textHandler.UNIT_STORY:
			self._startOffset=0
			self._endOffset=self._getStoryLength()
		elif unit==textHandler.UNIT_READINGCHUNK:
			(self._startOffset,self._endOffset)=self._getReadingChunkOffsets(self._startOffset)
		elif unit is not None:
			raise NotImplementedError("unit: %s not supported"%unit)

	def copy(self):
		o=self.__class__(self.obj,self.bookmark)
		for item in self.__dict__.keys():
			if item.startswith('_'):
				o.__dict__[item]=self.__dict__[item]
		return o

	def compareStart(self,info):
		return self._startOffset-info._startOffset

	def compareEnd(self,info):
		return self._endOffset-info._endOffset

	def _get_text(self):
		return self._getTextRange(self._startOffset,self._endOffset)

	def getFormattedText(self,searchRange=False,includes=set(),excludes=set()):
		if not searchRange:
			formats,start,end=self._getFormatAndOffsets(self._startOffset,includes=includes,excludes=excludes)
			formats.append(self.text)
			return formats
		lastFormatKeys={}
		l=[]
		finnished=False
		offset=self._startOffset
		while not finnished:
			curFormatKeys={}
			formats,start,end=self._getFormatAndOffsets(offset,includes=includes,excludes=excludes)
			for item in formats:
				itemKey="%d, %d, %s, %s"%(item.cmd,item.format.role,item.format.value,item.format.uniqueID)
				if itemKey not in lastFormatKeys:
					l.append(item)
				curFormatKeys[itemKey]=item
			for itemKey,item in lastFormatKeys.items():
				if item.cmd==textHandler.FORMAT_CMD_SWITCHON and itemKey not in curFormatKeys:
					l.append(textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHOFF,item.format))
			text=self._getTextRange(start,end)
			if len(l)>0 and isinstance(l[-1],basestring):
				text="%s%s"%(l[-1],text)
				del l[-1]
			l.append(text)
			lastFormatKeys=curFormatKeys
			offset=end
			if end>=self._endOffset:
				finnished=True
		return l

	def unitIndex(self,unit):
		if unit==textHandler.UNIT_LINE:  
			return self._lineNumFromOffset(self._startOffset)
		else:
			raise NotImplementedError

	def unitCount(self,unit):
		if unit==textHandler.UNIT_LINE:
			return self._getLineCount()
		else:
			raise NotImplementedError

	def moveByUnit(self,unit,num,start=True,end=True):
		oldStart=self._startOffset
		oldEnd=self._endOffset
		lowLimit=0
		highLimit=self._getStoryLength()
		count=0
		if num<0:
			while self._startOffset>lowLimit and count>num:
				self._startOffset-=1
				self.expand(unit)
				self.collapse()
				count-=1
 		elif num>0:
			while self._startOffset<highLimit and count<num:
				lastStart=self._startOffset
				lastEnd=self._endOffset
				self.expand(unit)
				self.collapse(end=True)
				count+=1
				if start and self._startOffset>=highLimit:
					count-=1
					self._startOffset=self._endOffset=lastStart
					break
		if start==False:
			self._startOffset=oldStart
		if end==False:
			self._endOffset=oldEnd
		return count

	def updateCaret(self):
		return self._setCaretOffset(self._startOffset)

	def updateSelection(self):
		return self._setSelectionOffsets(self._startOffset,self._endOffset)

	def _get_bookmark(self):
		return textHandler.Bookmark(self.__class__,(self._startOffset,self._endOffset))

class NVDAObject(baseObject.scriptableObject):
	"""
The baseType NVDA object. All other NVDA objects are based on this one.
@ivar _hashLimit: The limit in size for a hash of this object
@type _hashLimit: int
@ivar _hashPrime: the prime number used in calculating this object's hash
@type _hashPrime: int
@ivar _keyMap: A dictionary that stores key:method  key to script mappings. 
@type _keyMap: dict
@ivar name: The objects name or label. (e.g. the text of a list item, label of a button)
@type name: string
@ivar value: the object's value. (e.g. content of an edit field, percentage on a progresss bar)
@type value: string
@ivar role: The object's chosen role. (NVDA uses the set of IAccessible role constants for roles, however sometimes if there is no suitable role, this can be a string)
@type role: int or string
@ivar states: The object's states. (NVDA uses state constants for its states)
@type states: frozenset
@ivar description: The object's description. (e.g. Further info to describe the button's action to go with the label) 
@type description: string
@ivar positionString: a description of where the object is in relation to other objects around it. (e.g. a list item might say 2 of 5).
@type positionString: string
@ivar level: the object's level. Example: a tree view item has a level of 5
@type level: int
@ivar contains: a description of the object's content. Example: a tree view item contains '4 items'
@type contains: string
@ivar location: The object's location. (A tuple of left, top, width, depth).
@type location: 4-tuple (int)
@ivar next: gets the next logical NVDA object in the tree
@type next: L{NVDAObject}
@ivar previous: gets the previous logical NVDA object in the tree
@type previous: L{NVDAObject}
@ivar parent: gets the parent NVDA object to this one in the tree 
@type parent: L{NVDAObject}
@ivar firstChild: gets the first child NVDA object to this one in the tree 
@type firstChild: L{NVDAObject}
@ivar children: gets a list of child NVDA objects directly under this one in the tree
@type children: list of L{NVDAObject}
@ivar childCount: The number of child NVDA objects under this one in the tree
@type childCount: int
@ivar hasFocus: if true then the object believes it has focus
@type hasFocus: boolean 
@ivar isProtected: if true then this object should be treeted like a password field.
@type isProtected: boolean 
@ivar text_caretPosition: the caret position in this object's text as an offset from 0
@type text_caretPosition: int
@ivar text_reviewPosition: the review cursor's position in the object's text as an offset from 0
@type text_reviewPosition: int
@ivar text_characterCount: the number of characters in this object's text
@type text_characterCount: int
@ivar _text_lastReportedPresentation: a dictionary to store all the last reported attribute values such as font, page number, table position etc.
@type _text_lastReportedPresentation: dict
"""

	def __init__(self):
		self._oldValue=None
		self._oldStates=self.states
		self._oldName=None
		self._oldDescription=None
		self._mouseEntered=None
		self.textRepresentationLineLength=None #Use \r and or \n
		if not hasattr(self,'TextInfo'):
			self.TextInfo=NVDAObjectTextInfo
			self.reviewPosition=self.makeTextInfo(textHandler.POSITION_CARET)

	def _isEqual(self,other):
		return True
 
	def __eq__(self,other):
		return self is other or self._isEqual(other)
 
	def __ne__(self,other):
		return not self.__eq__(other)

	def getScript(self,keyPress):
		"""
Returns a script (instance method) if one is assigned to the keyPress given.
@param keyPress: The key you wish to retreave the script for
@type keyPress: key
""" 
		if self._keyMap.has_key(keyPress):
			return instancemethod(self._keyMap[keyPress],self,self.__class__)

	def _get_name(self):
		return None

	def _get_role(self):
		return controlTypes.ROLE_UNKNOWN

	def _get_value(self):
		return None

	def _get_description(self):
		return None

	def _get_actionStrings(self):
		return []

	def doAction(self,index):
		return

	def _get_groupName(self):
		focus=api.getFocusObject()
		foreground=api.getForegroundObject()
		if self!=focus or foreground.role!=controlTypes.ROLE_DIALOG: 
			return None
		try:
			curLocation=self.location
			groupObjA=groupObjB=self
			groupObj=None
			while not groupObj and (groupObjA or groupObjB):
				groupObjA=groupObjA.previous
				groupObjB=groupObjB.parent
				if groupObjA and groupObjA.role==controlTypes.ROLE_GROUPING:
					groupObj=groupObjA
					continue
				if groupObjB and groupObjB.role==controlTypes.ROLE_GROUPING:
					groupObj=groupObjB
					continue
			if groupObj:
				groupLocation=groupObj.location
				if curLocation and groupLocation and (curLocation[0]>=groupLocation[0]) and (curLocation[1]>=groupLocation[1]) and ((curLocation[0]+curLocation[2])<=(groupLocation[0]+groupLocation[2])) and ((curLocation[1]+curLocation[3])<=(groupLocation[1]+groupLocation[3])):
					name=groupObj.name
					return name
			return None
		except:
			return None

	def _get_keyboardShortcut(self):
		return None

	def _get_states(self):
		return frozenset()

	def _get_level(self):
		return None

	def _get_contains(self):
		return None

	def _get_location(self):
		return (0,0,0,0)

	def _get_parent(self):
		return None

	def _get_next(self):
		return None

	def _get_previous(self):
		return None

	def _get_firstChild(self):
		return None

	def _get_lastChild(self):
		return None

	def _get_children(self):
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children

	def getNextInFlow(self,down=None,up=None):
		"""Retreaves the next object in depth first tree traversal order
@param up: a list that all objects that we moved up out of will be placed in
@type up: list
@param down: a list which all objects we moved down in to will be placed
@type down: list
"""
		child=self.firstChild
		if child:
			if isinstance(down,list):
				down.append(self)
			return child
		next=self.next
		if next:
			return next
		parent=self.parent
		while not next and parent:
			next=parent.next
			if isinstance(up,list):
				up.append(parent)
			parent=parent.parent
		return next

	_get_nextInFlow=getNextInFlow

	def getPreviousInFlow(self,down=None,up=None):
		"""Retreaves the previous object in depth first tree traversal order
@param up: a list that all objects that we moved up out of will be placed in
@type up: list
@param down: a list which all objects we moved down in to will be placed
@type down: list
"""
		prev=self.previous
		if prev:
			lastLastChild=prev
			lastChild=prev.lastChild
			while lastChild:
				if isinstance(down,list):
					down.append(lastLastChild)
				lastLastChild=lastChild
				lastChild=lastChild.lastChild
			return lastLastChild
		parent=self.parent
		if parent:
			if isinstance(up,list):
				up.append(self)
			return parent

	_get_previousInFlow=getPreviousInFlow

	def _get_childCount(self):
		return len(self.children)

	def doDefaultAction(self):
		"""
Performs the default action on this object. (e.g. clicks a button)
"""
		pass

	def _get_activeChild(self):
		return None

	def _get_hasFocus(self):
		"""
Returns true of this object has focus, false otherwise.
"""
		return False

	def setFocus(self):
		"""
Tries to force this object to take the focus.
"""
		pass

	def _get_labeledBy(self):
		return None

	def _get_positionString(self):
		return None

	def _get_isProtected(self):
		return False


	def _get_statusBar(self):
		return None

	def speakDescendantObjects(self,hashList=None):
		if hashList is None:
			hashList=[]
		for child in self.children:
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				speech.speakObject(child)
				child.speakDescendantObjects(hashList=hashList)

	def reportFocus(self):
		speech.speakObject(self,reason=speech.REASON_FOCUS)

	def event_mouseMove(self,x,y):
		if not self._mouseEntered:
			speech.cancelSpeech()
			speech.speakObject(self,reason=speech.REASON_MOUSE)
		self._mouseEntered=True




	def event_stateChange(self):
		if id(self)==id(api.getFocusObject()):
			states=self.states
			if states!=self._oldStates:
				speech.speakObjectProperties(self,states=True, reason=speech.REASON_CHANGE)
				self._oldStates=states

	def event_focusEntered(self):
		speech.speakObject(self,reason=speech.REASON_FOCUS)

	def event_gainFocus(self):
		"""
This code is executed if a gain focus event is received by this object.
"""
		api.setNavigatorObject(self)
		self.reportFocus()

	def event_foreground(self):
		"""
This method will speak the object if L{speakOnForeground} is true and this object has just become the current foreground object.
"""
		speech.cancelSpeech()
		api.setNavigatorObject(self)
		speech.speakObject(self,reason=speech.REASON_FOCUS)

	def event_valueChange(self):
		value=self.value
		if id(self)==id(api.getFocusObject()) and value!=self._oldValue:
			speech.speakObjectProperties(self, value=True, reason=speech.REASON_CHANGE)
			self._oldValue=value

	def event_nameChange(self):
		name=self.name
		if id(self)==id(api.getFocusObject()) and name!=self._oldName:
			speech.speakObjectProperties(self, name=True, reason=speech.REASON_CHANGE)
			self._oldName=name

	def event_descriptionChange(self):
		description=self.description
		if id(self)==id(api.getFocusObject()) and description!=self._oldDescription:
			speech.speakObjectProperties(self, description=True, reason=speech.REASON_CHANGE)
			self._oldDescription=description

	def _get_basicText(self):
		basicText=" ".join([x for x in self.name, self.value, self.description if isinstance(x, basestring) and len(x) > 0 and not x.isspace()])
		if len(basicText)==0:
			basicText="\n"
		return basicText

	def _get_basicTextLineLength(self):
		return None

	def _get_basicCaretOffset(self):
		return 0

	def _set_basicCaretOffset(self,offset):
		pass

	def _get_basicSelectionOffsets(self):
		return [0,0]

	def _set_basicSelectionOffsets(self):
		pass

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)
	def setCaret(self,info):
		pass


	def script_review_top(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_FIRST)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_LINE)
		speech.speakMessage(_("top"))
		speech.speakFormattedText(info)

	def script_review_previousLine(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_LINE)
		info.collapse()
		res=info.moveByUnit(textHandler.UNIT_LINE,-1)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_LINE)
		if res==0:
			speech.speakMessage(_("top"))
		speech.speakFormattedText(info)

	def script_review_currentLine(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_LINE)
		speech.speakFormattedText(info)

	def script_review_nextLine(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_LINE)
		info.collapse()
		res=info.moveByUnit(textHandler.UNIT_LINE,1)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_LINE)
		if res==0:
			speech.speakMessage(_("bottom"))
		speech.speakFormattedText(info)

	def script_review_bottom(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_LAST)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_LINE)
		speech.speakMessage(_("bottom"))
		speech.speakFormattedText(info)

	def script_review_previousWord(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_WORD)
		info.collapse()
		res=info.moveByUnit(textHandler.UNIT_WORD,-1)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_WORD)
		if res==0:
			speech.speakMessage(_("top"))
		speech.speakFormattedText(info)

	def script_review_currentWord(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_WORD)
		speech.speakFormattedText(info)

	def script_review_nextWord(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_WORD)
		info.collapse()
		res=info.moveByUnit(textHandler.UNIT_WORD,1)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_WORD)
		if res==0:
			speech.speakMessage(_("bottom"))
		speech.speakFormattedText(info)

	def script_review_startOfLine(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_LINE)
		info.collapse()
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_CHARACTER)
		speech.speakMessage(_("left"))
		speech.speakFormattedText(info,handleSymbols=True)

	def script_review_previousCharacter(self,keyPress,nextScript):
		lineInfo=self.reviewPosition.copy()
		lineInfo.expand(textHandler.UNIT_LINE)
		charInfo=self.reviewPosition.copy()
		charInfo.expand(textHandler.UNIT_CHARACTER)
		charInfo.collapse()
		res=charInfo.moveByUnit(textHandler.UNIT_CHARACTER,-1)
		if res==0 or charInfo.compareStart(lineInfo)<0:
			speech.speakMessage(_("left"))
			reviewInfo=self.reviewPosition.copy()
			reviewInfo.expand(textHandler.UNIT_CHARACTER)
			speech.speakSymbol(reviewInfo.text)
		else:
			self.reviewPosition=charInfo.copy()
			charInfo.expand(textHandler.UNIT_CHARACTER)
			speech.speakFormattedText(charInfo,handleSymbols=True)

	def script_review_currentCharacter(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_CHARACTER)
		speech.speakFormattedText(info,handleSymbols=True)

	def script_review_nextCharacter(self,keyPress,nextScript):
		lineInfo=self.reviewPosition.copy()
		lineInfo.expand(textHandler.UNIT_LINE)
		charInfo=self.reviewPosition.copy()
		charInfo.expand(textHandler.UNIT_CHARACTER)
		charInfo.collapse()
		res=charInfo.moveByUnit(textHandler.UNIT_CHARACTER,1)
		if res==0 or charInfo.compareEnd(lineInfo)>=0:
			speech.speakMessage(_("right"))
			reviewInfo=self.reviewPosition.copy()
			reviewInfo.expand(textHandler.UNIT_CHARACTER)
			speech.speakSymbol(reviewInfo.text)
		else:
			self.reviewPosition=charInfo.copy()
			charInfo.expand(textHandler.UNIT_CHARACTER)
			speech.speakFormattedText(charInfo,handleSymbols=True)

	def script_review_endOfLine(self,keyPress,nextScript):
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_LINE)
		info.collapse(end=True)
		info.moveByUnit(textHandler.UNIT_CHARACTER,-1)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_CHARACTER)
		speech.speakMessage(_("right"))
		speech.speakFormattedText(info,handleSymbols=True)

	def script_review_moveToCaret(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		self.reviewPosition=info.copy()
		info.expand(textHandler.UNIT_LINE)
		speech.speakFormattedText(info)

	def script_review_moveCaretHere(self,keyPress,nextScript):
		self.reviewPosition.updateCaret()
		info=self.reviewPosition.copy()
		info.expand(textHandler.UNIT_LINE)
		speech.speakFormattedText(info)

	def script_moveByLine(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			info=focus.makeTextInfo(textHandler.POSITION_CARET)
			if globalVars.caretMovesReviewCursor:
				focus.reviewPosition=info.copy()
			info.expand(textHandler.UNIT_LINE)
			speech.speakFormattedText(info)

	def script_moveByCharacter(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			info=focus.makeTextInfo(textHandler.POSITION_CARET)
			if globalVars.caretMovesReviewCursor:
				focus.reviewPosition=info.copy()
			info.expand(textHandler.UNIT_CHARACTER)
			speech.speakFormattedText(info,handleSymbols=True)

	def script_moveByWord(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			info=focus.makeTextInfo(textHandler.POSITION_CARET)
			if globalVars.caretMovesReviewCursor:
				focus.reviewPosition=info.copy()
			info.expand(textHandler.UNIT_WORD)
			speech.speakFormattedText(info)

	def script_moveByParagraph(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			info=focus.makeTextInfo(textHandler.POSITION_CARET)
			if globalVars.caretMovesReviewCursor:
				focus.reviewPosition=info.copy()
			info.expand(textHandler.UNIT_PARAGRAPH)
			speech.speakFormattedText(info)

	def script_backspace(self,keyPress,nextScript):
		oldInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		testInfo=oldInfo.copy()
		res=testInfo.moveByUnit(textHandler.UNIT_CHARACTER,-1)
		if res<0:
			testInfo.expand(textHandler.UNIT_CHARACTER)
			delChar=testInfo.text
		else:
			delChar=""
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			newInfo=focus.makeTextInfo(textHandler.POSITION_CARET)
			if res<0 and newInfo.compareStart(testInfo)==0:
				speech.speakSymbol(delChar)
			if globalVars.caretMovesReviewCursor:
				focus.reviewPosition=newInfo

	def script_delete(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			info=focus.makeTextInfo(textHandler.POSITION_CARET)
			if globalVars.caretMovesReviewCursor:
				focus.reviewPosition=info.copy()
			info.expand(textHandler.UNIT_CHARACTER)
			speech.speakFormattedText(info,handleSymbols=True)

	def script_changeSelection(self,keyPress,nextScript):
		oldInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			newInfo=focus.makeTextInfo(textHandler.POSITION_SELECTION)
			speech.speakSelectionChange(oldInfo,newInfo)
