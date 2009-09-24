import time
from ctypes import *
from ctypes.wintypes import *
from comtypes import *
from comtypes.automation import *
import comtypes.client
import winKernel
import winUser
# Include functions from oleacc.dll in the module namespace.
m=comtypes.client.GetModule('oleacc.dll')
globals().update((key, val) for key, val in m.__dict__.iteritems() if not key.startswith("_"))

NAVDIR_MIN=0
NAVDIR_UP=1
NAVDIR_DOWN=2
NAVDIR_LEFT=3
NAVDIR_RIGHT=4
NAVDIR_NEXT=5
NAVDIR_PREVIOUS=6
NAVDIR_FIRSTCHILD=7
NAVDIR_LASTCHILD=8
NAVDIR_MAX=9

ROLE_SYSTEM_TITLEBAR=1
ROLE_SYSTEM_MENUBAR=2
ROLE_SYSTEM_SCROLLBAR=3
ROLE_SYSTEM_GRIP=4
ROLE_SYSTEM_SOUND=5
ROLE_SYSTEM_CURSOR=6
ROLE_SYSTEM_CARET=7
ROLE_SYSTEM_ALERT=8
ROLE_SYSTEM_WINDOW=9
ROLE_SYSTEM_CLIENT=10
ROLE_SYSTEM_MENUPOPUP=11
ROLE_SYSTEM_MENUITEM=12
ROLE_SYSTEM_TOOLTIP=13
ROLE_SYSTEM_APPLICATION=14
ROLE_SYSTEM_DOCUMENT=15
ROLE_SYSTEM_PANE=16
ROLE_SYSTEM_CHART=17
ROLE_SYSTEM_DIALOG=18
ROLE_SYSTEM_BORDER=19
ROLE_SYSTEM_GROUPING=20
ROLE_SYSTEM_SEPARATOR=21
ROLE_SYSTEM_TOOLBAR=22
ROLE_SYSTEM_STATUSBAR=23
ROLE_SYSTEM_TABLE=24
ROLE_SYSTEM_COLUMNHEADER=25
ROLE_SYSTEM_ROWHEADER=26
ROLE_SYSTEM_COLUMN=27
ROLE_SYSTEM_ROW=28
ROLE_SYSTEM_CELL=29
ROLE_SYSTEM_LINK=30
ROLE_SYSTEM_HELPBALLOON=31
ROLE_SYSTEM_CHARACTER=32
ROLE_SYSTEM_LIST=33
ROLE_SYSTEM_LISTITEM=34
ROLE_SYSTEM_OUTLINE=35
ROLE_SYSTEM_OUTLINEITEM=36
ROLE_SYSTEM_PAGETAB=37
ROLE_SYSTEM_PROPERTYPAGE=38
ROLE_SYSTEM_INDICATOR=39
ROLE_SYSTEM_GRAPHIC=40
ROLE_SYSTEM_STATICTEXT=41
ROLE_SYSTEM_TEXT=42
ROLE_SYSTEM_PUSHBUTTON=43
ROLE_SYSTEM_CHECKBUTTON=44
ROLE_SYSTEM_RADIOBUTTON=45
ROLE_SYSTEM_COMBOBOX=46
ROLE_SYSTEM_DROPLIST=47
ROLE_SYSTEM_PROGRESSBAR=48
ROLE_SYSTEM_DIAL=49
ROLE_SYSTEM_HOTKEYFIELD=50
ROLE_SYSTEM_SLIDER=51
ROLE_SYSTEM_SPINBUTTON=52
ROLE_SYSTEM_DIAGRAM=53
ROLE_SYSTEM_ANIMATION=54
ROLE_SYSTEM_EQUATION=55
ROLE_SYSTEM_BUTTONDROPDOWN=56
ROLE_SYSTEM_BUTTONMENU=57
ROLE_SYSTEM_BUTTONDROPDOWNGRID=58
ROLE_SYSTEM_WHITESPACE=59
ROLE_SYSTEM_PAGETABLIST=60
ROLE_SYSTEM_CLOCK=61
ROLE_SYSTEM_SPLITBUTTON=62
ROLE_SYSTEM_IPADDRESS=63
ROLE_SYSTEM_OUTLINEBUTTON=64

