# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import cast
import os
import threading
import subprocess
import rpyc
from rpyc.core.stream import PipeStream
import NVDAState
from utils.security import isRunningOnSecureDesktop
import secureProcess
from logHandler import log
import languageHandler
from _bridge.base import Connection, Service
from _bridge.components.services.logHandler import LogHandlerService
from _bridge.components.services.nvwave import WavePlayerService
from _bridge.components.services.synthDriver import SynthDriverService


@rpyc.service
class NVDAService(Service):
	""" The main NVDA service exposed to remote synth driver hosts. """

	def __init__(self, childProcess: secureProcess.SecurePopen):
		super().__init__(childProcess)

	@Service.exposed
	def LogHandler(self) -> LogHandlerService:
		""" Return a LogHandler service wrapping the NVDA log handler, so remote clients can log messsages and check the log level. """
		return LogHandlerService()

	@Service.exposed
	def getAppDir(self):
		""" Get the NVDA application directory. """
		import globalVars
		return globalVars.appDir

	@Service.exposed
	def getLanguage(self) -> str:
		"""Get the current NVDA language. """
		return languageHandler.getLanguage()

	@Service.exposed
	def WavePlayer(self, channels: int, samplesPerSec: int, bitsPerSample: int, outputDevice: str, wantDucking: bool = True):
		""" return a WavePlayer service wrapping a new real WavePlayer instance. """
		return WavePlayerService(self._childProcess, channels=channels, samplesPerSec=samplesPerSec, bitsPerSample=bitsPerSample, outputDevice=outputDevice, wantDucking=wantDucking)


_hostExe = os.path.join(NVDAState.ReadPaths.versionedLibX86Path, "synthDriverHost-runtime/nvda_synthDriverHost.exe")

def isSynthDriverHost32RuntimeAvailable():
	return os.path.isfile(_hostExe)


launchConfig_standard = dict(
	removeElevation=True, removePrivileges=True, integrityLevel='low', applyUIRestrictions=True,
	restrictToken=True, retainUserInRestrictedToken=True,
)
launchConfig_secure = dict(
	username="local service", domain="nt authority", logonType="service",
	appContainerName="nvdaSynthDriverHost", appContainerCapabilities=[],
	isolateWindowStation=True, applyUIRestrictions=True,
)

def createSynthDriver(name: str, synthDriversPath: str) -> tuple[Connection, SynthDriverService]:
	"""Start the 32-bit synth driver host process and connect to its RPYC service over the hosts standard pipes.
	Instructs the host to install proxies that use the given NVDAService for remote calls back into NVDA.
	:returns: The remote SynthDriverHostService instance.
	  """
	isSecureDesktop = isRunningOnSecureDesktop()
	log.debug(f"Starting synthDriverHost32 process: {_hostExe}")
	securePopenOptions = launchConfig_secure if isSecureDesktop else launchConfig_standard
	hostProc = secureProcess.SecurePopen(
		[_hostExe], killOnDelete=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
		hideCriticalErrorDialogs=True, createNoWindow=True,
		**securePopenOptions
		)
	log.debug("Creating PipeStream over host process std pipes")
	stream = PipeStream(hostProc.stdout, hostProc.stdin)
	log.debug("Connecting to synthDriverHost32 process RPYC service over PipeStream")
	service = NVDAService(hostProc)
	conn = Connection(stream, service, name="synthDriverHost32")
	conn.bgEventLoop(daemon=True)
	log.debug("Connection to synthDriverHost32 process RPYC service established")
	from _bridge.runtimes.synthDriverHost.synthDriverHost import HostService
	remoteService = cast(HostService, conn.remoteService)
	conn.remoteService.installProxies(service)
	log.debug("Creating SynthDriverProxy over remote SynthDriverService")
	conn.remoteService.registerSynthDriversPath(synthDriversPath)
	synthDriverService = conn.remoteService.SynthDriver(name)
	return conn, synthDriverService
