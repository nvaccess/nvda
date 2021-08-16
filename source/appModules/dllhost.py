# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2019 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" Under older builds of Windows 10 (from RTM release to Creators Update) dllhost is used to display a properties window. 
Read-Only edit boxes in it can contain dates that include unwanted left-to-right and right-to-left indicator characters.
This simply imports a proper class from the explorer app module, and maps it to a edit control.
"""

import appModuleHandler
import controlTypes
from .explorer import ReadOnlyEditBox

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		if windowClass == "Edit" and controlTypes.State.READONLY in obj.states:
			clsList.insert(0, ReadOnlyEditBox)
