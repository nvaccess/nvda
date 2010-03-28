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
from logHandler import log
import eventHandler
import baseObject
import speech
import api
import textInfos.offsets
import config
import controlTypes
import appModuleHandler
import virtualBufferHandler
import braille

class NVDAObjectTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getStoryText(self):
		return self.obj.basicText

	def _getStoryLength(self):
		return len(self._getStoryText())

	def _getTextRange(self,start,end):
		text=self._getStoryText()
		return text[start:end]

class DynamicNVDAObjectType(baseObject.ScriptableObject.__class__):
	_dynamicClassCache={}

	def __call__(self,chooseBestAPI=True,**kwargs):
		if chooseBestAPI:
			APIClass=self.findBestAPIClass(kwargs)
		else:
			APIClass=self

		if 'findOverlayClasses' not in APIClass.__dict__:
			raise TypeError("Cannot instantiate class %s as it does not implement findOverlayClasses"%APIClass.__name__)

		# Instantiate the requested class.
		obj=APIClass.__new__(APIClass,**kwargs)
		obj.APIClass=APIClass
		if isinstance(obj,self):
			obj.__init__(**kwargs)

		try:
			clsList=obj.findOverlayClasses([])
		except:
			log.debugWarning("findOverlayClasses failed",exc_info=True)
			return None
		# Determine the bases for the new class.
		bases=[]
		for index in xrange(len(clsList)):
			# A class doesn't need to be a base if it is already a subclass of a previous base.
			if index==0 or not issubclass(clsList[index-1],clsList[index]):
				bases.append(clsList[index])

		# Construct the new class.
		if len(bases) == 1:
			# We only have one base, so there's no point in creating a dynamic type.
			newCls=bases[0]
		else:
			bases=tuple(bases)
			newCls=self._dynamicClassCache.get(bases,None)
			if not newCls:
				name="Dynamic_%s"%"".join([x.__name__ for x in clsList])
				newCls=type(name,bases,{})
				self._dynamicClassCache[bases]=newCls

		oldMro=frozenset(obj.__class__.__mro__)
		# Mutate obj into the new class.
		obj.__class__=newCls

		# Initialise the overlay classes.
		for cls in reversed(newCls.__mro__):
			if cls in oldMro:
				# This class was part of the initially constructed object, so its constructor would have been called.
				continue
			initFunc=cls.__dict__.get("initOverlayClass")
			if initFunc:
				initFunc(obj)

		# Allow app modules to mutate NVDAObjects during creation.
		appModule=obj.appModule
		if appModule and hasattr(appModule,"event_NVDAObject_init"):
			appModule.event_NVDAObject_init(obj)

		return obj

