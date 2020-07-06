#appModules/zoom.py:
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2018 NV Access Limited,Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import eventHandler

class AppModule(appModuleHandler.AppModule):
	def __init__(self,*args,**kwargs):
		super(AppModule,self).__init__(*args,**kwargs)
		#Explicetly allow alert events for zoom's chat windows.
		#Zoom alerts are not  zoom foreground window descendants.
		eventHandler.requestEvents("alert",processId=self.processID,windowClassName="zoom_acc_notify_wnd")
