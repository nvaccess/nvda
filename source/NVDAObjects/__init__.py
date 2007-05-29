#NVDAObjects/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module that contains the base NVDA object type"""
from new import instancemethod
import baseObject
import speech
from keyUtils import key, sendKey
import globalVars
import api
from textPositionUtils import *
import textBuffer
import config
import controlTypes

class NVDAObject(textBuffer.textBufferObject):
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

	def __init__(self):
		textBuffer.textBufferObject.__init__(self)
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
		if self.hasFocus:
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

	def _get_textRepresentation(self,start=None,end=None):
		"""Gets either all the text the object has, or the text from a certain offset, or to a certain offset.
@param start: the start offset
@type start: int
@param end: the end offset
@type end: int
@returns: the text
@rtype: string
"""
		text = " ".join([x for x in self.name, self.value, self.description if isinstance(x, basestring) and len(x) > 0 and not x.isspace()])
		if start is None:
			start=0
		if end is None:
			end=len(text)
		return text[start:end]

	def event_caret(self):
		self.text_reviewOffset=self.text_caretOffset

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

	def script_review_currentLine(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		start=findStartOfLine(text,self.reviewOffset,lineLength=lineLength)
		end=findEndOfLine(text,self.reviewOffset,lineLength=lineLength)
		speech.speakText(text[start:end])

	def script_review_nextLine(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		start=findStartOfLine(text,self.reviewOffset,lineLength=lineLength)
		end=findEndOfLine(text,self.reviewOffset,lineLength=lineLength)
		if end<len(text):
			start=end
			end=findEndOfLine(text,start,lineLength=lineLength)
			self.reviewOffset=start
		else:
			speech.speakMessage(_("bottom"))
		speech.speakText(text[start:end])

	def script_review_prevLine(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		start=findStartOfLine(text,self.reviewOffset,lineLength=lineLength)
		end=findEndOfLine(text,self.reviewOffset,lineLength=lineLength)
		if start>0:
			end=start
			start=findStartOfLine(text,end-1,lineLength=lineLength)
			self.reviewOffset=start
		else:
			speech.speakMessage(_("top"))
		speech.speakText(text[start:end])

	def script_review_top(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		offset=0
		start=findStartOfLine(text,offset,lineLength=lineLength)
		end=findEndOfLine(text,offset,lineLength=lineLength)
		self.reviewOffset=offset
		speech.speakMessage(_("top"))
		speech.speakText(text[start:end])

	def script_review_bottom(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		offset=len(text)-1
		start=findStartOfLine(text,offset,lineLength=lineLength)
		end=findEndOfLine(text,offset,lineLength=lineLength)
		self.reviewOffset=offset
		speech.speakMessage(_("bottom"))
		speech.speakText(text[start:end])

	def script_review_currentWord(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		start=findStartOfWord(text,self.reviewOffset,lineLength=lineLength)
		end=findEndOfWord(text,self.reviewOffset,lineLength=lineLength)
		speech.speakText(text[start:end])

	def script_review_nextWord(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		start=findStartOfWord(text,self.reviewOffset,lineLength=lineLength)
		end=findEndOfWord(text,self.reviewOffset,lineLength=lineLength)
		if end<len(text):
			start=end
			end=findEndOfWord(text,start,lineLength=lineLength)
			self.reviewOffset=start
		else:
			speech.speakMessage(_("bottom"))
		speech.speakText(text[start:end])

	def script_review_prevWord(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		start=findStartOfWord(text,self.reviewOffset,lineLength=lineLength)
		end=findEndOfWord(text,self.reviewOffset,lineLength=lineLength)
		if start>0:
			end=start
			start=findStartOfWord(text,end-1,lineLength=lineLength)
			self.reviewOffset=start
		else:
			speech.speakMessage(_("top"))
		speech.speakText(text[start:end])

	def script_review_currentCharacter(self,keyPress,nextScript):
		text=self.textRepresentation
		speech.speakSymbol(text[self.reviewOffset])

	def script_review_nextCharacter(self,keyPress,nextScript):
		text=self.textRepresentation
		offset=self.reviewOffset+1
		if offset<len(text):
			self.reviewOffset=offset
		else:
			speech.speakMessage(_("bottom"))
		speech.speakSymbol(text[self.reviewOffset])

	def script_review_prevCharacter(self,keyPress,nextScript):
		text=self.textRepresentation
		offset=self.reviewOffset-1
		if offset>=0:
			self.reviewOffset=offset
		else:
			speech.speakMessage(_("top"))
		speech.speakSymbol(text[self.reviewOffset])

	def script_review_startOfLine(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		start=findStartOfLine(text,self.reviewOffset,lineLength=lineLength)
		self.reviewOffset=start
		speech.speakSymbol(text[self.reviewOffset])

	def script_review_endOfLine(self,keyPress,nextScript):
		text=self.textRepresentation
		lineLength=self.textRepresentationLineLength
		end=findEndOfLine(text,self.reviewOffset,lineLength=lineLength)-1
		self.reviewOffset=end
		speech.speakSymbol(text[self.reviewOffset])
