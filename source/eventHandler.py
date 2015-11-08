#eventHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2014 NV Access Limited

import threading
import queueHandler
import api
import speech
import appModuleHandler
import treeInterceptorHandler
import globalVars
import controlTypes
from logHandler import log
import globalPluginHandler
import config
import winUser

#Some dicts to store event counts by name and or obj
_pendingEventCountsByName={}
_pendingEventCountsByObj={}
_pendingEventCountsByNameAndObj={}
# Needed to ensure updates are atomic, as these might be updated from multiple threads simultaneously.
_pendingEventCountsLock=threading.RLock()

#: the last object queued for a gainFocus event. Useful for code running outside NVDA's core queue 
lastQueuedFocusObject=None

def queueEvent(eventName,obj,**kwargs):
	"""Queues an NVDA event to be executed.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	"""
	global lastQueuedFocusObject
	if eventName=="gainFocus":
		lastQueuedFocusObject=obj
	with _pendingEventCountsLock:
		_pendingEventCountsByName[eventName]=_pendingEventCountsByName.get(eventName,0)+1
		_pendingEventCountsByObj[obj]=_pendingEventCountsByObj.get(obj,0)+1
		_pendingEventCountsByNameAndObj[(eventName,obj)]=_pendingEventCountsByNameAndObj.get((eventName,obj),0)+1
	queueHandler.queueFunction(queueHandler.eventQueue,_queueEventCallback,eventName,obj,kwargs)

def _queueEventCallback(eventName,obj,kwargs):
	with _pendingEventCountsLock:
		curCount=_pendingEventCountsByName.get(eventName,0)
		if curCount>1:
			_pendingEventCountsByName[eventName]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByName[eventName]
		curCount=_pendingEventCountsByObj.get(obj,0)
		if curCount>1:
			_pendingEventCountsByObj[obj]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByObj[obj]
		curCount=_pendingEventCountsByNameAndObj.get((eventName,obj),0)
		if curCount>1:
			_pendingEventCountsByNameAndObj[(eventName,obj)]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByNameAndObj[(eventName,obj)]
	executeEvent(eventName,obj,**kwargs)

def isPendingEvents(eventName=None,obj=None):
	"""Are there currently any events queued?
	@param eventName: an optional name of an event type. If given then only if there are events of this type queued will it return True.
	@type eventName: string
	@param obj: the NVDAObject the event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@returns: True if there are events queued, False otherwise.
	@rtype: boolean
	"""
	if not eventName and not obj:
		return bool(len(_pendingEventCountsByName))
	elif not eventName and obj:
		return obj in _pendingEventCountsByObj
	elif eventName and not obj:
		return eventName in _pendingEventCountsByName
	elif eventName and obj:
		return (eventName,obj) in _pendingEventCountsByNameAndObj

class _EventExecuter(object):
	"""Facilitates execution of a chain of event functions.
	L{gen} generates the event functions and positional arguments.
	L{next} calls the next function in the chain.
	"""

	def __init__(self, eventName, obj, kwargs):
		self.kwargs = kwargs
		self._gen = self.gen(eventName, obj)
		try:
			self.next()
		except StopIteration:
			pass
		del self._gen

	def next(self):
		func, args = next(self._gen)
		return func(*args, **self.kwargs)

	def gen(self, eventName, obj):
		funcName = "event_%s" % eventName

		# Global plugin level.
		for plugin in globalPluginHandler.runningPlugins:
			func = getattr(plugin, funcName, None)
			if func:
				yield func, (obj, self.next)

		# App module level.
		app = obj.appModule
		if app:
			func = getattr(app, funcName, None)
			if func:
				yield func, (obj, self.next)

		# Tree interceptor level.
		treeInterceptor = obj.treeInterceptor
		if treeInterceptor:
			func = getattr(treeInterceptor, funcName, None)
			if func and (getattr(func,'ignoreIsReady',False) or treeInterceptor.isReady):
				yield func, (obj, self.next)

		# NVDAObject level.
		func = getattr(obj, funcName, None)
		if func:
			yield func, ()

def executeEvent(eventName,obj,**kwargs):
	"""Executes an NVDA event.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	@param obj: the object the event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param kwargs: Additional event parameters as keyword arguments.
	"""
	try:
		sleepMode=obj.sleepMode
		if eventName=="gainFocus" and not doPreGainFocus(obj,sleepMode=sleepMode):
			return
		elif not sleepMode and eventName=="documentLoadComplete" and not doPreDocumentLoadComplete(obj):
			return
		elif not sleepMode:
			_EventExecuter(eventName,obj,kwargs)
	except:
		log.exception("error executing event: %s on %s with extra args of %s"%(eventName,obj,kwargs))

