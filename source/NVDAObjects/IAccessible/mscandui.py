import time
import oleacc
import queueHandler
import eventHandler
import controlTypes
import config
import api
import ui
import winUser
import mouseHandler
import NVDAObjects.window
from . import IAccessible
from NVDAObjects.behaviors import CandidateItem as CandidateItemBehavior

def reportSelectedCandidate(candidateObject,allowDuplicate=False,newList=False):
	if not eventHandler.isPendingEvents("gainFocus") and (allowDuplicate or candidateObject!=api.getFocusObject()):
		if not isinstance(api.getFocusObject(),BaseCandidateItem):
			oldCandidateItemsText=None
			candidateObject.container=api.getFocusObject()
			eventHandler.queueEvent("foreground",candidateObject)
		else:
			oldCandidateItemsText=api.getFocusObject().visibleCandidateItemsText
			candidateObject.container=api.getFocusObject().container
		if config.conf["inputComposition"]["autoReportAllCandidates"] and (newList or candidateObject.visibleCandidateItemsText!=oldCandidateItemsText):
			queueHandler.queueFunction(queueHandler.eventQueue,ui.message,candidateObject.visibleCandidateItemsText)
		eventHandler.queueEvent("gainFocus",candidateObject)

class BaseCandidateItem(CandidateItemBehavior,IAccessible):

	role=controlTypes.Role.LISTITEM
	keyboardShortcut=""

	def _get_candidateNumber(self):
		number=super(BaseCandidateItem,self).keyboardShortcut
		try:
			number=int(number)
		except (ValueError,TypeError):
			pass
		return number

	def _get_parent(self):
		parent=super(BaseCandidateItem,self).parent
		# Translators: A label for a 'candidate' list which contains symbols the user can choose from  when typing east-asian characters into a document. 
		parent.name=_("Candidate")
		parent.description=None
		return parent

	def _get_name(self):
		try:
			number=int(self.candidateNumber)
		except (TypeError,ValueError):
			return super(BaseCandidateItem,self).name
		candidate=super(BaseCandidateItem,self).name
		return self.getFormattedCandidateName(number,candidate)

	def _get_description(self):
		candidate=super(BaseCandidateItem,self).name
		return self.getFormattedCandidateDescription(candidate)

	def _get_basicText(self):
		return super(BaseCandidateItem,self).name

class MSCandUI_candidateListItem(BaseCandidateItem):

	def _get_states(self):
		states=super(MSCandUI_candidateListItem,self).states
		states.add(controlTypes.State.SELECTABLE)
		return states

	def event_stateChange(self):
		if controlTypes.State.SELECTED in self.states:
			reportSelectedCandidate(self)

class MSCandUI21_candidateMenuItem(BaseCandidateItem):

	def _get_previous(self):
		item=super(MSCandUI21_candidateMenuItem,self).previous
		if not item or controlTypes.State.INVISIBLE in item.states: return
		return MSCandUI21_candidateMenuItem(IAccessibleObject=item.IAccessibleObject,IAccessibleChildID=item.IAccessibleChildID)

	def _get_next(self):
		item=super(MSCandUI21_candidateMenuItem,self).next
		if not item or controlTypes.State.INVISIBLE in item.states: return
		return MSCandUI21_candidateMenuItem(IAccessibleObject=item.IAccessibleObject,IAccessibleChildID=item.IAccessibleChildID)

	def doAction(self,index=None):
		if not index:
			l=self.location
			if l:
				x=l[0]
				y=l[1]
				oldX,oldY=winUser.getCursorPos()
				winUser.setCursorPos(x,y)
				mouseHandler.doPrimaryClick(releaseDelay=0.2)
				winUser.setCursorPos(oldX,oldY)
				return
		raise NotImplementedError

	def script_nextItem(self,gesture):
		item=self.next
		if not item or not isinstance(item.candidateNumber,int): return
		reportSelectedCandidate(item)

	def script_previousItem(self,gesture):
		item=self.previous
		if not item or not isinstance(item.candidateNumber,int): return
		reportSelectedCandidate(item)

	def script_changePage(self,gesture):
		try:
			del self.__dict__['visibleCandidateItemsText']
		except KeyError:
			pass
		gesture.send()
		api.processPendingEvents()
		oldItem=item=self
		while item and isinstance(item.candidateNumber,int):
			oldItem=item
			item=item.previous
		if oldItem and isinstance(oldItem.candidateNumber,int) and oldItem.name:
			reportSelectedCandidate(oldItem,allowDuplicate=True,newList=True)

	def script_activate(self,gesture):
		self.doAction()
		api.processPendingEvents()
		oldItem=item=self
		while item and isinstance(item.candidateNumber,int):
			oldItem=item
			item=item.previous
		if oldItem and isinstance(oldItem.candidateNumber,int) and oldItem.name:
			reportSelectedCandidate(oldItem,allowDuplicate=True,newList=True)

	__gestures={
		"kb:downArrow":"nextItem",
		"kb:upArrow":"previousItem",
		"kb:pageDown":"changePage",
		"kb:pageUp":"changePage",
		"kb:leftArrow":"changePage",
		"kb:rightArrow":"changePage",
		"kb:space":"activate",
		"kb:enter":"activate",
	}

