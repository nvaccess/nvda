# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Patrick Zajda, Babbage B.V.,
# Davy Kager
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Module that contains the base NVDA object type with dynamic class creation support,
as well as the associated TextInfo class."""

import time
import typing
import weakref
import textUtils
from logHandler import log
import review
import eventHandler
from displayModel import DisplayModelTextInfo
import baseObject
import documentBase
import speech
import ui
import api
import textInfos.offsets
import config
import controlTypes
import appModuleHandler
import treeInterceptorHandler
import braille
import vision
import globalPluginHandler
import brailleInput
import locationHelper
import aria


class NVDAObjectTextInfo(textInfos.offsets.OffsetsTextInfo):
	"""A default TextInfo which is used to enable text review of information about widgets that don't support text content.
	The L{NVDAObject.basicText} attribute is used as the text to expose.
	"""

	locationText=None
	# Do not use encoded text.
	encoding = None

	def _get_unit_mouseChunk(self):
		return textInfos.UNIT_STORY

	def _getStoryText(self):
		return self.obj.basicText

	def _getStoryLength(self):
		return len(self._getStoryText())

	def _get_boundingRects(self):
		if self.obj.hasIrrelevantLocation:
			raise LookupError("Object is off screen, invisible or has no location")
		return [self.obj.location,]

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
		except InvalidNVDAObject as e:
			log.debugWarning("Invalid NVDAObject: %s" % e, exc_info=True)
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
			try:
				appModule.chooseNVDAObjectOverlayClasses(obj, clsList)
			except Exception:
				log.exception(f"Exception in chooseNVDAObjectOverlayClasses for {appModule}")
				pass

		# Allow global plugins to choose overlay classes.
		for plugin in globalPluginHandler.runningPlugins:
			if "chooseNVDAObjectOverlayClasses" in plugin.__class__.__dict__:
				try:
					plugin.chooseNVDAObjectOverlayClasses(obj, clsList)
				except Exception:
					log.exception(f"Exception in chooseNVDAObjectOverlayClasses for {plugin}")
					pass

		# Determine the bases for the new class.
		bases=[]
		for index in range(len(clsList)):
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
				newCls=type(name,bases,{"__module__": __name__})
				self._dynamicClassCache[bases]=newCls

		oldMro=frozenset(obj.__class__.__mro__)
		# Mutate obj into the new class.
		obj.__class__=newCls

		# Initialise the overlay classes.
		for cls in reversed(newCls.__mro__):
			if cls in oldMro:
				# This class was part of the initially constructed object, so its constructor would have been called.
				continue
			initFunc = cls.__dict__.get("initOverlayClass")
			if initFunc:
				try:
					initFunc(obj)
				except Exception:
					log.exception(f"Exception in initOverlayClass for {cls}")
					continue
			# Bind gestures specified on the class.
			try:
				obj.bindGestures(getattr(cls, "_%s__gestures" % cls.__name__))
			except AttributeError:
				pass

		# Allow app modules to make minor tweaks to the instance.
		if appModule and hasattr(appModule,"event_NVDAObject_init"):
			try:
				appModule.event_NVDAObject_init(obj)
			except Exception:
				log.exception(f"Exception in event_NVDAObject_init for {appModule}")
				pass

		return obj

	@classmethod
	def clearDynamicClassCache(cls):
		"""Clear the dynamic class cache.
		This should be called when a plugin is unloaded so that any used overlay classes in the unloaded plugin can be garbage collected.
		"""
		cls._dynamicClassCache.clear()

class NVDAObject(documentBase.TextContainerObject, baseObject.ScriptableObject, metaclass=DynamicNVDAObjectType):
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

	cachePropertiesByDefault = True

	#: The TextInfo class this object should use to provide access to text.
	#: @type: type; L{textInfos.TextInfo}
	TextInfo=NVDAObjectTextInfo

	#: Indicates if the text selection is anchored at the start.
	#: The anchored position is the end that doesn't move when extending or shrinking the selection.
	#: For example, if you have no selection and you press shift+rightArrow to select the next character,
	#: this will be True.
	#: In contrast, if you have no selection and you press shift+leftArrow to select the previous character,
	#: this will be False.
	#: If the selection is anchored at the end or there is no information this is C{False}.
	#: @type: bool
	isTextSelectionAnchoredAtStart=True

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
		"""Retrieves an NVDAObject instance representing a control in the Operating System at the given x and y coordinates.
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
		"""Retrieves the object representing the control currently with focus in the Operating System. This differens from NVDA's focus object as this focus object is the real focus object according to the Operating System, not according to NVDA.
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
		"""Retrieves the object representing the current foreground control according to the
		Operating System. This may differ from NVDA's cached foreground object.
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
 
	# As __eq__ was defined on this class, we must provide __hash__ to remain hashable.
	# The default hash implementation is fine for  our purposes.
	def __hash__(self):
		return super().__hash__()

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

	#: Type definition for auto prop '_get_treeInterceptor'
	treeInterceptor: treeInterceptorHandler.TreeInterceptor

	def _get_treeInterceptor(self) -> treeInterceptorHandler.TreeInterceptor:
		"""Retrieves the treeInterceptor associated with this object.
		If a treeInterceptor has not been specifically set,
		the L{treeInterceptorHandler} is asked if it can find a treeInterceptor containing this object.
		@return: the treeInterceptor
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

	#: Type definition for auto prop '_get_appModule'
	appModule: "appModuleHandler.AppModule"

	def _get_appModule(self) -> "appModuleHandler.AppModule":
		"""Retrieves the appModule representing the application this object is a part of by
		asking L{appModuleHandler}.
		@return: the appModule
		"""
		if not hasattr(self,'_appModuleRef'):
			a=appModuleHandler.getAppModuleForNVDAObject(self)
			if a:
				self._appModuleRef=weakref.ref(a)
				return a
		else:
			return self._appModuleRef()

	#: Type definition for auto prop '_get_name'
	name: str

	def _get_name(self) -> str:
		"""The name or label of this object (example: the text of a button).
		"""
		return ""

	#: Type definition for auto prop '_get_role'
	role: controlTypes.Role

	def _get_role(self) -> controlTypes.Role:
		"""The role or type of control this object represents (example: button, list, dialog).
		"""  
		return controlTypes.Role.UNKNOWN

	#: Type definition for auto prop '_get_roleText'
	roleText: typing.Optional[str]

	def _get_roleText(self) -> typing.Optional[str]:
		"""
		A custom role string for this object, which is used for braille and speech presentation, which will override the standard label for this object's role property.
		No string is provided by default, meaning that NVDA will fall back to using role.
		Examples of where this property might be overridden are shapes in Powerpoint, or ARIA role descriptions.
		"""
		if self.landmark and self.landmark in aria.landmarkRoles:
			return f"{aria.landmarkRoles[self.landmark]} {controlTypes.Role.LANDMARK.displayString}"
		return None

	def _get_roleTextBraille(self):
		"""
		A custom role string for this object, which is used for braille presentation,
		which will override the standard label for this object's role property as well as the value of roleText.
		By default, NVDA falls back to using roleText.
		"""
		if self.landmark and self.landmark in braille.landmarkLabels:
			return f"{braille.roleLabels[controlTypes.Role.LANDMARK]} {braille.landmarkLabels[self.landmark]}"
		return self.roleText

	#: Typing information for auto property _get_value
	value: str

	def _get_value(self) -> str:
		"""The value of this object
		(example: the current percentage of a scrollbar, the selected option in a combo box).
		"""   
		return ""

	#: Typing information for auto property _get_description
	description: str

	def _get_description(self) -> str:
		"""The description or help text of this object.
		"""
		return ""

	#: Typing information for auto property _get_descriptionFrom
	descriptionFrom: controlTypes.DescriptionFrom

	def _get_descriptionFrom(self) -> controlTypes.DescriptionFrom:
		return controlTypes.DescriptionFrom.UNKNOWN

	#: Typing information for auto property _get_detailsSummary
	detailsSummary: typing.Optional[str]

	def _get_detailsSummary(self) -> typing.Optional[str]:
		if config.conf["debugLog"]["annotations"]:
			log.debugWarning(f"Fetching details summary not supported on: {self.__class__.__qualname__}")
		return None

	@property
	def hasDetails(self) -> bool:
		"""Default implementation is based on the result of _get_detailsSummary
		In most instances this should be optimised.
		"""
		return bool(self.detailsSummary)

	def _get_controllerFor(self):
		"""Retrieves the object/s that this object controls."""
		return []

	def _get_actionCount(self):
		"""Retrieves the number of actions supported by this object."""
		return 0

	def getActionName(self,index=None):
		"""Retrieves the name of an action supported by this object.
		If index is not given then the default action will be used if it exists.
		@param index: the optional 0-based index of the wanted action.
		@type index: int
		@return: the action's name
		@rtype: str
		"""
		raise NotImplementedError
 
	def doAction(self,index=None):
		"""Performs an action supported by this object.
		If index is not given then the default action will be used if it exists.
		"""
		raise NotImplementedError

	def _get_defaultActionIndex(self):
		"""Retrieves the index of the action that is the default."""
		return 0

	def _get_keyboardShortcut(self):
		"""The shortcut key that activates this object(example: alt+t).
		@rtype: str
		"""
		return ""

	def _get_isInForeground(self):
		"""
		Finds out if this object is currently within the foreground.
		"""
		raise NotImplementedError

	# Type info for auto property:
	states: typing.Set[controlTypes.State]

	def _get_states(self) -> typing.Set[controlTypes.State]:
		"""Retrieves the current states of this object (example: selected, focused).
		@return: a set of State constants from L{controlTypes}.
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

	#: Typing information for auto-property: _get_parent
	parent: typing.Optional['NVDAObject']
	"This object's parent (the object that contains this object)."

	def _get_parent(self) -> typing.Optional['NVDAObject']:
		"""Retrieves this object's parent (the object that contains this object).
		@return: the parent object if it exists else None.
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

	#: Typing information for auto-property: _get_next
	next: typing.Optional['NVDAObject']
	"The object directly after this object with the same parent."

	def _get_next(self) -> typing.Optional['NVDAObject']:
		"""Retrieves the object directly after this object with the same parent.
		@return: the next object if it exists else None.
		"""
		return None

	#: Typing information for auto-property: _get_previous
	previous: typing.Optional['NVDAObject']
	"The object directly before this object with the same parent."

	def _get_previous(self) -> typing.Optional['NVDAObject']:
		"""Retrieves the object directly before this object with the same parent.
		@return: the previous object if it exists else None.
		"""
		return None

	#: Type definition for auto prop '_get_firstChild'
	firstChild: typing.Optional["NVDAObject"]

	def _get_firstChild(self) -> typing.Optional["NVDAObject"]:
		"""Retrieves the first object that this object contains.
		@return: the first child object if it exists else None.
		"""
		return None

	#: Type definition for auto prop '_get_lastChild'
	lastChild: typing.Optional["NVDAObject"]

	def _get_lastChild(self) -> typing.Optional["NVDAObject"]:
		"""Retrieves the last object that this object contains.
		@return: the last child object if it exists else None.
		"""
		return None

	#: Type definition for auto prop '_get_children'
	children: typing.List["NVDAObject"]

	def _get_children(self):
		"""Retrieves a list of all the objects directly contained by this object (who's parent is this object).
		@rtype: list of L{NVDAObject}
		"""
		log.debugWarning(
			"Base implementation used."
			" Relies on child.next which is error prone in many IA2 implementations."
		)
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children

	def getChild(self, index: int) -> "NVDAObject":
		"""Retrieve a child by index.
		@note: Subclasses may override this if they have an efficient way to retrieve a single, arbitrary child.
			The base implementation uses L{children}.
		@param index: The 0-based index of the child to retrieve.
		@return: The child.
		"""
		return self.children[index]

	def _get_rowNumber(self):
		"""Retrieves the row number of this object if it is in a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_presentationalRowNumber(self):
		"""
		An optional version of the rowNumber property 
		used purely for speech and braille presentation if implemented.
		This is never used for navigational logic.
		This property should be implemented if the table has virtual content which may not all be loaded at one time.
		For example, a table with 1000 rows and 1000 columns, 
		yet the table only shows perhaps 10 rows by 10 columns at a time.
		Although the  rowNumber might be row 2 of 10, 
		the user needs to  be told it is perhaps row 500 (taking all virtual rows into account).
		If the underlying APIs do not distinguish between virtual and physical cell coordinates, 
		then this property should not be implemented.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_columnNumber(self):
		"""Retrieves the column number of this object if it is in a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_presentationalColumnNumber(self):
		"""
		An optional version of the columnNumber property 
		used purely for speech and braille presentation if implemented.
		This is never used for navigational logic.
		This property should be implemented if the table has virtual content which may not all be loaded at one time.
		For example, a table with 1000 rows and 1000 columns, 
		yet the table only shows perhaps 10 rows by 10 columns at a time.
		Although the  columnNumber might be column 2 of 10, 
		the user needs to  be told it is perhaps column 500 (taking all virtual columns into account).
		If the underlying APIs do not distinguish between virtual and physical cell coordinates, 
		then this property should not be implemented.
		@rtype: int
		"""
		raise NotImplementedError

	#: Typing information for auto-property: _get_cellCoordsText
	cellCoordsText: typing.Optional[str]

	def _get_cellCoordsText(self) -> typing.Optional[str]:
		"""
		An alternative text representation of cell coordinates e.g. "a1". Will override presentation of rowNumber and columnNumber.
		Only implement if the representation is really different.
		"""
		return None

	def _get_rowCount(self):
		"""Retrieves the number of rows this object contains if its a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_presentationalRowCount(self):
		"""
		An optional version of the rowCount property 
		used purely for speech and braille presentation if implemented.
		This is never used for navigational logic.
		This property should be implemented if the table has virtual content which may not all be loaded at one time.
		For example, a table with 1000 rows and 1000 columns, 
		yet the table only shows perhaps 10 rows by 10 columns at a time.
		Although the  rowCount might be 10, 
		the user needs to  be told the table really has 1000 rows. 
		If the underlying APIs do not distinguish between virtual and physical cell coordinates, 
		then this property should not be implemented.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_columnCount(self):
		"""Retrieves the number of columns this object contains if its a table.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_presentationalColumnCount(self):
		"""
		An optional version of the columnCount property 
		used purely for speech and braille presentation if implemented.
		This is never used for navigational logic.
		This property should be implemented if the table has virtual content which may not all be loaded at one time.
		For example, a table with 1000 rows and 1000 columns, 
		yet the table only shows perhaps 10 rows by 10 columns at a time.
		Although the  columnCount might be 10, 
		the user needs to  be told the table really has 1000 columns. 
		If the underlying APIs do not distinguish between virtual and physical cell coordinates, 
		then this property should not be implemented.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_rowSpan(self):
		"""The number of rows spanned by this cell.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_rowHeaderText(self):
		"""The text of the row headers for this cell.
		@rtype: str
		"""
		raise NotImplementedError

	def _get_columnSpan(self):
		"""The number of columns spanned by this cell.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_columnHeaderText(self):
		"""The text of the column headers for this cell.
		@rtype: str
		"""
		raise NotImplementedError

	def _get_table(self):
		"""Retrieves the object that represents the table that this object is contained in, if this object is a table cell.
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
		if controlTypes.State.INVISIBLE in states or controlTypes.State.UNAVAILABLE in states:
			return self.presType_unavailable
		role = self.role
		landmark = self.landmark
		if (
			role in (controlTypes.Role.LANDMARK, controlTypes.Role.REGION) or landmark
		) and not config.conf["documentFormatting"]["reportLandmarks"]:
			return self.presType_layout

		roleText = self.roleText
		if roleText:
			# If roleText is set, the object is very likely to communicate something relevant to the user.
			return self.presType_content

		#Static text should be content only if it really use usable text
		if role==controlTypes.Role.STATICTEXT:
			text=self.makeTextInfo(textInfos.POSITION_ALL).text
			return self.presType_content if text and not text.isspace() else self.presType_layout

		if role in (
			controlTypes.Role.UNKNOWN,
			controlTypes.Role.PANE,
			controlTypes.Role.TEXTFRAME,
			controlTypes.Role.ROOTPANE,
			controlTypes.Role.LAYEREDPANE,
			controlTypes.Role.SCROLLPANE,
			controlTypes.Role.SPLITPANE,
			controlTypes.Role.SECTION,
			controlTypes.Role.PARAGRAPH,
			controlTypes.Role.TITLEBAR,
			controlTypes.Role.LABEL,
			controlTypes.Role.WHITESPACE,
			controlTypes.Role.BORDER
		):
			return self.presType_layout
		name = self.name
		description = self.description
		if not name and not description:
			if role in (
				controlTypes.Role.WINDOW,
				controlTypes.Role.PANEL,
				controlTypes.Role.PROPERTYPAGE,
				controlTypes.Role.TEXTFRAME,
				controlTypes.Role.GROUPING,
				controlTypes.Role.OPTIONPANE,
				controlTypes.Role.INTERNALFRAME,
				controlTypes.Role.FORM,
				controlTypes.Role.TABLEBODY,
				controlTypes.Role.REGION,
			):
				return self.presType_layout
			if role == controlTypes.Role.TABLE and not config.conf["documentFormatting"]["reportTables"]:
				return self.presType_layout
			if role in (controlTypes.Role.TABLEROW,controlTypes.Role.TABLECOLUMN,controlTypes.Role.TABLECELL) and (not config.conf["documentFormatting"]["reportTables"] or not config.conf["documentFormatting"]["reportTableCellCoords"]):
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
		"""Retrieves the number of children this object contains.
		@rtype: int
		"""
		return len(self.children)

	def _get_activeChild(self):
		"""Retrieves the child of this object that currently has, or contains, the focus.
		@return: the active child if it has one else None
		@rtype: L{NVDAObject} or None
		"""
		return None

	def _get_isFocusable(self):
		"""Whether this object is focusable.
		@rtype: bool
		"""
		return controlTypes.State.FOCUSABLE in self.states

	def _get_hasFocus(self):
		"""Whether this object has focus.
		@rtype: bool
		"""
		return controlTypes.State.FOCUSED in self.states

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
		"""Retrieves the object that this object is labeled by (example: the static text label beside an edit field).
		@return: the label object if it has one else None.
		@rtype: L{NVDAObject} or None 
		"""
		return None

	def _get_positionInfo(self):
		"""Retrieves position information for this object such as its level, its index with in a group, and the number of items in that group.
		@return: a dictionary containing any of level, groupIndex and similarItemsInGroup.
		@rtype: dict
		"""
		return {}

	def _get_processID(self):
		"""Retrieves an identifyer of the process this object is a part of.
		@rtype: int
		"""
		raise NotImplementedError

	def _get_isProtected(self):
		"""
		@return: True if this object is protected (hides its input for passwords), or false otherwise
		@rtype: boolean
		"""
		# Objects with the protected state, or with a role of passWordEdit should always be protected.
		isProtected=(controlTypes.State.PROTECTED in self.states or self.role==controlTypes.Role.PASSWORDEDIT)
		# #7908: If this object is currently protected, keep it protected for the rest of its lifetime.
		# The most likely reason it would lose its protected state is because the object is dying.
		# In this case it is much more secure to assume it is still protected, thus the end of PIN codes will not be accidentally reported. 
		if isProtected:
			self.isProtected=isProtected
		return isProtected

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
		if self.presentationType in (self.presType_layout, self.presType_unavailable):
			return False
		if self.role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.LISTITEM, controlTypes.Role.PROGRESSBAR, controlTypes.Role.EDITABLETEXT):
			return False
		return True

	def _get_statusBar(self):
		"""Finds the closest status bar in relation to this object.
		@return: the found status bar else None
		@rtype: L{NVDAObject} or None
		"""
		return None

	isCurrent: controlTypes.IsCurrent  #: type info for auto property _get_isCurrent

	def _get_isCurrent(self) -> controlTypes.IsCurrent:
		"""Gets the value that indicates whether this object is the current element in a set of related 
		elements. This maps to aria-current.
		"""
		return controlTypes.IsCurrent.NO

	def _get_shouldAcceptShowHideCaretEvent(self):
		"""Some objects/applications send show/hide caret events when we don't expect it, such as when the cursor is blinking.
		@return: if show/hide caret events should be accepted for this object.
		@rtype: Boolean
		"""
		return True

	def reportFocus(self):
		"""Announces this object in a way suitable such that it gained focus.
		"""
		speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS)

	def _get_placeholder(self):
		"""If it exists for this object get the value of the placeholder text.
		For example this might be the aria-placeholder text for a field in a web page.
		@return: the placeholder text else None
		@rtype: String or None
		"""
		log.debug("Potential unimplemented child class: %r" %self)
		return None

	landmark: typing.Optional[str]
	"""Typing information for auto property _get_landmark
	"""

	def _get_landmark(self) -> typing.Optional[str]:
		"""If this object represents an ARIA landmark, fetches the ARIA landmark role.
		@return: ARIA landmark role else None
		"""
		return None

	def _get_liveRegionPoliteness(self) -> aria.AriaLivePoliteness:
		""" Retrieves the priority with which  updates to live regions should be treated.
		The base implementation returns C{aria.AriaLivePoliteness.OFF},
		indicating that the object isn't a live region.
		Subclasses supporting live region events must implement this.
		"""
		return aria.AriaLivePoliteness.OFF

	def event_liveRegionChange(self):
		"""
		A base implementation for live region change events.
		"""
		name = self.name
		if name:
			politeness = self.liveRegionPoliteness
			if politeness == aria.AriaLivePoliteness.OFF:
				log.debugWarning("Processing live region event for object with live politeness set to 'OFF'")
			ui.message(
				name,
				speechPriority=(
					speech.priorities.Spri.NEXT
					if politeness == aria.AriaLivePoliteness.ASSERTIVE
					else speech.priorities.Spri.NORMAL
				)
			)

	def event_typedCharacter(self,ch):
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
		vision.handler.handleMouseMove(self, x, y)
		try:
			info=self.makeTextInfo(locationHelper.Point(x,y))
		except NotImplementedError:
			info=NVDAObjectTextInfo(self,textInfos.POSITION_FIRST)
		except LookupError:
			return
		if config.conf["reviewCursor"]["followMouse"]:
			api.setReviewPosition(info, isCaret=True)
		info.expand(info.unit_mouseChunk)
		oldInfo=getattr(self,'_lastMouseTextInfoObject',None)
		self._lastMouseTextInfoObject=info
		if not oldInfo or info.__class__!=oldInfo.__class__ or info.compareEndPoints(oldInfo,"startToStart")!=0 or info.compareEndPoints(oldInfo,"endToEnd")!=0:
			text=info.text
			notBlank=False
			if text:
				for ch in text:
					if not ch.isspace() and ch != textUtils.OBJ_REPLACEMENT_CHAR:
						notBlank=True
			if notBlank:
				if not speechWasCanceled:
					speech.cancelSpeech()
				speech.speakText(text)

	def event_stateChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, states=True, reason=controlTypes.OutputReason.CHANGE)
		braille.handler.handleUpdate(self)
		vision.handler.handleUpdate(self, property="states")

	def event_focusEntered(self):
		if self.role in (controlTypes.Role.MENUBAR,controlTypes.Role.POPUPMENU,controlTypes.Role.MENUITEM):
			speech.cancelSpeech()
			return
		if self.isPresentableFocusAncestor:
			speech.speakObject(self, reason=controlTypes.OutputReason.FOCUSENTERED)

	def event_gainFocus(self):
		"""
This code is executed if a gain focus event is received by this object.
"""
		self.reportFocus()
		braille.handler.handleGainFocus(self)
		brailleInput.handler.handleGainFocus(self)
		vision.handler.handleGainFocus(self)

	def event_loseFocus(self):
		# Forget the word currently being typed as focus is moving to a new control. 
		speech.clearTypedWordBuffer()

	def event_foreground(self):
		"""Called when the foreground window changes.
		This method should only perform tasks specific to the foreground window changing.
		L{event_focusEntered} or L{event_gainFocus} will be called for this object, so this method should not speak/braille the object, etc.
		"""
		speech.cancelSpeech()
		vision.handler.handleForeground(self)

	def event_becomeNavigatorObject(self, isFocus=False):
		"""Called when this object becomes the navigator object.
		@param isFocus: true if the navigator object was set due to a focus change.
		@type isFocus: bool
		"""
		# When the navigator object follows the focus and braille is auto tethered to review,
		# we should not update braille with the new review position as a tether to focus is due.
		if not (braille.handler.shouldAutoTether and isFocus):
			braille.handler.handleReviewMove(shouldAutoTether=not isFocus)
		vision.handler.handleReviewMove(
			context=vision.constants.Context.FOCUS if isFocus else vision.constants.Context.NAVIGATOR
		)

	def event_valueChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, value=True, reason=controlTypes.OutputReason.CHANGE)
		braille.handler.handleUpdate(self)
		vision.handler.handleUpdate(self, property="value")

	def event_nameChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, name=True, reason=controlTypes.OutputReason.CHANGE)
		braille.handler.handleUpdate(self)
		vision.handler.handleUpdate(self, property="name")

	def event_descriptionChange(self):
		if self is api.getFocusObject():
			speech.speakObjectProperties(self, description=True, reason=controlTypes.OutputReason.CHANGE)
		braille.handler.handleUpdate(self)
		vision.handler.handleUpdate(self, property="description")

	def event_caret(self):
		if self is api.getFocusObject() and not eventHandler.isPendingEvents("gainFocus"):
			braille.handler.handleCaretMove(self)
			brailleInput.handler.handleCaretMove(self)
			vision.handler.handleCaretMove(self)
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
			self._basicText=u" ".join(x for x in (self.name, self.value, self.description) if isinstance(x, str) and len(x) > 0 and not x.isspace())
			if len(self._basicText)==0:
				self._basicText=u""
		else:
			self._basicTextTime=newTime
		return self._basicText

	def _get__isTextEmpty(self):
		"""
		@return C{True} if the text contained in the object is considered empty by the underlying implementation. In most cases this will match {isCollapsed}, however some implementations may consider a single space or line feed as an empty range.
		"""
		ti = self.makeTextInfo(textInfos.POSITION_FIRST)
		ti.move(textInfos.UNIT_CHARACTER, 1, endPoint="end")
		return ti.isCollapsed

	@staticmethod
	def _formatLongDevInfoString(string, truncateLen=250):
		"""Format a potentially long string value for inclusion in devInfo.
		This should be used for arbitrary string values which aren't usually useful in debugging past a certain length.
		If the string is too long to be useful, it will be truncated.
		This string should be included as returned. There is no need to call repr.
		@param string: The string to format.
		@type string: str
		@param truncateLen: The length at which to truncate the string.
		@type truncateLen: int
		@return: The formatted string.
		@rtype: str
		"""
		if isinstance(string, str) and len(string) > truncateLen:
			return "%r (truncated)" % string[:truncateLen]
		return repr(string)

	devInfo: typing.List[str]
	"""Information about this object useful to developers."""

	# C901 '_get_devInfo' is too complex
	# Note: when working on _get_devInfo, look for opportunities to simplify
	# and move logic out into smaller helper functions.
	def _get_devInfo(self) -> typing.List[str]:  # noqa: C901
		"""Information about this object useful to developers.
		Subclasses may extend this, calling the superclass property first.
		@return: A list of text strings providing information about this object useful to developers.
		"""
		info = []
		try:
			ret = repr(self.name)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("name: %s" % ret)
		ret = self.role
		info.append("role: %s" % ret)
		try:
			ret = repr(self.roleText)
		except Exception as e:
			ret = f"exception: {e}"
		info.append(f"roleText: {ret}")
		try:
			ret = ", ".join(str(state) for state in self.states)
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
			ret = repr(self.TextInfo)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("TextInfo: %s" % ret)
		info.extend(self.appModule.devInfo)
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
		objects with a role of L{controlTypes.Role.MATH}.
		@raise LookupError: If MathML can't be retrieved for this object.
		"""
		raise NotImplementedError

	#: The language/locale of this object.
	#: @type: str
	language = None

	def _get__hasNavigableText(self):
		# The generic NVDAObjectTextInfo by itself is never enough to be navigable
		if self.TextInfo is NVDAObjectTextInfo:
			return False
		role = self.role
		states = self.states
		if role in (controlTypes.Role.EDITABLETEXT,controlTypes.Role.TERMINAL,controlTypes.Role.DOCUMENT):
			# Edit fields, terminals and documents  are always navigable
			return True
		elif controlTypes.State.EDITABLE in states:
			# Anything that is specifically editable is navigable
			return True
		else:
			return False

	def _get_hasIrrelevantLocation(self):
		"""Returns whether the location of this object is irrelevant for mouse or magnification tracking or highlighting,
		either because it is programatically hidden (State.INVISIBLE), off screen or the object has no location."""
		states = self.states
		return controlTypes.State.INVISIBLE in states or controlTypes.State.OFFSCREEN in states or not self.location or not any(self.location)

	def _get_selectionContainer(self):
		""" An ancestor NVDAObject which manages the selection for this object and other descendants."""
		return None

	def getSelectedItemsCount(self,maxCount=2):
		"""
		Fetches the number of descendants currently selected.
		For performance, this method will only count up to the given maxCount number, and if there is one more above that, then sys.maxint is returned stating that many items are selected.
		"""
		return 0
