#vision/visionHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing the vision handler.
"""

from .constants import *
from .providerBase import VisionEnhancementProvider
from .visionHandlerExtensionPoints import VisionHandlerExtensionPoints
import pkgutil
from baseObject import AutoPropertyObject
import api
import config
import weakref
from logHandler import log
import wx
from collections import defaultdict

def getProviderClass(moduleName, caseSensitive=True):
	"""Returns a registered provider class with the specified moduleName."""
	try:
		return __import__(
			"visionEnhancementProviders.%s" % moduleName,
			globals(),
			locals(),
			("visionEnhancementProviders",)
		).VisionEnhancementProvider
	except ImportError as initialException:
		if caseSensitive:
			raise initialException
		for loader, name, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
			if name.startswith('_') or name.lower() != moduleName.lower():
				continue
			return __import__(
				"visionEnhancementProviders.%s" % name,
				globals(),
				locals(),
				("visionEnhancementProviders",)
			).VisionEnhancementProvider
		else:
			raise initialException

class VisionHandler(AutoPropertyObject):

	def __init__(self):
		self.lastReviewMoveContext = None
		self.lastCaretObjRef = None
		self.extensionPoints = VisionHandlerExtensionPoints()
		self.providers = dict()
		for providerName in config.conf['vision']['providers']]:
			# Some providers, such as the highlighter, rely on wx being fully initialized,
			# e.g. when they use an overlay window which parent is NVDA's main frame.
			wx.CallAfter(self.initializeProvider, providerName)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def terminateProvider(self, providerName):
		providerInstance =self.providers.pop(providerName, None):
		if not providerInstance:
			log.warning("Tried to terminate uninitialized provider %s" % providerName)
			return 
		try:
			providerInstance.terminate()
		except:
			# Purposely catch everything.
			# A provider can raise whatever exception,
			# therefore it is unknown what to expect.
			log.error("Error while terminating vision provider %s" % providerName, exc_info=True)
			return
		try:
			config.conf['vision']['providers'].remove(providerCls.name)
		except ValueError:
			pass

	def initializeProvider(self, providerName, temporary=False):
		"""
		Enables and activates the supplied provider.
		@param providerName: The name of the registered provider.
		@type providerName: str
		@param temporary: Whether the selected provider is enabled temporarily (e.g. as a fallback).
			This defaults to C{False}.
			If C{True}, no changes will be performed to the configuration.
		@type temporary: bool
		@returns: Whether initializing the requested provider succeeded.
		@rtype: bool
		"""
		if providerName in self.providers:
			# Todo, what to do here? silently reinit? This could be costly.
			self.terminateProvider(providerName)
		providerCls = getProviderClass(providerName)
		# Initialize the provider.
		try:
			providerInst = providerCls()
			providerInst.initSettings()

			if not temporary:
				config.conf['vision']['providers'].append(providerCls.name)
		except:
			# Purposely catch everything.
			# A provider can raise whatever exception,
			# therefore it is unknown what to expect.
			log.error("Error while initializing provider %s" % providerName, exc_info=True)
			return False

		try:
			self.initialFocus()
		except:
			# #8877: initialFocus might fail because NVDA tries to focus
			# an object for which property fetching raises an exception.
			# We should handle this more gracefully, since this is no reason
			# to stop a provider from loading successfully.
			log.debugWarning("Error in initial focus after provider load", exc_info=True)
		return True

	def _get_enabled(self):
		return bool(self.providers)

	def terminate(self):
		self.extensionPoints = None
		config.post_configProfileSwitch.unregister(self.handleConfigProfileSwitch)
		for instance in self.providers.values():
			instance.terminate()
		self.providers.clear()

	def handleUpdate(self, obj):
		if not self.enabled:
			return
		if obj is api.getFocusObject():
			self.handleGainFocus(obj)
		elif obj is api.getNavigatorObject():
			self.handleReviewMove(context=CONTEXT_NAVIGATOR)

	def handleForeground(self, obj):
		context = CONTEXT_FOREGROUND
		if self.magnifier:
			self.magnifier.trackToObject(obj, context=context)
		if self.highlighter:
			self.highlighter.updateContextRect(context, obj=obj)

	def handleGainFocus(self, obj):
		context = CONTEXT_FOCUS
		if self.magnifier:
			self.magnifier.trackToObject(obj, context=context)
		hasNavigableText = getattr(obj, "_hasNavigableText", False)
		if hasNavigableText:
			# This object most likely has a caret.
			# Intentionally check this after tracking a magnifier to the object itself.
			self.handleCaretMove(obj)
		if self.highlighter:
			self.highlighter.updateContextRect(context, obj=obj)
			if config.conf['reviewCursor']['followFocus']:
				# Purposely don't provide the object to updateContextRect here.
				# This is because obj could also be a tree interceptor.
				# Furthermore, even when review follows focus, there might be
				# reasons why the navigator object is not the same as the focus object.
				self.highlighter.updateContextRect(CONTEXT_NAVIGATOR)
			if not hasNavigableText:
				# If this object does not have a caret, clear the caret rectangle from the map
				# However, in the unlikely case it yet has a caret, we want to highlight that.
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
		# Import late to avoid circular import
		import cursorManager
		context = CONTEXT_CARET if not isinstance(obj, cursorManager.CursorManager) else CONTEXT_BROWSEMODE
		try:
			if self.magnifier:
				self.magnifier.trackToObject(obj, context=context)
			if self.highlighter:
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
		if lastReviewMoveContext in (CONTEXT_NAVIGATOR, CONTEXT_REVIEW) and self.magnifier:
			self.magnifier.trackToObject(context=lastReviewMoveContext)
		if self.highlighter:
			for context in (CONTEXT_NAVIGATOR, CONTEXT_REVIEW):
				self.highlighter.updateContextRect(context=context)

	def handleMouseMove(self, obj, x, y):
		# Mouse moves execute once per core cycle.
		if self.magnifier:
			self.magnifier.trackToPoint((x, y), context=CONTEXT_MOUSE)

	def handleConfigProfileSwitch(self):
		for role in ROLE_DESCRIPTIONS.keys():
			newProviderName = config.conf['vision'][role]
			curProvider = getattr(self, role)
			if not curProvider or newProviderName != curProvider.name:
				self.setProvider(newProviderName, (role,))

	def initialFocus(self):
		if not self.enabled or not api.getDesktopObject():
			# No active providers or focus/review hasn't yet been initialised.
			return
		self.handleGainFocus(api.getFocusObject())