STATE_SYSTEM_NORMAL=0
STATE_SYSTEM_UNAVAILABLE=0x1
STATE_SYSTEM_SELECTED=0x2
STATE_SYSTEM_FOCUSED=0x4
STATE_SYSTEM_PRESSED=0x8
STATE_SYSTEM_CHECKED=0x10
STATE_SYSTEM_MIXED=0x20
STATE_SYSTEM_INDETERMINATE=STATE_SYSTEM_MIXED
STATE_SYSTEM_READONLY=0x40
STATE_SYSTEM_HOTTRACKED=0x80
STATE_SYSTEM_DEFAULT=0x100
STATE_SYSTEM_EXPANDED=0x200
STATE_SYSTEM_COLLAPSED=0x400
STATE_SYSTEM_BUSY=0x800
STATE_SYSTEM_FLOATING=0x1000
STATE_SYSTEM_MARQUEED=0x2000
STATE_SYSTEM_ANIMATED=0x4000
STATE_SYSTEM_INVISIBLE=0x8000
STATE_SYSTEM_OFFSCREEN=0x10000
STATE_SYSTEM_SIZEABLE=0x20000
STATE_SYSTEM_MOVEABLE=0x40000
STATE_SYSTEM_SELFVOICING=0x80000
STATE_SYSTEM_FOCUSABLE=0x100000
STATE_SYSTEM_SELECTABLE=0x200000
STATE_SYSTEM_LINKED=0x400000
STATE_SYSTEM_TRAVERSED=0x800000
STATE_SYSTEM_MULTISELECTABLE=0x1000000
STATE_SYSTEM_EXTSELECTABLE=0x2000000
STATE_SYSTEM_ALERT_LOW=0x4000000
STATE_SYSTEM_ALERT_MEDIUM=0x8000000
STATE_SYSTEM_ALERT_HIGH=0x10000000
STATE_SYSTEM_PROTECTED=0x20000000
STATE_SYSTEM_HASPOPUP=0x40000000
STATE_SYSTEM_VALID=0x7fffffff

SELFLAG_NONE=0
SELFLAG_TAKEFOCUS=1
SELFLAG_TAKESELECTION=2
SELFLAG_EXTENDSELECTION=4
SELFLAG_ADDSELECTION=8
SELFLAG_REMOVESELECTION=16
SELFLAG_VALID=32

def LresultFromObject(wParam,obj):
	"""
	returns a reference, similar to a handle, to the specified object. 
	Servers return this reference when handling WM_GETOBJECT.
	@param wParam: the wParam value passed in with WM_GETOBJECT.
	@type wParam: int
	@param obj: the COM object instance you want a reference for.
	@type obj: COMObject
	@return: a reference to the object.
	@rtype: int
	""" 
	objIID=obj._iid_
	return oledll.oleacc.LresultFromObject(byref(objIID),obj._com_pointers_[objIID])

def ObjectFromLresult(res,wParam,interface):
	"""
	retrieves a requested interface pointer for an accessible object 
	based on a previously generated object reference.
	@param res: the previously generated object reference.
	@type res: int
	@param wParam: the wParam value passed in with WM_GETOBJECT.
	@type wParam: int
	@param interface: the requested COM interface.
	@type interface: comtypes COM interface
	@return: the object.
	@rtype: COMObject
	"""
	p=POINTER(interface)()
	oledll.oleacc.ObjectFromLresult(res,byref(interface._iid_),wParam,byref(p))
	return p

def CreateStdAccessibleProxy(hwnd,className,objectID,interface=IAccessible):
	"""
	creates an accessible object using a specific window class, with the methods and properties 
	of the specified type of system-provided user interface element.
	@param hwnd: the handle of the window this accessible object should represent.
	@type hwnd: int
	@param className: the window class name to use.
	@type className: basestring
	@param objectID: an OBJID_* constant or custom value stating the specific object in the window.
	@type objectID: int
	@param interface: the requested COM interface for this object. Defaults to IAccessible.
	@type interface: comtypes COM interface
	@return: the created object.
	@rtype: COMObject
	"""
	p=POINTER(interface)()
	oledll.oleacc.CreateStdAccessibleProxyW(hwnd,className,objectID,byref(interface._iid_),byref(p))
	return p

def CreateStdAccessibleObject(hwnd,objectID,interface=IAccessible):
	"""
	creates an accessible object with the methods and properties 
	of the specified type of system-provided user interface element.
	@param hwnd: the handle of the window this accessible object should represent.
	@type hwnd: int
	@param objectID: an OBJID_* constant or custom value stating the specific object in the window.
	@type objectID: int
	@param interface: the requested COM interface for this object. Defaults to IAccessible.
	@type interface: comtypes COM interface
	@return: the created object.
	@rtype: COMObject
	""" 
	p=POINTER(interface)()
	oledll.oleacc.CreateStdAccessibleObject(hwnd,objectID,byref(interface._iid_),byref(p))
	return p

