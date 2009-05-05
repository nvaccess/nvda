from ctypes import *
from ctypes.wintypes import *
import threading
import win32serviceutil
import win32service
import sys
import os
import time

CREATE_UNICODE_ENVIRONMENT=1024
INFINITE = 0xffffffff
UOI_NAME = 2
SYNCHRONIZE = 0x100000
WAIT_OBJECT_0 = 0
MAXIMUM_ALLOWED = 0x2000000
SecurityIdentification = 2
TokenPrimary = 1
PROCESS_QUERY_INFORMATION = 0x0400
TokenSessionId = 12
TokenUIAccess = 26
WTS_CONSOLE_CONNECT = 0x1
WTS_CONSOLE_DISCONNECT = 0x2
WTS_SESSION_LOGON = 0x5
WTS_SESSION_LOGOFF = 0x6
WTS_SESSION_LOCK = 0x7
WTS_SESSION_UNLOCK = 0x8
WTS_CURRENT_SERVER_HANDLE = 0
WTSUserName = 5

nvdaExec = os.path.join(sys.prefix,"nvda.exe")
launcherExec = os.path.join(sys.prefix,"nvda_service_nvdaLauncher.exe")

def debug(msg):
	file(r"c:\windows\temp\nvdaserv", "a").write(msg + "\n")

def getInputDesktopName():
	desktop = windll.user32.OpenInputDesktop(0, False, 0)
	name = create_unicode_buffer(256)
	windll.user32.GetUserObjectInformationW(desktop, UOI_NAME, byref(name), sizeof(name), None)
	windll.user32.CloseDesktop(desktop)
	return ur"WinSta0\%s" % name.value

class STARTUPINFO(Structure):
	_fields_=[
		('cb',DWORD),
		('lpReserved',LPWSTR),
		('lpDesktop',LPWSTR),
		('lpTitle',LPWSTR),
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

def getLoggedOnUserToken(session):
	# Only works in Windows XP and above.
	token = HANDLE()
	windll.wtsapi32.WTSQueryUserToken(session, byref(token))
	return token.value

def duplicateTokenPrimary(token):
	newToken = HANDLE()
	windll.advapi32.DuplicateTokenEx(token, MAXIMUM_ALLOWED, None, SecurityIdentification, TokenPrimary, byref(newToken))
	windll.kernel32.CloseHandle(token)
	return newToken.value

def getOwnToken():
	process = windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, os.getpid())
	token = HANDLE()
	windll.advapi32.OpenProcessToken(process, MAXIMUM_ALLOWED, byref(token))
	windll.kernel32.CloseHandle(process)
	return token

def getSessionSystemToken(session):
	token = duplicateTokenPrimary(getOwnToken())
	session = DWORD(session)
	windll.advapi32.SetTokenInformation(token, TokenSessionId, byref(session), sizeof(DWORD))
	return token

def executeProcess(desktop, token, executable, *argStrings):
	argsString=" ".join(list(argStrings))
	startupInfo=STARTUPINFO(cb=sizeof(STARTUPINFO),lpDesktop=desktop)
	processInformation=PROCESS_INFORMATION()
	cmdBuf=create_unicode_buffer(u'"%s" %s'%(executable,argsString))
	if token:
		env=c_void_p()
		windll.userenv.CreateEnvironmentBlock(byref(env),token,False)
		try:
			if windll.advapi32.CreateProcessAsUserW(token, None, cmdBuf,None,None,False,CREATE_UNICODE_ENVIRONMENT,env,None,byref(startupInfo),byref(processInformation)) == 0:
				raise WinError()
		finally:
			windll.kernel32.CloseHandle(token)
			windll.userenv.DestroyEnvironmentBlock(env)
	else:
		if windll.kernel32.CreateProcessW(None, cmdBuf,None,None,False,0,None,None,byref(startupInfo),byref(processInformation)) == 0:
			raise WinError()
	return processInformation.hProcess

def nvdaLauncher():
	desktop = getInputDesktopName()
	if desktop == ur"WinSta0\Default":
		return

	startNVDA(desktop)
	desktopSwitchEvt = windll.kernel32.OpenEventW(SYNCHRONIZE, False, u"WinSta0_DesktopSwitch")
	windll.kernel32.WaitForSingleObject(desktopSwitchEvt, INFINITE)
	windll.kernel32.CloseHandle(desktopSwitchEvt)
	exitNVDA(desktop)

def startNVDA(desktop):
	process = executeProcess(desktop, None, nvdaExec)
	windll.kernel32.CloseHandle(process)

def startNVDAUIAccess(session, desktop):
	token = duplicateTokenPrimary(getLoggedOnUserToken(session))
	uiAccess = ULONG(1)
	windll.advapi32.SetTokenInformation(token, TokenUIAccess, byref(uiAccess), sizeof(ULONG))
	process = executeProcess(desktop, token, nvdaExec, "-m")
	windll.kernel32.CloseHandle(process)

