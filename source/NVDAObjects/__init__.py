# -*- coding: UTF-8 -*-
#NVDAObjects/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2016 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Patrick Zajda
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module that contains the base NVDA object type"""
from new import instancemethod
import time
import re
import weakref
from logHandler import log
import review
import eventHandler
from displayModel import DisplayModelTextInfo
import baseObject
import speech
import api
import textInfos.offsets
import config
import controlTypes
import appModuleHandler
import treeInterceptorHandler
import braille
import globalPluginHandler

class NVDAObjectTextInfo(textInfos.offsets.OffsetsTextInfo):
	"""A default TextInfo which is used to enable text review of information about widgets that don't support text content.
	The L{NVDAObject.basicText} attribute is used as the text to expose.
	"""

	locationText=None

	def _get_unit_mouseChunk(self):
		return textInfos.UNIT_STORY

	def _getStoryText(self):
		return self.obj.basicText

	def _getStoryLength(self):
		return len(self._getStoryText())

	def _getTextRange(self,start,end):
		text=self._getStoryText()
		return text[start:end]

class InvalidNVDAObject(RuntimeError):
	"""Raised by NVDAObjects during construction to inform that this object is invalid.
	In this case, for the purposes of NVDA, the object should be considered non-existent.
	Therefore, L{DynamicNVDAObjectType} will return C{None} if this exception is raised.
	"""

class DynamicNVDAObjectType(baseObject.ScriptableObject.__class__):
	_dynamicClassCache={}

	def __call__(self,chooseBestAPI=True,**kwargs):
		if chooseBestAPI:
			APIClass=self.findBestAPIClass(kwargs)
			if not APIClass: return None
		else:
			APIClass=self

		# Instantiate the requested class.
		try:
			obj=APIClass.__new__(APIClass,**kwargs)
			obj.APIClass=APIClass
			if isinstance(obj,self):
				obj.__init__(**kwargs)
		except InvalidNVDAObject, e:
			log.debugWarning("Invalid NVDAObject: %s" % e, stack_info=True)
			return None

		clsList = []
		if "findOverlayClasses" in APIClass.__dict__:
			obj.findOverlayClasses(clsList)
		else:
			clsList.append(APIClass)
		# Allow app modules to choose overlay classes.
		appModule=obj.appModule
		# optimisation: The base implementation of chooseNVDAObjectOverlayClasses does nothing,
		# so only call this method if it's been overridden.
		if appModule and not hasattr(appModule.chooseNVDAObjectOverlayClasses, "_isBase"):
			appModule.chooseNVDAObjectOverlayClasses(obj, clsList)
		# Allow global plugins to choose overlay classes.
		for plugin in globalPluginHandler.runningPlugins:
			if "chooseNVDAObjectOverlayClasses" in plugin.__class__.__dict__:
				plugin.chooseNVDAObjectOverlayClasses(obj, clsList)

		# Determine the bases for the new class.
		bases=[]
		for index in xrange(len(clsList)):
			# A class doesn't need to be a base if it is already implicitly included by being a superclass of a previous base.
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
			# Bind gestures specified on the class.
			try:
				obj.bindGestures(getattr(cls, "_%s__gestures" % cls.__name__))
			except AttributeError:
				pass

		# Allow app modules to make minor tweaks to the instance.
		if appModule and hasattr(appModule,"event_NVDAObject_init"):
			appModule.event_NVDAObject_init(obj)

		return obj

	@classmethod
	def clearDynamicClassCache(cls):
		"""Clear the dynamic class cache.
		This should be called when a plugin is unloaded so that any used overlay classes in the unloaded plugin can be garbage collected.
		"""
		cls._dynamicClassCache.clear()

class NVDAObject(baseObject.ScriptableObject):
	"""NVDA's representation of a single control/widget.
	Every widget, regardless of how it is exposed by an application or the operating system, is represented by a single NVDAObject instance.
	This allows NVDA to work with all widgets in a uniform way.
	An NVDAObject provides information about the widget (e.g. its name, role and value),
	as well as functionality to manipulate it (e.g. perform an action or set focus).
	Events for the widget are handled by special event methods on the object.
	Commands triggered by input from the user can also be handled by special methods called scripts.
	See L{ScriptableObject} for more details.
	
	The only attribute that absolutely must be provided is L{processID}.
	However, subclasses should provide at least the L{name} and L{role} attributes in order for the object to be meaningful to the user.
	Attributes such as L{parent}, L{firstChild}, L{next} and L{previous} link an instance to other NVDAObjects in the hierarchy.
	In order to facilitate access to text exposed by a widget which supports text content (e.g. an editable text control),
	a L{textInfos.TextInfo} should be implemented and the L{TextInfo} attribute should specify this class.
	
	There are two main types of NVDAObject classes:
		* API classes, which provide the core functionality to work with objects exposed using a particular API (e.g. MSAA/IAccessible).
		* Overlay classes, which supplement the core functionality provided by an API class to handle a specific widget or type of widget.
	Most developers need only be concerned with overlay classes.
	The overlay classes to be used for an instance are determined using the L{findOverlayClasses} method on the API class.
	An L{AppModule} can also choose overlay classes for an instance using the L{AppModule.chooseNVDAObjectOverlayClasses} method.
	"""

	__metaclass__=DynamicNVDAObjectType
	cachePropertiesByDefault = True

	#: The TextInfo class this object should use to provide access to text.
	#: @type: type; L{textInfos.TextInfo}
	TextInfo=NVDAObjectTextInfo

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
		return newAPIClass if newAPIClass is not NVDAObject else None


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
		@param clsList: The list of classes, which will be modified by this method if appropriate.
		@type clsList: list of L{NVDAObject}
		"""
		clsList.append(NVDAObject)

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
		return APIClass(chooseBestAPI=False,**kwargs) if APIClass else None

	@staticmethod
	def objectWithFocus():
		"""Retreaves the object representing the control currently with focus in the Operating System. This differens from NVDA's focus object as this focus object is the real focus object according to the Operating System, not according to NVDA.
		@return: the object with focus.
		@rtype: L{NVDAObject}
		"""
		kwargs={}
		APIClass=NVDAObject.findBestAPIClass(kwargs,relation="focus")
		if not APIClass:
			return None
		obj=APIClass(chooseBestAPI=False,**kwargs)
		if not obj:
			return None
		focusRedirect=obj.focusRedirect
		if focusRedirect:
			obj=focusRedirect
		return obj

	@staticmethod
	def objectInForeground():
		"""Retreaves the object representing the current foreground control according to the Operating System. This differes from NVDA's foreground object as this object is the real foreground object according to the Operating System, not according to NVDA.
		@return: the foreground object
		@rtype: L{NVDAObject}
		"""
		kwargs={}
		APIClass=NVDAObject.findBestAPIClass(kwargs,relation="foreground")
		return APIClass(chooseBestAPI=False,**kwargs) if APIClass else None


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

	focusRedirect=None #: Another object which should be treeted as the focus if focus is ever given to this object.

	def _get_treeInterceptorClass(self):
		"""
		If this NVDAObject should use a treeInterceptor, then this property provides the L{treeInterceptorHandler.TreeInterceptor} class it should use. 
		If not then it should be not implemented.
		"""
		raise NotImplementedError

	#: Whether to create a tree interceptor for this object.
	#: This is only relevant if L{treeInterceptorClass} is valid.
	#: Normally, this should be C{True}.
	#: However, for some objects (e.g. ARIA applications), a tree interceptor shouldn't be used by default,
	#: but the user may wish to override this.
	#: In this case, this can be set to C{False} and updated later.
	#: @type: bool
	shouldCreateTreeInterceptor = True

	def _get_treeInterceptor(self):
		"""Retreaves the treeInterceptor associated with this object.
		If a treeInterceptor has not been specifically set, the L{treeInterceptorHandler} is asked if it can find a treeInterceptor containing this object.
		@return: the treeInterceptor
		@rtype: L{treeInterceptorHandler.TreeInterceptor}
		""" 
		if hasattr(self,'_treeInterceptor'):
			ti=self._treeInterceptor
			if isinstance(ti,weakref.ref):
				ti=ti()
			if ti and ti in treeInterceptorHandler.runningTable:
				return ti
			else:
				self._treeInterceptor=None
				return None
		else:
			ti=treeInterceptorHandler.getTreeInterceptor(self)
			if ti:
				self._treeInterceptor=weakref.ref(ti)
			return ti

	def _set_treeInterceptor(self,obj):
		"""Specifically sets a treeInterceptor to be associated with this object.
		"""
		if obj:
			self._treeInterceptor=weakref.ref(obj)
		else: #We can't point a weakref to None, so just set the private variable to None, it can handle that
			self._treeInterceptor=None

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

	def _get_controllerFor(self):
		"""Retreaves the object/s that this object controls."""
		return []

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

	def _get_locationText(self):
		"""A message that explains the location of the object in friendly terms."""
		location=self.location
		if not location:
			return None
		(left,top,width,height)=location
		deskLocation=api.getDesktopObject().location
		(deskLeft,deskTop,deskWidth,deskHeight)=deskLocation
		percentFromLeft=(float(left-deskLeft)/deskWidth)*100
		percentFromTop=(float(top-deskTop)/deskHeight)*100
		percentWidth=(float(width)/deskWidth)*100
		percentHeight=(float(height)/deskHeight)*100
		# Translators: Reports navigator object's dimensions (example output: object edges positioned 20 per cent from left edge of screen, 10 per cent from top edge of screen, width is 40 per cent of screen, height is 50 per cent of screen).
		return _("Object edges positioned {left:.1f} per cent from left edge of screen, {top:.1f} per cent from top edge of screen, width is {width:.1f} per cent of screen, height is {height:.1f} per cent of screen").format(left=percentFromLeft,top=percentFromTop,width=percentWidth,height=percentHeight)

	def _get_parent(self):
		"""Retreaves this object's parent (the object that contains this object).
		@return: the parent object if it exists else None.
		@rtype: L{NVDAObject} or None
		"""
		return None

	def _get_container(self):
		"""
		Exactly like parent, however another object at this same sibling level may be retreaved first (e.g. a groupbox). Mostly used when presenting context such as focus ancestry.
		"""
		# Cache parent.
		parent = self.parent
		self.parent = parent
		return parent

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

	def getChild(self, index):
		"""Retrieve a child by index.
		@note: Subclasses may override this if they have an efficient way to retrieve a single, arbitrary child.
			The base implementation uses L{children}.
		@param index: The 0-based index of the child to retrieve.
		@type index: int
		@return: The child.
		@rtype: L{NVDAObject}
		"""
		return self.children[index]

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

	def _get_cellCoordsText(self):
		"""
		An alternative text representation of cell coordinates e.g. "a1". Will override presentation of rowNumber and columnNumber.
		Only implement if the representation is really different.
		"""
		return None
		

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

	def _get_rowHeaderText(self):
		"""The text of the row headers for this cell.
		@rtype: str
		"""
		raise NotImplementedError

	def _get_columnHeaderText(self):
		"""The text of the column headers for this cell.
		@rtype: str
		"""
		raise NotImplementedError

	def _get_table(self):
		"""Retreaves the object that represents the table that this object is contained in, if this object is a table cell.
		@rtype: L{NVDAObject}
		"""
		raise NotImplementedError

	def _get_tableID(self):
		"""The identifier of the table associated with this object if it is a table cell.
		This identifier must distinguish this table from other tables.
		If this is not implemented, table cell information will still be reported,
		but row and column information will always be reported
		even if the user moves to a cell in the same row/column.
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

		#Static text should be content only if it really use usable text
		if role==controlTypes.ROLE_STATICTEXT:
			text=self.makeTextInfo(textInfos.POSITION_ALL).text
			return self.presType_content if text and not text.isspace() else self.presType_layout

		if role in (controlTypes.ROLE_UNKNOWN, controlTypes.ROLE_PANE, controlTypes.ROLE_TEXTFRAME, controlTypes.ROLE_ROOTPANE, controlTypes.ROLE_LAYEREDPANE, controlTypes.ROLE_SCROLLPANE, controlTypes.ROLE_SECTION, controlTypes.ROLE_PARAGRAPH, controlTypes.ROLE_TITLEBAR, controlTypes.ROLE_LABEL, controlTypes.ROLE_WHITESPACE,controlTypes.ROLE_BORDER):
			return self.presType_layout
		name = self.name
		description = self.description
		if not name and not description:
			if role in (controlTypes.ROLE_WINDOW,controlTypes.ROLE_PANEL, controlTypes.ROLE_PROPERTYPAGE, controlTypes.ROLE_TEXTFRAME, controlTypes.ROLE_GROUPING,controlTypes.ROLE_OPTIONPANE,controlTypes.ROLE_INTERNALFRAME,controlTypes.ROLE_FORM,controlTypes.ROLE_TABLEBODY):
				return self.presType_layout
			if role == controlTypes.ROLE_TABLE and not config.conf["documentFormatting"]["reportTables"]:
				return self.presType_layout
			if role in (controlTypes.ROLE_TABLEROW,controlTypes.ROLE_TABLECOLUMN,controlTypes.ROLE_TABLECELL) and (not config.conf["documentFormatting"]["reportTables"] or not config.conf["documentFormatting"]["reportTableCellCoords"]):
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

	def _get_isFocusable(self):
		"""Whether this object is focusable.
		@rtype: bool
		"""
		return controlTypes.STATE_FOCUSABLE in self.states

	def _get_hasFocus(self):
		"""Whether this object has focus.
		@rtype: bool
		"""
		return controlTypes.STATE_FOCUSED in self.states

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

	def _get_indexInParent(self):
		"""The index of this object in its parent object.
		@return: The 0 based index, C{None} if there is no parent.
		@rtype: int
		@raise NotImplementedError: If not supported by the underlying object.
		"""
		raise NotImplementedError

	def _get_flowsTo(self):
		"""The object to which content flows from this object.
		@return: The object to which this object flows, C{None} if none.
		@rtype: L{NVDAObject}
		@raise NotImplementedError: If not supported by the underlying object.
		"""
		raise NotImplementedError

	def _get_flowsFrom(self):
		"""The object from which content flows to this object.
		@return: The object from which this object flows, C{None} if none.
		@rtype: L{NVDAObject}
		@raise NotImplementedError: If not supported by the underlying object.
		"""
		raise NotImplementedError

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

	def reportFocus(self):
		"""Announces this object in a way suitable such that it gained focus.
		"""
		speech.speakObject(self,reason=controlTypes.REASON_FOCUS)

	def _reportErrorInPreviousWord(self):
		try:
			# self might be a descendant of the text control; e.g. Symphony.
			# We want to deal with the entire text, so use the caret object.
			info = api.getCaretObject().makeTextInfo(textInfos.POSITION_CARET)
			# This gets called for characters which might end a word; e.g. space.
			# The character before the caret is the word end.
			# The one before that is the last of the word, which is what we want.
			info.move(textInfos.UNIT_CHARACTER, -2)
			info.expand(textInfos.UNIT_CHARACTER)
			fields = info.getTextWithFields()
		except RuntimeError:
			return
		except:
			# Focus probably moved.
			log.debugWarning("Error fetching last character of previous word", exc_info=True)
			return
		for command in fields:
			if isinstance(command, textInfos.FieldCommand) and command.command == "formatChange" and command.field.get("invalid-spelling"):
				break
		else:
			# No error.
			return
		import nvwave
		nvwave.playWaveFile(r"waves\textError.wav")

	def event_typedCharacter(self,ch):
		if config.conf["documentFormatting"]["reportSpellingErrors"] and config.conf["keyboard"]["alertForSpellingErrors"] and (
			# Not alpha, apostrophe or control.
			ch.isspace() or (ch >= u" " and ch not in u"'\x7f" and not ch.isalpha())
		):
			# Reporting of spelling errors is enabled and this character ends a word.
			self._reportErrorInPreviousWord()
		speech.speakTypedCharacters(ch)
		import winUser
		if config.conf["keyboard"]["beepForLowercaseWithCapslock"] and ch.islower() and winUser.getKeyState(winUser.VK_CAPITAL)&1:
			import tones
			tones.beep(3000,40)

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
		except NotImplementedError:
			info=NVDAObjectTextInfo(self,textInfos.POSITION_FIRST)
		except LookupError:
			return
		if config.conf["reviewCursor"]["followMouse"]:
			api.setReviewPosition(info)
		info.expand(info.unit_mouseChunk)
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
			speech.speakObjectProperties(self,states=True, reason=controlTypes.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_focusEntered(self):
		if self.role in (controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM):
			speech.cancelSpeech()
			return
		if self.isPresentableFocusAncestor:
			speech.speakObject(self,reason=controlTypes.REASON_FOCUSENTERED)

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
			speech.speakObjectProperties(self, value=True, reason=controlTypes.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_nameChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, name=True, reason=controlTypes.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_descriptionChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, description=True, reason=controlTypes.REASON_CHANGE)
		braille.handler.handleUpdate(self)

	def event_caret(self):
		if self is api.getFocusObject() and not eventHandler.isPendingEvents("gainFocus"):
			braille.handler.handleCaretMove(self)
			review.handleCaretMove(self)

	def _get_flatReviewPosition(self):
		"""Locates a TextInfo positioned at this object, in the closest flat review."""
		parent=self.simpleParent
		while parent:
			ti=parent.treeInterceptor
			if ti and self in ti and ti.rootNVDAObject==parent:
				return ti.makeTextInfo(self)
			if issubclass(parent.TextInfo,DisplayModelTextInfo):
				try:
					return parent.makeTextInfo(api.getReviewPosition().pointAtStart)
				except (NotImplementedError,LookupError):
					pass
				try:
					return parent.makeTextInfo(self)
				except (NotImplementedError,RuntimeError):
					pass
				return parent.makeTextInfo(textInfos.POSITION_FIRST)
			parent=parent.simpleParent

	def _get_basicText(self):
		newTime=time.time()
		oldTime=getattr(self,'_basicTextTime',0)
		if newTime-oldTime>0.5:
			self._basicText=u" ".join([x for x in self.name, self.value, self.description if isinstance(x, basestring) and len(x) > 0 and not x.isspace()])
			if len(self._basicText)==0:
				self._basicText=u""
		else:
			self._basicTextTime=newTime
		return self._basicText

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	@staticmethod
	def _formatLongDevInfoString(string, truncateLen=250):
		"""Format a potentially long string value for inclusion in devInfo.
		This should be used for arbitrary string values which aren't usually useful in debugging past a certain length.
		If the string is too long to be useful, it will be truncated.
		This string should be included as returned. There is no need to call repr.
		@param string: The string to format.
		@type string: nbasestring
		@param truncateLen: The length at which to truncate the string.
		@type truncateLen: int
		@return: The formatted string.
		@rtype: basestring
		"""
		if isinstance(string, basestring) and len(string) > truncateLen:
			return "%r (truncated)" % string[:truncateLen]
		return repr(string)

	def _get_devInfo(self):
		"""Information about this object useful to developers.
		Subclasses may extend this, calling the superclass property first.
		@return: A list of text strings providing information about this object useful to developers.
		@rtype: list of str
		"""
		info = []
		try:
			ret = repr(self.name)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("name: %s" % ret)
		try:
			ret = self.role
			for name, const in controlTypes.__dict__.iteritems():
				if name.startswith("ROLE_") and ret == const:
					ret = name
					break
		except Exception as e:
			ret = "exception: %s" % e
		info.append("role: %s" % ret)
		try:
			stateConsts = dict((const, name) for name, const in controlTypes.__dict__.iteritems() if name.startswith("STATE_"))
			ret = ", ".join(
				stateConsts.get(state) or str(state)
				for state in self.states)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("states: %s" % ret)
		try:
			ret = repr(self.isFocusable)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("isFocusable: %s" % ret)
		try:
			ret = repr(self.hasFocus)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("hasFocus: %s" % ret)
		try:
			ret = repr(self)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("Python object: %s" % ret)
		try:
			ret = repr(self.__class__.__mro__)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("Python class mro: %s" % ret)
		try:
			ret = repr(self.description)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("description: %s" % ret)
		try:
			ret = repr(self.location)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("location: %s" % ret)
		formatLong = self._formatLongDevInfoString
		try:
			ret = formatLong(self.value)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("value: %s" % ret)
		try:
			ret = repr(self.appModule)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("appModule: %s" % ret)
		try:
			ret = repr(self.appModule.productName)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("appModule.productName: %s" % ret)
		try:
			ret = repr(self.appModule.productVersion)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("appModule.productVersion: %s" % ret)
		try:
			ret = repr(self.TextInfo)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("TextInfo: %s" % ret)
		return info

	def _get_sleepMode(self):
		"""Whether NVDA should sleep for this object (e.g. it is self-voicing).
		If C{True}, all  events and script requests for this object are silently dropped.
		@rtype: bool
		"""
		if self.appModule:
			return self.appModule.sleepMode
		return False
	# Don't cache sleepMode, as it is derived from a property which might change
	# and we want the changed value immediately.
	_cache_sleepMode = False

	def _get_mathMl(self):
		"""Obtain the MathML markup for an object containing math content.
		This will only be called (and thus only needs to be implemented) for
		objects with a role of L{controlTypes.ROLE_MATH}.
		@raise LookupError: If MathML can't be retrieved for this object.
		"""
		raise NotImplementedError

	#: The language/locale of this object.
	#: @type: basestring
	language = None
