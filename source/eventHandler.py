import appModuleHandler
import globalVars
import virtualBuffers
import controlTypes

def manageEvent(eventName,obj):
	#Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	if eventName=="gainFocus":
		for parent in globalVars.focusAncestors[globalVars.focusDifferenceLevel:]:
			role=parent.role
			if role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_WINDOW,controlTypes.ROLE_SECTION,controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM,controlTypes.ROLE_PARAGRAPH,controlTypes.ROLE_PANE,controlTypes.ROLE_PROGRESSBAR,controlTypes.ROLE_EDITABLETEXT):
				continue
			name=parent.name
			description=parent.description
			if role==controlTypes.ROLE_PANEL and not name and not description:
				continue
			states=parent.states
			if controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_UNAVAILABLE in states:
				continue
			manageEvent("focusEntered",parent)
	manageEvent_appModuleLevel(eventName,obj)

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
