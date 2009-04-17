import queueHandler
import api
import speech
import appModuleHandler
import virtualBufferHandler
import globalVars
import controlTypes
from logHandler import log

#Some dicts to store event counts by name and or obj
_pendingEventCountsByName={}
_pendingEventCountsByObj={}
_pendingEventCountsByNameAndObj={}

#: the last object queued for a gainFocus event. Useful for code running outside NVDA's core queue 
lastQueuedFocusObject=None

def queueEvent(eventName,obj,**kwargs):
	"""Queues an NVDA event to be executed.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	"""
	global lastQueuedFocusObject
	queueHandler.queueFunction(queueHandler.eventQueue,_queueEventCallback,eventName,obj,kwargs)
	if eventName=="gainFocus":
		lastQueuedFocusObject=obj
	_pendingEventCountsByName[eventName]=_pendingEventCountsByName.get(eventName,0)+1
	_pendingEventCountsByObj[obj]=_pendingEventCountsByObj.get(obj,0)+1
	_pendingEventCountsByNameAndObj[(eventName,obj)]=_pendingEventCountsByNameAndObj.get((eventName,obj),0)+1

def _queueEventCallback(eventName,obj,kwargs):
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

def executeEvent(eventName,obj,**kwargs):
	"""Executes an NVDA event.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	@param obj: the object the event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@param kwargs: Additional event parameters as keyword arguments.
	"""
	try:
		if eventName=="gainFocus" and not doPreGainFocus(obj):
			return
		elif eventName=="documentLoadComplete" and not doPreDocumentLoadComplete(obj):
			return
		executeEvent_appModuleLevel(eventName,obj,**kwargs)
	except:
		log.error("error executing event: %s on %s with extra args of %s"%(eventName,obj,kwargs),exc_info=True)


def doPreGainFocus(obj):
	oldForeground=api.getForegroundObject()
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
	#Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	for parent in globalVars.focusAncestors[globalVars.focusDifferenceLevel:]:
		executeEvent("focusEntered",parent)
	return True
 
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
	return True

def executeEvent_appModuleLevel(name,obj,**kwargs):
	appModule=obj.appModule
	if appModule and appModule.selfVoicing:
		return
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
