# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from .client import RemoteClient


def initialize():
	"""Initialise the remote client."""
	import globalVars
	import globalCommands

	globalVars.remoteClient = RemoteClient()
	globalVars.remoteClient.registerLocalScript(globalCommands.commands.script_sendKeys)


def terminate():
	"""Terminate the remote client."""
	import globalVars

	globalVars.remoteClient.terminate()
	globalVars.remoteClient = None
