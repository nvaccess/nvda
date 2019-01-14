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

	role = controlTypes.ROLE_DOCUMENT

class AzardiTreeViewItem(TreeViewItem):
	"""Scripts to perform common tasks for the selected book using the keyboard, so that mouse commands aren't required."""

	def script_enter(self, gesture):
		api.moveMouseToNVDAObject(self)
		api.setMouseObject(self)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP,0,0)

	def script_contextMenu(self, gesture):
		api.moveMouseToNVDAObject(self)
		api.setMouseObject(self)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN,0,0)
		mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP,0,0)

	__gestures = {
		"kb:enter": "enter",
		"kb:applications": "contextMenu",
	}

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_GROUPING or obj.role == controlTypes.ROLE_FRAME:
			clsList.insert(0, AzardiDocument)
		elif obj.role == controlTypes.ROLE_TREEVIEWITEM:
			clsList.insert(0, AzardiTreeViewItem)
