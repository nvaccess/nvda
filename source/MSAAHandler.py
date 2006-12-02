#MSAAHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import ctypes
import comtypesClient
import comtypes.automation
import debug
import winUser
import audio
from constants import *
import api
import core
import virtualBuffers
import NVDAObjects
import globalVars
import appModuleHandler
from config import conf

#A list to store handles received from setWinEventHook, for use with unHookWinEvent  
objectEventHandles=[]

#Load IAccessible from oleacc.dll
IAccessible=comtypesClient.GetModule('oleacc.dll').IAccessible

def getRoleName(role):
	if isinstance(role,int):
		return getRoleText(role)
	else:
		return role

def createStateList(stateBits):
	stateList=[]
	for bitPos in range(32):
		bitVal=1<<bitPos
		if stateBits&bitVal:
			stateList+=[bitVal]
	return stateList

def getStateNames(states,opposite=False):
	str=""
	for state in createStateList(states):
		str="%s %s"%(str,getStateName(state,opposite=opposite))
	return str

def getStateName(state,opposite=False):
	if isinstance(state,int):
		newState=getStateText(state)
	else:
		newState=state
	if opposite:
		newState=_("not")+" "+newState
	return newState

#A c ctypes struct to hold the x and y of a point on the screen 
class screenPointType(ctypes.Structure):
	_fields_=[
	('x',ctypes.c_int),
	('y',ctypes.c_int)
	]

def accessibleObjectFromWindow(window,objectID):
	if not winUser.isWindow(window):
		return None
	ptr=ctypes.POINTER(IAccessible)()
	res=ctypes.windll.oleacc.AccessibleObjectFromWindow(window,objectID,ctypes.byref(IAccessible._iid_),ctypes.byref(ptr))
	if res==0:
		return ptr
	else:
		return None

def accessibleObjectFromEvent(window,objectID,childID):
	if not winUser.isWindow(window):
		return None
	pacc=ctypes.POINTER(IAccessible)()
	varChild=comtypes.automation.VARIANT()
	res=ctypes.windll.oleacc.AccessibleObjectFromEvent(window,objectID,childID,ctypes.byref(pacc),ctypes.byref(varChild))
	if res==0:
		if not isinstance(varChild.value,int):
			child=0
		else:
			child=varChild.value
		return (pacc,child)
	else:
		return None

def accessibleObjectFromPoint(x,y):
	point=screenPointType(x,y)
	pacc=ctypes.POINTER(IAccessible)()
	varChild=comtypes.automation.VARIANT()
	res=ctypes.windll.oleacc.AccessibleObjectFromPoint(point,ctypes.byref(pacc),ctypes.byref(varChild))
	if res==0:
		if not isinstance(varChild.value,int):
			child=0
		else:
			child=varChild.value
		return (pacc,child)

def windowFromAccessibleObject(ia):
	hwnd=ctypes.c_int()
	try:
		res=ctypes.windll.oleacc.WindowFromAccessibleObject(ia,ctypes.byref(hwnd))
	except:
		res=0
	if res==0:
		return hwnd.value
	else:
		return 0

def getRoleText(role):
	len=ctypes.windll.oleacc.GetRoleTextW(role,0,0)
	if len:
		buf=ctypes.create_unicode_buffer(len+2)
		ctypes.windll.oleacc.GetRoleTextW(role,buf,len+1)
		return buf.value
	else:
		return None

def getStateText(state):
	len=ctypes.windll.oleacc.GetStateTextW(state,0,0)
	if len:
		buf=ctypes.create_unicode_buffer(len+2)
		ctypes.windll.oleacc.GetStateTextW(state,buf,len+1)
		return buf.value
	else:
		return None

def accName(ia,child):
	try:
		return ia.accName(child)
	except:
		return ""

def accValue(ia,child):
	try:
		return ia.accValue(child)
	except:
		return ""

def accRole(ia,child):
	try:
		return ia.accRole(child)
	except:
		return 0

def accState(ia,child):
	try:
		return ia.accState(child)
	except:
		return 0

def accDescription(ia,child):
	try:
		return ia.accDescription(child)
	except:
		return ""

def accHelp(ia,child):
	try:
		return ia.accHelp(child)
	except:
		return ""

def accKeyboardShortcut(ia,child):
	try:
		return ia.accKeyboardShortcut(child)
	except:
		return ""

def accDoDefaultAction(ia,child):
	try:
		ia.accDoDefaultAction(child)
	except:
		pass