class MSCandUI21(IAccessible):

	def _get_isPresentableFocusAncestor(self):
		return False

	def event_show(self):
		candidateList=self.simpleFirstChild
		if not candidateList: return
		role=candidateList.role
		if role==controlTypes.Role.LIST:
			item=candidateList.firstChild
			while item and controlTypes.State.SELECTED not in item.states:
				item=item.next
			if item:
				reportSelectedCandidate(item)
				return
			elif config.conf["reviewCursor"]["followFocus"]:
				api.setNavigatorObject(candidateList, isFocus=True)
		elif role==controlTypes.Role.MENUBUTTON:
			item=candidateList.firstChild.next.next
			item=MSCandUI21_candidateMenuItem(IAccessibleObject=item.IAccessibleObject,IAccessibleChildID=item.IAccessibleChildID)
			if item and isinstance(item.candidateNumber,int) and item.name:
				reportSelectedCandidate(item)

###IME 2002

class MSCandUIWindow_candidateListItem(MSCandUI_candidateListItem):

	def _get_isValidCandidate(self):
		if self.IAccessibleRole!=oleacc.ROLE_SYSTEM_LISTITEM:
			return False
		name=super(BaseCandidateItem,self).name
		if not name:
			return False
		return True

	def _get_candidateNumber(self):
		index=self.IAccessibleChildID-2
		if index>0:
			return index

	def _get_next(self):
		childID=self.IAccessibleChildID+1
		item=self.__class__(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=childID)
		if item.isValidCandidate:
			return item

	def _get_previous(self):
		childID=self.IAccessibleChildID-1
		if childID>=3:
			item=self.__class__(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=childID)
			if item.isValidCandidate:
				return item

class MSCandUIWindow(IAccessible):

	# Translators: A label for a 'candidate' list which contains symbols the user can choose from  when typing east-asian characters into a document.
	name=_("Candidate")
	role=controlTypes.Role.LIST

	def _get_states(self):
		states=super(MSCandUIWindow,self).states
		states.discard(controlTypes.State.UNAVAILABLE)
		return states

	def event_show(self):
		item=MSCandUIWindow_candidateListItem(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=3)
		reportSelectedCandidate(item)

class ModernCandidateUICandidateItem(BaseCandidateItem):

	def _get_parent(self):
		# Candidate list in Microsoft Quick cannot be obtained in IAccessible _get_parent.
		# Use _get_parent in NVDAObject.window.
		parent=NVDAObjects.window.Window._get_parent(self)
		return parent

	def _get_candidateCharacters(self):
		return super(BaseCandidateItem,self).name

	_candidateNumber=""

	_visibleCandidateItemsText=""

	def refreshCandidateList(self):
		textList=[]
		candidateItems = super(ModernCandidateUICandidateItem,self).parent.children
		for child in candidateItems:
			if not isinstance(child,ModernCandidateUICandidateItem) or controlTypes.State.SELECTABLE not in child.states:
				continue
			textList.append(child.candidateCharacters)
		if not len(textList)<=1:
			self._visibleCandidateItemsText=(u", ".join(textList))+u", "
			try:
				self._candidateNumber = textList.index(self.candidateCharacters)+1
			except ValueError:
				pass


	def _get_candidateNumber(self):
		if not self._candidateNumber:
			self.refreshCandidateList()
		return self._candidateNumber

	def _get_visibleCandidateItemsText(self):
		if not self._visibleCandidateItemsText:
			self.refreshCandidateList()
		return self._visibleCandidateItemsText

	def event_stateChange(self):
		if controlTypes.State.SELECTED in self.states:
			reportSelectedCandidate(self)

def findExtraOverlayClasses(obj,clsList):
	windowClassName=obj.windowClassName
	role=obj.IAccessibleRole
	if (
		windowClassName=="Microsoft.IME.CandidateWindow.View"
		and (
			obj.role==controlTypes.Role.BUTTON
			or obj.role==controlTypes.Role.LISTITEM
	)):
			clsList.append(ModernCandidateUICandidateItem)
	elif windowClassName=="MSCandUIWindow_Candidate":
		if role==oleacc.ROLE_SYSTEM_CLIENT:
			clsList.append(MSCandUIWindow)
		elif role==oleacc.ROLE_SYSTEM_LISTITEM:
			clsList.append(MSCandUIWindow_candidateListItem)
	elif windowClassName in ("mscandui21.candidate","mscandui40.candidate"):
		if role==oleacc.ROLE_SYSTEM_LISTITEM:
			clsList.append(MSCandUI_candidateListItem)
		elif role==oleacc.ROLE_SYSTEM_CLIENT:
			clsList.append(MSCandUI21)
