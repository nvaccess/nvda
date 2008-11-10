from ctypes import *
from ctypes.wintypes import *
import braille
import queueHandler

#Try to load the fs braille dll
try:
	fsbLib=windll.fsbrldspapi
except:
	fsbLib=None

#Map the needed functions in the fs braille dll
if fsbLib:
	fbOpen=getattr(fsbLib,'_fbOpen@12')
	fbGetCellCount=getattr(fsbLib,'_fbGetCellCount@4')
	fbWrite=getattr(fsbLib,'_fbWrite@16')
	fbClose=getattr(fsbLib,'_fbClose@4')

FB_INPUT=1
FB_DISCONNECT=2

LRESULT=c_long
HCURSOR=c_long

#Standard window class stuff

WNDPROC=CFUNCTYPE(LRESULT,HWND,c_uint,WPARAM,LPARAM)

class WNDCLASSEXW(Structure):
	_fields_=[
		('cbSize',c_uint),
		('style',c_uint),
		('lpfnWndProc',WNDPROC),
		('cbClsExtra',c_int),
		('cbWndExtra',c_int),
		('hInstance',HINSTANCE),
		('hIcon',HICON),
		('HCURSOR',HCURSOR),
		('hbrBackground',HBRUSH),
		('lpszMenuName',LPWSTR),
		('lpszClassName',LPWSTR),
		('hIconSm',HICON),
	]

appInstance=windll.kernel32.GetModuleHandleW(None)

nvdaFsBrlWm=windll.user32.RegisterWindowMessageW(u"nvdaFsBrlWm")

@WNDPROC
def nvdaFsBrlWndProc(hwnd,msg,wParam,lParam):
	if msg==nvdaFsBrlWm and wParam==FB_INPUT:
		a=lParam&0xFF
		b=(lParam>>8)&0xFF
		c=(lParam>>16)&0xff
		d=(lParam>>24)&0xFF
		if a==5: #wizzwheels
			if bool((b>>3)&1) is bool((b>>4)&1):
				braille.handler.scrollBack()
			else:
				braille.handler.scrollForward()
		elif a==4 and c==1 and d==0: #press down bottom row routing key
			queueHandler.queueFunction(queueHandler.eventQueue,braille.handler.routeTo,b)
		return 0
	return windll.user32.DefWindowProcW(hwnd,msg,wParam,lParam)

nvdaFsBrlWndCls=WNDCLASSEXW()
nvdaFsBrlWndCls.cbSize=sizeof(nvdaFsBrlWndCls)
nvdaFsBrlWndCls.lpfnWndProc=nvdaFsBrlWndProc
nvdaFsBrlWndCls.hInstance=appInstance
nvdaFsBrlWndCls.lpszClassName=u"nvdaFsBrlWndCls"

class BrailleDisplayDriver(braille.BrailleDisplayDriverWithCursor):

	name="freedomScientific"
	description="Freedom Scientific Focus / Pacmate series"

	@classmethod
	def check(cls):
		return bool(fsbLib)

	def __init__(self):
		super(BrailleDisplayDriver,self).__init__()
		self._messageWindowClassAtom=windll.user32.RegisterClassExW(byref(nvdaFsBrlWndCls))
		self._messageWindow=windll.user32.CreateWindowExW(0,self._messageWindowClassAtom,u"nvdaFsBrlWndCls window",0,0,0,0,0,None,None,appInstance,None)
		fbHandle=-1
		for port in ("usb","serial"):
			fbHandle=fbOpen(port,self._messageWindow,nvdaFsBrlWm)
			if fbHandle!=-1:
				break
		if fbHandle==-1:
			raise RuntimeError("No display found")
		self.fbHandle=fbHandle

	def terminate(self):
		super(BrailleDisplayDriver,self).terminate()
		fbClose(self.fbHandle)
		windll.user32.DestroyWindow(self._messageWindow)
		windll.user32.UnregisterClassW(self._messageWindowClassAtom,appInstance)

	def _get_numCells(self):
		return fbGetCellCount(self.fbHandle)

	def _display(self,cells):
		cells="".join([chr(x) for x in cells])
		fbWrite(self.fbHandle,0,len(cells),cells)
