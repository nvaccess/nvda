#NVDAObjects/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module that contains the base NVDA object type"""
from new import instancemethod
import baseObject
import debug
import speech
from keyUtils import key, sendKey, isKeyWaiting
import globalVars
import api
import text
import config
import controlTypes
import baseObject

class NVDAObjectTextInfo(text.TextInfo):

	def __init__(self,obj,position,expandToUnit=None,limitToUnit=None,_text=None):
		super(NVDAObjectTextInfo,self).__init__(obj,position,expandToUnit,limitToUnit)
		#cache the text of the object, either from a parameter, or get it from the object
		if _text is not None:
			self._text=_text
		else:
			self._text=self.obj.textRepresentation
			if not self._text:
				self._text="\0"
		#Translate the position in to offsets and cache it
		if position==text.POSITION_FIRST:
			self._startOffset=self._endOffset=0
		elif position==text.POSITION_LAST:
			self._startOffset=self._endOffset=len(self._text)-1
		elif position==text.POSITION_CARET:
			self._startOffset=self._endOffset=obj.caretOffset
		elif position==text.POSITION_SELECTION:
			(self._startOffset,self._endOffset)=obj.selectionOffsets
		elif isinstance(position,text.OffsetPosition):
			self._startOffset=self._endOffset=position.offset
		elif isinstance(position,text.OffsetsPosition):
			self._startOffset=position.start
			self._endOffset=position.end
		else:
			raise NotImplementedError("position: %s not supported"%position)
		#Set the start and end offsets from expanding position to a unit 
		if expandToUnit is text.UNIT_CHARACTER:
			self._startOffset=self._startOffset
			self._endOffset=self.startOffset+1
		elif expandToUnit is text.UNIT_WORD:
			self._startOffset=text.findStartOfWord(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength) 
			self._endOffset=text.findEndOfWord(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength)
		elif expandToUnit is text.UNIT_LINE:
			self._startOffset=text.findStartOfLine(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength)
			self._endOffset=text.findEndOfLine(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength)
		elif expandToUnit in [text.UNIT_SCREEN,text.UNIT_STORY]:
			self._startOffset=0
			self._endOffset=len(self._text)
		elif expandToUnit is not None:
			raise NotImplementedError("unit: %s not supported"%unit)
		if limitToUnit in [None,text.UNIT_SCREEN,text.UNIT_STORY]:
			self._lowOffsetLimit=0
			self._highOffsetLimit=len(self._text)-1
		elif limitToUnit is text.UNIT_CHARACTER:
			self._lowOffsetLimit=self._startOffset
			self._highOffset=self._lowOffsetLimit+1
		elif limitToUnit is text.UNIT_WORD:
			self._lowOffsetLimit=text.findStartOfWord(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength)
			self._highOffsetLimit=text.findEndOfWord(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength)
		elif limitToUnit is text.UNIT_LINE:
			self._lowOffsetLimit=text.findStartOfLine(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength)
			self._highOffsetLimit=text.findEndOfLine(self._text,self._startOffset,lineLength=obj.textRepresentationLineLength)
		else:
			raise NotImplementedError("limitToUnit: %s not supported"%limitToUnit)

	def _get_startOffset(self):
		return self._startOffset

	def _get_endOffset(self):
		return self._endOffset

	def _get_text(self):
		return self._text[self._startOffset:self._endOffset]

	def getRelatedUnit(self,relation):
		if self.unit is None:
			raise RuntimeError("no unit specified")
		if relation==text.UNITRELATION_NEXT:
			newOffset=self._endOffset
		elif relation==text.UNITRELATION_PREVIOUS:
			newOffset=self._startOffset-1
		elif relation==text.UNITRELATION_FIRST:
			newOffset=self._lowOffsetLimit
		elif relation==text.UNITRELATION_LAST:
			newOffset=self._highOffsetLimit-1
		else:
			raise NotImplementedError("unit relation: %s not supported"%relation)
		if newOffset<self._lowOffsetLimit or newOffset>=self._highOffsetLimit:
			raise text.E_noRelatedUnit("offset %d is out of range for limits %d, %d"%(newOffset,self._lowOffsetLimit,self._highOffsetLimit))
		return self.__class__(self.obj,text.OffsetPosition(newOffset),_text=self._text,expandToUnit=self.unit,limitToUnit=self.limitUnit)

	def _get_inUnit(self):
		if self.unit is None:
			raise RuntimeError("no unit specified")
		return True

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
@ivar text_caretOffset: the caret position in this object's text as an offset from 0
@type text_caretOffset: int
@ivar text_reviewOffset: the review cursor's position in the object's text as an offset from 0
@type text_reviewOffset: int
@ivar text_characterCount: the number of characters in this object's text
@type text_characterCount: int
@ivar _text_lastReportedPresentation: a dictionary to store all the last reported attribute values such as font, page number, table position etc.
@type _text_lastReportedPresentation: dict
"""

	TextInfo=NVDAObjectTextInfo

	def __init__(self):
		self._oldValue=None
		self._oldStates=self.states
		self._oldName=None
		self._oldDescription=None
		self._hashLimit=10000000
		self._hashPrime=23
		self.reviewOffset=0
		self.textRepresentationLineLength=None #Use \r and or \n

	def __hash__(self):
		l=self._hashLimit
		p=self._hashPrime
		h=0
		h=(h+(hash(self.__class__.__name__)*p))%l
		h=(h+(hash(self.role)*p))%l
		h=(h+(hash(self.description)*p))%l
		h=(h+(hash(self.keyboardShortcut)*p))%l
		location=self.location
		if location and (len(location)==4):
			(left,top,width,height)=location
			h=(h+(hash(left)*p))%l
			h=(h+(hash(top)*p))%l
			h=(h+(hash(width)*p))%l
			h=(h+(hash(height)*p))%l
		return h

	def __eq__(self,other):
		if hash(self)==hash(other):
			return True
		else:
			return False

	def __ne__(self,other):
		if hash(self)!=hash(other):
			return True
		else:
			return False

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

	def _get_children(self):
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children

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
		child=self.firstChild
		while child:
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				speech.speakObject(child)
				child.speakDescendantObjects(hashList=hashList)
			child=child.next

	def reportFocus(self):
		speech.speakObject(self,reason=speech.REASON_FOCUS)

	def event_stateChange(self):
		if self.hasFocus:
			states=self.states
			if states!=self._oldStates:
				speech.speakObjectProperties(self,states=True, reason=speech.REASON_CHANGE)
				self._oldStates=states

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

	def _get_textRepresentation(self):
		return " ".join([x for x in self.name, self.value, self.description if isinstance(x, basestring) and len(x) > 0 and not x.isspace()])

	def event_valueChange(self):
		value=self.value
		if self.hasFocus and value!=self._oldValue:
			speech.speakObjectProperties(self, value=True, reason=speech.REASON_CHANGE)
			self._oldValue=value

	def event_nameChange(self):
		name=self.name
		if self.hasFocus and name!=self._oldName:
			speech.speakObjectProperties(self, name=True, reason=speech.REASON_CHANGE)
			self._oldName=name

	def event_descriptionChange(self):
		description=self.description
		if self.hasFocus and description!=self._oldDescription:
			speech.speakObjectProperties(self, description=True, reason=speech.REASON_CHANGE)
			self._oldDescription=description

	def _get_caretOffset(self):
		raise NotImplementedError("caret not supported")

	def _get_selectionOffsets(self):
		raise NotImplementedError("selection not supported")

	def makeTextInfo(self,position,expandToUnit=None,limitToUnit=None):
		return self.TextInfo(self,position,expandToUnit,limitToUnit)

	def script_moveByLine(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			textInfo=api.getFocusObject().makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_LINE)
			speech.speakText(textInfo.text)

	def script_moveByCharacter(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			textInfo=api.getFocusObject().makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_CHARACTER)
			speech.speakSymbol(textInfo.text)

	def script_moveByWord(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			textInfo=api.getFocusObject().makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_WORD)
			speech.speakText(textInfo.text)

	def script_moveByParagraph(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			textInfo=api.getFocusObject().makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_PARAGRAPH)
			speech.speakText(textInfo.text)

	def script_backspace(self,keyPress,nextScript):
		textInfo=api.getFocusObject().makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_CHARACTER)
		oldOffset=textInfo.startOffset
		if oldOffset>0:
			delChar=textInfo.getRelatedUnit(text.UNITRELATION_PREVIOUS).text
			sendKey(keyPress)
			if not isKeyWaiting():
				api.processPendingEvents()
				textInfo=api.getFocusObject().makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_CHARACTER)
				newOffset=textInfo.startOffset
				if newOffset<oldOffset:
					speech.speakSymbol(delChar)
		else:
			sendKey(keyPress)

	def script_delete(self,keyPress,nextScript):
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			textInfo=api.getFocusObject().makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_CHARACTER)
			speech.speakSymbol(textInfo.text)

	def script_changeSelection(self,keyPress,nextScript):
		oldObj=api.getFocusObject()
		textInfo=oldObj.makeTextInfo(text.POSITION_SELECTION)
		oldStart=textInfo.startOffset
		oldEnd=textInfo.endOffset
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			newObj=api.getFocusObject()
			textInfo=newObj.makeTextInfo(text.POSITION_SELECTION)
			newStart=textInfo.startOffset
			newEnd=textInfo.endOffset
			mode=None
			mode_selected=_("selected")
			mode_unselected=_("unselected")
			if newEnd>oldEnd:
				mode=mode_selected
				fromOffset=oldEnd
				toOffset=newEnd
			elif newStart<oldStart:
				mode=mode_selected
				fromOffset=newStart
				toOffset=oldStart
			elif oldEnd>newEnd:
				mode=mode_unselected
				fromOffset=newEnd
				toOffset=oldEnd
			elif oldStart<newStart:
				mode=mode_unselected
				fromOffset=oldStart
				toOffset=newStart
			if isinstance(mode,basestring):
				selectingText=newObj.makeTextInfo(text.OffsetsPosition(fromOffset,toOffset)).text
				if len(selectingText)==1:
					selectingText=speech.processSymbol(selectingText)
				speech.speakMessage("%s %s"%(mode,selectingText))

