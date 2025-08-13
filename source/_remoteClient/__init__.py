# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
from logHandler import log

from .client import RemoteClient
from .configuration import getRemoteConfig

_remoteClient: RemoteClient = None


def initialize():
	"""Initialise the remote client."""
	global _remoteClient
	if not getRemoteConfig()["enabled"]:
		log.debug("Remote Access disabled. Not initializing.")
		return
	import globalCommands

	log.debug("Initializing Remote Access")
	_remoteClient = RemoteClient()
	_remoteClient.registerLocalScript(globalCommands.commands.script_sendKeys)
	_remoteClient.registerLocalScript(globalCommands.commands.script_sendSAS)


def terminate():
	"""Terminate the remote client."""
	global _remoteClient
	if _remoteClient is None:
		log.debug("Remote Access not running.")
		return
	log.debug("Terminating Remote Access")
	_remoteClient.terminate()
	_remoteClient = None


def remoteRunning() -> bool:
	return _remoteClient is not None
