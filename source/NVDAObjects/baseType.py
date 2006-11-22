import audio
import api
from config import conf

class NVDAObject(object):

	def __init__(self,*args):
		self._keyMap={}
		self.allowedPositiveStates=0
		self.allowedNegativeStates=0

	def getScript(self,keyPress):
		if self._keyMap.has_key(keyPress):
			return self._keyMap[keyPress]

	def executeScript(self,keyPress):
		script=self.getScript(self,keyPress)
		script(keyPress)

	def registerScriptKey(self,keyPress,methodName):
		self._keyMap[keyPress]=methodName

	def registerScriptKeys(self,keyDict):
		self._keyMap.update(keyDict)

	def getAllowedPositiveStates(self):
		return self._allowedPositiveStates

	def setAllowedPositiveStates(self,states):
		self._allowedPositiveStates=states

	allowedPositiveStates=property(fget=getAllowedPositiveStates,fset=setAllowedPositiveStates)

	def getAllowedNegativeStates(self):
		return self._allowedNegativeStates

	def setAllowedNegativeStates(self,states):
		self._allowedNegativeStates=states

	allowedNegativeStates=property(fget=getAllowedNegativeStates,fset=setAllowedNegativeStates)

	def getName(self):
		return ""
	name=property(fget=getName)

	def getRole(self):
		return "NVDA object"
	role=property(fget=getRole)

	def getTypeString(self):
		return lang.roleNames.get(self.role,"role %s"%self.role)
	typeString=property(fget=getTypeString)

	def getValue(self):
		return ""
	value=property(fget=getValue)

	def getDescription(self):
		return ""
	description=property(fget=getDescription)

	def getKeyboardShortcut(self):
		return ""
	keyboardShortcut=property(fget=getKeyboardShortcut)

	def getStates(self):
		return 0
	states=property(fget=getStates)

	def calculatePositiveStates(self):
		return self.states&self.allowedPositiveStates

	def calculateNegativeStates(self):
		return (~self.states)&self.allowedNegativeStates

	def getStateName(self,state,opposite=False):
		text=_("state")+" %s"%state
		if opposite:
			text="%s %s"%(_("not"),text)
		return text

	def getStateNames(self,states,opposite=False):
		stateNames=""
		for state in api.createStateList(states):
			stateNames+=" %s"%self.getStateName(state,opposite=opposite)
		return stateNames

	def getLocation(self):
		return (0,0,0,0)
	location=property(fget=getLocation)

	def getParent(self):
		return None
	parent=property(fget=getParent)

	def getNext(self):
		return None
	next=property(fget=getNext)

	def getPrevious(self):
		return None
	previous=property(fget=getPrevious)

	def getFirstChild(self):
		return None
	firstChild=property(fget=getFirstChild)

	def getChildren(self):
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children
	children=property(fget=getChildren)

	def getChildCount(self):
		return len(self.children)
	childCount=property(fget=getChildCount)

	def doDefaultAction(self):
		pass

	def getActiveChild(self):
		return None
	activeChild=property(fget=getActiveChild)

	def hasFocus(self):
		return False

	def setFocus(self):
		pass

	def getPositionString(self):
		return ""
	positionString=property(fget=getPositionString)

	def speakObject(self):
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
