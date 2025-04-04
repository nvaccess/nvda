# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2025 NV Access Limited, Aleksey Sadovoy, Leonard de Ruijter, Babbage B.V.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities to generate and play tones"""

import atexit
import collections
import threading
import time
from ctypes import create_string_buffer
from typing import TypeAlias
import collections.abc

import config
import extensionPoints
import nvwave
from logHandler import log

SAMPLE_RATE = 44100

player = None


def initialize():
	global player
	try:
		player = nvwave.WavePlayer(
			channels=2,
			samplesPerSec=int(SAMPLE_RATE),
			bitsPerSample=16,
			outputDevice=config.conf["audio"]["outputDevice"],
			wantDucking=False,
			purpose=nvwave.AudioPurpose.SOUNDS,
		)
	except Exception:
		log.warning("Failed to initialize audio for tones", exc_info=True)
		player = None


# When exiting, ensure player is deleted before modules get cleaned up.
# Otherwise, WavePlayer.__del__ will fail with an exception.
@atexit.register
def terminate():
	global player
	player = None


decide_beep = extensionPoints.Decider()
"""
Notifies when a beep is about to be generated and played,
and allows components or add-ons to decide whether the beep should actually be played.
For example, when controlling a remote system,
the remote system must be notified of beeps played on the local system.
Also, registrars should be able to suppress playing beeps if desired.
Handlers are called with the same arguments as L{beep} as keyword arguments.
"""


def beep(
	hz: float,
	length: int,
	left: int = 50,
	right: int = 50,
	isSpeechBeepCommand: bool = False,
):
	"""Plays a tone at the given hz, length, and stereo balance.
	@param hz: pitch in hz of the tone
	@param length: length of the tone in ms
	@param left: volume of the left channel (0 to 100)
	@param right: volume of the right channel (0 to 100)
	@param isSpeechBeepCommand: whether this beep is created as part of a speech sequence
	"""
	log.io("Beep at pitch %s, for %s ms, left volume %s, right volume %s" % (hz, length, left, right))
	if not decide_beep.decide(
		hz=hz,
		length=length,
		left=left,
		right=right,
		isSpeechBeepCommand=isSpeechBeepCommand,
	):
		log.debug(
			"Beep canceled by handler registered to decide_beep extension point",
		)
		return
	if not player:
		return
	from NVDAHelper import generateBeep

	bufSize = generateBeep(None, hz, length, left, right)
	buf = create_string_buffer(bufSize)
	generateBeep(buf, hz, length, left, right)
	player.stop()
	player.feed(buf.raw)


BeepSequenceElement: TypeAlias = int | tuple[int, int]  # Either delay_ms or (frequency_hz, duration_ms)
BeepSequence: TypeAlias = collections.abc.Iterable[BeepSequenceElement]


def beepSequence(*sequence: BeepSequenceElement) -> None:
	"""Play a simple synchronous monophonic beep sequence
	A beep sequence is an iterable containing one of two kinds of elements.
	An element consisting of a tuple of two items is interpreted as a frequency and duration. Note, this function plays beeps synchronously, unlike tones.beep
	A single integer is assumed to be a delay in ms.
	"""
	for element in sequence:
		if not isinstance(element, collections.abc.Sequence):
			time.sleep(float(element) / 1000)
		else:
			freq, duration = element
			time.sleep(float(duration) / 1000)
			beep(freq, duration)


def beepSequenceAsync(*sequence: BeepSequenceElement) -> threading.Thread:
	"""Play an asynchronous beep sequence.
	This is the same as `beepSequence`, except it runs in a thread."""
	thread = threading.Thread(target=beepSequence, args=sequence)
	thread.daemon = True
	thread.start()
	return thread
