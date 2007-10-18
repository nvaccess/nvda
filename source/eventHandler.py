import appModuleHandler
import globalVars
import virtualBuffers
import debug
import controlTypes

def manageEvent(name,obj):
	#Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	foregroundObject=globalVars.foregroundObject
	if name=="gainFocus":
		for parent in globalVars.focusAncestors[globalVars.focusDifferenceLevel:]:
			if parent==foregroundObject:
				continue
			states=parent.states
			role=parent.role
			if role not in (controlTypes.ROLE_WINDOW,controlTypes.ROLE_PANE,controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM,controlTypes.ROLE_PARAGRAPH,controlTypes.ROLE_SECTION) and (controlTypes.STATE_UNAVAILABLE not in states) and (controlTypes.STATE_INVISIBLE not in states):
				manageEvent("focusEntered",parent)
	manageEvent_appModuleLevel(name,obj)

def manageEvent_appModuleLevel(name,obj):
	appModule=obj.appModule()
	if hasattr(appModule,"event_%s"%name):
		getattr(appModule,"event_%s"%name)(obj,lambda: manageEvent_defaultAppModuleLevel(name,obj)) 
	else:
		manageEvent_defaultAppModuleLevel(name,obj)

def manageEvent_defaultAppModuleLevel(name,obj):
	default=appModuleHandler.default
	if hasattr(default,"event_%s"%name):
		getattr(default,"event_%s"%name)(obj,lambda: manageEvent_virtualBufferLevel(name,obj)) 
	else:
		manageEvent_virtualBufferLevel(name,obj)

def manageEvent_virtualBufferLevel(name,obj):
	virtualBuffer=obj.virtualBuffer()
	if hasattr(virtualBuffer,'event_%s'%name):
		getattr(virtualBuffer,'event_%s'%name)(obj,lambda: manageEvent_NVDAObjectLevel(name,obj))
	else:
		manageEvent_NVDAObjectLevel(name,obj)

def manageEvent_NVDAObjectLevel(name,obj):
	if hasattr(obj,'event_%s'%name):
		getattr(obj,'event_%s'%name)()
