# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import appModuleHandler
from NVDAObjects.window import DisplayModelEditableText
from NVDAObjects.window.edit import UnidentifiedEdit

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		# #9042: Edit fields in Excel have to be accessed via displayModel.
		if windowClass == "EDTBX":
			try:
				clsList.remove(UnidentifiedEdit)
			except ValueError:
				pass
			clsList.insert(0, DisplayModelEditableText)