def AccessibleObjectFromWindow(hwnd,objectID,interface=IAccessible):
	"""
	Retreaves a COM object from the given window, with the given object ID.
	@param hwnd: the handle of the window to retreave the object from.
	@type hwnd: int
	@param objectID: one of the OBJID_* constants or a custom positive value representing the specific object you want to retreave.
	@type objectID: int
	@param interface: the requested COM interface you wish to use on the retreaved object.
	@type interface: comtypes COM interface
	@return: the retreaved object.
	@rtype: COMObject
	"""
	p=POINTER(interface)()
	oledll.oleacc.AccessibleObjectFromWindow(hwnd,objectID,byref(p._iid_),byref(p))
	return p

def AccessibleObjectFromWindow_safe(hwnd,objectID,interface=IAccessible,timeout=2):
	if not hwnd:
		raise ValueError("Invalid window")
	wmResult=c_long()
	res=windll.user32.SendMessageTimeoutW(hwnd,winUser.WM_GETOBJECT,0,objectID,winUser.SMTO_ABORTIFHUNG,int(timeout*1000),byref(wmResult))==0
	if res:
		raise OSError("WM_GETOBJECT failed")
	if wmResult.value:
		return ObjectFromLresult(wmResult.value,0,interface)
	return CreateStdAccessibleObject(hwnd,objectID,interface)

def AccessibleObjectFromEvent(hwnd,objectID,childID):
	"""
	Retreaves an  IAccessible object from the given window, with the given object ID and child ID.
	@param hwnd: the handle of the window to retreave the object from.
	@type hwnd: int
	@param objectID: one of the OBJID_* constants or a custom positive value representing the specific object you want to retreave.
	@type objectID: int
	@param childID: the ID of the child element you wish to retreave.
	@type childID: int
	@return: the retreaved object.
	@rtype: COMObject
	"""
	p=POINTER(IAccessible)()
	varChild=VARIANT()
	oledll.oleacc.AccessibleObjectFromEvent(hwnd,objectID,childID,byref(p),byref(varChild))
	if varChild.vt==VT_I4:
		childID=varChild.value
	return (p,childID)

def AccessibleObjectFromEvent_safe(hwnd,objectID,childID,timeout=2):
	obj=AccessibleObjectFromWindow_safe(hwnd,objectID,timeout=timeout)
	if not obj:
		raise RuntimeError("AccessibleObjectFromWindow failed")
	if childID!=0:
		try:
			childObj=obj.accChild(childID)
		except COMError:
			childObj=None
		if childObj:
			obj=childObj
			childID=0
	return (obj,childID)

def WindowFromAccessibleObject(pacc):
	"""
	Retreaves the handle of the window this IAccessible object belongs to.
	@param pacc: the IAccessible object who's window you want to fetch.
	@type pacc: POINTER(IAccessible)
	@return: the window handle.
	@rtype: int
	"""
	hwnd=c_int()
	oledll.oleacc.WindowFromAccessibleObject(pacc,byref(hwnd))
	return hwnd.value

def AccessibleObjectFromPoint(x,y):
	point=POINT(x,y)
	pacc=POINTER(IAccessible)()
	varChild=VARIANT()
	oledll.oleacc.AccessibleObjectFromPoint(point,byref(pacc),byref(varChild))
	if not isinstance(varChild.value,int):
		child=0
	else:
		child=varChild.value
	return (pacc,child)

def AccessibleChildren(pacc,iChildStart,cChildren):
	varChildren=(VARIANT*cChildren)()
	pcObtained=c_int()
	oledll.oleacc.AccessibleChildren(pacc,iChildStart,cChildren,byref(varChildren),byref(pcObtained))
	return [x.value for x in varChildren[0:pcObtained.value]]

def GetProcessHandleFromHwnd(windowHandle):
	"""Retreaves a process handle of the process who owns the window.
	If Windows Vista, uses GetProcessHandleFromHwnd found in oleacc.dll which allows a client with UIAccess to open a process who is elevated.
	if older than Windows Vista, just uses OpenProcess from user32.dll instead.
	@param windowHandle: a window of a process you wish to retreave a process handle for
	@type windowHandle: integer
	@returns: a process handle with read, write and operation access
	@rtype: integer
	"""
	try:
		return oledll.oleacc.GetProcessHandleFromHwnd(windowHandle)
	except:
		import winKernel
		return winKernel.openProcess(winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE|winKernel.PROCESS_VM_OPERATION,False,winUser.getWindowThreadProcessID(windowHandle)[0])

def GetRoleText(role):
	textLen=oledll.oleacc.GetRoleTextW(role,0,0)
	if textLen:
		buf=create_unicode_buffer(textLen+2)
		oledll.oleacc.GetRoleTextW(role,buf,textLen+1)
		return buf.value
	else:
		return None

def GetStateText(state):
	textLen=oledll.oleacc.GetStateTextW(state,0,0)
	if textLen:
		buf=create_unicode_buffer(textLen+2)
		oledll.oleacc.GetStateTextW(state,buf,textLen+1)
		return buf.value
	else:
		return None