class NVDAObject(baseObject.ScriptableObject):
	"""
	NVDA's representation of a control or widget in the Operating System. Provides information such as a name, role, value, description etc.
	"""

	__metaclass__=DynamicNVDAObjectType
	cachePropertiesByDefault = True

	TextInfo=NVDAObjectTextInfo #:The TextInfo class this object should use

	@classmethod
	def findBestAPIClass(cls,kwargs,relation=None):
		"""
		Finds out the highest-level APIClass this object can get to given these kwargs, and updates the kwargs and returns the APIClass.
		@param relation: the relationship of a possible new object of this type to  another object creating it (e.g. parent).
		@param type: string
		@param kwargs: the arguments necessary to construct an object of the class this method was called on.
		@type kwargs: dictionary
		@returns: the new APIClass
		@rtype: DynamicNVDAObjectType
		"""
		newAPIClass=cls
		if 'getPossibleAPIClasses' in newAPIClass.__dict__:
			for possibleAPIClass in newAPIClass.getPossibleAPIClasses(kwargs,relation=relation):
				if 'kwargsFromSuper' not in possibleAPIClass.__dict__:  
					log.error("possible API class %s does not implement kwargsFromSuper"%possibleAPIClass)
					continue
				if possibleAPIClass.kwargsFromSuper(kwargs,relation=relation):
					return possibleAPIClass.findBestAPIClass(kwargs,relation=relation)
		return newAPIClass

	@classmethod
	def getPossibleAPIClasses(cls,kwargs,relation=None):
		"""
		Provides a generator which can generate all the possible API classes (in priority order) that inherit directly from the class it was called on.
		@param relation: the relationship of a possible new object of this type to  another object creating it (e.g. parent).
		@param type: string
		@param kwargs: the arguments necessary to construct an object of the class this method was called on.
		@type kwargs: dictionary
		@returns: a generator
		@rtype: generator
		"""
		import NVDAObjects.window
		yield NVDAObjects.window.Window

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		"""
		Finds out if this class can be instanciated from the given super kwargs.
		If so it updates the kwargs to contain everything it will need to instanciate this class, and returns True.
		If this class can not be instanciated, it returns False and kwargs is not touched.
		@param relation: why is this class being instanciated? parent, focus, foreground etc...
		@type relation: string
		@param kwargs: the kwargs for constructing this class's super class.
		@type kwargs: dict
		@rtype: boolean
		"""
		raise NotImplementedError
 

	def findOverlayClasses(self, clsList):
		"""Chooses overlay classes which should be added to this object's class structure after the object has been initially instantiated.
		After an NVDAObject class (normally an API-level class) is instantiated, this method is called on the instance to choose appropriate overlay classes.
		This method may use properties, etc. on the instance to make this choice.
		The object's class structure is then mutated to contain these classes.
		L{initOverlayClass} is then called for each class which was not part of the initially instantiated object.
		This process allows an NVDAObject to be dynamically created using the most appropriate NVDAObject subclass at each API level.
		Classes should be listed with subclasses first. That is, subclasses should generally call super and then append their own classes to the list.
		For example: Called on an IAccessible NVDAObjectThe list might contain DialogIaccessible (a subclass of IAccessible), Edit (a subclass of Window).
		@param clsList: The list of classes from the caller.
		@type clsList: list of L{NVDAObject}
		@@return: the new list of classes.
		@rtype: list of L{NVDAObject}
		"""
		clsList.append(NVDAObject)
		return clsList

	beTransparentToMouse=False #:If true then NVDA will never consider the mouse to be on this object, rather it will be on an ancestor.

	@staticmethod
	def objectFromPoint(x,y):
		"""Retreaves an NVDAObject instance representing a control in the Operating System at the given x and y coordinates.
		@param x: the x coordinate.
		@type x: int
		@param y: the y coordinate.
		@param y: int
		@return: The object at the given x and y coordinates.
		@rtype: L{NVDAObject}
		"""
		kwargs={}
		APIClass=NVDAObject.findBestAPIClass(kwargs,relation=(x,y))
		return APIClass(chooseBestAPI=False,**kwargs)

	@staticmethod
	def objectWithFocus():
		"""Retreaves the object representing the control currently with focus in the Operating System. This differens from NVDA's focus object as this focus object is the real focus object according to the Operating System, not according to NVDA.
		@return: the object with focus.
		@rtype: L{NVDAObject}
		"""
		kwargs={}
		APIClass=NVDAObject.findBestAPIClass(kwargs,relation="focus")
		return APIClass(chooseBestAPI=False,**kwargs)

	@staticmethod
	def objectInForeground():
		"""Retreaves the object representing the current foreground control according to the Operating System. This differes from NVDA's foreground object as this object is the real foreground object according to the Operating System, not according to NVDA.
		@return: the foreground object
		@rtype: L{NVDAObject}
		"""
		kwargs={}
		APIClass=NVDAObject.findBestAPIClass(kwargs,relation="foreground")
		return APIClass(chooseBestAPI=False,**kwargs)

	def __init__(self):
		super(NVDAObject,self).__init__()
		self._mouseEntered=False #:True if the mouse has entered this object (for use in L{event_mouseMoved})
		self.textRepresentationLineLength=None #:If an integer greater than 0 then lines of text in this object are always this long.

	def _isEqual(self,other):
		"""Calculates if this object is equal to another object. Used by L{NVDAObject.__eq__}.
		@param other: the other object to compare with.
		@type other: L{NVDAObject}
		@return: True if equal, false otherwise.
		@rtype: boolean
		"""
		return True
 
	def __eq__(self,other):
		"""Compaires the objects' memory addresses, their type, and uses L{NVDAObject._isEqual} to see if they are equal.
		"""
		if self is other:
			return True
		if type(self) is not type(other):
			return False
		return self._isEqual(other)
 
	def __ne__(self,other):
		"""The opposite to L{NVDAObject.__eq__}
		"""
		return not self.__eq__(other)

	def _get_virtualBufferClass(self):
		"""
		If this NVDAObject should use a virtualBuffer, then this property provides the L{virtualBuffers.VirtualBuffer} class it should use. 
		If not then it should be not implemented.
		"""
		raise NotImplementedError

	def _get_virtualBuffer(self):
		"""Retreaves the virtualBuffer associated with this object.
		If a virtualBuffer has not been specifically set, the L{virtualBufferHandler} is asked if it can find a virtualBuffer containing this object.
		@return: the virtualBuffer
		@rtype: L{virtualBuffers.VirtualBuffer}
		""" 
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
		"""Specifically sets a virtualBuffer to be associated with this object.
		"""
		if obj:
			self._virtualBuffer=weakref.ref(obj)
		else: #We can't point a weakref to None, so just set the private variable to None, it can handle that
			self._virtualBuffer=None

	def _get_appModule(self):
		"""Retreaves the appModule representing the application this object is a part of by asking L{appModuleHandler}.
		@return: the appModule
		@rtype: L{appModuleHandler.AppModule}
		"""
		if not hasattr(self,'_appModuleRef'):
			a=appModuleHandler.getAppModuleForNVDAObject(self)
			if a:
				self._appModuleRef=weakref.ref(a)
				return a
		else:
			return self._appModuleRef()

	def _get_name(self):
		"""The name or label of this object (example: the text of a button).
		@rtype: basestring
		"""
		return ""

	def _get_role(self):
		"""The role or type of control this object represents (example: button, list, dialog).
		@return: a ROLE_* constant from L{controlTypes}
		@rtype: int
		"""  
		return controlTypes.ROLE_UNKNOWN

	def _get_value(self):
		"""The value of this object (example: the current percentage of a scrollbar, the selected option in a combo box).
		@rtype: basestring
		"""   
		return ""

	def _get_description(self):
		"""The description or help text of this object.
		@rtype: basestring
		"""
		return ""

	def _get_actionCount(self):
		"""Retreaves the number of actions supported by this object."""
		return 0

	def getActionName(self,index=None):
		"""Retreaves the name of an action supported by this object.
		If index is not given then the default action will be used if it exists.
		@param index: the optional 0-based index of the wanted action.
		@type index: int
		@return: the action's name
		@rtype: basestring
		"""
		raise NotImplementedError
 
	def doAction(self,index=None):
		"""Performs an action supported by this object.
		If index is not given then the default action will be used if it exists.
		"""
		raise NotImplementedError

	def _get_defaultActionIndex(self):
		"""Retreaves the index of the action that is the default."""
		return 0

	def _get_keyboardShortcut(self):
		"""The shortcut key that activates this object(example: alt+t).
		@rtype: basestring
		"""
		return ""

	def _get_isInForeground(self):
		"""
		Finds out if this object is currently within the foreground.
		"""
		raise NotImplementedError

	def _get_states(self):
		"""Retreaves the current states of this object (example: selected, focused).
		@return: a set of  STATE_* constants from L{controlTypes}.
		@rtype: set of int
		"""
		return set()

	def _get_location(self):
		"""The location of this object on the screen.
		@return: left, top, width and height of the object.
		@rtype: tuple of int
		"""
		raise NotImplementedError

	def _get_parent(self):
		"""Retreaves this object's parent (the object that contains this object).
		@return: the parent object if it exists else None.
		@rtype: L{NVDAObject} or None
		"""
		return None

	def _get_next(self):
		"""Retreaves the object directly after this object with the same parent.
		@return: the next object if it exists else None.
		@rtype: L{NVDAObject} or None
		"""
		return None

	def _get_previous(self):
		"""Retreaves the object directly before this object with the same parent.
		@return: the previous object if it exists else None.
		@rtype: L{NVDAObject} or None
		"""
		return None

	def _get_firstChild(self):
		"""Retreaves the first object that this object contains.
		@return: the first child object if it exists else None.
		@rtype: L{NVDAObject} or None
		"""
		return None

	def _get_lastChild(self):
		"""Retreaves the last object that this object contains.
		@return: the last child object if it exists else None.
		@rtype: L{NVDAObject} or None
		"""
		return None

	def _get_children(self):
		"""Retreaves a list of all the objects directly contained by this object (who's parent is this object).
		@rtype: list of L{NVDAObject}
		"""
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children

	def _get_rowNumber(self):
		"""Retreaves the row number of this object if it is in a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_columnNumber(self):
		"""Retreaves the column number of this object if it is in a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_rowCount(self):
		"""Retreaves the number of rows this object contains if its a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_columnCount(self):
		"""Retreaves the number of columns this object contains if its a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_table(self):
		"""Retreaves the object that represents the table that this object is contained in, if this object is a table cell.
		@rtype: L{NVDAObject}
		"""
		raise NotImplementedError

	def _get_recursiveDescendants(self):
		"""Recursively traverse and return the descendants of this object.
		This is a depth-first forward traversal.
		@return: The recursive descendants of this object.
		@rtype: generator of L{NVDAObject}
		"""
		for child in self.children:
			yield child
			for recursiveChild in child.recursiveDescendants:
				yield recursiveChild

	presType_unavailable="unavailable"
	presType_layout="layout"
	presType_content="content"

	def _get_presentationType(self):
		states=self.states
		if controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_UNAVAILABLE in states:
			return self.presType_unavailable
		role=self.role
		if controlTypes.STATE_FOCUSED in states:
			return self.presType_content

		#Static text should be content only if it really use usable text
		if role==controlTypes.ROLE_STATICTEXT:
			text=self.makeTextInfo(textInfos.POSITION_ALL).text
			return self.presType_content if text and not text.isspace() else self.presType_layout

		if role in (controlTypes.ROLE_UNKNOWN, controlTypes.ROLE_PANE, controlTypes.ROLE_ROOTPANE, controlTypes.ROLE_LAYEREDPANE, controlTypes.ROLE_SCROLLPANE, controlTypes.ROLE_SECTION,controlTypes.ROLE_PARAGRAPH,controlTypes.ROLE_TITLEBAR):
			return self.presType_layout
		name = self.name
		description = self.description
		if not name and not description and role in (controlTypes.ROLE_WINDOW,controlTypes.ROLE_LABEL,controlTypes.ROLE_PANEL, controlTypes.ROLE_PROPERTYPAGE, controlTypes.ROLE_TEXTFRAME, controlTypes.ROLE_GROUPING,controlTypes.ROLE_OPTIONPANE,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_FORM,controlTypes.ROLE_TABLEBODY):
			return self.presType_layout
		if not name and not description and role in (controlTypes.ROLE_TABLE,controlTypes.ROLE_TABLEROW,controlTypes.ROLE_TABLECOLUMN,controlTypes.ROLE_TABLECELL) and not config.conf["documentFormatting"]["reportTables"]:
			return self.presType_layout
		if role in (controlTypes.ROLE_TABLEROW,controlTypes.ROLE_TABLECOLUMN):
			try:
				table=self.table
			except NotImplementedError:
				table=None
			if table:
				# This is part of a real table, so the cells will report row/column information.
				# Therefore, this object is just for layout.
				return self.presType_layout
		return self.presType_content

	def _get_simpleParent(self):
		obj=self.parent
		while obj and obj.presentationType!=self.presType_content:
			obj=obj.parent
		return obj

	def _findSimpleNext(self,useChild=False,useParent=True,goPrevious=False):
		nextPrevAttrib="next" if not goPrevious else "previous"
		firstLastChildAttrib="firstChild" if not goPrevious else "lastChild"
		found=None
		if useChild:
			child=getattr(self,firstLastChildAttrib)
			childPresType=child.presentationType if child else None
			if childPresType==self.presType_content:
				found=child
			elif childPresType==self.presType_layout:
				found=child._findSimpleNext(useChild=True,useParent=False,goPrevious=goPrevious)
			elif child:
				found=child._findSimpleNext(useChild=False,useParent=False,goPrevious=goPrevious)
			if found:
				return found
		next=getattr(self,nextPrevAttrib)
		nextPresType=next.presentationType if next else None
		if nextPresType==self.presType_content:
			found=next
		elif nextPresType==self.presType_layout:
			found=next._findSimpleNext(useChild=True,useParent=False,goPrevious=goPrevious)
		elif next:
			found=next._findSimpleNext(useChild=False,useParent=False,goPrevious=goPrevious)
		if found:
			return found
		parent=self.parent if useParent else None
		while parent and parent.presentationType!=self.presType_content:
			next=parent._findSimpleNext(useChild=False,useParent=False,goPrevious=goPrevious)
			if next:
				return next
			parent=parent.parent

	def _get_simpleNext(self):
		return self._findSimpleNext()

	def _get_simplePrevious(self):
		return self._findSimpleNext(goPrevious=True)

	def _get_simpleFirstChild(self):
		child=self.firstChild
		if not child:
			return None
		presType=child.presentationType
		if presType!=self.presType_content: return child._findSimpleNext(useChild=(presType!=self.presType_unavailable),useParent=False)
		return child

	def _get_simpleLastChild(self):
		child=self.lastChild
		if not child:
			return None
		presType=child.presentationType
		if presType!=self.presType_content: return child._findSimpleNext(useChild=(presType!=self.presType_unavailable),useParent=False,goPrevious=True)
		return child

	def getNextInFlow(self,down=None,up=None):
		"""Retreaves the next object in depth first tree traversal order
@param up: a list that all objects that we moved up out of will be placed in
@type up: list
@param down: a list which all objects we moved down in to will be placed
@type down: list
"""
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		child=self.firstChildPresentable if simpleReviewMode else self.firstChild
		if child:
			if isinstance(down,list):
				down.append(self)
			return child
		next=self.nextPresentable if simpleReviewMode else self.next
		if next:
			return next
		parent=self.parent
		while not next and parent:
			next=parent.nextPresentable if simpleReviewMode else parent.next
			if isinstance(up,list):
				up.append(parent)
			parent=parent.parentPresentable if simpleReviewMode else parent.parent
		return next

	_get_nextInFlow=getNextInFlow

	def getPreviousInFlow(self,down=None,up=None):
		"""Retreaves the previous object in depth first tree traversal order
@param up: a list that all objects that we moved up out of will be placed in
@type up: list
@param down: a list which all objects we moved down in to will be placed
@type down: list
"""
		simpleReviewMode=config.conf["reviewCursor"]["simpleReviewMode"]
		prev=self.previousPresentable if simpleReviewMode else self.previous
		if prev:
			lastLastChild=prev
			lastChild=prev.lastChildPresentable if simpleReviewMode else prev.lastChild
			while lastChild:
				if isinstance(down,list):
					down.append(lastLastChild)
				lastLastChild=lastChild
				lastChild=lastChild.lastChildPresentable if simpleReviewMode else lastChild.lastChild
			return lastLastChild
		parent=self.parentPresentable if simpleReviewMode else self.parent
		if parent:
			if isinstance(up,list):
				up.append(self)
			return parent

	_get_previousInFlow=getPreviousInFlow

	def _get_childCount(self):
		"""Retreaves the number of children this object contains.
		@rtype: int
		"""
		return len(self.children)

	def _get_activeChild(self):
		"""Retreaves the child of this object that currently has, or contains, the focus.
		@return: the active child if it has one else None
		@rtype: L{NVDAObject} or None
		"""
		return None

	def setFocus(self):
		"""
Tries to force this object to take the focus.
"""
		pass

	def scrollIntoView(self):
		"""Scroll this object into view on the screen if possible.
		"""
		raise NotImplementedError

	def _get_labeledBy(self):
		"""Retreaves the object that this object is labeled by (example: the static text label beside an edit field).
		@return: the label object if it has one else None.
		@rtype: L{NVDAObject} or None 
		"""
		return None

	def _get_positionInfo(self):
		"""Retreaves position information for this object such as its level, its index with in a group, and the number of items in that group.
		@return: a dictionary containing any of level, groupIndex and similarItemsInGroup.
		@rtype: dict
		"""
		return {}

	def _get_processID(self):
		"""Retreaves an identifyer of the process this object is a part of.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_isProtected(self):
		"""
		@return: True if this object is protected (hides its input for passwords), or false otherwise
		@rtype: boolean
		"""
		return False

	def _get_isPresentableFocusAncestor(self):
		"""Determine if this object should be presented to the user in the focus ancestry.
		@return: C{True} if it should be presented in the focus ancestry, C{False} if not.
		@rtype: bool
		"""
		if self.presentationType == self.presType_layout:
			return False
		if self.role in (controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_LISTITEM, controlTypes.ROLE_PROGRESSBAR, controlTypes.ROLE_EDITABLETEXT):
			return False
		return True

	def _get_statusBar(self):
		"""Finds the closest status bar in relation to this object.
		@return: the found status bar else None
		@rtype: L{NVDAObject} or None
		"""
		return None

	def speakDescendantObjects(self,hashList=None):
		"""Speaks all the descendants of this object.
		"""
		if hashList is None:
			hashList=[]
		for child in self.children:
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				speech.speakObject(child)
				child.speakDescendantObjects(hashList=hashList)

	def reportFocus(self):
		"""Announces this object in a way suitable such that it gained focus.
		"""
		speech.speakObject(self,reason=speech.REASON_FOCUS)

	def event_typedCharacter(self,ch):
		speech.speakTypedCharacters(ch)


	def event_mouseMove(self,x,y):
		if not self._mouseEntered and config.conf['mouse']['reportObjectRoleOnMouseEnter']:
			speech.cancelSpeech()
			speech.speakObjectProperties(self,role=True)
			speechWasCanceled=True
		else:
			speechWasCanceled=False
		self._mouseEntered=True
		try:
			info=self.makeTextInfo(textInfos.Point(x,y))
			info.expand(info.unit_mouseChunk)
		except:
			info=NVDAObjectTextInfo(self,textInfos.POSITION_ALL)
		if config.conf["reviewCursor"]["followMouse"]:
			api.setReviewPosition(info)
		if not config.conf["mouse"]["reportTextUnderMouse"]:
			return
		oldInfo=getattr(self,'_lastMouseTextInfoObject',None)
		self._lastMouseTextInfoObject=info
		if not oldInfo or info.__class__!=oldInfo.__class__ or info.compareEndPoints(oldInfo,"startToStart")!=0 or info.compareEndPoints(oldInfo,"endToEnd")!=0:
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
		if self.role in (controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM):
			speech.cancelSpeech()
			return
		if self.isPresentableFocusAncestor:
			speech.speakObject(self,reason=speech.REASON_FOCUSENTERED)

	def event_gainFocus(self):
		"""
