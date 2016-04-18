import appModuleHandler
from NVDAObjects.behaviors import ProgressBar
import controlTypes
import ui

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName=="msctls_progress32":
			try:
				clsList.remove(ProgressBar)
			except ValueError:
				pass
