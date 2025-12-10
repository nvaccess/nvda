# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import typing
import importlib
import types
import logging
import rpyc
from _bridge.components.services.synthDriver import SynthDriverService
if typing.TYPE_CHECKING:
	from _bridge.clients.synthDriverHost32 import NVDAService

# Monkeypatch RPYC to force it to use builtins for its exceptions module.
# On Python 3 it normally would, but
# as we have an `exceptions` module in NVDA, it picks that up instead,
# thinking it is the old Python 2 exceptions module
# and causing remote exceptions to fail deserialization.
import builtins
import rpyc.core.vinegar
rpyc.core.vinegar.exceptions_module = builtins

log = logging.getLogger()


@rpyc.service
class HostService(rpyc.Service):
	"""RPYC service for the synth driver host runtime."""

	@rpyc.exposed
	def installProxies(self, remoteService: NVDAService):
		"""Install and bind proxy objects from the parent NVDA process.

		This exposed RPYC service method configures the local runtime to use
		proxies provided by the parent NVDA process. It performs a set of
		side-effects required so local synth drivers can initialize and use the
		remote implementations.
		This includes languageHandler, logging and nvwave.

		:param remoteService: A remote service proxy exposing the required components.
		:raises ImportError: If required local components cannot be imported.
		:raises AttributeError: If the remoteService is missing expected
		    attributes.
		:returns: None
		"""

		global log
		log.info("Injecting log into logHandler")
		from _bridge.components.proxies.logHandler import LogHandlerProxy
		log = LogHandlerProxy(remoteService.LogHandler())
		import logHandler
		logHandler.log = log
		log.info("Injecting languageHandler.getLanguage")
		import languageHandler
		languageHandler.getLanguage = remoteService.getLanguage
		log.info("Injecting WavePlayerProxy into nvwave module")
		from _bridge.components.proxies.nvwave import WavePlayerProxy
		import nvwave
		nvwave.WavePlayer = WavePlayerProxy._createBoundProxyClass(remoteService.WavePlayer)

	@rpyc.exposed
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
		import synthDrivers
		synthDrivers.__path__.insert(0, path)

	@rpyc.exposed
	def SynthDriver(self, name: str) -> SynthDriverService:
		""" Loads a synthDriver with the given name, exposing it to the remote caller as a SynthDriverService.

		:param name: Name of the synth driver to load.
		:raises ImportError: If the SynthDriverService implementation cannot be imported.
		:returns: SynthDriverService instance bound to the requested driver name.
		"""
		mod = importlib.import_module(f'synthDrivers.{name}')
		synth = mod.SynthDriver()
		return SynthDriverService(synth)


def main():
	"""Entry point for the synth driver host runtime. """
	global log
	log.info("Connecting to RPYC server over standard pipes")
	conn = rpyc.connect_stdpipes(HostService, config={'allowpublic_attrs': False, 'allow_safe_attrs': False})
	log.info("Connected to remote service")
	log.info("Entering service loop.")
	conn.serve_all()