def accFocus(ia):
	try:
		res=ia.accFocus
		if isinstance(res,ctypes.POINTER(IAccessible)):
			new_ia=res
			new_child=0
		elif isinstance(res,comtypesClient._Dispatch):
			new_ia=res.QueryInterface(IAccessible)
			new_child=0
		elif isinstance(res,int):
			new_ia=ia
			new_child=res
		else:
			return None
		return (new_ia,new_child)
	except:
		return None

def accChild(ia,child):
	try:
		res=ia.accChild(child)
		if isinstance(res,ctypes.POINTER(IAccessible)):
			new_ia=res
			new_child=0
		elif isinstance(res,comtypesClient._Dispatch):
			new_ia=res.QueryInterface(IAccessible)
			new_child=0
		elif isinstance(res,int):
			new_ia=ia
			new_child=res
		return (new_ia,new_child)
	except:
		return None

def accChildCount(ia,child):
	if child==0:
		count=ia.accChildCount
	else:
		count=0
	return count

def accParent(ia,child):
	try:
		if not child:
			res=ia.accParent
			if isinstance(res,ctypes.POINTER(IAccessible)):
				new_ia=res
				new_child=0
			elif isinstance(res,comtypesClient._Dispatch):
				new_ia=res.QueryInterface(IAccessible)
				new_child=0
			elif isinstance(res,int): 
				new_ia=ia
				new_child=res
		else:
			new_ia=ia
			new_child=0
		return (new_ia,new_child)
	except:
		return None

def accNavigate(ia,child,direction):
	try:
		res=ia.accNavigate(direction,child)
		if isinstance(res,ctypes.POINTER(IAccessible)):
			new_ia=res
			new_child=0
		elif isinstance(res,int):
			new_ia=ia
			new_child=res
		elif isinstance(res,comtypesClient._Dispatch):
			new_ia=res.QueryInterface(IAccessible)
			new_child=0
		else:
			return None
		return (new_ia,new_child)
	except:
		return None

def accLocation(ia,child):
	try:
		return ia.accLocation(child)
	except:
		return None

eventMap={
EVENT_SYSTEM_FOREGROUND:"foreground",
EVENT_SYSTEM_MENUSTART:"menuStart",
EVENT_SYSTEM_MENUEND:"menuEnd",
EVENT_SYSTEM_MENUPOPUPSTART:"menuStart",
EVENT_SYSTEM_MENUPOPUPEND:"menuEnd",
EVENT_SYSTEM_SWITCHSTART:"switchStart",
EVENT_SYSTEM_SWITCHEND:"switchEnd",
EVENT_OBJECT_FOCUS:"gainFocus",
EVENT_OBJECT_SHOW:"show",
EVENT_OBJECT_HIDE:"hide",
EVENT_OBJECT_DESCRIPTIONCHANGE:"descriptionChange",
EVENT_OBJECT_HELPCHANGE:"helpChange",
EVENT_OBJECT_LOCATIONCHANGE:"locationChange",
EVENT_OBJECT_NAMECHANGE:"nameChange",
EVENT_OBJECT_REORDER:"reorder",
EVENT_OBJECT_SELECTION:"selection",
EVENT_OBJECT_SELECTIONADD:"selectionAdd",
EVENT_OBJECT_SELECTIONREMOVE:"selectionRemove",
EVENT_OBJECT_SELECTIONWITHIN:"selectionWithIn",
EVENT_OBJECT_STATECHANGE:"stateChange",
EVENT_OBJECT_VALUECHANGE:"valueChange"
}

#Internal function for object events

def objectEventCallback(handle,eventID,window,objectID,childID,threadID,timestamp):
	try:
		eventName=eventMap[eventID]
		if objectID==0:
			objectID=OBJID_CLIENT
		#Let tooltips through
		if (eventID==EVENT_OBJECT_SHOW) and (winUser.getClassName(window)=="tooltips_class32"):
			core.executeFunction(EXEC_USERINTERFACE,executeEvent,"toolTip",window,objectID,childID)
		#Let caret events through
		elif (eventID in [EVENT_OBJECT_LOCATIONCHANGE,EVENT_OBJECT_FOCUS]) and (objectID==OBJID_CARET):
			core.executeFunction(EXEC_USERINTERFACE,executeEvent,"caret",window,objectID,childID)
		#Let menu events through
		elif eventID in [EVENT_SYSTEM_MENUSTART,EVENT_SYSTEM_MENUEND,EVENT_SYSTEM_MENUPOPUPSTART,EVENT_SYSTEM_MENUPOPUPEND]:
			core.executeFunction(EXEC_USERINTERFACE,executeEvent,eventName,window,objectID,childID)
		#Let foreground and focus events through
		elif (eventID==EVENT_SYSTEM_FOREGROUND) or (eventID==EVENT_OBJECT_FOCUS):
			core.executeFunction(EXEC_USERINTERFACE,executeEvent,eventName,window,objectID,childID)
		#Let events for the focus object through
		elif isinstance(api.getFocusObject(),NVDAObjects.MSAA.NVDAObject_MSAA) and (window,objectID,childID)==api.getFocusObject().MSAAOrigEventLocator:
			core.executeFunction(EXEC_USERINTERFACE,executeEvent,eventName,window,objectID,childID)
	except:
		debug.writeException("objectEventCallback")

