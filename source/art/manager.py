# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import subprocess
from pathlib import Path
from typing import Dict, Optional
import threading
import time

import Pyro5.api

from processManager import SubprocessManager, ProcessConfig
from logHandler import log


ART_CONFIG = ProcessConfig(
	name="NVDA ART",
	sourceScriptPath=Path("nvda_art.pyw"),
	builtExeName="nvda_art.pyw",
	popenFlags={
		"creationflags": subprocess.CREATE_NO_WINDOW,
		"bufsize": 0,
		"stdin": subprocess.PIPE,
		"stdout": subprocess.PIPE,
	}
)


class ARTManager:
	"""Manages the NVDA Add-on Runtime process."""
	
	def __init__(self):
		self.subprocessManager = SubprocessManager(ART_CONFIG)
		self.artServices: Dict[str, Pyro5.api.Proxy] = {}
		self._connectionThread: Optional[threading.Thread] = None
		self._shutdownEvent = threading.Event()
		
	def start(self):
		"""Start the ART process and connect to its services."""
		log.info("Starting NVDA ART process")
		self.subprocessManager.ensureProcessRunning()
		
		# Start connection thread to read service URIs
		self._connectionThread = threading.Thread(
			target=self._connectToServices,
			name="ARTConnection"
		)
		self._connectionThread.start()
		
	def _connectToServices(self):
		"""Read service URIs from ART process stdout and connect."""
		if not self.subprocessManager.subprocess:
			log.error("ART subprocess not available")
			return
			
		stdout = self.subprocessManager.subprocess.stdout
		endTime = time.time() + 10.0  # 10 second timeout
		
		while not self._shutdownEvent.is_set():
			if time.time() > endTime:
				log.error("Timeout waiting for ART service URIs")
				break
				
			line = stdout.readline()
			if not line:
				time.sleep(0.1)
				continue
				
			line = line.decode('utf-8').strip()
			
			if line.startswith("ART_SERVICE_URI:"):
				uri = line.split(":", 1)[1]
				self._connectService("addon_lifecycle", uri)
				
			elif line.startswith("ART_EXT_SERVICE_URI:"):
				uri = line.split(":", 1)[1]
				self._connectService("extension_points", uri)
				
			elif line.startswith("ART_HANDLER_SERVICE_URI:"):
				uri = line.split(":", 1)[1]
				self._connectService("handlers", uri)
				
			# Check if we have all expected services
			if len(self.artServices) >= 3:
				log.info("Connected to all ART services")
				break
				
	def _connectService(self, name: str, uri: str):
		"""Connect to a specific ART service."""
		try:
			proxy = Pyro5.api.Proxy(uri)
			proxy._pyroTimeout = 2.0
			self.artServices[name] = proxy
			log.info(f"Connected to ART service: {name}")
		except Exception:
			log.exception(f"Failed to connect to ART service: {name}")
			
	def stop(self):
		"""Stop the ART process."""
		log.info("Stopping NVDA ART process")
		self._shutdownEvent.set()
		
		if self._connectionThread:
			self._connectionThread.join(timeout=5.0)
			
		# Close service proxies
		for proxy in self.artServices.values():
			try:
				proxy._pyroRelease()
			except Exception:
				pass
				
		self.artServices.clear()
		self.subprocessManager.terminate()
		
	def getService(self, name: str) -> Optional[Pyro5.api.Proxy]:
		"""Get a proxy to an ART service."""
		return self.artServices.get(name)
