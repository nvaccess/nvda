# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2026 NV Access Limited, Babbage B.V., Cyrille Bougot, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Module containing the vision handler.

The vision handler is the core of the vision framework.
See the documentation of L{VisionHandler} for more details about what it does.
"""

from . import providerInfo  # noqa: I001
from .constants import Context
from locationHelper import RectLTRB
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
from . import exceptions


def _getProviderClass(
	moduleName: str,
	caseSensitive: bool = True,
) -> type[VisionEnhancementProvider]:
	"""Returns a registered provider class with the specified moduleName."""
	try:
		return importlib.import_module(
			"visionEnhancementProviders.%s" % moduleName,  # noqa: UP031
			package="visionEnhancementProviders",
		).VisionEnhancementProvider
	except ImportError as initialException:
		if caseSensitive:
			raise initialException  # noqa: TRY201
		for loader, name, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
			if name.startswith("_") or name.lower() != moduleName.lower():
				continue
			return importlib.import_module(
				"visionEnhancementProviders.%s" % name,  # noqa: UP031
				package="visionEnhancementProviders",
			).VisionEnhancementProvider
		raise initialException  # noqa: TRY201


def _getProvidersFromFileSystem():
	for loader, moduleName, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
		if moduleName.startswith("_"):
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
				providerClass=provider,
			)
		except Exception:  # Purposely catch everything as we don't know what a provider might raise.
			log.error(  # noqa: G201
				f"Error while importing vision enhancement provider module {moduleName}",
				exc_info=True,
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
		self._providers: dict[providerInfo.ProviderIdT, VisionEnhancementProvider] = dict()  # noqa: C408
		self.extensionPoints: EventExtensionPoints = EventExtensionPoints()
		queueHandler.queueFunction(queueHandler.eventQueue, self.postGuiInit)

	def postGuiInit(self) -> None:
		"""Handles first initialization of the handler as a config profile switch.
		This is executed on the main thread by L{__init__} using the events queue.
		This ensures that the gui is fully initialized before providers are initialized that might rely on it.
		"""
		self._updateAllProvidersList()
		self.handleConfigProfileSwitch()
		config.pre_configProfileSwitch.register(self.saveSettings)
		config.pre_configSave.register(self.saveSettings)
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	_allProviders: list[providerInfo.ProviderInfo] = []  # noqa: RUF012

	def _getBuiltInProviderIds(self):
		from visionEnhancementProviders.NVDAHighlighter import NVDAHighlighterSettings

		return [
			NVDAHighlighterSettings.getId(),
		]

	def _updateAllProvidersList(self):
		# Sort the providers alphabetically by id.
		# id is used because it will not vary by locale
		allProviders = sorted(
			_getProvidersFromFileSystem(),
			key=lambda info: info.providerId.lower(),
		)
		# Built in providers should come first
		# Python list.sort is stable sort again by 'built-in'
		builtInProviderIds = self._getBuiltInProviderIds()
		allProviders = sorted(
			allProviders,
			key=lambda info: info.providerId in builtInProviderIds,
			reverse=True,  # Because False comes before True, we want built-ins first.
		)
		self._allProviders = list(allProviders)

	def getProviderList(
		self,
		onlyStartable: bool = True,
		reloadFromSystem: bool = False,
	) -> list[providerInfo.ProviderInfo]:
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
				log.error(f"Error calling canStart for provider {provider.moduleName}", exc_info=True)  # noqa: G201
			else:
				if not onlyStartable or providerCanStart:
					providerList.append(provider)
				else:
					log.debugWarning(
						f"Excluding Vision enhancement provider module {provider.moduleName} which is unable to start",
					)
		return providerList

	def getProviderInfo(self, providerId: providerInfo.ProviderIdT) -> providerInfo.ProviderInfo | None:
		for p in self._allProviders:
			if p.providerId == providerId:
				return p
		raise LookupError(f"Provider with id ({providerId}) does not exist.")

	def getActiveProviderInstances(self):
		return list(self._providers.values())

	def getActiveProviderInfos(self) -> list[providerInfo.ProviderInfo]:
		activeProviderInfos = [self.getProviderInfo(p) for p in self._providers]
		return list(activeProviderInfos)

	def getConfiguredProviderInfos(self) -> list[providerInfo.ProviderInfo]:
		configuredProviderInfos: list[providerInfo.ProviderInfo] = [
			p for p in self._allProviders if p.providerClass.isEnabledInConfig()
		]
		return configuredProviderInfos

	def getProviderInstance(
		self,
		provider: providerInfo.ProviderInfo,
	) -> VisionEnhancementProvider | None:
		return self._providers.get(provider.providerId)

	def terminateProvider(
		self,
		provider: providerInfo.ProviderInfo,
		saveSettings: bool = True,
	) -> None:
		"""Terminates a currently active provider.
		When termination fails, an exception is raised.
		Yet, the provider will be removed from the providers dictionary,
		so its instance goes out of scope and wil lbe garbage collected.
		@param provider: The provider to terminate.
		@param saveSettings: Whether settings should be saved on termination.
		"""
		providerInstance = self._providers.get(provider.providerId)
		if providerInstance is None:
			raise exceptions.ProviderTerminateException(
				f"Tried to terminate uninitialized provider {provider.providerId!r}",
			)
		if saveSettings:
			try:
				providerInstance.getSettings().saveSettings()
			except Exception:
				log.exception(f"Error saving settings for {provider.providerId}")
		try:
			self._terminateProvider(provider)
		finally:
			providerInstance.enableInConfig(False)

	def _terminateProvider(self, provider: providerInfo.ProviderInfo) -> None:
		"""Release a provider without changing its configuration."""
		providerId = provider.providerId
		providerInstance = self._providers.pop(providerId)
		exception = None
		try:
			providerInstance.terminate()
		except Exception as e:  # noqa: BLE001
			# Purposely catch everything.
			# A provider can raise whatever exception,
			# therefore it is unknown what to expect.
			exception = e
		# As we cant rely on providers to de-register themselves from extension points when terminating them,
		# Re-create our extension points instance and ask active providers to reregister.
		self.extensionPoints = EventExtensionPoints()
		for providerInst in self._providers.values():
			try:
				providerInst.registerEventExtensionPoints(self.extensionPoints)
			except Exception:
				log.error(  # noqa: G201
					f"Error while registering to extension points for provider {providerId}",
					exc_info=True,
				)
		if exception:
			raise exception

	def initializeProvider(
		self,
		provider: providerInfo.ProviderInfo,
		temporary: bool = False,
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
				raise e  # noqa: TRY201
		else:
			providerCls = provider.providerClass
			if not providerCls.canStart():
				raise exceptions.ProviderInitException(
					f"Trying to initialize provider {providerId} which reported being unable to start",
				)
			try:
				# Initialize the provider.
				providerInst = providerCls()
			except Exception as e:
				# Disable the provider, so that it does not error every startup.
				providerCls.enableInConfig(False)
				log.warning(f"Error initialising {providerId}. Disabling in config.")
				raise e  # noqa: TRY201
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
					log.error(  # noqa: G201
						f"Error terminating provider {providerId} after registering to extension points",
						exc_info=True,
					)
				raise registerEventExtensionPointsException  # noqa: TRY201
		if not temporary:
			providerInst.enableInConfig(True)
		self._providers[providerId] = providerInst
		self._updateProviderPositions()

	def _updateProviderPositions(self) -> None:
		for update in (self.initialFocus, self.initialNavigatorObject):
			try:
				update()
			except Exception:  # noqa: BLE001
				# An inaccessible object must not prevent providers from starting or applying settings.
				log.debugWarning(f"Error in {update.__name__} after provider settings load", exc_info=True)

	def terminate(self) -> None:
		self.extensionPoints = None
		config.pre_configProfileSwitch.unregister(self.saveSettings)
		config.pre_configSave.unregister(self.saveSettings)
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

	def handleMathNavigation(self, rect: RectLTRB | None) -> None:
		"""Notify providers that the math navigation position has changed.

		:param rect: The current math navigation rectangle, or ``None`` if no rectangle is available.
		"""
		self.extensionPoints.post_mathNavigation.notify(rect=rect)

	def handleMouseMove(self, obj, x: int, y: int) -> None:
		# For now, mouse moves execute once per core cycle.
		self.extensionPoints.post_mouseMove.notify(obj=obj, x=x, y=y)

	def saveSettings(self) -> None:
		"""Save the settings of active providers."""
		for providerId, instance in self._providers.items():
			try:
				instance.getSettings().saveSettings()
			except Exception:
				log.exception(f"Error saving settings for {providerId}")

	def handleConfigProfileSwitch(self) -> None:
		configuredProviders: set[providerInfo.ProviderIdT] = set(  # noqa: C401
			info.providerId for info in self.getConfiguredProviderInfos()
		)
		curProviders: set[providerInfo.ProviderIdT] = set(self._providers)
		providersToInitialize = configuredProviders - curProviders
		providersToTerminate = curProviders - configuredProviders
		for providerId in providersToTerminate:
			try:
				info = self.getProviderInfo(providerId)
				self._terminateProvider(info)
			except Exception:
				log.error(  # noqa: G201
					f"Could not terminate the {providerId} vision enhancement provider",
					exc_info=True,
				)
		# Inactive providers also retain settings objects used by the settings dialog.
		for info in self._allProviders:
			try:
				info.providerClass.getSettings().loadSettings(onlyChanged=True)
				if instance := self._providers.get(info.providerId):
					instance.invalidateCache()
			except Exception:
				log.exception(f"Error loading settings for {info.providerId}")
		if self._providers:
			self._updateProviderPositions()
		for providerId in providersToInitialize:
			try:
				info = self.getProviderInfo(providerId)
				self.initializeProvider(info, temporary=True)
			except Exception:
				log.error(  # noqa: G201
					f"Could not initialize the {providerId} vision enhancement provider",
					exc_info=True,
				)

	def initialFocus(self) -> None:
		"""Handles the current focus when the provider is initialized.
		This function notifies one or more extension points; thus it can raise any type of exception.
		"""
		if not api.getDesktopObject():
			# focus/review hasn't yet been initialized.
			return
		self.handleGainFocus(api.getFocusObject())

	def initialNavigatorObject(self) -> None:
		"""Handles the current navigator object when the provider is initialized.
		This function notifies an extension point; thus it can raise any type of exception.
		"""
		if not api.getDesktopObject():
			# focus/review hasn't yet been initialized.
			return
		self.handleReviewMove(context=Context.REVIEW)