def executeEvent(name,window,objectID,childID):
	obj=NVDAObjects.MSAA.getNVDAObjectFromEvent(window,objectID,childID)
	#If foreground event, see if we should change appModules, and also update the foreground global variables
	if name=="foreground":
		audio.cancel()
		processID=winUser.getWindowThreadProcessID(window)
		if processID!=globalVars.foregroundProcessID:
			appName=api.getAppName(processID)
			appModuleHandler.load(appName,window,processID)
			globalVars.foregroundProcessID=processID
		api.setForegroundObject(obj)
		virtualBuffers.MSAA.updateVirtualBuffers(obj)
	#If focus event then update the focus global variables
	if (name=="gainFocus"):
		#If this event is the same as the current focus object, just return, we don't need to set focus or use the event, its bad
		if isinstance(api.getFocusObject(),NVDAObjects.MSAA.NVDAObject_MSAA) and ((window,objectID,childID)==api.getFocusObject().MSAAOrigEventLocator): 
			return
		api.setFocusObject(obj)
		virtualBuffers.MSAA.updateVirtualBuffers(obj)
	#If this event is for the same window as a virtualBuffer, then give it to the virtualBuffer and then continue
	virtualBuffer=virtualBuffers.getVirtualBuffer(obj)
	if virtualBuffer and hasattr(virtualBuffer,"event_MSAA_%s"%name):
		event=getattr(virtualBuffer,"event_MSAA_%s"%name)
		try:
			event(window,objectID,childID)
		except:
			debug.writeException("virtualBuffer event")
	#If this is a hide event and it it is specifically for a window and there is a virtualBuffer for this window, remove the virtualBuffer 
	#and then continue 
	if (name=="hide") and (objectID==0): 
		virtualBuffers.removeVirtualBuffer(window)
	#This event is either for the current appModule if the appModule has an event handler,
	#the foregroundObject if its a foreground event and the foreground object handles this event,
	#the focus object if the focus object has a handler for this event,
	#the specific object that this event describes if the object has a handler for this event.
	if hasattr(appModuleHandler.current,"event_%s"%name):
		event=getattr(appModuleHandler.current,"event_%s"%name)
		try:
			event(window,objectID,childID)
		except:
			debug.writeException("Error executing event %s from appModule"%event.__name__)
		return
	if (name=="foreground") and (api.getForegroundObject()==obj) and hasattr(api.getForegroundObject(),"event_%s"%name):
		try:
			getattr(api.getForegroundObject(),"event_%s"%name)()
		except:
			debug.writeException("foregroundObject: event_%s"%name)
		return
	if ((isinstance(api.getFocusObject(),NVDAObjects.MSAA.NVDAObject_MSAA) and ((window,objectID,childID)==api.getFocusObject().MSAAOrigEventLocator)) or (name=="caret")) and hasattr(api.getFocusObject(),"event_%s"%name):
		try:
			getattr(api.getFocusObject(),"event_%s"%name)()
		except:
			debug.writeException("Error executing event event_%s from focusObject"%name)
		return
	if obj and hasattr(obj,"event_%s"%name):
		try:
			getattr(obj,"event_%s"%name)()
		except:
			debug.writeException("Error executing event event_%s from object"%name)
		return

#Register internal object event with MSAA
cObjectEventCallback=ctypes.CFUNCTYPE(ctypes.c_voidp,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int)(objectEventCallback)

def initialize():
	for eventType in eventMap.keys():
		handle=winUser.setWinEventHook(eventType,eventType,0,cObjectEventCallback,0,0,0)
		if handle:
			objectEventHandles.append(handle)
			debug.writeMessage("Initialize: registered 0x%x (%s) as handle %s"%(eventType,eventMap[eventType],handle))
		else:
			debug.writeError("initialize: could not register callback for event %s (%s)"%(eventType,eventMap[eventType]))

def terminate():
	for handle in objectEventHandles:
		winUser.unhookWinEvent(handle)
