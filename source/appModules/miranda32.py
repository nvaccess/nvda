#appModules/miranda32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from keyboardHandler import key, sendKey
import audio
import IAccessibleHandler
import NVDAObjects
import appModuleHandler

class appModule(appModuleHandler.appModule):

	def __init__(self,*args):
		appModuleHandler.appModule.__init__(self,*args)
		NVDAObjects.IAccessible.registerNVDAObjectClass(self,"CListControl",IAccessibleHandler.ROLE_SYSTEM_CLIENT,NVDAObject_mirandaContactList)
		NVDAObjects.IAccessible.registerNVDAObjectClass(self,"CListControl",IAccessibleHandler.ROLE_SYSTEM_WINDOW,NVDAObject_mirandaContactList)

	def __del__(self):
		NVDAObjects.IAccessible.unregisterNVDAObjectClass(self,"CListControl",IAccessibleHandler.ROLE_SYSTEM_CLIENT)
		NVDAObjects.IAccessible.unregisterNVDAObjectClass(self,"CListControl",IAccessibleHandler.ROLE_SYSTEM_WINDOW)

class NVDAObject_mirandaContactList(NVDAObjects.IAccessible.NVDAObject_IAccessible):

	def __init__(self,*args,**vars):
		NVDAObjects.IAccessible.NVDAObject_IAccessible.__init__(self,*args,**vars)
		self.registerScriptKeys({
			key("extendedDown"):self.script_selectItem,
			key("extendedUp"):self.script_selectItem,
			key("extendedHome"):self.script_selectItem,
			key("extendedEnd"):self.script_selectItem,
		})

	def _get_typeString(self):
		return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_LIST)

	def event_gainFocus(self):
		NVDAObjects.IAccessible.NVDAObject_IAccessible.event_gainFocus(self)
		self.showActiveItemText()

	def showActiveItemText(self):
		sendKey(key("F2"))
		child=self.firstChild
		if child:
			next=child.next
			while next:
				child=next
				next=next.next
		audio.speakMessage("%s"%child.value)
		sendKey(key("Escape"))

	def script_selectItem(self,keyPress):
		sendKey(keyPress)
		self.showActiveItemText()


