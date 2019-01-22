#vision.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Framework to facilitate changes in how content is displayed on screen.
Three roles (types) of vision enhancement providers are supported:
	* Magnifier: to magnify the full screen or a part of it.
	* Highlighter: to highlight important areas of the screen (e.g. the focus, mouse or review position).
	* ColorEnhancer: to change the color presentation of the whole screen or a part of it.
A vision enhancement provider can implement either one or more of the above assistant functions.
Add-ons can provide their own implementation for any or all of these
using modules in the visionEnhancementProviders package containing a L{VisionEnhancementProvider} class.
"""

import config
import visionEnhancementProviders
import pkgutil
from baseObject import AutoPropertyObject
from abc import abstractmethod
import api
import config
import weakref
from logHandler import log
import wx
from collections import defaultdict, OrderedDict
import textInfos
import NVDAObjects
import winVersion
from locationHelper import RectLTRB
from synthDriverHandler import StringParameterInfo
import textInfos

# Context in which cases in NVDA can trigger a visual change
# When tracking a magnifier to a specified area on screen,
# it can use the context to apply specific behavior.
# For example, the focus object could be centered on the magnified screen,
# whereas the caret doesn't necessarily have to be centered.
# A highlighter can use the context to change the position of a specific highlight.
#: Context for undetermined events
CONTEXT_UNDETERMINED = "undetermined"
#: Context for focus changes
CONTEXT_FOCUS = "focus"
#: Context for foreground changes
CONTEXT_FOREGROUND = "foreground"
#: Context for caret changes, either physical or virtual
CONTEXT_CARET = "caret"
#: Context for review cursor changes
CONTEXT_REVIEW = "review"
#: Context for navigator object changes
CONTEXT_NAVIGATOR = "navigatorObj"
#: Context for mouse movement
CONTEXT_MOUSE = "mouse"

# Role constants
ROLE_MAGNIFIER = "magnifier"
ROLE_HIGHLIGHTER = "highlighter"
ROLE_COLORENHANCER = "colorEnhancer"

class VisionEnhancementProvider(AutoPropertyObject):
	"""A basic, abstract class for vision enhancement providers.
	Providers should usually base themselves on one or more of its subclasses.
	"""
	name = ""
	description = ""
	#: The roles that would cause conflicts with this provider when initialized.
	#: Providers for conflicting roles are always terminated before initializing the provider.
	#: For example, if a color enhancer is used to make the screen black,
	#: It does not make sense to magnify the screen or use a highlighter.
	conflictingRoles = frozenset()
	#: A vision enhancement provider is a singleton.
	_instance = None
	cachePropertiesByDefault = True

	@classmethod
	def check(cls):
		return True

	@classmethod
	def __new__(cls, *args, **kwargs):
		# Make this a singleton.
		inst = cls._instance() if cls._instance else None
		if not inst:
			obj = super(VisionEnhancementProvider, cls).__new__(cls, *args, **kwargs)
			obj.activeRoles = set()
			cls._instance = weakref.ref(obj)
			return obj
		return inst

	def __init__(self, *roles):
		"""Constructor.
		Subclasses may extend this method.
		They must extend this method if additional initialization has to be performed before all roles are initialized,
		e.g. when a library has to be loaded or initialized.
		"""
		super(VisionEnhancementProvider, self).__init__()
		if not roles:
			roles = self.supportedRoles
		for role in roles:
			if role not in self.supportedRoles:
				raise RuntimeError("Role %s not supported by %s" % (role, self.name))
			if role in self.activeRoles:
				log.debug("Role %s for provider %s is already initialized, silently ignoring" % (role, self.name))
				continue
			getattr(self, "initialize%s" % (role[0].upper()+role[1:]))()
			self.activeRoles.add(role)

	@classmethod
	def _get_supportedRoles(cls):
		"""Returns the roles supported by this provider."""
		return frozenset(role for role, baseCls in ROLE_TO_CLASS_MAP.iteritems() if issubclass(cls, baseCls))

	def _get_running(self):
		"""Returns whether the provider is running.
		This is required for third party software, which runs in a separate process.
		Providers that run out of the NVDA process should override this method.
		"""
		return True

	def _get_enabled(self):
		"""Returns whether the provider is enabled.
		This differs from L{running}, as a provider could be temporarily disabled
		while still active in the background.
		By convension, this should always return C{False} when not running.
		"""
		return self.running and bool(self.activeRoles)

	@classmethod
	def getContextObject(cls, context):
		"""Gets the appropriate NVDAObject associated with the provided context."""
		if context == CONTEXT_FOCUS:
			return api.getFocusObject()
		elif context == CONTEXT_FOREGROUND:
			return api.getForegroundObject()
		elif context == CONTEXT_CARET:
			obj = api.getCaretObject()
		elif context == CONTEXT_REVIEW:
			return api.getReviewPosition().obj
		elif context == CONTEXT_NAVIGATOR:
			return api.getNavigatorObject()
		elif context == CONTEXT_MOUSE:
			return api.getMouseObject()
		else:
			raise NotImplementedError("Couldn't get object for context %s" % context)

	@classmethod
	def getContextRect(cls, context, obj=None):
		"""Gets a rectangle for the specified context.
		If L{obj} is not C{None}, the object is used to get the rectangle from, if necessary.
		Otherwise, the base implementation calls L{getContextObject} and gets a rectangle from the object, if necessary."""
		if context == CONTEXT_REVIEW:
			return cls._getRectFromTextInfo(api.getReviewPosition())
		if not obj:
			obj = cls.getContextObject(context)
		if not obj:
			raise LookupError
		# Import late to avoid circular import
		import treeInterceptorHandler
		isTreeInterceptor = isinstance(obj, treeInterceptorHandler.TreeInterceptor)
		if (
			(context == CONTEXT_FOCUS and isTreeInterceptor) or
			context == CONTEXT_CARET
		):
			if isTreeInterceptor:
				pass
			elif getattr(obj, "treeInterceptor", None) and not obj.treeInterceptor.passThrough:
				obj = obj.treeInterceptor
			elif isinstance(obj, NVDAObjects.NVDAObject):
				# Import late to avoid circular import
				from displayModel import getCaretRect
				# Check whether there is a caret in the window.
				# Note that, even windows that don't have navigable text could have a caret, such as in Excel.
				try:
					return RectLTRB.fromCompatibleType(getCaretRect(obj))
				except RuntimeError:
					if not obj._hasNavigableText:
						return None
			try:
				caretInfo = obj.makeTextInfo(textInfos.POSITION_CARET)
			except (NotImplementedError, RuntimeError):
				pass
			# Try a selection
			try:
				caretInfo = obj.makeTextInfo(textInfos.POSITION_SELECTION)
			except (NotImplementedError, RuntimeError):
				# There is nothing to do here
				raise LookupError
			return cls._getRectFromTextInfo(caretInfo)
		location = obj.location
		if not location:
			raise LookupError
		return location.toLTRB()

	@classmethod
	def _getRectFromTextInfo(cls, textInfo):
		if textInfo.isCollapsed:
			textInfo.expand(textInfos.UNIT_CHARACTER)
		try:
			rects = textInfo.boundingRects
		except NotImplementedError:
			rects = None
		if rects:
			index = 0 if textInfo.obj.isTextSelectionAnchoredAtStart else -1
			rect = rects[index].toLTRB()
		else:
			rect = RectLTRB.fromPoint(textInfo.pointAtStart)
		return rect

	def terminate(self, *roles):
		"""Executed when terminating this provider.
		Subclasses may extend this method.
		They must extend this method if additional cleanup has to be performed after all roles are terminated,
		e.g. when resources have to be freed or a process has to be terminated.
		"""
		if not roles:
			roles = self.activeRoles.copy()
		for role in roles:
			if role not in self.supportedRoles:
				raise RuntimeError("Role %s not supported by %s" % (role, self.name))
			if role not in self.activeRoles:
				log.debug("Role %s for provider %s is not initialized, silently ignoring" % (role, self.name))
				continue
			getattr(self, "terminate%s" % (role[0].upper()+role[1:]))()
			self.activeRoles.remove(role)

class Highlighter(VisionEnhancementProvider):
	"""A vision enhancement provider that supports highlighting certain portions of the screen.
	Subclasses should at least implement the L{initializeHighlighter},
	L{terminateHighlighter} and L{refresh} methods.
	Supported contexts should be listed in L{supportedHighlightContexts}.
	"""

	#: Tuple of supported contexts for this highlighter.
	supportedHighlightContexts = tuple()

	@abstractmethod
	def initializeHighlighter(self):
		"""Initializes a highlighter.
		Subclasses must extend this method.
		"""
		#: A dictionary that maps contexts to their current rectangle.
		self.contextToRectMap = {}
		# Initialize the map with their current values
		for context in self.enabledHighlightContexts:
			# Always call the base implementation here
			Highlighter.updateContextRect(self, context)

	@abstractmethod
	def terminateHighlighter(self):
		"""Terminates a highlighter.
		Subclasses must extend this method.
		"""
		self.contextToRectMap.clear()

	def updateContextRect(self, context, rect=None, obj=None):
		"""Updates the position rectangle of the highlight for the specified context.
		The base implementation updates the position in the L{contextToRectMap}.
		if rect and obj are C{None}, the position is retrieved from the object associated with the context.
		Otherwise, either L{obj} or L{rect} should be provided.
		Subclasses should extend or override this method if they want to get the context position in a different way.
		"""
		if context not in self.supportedHighlightContexts:
			raise NotImplementedError
		if rect is not None and obj is not None:
			raise ValueError("Only one of rect or obj should be provided")
		if rect is None:
			try:
				rect= self.getContextRect(context, obj)
			except (LookupError, NotImplementedError):
				rect = None
		self.contextToRectMap[context] = rect

	@abstractmethod
	def refresh(self):
		"""Refreshes the screen positions of the enabled highlights.
		This is called once in every core cycle.
		Subclasses must override this method.
		"""
		raise NotImplementedError

	def _get_enabledHighlightContexts(self):
		"""Gets the contexts for which the highlighter is enabled."""
		if not self.enabled:
			return ()
		return tuple(
			context for context in self.supportedHighlightContexts
			if config.conf['vision'][self.name]['highlight%s' % (context[0].upper() + context[1:])]
		)

class Magnifier(VisionEnhancementProvider):
	"""A vision enhancement provider that supports magnifying (a part of) the screen.
	Subclasses should at least implement the L{initializeMagnifier},
	L{terminateMagnifier} and L{trackToRectangle} methods,
	and should implement the L{magnificationLevel} property.
	Supported contexts should be listed in L{supportedTrackingContexts}.
	"""
	#: Tuple of supported contexts for this magnifier to track to.
	supportedTrackingContexts = tuple()

	@abstractmethod
	def initializeMagnifier(self):
		"""Initializes a magnifier.
		Subclasses must extend this method.
		"""

	@abstractmethod
	def terminateMagnifier(self):
		"""Terminates a magnifier.
		Subclasses must extend this method.
		"""

	def trackToObject(self, obj=None, context=CONTEXT_UNDETERMINED, area=None):
		"""Tracks the magnifier to the given object.
		If object is C{None}, the appropriate object is fetched automatically.
		The base implementation simply tracks to the location of the object.
		Subclasses may override this method to implement context specific behaviour at the object level.
		"""
		try:
			rect = self.getContextRect(context, obj)
		except (LookupError, NotImplementedError):
			rect = None
		if not rect:
			return
		self.trackToRectangle(rect, context=context, area=area)

	@abstractmethod
	def trackToRectangle(self, rect, context=CONTEXT_UNDETERMINED, area=None):
		"""Tracks the magnifier to the given rectangle."""
		raise NotImplementedError

	def trackToPoint(self, point, context=CONTEXT_UNDETERMINED, area=None):
		"""Tracks the magnifier to the given point.
		The base implementation creates a rectangle from a point and tracks to that rectangle."""
		x, y = point
		rect = RectLTRB(x, y, x+1, y+1)
		self.trackToRectangle((rect), context=context, area=area)

	_abstract_magnificationLevel = True
	def _get_magnificationLevel(self):
		raise NotImplementedError

	def _set_magnificationLevel(self, level):
		raise NotImplementedError

	def _get_isMagnifying(self):
		"""Returns C{True} if the magnifier is magnifying the screen, C{False} otherwise.
		By default, this property is based on L{enabled} and L{magnificationLevel}
		"""
		return self.enabled and self.magnificationLevel > 1.0

	def _get_enabledTrackingContexts(self):
		"""Gets the contexts for which the magnifier is enabled."""
		if not self.isMagnifying:
			return ()
		return tuple(
			context for context in self.supportedTrackingContexts
			if config.conf['vision'][self.name]['trackTo%s' % (context[0].upper() + context[1:])]
		)

class ColorTransformationInfo(StringParameterInfo):
	"""Represents a color transformation.
	"""

	def __init__(self,ID,name,value):
		#: The value that cointains the color transformation info (e.g. a matrix).
		self.value=value
		super(ColorTransformationInfo,self).__init__(ID,name)

class ColorEnhancer(VisionEnhancementProvider):
	"""A vision enhancement provider that changes the coloring of the screen.
	For example, it could implement high contrast schemes,
	or act as a screen curtain in making the screen invisible for users.
	Subclasses should at least implement the L{initializeColorEnhancer}
	and L{terminateColorEnhancer} methods.
	If the enhancer supports multiple transformations (color schemes or enhancements),
	they should be returned when calling L{_getAvailableTransformations}.
	In this case, the L{transformation} property ought to be implemented
	to retrieve or change the current transformation.
	"""
	
	@abstractmethod
	def initializeColorEnhancer(self):
		"""Initializes a color enhancer.
		Subclasses must extend this method.
		"""

	@abstractmethod
	def terminateColorEnhancer(self):
		"""Terminates a color enhancer.
		Subclasses must extend this method.
		"""

	def _getAvailableTransformations(self):
		"""Returns the color transformations supported by this color enhancer.
		@rtype: [L{ColorTransformationInfo}]
		"""
		return []

	def _get_availableTransformations(self):
		return OrderedDict((info.ID,info) for info in self._getAvailableTransformations())

	def _get_transformation(self):
		return None

ROLE_TO_CLASS_MAP = {
	ROLE_MAGNIFIER: Magnifier,
	ROLE_HIGHLIGHTER: Highlighter,
	ROLE_COLORENHANCER: ColorEnhancer,
}

ROLE_DESCRIPTIONS = {
	# Translators: The name for a vision enhancement provider that magnifies (a part of) the screen.
	ROLE_MAGNIFIER: _("Magnifier"),
	# Translators: The name for a vision enhancement provider that highlights important areas on screen,
	# such as the focus, caret or review cursor location.
	ROLE_HIGHLIGHTER: _("Highlighter"),
	# Translators: The name for a vision enhancement provider that enhances the color presentation.
	# (i.e. color inversion, gray scale coloring, etc.)
	ROLE_COLORENHANCER: _("Color enhancer"),
}

def initialize():
	global handler
	config.addConfigDirsToPythonPackagePath(visionEnhancementProviders)
	handler = VisionHandler()

def pumpAll():
	"""Runs tasks at the end of each core cycle."""
	# Note that a pending review update has to be executed before a pending caret update.
	handler.handlePendingReviewUpdate()
	handler.handlePendingCaretUpdate()

def getProvider(moduleName, caseSensitive=True):
	"""Returns a registered provider class with the specified moduleName."""
	try:
		return __import__("visionEnhancementProviders.%s" % moduleName, globals(), locals(), ("visionEnhancementProviders",)).VisionEnhancementProvider
	except ImportError as initialException:
		if caseSensitive:
			raise initialException
		for loader, name, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
			if name.startswith('_') or name.lower() != moduleName.lower():
				continue
			return __import__("visionEnhancementProviders.%s" % name, globals(), locals(), ("visionEnhancementProviders",)).VisionEnhancementProvider
		else:
			raise initialException

def terminate():
	global handler
	handler.terminate()
	handler = None

def getProviderList(excludeNegativeChecks=True):
	"""Gets a list of available vision enhancement names with their descriptions as well as supported and conflicting roles.
	@param excludeNegativeChecks: excludes all providers for which the check method returns C{False}.
	@type excludeNegativeChecks: bool
	@return: list of tuples with provider names, descriptions, supported roles and conflicting roles.
	@rtype: [(str,unicode,[ROLE_*],[ROLE_*])]
	"""
	providerList = []
	for loader, name, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
		if name.startswith('_'):
			continue
		try:
			provider = getProvider(name)
		except:
			log.error("Error while importing vision enhancement provider %s" % name,
				exc_info=True)
			continue
		try:
			if not excludeNegativeChecks or provider.check():
				providerList.append((provider.name, provider.description, list(provider.supportedRoles), list(provider.conflictingRoles)))
			else:
				log.debugWarning("Vision enhancement provider %s reports as unavailable, excluding" % provider.name)
		except:
			log.error("", exc_info=True)
	providerList.sort(key=lambda d : d[1].lower())
	return providerList

class VisionHandler(AutoPropertyObject):
	cachePropertiesByDefault = True

	def __init__(self):
		self.lastReviewMoveContext = None
		self.lastCaretObjRef = None
		configuredProviders = defaultdict(set)
		for role in ROLE_TO_CLASS_MAP.iterkeys():
			setattr(self, role, None)
			configuredProviders[config.conf['vision'][role]].add(role)
		for name, roles in configuredProviders.iteritems():
			if name:
				# Some providers might rely on wx being fully initialized,
				# e.g. when they use an overlay window.
				wx.CallAfter(self.setProvider, name, *roles)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def terminateProviderForRole(self, role):
		curProvider = getattr(self, role)
		if curProvider:
			curProvider.terminate(role)
			setattr(self, role, None)

	def setProvider(self, name, *roles, **kwargs):
		"""Enables and activates the selected provider for the provided roles.
		If there was a previous provider in use for a role,
		that provider will be terminated for that role.
		A provider won't load if another provider has to be terminated
		because of conflicting roles set for the new provider,
		@param name: The name of the registered provider class.
		@type name: str
		@param roles: names of roles to enable the provider for.
			Supplied values should be one of the C{ROLE_*} constants.
			If no roles are provided, the provider is enabled for all the roles it supports.
			This parameter can be suplied multiple times for multiple roles.
		@type roles: str
		@param temporary: Whether the selected provider is enabled temporarily (e.g. as a fallback).
			This defaults to C{False}.
			If C{True}, no changes will be performed to the configuration.
		@type temporary: bool
		@param catchExceptions: Whether exceptions raised while loading a provider should be handled gracefully.
			This defaults to C{True}, in which case an error is logged on failure,
			and there is an automatic fallback to no provider for the supplied roles.
			If C{False}, the caller should catch possible exceptions.
		@type temporary: bool
		@returns: Whether loading of the requested provider succeeded.
		@rtype: bool
		"""
		# In python 2, we need to use a **kwargs handler for keyword arguments,
		# because we also use a catch all for positional arguments.
		# In python 3, this is no longer necessary.
		temporary = kwargs.pop("temporary", False)
		catchExceptions = kwargs.pop("catchExceptions", True)
		assert not kwargs
		if name in (None, "None"):
			if not roles:
				raise ValueError("No name and no roles provided")
			for role in roles:
				try:
					self.terminateProviderForRole(role)
				except:
					log.error("Couldn't terminate provider for role %s" % role, exc_info=True)
				if not temporary:
					config.conf['vision'][role] = None
			return True
		providerCls = getProvider(name)
		if not roles:
			roles = providerCls.supportedRoles
		else:
			roles = set(roles)
			for role in roles:
				if role not in providerCls.supportedRoles:
					raise NotImplementedError("Provider %s does not implement role %s" % (name, role))

		try:
			conflicts = {name for name in (getattr(self, role) for role in providerCls.conflictingRoles) if name}
			if conflicts:
				raise RuntimeError("Provider %s couldn't be activated because of conflicts with provider(s) %s." %
					(providerCls.name, ", ".join(conflict.name for conflict in conflicts))
				)

			# Providers are singletons.
			# Get a new or current instance of the provider
			providerInst = providerCls.__new__(providerCls)
			if providerInst.enabled:
				log.debug("Provider %s is already active" % name)
			# Terminate the provider for the roles that overlap between the provided roles and the active roles.
			overlappingRoles =  providerInst.activeRoles & roles
			newRoles =  roles - overlappingRoles
			if overlappingRoles:
				providerInst.terminate(*overlappingRoles)
			# Properly terminate  conflicting providers.
			for conflict in newRoles:
				self.terminateProviderForRole(conflict)
				if not temporary:
					config.conf['vision'][conflict] = None
			# Initialize the provider for the new and overlapping roles
			providerInst.__init__(*roles)
			# Assign the new provider to the new roles.
			for role in newRoles:
				setattr(self, role, providerInst)
				if not temporary:
					config.conf['vision'][role] = providerCls.name
			self.initialFocus()
			return True
		except:
			if not catchExceptions:
				raise
			log.error("Error initializing vision enhancement provider %s for roles %s" % (name, ", ".join(roles)), exc_info=True)
			self.setProvider(None, *roles, temporary=True)
			return False

	def _get_initializedProviders(self):
		return set(
			provider for provider in (self.magnifier, self.highlighter, self.colorEnhancer)
			if provider
		)

	def _get_enabled(self):
		return bool(self.initializedProviders)

	def terminate(self):
		config.post_configProfileSwitch.unregister(self.handleConfigProfileSwitch)
		for role in ROLE_TO_CLASS_MAP.iterkeys():
			self.terminateProviderForRole(role)

	def handleUpdate(self, obj):
		if not self.enabled:
			return
		if obj is api.getFocusObject():
			self.handleGainFocus(obj)
		elif obj is api.getNavigatorObject():
			self.handleReviewMove(context=CONTEXT_NAVIGATOR)

	def handleForeground(self, obj):
		context = CONTEXT_FOREGROUND
		if self.magnifier and context in self.magnifier.enabledTrackingContexts:
			self.magnifier.trackToObject(obj, context=context)
		if self.highlighter and context in self.highlighter.enabledHighlightContexts:
			self.highlighter.updateContextRect(context, obj=obj)

	def handleGainFocus(self, obj):
		context = CONTEXT_FOCUS
		if self.magnifier and context in self.magnifier.enabledTrackingContexts:
			self.magnifier.trackToObject(obj, context=context)
		mightHaveCaret = getattr(obj, "_hasNavigableText", False)
		if mightHaveCaret:
			# This object most likely has a caret.
			# Intentionally check this after tracking a magnifier to the object itself.
			self.handleCaretMove(obj)
		if self.highlighter and context in self.highlighter.enabledHighlightContexts:
			if context != CONTEXT_CARET:
				self.highlighter.updateContextRect(context, obj=obj)
			if not mightHaveCaret and CONTEXT_CARET in self.highlighter.enabledHighlightContexts:
				# If this object does not have a caret, clear the caret rectangle from the map
				# However, in the unlikely case it yet has a caret, we want to highlight that.
				# This happens in Microsoft Excel, for example.
				self.highlighter.updateContextRect(CONTEXT_CARET, obj=obj)

	def handleCaretMove(self, obj):
		if not self.enabled:
			return
		self.lastCaretObjRef = weakref.ref(obj)

	def handlePendingCaretUpdate(self):
		if not callable(self.lastCaretObjRef):
			# No caret change
			return
		obj = self.lastCaretObjRef()
		if not obj:
			# The caret object died
			self.lastCaretObjRef = None
			return
		context = CONTEXT_CARET
		try:
			if self.magnifier and context in self.magnifier.enabledTrackingContexts:
				self.magnifier.trackToObject(obj, context=context)
			if self.highlighter and context in self.highlighter.enabledHighlightContexts:
				self.highlighter.updateContextRect(context, obj=obj)
		finally:
			self.lastCaretObjRef = None

	def handleReviewMove(self, context=CONTEXT_REVIEW):
		if not self.enabled:
			return
		self.lastReviewMoveContext = context

	def handlePendingReviewUpdate(self):
		if self.lastReviewMoveContext is None:
			# No review change.
			return
		lastReviewMoveContext = self.lastReviewMoveContext
		self.lastReviewMoveContext = None
		if lastReviewMoveContext in (CONTEXT_NAVIGATOR, CONTEXT_REVIEW) and self.magnifier and lastReviewMoveContext in self.magnifier.enabledTrackingContexts:
			self.magnifier.trackToObject(context=lastReviewMoveContext)
		if self.highlighter:
			for context in (CONTEXT_NAVIGATOR, CONTEXT_REVIEW):
				if context in self.highlighter.enabledHighlightContexts:
					self.highlighter.updateContextRect(context=context)

	def handleMouseMove(self, obj, x, y):
		# Mouse moves execute once per core cycle.
		if self.magnifier and CONTEXT_MOUSE in self.magnifier.enabledTrackingContexts:
			self.magnifier.trackToPoint((x, y), context=CONTEXT_MOUSE)

	def handleConfigProfileSwitch(self):
		for role in ROLE_TO_CLASS_MAP.iterkeys():
			newProviderName = config.conf['vision'][role]
			curProvider = getattr(self, role)
			if  not curProvider or newProviderName != curProvider.name:
				self.setProvider(newProviderName, role)

	def initialFocus(self):
		if not self.enabled or not api.getDesktopObject():
			# No active providers or focus/review hasn't yet been initialised.
			return
		self.handleGainFocus(api.getFocusObject())
