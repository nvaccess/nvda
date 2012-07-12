import time
import oleacc
import eventHandler
import controlTypes
import characterProcessing
import api
import speech
import winUser
from . import IAccessible

def reportSelectedCandidate(candidateObject,allowDuplicate=False):
	if not eventHandler.isPendingEvents("gainFocus") and (allowDuplicate or candidateObject!=api.getFocusObject()):
		if not isinstance(api.getFocusObject(),BaseCandidateItem):
			candidateObject.container.container=api.getFocusObject()
			eventHandler.queueEvent("foreground",candidateObject.container)
		else:
			candidateObject.container.container=api.getFocusObject().container.container
		eventHandler.queueEvent("gainFocus",candidateObject)

class BaseCandidateItem(IAccessible):

	role=controlTypes.ROLE_LISTITEM

	def _get_parent(self):
		parent=super(BaseCandidateItem,self).parent
		parent.name=_("Candidate")
		parent.description=None
		return parent

	def _get_keyboardShortcut(self):
		return ""

	def _get_value(self):
		return super(BaseCandidateItem,self).keyboardShortcut

	def _get_description(self):
		symbols=self.name
		descriptions=[]
		numSymbols=len(symbols)
		for symbol in symbols:
			try:
				symbolDescriptions=characterProcessing.getCharacterDescription(speech.getCurrentLanguage(),symbol)[:1] or []
			except TypeError:
				symbolDescriptions=[]
			numSymbolDescriptions=len(symbolDescriptions)
			for desc in symbolDescriptions:
				if desc and desc[0]=='(' and desc[-1]==')':
					desc=desc[1:-1]
				elif numSymbols>1 or len(symbolDescriptions)==1:
					desc=_("{symbol} as in {description}").format(symbol=symbol,description=desc)
				descriptions.append(desc)
		if descriptions:
			return ", ".join(descriptions)

class MSCandUI_candidateListItem(BaseCandidateItem):

	def _get_states(self):
		states=super(MSCandUI_candidateListItem,self).states
		states.add(controlTypes.STATE_SELECTABLE)
		return states

	def event_stateChange(self):
		if controlTypes.STATE_SELECTED in self.states:
			reportSelectedCandidate(self)

class MSCandUI21_candidateMenuItem(BaseCandidateItem):

	def doAction(self,index=None):
		if not index:
			l=self.location
			if l:
				x=l[0]
				y=l[1]
				oldX,oldY=winUser.getCursorPos()
				winUser.setCursorPos(x,y)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
				time.sleep(0.2)
				winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
				winUser.setCursorPos(oldX,oldY)
				return
		raise NotImplementedError

	def script_nextItem(self,gesture):
		item=self.next
		if not item or controlTypes.STATE_INVISIBLE in item.states: return
		item=MSCandUI21_candidateMenuItem(IAccessibleObject=item.IAccessibleObject,IAccessibleChildID=item.IAccessibleChildID)
		reportSelectedCandidate(item)

	def script_previousItem(self,gesture):
		item=self.previous
		if not item or controlTypes.STATE_INVISIBLE in item.states: return
		item=MSCandUI21_candidateMenuItem(IAccessibleObject=item.IAccessibleObject,IAccessibleChildID=item.IAccessibleChildID)
		reportSelectedCandidate(item)

	def script_changePage(self,gesture):
		gesture.send()
		api.processPendingEvents()
		item=self.parent.firstChild.next.next
		item=MSCandUI21_candidateMenuItem(IAccessibleObject=item.IAccessibleObject,IAccessibleChildID=item.IAccessibleChildID)
		reportSelectedCandidate(item,allowDuplicate=True)

	def script_activate(self,gesture):
		self.doAction()

	__gestures={
		"kb:downArrow":"nextItem",
		"kb:upArrow":"previousItem",
		"kb:pageDown":"changePage",
		"kb:pageUp":"changePage",
		"kb:enter":"activate",
	}

class MSCandUI21(IAccessible):

	def _get_isPresentableFocusAncestor(self):
		return False

	def event_show(self):
		candidateList=self.simpleFirstChild
		if not candidateList: return
		role=candidateList.role
		if role==controlTypes.ROLE_LIST:
			api.setNavigatorObject(candidateList)
			item=candidateList.firstChild
			while item and controlTypes.STATE_SELECTED not in item.states:
				item=item.next
			if item:
				reportSelectedCandidate(item)
				return
		elif role==controlTypes.ROLE_MENUBUTTON:
			item=candidateList.firstChild.next.next
			item=MSCandUI21_candidateMenuItem(IAccessibleObject=item.IAccessibleObject,IAccessibleChildID=item.IAccessibleChildID)
			reportSelectedCandidate(item)

###IME 2002

class MSCandUIWindow_candidateListItem(MSCandUI_candidateListItem):

	def _get_value(self):
		index=self.IAccessibleChildID-2
		if index>0:
			return unicode(index)

	def _get_next(self):
		childID=self.IAccessibleChildID+1
		item=self.__class__(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=childID)
		if item.IAccessibleRole==oleacc.ROLE_SYSTEM_LISTITEM:
			return item

	def _get_previous(self):
		childID=self.IAccessibleChildID-1
		if childID>=3:
			return self.__class__(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=childID)

class MSCandUIWindow(IAccessible):

	name=_("Candidates")
	role=controlTypes.ROLE_LIST

	def _get_states(self):
		states=super(MSCandUIWindow,self).states
		states.discard(controlTypes.STATE_UNAVAILABLE)
		return states

	def event_show(self):
		item=MSCandUIWindow_candidateListItem(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=3)
		reportSelectedCandidate(item)

def findExtraOverlayClasses(obj,clsList):
	windowClassName=obj.windowClassName
	role=obj.IAccessibleRole
	if windowClassName=="MSCandUIWindow_Candidate":
		if role==oleacc.ROLE_SYSTEM_CLIENT:
			clsList.append(MSCandUIWindow)
		elif role==oleacc.ROLE_SYSTEM_LISTITEM:
			clsList.append(MSCandUIWindow_candidateListItem)
	elif windowClassName in ("mscandui21.candidate","mscandui40.candidate"):
		if role==oleacc.ROLE_SYSTEM_LISTITEM:
			clsList.append(MSCandUI_candidateListItem)
		elif role==oleacc.ROLE_SYSTEM_CLIENT:
			clsList.append(MSCandUI21)