This code is executed if a gain focus event is received by this object.
"""
		self.reportFocus()
		braille.handler.handleGainFocus(self)

	def event_foreground(self):
		"""Called when the foreground window changes.
		This method should only perform tasks specific to the foreground window changing.
		L{event_focusEntered} or L{event_gainFocus} will be called for this object, so this method should not speak/braille the object, etc.
		"""
		speech.cancelSpeech()

	def event_becomeNavigatorObject(self):
		"""Called when this object becomes the navigator object.
		"""
		braille.handler.handleReviewMove()

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
		if self is api.getFocusObject() and not eventHandler.isPendingEvents("gainFocus"):
			braille.handler.handleCaretMove(self)
			if config.conf["reviewCursor"]["followCaret"]:
				try:
					api.setReviewPosition(self.makeTextInfo(textInfos.POSITION_CARET))
				except (NotImplementedError, RuntimeError):
					pass

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

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

class AutoSelectDetectionNVDAObject(NVDAObject):

	"""Provides an NVDAObject with the means to detect if the text selection has changed, and if so to announce the change
	@ivar hasContentChangedSinceLastSelection: if True then the content has changed.
	@ivar hasContentChangedSinceLastSelection: boolean
	"""

	def initAutoSelectDetection(self):
		"""Initializes the autoSelect detection code so that it knows about what is currently selected."""
		try:
			self._lastSelectionPos=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			self._lastSelectionPos=None
		self.hasContentChangedSinceLastSelection=False

	def detectPossibleSelectionChange(self):
		"""Detects if the selection has been changed, and if so it speaks the change."""
		oldInfo=getattr(self,'_lastSelectionPos',None)
		if not oldInfo:
			return
		try:
			newInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
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
