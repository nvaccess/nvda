# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
from typing import TypedDict

import globalVars
import nvwave
import ui
from logHandler import log


class Cue(TypedDict, total=False):
	wave: str | None
	message: str | None


# Declarative dictionary of all possible cues
CUES: dict[str, Cue] = {
	"connected": {
		"wave": "connected",
	},
	"disconnected": {
		"wave": "disconnected",
		# Translators: Message shown when the connection to the remote computer is lost.
		"message": _("Disconnected"),
	},
	"controlServerConnected": {
		"wave": "controlled",
		# Translators: Presented in direct (client to server) Remote Access connection when the controlled computer is ready.
		"message": pgettext("remote", "Connected as controlled computer"),
	},
	"clientConnected": {
		"wave": "controlling",
	},
	"clientDisconnected": {
		"wave": "disconnected",
	},
	"clipboardPushed": {
		"wave": "clipboardPush",
		# Translators: Message shown when the clipboard is successfully sent to the remote computer.
		"message": pgettext("remote", "Clipboard sent"),
	},
	"clipboardReceived": {
		"wave": "clipboardReceive",
		# Translators: Message shown when the clipboard is successfully received from the remote computer.
		"message": _("Clipboard received"),
	},
}


def _playCue(cueName: str) -> None:
	"""Helper function to play a cue by name"""
	# Play wave file
	if wave := CUES[cueName].get("wave"):
		filePath = os.path.join(globalVars.appDir, "waves", wave + ".wav")
		try:
			nvwave.playWaveFile(filePath)
		except Exception:
			# We mustn't log at error level, as this may play a sound
			# and playing a sound is what caused this exception.
			log.debugWarning(f"Failed to play cue {filePath!r}.", exc_info=True)

	# Show message if specified
	if message := CUES[cueName].get("message"):
		ui.delayedMessage(message)


def connected():
	_playCue("connected")


def disconnected():
	_playCue("disconnected")


def controlServerConnected():
	_playCue("controlServerConnected")


def clientConnected():
	_playCue("clientConnected")


def clientDisconnected():
	_playCue("clientDisconnected")


def clipboardPushed():
	_playCue("clipboardPushed")


def clipboardReceived():
	_playCue("clipboardReceived")
