#synthDrivers/silence.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import synthDriverHandler

class SynthDriver(synthDriverHandler.SynthDriver):
	"""A dummy synth driver used to disable speech in NVDA.
	"""
	name="silence"
	description=_("No speech")

	@classmethod
	def check(cls):
		return True
