import appModuleHandler
import virtualBuffers
import debug

def manageEvent(name,obj):
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
