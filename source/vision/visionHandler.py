# vision/visionHandler.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing the vision handler.

The vision handler is the core of the vision framework.
See the documentation of L{VisionHandler} for more details about what it does.
"""

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
from typing import Type, Dict, List
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


class VisionHandler(AutoPropertyObject):
	"""The singleton vision handler is the core of the vision framework.
	It performs the following tasks:

		* It keeps track of active vision enhancement providers in the L{providers} dictionary.
		* It processes initialization and termnation of  providers.
		* It receives certain events from the core of NVDA,
			delegating them to the appropriate extension points.
	"""

	def __init__(self):
		self.providers: Dict[str, VisionEnhancementProvider] = dict()
		self.extensionPoints: EventExtensionPoints = EventExtensionPoints()
		queueHandler.queueFunction(queueHandler.eventQueue, self.postGuiInit)

	def postGuiInit(self) -> None:
		"""Handles first initialization of the handler as a config profile switch.
		This is executed on the main thread by L{__init__} using the events queue.
		This ensures that the gui is fully initialized before providers are initialized that might rely on it.
		"""
		self.handleConfigProfileSwitch()
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

	def terminateProvider(self, providerName: str, saveSettings: bool = True):
		"""Terminates a currently active provider.
		When termnation fails, an exception is raised.
		Yet, the provider wil lbe removed from the providers dictionary,
		so its instance goes out of scope and wil lbe garbage collected.
		@param providerName: The provider to terminate.
		@param saveSettings: Whether settings should be saved on termionation.
		"""
		success = True  # todo: can we remove this? seems unused, what is the history?
		# Remove the provider from the providers dictionary.
		providerInstance = self.providers.pop(providerName, None)
		if not providerInstance:
			raise exceptions.ProviderTerminateException(
				f"Tried to terminate uninitialized provider {providerName!r}"
			)
		exception = None
		try:
			providerInstance.terminate(saveSettings=saveSettings)
		except Exception as e:
			# Purposely catch everything.
			# A provider can raise whatever exception,
			# therefore it is unknown what to expect.
			exception = e
		# Copy the configured providers before mutating the list.
		# If we don't, configobj won't be aware of changes the list.
		configuredProviders: List = config.conf['vision']['providers'][:]
		try:
			configuredProviders.remove(providerName)
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
				log.error("Error while registering to extension points for provider %s" % providerName, exc_info=True)
		if exception:
			raise exception

	@staticmethod
	def confirmInitWithUser(providerName: str) -> bool:
		"""Before initialisation of a provider,
		confirm with the user that the provider should start.
		This method calls confirmInitWithUser on the provider,
		and should be executed on the main thread.
		@returns: C{True} if initialisation should continue, C{False} otherwise.
		"""
		providerCls = getProviderClass(providerName)
		return providerCls.confirmInitWithUser()

	def initializeProvider(self, providerName: str, temporary: bool = False):
		"""
		Enables and activates the supplied provider.
		@param providerName: The name of the registered provider.
		@param temporary: Whether the selected provider is enabled temporarily (e.g. as a fallback).
			This defaults to C{False}.
			If C{True}, no changes will be performed to the configuration.
		"""
		providerInst = self.providers.pop(providerName, None)
		if providerInst is not None:
			providerCls = type(providerInst)
			providerInst.reinitialize()
		else:
			try:
				providerCls = getProviderClass(providerName)
			except ModuleNotFoundError:
				raise exceptions.ProviderInitException(f"No provider named {providerName!r}")
			else:
				if not providerCls.canStart():
					raise exceptions.ProviderInitException(
						f"Trying to initialize provider {providerName!r} which reported being unable to start"
					)
			# Initialize the provider.
			providerInst = providerCls()
			# Register extension points.
			try:
				providerInst.registerEventExtensionPoints(self.extensionPoints)
			except Exception as registerEventExtensionPointsException:
				log.error(
					f"Error while registering to extension points for provider {providerName}",
				)
				try:
					providerInst.terminate()
				except Exception:
					log.error(
						f"Error terminating provider {providerName} after registering to extension points", exc_info=True)
				raise registerEventExtensionPointsException
		providerSettings = providerCls.getSettings()
		providerSettings.initSettings()  # todo: do we actually have to do this here? It might actually cause a bug, reloading settings and overwriting current static settings.
		if not temporary and providerName not in config.conf['vision']['providers']:
			config.conf['vision']['providers'] = config.conf['vision']['providers'][:] + [providerName]
		self.providers[providerName] = providerInst
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
		for provider in providersToTerminate:
			try:
				self.terminateProvider(provider)
			except Exception:
				log.error(
					f"Could not terminate the {provider} vision enhancement provider",
					exc_info=True
				)
		for provider in providersToInitialize:
			try:
				self.initializeProvider(provider)
			except Exception:
				log.error(
					f"Could not initialize the {provider} vision enhancement provider",
					exc_info=True
				)

	def initialFocus(self) -> None:
		if not api.getDesktopObject():
			# focus/review hasn't yet been initialised.
			return
		self.handleGainFocus(api.getFocusObject())
