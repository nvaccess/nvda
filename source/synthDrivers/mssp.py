#synthDrivers/mssp.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2011 NV Access Inc
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from .sapi5 import SynthDriver

class SynthDriver(SynthDriver):
	COM_CLASS = "speech.SPVoice"

	name="mssp"
	description="Microsoft Speech Platform"
