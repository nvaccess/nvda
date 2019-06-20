#vision/visionHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing the vision handler.
"""

from .constants import *
from .providerBase import VisionEnhancementProvider
from .visionHandlerExtensionPoints import EventExtensionPoints
import pkgutil
import importlib
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
		self.extensionPoints = EventExtensionPoints()
		self.providers = dict()
		for providerName in config.conf['vision']['providers']:
			# Some providers, such as the highlighter, rely on wx being fully initialized,
			# e.g. when they use an overlay window which parent is NVDA's main frame.
			wx.CallAfter(self.initializeProvider, providerName)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def terminateProvider(self, providerName):
		providerInstance =self.providers.pop(providerName, None)
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
		providerInst = self.providers.pop(providerName, None)
		if providerInst is not None:
			try:
				providerInst.reinitialize()
			except:
				# Purposely catch everything.
				# A provider can raise whatever exception,
				# therefore it is unknown what to expect.
				log.error("Error while reinitializing provider %s" % providerName, exc_info=True)
				return False
		else:
			providerCls = getProviderClass(providerName)
			# Initialize the provider.
			try:
				providerInst = providerCls()
			except:
				# Purposely catch everything.
				# A provider can raise whatever exception,
				# therefore it is unknown what to expect.
				log.error("Error while initializing provider %s" % providerName, exc_info=True)
				return False
			# Register extension points.
			try:
				providerInst.registerEventExtensionPoints(self.extensionPoints)
			except:
				log.error("Error while registering to extension points for provider %s" % providerName, exc_info=True)
				try:
					providerInst.terminate()
				except:
					pass
				return False
		providerInst.initSettings()
		if not temporary and providerCls.name not in config.conf['vision']['providers']:
			config.conf['vision']['providers'].append(providerCls.name)
		self.providers[providerName] = providerInst
		try:
			self.initialFocus()
		except:
			# #8877: initialFocus might fail because NVDA tries to focus
			# an object for which property fetching raises an exception.
			# We should handle this more gracefully, since this is no reason
			# to stop a provider from loading successfully.
			log.debugWarning("Error in initial focus after provider load", exc_info=True)
		return True

	def terminate(self):
		self.extensionPoints = None
		config.post_configProfileSwitch.unregister(self.handleConfigProfileSwitch)
		for instance in self.providers.values():
			instance.terminate()
		self.providers.clear()

	def handleUpdate(self, obj, attribute):
		self.extensionPoints.post_objectUpdate.notify(obj=obj, attribute=attribute)

	def handleForeground(self, obj):
		self.extensionPoints.post_foregroundChange.notify(obj=obj)

	def handleGainFocus(self, obj):
		self.extensionPoints.post_focusChange.notify(obj=obj)
		hasNavigableText = getattr(obj, "_hasNavigableText", False)
		if hasNavigableText:
			# This object most likely has a caret.
			self.handleCaretMove(obj)

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
		if api.isCursorManager(obj):
			self.extensionPoints.post_browseModeMove(obj=obj)
		else:
			self.extensionPoints.post_caretMove(obj=obj)

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
		self.extensionPoints.post_reviewMove(obj=obj, context=lastReviewMoveContext)

	def handleMouseMove(self, obj, x, y):
		# For now, mouse moves execute once per core cycle.
		self.extensionPoints.post_mouseMove(obj=obj, x=x, y=y)

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
