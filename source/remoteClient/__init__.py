# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from .client import RemoteClient

_remoteClient: RemoteClient = None


def initialize():
	"""Initialise the remote client."""
	global _remoteClient
	import globalCommands

	_remoteClient = RemoteClient()
	_remoteClient.registerLocalScript(globalCommands.commands.script_sendKeys)


def terminate():
	"""Terminate the remote client."""
	global _remoteClient
	if _remoteClient is not None:
		_remoteClient.terminate()
		_remoteClient = None


def remoteRunning() -> bool:
	return _remoteClient is not None
