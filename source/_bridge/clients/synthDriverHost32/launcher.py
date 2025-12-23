# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

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
from _bridge.components.services.logHandler import LogHandlerService
from _bridge.components.services.nvwave import WavePlayerService


@rpyc.service
class NVDAService:

	@rpyc.exposed
	def LogHandler(self) -> LogHandlerService:
		""" Return a LogHandler service wrapping the NVDA log handler, so remote clients can log messsages and check the log level. """
		return LogHandlerService()

	@rpyc.exposed
	def getLanguage(self) -> str:
		"""Get the current NVDA language. """
		return languageHandler.getLanguage()

	@rpyc.exposed
	def WavePlayer(self, channels: int, samplesPerSec: int, bitsPerSample: int, outputDevice: str, wantDucking: bool = True):
		""" return a WavePlayer service wrapping a new real WavePlayer instance. """
		return WavePlayerService(channels=channels, samplesPerSec=samplesPerSec, bitsPerSample=bitsPerSample, outputDevice=outputDevice, wantDucking=wantDucking)


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

def createSynthDriverHost32():
	"""Start the 32-bit synth driver host process and connect to its RPYC service over the hosts standard pipes.
	Instructs the host to install proxies that use the given NVDAService for remote calls back into NVDA.
	:returns: The remote SynthDriverHostService instance.
	  """
	global stream, conn
	isSecureDesktop = isRunningOnSecureDesktop()
	log.info(f"Starting synthDriverHost32 process: {_hostExe}")
	securePopenOptions = launchConfig_secure if isSecureDesktop else launchConfig_standard
	hostProc = secureProcess.SecurePopen(
		[_hostExe], killOnDelete=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
		hideCriticalErrorDialogs=True, createNoWindow=True,
		**securePopenOptions
		)
	log.info("Creating PipeStream over host process std pipes")
	stream = PipeStream(hostProc.stdout, hostProc.stdin)
	log.info("Connecting to synthDriverHost32 process RPYC service over PipeStream")
	conn = rpyc.connect_stream(stream, config={'allow_public_attrs': False, 'allow_safe_attrs': False})
	conn._hostProc = hostProc
	log.info("Starting background thread to service synthDriverHost32 process RPYC requests")
	t = threading.Thread(target=conn.serve_all, daemon=True)
	t.start()
	conn.root.installProxies(NVDAService())
	return conn.root
