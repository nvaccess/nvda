import os
from typing import Dict, Optional, TypedDict

import nvwave
import tones
import ui
from . import configuration
from .beepSequence import beepSequenceAsync, BeepSequence

local_beep = tones.beep
local_playWaveFile = nvwave.playWaveFile


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
	"control_server_connected": {
		"wave": "controlled",
		"beeps": [(720, 100), (None, 50), (720, 100), (None, 50), (720, 100)],
		# Translators: Presented in direct (client to server) remote connection when the controlled computer is ready.
		"message": _("Connected to control server"),
	},
	"client_connected": {"wave": "controlling", "beeps": [(1000, 300)]},
	"client_disconnected": {"wave": "disconnected", "beeps": [(108, 300)]},
	"clipboard_pushed": {
		"wave": "push_clipboard",
		"beeps": [(500, 100), (600, 100)],
		# Translators: Message shown when the clipboard is successfully pushed to the remote computer.
		"message": _("Clipboard pushed"),
	},
	"clipboard_received": {
		"wave": "receive_clipboard",
		"beeps": [(600, 100), (500, 100)],
		# Translators: Message shown when the clipboard is successfully received from the remote computer.
		"message": _("Clipboard received"),
	},
}


def _play_cue(cue_name: str) -> None:
	"""Helper function to play a cue by name"""
	if not should_play_sounds():
		# Play beep sequence
		if beeps := CUES[cue_name].get("beeps"):
			filtered_beeps = [(freq, dur) for freq, dur in beeps if freq is not None]
			beepSequenceAsync(*filtered_beeps)
		return

	# Play wave file
	if wave := CUES[cue_name].get("wave"):
		playSound(wave)

	# Show message if specified
	if message := CUES[cue_name].get("message"):
		ui.message(message)


def connected():
	_play_cue("connected")


def disconnected():
	_play_cue("disconnected")


def control_server_connected():
	_play_cue("control_server_connected")


def client_connected():
	_play_cue("client_connected")


def client_disconnected():
	_play_cue("client_disconnected")


def clipboard_pushed():
	_play_cue("clipboard_pushed")


def clipboard_received():
	_play_cue("clipboard_received")


def should_play_sounds():
	return configuration.get_config()["ui"]["play_sounds"]


def playSound(filename):
	path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "waves", filename))
	return local_playWaveFile(path + ".wav")
