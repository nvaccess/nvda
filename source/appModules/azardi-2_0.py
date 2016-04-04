# -*- coding: UTF-8 -*-
#appModules/azardi-2_0.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 Noelia Ruiz Martínez
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import winUser
import api
from NVDAObjects.IAccessible.mozilla import Document
from NVDAObjects.IAccessible.sysTreeView32 import TreeViewItem

class AzardiDocument(Document):

	role = controlTypes.ROLE_DOCUMENT

class AzardiTreeViewItem(TreeViewItem):

	def script_enter(self, gesture):
		api.moveMouseToNVDAObject(self)
		api.setMouseObject(self)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)

	def script_contextMenu(self, gesture):
		api.moveMouseToNVDAObject(self)
		api.setMouseObject(self)
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_RIGHTUP,0,0,None,None)

	__gestures = {
		"kb:enter": "enter",
		"kb:applications": "contextMenu",
	}

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_GROUPING:
			clsList.insert(0, AzardiDocument)
		elif obj.role == controlTypes.ROLE_TREEVIEWITEM:
			clsList.insert(0, AzardiTreeViewItem)
