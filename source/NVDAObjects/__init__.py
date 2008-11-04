#NVDAObjects/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module that contains the base NVDA object type"""
from new import instancemethod
import time
import re
import weakref
import eventHandler
import baseObject
import speech
from keyUtils import key, sendKey
from scriptHandler import isScriptWaiting
import globalVars
import api
import textHandler
import config
import controlTypes
import appModuleHandler
import virtualBufferHandler
import braille

class NVDAObjectTextInfo(textHandler.TextInfo):

	def __eq__(self,other):
		if self is other or (isinstance(other,NVDAObjectTextInfo) and self._startOffset==other._startOffset and self._endOffset==other._endOffset):
			return True
		else:
			return False

	def _getStoryText(self):
		return self.obj.basicText

	def _getStoryLength(self):
		return len(self._getStoryText())

	def _getTextLineLength(self):
		return self.obj.basicTextLineLength

	def _getCaretOffset(self):
		return self.obj.basicCaretOffset

	def _setCaretOffset(self,offset):
		self.obj.basicCaretOffset=offset

	def _getSelectionOffsets(self):
		return self.obj.basicSelectionOffsets

	def _setSelectionOffsets(self):
		self.obj.basicSelectionOffsets=(self._startOffset,self._endOffset)

	def _getTextRange(self,start,end):
		text=self._getStoryText()
		return text[start:end]

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		formatField=textHandler.FormatField()
		startOffset,endOffset=self._startOffset,self._endOffset
		if formatConfig["reportLineNumber"]:
			if calculateOffsets:
				startOffset,endOffset=self._getLineOffsets(offset)
			lineNum=self._getLineNumFromOffset(offset)
			if lineNum is not None:
				formatField["line-number"]=lineNum+1
		return formatField,(startOffset,endOffset)

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

	def _getParagraphOffsets(self,offset):
		return self._getLineOffsets(offset)

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

	def _getUnitOffsets(self,unit,offset):
		if unit==textHandler.UNIT_CHARACTER:
			offsetsFunc=self._getCharacterOffsets
		elif unit==textHandler.UNIT_WORD:
			offsetsFunc=self._getWordOffsets
		elif unit==textHandler.UNIT_LINE:
			offsetsFunc=self._getLineOffsets
		elif unit==textHandler.UNIT_SENTENCE:
			offsetsFunc=self._getSentenceOffsets
		elif unit==textHandler.UNIT_PARAGRAPH:
			offsetsFunc=self._getParagraphOffsets
		elif unit==textHandler.UNIT_READINGCHUNK:
			offsetsFunc=self._getReadingChunkOffsets
		else:
			raise ValueError("unknown unit: %s"%unit)
		return offsetsFunc(offset)

	def _getPointFromOffset(self,offset):
		raise NotImplementedError

	def _getOffsetFromPoint(self,x,y):
		raise NotImplementedError

	def __init__(self,obj,position):
		super(NVDAObjectTextInfo,self).__init__(obj,position)
		if isinstance(position,textHandler.Point):
			offset=self._getOffsetFromPoint(position.x,position.y)
			position=textHandler.Offsets(offset,offset)
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
		elif isinstance(position,textHandler.Offsets):
			self._startOffset=max(min(position.startOffset,self._getStoryLength()-1),0)
			self._endOffset=max(min(position.endOffset,self._getStoryLength()),0)
		else:
			raise NotImplementedError("position: %s not supported"%position)

	def _get_pointAtStart(self):
		return self._getPointFromOffset(self._startOffset)

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
		self._startOffset,self._endOffset=self._getUnitOffsets(unit,self._startOffset)

	def copy(self):
		o=self.__class__(self.obj,self.bookmark)
		for item in self.__dict__.keys():
			if item.startswith('_'):
				o.__dict__[item]=self.__dict__[item]
		return o

	def compareEndPoints(self,other,which):
		if which=="startToStart":
			diff=self._startOffset-other._startOffset
		elif which=="startToEnd":
			diff=self._startOffset-other._endOffset
		elif which=="endToStart":
			diff=self._endOffset-other._startOffset
		elif which=="endToEnd":
			diff=self._endOffset-other._endOffset
		else:
			raise ValueError("bad argument - which: %s"%which)
		if diff<0:
			diff=-1
		elif diff>0:
			diff=1
		return diff

	def setEndPoint(self,other,which):
		if which=="startToStart":
			self._startOffset=other._startOffset
		elif which=="startToEnd":
			self._startOffset=other._endOffset
		elif which=="endToStart":
			self._endOffset=other._startOffset
		elif which=="endToEnd":
			self._endOffset=other._endOffset
		else:
			raise ValueError("bad argument - which: %s"%which)

	def getInitialFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		return [self._getFormatFieldAndOffsets(self._startOffset,formatConfig,calculateOffsets=False)[0]]

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		if not formatConfig["detectFormatAfterCursor"]:
			return [self.text]
		commandList=[]
		offset=self._startOffset
		while offset<self._endOffset:
			field,(boundStart,boundEnd)=self._getFormatFieldAndOffsets(offset,formatConfig)
			if boundEnd<=boundStart:
				boundEnd=boundStart+1
			if boundEnd<=offset:
				boundEnd=offset+1
			if offset>self._startOffset:
				command=textHandler.FieldCommand("formatChange",field)
				commandList.append(command)
			text=self._getTextRange(offset,min(boundEnd,self._endOffset))
			commandList.append(text)
			offset=boundEnd
		return commandList

	def _get_text(self):
		return self._getTextRange(self._startOffset,self._endOffset)

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

	def move(self,unit,direction,endPoint=None):
		if direction==0:
			return 0;
		if endPoint=="end":
			offset=self._endOffset
		elif endPoint=="start":
			offset=self._startOffset
		else:
			self.collapse()
			offset=self._startOffset
		lastOffset=None
		count=0
		lowLimit=0
		highLimit=self._getStoryLength()
		while count!=direction and (lastOffset is None or (direction>0 and offset>lastOffset) or (direction<0 and offset<lastOffset)) and (offset<highLimit or direction<0) and (offset>lowLimit or direction>0):
			lastOffset=offset
			if direction<0 and offset>lowLimit:
				offset-=1
			newStart,newEnd=self._getUnitOffsets(unit,offset)
			if direction<0:
				offset=newStart
			elif direction>0:
				offset=newEnd
			count=count+1 if direction>0 else count-1
		if endPoint=="start":
			if (direction>0 and offset<=self._startOffset) or (direction<0 and offset>=self._startOffset) or offset<lowLimit or offset>=highLimit:
				return 0
			self._startOffset=offset
		elif endPoint=="end":
			if (direction>0 and offset<=self._endOffset) or (direction<0 and offset>=self._endOffset) or offset<lowLimit or offset>highLimit:
				return 0
			self._endOffset=offset
		else:
			if (direction>0 and offset<=self._startOffset) or (direction<0 and offset>=self._startOffset) or offset<lowLimit or offset>=highLimit:
				return 0
			self._startOffset=self._endOffset=offset
		if self._startOffset>self._endOffset:
			tempOffset=self._startOffset
			self._startOffset=self._endOffset
			self._endOffset=tempOffset
		return count

	def find(self,text,caseSensitive=False,reverse=False):
		if reverse:
			# When searching in reverse, we reverse both strings and do a forwards search.
			text = text[::-1]
			# Start searching one before the start to avoid finding the current match.
			inText=self._getTextRange(0,self._startOffset)[::-1]
		else:
			# Start searching one past the start to avoid finding the current match.
			inText=self._getTextRange(self._startOffset+1,self._getStoryLength())
		m=re.search(re.escape(text),inText,re.IGNORECASE)
		if not m:
			return False
		if reverse:
			offset=self._startOffset-m.end()
		else:
			offset=self._startOffset+1+m.start()
		self._startOffset=self._endOffset=offset
		return True

	def updateCaret(self):
		return self._setCaretOffset(self._startOffset)

	def updateSelection(self):
		return self._setSelectionOffsets(self._startOffset,self._endOffset)

	def _get_bookmark(self):
		return textHandler.Offsets(self._startOffset,self._endOffset)

