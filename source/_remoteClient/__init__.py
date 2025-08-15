# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from gui.message import DefaultButton, DialogType, MessageDialog, ReturnCode
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


def _confirmBeforeNVDAExit() -> bool:
	if remoteRunning():
		if (
			_remoteClient.followerSession is not None
			and getRemoteConfig()["ui"]["confirmDisconnectAsFollower"]
		):
			dialog = MessageDialog(
				parent=None,
				# Translators: Title of the Remote Access disconnection confirmation dialog.
				title=_("Exit NVDA"),
				message=_(
					# Translators: Confirmation before exiting when controlled.
					"Are you sure you want to exit NVDA? You will be disconnected from the Remote Access session.",
				),
				dialogType=DialogType.WARNING,
				buttons=(
					DefaultButton.YES,
					DefaultButton.NO.value._replace(defaultFocus=True, fallbackAction=True),
				),
			)
			return dialog.ShowModal() == ReturnCode.YES
	return True