def doPreGainFocus(obj,sleepMode=False):
	oldForeground=api.getForegroundObject()
	oldFocus=api.getFocusObject()
	oldTreeInterceptor=oldFocus.treeInterceptor if oldFocus else None
	api.setFocusObject(obj)
	if globalVars.focusDifferenceLevel<=1:
		newForeground=api.getDesktopObject().objectInForeground()
		if not newForeground:
			log.debugWarning("Can not get real foreground, resorting to focus ancestors")
			ancestors=api.getFocusAncestors()
			if len(ancestors)>1:
				newForeground=ancestors[1]
			else:
				newForeground=obj
		api.setForegroundObject(newForeground)
		executeEvent('foreground',newForeground)
	if sleepMode: return True
	#Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	for parent in globalVars.focusAncestors[globalVars.focusDifferenceLevel:]:
		executeEvent("focusEntered",parent)
	if obj.treeInterceptor is not oldTreeInterceptor:
		if hasattr(oldTreeInterceptor,"event_treeInterceptor_loseFocus"):
			oldTreeInterceptor.event_treeInterceptor_loseFocus()
		if obj.treeInterceptor and obj.treeInterceptor.isReady and hasattr(obj.treeInterceptor,"event_treeInterceptor_gainFocus"):
			obj.treeInterceptor.event_treeInterceptor_gainFocus()
	return True
 
def doPreDocumentLoadComplete(obj):
	focusObject=api.getFocusObject()
	if (not obj.treeInterceptor or not obj.treeInterceptor.isAlive or obj.treeInterceptor.shouldPrepare) and (obj==focusObject or obj in api.getFocusAncestors()):
		ti=treeInterceptorHandler.update(obj)
		if ti:
			obj.treeInterceptor=ti
			#Focus may be in this new treeInterceptor, so force focus to look up its treeInterceptor
			focusObject.treeInterceptor=treeInterceptorHandler.getTreeInterceptor(focusObject)
	return True

#: set of (eventName, processId, windowClassName) of events to accept.
_acceptEvents = set()
#: Maps process IDs to sets of events so they can be cleaned up when the process exits.
_acceptEventsByProcess = {}

def requestEvents(eventName=None, processId=None, windowClassName=None):
	"""Request that particular events be accepted from a platform API.
	Normally, L{shouldAcceptEvent} rejects certain events, including
	most show events, events indicating changes in background processes, etc.
	This function allows plugins to override this for specific cases;
	e.g. to receive show events from a specific control or
	to receive certain events even when in the background.
	Note that NVDA may block some events at a lower level and doesn't listen for some event types at all.
	In these cases, you will not be able to override this.
	This should generally be called when a plugin is instantiated.
	All arguments must be provided.
	"""
	if not eventName or not processId or not windowClassName:
		raise ValueError("eventName, processId or windowClassName not specified")
	entry = (eventName, processId, windowClassName)
	procEvents = _acceptEventsByProcess.get(processId)
	if not procEvents:
		procEvents = _acceptEventsByProcess[processId] = set()
	procEvents.add(entry)
	_acceptEvents.add(entry)

def handleAppTerminate(appModule):
	global _acceptEvents
	events = _acceptEventsByProcess.pop(appModule.processID, None)
	if not events:
		return
	_acceptEvents -= events

def shouldAcceptEvent(eventName, windowHandle=None):
	"""Check whether an event should be accepted from a platform API.
	Creating NVDAObjects and executing events can be expensive
	and might block the main thread noticeably if the object is slow to respond.
	Therefore, this should be used before NVDAObject creation to filter out any unnecessary events.
	A platform API handler may do its own filtering before this.
	"""
	if not windowHandle:
		# We can't filter without a window handle.
		return True
	key = (eventName,
		winUser.getWindowThreadProcessID(windowHandle)[0],
		winUser.getClassName(windowHandle))
	if key in _acceptEvents:
		return True
	if eventName == "valueChange" and config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"]:
		return True
	if eventName == "show":
		# Only accept 'show' events for specific cases, as otherwise we get flooded.
		return winUser.getClassName(windowHandle) in (
			"Frame Notification Bar", # notification bars
			"tooltips_class32", # tooltips
			"mscandui21.candidate", "mscandui40.candidate", "MSCandUIWindow_Candidate", # IMM candidates
			"TTrayAlert", # 5405: Skype
		)
	if eventName == "reorder":
		# Prevent another flood risk.
		return winUser.getClassName(windowHandle) == "TTrayAlert" # #4841: Skype
	if eventName == "alert" and winUser.getClassName(winUser.getAncestor(windowHandle, winUser.GA_PARENT)) == "ToastChildWindowClass":
		# Toast notifications.
		return True
	if eventName in ("menuEnd", "switchEnd", "desktopSwitch"):
		# #5302, #5462: These events can be fired on the desktop window
		# or windows that would otherwise be blocked.
		# Platform API handlers will translate these events to focus events anyway,
		# so we must allow them here.
		return True

	fg = winUser.getForegroundWindow()
	if (winUser.isDescendantWindow(fg, windowHandle)
			# #3899, #3905: Covers cases such as the Firefox Page Bookmarked window and OpenOffice/LibreOffice context menus.
			or winUser.isDescendantWindow(fg, winUser.getAncestor(windowHandle, winUser.GA_ROOTOWNER))):
		# This is for the foreground application.
		return True
	if (winUser.user32.GetWindowLongW(windowHandle, winUser.GWL_EXSTYLE) & winUser.WS_EX_TOPMOST
			or winUser.user32.GetWindowLongW(winUser.getAncestor(windowHandle, winUser.GA_ROOT), winUser.GWL_EXSTYLE) & winUser.WS_EX_TOPMOST):
		# This window or its root is a topmost window.
		# This includes menus, combo box pop-ups and the task switching list.
		return True
	return False
