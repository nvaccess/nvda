# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import typing
import sys
import importlib
import rpyc
from rpyc.core.stream import PipeStream
from _bridge.components.services.synthDriver import SynthDriverService


if typing.TYPE_CHECKING:
	from _bridge.clients.synthDriverHost32.launcher import NVDAService
from _bridge.base import Connection
from logHandler import log
from _bridge.base import Service


# Monkeypatch RPYC to force it to use builtins for its exceptions module.
# On Python 3 it normally would, but
# as we have an `exceptions` module in NVDA, it picks that up instead,
# thinking it is the old Python 2 exceptions module
# and causing remote exceptions to fail deserialization.
import builtins
import rpyc.core.vinegar

rpyc.core.vinegar.exceptions_module = builtins


@rpyc.service
class HostService(Service):
	"""RPYC service for the synth driver host runtime."""

	def __init__(self):
		super().__init__()

	@Service.exposed
	def installProxies(self, remoteService: NVDAService):
		"""Install and bind proxy objects from the parent NVDA process.

		This exposed RPYC service method configures the local runtime to use
		proxies provided by the parent NVDA process. It performs a set of
		side-effects required so local synth drivers can initialize and use the
		remote implementations.
		:param remoteService: A remote service proxy exposing the required components.
		:raises ImportError: If required local components cannot be imported.
		:raises AttributeError: If the remoteService is missing expected
		    attributes.
		:returns: None
		"""
		log.debug("Installing proxies from remote NVDAService")
		import NVDAState

		isRunningAsSource = remoteService.isRunningAsSource()
		NVDAState.isRunningAsSource = lambda: isRunningAsSource

		class _ReadPaths(NVDAState._ReadPaths):
			@property
			def versionedLibPath(self) -> str:
				if not hasattr(self, "_versionedLibPath"):
					self._versionedLibPath = remoteService.getVersionedLibPath()
				return self._versionedLibPath

		NVDAState.ReadPaths = _ReadPaths()
		import globalVars

		globalVars.appDir = remoteService.getAppDir()
		log.debug("Injecting languageHandler.getLanguage")
		import languageHandler

		languageHandler.getLanguage = remoteService.getLanguage

		log.debug("Synchronizing configuration values")
		configNeeded = [
			("audio", ["outputDevice", "audioAwakeTime", "whiteNoiseVolume"]),
			("speech", ["useWASAPIForSAPI4", "trimLeadingSilence"]),
			("debugLog", ["synthDriver"]),
		]
		import config

		for section, keys in configNeeded:
			config.conf[section] = {}
			for key in keys:
				config.conf[section][key] = remoteService.getConfigValue(section, key)

		log.debug("Initializing nvwave")
		import nvwave

		nvwave.initialize()

	@Service.exposed
	def registerSynthDriversPath(self, path: str):
		"""Register an additional path to search for synth drivers.

		This exposed RPYC method inserts the given filesystem path at the
		front of the synthDrivers package search path so that synth drivers
		located in the provided directory are discovered and loaded before
		those on the existing path.

		:param path: Filesystem path to register for synth driver discovery.
		:raises ImportError: If the local synthDrivers package cannot be
		    imported.
		:returns: None
		"""
		log.debug(f"Registering synth drivers path: {path}")
		import synthDrivers

		synthDrivers.__path__.insert(0, path)

	@Service.exposed
	def SynthDriver(self, name: str) -> SynthDriverService:
		"""Loads a synthDriver with the given name, exposing it to the remote caller as a SynthDriverService.

		:param name: Name of the synth driver to load.
		:raises ImportError: If the SynthDriverService implementation cannot be imported.
		:returns: SynthDriverService instance bound to the requested driver name.
		"""
		log.debug(f"Loading synth driver '{name}'")
		mod = importlib.import_module(f"synthDrivers.{name}")
		synth = mod.SynthDriver()
		return SynthDriverService(synth)


def main():
	"""Entry point for the synth driver host runtime."""
	log.debug("Connecting to RPYC server over standard pipes")
	stream = PipeStream(sys.stdin, sys.stdout)
	service = HostService()
	conn = Connection(stream, service, name="synthDriverHost service connection")
	log.debug("Entering service loop.")
	conn.eventLoop()
	log.debug("Service loop exited, shutting down.")
