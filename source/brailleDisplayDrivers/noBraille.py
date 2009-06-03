#brailleDisplayDrivers/noBraille.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import braille

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""A dummy braille display driver used to disable braille in NVDA.
	"""
	name = "noBraille"
	description = _("No braille")

	@classmethod
	def check(cls):
		return True