def exitNVDA(desktop):
	process = executeProcess(desktop, None, nvdaExec, "-q")
	windll.kernel32.WaitForSingleObject(process, 10000)
	windll.kernel32.CloseHandle(process)

def isUserRunningNVDA(session):
	token = getSessionSystemToken(session)
	process = executeProcess(ur"WinSta0\Default", token, nvdaExec, u"--check-running")
	windll.kernel32.WaitForSingleObject(process, INFINITE)
	exitCode = DWORD()
	windll.kernel32.GetExitCodeProcess(process, byref(exitCode))
	windll.kernel32.CloseHandle(process)
	return exitCode.value == 0

def isSessionLoggedOn(session):
	username = c_wchar_p()
	size = DWORD()
	windll.wtsapi32.WTSQuerySessionInformationW(WTS_CURRENT_SERVER_HANDLE, session, WTSUserName, byref(username), byref(size))
	ret = bool(username.value)
	windll.wtsapi32.WTSFreeMemory(username)
	return ret

def execBg(func):
	t = threading.Thread(target=func)
	t.setDaemon(True)
	t.start()

class NVDAService(win32serviceutil.ServiceFramework):

	_svc_name_="nvda"
	_svc_display_name_="nonVisual Desktop Access"

	def GetAcceptedControls(self):
		return win32serviceutil.ServiceFramework.GetAcceptedControls(self) | win32service.SERVICE_ACCEPT_SESSIONCHANGE

	def initSession(self, session):
		debug("init session %d" % session)
		self.session = session
		self.launcherLock = threading.RLock()
		self.launcherStarted = False
		self.desktopSwitchSupervisorStarted = False
		self.isSessionLoggedOn = isSessionLoggedOn(session)
		debug("session logged on: %r" % self.isSessionLoggedOn)

		if self.isSessionLoggedOn:
			self.handleDesktopSwitch()
			execBg(self.desktopSwitchSupervisor)
		else:
			execBg(self.startLauncher)

	def desktopSwitchSupervisor(self):
		if self.desktopSwitchSupervisorStarted:
			return
		self.desktopSwitchSupervisorStarted = True
		origSession = self.session
		debug("starting desktop switch supervisor, session %d" % origSession)
		desktopSwitchEvt = windll.kernel32.OpenEventW(SYNCHRONIZE, False, u"Session\%d\WinSta0_DesktopSwitch" % self.session)
		if not desktopSwitchEvt:
			try:
				raise WinError()
			except Exception, e:
				debug("error opening event: %s" % e)
				raise

		while self.session == origSession:
			windll.kernel32.WaitForSingleObject(desktopSwitchEvt, INFINITE)
			debug("desktop switch, session %r" % self.session)
			self.handleDesktopSwitch()

		windll.kernel32.CloseHandle(desktopSwitchEvt)
		debug("desktop switch supervisor terminated, session %d" % origSession)

	def handleDesktopSwitch(self):
		with self.launcherLock:
			self.launcherStarted = False

		if not self.isSessionLoggedOn or isUserRunningNVDA(self.session):
			self.startLauncher()
		else:
			debug("not starting launcher; session logged on and user not running NVDA")

	def SvcOtherEx(self, control, eventType, data):
		if control == win32service.SERVICE_CONTROL_SESSIONCHANGE:
			self.handleSessionChange(eventType, data[0])

	def handleSessionChange(self, event, session):
		if event == WTS_CONSOLE_CONNECT:
			debug("connect %d" % session)
			if session != self.session:
				self.initSession(session)
		elif event == WTS_SESSION_LOGON:
			debug("logon %d" % session)
			self.isSessionLoggedOn = True
			execBg(self.desktopSwitchSupervisor)
		elif event == WTS_SESSION_LOGOFF:
			debug("logoff %d" % session)
			self.isSessionLoggedOn = False
			execBg(self.startLauncher)
		elif event == WTS_SESSION_LOCK:
			debug("lock %d" % session)
			if session == self.session:
				self.startLauncher()

	def startLauncher(self):
		with self.launcherLock:
			if self.launcherStarted:
				return

			debug("attempt launcher start")
			token = getSessionSystemToken(self.session)
			try:
				process = executeProcess(ur"WinSta0\Winlogon", token, launcherExec)
				self.launcherStarted = True
				debug("launcher started")
				windll.kernel32.CloseHandle(process)
			except Exception, e:
				debug("error starting launcher: %s" % e)

	def SvcDoRun(self):
		debug("service starting")
		self.exitEvent = threading.Event()
		self.initSession(windll.kernel32.WTSGetActiveConsoleSessionId())
		self.exitEvent.wait()
		debug("service exiting")

	def SvcStop(self):
		self.exitEvent.set()

if __name__=='__main__':
	if not getattr(sys, "frozen", None):
		raise RuntimeError("Can only be run compiled with py2exe")
	win32serviceutil.HandleCommandLine(NVDAService)
