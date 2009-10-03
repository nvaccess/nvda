#tones.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities to generate and play tones"""

import nvwave
import config
import globalVars
from logHandler import log
from ctypes import create_string_buffer, byref

sampleRate=44100
player = nvwave.WavePlayer(channels=2, samplesPerSec=int(sampleRate), bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])

def beep(hz,length,left=50,right=50):
	"""Plays a tone at the given hz, length, and stereo balance.
	@param hz: pitch in hz of the tone
	@type hz: float
	@param length: length of the tone in ms
	@type length: integer
	@param left: volume of the left channel (0 to 100)
	@type left: integer
	@param right: volume of the right channel (0 to 100)
	@type right: float
	""" 
	from NVDAHelper import generateBeep
	log.io("Beep at pitch %s, for %s ms, left volume %s, right volume %s"%(hz,length,left,right))
	bufSize=generateBeep(None,hz,length,left,right)
	buf=create_string_buffer(bufSize)
	generateBeep(buf,hz,length,left,right)
	player.stop()
	player.feed(buf.raw)
