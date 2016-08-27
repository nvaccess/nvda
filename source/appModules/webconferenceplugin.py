#webconferenceplugin.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 NV Access Limited, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

""" AppModule to remove redundant progressbar announcement from the web conference plugin. """
import appModuleHandler
from NVDAObjects.behaviors import ProgressBar

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName=="msctls_progress32":
			try:
				clsList.remove(ProgressBar)
			except ValueError:
				pass
