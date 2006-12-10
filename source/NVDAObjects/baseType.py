"""Module that contains the base NVDA object type"""
import autoPropertyType
import audio
import api
from config import conf

class NVDAObject(object):
	"""
The baseType NVDA object. All other NVDA objects are based on this one.
@ivar _hashLimit: The limit in size for a hash of this object
@type _hashLimit: int
@ivar _hashPrime: the prime number used in calculating this object's hash
@type _hashPrime: int
@ivar _cachedHash: The stored hash value for this object. This is calculated in __init__, change the L{_makeHash} function to change the way hashes are generated.
@type _cachedHash: int
@ivar _keyMap: A dictionary that stores key:method  key to script mappings. Do not change this directly, use L{getScript}, L{executeScript}, L{registerScriptKey} or L{registerScriptKeys} instead.
@type _keyMap: dict
@ivar name: The objects name or label. (e.g. the text of a list item, label of a button)
@type name: string
@ivar value: the object's value. (e.g. content of an edit field, percentage on a progresss bar)
@type value: string
@ivar role: The object's chosen role. (NVDA uses the set of MSAA role constants for roles, however sometimes if there is no suitable role, this can be a string)
@type role: int or string
@ivar typeString: The object's friendly type. (e.g. a link will have a link role, but its typeString may be 'visited link' depending on its states etc). This type can be anything, it is only communicated to the user, never used programatically.
@type typeString: string 
@ivar states: The object's states. (NVDA uses MSAA state constants for its states, bitwised grouped together)
@type states: int
@ivar allowedPositiveStates: a bitwise group of states that are allowed to be reported when on
@type allowedPositiveStates: int
@ivar allowedNegativeStates: a bitwise group of states that are allowed to be reported when off
@type allowedNegativeStates: int
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
@ivar speakOnGainFocus: If true, the object will speak when it gains focus, if false it will not.
@type speakOnGainFocus: boolean
@ivar needsFocusState: If true the object will only react to gainFocus events if its focus state is set at the time.
@type needsFocusState: boolean
@ivar speakOnForeground: if true, this object is spoken if it becomes the current foreground object
@type speakOnForeground: boolean
"""

	__metaclass__=autoPropertyType.autoPropertyType

	def __init__(self,*args):
		self._hashLimit=10000000
		self._hashPrime=17
		self._keyMap={}
		self.allowedPositiveStates=0
		self.allowedNegativeStates=0
		self.speakOnGainFocus=True
		self.needsFocusState=True
		self.speakOnForeground=True
		#Calculate the hash
		l=self._hashLimit
		p=self._hashPrime
		h=0
		h=(h+(hash(self.__class__.__name__)*p))%l
		h=(h+(hash(self.role)*p))%l
		h=(h+(hash(self.description)*p))%l
		h=(h+(hash(self.keyboardShortcut)*p))%l
		self._cachedHash=h

	def __hash__(self):
		return self._cachedHash

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
			return self._keyMap[keyPress]

	def executeScript(self,keyPress):
		"""
executes a script (instance method) if one is assigned to the keyPress given.
@param keyPress: The key you wish to execute the script for
@type keyPress: key
""" 
		script=self.getScript(self,keyPress)
		script(keyPress)

	def registerScriptKey(self,keyPress,func):
		"""
Registers the given script (instance method) along with the given keyPress internally so that this method can be executed by the keyPress.
@param keyPress: The chosen key to link the method with
@type keyPress: key
@param func: The method you want to register
@type func: instance method
"""
		self._keyMap[keyPress]=func

	def registerScriptKeys(self,keyDict):
		"""
Registers a number of methods with their respective keys so that these methods can be later executed by the keys.
@param dict: A dictionary of keyPress:method paires.
@type dict: dictionary
"""
		self._keyMap.update(keyDict)

	def _get_name(self):
		return ""

	def _get_role(self):
		return "NVDA object"

	def _get_typeString(self):
		return lang.roleNames.get(self.role,"role %s"%self.role)

	def _get_value(self):
		return ""

	def _get_description(self):
		return ""

	def _get_keyboardShortcut(self):
		return ""

	def _get_states(self):
		return 0

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
@param state: MSAA state constant
@type state: int
@param opposite: True if the state is negative, or false if the state is positive, default is False
@type opposite: boolean
"""
		text=_("state")+" %s"%state
		if opposite:
			text="%s %s"%(_("not"),text)
		return text

	def getStateNames(self,states,opposite=False):
		"""
Returns a string of names for a given bitwise group of states. Takes in to account if opposite is true or not.
@param states: bitwise group of MSAA state constants
@type state: int
@param opposite: True if the states are negative, or false if the states are positive, default is False
@type opposite: boolean
"""
		stateNames=""
		for state in api.createStateList(states):
			stateNames+=" %s"%self.getStateName(state,opposite=opposite)
		return stateNames

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

	def hasFocus(self):
		"""
Returns true of this object has focus, false otherwise.
"""
		return False

	def setFocus(self):
		"""
Tries to force this object to take the focus.
"""
		pass

	def _get_positionString(self):
		return ""

	def speakObject(self):
		"""
Speaks the properties of this object such as name, typeString,value, description, states, position etc.
"""
		name=self.name
		typeString=self.typeString
		positiveStateNames=self.getStateNames(self.calculatePositiveStates())
		negativeStateNames=self.getStateNames(self.calculateNegativeStates(),opposite=True)
		stateNames="%s %s"%(positiveStateNames,negativeStateNames)
		value=self.value
		description=self.description
		if description==name:
			description=None
		if conf["presentation"]["reportKeyboardShortcuts"]:
			keyboardShortcut=self.keyboardShortcut
		else:
			keyboardShortcut=None
		position=self.positionString
		audio.speakObjectProperties(name=name,typeString=typeString,stateText=stateNames,value=value,description=description,keyboardShortcut=keyboardShortcut,position=position)

	def event_gainFocus(self):
		"""
This code is executed if a gain focus event is received by this object.
"""
		if self.speakOnGainFocus and (not self.needsFocusState or (self.needsFocusState and self.hasFocus())):
			api.setNavigatorObject(self)
			if not ((self==api.getForegroundObject()) and self.speakOnForeground):
				self.speakObject()

	def event_foreground(self):
		"""
This method will speak the object if L{speakOnForeground} is true and this object has just become the current foreground object.
"""
		if self.speakOnForeground:
			api.setNavigatorObject(self)
			self.speakObject()
