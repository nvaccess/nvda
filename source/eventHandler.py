import queueHandler
import api
import speech
import appModuleHandler
import treeInterceptorHandler
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
		log.exception("error executing event: %s on %s with extra args of %s"%(eventName,obj,kwargs))


def doPreGainFocus(obj):
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
	#Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	for parent in globalVars.focusAncestors[globalVars.focusDifferenceLevel:]:
		executeEvent("focusEntered",parent)
	if obj.treeInterceptor is not oldTreeInterceptor:
		if hasattr(oldTreeInterceptor,"event_treeInterceptor_loseFocus"):
			oldTreeInterceptor.event_treeInterceptor_loseFocus()
		if obj.treeInterceptor and not obj.treeInterceptor.isTransitioning and hasattr(obj.treeInterceptor,"event_treeInterceptor_gainFocus"):
			obj.treeInterceptor.event_treeInterceptor_gainFocus()
	return True
 
def doPreDocumentLoadComplete(obj):
	focusObject=api.getFocusObject()
	if (not obj.treeInterceptor or not obj.treeInterceptor.isAlive) and (obj==focusObject or obj in api.getFocusAncestors()):
		ti=treeInterceptorHandler.update(obj)
		if ti:
			obj.treeInterceptor=ti
			#Focus may be in this new treeInterceptor, so force focus to look up its treeInterceptor
			focusObject.treeInterceptor=treeInterceptorHandler.getTreeInterceptor(focusObject)
	return True

def executeEvent_appModuleLevel(name,obj,**kwargs):
	appModule=obj.appModule
	if appModule and appModule.selfVoicing:
		return
	if hasattr(appModule,"event_%s"%name):
		getattr(appModule,"event_%s"%name)(obj,lambda: executeEvent_treeInterceptorLevel(name,obj,**kwargs),**kwargs)
	else:
		executeEvent_treeInterceptorLevel(name,obj,**kwargs)

def executeEvent_treeInterceptorLevel(name,obj,**kwargs):
	treeInterceptor=obj.treeInterceptor
	if hasattr(treeInterceptor,'event_%s'%name) and not treeInterceptor.isTransitioning:
		getattr(treeInterceptor,'event_%s'%name)(obj,lambda: executeEvent_NVDAObjectLevel(name,obj,**kwargs),**kwargs)
	else:
		executeEvent_NVDAObjectLevel(name,obj,**kwargs)

def executeEvent_NVDAObjectLevel(name,obj,**kwargs):
	if hasattr(obj,'event_%s'%name):
		getattr(obj,'event_%s'%name)(**kwargs)
