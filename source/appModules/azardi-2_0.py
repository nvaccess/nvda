# -*- coding: UTF-8 -*-
#appModules/azardi-2_0.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016-2017 NV Access Limited, Noelia Ruiz Martínez
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import winUser
import mouseHandler
import api
from NVDAObjects.IAccessible.mozilla import Document
from NVDAObjects.IAccessible.sysTreeView32 import TreeViewItem

class AzardiDocument(Document):

	role = controlTypes.Role.DOCUMENT

class AzardiTreeViewItem(TreeViewItem):
	"""Scripts to perform common tasks for the selected book using the keyboard, so that mouse commands aren't required."""

	def script_enter(self, gesture):
		api.moveMouseToNVDAObject(self)
		api.setMouseObject(self)
		mouseHandler.doPrimaryClick()
		mouseHandler.doPrimaryClick()

	def script_contextMenu(self, gesture):
		api.moveMouseToNVDAObject(self)
		api.setMouseObject(self)
		mouseHandler.doSecondaryClick()

	__gestures = {
		"kb:enter": "enter",
		"kb:applications": "contextMenu",
	}

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.Role.GROUPING or obj.role == controlTypes.Role.FRAME:
			clsList.insert(0, AzardiDocument)
		elif obj.role == controlTypes.Role.TREEVIEWITEM:
			clsList.insert(0, AzardiTreeViewItem)
