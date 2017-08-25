#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2017 NV Access Limited, Aleksey Sadovoy, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities to generate and play tones"""

import atexit
import nvwave
import config
import globalVars
from logHandler import log
from ctypes import create_string_buffer, byref
import extensionPoints

SAMPLE_RATE = 44100

try:
	player = nvwave.WavePlayer(channels=2, samplesPerSec=int(SAMPLE_RATE), bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"],wantDucking=False)
except:
	log.warning("Failed to initialize audio for tones", exc_info=True)
	player = None

# When exiting, ensure player is deleted before modules get cleaned up.
# Otherwise, WavePlayer.__del__ will fail with an exception.
@atexit.register
def _cleanup():
	global player
	player = None

#: Notifies when a beep is about to be generated and played,
#: and allows components or add-ons to decide whether the beep should actually be played.
#: For example, when controlling a remote system,
#: the remote system must be notified of beeps played on the local system.
#: Also, registrars should be able to suppress playing beeps if desired.
#: Handlers are called with the same arguments as L{beep} as keyword arguments.
decide_beep = extensionPoints.Decider()

def beep(hz,length,left=50,right=50,partOfSpeechSequence=False):
	"""Plays a tone at the given hz, length, and stereo balance.
	@param hz: pitch in hz of the tone.
	@type hz: float
	@param length: length of the tone in ms.
	@type length: integer
	@param left: volume of the left channel (0 to 100).
	@type left: integer
	@param right: volume of the right channel (0 to 100).
	@type right: integer
	@param partOfSpeechSequence: whether this beep is created as part of a speech sequence.
	@type partOfSpeechSequence: bool
	""" 
	log.io("Beep at pitch %s, for %s ms, left volume %s, right volume %s"%(hz,length,left,right))
	if not decide_beep.decide(hz=hz, length=length, left=left, right=right, partOfSpeechSequence=partOfSpeechSequence):
		log.debug("Beep canceled by handler registered to decide_beep extension point")
		return
	if not player:
		return
	from NVDAHelper import generateBeep
	bufSize=generateBeep(None,hz,length,left,right)
	buf=create_string_buffer(bufSize)
	generateBeep(buf,hz,length,left,right)
	player.stop()
	player.feed(buf.raw)