class NVDAObject(baseObject.ScriptableObject):
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
@type states: set
@ivar description: The object's description. (e.g. Further info to describe the button's action to go with the label) 
@type description: string
@ivar positionString: a description of where the object is in relation to other objects around it. (e.g. a list item might say 2 of 5).
@type positionString: string
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
@ivar text_characterCount: the number of characters in this object's text
@type text_characterCount: int
@ivar _text_lastReportedPresentation: a dictionary to store all the last reported attribute values such as font, page number, table position etc.
@type _text_lastReportedPresentation: dict
"""

	def __init__(self):
		self._mouseEntered=None
		self.textRepresentationLineLength=None #Use \r and or \n
		self.TextInfo=NVDAObjectTextInfo
		if hasattr(self.appModule,'event_NVDAObject_init'):
			self.appModule.event_NVDAObject_init(self)

	def _isEqual(self,other):
		return True
 
	def __eq__(self,other):
		return self is other or self._isEqual(other)
 
	def __ne__(self,other):
		return not self.__eq__(other)

	def _get_virtualBuffer(self):
		if hasattr(self,'_virtualBuffer'):
			v=self._virtualBuffer
			if isinstance(v,weakref.ref):
				v=v()
			if v and v in virtualBufferHandler.runningTable:
				return v
			else:
				self._virtualBuffer=None
				return None
		else:
			v=virtualBufferHandler.getVirtualBuffer(self)
			if v:
				self._virtualBuffer=weakref.ref(v)
			return v

	def _set_virtualBuffer(self,obj):
		if obj:
			self._virtualBuffer=weakref.ref(obj)
		else: #We can't point a weakref to None, so just set the private variable to None, it can handle that
			self._virtualBuffer=None





	def _get_appModule(self):
		if not hasattr(self,'_appModuleRef'):
			a=appModuleHandler.getAppModuleForNVDAObject(self)
			if a:
				self._appModuleRef=weakref.ref(a)
				return a
		else:
			return self._appModuleRef()

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
		return set()

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

	def scrollIntoView(self):
		"""Scroll this object into view on the screen if possible.
		"""

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
		if not self._mouseEntered and config.conf['mouse']['reportObjectRoleOnMouseEnter']:
			speech.cancelSpeech()
			speech.speakObjectProperties(self,role=True)
			speechWasCanceled=True
		else:
			speechWasCanceled=False
		self._mouseEntered=True
		if not config.conf['mouse']['reportTextUnderMouse']:
			return
		try:
			info=self.makeTextInfo(textHandler.Point(x,y))
			info.expand(config.conf["mouse"]["mouseTextUnit"])
		except:
			info=self.makeTextInfo(textHandler.POSITION_ALL)
		oldInfo=getattr(self,'_lastMouseTextInfoObject',None)
		self._lastMouseTextInfoObject=info
		if not oldInfo or info.compareEndPoints(oldInfo,"startToStart")!=0 or info.compareEndPoints(oldInfo,"endToEnd")!=0:
			text=info.text
			notBlank=False
			if text:
				for ch in text:
					if not ch.isspace() and ch!=u'\ufffc':
						notBlank=True
			if notBlank:
				if not speechWasCanceled:
					speech.cancelSpeech()
				speech.speakText(text)

	def event_stateChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self,states=True, reason=speech.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_focusEntered(self):
		speech.speakObjectProperties(self,name=True,role=True,description=True,reason=speech.REASON_FOCUS)

	def event_gainFocus(self):
		"""
