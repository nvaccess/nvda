import CoCallCancellationHandler
import queueHandler
import api
import speech
import appModuleHandler
import virtualBufferHandler
import globalVars
import controlTypes

#Some dicts to store event counts by name and or obj
_pendingEventCountsByName={}
_pendingEventCountsByObj={}
_pendingEventCountsByNameAndObj={}

def queueEvent(eventName,obj):
	"""Queues an NVDA event to be executed.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	"""
	_pendingEventCountsByName[eventName]=_pendingEventCountsByName.get(eventName,0)+1
	_pendingEventCountsByObj[obj]=_pendingEventCountsByObj.get(obj,0)+1
	_pendingEventCountsByNameAndObj[(eventName,obj)]=_pendingEventCountsByNameAndObj.get((eventName,obj),0)+1
	queueHandler.queueFunction(queueHandler.eventQueue,_queueEventCallback,eventName,obj)

def _queueEventCallback(eventName,obj):
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
	executeEvent(eventName,obj)

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

def executeEvent(eventName,obj,**kwargs):
	"""Executes an NVDA event.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	@param obj: the object the event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param kwargs: Additional event parameters as keyword arguments.
	"""
	if eventName=="gainFocus":
		doPreGainFocus(obj)
	elif eventName=="foreground":
		doPreForeground(obj)
	elif eventName=="documentLoadComplete":
		doPreDocumentLoadComplete(obj)
	executeEvent_appModuleLevel(eventName,obj,**kwargs)

def doPreGainFocus(obj):
	api.setFocusObject(obj)
	#Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	for parent in globalVars.focusAncestors[globalVars.focusDifferenceLevel:]:
		role=parent.role
		if role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_WINDOW,controlTypes.ROLE_SECTION,controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM,controlTypes.ROLE_PARAGRAPH,controlTypes.ROLE_PANE,controlTypes.ROLE_PROGRESSBAR,controlTypes.ROLE_EDITABLETEXT):
			continue
		name=parent.name
		description=parent.description
		if role in (controlTypes.ROLE_PANEL,controlTypes.ROLE_PROPERTYPAGE,controlTypes.ROLE_TABLECELL,controlTypes.ROLE_TEXTFRAME,controlTypes.ROLE_SECTION) and not name and not description:
			continue
		states=parent.states
		if controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_UNAVAILABLE in states:
			continue
		executeEvent("focusEntered",parent)
	if len(globalVars.focusAncestors)>1 and (obj.windowClassName=="SALTMPSUBFRAME" or 
(globalVars.focusAncestors[1].windowClassName=="TformMain" and 
globalVars.focusAncestors[1].name=="SpyBot - Search & Destroy") or 
globalVars.focusAncestors[1].windowClassName=="NativeHWNDHost"): 
		if not CoCallCancellationHandler.isRunning: 
			CoCallCancellationHandler.start() 
	elif CoCallCancellationHandler.isRunning:
		import wx
		wx.CallAfter(CoCallCancellationHandler.stop)

def doPreForeground(obj):
	api.setFocusObject(obj)
	speech.cancelSpeech()

def doPreDocumentLoadComplete(obj):
	focusObject=api.getFocusObject()
	if (not obj.virtualBuffer or not obj.virtualBuffer.isAlive()) and (obj==focusObject or obj in api.getFocusAncestors()):
		v=virtualBufferHandler.update(obj)
		if v:
			obj.virtualBuffer=v
			#Focus may be in this new virtualBuffer, so force focus to look up its virtualBuffer
			focusObject.virtualBuffer=virtualBufferHandler.getVirtualBuffer(focusObject)
			if focusObject.virtualBuffer==v:
				if hasattr(v,"event_virtualBuffer_firstGainFocus"):
					v.event_virtualBuffer_firstGainFocus()
				if hasattr(v,"event_virtualBuffer_gainFocus"):
					v.event_virtualBuffer_gainFocus()


def executeEvent_appModuleLevel(name,obj,**kwargs):
	appModule=obj.appModule
	if hasattr(appModule,"event_%s"%name):
		getattr(appModule,"event_%s"%name)(obj,lambda: executeEvent_virtualBufferLevel(name,obj,**kwargs),**kwargs)
	else:
		executeEvent_virtualBufferLevel(name,obj,**kwargs)

def executeEvent_virtualBufferLevel(name,obj,**kwargs):
	virtualBuffer=obj.virtualBuffer
	if hasattr(virtualBuffer,'event_%s'%name):
		getattr(virtualBuffer,'event_%s'%name)(obj,lambda: executeEvent_NVDAObjectLevel(name,obj,**kwargs),**kwargs)
	else:
		executeEvent_NVDAObjectLevel(name,obj,**kwargs)

def executeEvent_NVDAObjectLevel(name,obj,**kwargs):
	if hasattr(obj,'event_%s'%name):
		getattr(obj,'event_%s'%name)(**kwargs)
