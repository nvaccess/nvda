#NVDAObjects/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module that contains the base NVDA object type"""
from new import instancemethod
import textBuffer
import speech
from keyUtils import key, sendKey
import globalVars
import api
import config

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
@ivar typeString: The object's friendly type. (e.g. a link will have a link role, but its typeString may be 'visited link' depending on its states etc). This type can be anything, it is only communicated to the user, never used programatically.
@type typeString: string 
@ivar states: The object's states. (NVDA uses IAccessible state constants for its states, bitwised grouped together)
@type states: int
@ivar allowedPositiveStates: a bitwise group of states that are allowed to be reported when on
@type allowedPositiveStates: int
@ivar allowedNegativeStates: a bitwise group of states that are allowed to be reported when off
@type allowedNegativeStates: int
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
@ivar speakOnGainFocus: If true, the object will speak when it gains focus, if false it will not.
@type speakOnGainFocus: boolean
@ivar needsFocusState: If true the object will only react to gainFocus events if its focus state is set at the time.
@type needsFocusState: boolean
@ivar speakOnForeground: if true, this object is spoken if it becomes the current foreground object
@type speakOnForeground: boolean
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

	allowedPositiveStates=0
	allowedNegativeStates=0
	speakOnGainFocus=True
	needsFocusState=True
	speakOnForeground=True

	def __init__(self):
		textBuffer.textBufferObject.__init__(self)
		self._oldValue=None
		self._oldStates=self.states
		self._oldName=None
		self._oldDescription=None
		self._hashLimit=10000000
		self._hashPrime=23

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
		return "NVDA object"

	def _get_typeString(self):
		return _("role %s")%self.role

	def _get_value(self):
		return None

	def _get_description(self):
		return None

	def _get_keyboardShortcut(self):
		return None

	def _get_states(self):
		return frozenset()

	def calculatePositiveStates(self):
		"""
Filters the states property, only allowing certain positive states.
"""
		return self.states&self.allowedPositiveStates

	def calculateNegativeStates(self):
		"""
Filters the states property, only allowing certain positive states.
"""
		return (~self.states)&self.allowedNegativeStates

	def getStateName(self,state,opposite=False):
		"""
Returns a name for a given state. Takes in to account if opposite is true or not.
@param state: IAccessible state constant
@type state: int
@param opposite: True if the state is negative, or false if the state is positive, default is False
@type opposite: boolean
"""
		text=_("state %s")%state
		if opposite:
			text=_("not %s")%text
		return text

	def getStateNames(self,states,opposite=False):
		"""
Returns a string of names for a given bitwise group of states. Takes in to account if opposite is true or not.
@param states: bitwise group of IAccessible state constants
@type state: int
@param opposite: True if the states are negative, or false if the states are positive, default is False
@type opposite: boolean
"""
		return " ".join([self.getStateName(state,opposite) for state in api.createStateList(states)])

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
		speech.speakObject(self)

	def text_getText(self,start=None,end=None):
		"""Gets either all the text the object has, or the text from a certain offset, or to a certain offset.
@param start: the start offset
@type start: int
@param end: the end offset
@type end: int
@returns: the text
@rtype: string
"""
		text=" ".join([x for x in [self.name,self.value,self.description] if isinstance(x,basestring) and not x.isspace()])
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
