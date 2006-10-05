#mouseHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyHook
import Queue

queue_events=Queue.Queue(1000)

#Internal mouse event

def internal_mouseEvent(event):
	if event.MessageName=="mouse move":
		queue_events.put_nowait(["mouseMove",event.Position])
	return True



#Register internal mouse event

def initialize():
	hookManager=pyHook.HookManager()
	hookManager.MouseAll=internal_mouseEvent
	hookManager.HookMouse()


