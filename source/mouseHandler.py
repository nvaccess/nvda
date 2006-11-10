#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyHook
import NVDAThreads
import api

#Internal mouse event

def internal_mouseEvent(event):
	try:
		if event.MessageName=="mouse move":
			NVDAThreads.executeFunction(api.notifyMouseMoved,event.Position[0],event.Position[1])
		return True
	except:
		debug.writeException("mouseHandler.internal_mouseEvent")

#Register internal mouse event

def initialize():
	hookManager=pyHook.HookManager()
	hookManager.MouseAll=internal_mouseEvent
	hookManager.HookMouse()
