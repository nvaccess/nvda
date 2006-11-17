import winUser
import MSAAHandler
from constants import *
import MSAA

def getNVDAObjectClass(processID,windowClass,objectRole):
	if _dynamicMap.has_key((processID,windowClass,objectRole)):
		return _dynamicMap[(processID,windowClass,objectRole)]
	elif _dynamicMap.has_key((processID,windowClass,None)):
		return _dynamicMap[(processID,windowClass,None)]
	elif _dynamicMap.has_key((processID,None,objectRole)):
		return _dynamicMap[(processID,None,objectRole)]
	elif _staticMap.has_key((windowClass,objectRole)):
		return _staticMap[(windowClass,objectRole)]
	elif _staticMap.has_key((windowClass,None)):
		return _staticMap[(windowClass,None)]
	elif _staticMap.has_key((None,objectRole)):
		return _staticMap[(None,objectRole)]
	else:
		return MSAA.NVDAObject_MSAA

def getNVDAObjectByAccessibleObject(ia,child):
	window=MSAAHandler.windowFromAccessibleObject(ia)
	windowClass=winUser.getClassName(window)
	processID=winUser.getWindowThreadProcessID(window)
	role=MSAAHandler.accRole(ia,child)
	return getNVDAObjectClass(processID,windowClass,role)(ia,child)

def getNVDAObjectByLocator(window,objectID,childID):
	res=MSAAHandler.accessibleObjectFromEvent(window,objectID,childID)
	if res:
		return getNVDAObjectByAccessibleObject(res[0],res[1])

def getNVDAObjectByPoint(x,y):
	res=MSAAHandler.accessibleObjectFromPoint(x,y)
	if res:
		return getNVDAObjectByAccessibleObject(res[0],res[1])

def registerNVDAObjectClass(processID,windowClass,objectRole,cls):
	_dynamicMap[(processID,windowClass,objectRole)]=cls

def unregisterNVDAObjectClass(windowClass,objectRole):
	del _dynamicMap[(processID,windowClass,objectRole)]

_dynamicMap={}

_staticMap={
("Shell_TrayWnd",ROLE_SYSTEM_CLIENT):MSAA.NVDAObject_Shell_TrayWnd,
("tooltips_class32",ROLE_SYSTEM_TOOLTIP):MSAA.NVDAObject_tooltip,
("tooltips_class32",ROLE_SYSTEM_HELPBALLOON):MSAA.NVDAObject_tooltip,
("Progman",ROLE_SYSTEM_CLIENT):MSAA.NVDAObject_Progman,
("#32770",ROLE_SYSTEM_DIALOG):MSAA.NVDAObject_dialog,
("TrayClockWClass",ROLE_SYSTEM_CLIENT):MSAA.NVDAObject_TrayClockWClass,
("Edit",ROLE_SYSTEM_TEXT):MSAA.NVDAObject_edit,
("Static",ROLE_SYSTEM_STATICTEXT):MSAA.NVDAObject_staticText,
("RichEdit20W",ROLE_SYSTEM_TEXT):MSAA.NVDAObject_richEdit,
("RICHEDIT50W",ROLE_SYSTEM_TEXT):MSAA.NVDAObject_richEdit,
(None,ROLE_SYSTEM_CHECKBUTTON):MSAA.NVDAObject_checkBox,
(None,ROLE_SYSTEM_OUTLINEITEM):MSAA.NVDAObject_outlineItem,
("MozillaUIWindowClass",None):MSAA.NVDAObject_mozillaUIWindowClass,
("MozillaUIWindowClass",ROLE_SYSTEM_APPLICATION):MSAA.NVDAObject_mozillaUIWindowClass_application,
("ConsoleWindowClass",ROLE_SYSTEM_WINDOW):MSAA.NVDAObject_consoleWindowClass,
("ConsoleWindowClass",ROLE_SYSTEM_CLIENT):MSAA.NVDAObject_consoleWindowClassClient,
("Internet Explorer_Server",None):MSAA.NVDAObject_internetExplorerServer,
}