This code is executed if a gain focus event is received by this object.
"""
		api.setNavigatorObject(self)
		self.reportFocus()
		braille.handler.handleGainFocus(self)

	def event_foreground(self):
		"""
This method will speak the object if L{speakOnForeground} is true and this object has just become the current foreground object.
"""
		speech.cancelSpeech()
		api.setNavigatorObject(self)
		speech.speakObjectProperties(self,name=True,role=True,description=True,reason=speech.REASON_FOCUS)

	def event_valueChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, value=True, reason=speech.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_nameChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, name=True, reason=speech.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_descriptionChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, description=True, reason=speech.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_caret(self):
		if self is api.getFocusObject():
			braille.handler.handleCaretMove(self)

	def _get_basicText(self):
		newTime=time.time()
		oldTime=getattr(self,'_basicTextTime',0)
		if newTime-oldTime>0.5:
			self._basicText=" ".join([x for x in self.name, self.value, self.description if isinstance(x, basestring) and len(x) > 0 and not x.isspace()])
			if len(self._basicText)==0:
				self._basicText="\n"
		else:
			self._basicTextTime=newTime
		return self._basicText

	def _get_basicTextLineLength(self):
		return None

	def _get_basicCaretOffset(self):
		raise NotImplementedError

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

	def _hasCaretMoved(self, bookmark, retryInterval=0.01, timeout=0.03):
		elapsed = 0
		while elapsed < timeout:
			if isScriptWaiting():
				return False
			api.processPendingEvents(processEventQueue=False)
			if eventHandler.isPendingEvents("gainFocus"):
				oldInCaretMovement=globalVars.inCaretMovement
				globalVars.inCaretMovement=True
				try:
					api.processPendingEvents()
				finally:
					globalVars.inCaretMovement=oldInCaretMovement
				return True
			#The caret may stop working as the focus jumps, we want to stay in the while loop though
			try:
				newBookmark = self.makeTextInfo(textHandler.POSITION_CARET).bookmark
				if newBookmark!=bookmark:
					return True
			except:
				pass
			time.sleep(retryInterval)
			elapsed += retryInterval
		return False

	def script_moveByLine(self,keyPress):
		try:
			info=self.makeTextInfo(textHandler.POSITION_CARET)
		except:
			sendKey(keyPress)
			return
		bookmark=info.bookmark
		sendKey(keyPress)
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, keyPress=keyPress)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textHandler.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textHandler.UNIT_LINE)
			speech.speakTextInfo(info)

	def script_moveByCharacter(self,keyPress):
		try:
			info=self.makeTextInfo(textHandler.POSITION_CARET)
		except:
			sendKey(keyPress)
			return
		bookmark=info.bookmark
		sendKey(keyPress)
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, keyPress=keyPress)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textHandler.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textHandler.UNIT_CHARACTER)
			speech.speakTextInfo(info,handleSymbols=True,extraDetail=True)

	def script_moveByWord(self,keyPress):
		try:
			info=self.makeTextInfo(textHandler.POSITION_CARET)
		except:
			sendKey(keyPress)
			return
		bookmark=info.bookmark
		sendKey(keyPress)
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, keyPress=keyPress)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textHandler.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textHandler.UNIT_WORD)
			speech.speakTextInfo(info,extraDetail=True,handleSymbols=True)

	def script_moveByParagraph(self,keyPress):
		try:
			info=self.makeTextInfo(textHandler.POSITION_CARET)
		except:
			sendKey(keyPress)
			return
		bookmark=info.bookmark
		sendKey(keyPress)
		if not self._hasCaretMoved(bookmark):
			eventHandler.executeEvent("caretMovementFailed", self, keyPress=keyPress)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textHandler.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textHandler.UNIT_PARAGRAPH)
			speech.speakTextInfo(info)

	def script_backspace(self,keyPress):
		try:
			oldInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		except:
			sendKey(keyPress)
			return
		oldBookmark=oldInfo.bookmark
		testInfo=oldInfo.copy()
		res=testInfo.move(textHandler.UNIT_CHARACTER,-1)
		if res<0:
			testInfo.expand(textHandler.UNIT_CHARACTER)
			delChar=testInfo.text
		else:
			delChar=""
		sendKey(keyPress)
		if self._hasCaretMoved(oldBookmark):
			speech.speakSpelling(delChar)
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textHandler.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info)

	def script_delete(self,keyPress):
		try:
			info=self.makeTextInfo(textHandler.POSITION_CARET)
		except:
			sendKey(keyPress)
			return
		bookmark=info.bookmark
		sendKey(keyPress)
		# We'll try waiting for the caret to move, but we don't care if it doesn't.
		self._hasCaretMoved(bookmark)
		if not isScriptWaiting():
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textHandler.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textHandler.UNIT_CHARACTER)
			speech.speakTextInfo(info,handleSymbols=True)

	def script_changeSelection(self,keyPress):
		try:
			oldInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		except:
			sendKey(keyPress)
			return
		sendKey(keyPress)
		if not isScriptWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			try:
				newInfo=focus.makeTextInfo(textHandler.POSITION_SELECTION)
			except:
				return
			speech.speakSelectionChange(oldInfo,newInfo)

class AutoSelectDetectionNVDAObject(NVDAObject):

	"""Provides an NVDAObject with the means to detect if the text selection has changed, and if so to announce the change
	@ivar hasContentChangedSinceLastSelection: if True then the content has changed.
	@ivar hasContentChangedSinceLastSelection: boolean
	"""

	def initAutoSelectDetection(self):
		"""Initializes the autoSelect detection code so that it knows about what is currently selected."""
		try:
			self._lastSelectionPos=self.makeTextInfo(textHandler.POSITION_SELECTION)
		except:
			self._lastSelectionPos=None
		self.hasContentChangedSinceLastSelection=False

	def detectPossibleSelectionChange(self):
		"""Detects if the selection has been changed, and if so it speaks the change."""
		oldInfo=getattr(self,'_lastSelectionPos',None)
		if not oldInfo:
			return
		try:
			newInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		except:
			self._lastSelectionPos=None
			return
		self._lastSelectionPos=newInfo.copy()
		hasContentChanged=self.hasContentChangedSinceLastSelection
		self.hasContentChangedSinceLastSelection=False
		if hasContentChanged:
			generalize=True
		else:
			generalize=False
		speech.speakSelectionChange(oldInfo,newInfo,generalize=generalize)
