#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2019 NV Access Limited, Joseph Lee

"""App module host for Windows 8.x and 10 web apps hosted by wwahost.exe.
In Windows 8, apps written in Javascript are executed inside WWAHost, including some WinRT apps.
In Windows 10, progressive web apps (PWA) and friends are hosted inside this process.
App modules wishing to support apps hosted inside this process must import contents of this app module.
"""

from comtypes import COMError
import IAccessibleHandler
from NVDAObjects.IAccessible.MSHTML import Body
import appModuleHandler
import controlTypes
import winUser

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		#The root document of HTML Metro Apps must be treeted as an application. 
		if isinstance(obj,Body) and obj.windowClassName=="Internet Explorer_Server":
			try:
				paccParent=obj.IAccessibleObject.accParent.accParent
				identity=IAccessibleHandler.getIAccIdentity(paccParent,0)
			except (COMError,AttributeError):
				identity=None
			if identity:
				windowHandle=identity.get('windowHandle')
				if windowHandle and winUser.getClassName(windowHandle)=="Web Platform Embedding":
					obj.role=controlTypes.ROLE_APPLICATION
