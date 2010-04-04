#appModules/teamtalk4classic.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
from NVDAObjects.behaviors import ProgressBar

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		# The richedit control displaying incoming chat does not return correct _isWindowUnicode flag.
		if obj.windowClassName=="RichEdit20A":
			obj._isWindowUnicode=False

	def findExtraNVDAObjectOverlayClasses(self, obj, clsList):
		# There is a VU meter progress bar in the main window which we don't want to get anounced as all the other progress bars.
		if obj.windowClassName=="msctls_progress32" and obj.name==u'VU':
			try:
				clsList.remove(ProgressBar)
			except ValueError:
				pass
