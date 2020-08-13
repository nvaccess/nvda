# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import appModuleHandler
from NVDAObjects.window import DisplayModelEditableText
from NVDAObjects.window.edit import UnidentifiedEdit


class TSynMemo(DisplayModelEditableText):

	name = None  # Name is complete garbage as well.


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		if windowClass == "TSynMemo":
			# #8996: Edit fields in Fast Log Entry can't use UnidentifiedEdit
			# because  their WindowText contains complete garbage.
			try:
				clsList.remove(UnidentifiedEdit)
			except ValueError:
				pass
			clsList.insert(0, TSynMemo)
