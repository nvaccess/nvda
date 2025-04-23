# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
from typing import Dict, Optional, TypedDict

import globalVars
import nvwave
import ui
from tones import BeepSequence, beepSequenceAsync

from . import configuration


class Cue(TypedDict, total=False):
	wave: Optional[str]
	beeps: Optional[BeepSequence]
	message: Optional[str]


# Declarative dictionary of all possible cues
CUES: Dict[str, Cue] = {
	"connected": {"wave": "connected", "beeps": [(440, 60), (660, 60)]},
	"disconnected": {
		"wave": "disconnected",
		"beeps": [(660, 60), (440, 60)],
		# Translators: Message shown when the connection to the remote computer is lost.
		"message": _("Disconnected"),
	},
	"controlServerConnected": {
		"wave": "controlled",
		"beeps": [(720, 100), (None, 50), (720, 100), (None, 50), (720, 100)],
		# Translators: Presented in direct (client to server) remote connection when the controlled computer is ready.
		"message": pgettext("remote", "Connected as controlled computer"),
	},
	"clientConnected": {"wave": "controlling", "beeps": [(1000, 300)]},
	"clientDisconnected": {"wave": "disconnected", "beeps": [(108, 300)]},
	"clipboardPushed": {
		"wave": "clipboardPush",
		"beeps": [(500, 100), (600, 100)],
		# Translators: Message shown when the clipboard is successfully sent to the remote computer.
		"message": _("Clipboard sent"),
	},
	"clipboardReceived": {
		"wave": "clipboardReceive",
		"beeps": [(600, 100), (500, 100)],
		# Translators: Message shown when the clipboard is successfully received from the remote computer.
		"message": _("Clipboard received"),
	},
}


def _playCue(cueName: str) -> None:
	"""Helper function to play a cue by name"""
	if shouldPlaySounds():
		# Play wave file
		if wave := CUES[cueName].get("wave"):
			nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", wave + ".wav"))
	elif beeps := CUES[cueName].get("beeps"):
		# Play beep sequence
		filteredBeeps = [(freq, dur) for freq, dur in beeps if freq is not None]
		beepSequenceAsync(*filteredBeeps)

	# Show message if specified
	if message := CUES[cueName].get("message"):
		ui.message(message)


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


def shouldPlaySounds() -> bool:
	return configuration.getRemoteConfig()["ui"]["playSounds"]
