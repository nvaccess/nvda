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
from typing import Type, Dict, List, Optional, Set
from . import exceptions


def _getProviderClass(
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


def _getProvidersFromFileSystem():
	for loader, moduleName, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
		if moduleName.startswith('_'):
			continue
		try:
			#  Get each piece of info in a new statement so any exceptions raised identifies the line correctly.
			provider = _getProviderClass(moduleName)
			providerSettings = provider.getSettings()
			providerId = providerSettings.getId()
			displayName = providerSettings.getDisplayName()
			yield providerInfo.ProviderInfo(
				providerId=providerId,
				moduleName=moduleName,
				displayName=displayName,
				providerClass=provider
			)
		except Exception:  # Purposely catch everything as we don't know what a provider might raise.
			log.error(
				f"Error while importing vision enhancement provider module {moduleName}",
				exc_info=True
			)
			continue


class VisionHandler(AutoPropertyObject):
	"""The singleton vision handler is the core of the vision framework.
	It performs the following tasks:

		* It keeps track of active vision enhancement _providers in the L{_providers} dictionary.
		* It processes initialization and termination of providers.
		* It receives certain events from the core of NVDA,
			delegating them to the appropriate extension points.
	"""

	def __init__(self):
		self._providers: Dict[providerInfo.ProviderIdT, VisionEnhancementProvider] = dict()
		self.extensionPoints: EventExtensionPoints = EventExtensionPoints()
		queueHandler.queueFunction(queueHandler.eventQueue, self.postGuiInit)

	def postGuiInit(self) -> None:
		"""Handles first initialization of the handler as a config profile switch.
		This is executed on the main thread by L{__init__} using the events queue.
		This ensures that the gui is fully initialized before providers are initialized that might rely on it.
		"""
		self._updateAllProvidersList()
		self.handleConfigProfileSwitch()
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	_allProviders: List[providerInfo.ProviderInfo] = []

	def _getBuiltInProviderIds(self):
		from visionEnhancementProviders.NVDAHighlighter import NVDAHighlighterSettings
		from visionEnhancementProviders.screenCurtain import ScreenCurtainSettings
		return [
			NVDAHighlighterSettings.getId(),
			ScreenCurtainSettings.getId()
		]

	def _updateAllProvidersList(self):
		# Sort the providers alphabetically by id.
		# id is used because it will not vary by locale
		allProviders = sorted(
			_getProvidersFromFileSystem(),
			key=lambda info: info.providerId.lower()
		)
		# Built in providers should come first
		# Python list.sort is stable sort again by 'built-in'
		builtInProviderIds = self._getBuiltInProviderIds()
		allProviders = sorted(
			allProviders,
			key=lambda info: info.providerId in builtInProviderIds,
			reverse=True  # Because False comes before True, we want built-ins first.
		)
		self._allProviders = list(allProviders)

	def getProviderList(
			self,
			onlyStartable: bool = True,
			reloadFromSystem: bool = False,
	) -> List[providerInfo.ProviderInfo]:
		"""Gets a list of available vision enhancement provider information
		@param onlyStartable: excludes all providers for which the check method returns C{False}.
		@param reloadFromSystem: ensure the list is fresh. Providers may have been added to the file system.
		@return: List of available providers
		"""
		if reloadFromSystem or not self._allProviders:
			self._updateAllProvidersList()

		providerList = []
		for provider in self._allProviders:
			try:
				providerCanStart = provider.providerClass.canStart()
			except Exception:  # Purposely catch everything as we don't know what a provider might raise.
				log.error(f"Error calling canStart for provider {provider.moduleName}", exc_info=True)
			else:
				if not onlyStartable or providerCanStart:
					providerList.append(provider)
				else:
					log.debugWarning(
						f"Excluding Vision enhancement provider module {provider.moduleName} which is unable to start"
					)
		return providerList

	def getProviderInfo(self, providerId: providerInfo.ProviderIdT) -> Optional[providerInfo.ProviderInfo]:
		for p in self._allProviders:
			if p.providerId == providerId:
				return p
		raise LookupError(f"Provider with id ({providerId}) does not exist.")

	def getActiveProviderInstances(self):
		return list(self._providers.values())

	def getActiveProviderInfos(self) -> List[providerInfo.ProviderInfo]:
		activeProviderInfos = [
			self.getProviderInfo(p) for p in self._providers
		]
		return list(activeProviderInfos)

	def getConfiguredProviderInfos(self) -> List[providerInfo.ProviderInfo]:
		configuredProviderInfos: List[providerInfo.ProviderInfo] = [
			p for p in self._allProviders
			if p.providerClass.isEnabledInConfig()
		]
		return configuredProviderInfos

	def getProviderInstance(
			self,
			provider: providerInfo.ProviderInfo
	) -> Optional[VisionEnhancementProvider]:
		return self._providers.get(provider.providerId)

	def terminateProvider(
			self,
			provider: providerInfo.ProviderInfo,
			saveSettings: bool = True
	) -> None:
		"""Terminates a currently active provider.
		When termination fails, an exception is raised.
		Yet, the provider will be removed from the providers dictionary,
		so its instance goes out of scope and wil lbe garbage collected.
		@param provider: The provider to terminate.
		@param saveSettings: Whether settings should be saved on termination.
		"""
		providerId = provider.providerId
		# Remove the provider from the _providers dictionary.
		providerInstance = self._providers.pop(providerId, None)
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
		providerInstance.enableInConfig(False)
		# As we cant rely on providers to de-register themselves from extension points when terminating them,
		# Re-create our extension points instance and ask active providers to reregister.
		self.extensionPoints = EventExtensionPoints()
		for providerInst in self._providers.values():
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
		@param provider: The provider to initialize.
		@param temporary: Whether the selected provider is enabled temporarily (e.g. as a fallback).
			This defaults to C{False}.
			If C{True}, no changes will be performed to the configuration.
		@note: On error, an an Exception is raised.
		"""
		providerId = provider.providerId
		providerInst = self._providers.pop(providerId, None)
		if providerInst is not None:
			try:
				providerInst.reinitialize()
			except Exception as e:
				log.error(f"Error while re-initialising {providerId}")
				raise e
		else:
			providerCls = provider.providerClass
			if not providerCls.canStart():
				raise exceptions.ProviderInitException(
					f"Trying to initialize provider {providerId} which reported being unable to start"
				)
			try:
				# Initialize the provider.
				providerInst = providerCls()
			except Exception as e:
				# Disable the provider, so that it does not error every startup.
				providerCls.enableInConfig(False)
				log.warning(f"Error initialising {providerId}. Disabling in config.")
				raise e
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
		if not temporary:
			providerInst.enableInConfig(True)
		self._providers[providerId] = providerInst
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
		for instance in self._providers.values():
			instance.terminate()
		self._providers.clear()

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
		configuredProviders: Set[providerInfo.ProviderIdT] = set(
			info.providerId for info in self.getConfiguredProviderInfos()
		)
		curProviders: Set[providerInfo.ProviderIdT] = set(self._providers)
		providersToInitialize = configuredProviders - curProviders
		providersToTerminate = curProviders - configuredProviders
		for providerId in providersToTerminate:
			try:
				info = self.getProviderInfo(providerId)
				self.terminateProvider(info)
			except Exception:
				log.error(
					f"Could not terminate the {providerId} vision enhancement provider",
					exc_info=True
				)
		for providerId in providersToInitialize:
			try:
				info = self.getProviderInfo(providerId)
				self.initializeProvider(info)
			except Exception:
				log.error(
					f"Could not initialize the {providerId} vision enhancement provider",
					exc_info=True
				)

	def initialFocus(self) -> None:
		if not api.getDesktopObject():
			# focus/review hasn't yet been initialized.
			return
		self.handleGainFocus(api.getFocusObject())
