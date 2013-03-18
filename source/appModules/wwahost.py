#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited

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
