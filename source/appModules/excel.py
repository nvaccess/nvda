# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import time
import eventHandler
import api
import UIAHandler
from NVDAObjects.UIA import UIA
import controlTypes
import appModuleHandler
from NVDAObjects.window import DisplayModelEditableText
from NVDAObjects.window.edit import UnidentifiedEdit
from NVDAObjects.window import Window
from NVDAObjects.window.excel import ExcelCell

class Excel6(Window):
	"""
	The Excel cell edit window.
	If it is not accessible (no displayModel) then wait for the CellEdit UIA element to get focus and redirect to that.
	"""

	def _get_focusRedirect(self):
		if self.role==controlTypes.ROLE_UNKNOWN:
			# The control is inaccessible, try several times to find the CellEdit UIA element with focus and use that instead.
			for count in range(10):
				if count>=1:
					api.processPendingEvents(processEventQueue=False)
					if eventHandler.isPendingEvents("gainFocus"):
						return
					time.sleep(0.05)
				e=UIAHandler.handler.lastFocusedUIAElement
				if e and e.cachedAutomationID=="CellEdit":
					obj=UIA(UIAElement=e)
					oldFocus=api.getFocusObject()
					if isinstance(oldFocus,ExcelCell):
						# Set the edit control's parent as the cell that previously had focus. I.e. the cell being edited.
						# otherwise a whole bunch of UIA focus ancestors for the edit control will be reported.
						obj.parent=oldFocus
					# Cache this for as long as this object exists.
					self.focusRedirect=obj
					return obj

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
		if windowClass=="EXCEL6":
			clsList.insert(0,Excel6)
