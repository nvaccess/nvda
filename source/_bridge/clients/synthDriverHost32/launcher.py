# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import subprocess
import rpyc
from rpyc.core.stream import PipeStream
import NVDAState
from logHandler import log
import languageHandler
from _bridge.base import Connection, Service
from _bridge.components.services.synthDriver import SynthDriverService
from winBindings.jobapi2 import JOB_OBJECT_LIMIT
import jobObject


@rpyc.service
class NVDAService(Service):
	"""The main NVDA service exposed to remote synth driver hosts."""

	def __init__(self, childProcess: subprocess.Popen):
		super().__init__(childProcess)

	@Service.exposed
	def getAppDir(self):
		"""Get the NVDA application directory."""
		import globalVars

		return globalVars.appDir

	@Service.exposed
	def getLanguage(self) -> str:
		"""Get the current NVDA language."""
		return languageHandler.getLanguage()

	@Service.exposed
	def isRunningAsSource(self) -> bool:
		"""Return whether NVDA is running from source."""
		return NVDAState.isRunningAsSource()

	@Service.exposed
	def getVersionedLibPath(self) -> str:
		return NVDAState.ReadPaths.versionedLibPath


_hostExe = os.path.join(
	NVDAState.ReadPaths.versionedLibX86Path,
	"synthDriverHost-runtime/nvda_synthDriverHost.exe",
)


def isSynthDriverHost32RuntimeAvailable():
	return os.path.isfile(_hostExe)


def createSynthDriver(name: str, synthDriversPath: str) -> tuple[Connection, SynthDriverService]:
	"""Start the 32-bit synth driver host process and connect to its RPYC service over the hosts standard pipes.
	Instructs the host to install proxies that use the given NVDAService for remote calls back into NVDA.
	:returns: The remote SynthDriverHostService instance.
	"""
	job = jobObject.Job()
	job.setBasicLimits(JOB_OBJECT_LIMIT.KILL_ON_JOB_CLOSE)
	log.debug(f"Starting synthDriverHost32 process: {_hostExe}")
	hostProc = subprocess.Popen(
		[_hostExe],
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		creationflags=subprocess.CREATE_NO_WINDOW,
	)
	job.assignProcess(hostProc._handle)
	hostProc._job = job  # Prevent job from being GC'd while process is running
	log.debug("Creating PipeStream over host process std pipes")
	stream = PipeStream(hostProc.stdout, hostProc.stdin)
	log.debug("Connecting to synthDriverHost32 process RPYC service over PipeStream")
	service = NVDAService(hostProc)
	conn = Connection(stream, service, name="synthDriverHost32")
	conn.bgEventLoop(daemon=True)
	log.debug("Connection to synthDriverHost32 process RPYC service established")

	conn.remoteService.installProxies(service)
	log.debug("Creating SynthDriverProxy over remote SynthDriverService")
	conn.remoteService.registerSynthDriversPath(synthDriversPath)
	synthDriverService = conn.remoteService.SynthDriver(name)
	return conn, synthDriverService
