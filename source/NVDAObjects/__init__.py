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
from keyUtils import key, sendKey
from scriptHandler import isScriptWaiting
import globalVars
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

	def __call__(self,*args,**kwargs):
		if 'findBestAPIClass' not in self.__dict__:
			APIClass=self
		else:
			APIClass=self.findBestAPIClass(**kwargs)

		if 'findOverlayClasses' not in APIClass.__dict__:
			raise TypeError("Cannot instantiate class %s as it does not implement findOverlayClasses"%APIClass.__name__)

		# Instantiate the requested class.
		obj=APIClass.__new__(APIClass,*args,**kwargs)
		obj.APIClass=APIClass
		if isinstance(obj,self):
			obj.__init__(*args,**kwargs)

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
	def findBestAPIClass(cls):
		"""Chooses the most appropriate API-level NVDAObject class that should be used instead of this class.
		An API-level NVDAObject is an NVDAObject that takes a specific set of arguments for instanciation.
		@return: the suitable API-level subclass.
		@rtype: L{NVDAObject} class
		"""  
		return cls

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

	@classmethod
	def objectFromPoint(x,y):
		"""Retreaves an NVDAObject instance representing a control in the Operating System at the given x and y coordinates.
		@param x: the x coordinate.
		@type x: int
		@param y: the y coordinate.
		@param y: int
		@return: The object at the given x and y coordinates.
		@rtype: L{NVDAObject}
		"""
		raise NotImplementedError

	@classmethod
	def objectWithFocus(cls):
		"""Retreaves the object representing the control currently with focus in the Operating System. This differens from NVDA's focus object as this focus object is the real focus object according to the Operating System, not according to NVDA.
		@return: the object with focus.
		@rtype: L{NVDAObject}
		"""
		raise NotImplementedError

	@classmethod
	def objectInForeground(cls):
		"""Retreaves the object representing the current foreground control according to the Operating System. This differes from NVDA's foreground object as this object is the real foreground object according to the Operating System, not according to NVDA.
		@return: the foreground object
		@rtype: L{NVDAObject}
		"""
		raise NotImplementedError

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
		role = self.role
		if role in (controlTypes.ROLE_UNKNOWN, controlTypes.ROLE_PANE, controlTypes.ROLE_ROOTPANE, controlTypes.ROLE_LAYEREDPANE, controlTypes.ROLE_SCROLLPANE, controlTypes.ROLE_SECTION, controlTypes.ROLE_TREEVIEWITEM, controlTypes.ROLE_LISTITEM, controlTypes.ROLE_PARAGRAPH, controlTypes.ROLE_PROGRESSBAR, controlTypes.ROLE_EDITABLETEXT):
			return False
		name = self.name
		description = self.description
		if role in (controlTypes.ROLE_WINDOW,controlTypes.ROLE_LABEL,controlTypes.ROLE_PANEL, controlTypes.ROLE_PROPERTYPAGE, controlTypes.ROLE_TEXTFRAME, controlTypes.ROLE_GROUPING,controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_OPTIONPANE,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_FORM) and not name and not description:
			return False
		if not name and not description and role in (controlTypes.ROLE_TABLE,controlTypes.ROLE_TABLEROW,controlTypes.ROLE_TABLECOLUMN,controlTypes.ROLE_TABLECELL) and not config.conf["documentFormatting"]["reportTables"]:
			return False
		if role in (controlTypes.ROLE_TABLEROW,controlTypes.ROLE_TABLECOLUMN):
			try:
				table=self.table
			except NotImplementedError:
				table=None
			if table:
				# This is part of a real table, so the cells will report row/column information.
				# Therefore, we don't want to present this in the ancestry.
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
		if not config.conf['mouse']['reportTextUnderMouse']:
			return
		try:
			info=self.makeTextInfo(textInfos.Point(x,y))
			info.expand(info.unit_mouseChunk)
		except:
			info=NVDAObjectTextInfo(self,textInfos.POSITION_ALL)
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
			if globalVars.caretMovesReviewCursor:
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
				newBookmark = self.makeTextInfo(textInfos.POSITION_CARET).bookmark
				if newBookmark!=bookmark:
					return True
			except:
				pass
			time.sleep(retryInterval)
			elapsed += retryInterval
		return False

	def script_moveByLine(self,keyPress):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
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
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_LINE)
			speech.speakTextInfo(info)

	def script_moveByCharacter(self,keyPress):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
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
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER)

	def script_moveByWord(self,keyPress):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
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
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_WORD)
			speech.speakTextInfo(info,unit=textInfos.UNIT_WORD)

	def script_moveByParagraph(self,keyPress):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
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
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_PARAGRAPH)
			speech.speakTextInfo(info)

	def _backspaceScriptHelper(self,unit,keyPress):
		try:
			oldInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			sendKey(keyPress)
			return
		oldBookmark=oldInfo.bookmark
		testInfo=oldInfo.copy()
		res=testInfo.move(textInfos.UNIT_CHARACTER,-1)
		if res<0:
			testInfo.expand(unit)
			delChunk=testInfo.text
		else:
			delChunk=""
		sendKey(keyPress)
		if self._hasCaretMoved(oldBookmark):
			if len(delChunk)>1:
				speech.speakMessage(delChunk)
			else:
				speech.speakSpelling(delChunk)
			focus=api.getFocusObject()
			try:
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info)

	def script_backspaceCharacter(self,keyPress):
		self._backspaceScriptHelper(textInfos.UNIT_CHARACTER,keyPress)

	def script_backspaceWord(self,keyPress):
		self._backspaceScriptHelper(textInfos.UNIT_WORD,keyPress)

	def script_delete(self,keyPress):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
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
				info=focus.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(info.copy())
			info.expand(textInfos.UNIT_CHARACTER)
			speech.speakTextInfo(info,unit=textInfos.UNIT_CHARACTER)

	def script_changeSelection(self,keyPress):
		try:
			oldInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			sendKey(keyPress)
			return
		sendKey(keyPress)
		if not isScriptWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			try:
				newInfo=focus.makeTextInfo(textInfos.POSITION_SELECTION)
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
