from ctypes import *
from ctypes.wintypes import *
import win32serviceutil
import servicemanager
import sys
import os
import time

if not getattr(sys, "frozen", None):
	raise RuntimeError("Can only be run compiled with py2exe")

INFINITE = 0xffffffff
UOI_NAME = 2
SYNCHRONIZE = 0x100000
WAIT_OBJECT_0 = 0
#MAXIMUM_ALLOWED = 0x2000000
#SecurityIdentification = 2
#TokenPrimary = 1

def getInputDesktopName():
	desktop = windll.user32.OpenInputDesktop(0, False, 0)
	name = create_string_buffer(256)
	windll.user32.GetUserObjectInformationA(desktop, UOI_NAME, byref(name), sizeof(name), None)
	windll.user32.CloseDesktop(desktop)
	return r"winsta0\%s" % name.value

class STARTUPINFO(Structure):
	_fields_=[
		('cb',DWORD),
		('lpReserved',LPSTR),
		('lpDesktop',LPSTR),
		('lpTitle',LPSTR),
		('dwX',DWORD),
		('dwY',DWORD),
		('dwXSize',DWORD),
		('dwYSize',DWORD),
		('dwXCountChars',DWORD),
		('dwYCountChars',DWORD),
		('dwFillAttribute',DWORD),
		('dwFlags',DWORD),
		('wShowWindow',WORD),
		('cbReserved2',WORD),
		('lpReserved2',POINTER(c_byte)),
		('hSTDInput',HANDLE),
		('hSTDOutput',HANDLE),
		('hSTDError',HANDLE),
	]

class PROCESS_INFORMATION(Structure):
	_fields_=[
		('hProcess',HANDLE),
		('hThread',HANDLE),
		('dwProcessID',DWORD),
		('dwThreadID',DWORD),
	]

def getLoggedOnUserToken():
	# Only works in Windows XP and above.
	token = HANDLE()
	windll.wtsapi32.WTSQueryUserToken(windll.kernel32.WTSGetActiveConsoleSessionId(), byref(token))
	return token.value

def executeNVDA(desktop, token, *argStrings):
	argsString=" ".join(list(argStrings))
	executable=os.path.join(sys.prefix,"nvda.exe")
	startupInfo=STARTUPINFO(cb=sizeof(STARTUPINFO),lpDesktop=desktop)
	processInformation=PROCESS_INFORMATION()
	if token:
		#newToken = HANDLE()
		#windll.advapi32.DuplicateTokenEx(token, MAXIMUM_ALLOWED, None, SecurityIdentification, TokenPrimary, byref(newToken))
		#windll.kernel32.CloseHandle(token)
		#token = newToken.value
		windll.advapi32.CreateProcessAsUserA(token, None, '"%s" %s'%(executable,argsString),None,None,False,0,None,None,byref(startupInfo),byref(processInformation))
		windll.kernel32.CloseHandle(token)
	else:
		windll.kernel32.CreateProcessA(None, '"%s" %s'%(executable,argsString),None,None,False,0,None,None,byref(startupInfo),byref(processInformation))
	return processInformation.hProcess

class NVDAService(win32serviceutil.ServiceFramework):

	_svc_name_="nvda"
	_svc_display_name_="nonVisual Desktop Access"

	def SvcDoRun(self):
		desktopSwitchEvt = windll.kernel32.OpenEventA(SYNCHRONIZE, False, "WinSta0_DesktopSwitch")

		while True:
			desktop = getInputDesktopName()
			# Start NVDA on the input desktop.
			if desktop.endswith("Winlogon"):
				# Don't run with the logged on user token for the Winlogon desktop.
				token = None
			else:
				token = getLoggedOnUserToken()
			process = executeNVDA(desktop, token, "-m")
			# Wait for NVDA to exit or the input desktop to change.
			res = windll.kernel32.WaitForMultipleObjects(2, (HANDLE * 2)(process, desktopSwitchEvt), False, INFINITE)
			if res == WAIT_OBJECT_0:
				# NVDA has been exited.
				exitCode = DWORD()
				windll.kernel32.GetExitCodeProcess(process, byref(exitCode))
				if exitCode.value == 0:
					# NVDA was exited gracefully, so the service should terminate.
					windll.kernel32.CloseHandle(process)
					break
				else:
					# The NVDA process was terminated.
					# Impose a delay to avoid flooding restarts.
					time.sleep(2)
			else:
				# The input desktop has changed.
				# Exit NVDA on the old input desktop.
				windll.kernel32.WaitForSingleObject(executeNVDA(desktop, None, "-q"), 10000)
			windll.kernel32.CloseHandle(process)

		windll.kernel32.CloseHandle(desktopSwitchEvt)

	def SvcStop(self):
		executeNVDA(getInputDesktopName(), None, "-q")

if __name__=='__main__':
	win32serviceutil.HandleCommandLine(NVDAService)
