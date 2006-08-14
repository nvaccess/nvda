from default import *

busyDocument=False

def event_focusObject(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if accObject is None:
		return
	className=getObjectClass(accObject)
	states=getObjectStates(accObject)
	if (className=="MozillaContentWindowClass") and (STATE_SYSTEM_BUSY not in states):
		navigator_object_recursive(accObject)
	default["event_focusObject"](window,objectID,childID)

def event_objectStateChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if accObject is None:
		return
	className=getObjectClass(accObject)
	states=getObjectStates(accObject)
	if (className=="MozillaContentWindowClass") and (STATE_SYSTEM_BUSY not in states):
		audio.speakMessage("Loading document")
	else:
		navigator_object_recursive(accObject)
	default["event_objectStateChange"](window,objectID,childID)
