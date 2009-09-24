from ctypes import *
from ctypes.wintypes import *
import threading
import win32serviceutil
import win32service
import sys
import os
import time
import _winreg

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
slaveExec = os.path.join(sys.prefix,"nvda_slave.exe")

def debug(msg):
	try:
		file(os.path.join(os.getenv("windir"), "temp", "nvda_service.log"), "a").write(msg + "\n")
	except (OSError, IOError):
		pass

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
	debug("launcher: starting with desktop %s" % desktop)
	if os.path.basename(desktop) in (u"Default", u"Screen-saver"):
		debug("launcher: default or screen-saver desktop, exiting")
		return

	debug("launcher: starting NVDA")
	process = startNVDA(desktop)
	desktopSwitchEvt = windll.kernel32.OpenEventW(SYNCHRONIZE, False, u"WinSta0_DesktopSwitch")
	windll.kernel32.WaitForSingleObject(desktopSwitchEvt, INFINITE)
	windll.kernel32.CloseHandle(desktopSwitchEvt)
	debug("launcher: desktop switch, exiting NVDA on desktop %s" % desktop)
	exitNVDA(desktop)
	# NVDA should never ever be left running on other desktops, so make certain it is dead.
	# It may still be running if it hasn't quite finished initialising yet, in which case -q won't work.
	windll.kernel32.TerminateProcess(process, 1)
	windll.kernel32.CloseHandle(process)

def startNVDA(desktop):
	return executeProcess(desktop, None, nvdaExec, "-m", "--secure")

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

def shouldStartOnLogonScreen():
	try:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, ur"SOFTWARE\NVDA")
		return bool(_winreg.QueryValueEx(k, u"startOnLogonScreen")[0])
	except WindowsError:
		return False

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

		if self.isWindowsXP and session != 0 and not self.isSessionLoggedOn:
			# In Windows XP, sessions other than 0 are broken before logon, so we can't do anything more here.
			debug("Windows XP, returning before action")
			return

		if self.isSessionLoggedOn:
			# The session is logged on, so treat this as a normal desktop switch.
			self.handleDesktopSwitch()
		else:
			# We're at the logon screen.
			if shouldStartOnLogonScreen():
				execBg(self.startLauncher)
		execBg(self.desktopSwitchSupervisor)

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

		while True:
			windll.kernel32.WaitForSingleObject(desktopSwitchEvt, INFINITE)
			if self.session != origSession:
				break
			debug("desktop switch, session %r" % self.session)
			self.handleDesktopSwitch()

		windll.kernel32.CloseHandle(desktopSwitchEvt)
		debug("desktop switch supervisor terminated, session %d" % origSession)

	def handleDesktopSwitch(self):
		with self.launcherLock:
			self.launcherStarted = False

		if (not self.isSessionLoggedOn and shouldStartOnLogonScreen()) or isUserRunningNVDA(self.session):
			self.startLauncher()
		else:
			debug("not starting launcher")

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
			if session == 0 and shouldStartOnLogonScreen():
				# In XP, a logoff in session 0 does not cause a new session to be created.
				# Instead, we're probably heading back to the logon screen.
				execBg(self.startLauncher)
		elif event == WTS_SESSION_LOCK:
			debug("lock %d" % session)
			# If the user was running NVDA, the desktop switch will have started NVDA on the secure desktop.
			# This only needs to cover the case where the user was not running NVDA and the session is locked.
			# In this case, we should treat the lock screen like the logon screen.
			if session == self.session and shouldStartOnLogonScreen():
				self.startLauncher()

	def startLauncher(self):
		with self.launcherLock:
			if self.launcherStarted:
				return

			debug("attempt launcher start on session %d" % self.session)
			token = getSessionSystemToken(self.session)
			try:
				process = executeProcess(ur"WinSta0\Winlogon", token, slaveExec, u"service_NVDALauncher")
				self.launcherStarted = True
				debug("launcher started on session %d" % self.session)
				windll.kernel32.CloseHandle(process)
			except Exception, e:
				debug("error starting launcher: %s" % e)

	def SvcDoRun(self):
		debug("service starting")
		self.isWindowsXP = sys.getwindowsversion()[0:2] == (5, 1)
		self.exitEvent = threading.Event()
		self.initSession(windll.kernel32.WTSGetActiveConsoleSessionId())
		self.exitEvent.wait()
		debug("service exiting")

	def SvcStop(self):
		self.exitEvent.set()

def installService(nvdaDir):
	servicePath = os.path.join(nvdaDir, __name__ + ".exe")
	if not os.path.isfile(servicePath):
		raise RuntimeError("Could not find service executable")
	win32serviceutil.InstallService(None, NVDAService._svc_name_, NVDAService._svc_display_name_, startType=win32service.SERVICE_AUTO_START, exeName=servicePath)

def removeService():
	win32serviceutil.RemoveService(NVDAService._svc_name_)

def startService():
	win32serviceutil.StartService(NVDAService._svc_name_)

def stopService():
	"""Stop the running service and wait for its process to die.
	"""
	scm = win32service.OpenSCManager(None,None,win32service.SC_MANAGER_ALL_ACCESS)
	try:
		serv = win32service.OpenService(scm, NVDAService._svc_name_, win32service.SERVICE_ALL_ACCESS)
		try:
			pid = win32service.QueryServiceStatusEx(serv)["ProcessId"]

			# Stop the service.
			win32service.ControlService(serv, win32service.SERVICE_CONTROL_STOP)

			# Wait for the process to exit.
			proc = windll.kernel32.OpenProcess(SYNCHRONIZE, False, pid)
			if not proc:
				return
			try:
				windll.kernel32.WaitForSingleObject(proc, INFINITE)
			finally:
				windll.kernel32.CloseHandle(proc)

		finally:
			win32service.CloseServiceHandle(serv)
	finally:
		win32service.CloseServiceHandle(scm)

if __name__=='__main__':
	if not getattr(sys, "frozen", None):
		raise RuntimeError("Can only be run compiled with py2exe")
	win32serviceutil.HandleCommandLine(NVDAService)
