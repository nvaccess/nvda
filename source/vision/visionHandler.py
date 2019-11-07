# vision/visionHandler.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing the vision handler.

The vision handler is the core of the vision framework.
See the documentation of L{VisionHandler} for more details about what it does.
"""
from . import providerInfo
from .constants import Context
from .providerBase import VisionEnhancementProvider
from .visionHandlerExtensionPoints import EventExtensionPoints
import importlib
import pkgutil
from baseObject import AutoPropertyObject
import api
import config
from logHandler import log
import visionEnhancementProviders
import queueHandler
from typing import Type, Dict, List, Optional
from . import exceptions


def getProviderClass(
		moduleName: str,
		caseSensitive: bool = True
) -> Type[VisionEnhancementProvider]:
	"""Returns a registered provider class with the specified moduleName."""
	try:
		return importlib.import_module(
			"visionEnhancementProviders.%s" % moduleName,
			package="visionEnhancementProviders"
		).VisionEnhancementProvider
	except ImportError as initialException:
		if caseSensitive:
			raise initialException
		for loader, name, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
			if name.startswith('_') or name.lower() != moduleName.lower():
				continue
			return importlib.import_module(
				"visionEnhancementProviders.%s" % name,
				package="visionEnhancementProviders"
			).VisionEnhancementProvider
		else:
			raise initialException


def getProviderList(
		onlyStartable: bool = True
) -> List[providerInfo.ProviderInfo]:
	"""Gets a list of available vision enhancement provider information
	@param onlyStartable: excludes all providers for which the check method returns C{False}.
	@return: List of available providers
	"""
	providerList = []
	for loader, moduleName, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
		if moduleName.startswith('_'):
			continue
		try:
			provider = getProviderClass(moduleName)
		except Exception:
			# Purposely catch everything.
			# A provider can raise whatever exception it likes,
			# therefore it is unknown what to expect.
			log.error(
				f"Error while importing vision enhancement provider module {moduleName}",
				exc_info=True
			)
			continue
		try:
			if not onlyStartable or provider.canStart():
				providerSettings = provider.getSettings()
				providerList.append(
					providerInfo.ProviderInfo(
						providerId=providerSettings.getId(),
						moduleName=moduleName,
						translatedName=providerSettings.getTranslatedName(),
						providerClass=provider
					)
				)
			else:
				log.debugWarning(
					f"Excluding Vision enhancement provider module {moduleName} which is unable to start"
				)
		except Exception:
			# Purposely catch everything else as we don't want one failing provider
			# make it impossible to list all the others.
			log.error("", exc_info=True)
	# Sort the providers alphabetically by name.
	providerList.sort(key=lambda info: info.translatedName.lower())
	return providerList


def getProviderInfo(providerId: providerInfo.ProviderIdT) -> Optional[providerInfo.ProviderInfo]:
	# This mechanism of getting the provider list and looking it up is particularly inefficient, but, before
	# refactoring, confirm that getProviderList is / isn't cached.
	for p in getProviderList(onlyStartable=False):
		if p.providerId == providerId:
			return p
	raise LookupError(f"Provider with id ({providerId}) does not exist.")


class VisionHandler(AutoPropertyObject):
	"""The singleton vision handler is the core of the vision framework.
	It performs the following tasks:

		* It keeps track of active vision enhancement providers in the L{providers} dictionary.
		* It processes initialization and termination of providers.
		* It receives certain events from the core of NVDA,
			delegating them to the appropriate extension points.
	"""

	def __init__(self):
		self.providers: Dict[providerInfo.ProviderIdT, VisionEnhancementProvider] = dict()
		self.extensionPoints: EventExtensionPoints = EventExtensionPoints()
		queueHandler.queueFunction(queueHandler.eventQueue, self.postGuiInit)

	def postGuiInit(self) -> None:
		"""Handles first initialization of the handler as a config profile switch.
		This is executed on the main thread by L{__init__} using the events queue.
		This ensures that the gui is fully initialized before providers are initialized that might rely on it.
		"""
		self.handleConfigProfileSwitch()
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def terminateProvider(
			self,
			provider: providerInfo.ProviderInfo,
			saveSettings: bool = True
	) -> None:
		"""Terminates a currently active provider.
		When termnation fails, an exception is raised.
		Yet, the provider wil lbe removed from the providers dictionary,
		so its instance goes out of scope and wil lbe garbage collected.
		@param provider: The provider to terminate.
		@param saveSettings: Whether settings should be saved on termination.
		"""
		providerId = provider.providerId
		# Remove the provider from the providers dictionary.
		providerInstance = self.providers.pop(providerId, None)
		if not providerInstance:
			raise exceptions.ProviderTerminateException(
				f"Tried to terminate uninitialized provider {providerId!r}"
			)
		exception = None
		if saveSettings:
			try:
				providerInstance.getSettings().saveSettings()
			except Exception:
				log.error(f"Error while saving settings during termination of {providerId}")
		try:
			providerInstance.terminate()
		except Exception as e:
			# Purposely catch everything.
			# A provider can raise whatever exception,
			# therefore it is unknown what to expect.
			exception = e
		# Copy the configured providers before mutating the list.
		# If we don't, configobj won't be aware of changes in the list.
		configuredProviders: List = config.conf['vision']['providers'][:]
		try:
			configuredProviders.remove(providerId)
			config.conf['vision']['providers'] = configuredProviders
		except ValueError:
			pass
		# As we cant rely on providers to de-register themselves from extension points when terminating them,
		# Re-create our extension points instance and ask active providers to reregister.
		self.extensionPoints = EventExtensionPoints()
		for providerInst in self.providers.values():
			try:
				providerInst.registerEventExtensionPoints(self.extensionPoints)
			except Exception:
				log.error(f"Error while registering to extension points for provider {providerId}", exc_info=True)
		if exception:
			raise exception

	def initializeProvider(
			self,
			provider: providerInfo.ProviderInfo,
			temporary: bool = False
	) -> None:
		"""
		Enables and activates the supplied provider.
		@param provider: The provider to initialise.
		@param temporary: Whether the selected provider is enabled temporarily (e.g. as a fallback).
			This defaults to C{False}.
			If C{True}, no changes will be performed to the configuration.
		"""
		providerId = provider.providerId
		providerInst = self.providers.pop(providerId, None)
		if providerInst is not None:
			providerInst.reinitialize()
		else:
			providerCls = provider.providerClass
			if not providerCls.canStart():
				raise exceptions.ProviderInitException(
					f"Trying to initialize provider {providerId!r} which reported being unable to start"
				)
			# Initialize the provider.
			providerInst = providerCls()
			# Register extension points.
			try:
				providerInst.registerEventExtensionPoints(self.extensionPoints)
			except Exception as registerEventExtensionPointsException:
				log.error(
					f"Error while registering to extension points for provider: {providerId}",
				)
				try:
					providerInst.terminate()
				except Exception:
					log.error(
						f"Error terminating provider {providerId} after registering to extension points", exc_info=True)
				raise registerEventExtensionPointsException
		if not temporary and providerId not in config.conf['vision']['providers']:
			config.conf['vision']['providers'] = config.conf['vision']['providers'][:] + [providerId]
		self.providers[providerId] = providerInst
		try:
			self.initialFocus()
		except Exception:
			# #8877: initialFocus might fail because NVDA tries to focus
			# an object for which property fetching raises an exception.
			# We should handle this more gracefully, since this is no reason
			# to stop a provider from loading successfully.
			log.debugWarning("Error in initial focus after provider load", exc_info=True)

	def terminate(self) -> None:
		self.extensionPoints = None
		config.post_configProfileSwitch.unregister(self.handleConfigProfileSwitch)
		for instance in self.providers.values():
			instance.terminate()
		self.providers.clear()

	def handleUpdate(self, obj, property: str) -> None:
		self.extensionPoints.post_objectUpdate.notify(obj=obj, property=property)

	def handleForeground(self, obj) -> None:
		self.extensionPoints.post_foregroundChange.notify(obj=obj)

	def handleGainFocus(self, obj) -> None:
		self.extensionPoints.post_focusChange.notify(obj=obj)
		hasNavigableText = getattr(obj, "_hasNavigableText", False)
		if hasNavigableText:
			# This object most likely has a caret.
			self.handleCaretMove(obj)

	def handleCaretMove(self, obj) -> None:
		if api.isCursorManager(obj):
			self.extensionPoints.post_browseModeMove.notify(obj=obj)
		else:
			self.extensionPoints.post_caretMove.notify(obj=obj)

	def handleReviewMove(self, context: Context = Context.REVIEW) -> None:
		self.extensionPoints.post_reviewMove.notify(context=context)

	def handleMouseMove(self, obj, x: int, y: int) -> None:
		# For now, mouse moves execute once per core cycle.
		self.extensionPoints.post_mouseMove.notify(obj=obj, x=x, y=y)

	def handleConfigProfileSwitch(self) -> None:
		configuredProviders = set(config.conf['vision']['providers'])
		curProviders = set(self.providers)
		providersToInitialize = configuredProviders - curProviders
		providersToTerminate = curProviders - configuredProviders
		for providerId in providersToTerminate:
			try:
				providerInfo = getProviderInfo(providerId)
				self.terminateProvider(providerInfo)
			except Exception:
				log.error(
					f"Could not terminate the {providerId} vision enhancement providerId",
					exc_info=True
				)
		for providerId in providersToInitialize:
			try:
				providerInfo = getProviderInfo(providerId)
				self.initializeProvider(providerInfo)
			except Exception:
				log.error(
					f"Could not initialize the {providerId} vision enhancement providerId",
					exc_info=True
				)

	def initialFocus(self) -> None:
		if not api.getDesktopObject():
			# focus/review hasn't yet been initialised.
			return
		self.handleGainFocus(api.getFocusObject())
