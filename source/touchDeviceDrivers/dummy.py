#touchDeviceDrivers/dummy.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 Aleksey Sadovoy <lex@progger.ru>

import touchReview

class TouchDeviceDriver(touchReview.TouchDeviceDriver):
	"""A dummy driver which does nothing."""
	name="dummy"

	@classmethod
	def check(cls):
		return True
