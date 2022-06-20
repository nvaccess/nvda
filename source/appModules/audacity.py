# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2019 NV Access Limited, Robert Hänggi, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import appModuleHandler
import controlTypes

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if (
			obj.windowClassName == "Button"
			and obj.role not in [controlTypes.Role.MENUBAR, controlTypes.Role.MENUITEM, controlTypes.Role.POPUPMENU]
			and obj.name is not None
		):
			obj.name=obj.name.replace('&','')
