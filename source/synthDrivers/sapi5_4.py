#synthDrivers/sapi5.4.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2011 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from sapi5 import *

class SynthDriver(SynthDriver):
	COM_CLASS = "speech.SPVoice"

	name="sapi5_4"
	description="Microsoft Speech API version 5.4"
