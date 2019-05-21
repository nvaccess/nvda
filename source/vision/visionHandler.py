#vision/visionHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing the vision handler.
"""

from .constants import *
from .providerBase import VisionEnhancementProvider
from .highlighterBase import Highlighter
from .magnifierBase import Magnifier
from .colorEnhancerBase import ColorEnhancer
import pkgutil
from baseObject import AutoPropertyObject
import api
import config
import weakref
from logHandler import log
import wx
from collections import defaultdict

def getProvider(moduleName, caseSensitive=True):
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
		configuredProviders = defaultdict(set)
		for role in ROLE_DESCRIPTIONS.keys():
			setattr(self, role, None)
			configuredProviders[config.conf['vision'][role]].add(role)
		for name, roles in configuredProviders.items():
			if name:
				# Some providers, such as the highlighter, rely on wx being fully initialized,
				# e.g. when they use an overlay window which parent is NVDA's main frame.
				wx.CallAfter(self.setProvider, name, roles)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def terminateProviderForRole(self, role):
		curProvider = getattr(self, role)
		if curProvider:
			curProvider.terminate(role)
			setattr(self, role, None)

	def setProvider(self, name, roles, temporary=False, catchExceptions=True):
		"""Enables and activates the selected provider for the provided roles.
		If there was a previous provider in use for a role,
		that provider will be terminated for that role.
		@param name: The name of the registered provider class.
		@type name: str
		@param roles: names of roles to enable the provider for.
			Supplied values should be one of the C{ROLE_*} constants.
			if roles is empty, the provider is enabled for all the roles it supports.
		@type roles: [str]
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
		if name in (None, "None"):
			if not roles:
				raise ValueError("No name and no roles provided")
			for role in roles:
				try:
					self.terminateProviderForRole(role)
				except:
					# Purposely catch everything.
					# A provider can raise whatever exception,
					# therefore it is unknown what to expect.
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
			# Providers are singletons.
			# Get a new or current instance of the provider
			providerInst = providerCls.__new__(providerCls)
			initiallyEnabled = bool(providerInst.activeRoles)
			if initiallyEnabled:
				log.debug("Provider %s is already active" % name)
			# Terminate the provider for the roles that overlap between the provided roles and the active roles.
			# For these roles, we want to reinitialize the provider.
			overlappingRoles = providerInst.activeRoles & roles
			newRoles = roles - overlappingRoles
			if overlappingRoles:
				providerInst.terminate(*overlappingRoles)
			# Properly terminate  providers that are active for the current role.
			for conflict in newRoles:
				self.terminateProviderForRole(conflict)
				if not temporary:
					config.conf['vision'][conflict] = None
			# Initialize the provider for the new and overlapping roles
			providerInst.__init__(*roles)
			if initiallyEnabled:
				providerInst.loadSettings(onlyChanged=True)
			else:
				providerInst.initSettings()

			# Assign the new provider to the new roles.
			for role in newRoles:
				setattr(self, role, providerInst)
				if not temporary:
					config.conf['vision'][role] = providerCls.name
			try:
				self.initialFocus()
			except:
				# #8877: initialFocus might fail because NVDA tries to focus
				# an object for which property fetching raises an exception.
				# We should handle this more gracefully, since this is no reason
				# to stop a provider from loading successfully.
				log.debugWarning("Error in initial focus after provider load", exc_info=True)
			return True
		except:
			if not catchExceptions:
				raise
			log.error("Error initializing vision enhancement provider %s for roles %s" % (name, ", ".join(roles)), exc_info=True)
			self.setProvider(None, roles, temporary=True)
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
		for role in ROLE_DESCRIPTIONS.keys():
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
		if self.magnifier:
			self.magnifier.trackToObject(obj, context=context)
		if self.highlighter:
			self.highlighter.updateContextRect(context, obj=obj)

	def handleGainFocus(self, obj):
		context = CONTEXT_FOCUS
		if self.magnifier:
			self.magnifier.trackToObject(obj, context=context)
		if getattr(obj, "_hasNavigableText", False):
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
			if not mightHaveCaret:
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
