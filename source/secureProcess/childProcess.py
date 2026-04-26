# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


import io
import contextlib
import sys
import threading
import os
import msvcrt
import winerror
import ctypes
from ctypes import (
	byref,
	POINTER,
	cast,
	sizeof,
)
from ctypes.wintypes import (
	HANDLE,
	DWORD,
	LPVOID,
	LPWSTR,
)
from comtypes.hresult import HRESULT_FROM_WIN32
import subprocess
import ctypes.wintypes
import win32security
import win32con
from winBindings.advapi32 import (
	CreateProcessWithToken,
	CreateProcessAsUser,
	FreeSid,
	ConvertSidToStringSid,
)
from winBindings.winnt import (
	STARTUPINFOEX,
	PROCESS_INFORMATION,
	STARTF_USESTDHANDLES,
	CREATIONFLAGS_CREATE_NO_WINDOW,
	CREATIONFLAGS_CREATE_SUSPENDED,
	CREATIONFLAGS_CREATE_UNICODE_ENVIRONMENT,
	CREATIONFLAGS_EXTENDED_STARTUPINFO_PRESENT,
	PSID,
	SECURITY_CAPABILITIES,
	SID_AND_ATTRIBUTES,
	PROC_THREAD_ATTRIBUTE,
)
from winBindings.kernel32 import (
	GetExitCodeProcess,
	WaitForSingleObject,
	TerminateProcess,
	CreateProcess,
	ResumeThread,
	CloseHandle,
	SetErrorMode,
	InitializeProcThreadAttributeList,
	UpdateProcThreadAttribute,
	DeleteProcThreadAttributeList,
	LocalFree,
	DeriveCapabilitySidsFromName,
	GetCurrentProcess,
	DuplicateHandle,
)
from winBindings.ole32 import (
	CoTaskMemFree,
)
from .token import (
	createEnvironmentBlock,
)
from .raiiUtils import (
	makeAutoFree,
	OnDelete,
)
from logHandler import log


class BasicPopen:
	def __init__(
		self,
		args: list[str],
		env: dict[str, str] | None = None,
		cwd: str | None = None,
		desktop: str | None = None,
		stdin: int | None = None,
		stdout: int | None = None,
		stderr: int | None = None,
		startSuspended: bool = False,
		hideCriticalErrorDialogs: bool = False,
		createNoWindow: bool = False,
	):
		"""
		Initialize and create a child process.

		Sets up creation flags, optional environment block and standard I/O pipes, and
		creates the process (optionally suspended). The method prepares STARTUPINFO
		and PROCESS_INFORMATION, configures handle inheritance for any requested
		standard streams, and calls the CreateProcess Windows API to create the
		process.

		:param args: Command and arguments to execute.
		:param env: Environment variables for the child process; if provided, a
			Unicode environment block will be created for use by the new process.
		:param cwd: Working directory for the child process.
		:param desktop: Desktop name for the new process.
		:param stdin: If subprocess.PIPE, a writable file object connected to the
			child's standard input is created.
		:param stdout: If subprocess.PIPE, a readable file object connected to the
			child's standard output is created.
		:param stderr: If subprocess.PIPE, a readable file object connected to the
			child's standard error is created. If subprocess.STDOUT, stderr is
			redirected to stdout.
		:param startSuspended: If True, the child process is created suspended.
		:param hideCriticalErrorDialogs: If True, the error mode is temporarily
			changed to suppress critical error dialogs while creating the process.
		:param createNoWindow: If True, the process is created without a window (I.e. CREATIONFLAGS_CREATE_NO_WINDOW).
		"""
		self.args = args
		self._creationFlags = 0
		if createNoWindow:
			self._creationFlags |= CREATIONFLAGS_CREATE_NO_WINDOW
		self._hideCriticalErrorDialogs = hideCriticalErrorDialogs
		if startSuspended:
			self._creationFlags |= CREATIONFLAGS_CREATE_SUSPENDED
		self.cwd = cwd
		if env:
			self._envBlock = createEnvironmentBlock(env)
			self._creationFlags |= CREATIONFLAGS_CREATE_UNICODE_ENVIRONMENT
		else:
			self._envBlock = None
		self._cmdline = subprocess.list2cmdline(args)
		self.returncode = None
		self._handle = None
		self._thread_handle = None
		self.pid = None
		self.stdin = None
		self.stdout = None
		self.stderr = None
		pStdinRead = pStdoutWrite = pStderrWrite = 0
		if stdin == subprocess.PIPE:
			self.stdin, pStdinRead = self._createPipe(push=True)
		if stdout == subprocess.PIPE:
			self.stdout, pStdoutWrite = self._createPipe(push=False)
		if stderr == subprocess.PIPE:
			self.stderr, pStderrWrite = self._createPipe(push=False)
		elif stderr == subprocess.STDOUT:
			pStderrWrite = pStdoutWrite
		siEx = STARTUPINFOEX()
		siEx.startupInfo.cb = sizeof(STARTUPINFOEX)
		if desktop:
			siEx.startupInfo.lpDesktop = desktop
			log.debug(f"Setting STARTUPINFO.lpDesktop to: {desktop}")
		siEx.startupInfo.hSTDInput = pStdinRead
		siEx.startupInfo.hSTDOutput = pStdoutWrite
		siEx.startupInfo.hSTDError = pStderrWrite
		if pStdinRead or pStdoutWrite or pStderrWrite:
			siEx.startupInfo.dwFlags |= STARTF_USESTDHANDLES
			handlesList = []
			if pStdinRead:
				handlesList.append(pStdinRead)
			if pStdoutWrite:
				handlesList.append(pStdoutWrite)
			if pStderrWrite and pStderrWrite != pStdoutWrite:
				handlesList.append(pStderrWrite)
			handlesBuf = (HANDLE * len(handlesList))(*handlesList)
			self._addProcthreadAttribute(PROC_THREAD_ATTRIBUTE.HANDLE_LIST, handlesBuf)
		procThreadAttributes = self._getProcThreadAttributes()
		if len(procThreadAttributes) > 0:
			attribsBufSize = ctypes.c_size_t()
			InitializeProcThreadAttributeList(None, len(procThreadAttributes), 0, byref(attribsBufSize))
			if attribsBufSize.value == 0:
				raise RuntimeError(f"Failed to get attribute list size, {ctypes.WinError()}")
			attribsBuf = OnDelete(ctypes.c_buffer(attribsBufSize.value), DeleteProcThreadAttributeList)
			if not InitializeProcThreadAttributeList(
				attribsBuf.value,
				len(procThreadAttributes),
				0,
				byref(attribsBufSize),
			):
				raise RuntimeError(f"Failed to initialize attribute list, {ctypes.WinError()}")
			log.debug(f"Initialized proc thread attributes, size ={attribsBufSize.value}")
			for attrib, val in procThreadAttributes.items():
				log.debug(f"Updating proc thread attribute: {attrib.name}")
				if not UpdateProcThreadAttribute(
					attribsBuf.value,
					0,
					attrib,
					byref(val),
					sizeof(val),
					None,
					None,
				):
					raise RuntimeError(f"Failed to update attribute list, {ctypes.WinError()}")
			siEx.lpAttributeList = cast(attribsBuf.value, LPVOID)
			siEx._attribsBufRef = attribsBuf  # Keep a reference to avoid GC
		self._siEx = siEx
		self._creationFlags |= CREATIONFLAGS_EXTENDED_STARTUPINFO_PRESENT
		self._pi = PROCESS_INFORMATION()

		with self._beforeAfterCreateProcess():
			self._createProcess()
		self._handle = makeAutoFree(HANDLE, CloseHandle)(self._pi.hProcess)
		self._thread_handle = makeAutoFree(HANDLE, CloseHandle)(self._pi.hThread)
		self.pid = self._pi.dwProcessID
		log.debug(f"Created process with PID: {self.pid}")

	def _getProcThreadAttributes(self):
		if not hasattr(self, "_procThreadAttributes"):
			self._procThreadAttributes = {}
		return self._procThreadAttributes

	def _addProcthreadAttribute(self, attrib: PROC_THREAD_ATTRIBUTE, value: object):
		"""
		Add an attribute to the process thread attribute list.

		:param attrib: Attribute key.
		:param value: Attribute value.
		"""
		pta = self._getProcThreadAttributes()
		pta[attrib] = value

	@contextlib.contextmanager
	def _beforeAfterCreateProcess(self):
		"""
		A Context manager that wraps the call to CreateProcess, which temporarily modifies the process error mode during process creation to hide error dialogs if configured to do so.
		"""
		prevErrorMode = 0
		if self._hideCriticalErrorDialogs:
			log.debug("Setting error mode to hide critical error dialogs...")
			prevErrorMode = SetErrorMode(1)
		try:
			yield
		finally:
			if self._hideCriticalErrorDialogs:
				log.debug("Restoring previous error mode...")
				SetErrorMode(prevErrorMode)

	def _createProcess(self):
		"""
		Calls the CreateProcess Windows API to create the child process.
		::raise RuntimeError: If process creation fails.
		"""
		log.debug("Calling CreateProcess...")
		if not CreateProcess(
			None,
			self._cmdline,
			None,
			None,
			True,
			self._creationFlags,
			self._envBlock,
			self.cwd,
			byref(self._siEx.startupInfo),
			byref(self._pi),
		):
			raise RuntimeError(f"Failed to create process, {ctypes.WinError()}")

	def _duplicateHandleForProcess(self, handle: HANDLE, accessMask: int) -> HANDLE:
		"""
		Duplicate a handle into the child process.

		:param handle: Handle to duplicate.
		:param accessMask: Desired access mask for the duplicated handle.
		:returns: Duplicated handle valid in the child process.
		:raises RuntimeError: If duplicating the handle fails.
		"""
		dupHandle = HANDLE()
		hCurProcess = GetCurrentProcess()
		if not DuplicateHandle(hCurProcess, handle, self._handle, byref(dupHandle), accessMask, False, 0):
			raise RuntimeError(f"Failed to duplicate handle into child process, {ctypes.WinError()}")
		return dupHandle

	def _createPipe(self, push: bool = True, duplicateIntoProcess: bool = False) -> tuple[io.FileIO, HANDLE]:
		"""
		Create an anonymous pipe and return the parent-side Python object and the
		child-side HANDLE suitable for use as a standard stream.

		When ``push`` is True this prepares a writable file object that the parent
		can write to (typically connected to the child's standard input) and a
		native HANDLE for the read end.

		When ``push`` is False this prepares a readable file object that the
		parent can read from (typically connected to the child's standard output
		or error) and a native HANDLE for the write end.

		If ``duplicateIntoProcess`` is True, the child-side HANDLE is duplicated
		into the child process. useful if the child is already created .

		The returned file objects are opened in binary mode with no buffering, and
		if duplicateIntoProcess is True, the native handles are wrapped with makeAutoFree so they will be closed
		automatically when no longer needed.

		:param push: If True create a writable parent-side file and a child-side
			read HANDLE; otherwise create a readable parent-side file and a
			child-side write HANDLE.
		:returns: A tuple containing (parent_file_object, child_handle).
		"""
		r_fd, w_fd = os.pipe()
		if push:
			w_file = os.fdopen(w_fd, "wb", 0)
			r_handle = makeAutoFree(HANDLE, CloseHandle)(msvcrt.get_osfhandle(r_fd))
			if duplicateIntoProcess:
				r_handle = self._duplicateHandleForProcess(r_handle, win32con.GENERIC_READ)
			else:
				os.set_inheritable(r_fd, True)
			return w_file, r_handle
		else:
			r_file = os.fdopen(r_fd, "rb", 0)
			w_handle = makeAutoFree(HANDLE, CloseHandle)(msvcrt.get_osfhandle(w_fd))
			if duplicateIntoProcess:
				w_handle = self._duplicateHandleForProcess(w_handle, win32con.GENERIC_WRITE)
			else:
				os.set_inheritable(w_fd, True)
			return r_file, w_handle

	def resume(self):
		"""
		Resume the main thread of a suspended child process.

		This resumes the primary thread of the process if it was created in a
		suspended state. If the process was not started (no thread handle is
		available) a RuntimeError is raised. If the underlying ResumeThread call
		fails, a RuntimeError is raised containing the Windows error. If the
		previous suspend count is greater than one, the thread is not yet fully
		resumed and a debug warning is logged.

		:raises RuntimeError: if the process was not started or ResumeThread fails.
		:returns: None
		"""

		if not self._thread_handle:
			raise RuntimeError("Process not started")
		prevCount = ResumeThread(self._thread_handle)
		if prevCount == -1:
			raise RuntimeError(f"Failed to resume process thread, {ctypes.WinError()}")
		elif prevCount > 1:
			log.warning(f"ResumeThread returned previous count {prevCount}, not resumed yet")

	def poll(self) -> int | None:
		"""
		Poll the child process to determine whether it has terminated.

		Checks and returns the cached returncode if available. Otherwise this
		queries the system for the process exit code. If the process is still
		active, None is returned. The exit code is cached on first retrieval so
		subsequent calls return the same value.

		:raises RuntimeError: If querying the process exit code via the Windows
		    API fails.
		:return: The process exit code, or None if the process is still running.
		"""

		if self.returncode is not None:
			return self.returncode
		exitCode = DWORD()
		if not GetExitCodeProcess(self._handle, byref(exitCode)):
			raise RuntimeError(f"Failed to get process exit code, {ctypes.WinError()}")
		if exitCode.value == 259:  # STILL_ACTIVE
			return None
		self.returncode = exitCode.value
		return self.returncode

	def wait(self, timeoutMS: int | None = None):
		"""
		Wait for the child process to terminate.

		Blocks until the process exits or until the optional timeout elapses.

		:param timeoutMS: Number of millyseconds to wait. If None, wait indefinitely.
		:return: The process exit code, or None if the timeout expired and the
		    process is still running.
		:raises RuntimeError: If querying the process exit code fails.
		"""
		if timeoutMS is None:
			dur = 0xFFFFFFFF  # INFINITE
		else:
			dur = timeoutMS
		log.debug("Waiting for process to terminate...")
		WaitForSingleObject(self._handle, dur)
		return self.poll()

	def terminate(self):
		"""Terminates the process"""
		if self.poll() is None:
			log.debug("Terminating process...")
			TerminateProcess(self._handle, 1)

	def isRunning(self) -> bool:
		"""Check if the process is still running."""
		return self.poll() is None

	def interact(self):
		"""
		Allow interacting with the child process via the parent's console, until the child process exits.

		Start background threads to forward data between this process and the
		child when standard streams were configured as pipes. The method
		blocks until the child process exits. If the parent's standard input was
		connected, a daemon thread is started to feed data to the child's stdin.
		If the child's stdout was connected, a thread is started to copy its
		output to the parent's stdout.

		On KeyboardInterrupt the child process will be terminated.

		:returns: None
		:raises RuntimeError: If waiting for, or querying, the child process
		    fails, or if an I/O error occurs while reading or writing stream data.
		"""
		log.debug("Interacting with process...")
		if self.stdin:
			stdinThread = threading.Thread(target=self._stdinThreadProc, daemon=True)
			stdinThread.start()
		if self.stdout:
			stdoutThread = threading.Thread(target=self._stdoutThreadProc)
			stdoutThread.start()
		try:
			self.wait()
		except KeyboardInterrupt:
			self.terminate()
		if self.stdout:
			stdoutThread.join()

	def _stdinThreadProc(self):
		if self.stdin:
			while True:
				data = os.read(sys.stdin.fileno(), 1024)
				if not data:
					break
				lines = data.splitlines(keepends=True)
				for line in lines:
					self.stdin.write(line)
				self.stdin.flush()
			self.stdin.close()

	def _stdoutThreadProc(self):
		if self.stdout:
			while True:
				data = self.stdout.read(1024)
				if not data:
					break
				sys.stdout.buffer.write(data)
				sys.stdout.buffer.flush()


class PopenWithToken(BasicPopen):
	"""
	Create a child process using a specific user token.

	This subclass of BasicPopen selects the appropriate Windows API to
	create a process under the security context represented by the
	provided token. It can either use CreateProcessWithToken (secure logon)
	or CreateProcessAsUser depending on the ``useSecLogon`` flag.
	"""

	def __init__(self, token: HANDLE, *args, useSecLogon: bool = False, logonFlags: int = 0, **kwargs):
		"""
		Initialize the PopenWithToken instance.

		Creates a process wrapper that will create child processes using the
		supplied security token. The instance stores the token and options that
		control which Windows API is used when creating the process. Positional
		and keyword arguments are forwarded to the BasicPopen initializer.

		:param token: Handle to the user token to use for process creation.
		:param args: Positional arguments forwarded to BasicPopen.
		:param useSecLogon: If true, CreateProcessWithToken will be used instead
		    of CreateProcessAsUser.
		:param logonFlags: Flags to pass to CreateProcessWithToken when used.
		:param kwargs: Additional keyword arguments forwarded to BasicPopen.
		"""
		self.token = token
		self.logonFlags = logonFlags
		self.useSecLogon = useSecLogon
		super().__init__(*args, **kwargs)

	def _createProcess(self):
		if self.useSecLogon:
			self._createProcessWithToken()
		else:
			self._createProcessAsUser()

	def _createProcessWithToken(self):
		log.debug("Calling CreateProcessWithToken...")
		creationFlags = self._creationFlags
		# Remove extended startup info flag as it's not "supported" by CreateProcessWithToken.
		# Oddly enough, it will check cbSize of STARTUPINFO and honor it anyway.
		creationFlags &= ~CREATIONFLAGS_EXTENDED_STARTUPINFO_PRESENT
		if not CreateProcessWithToken(
			self.token,
			self.logonFlags,
			None,
			self._cmdline,
			creationFlags,
			self._envBlock,
			self.cwd,
			byref(self._siEx.startupInfo),
			byref(self._pi),
		):
			raise RuntimeError(f"CreateProcessWithToken failed, {ctypes.WinError()}")

	def _createProcessAsUser(self):
		log.debug("Calling CreateProcessAsUser...")
		if not CreateProcessAsUser(
			self.token,
			None,
			self._cmdline,
			None,
			None,
			True,
			self._creationFlags,
			self._envBlock,
			self.cwd,
			byref(self._siEx.startupInfo),
			byref(self._pi),
		):
			raise RuntimeError(f"CreateProcessAsUser failed, {ctypes.WinError()}")


class PopenInAppContainerMixin(BasicPopen):
	appContainerName: str
	appContainerSidString: str
	appContainerCapabilities: list[str]
	appContainerPath: str

	def appContainerInit(self, appContainerName: str, appContainerCapabilities: list[str]):
		appContainerSid = makeAutoFree(PSID, FreeSid)()
		res = ctypes.windll.userenv.CreateAppContainerProfile(
			appContainerName,
			appContainerName,
			appContainerName,
			None,
			0,
			byref(appContainerSid),
		)
		if res == HRESULT_FROM_WIN32(winerror.ERROR_ALREADY_EXISTS):
			log.debug("AppContainer already exists")
		elif res < 0:
			raise RuntimeError(
				f"Failed to create AppContainer profile {appContainerName}, {ctypes.WinError()}",
			)
		if (
			ctypes.windll.userenv.DeriveAppContainerSidFromAppContainerName(
				appContainerName,
				byref(appContainerSid),
			)
			< 0
		):
			raise RuntimeError(
				f"Failed to derive AppContainer SID from name {appContainerName}, {ctypes.WinError()}",
			)
		appContainerSidString = makeAutoFree(LPWSTR, LocalFree)()
		if not ConvertSidToStringSid(appContainerSid, byref(appContainerSidString)):
			raise RuntimeError(f"Failed to convert AppContainer SID to string, {ctypes.WinError()}")
		appContainerPath = makeAutoFree(LPWSTR, CoTaskMemFree)()
		if (
			ctypes.windll.userenv.GetAppContainerFolderPath(appContainerSidString, byref(appContainerPath))
			< 0
		):
			raise RuntimeError(f"Failed to get AppContainer folder path, {ctypes.WinError()}")
		sc = SECURITY_CAPABILITIES()
		sc.AppContainerSid = appContainerSid
		sc._appContainerSidRef = appContainerSid  # prevent GC
		if appContainerCapabilities:
			capabilitySids = []
			for name in appContainerCapabilities:
				log.debug(f"Deriving capability SID for capability name: {name}...")
				groupSids = makeAutoFree(POINTER(PSID), LocalFree)()
				groupSidsCount = DWORD()
				appSids = makeAutoFree(POINTER(PSID), LocalFree)()
				appSidsCount = DWORD()
				if not DeriveCapabilitySidsFromName(
					name,
					byref(groupSids),
					byref(groupSidsCount),
					byref(appSids),
					byref(appSidsCount),
				):
					raise RuntimeError(
						f"Failed to derive capability SID for capability name {name}, {ctypes.WinError()}",
					)
				for i in range(groupSidsCount.value):
					psid = makeAutoFree(PSID, LocalFree)(groupSids[i])
					# capabilitySids.append(psid)
					sidString = makeAutoFree(LPWSTR, LocalFree)()
					if not ConvertSidToStringSid(psid, byref(sidString)):
						raise RuntimeError(f"Failed to convert capability SID to string, {ctypes.WinError()}")
					log.debug(f"  Derived capability group SID: {sidString.value}")
				for i in range(appSidsCount.value):
					psid = makeAutoFree(PSID, LocalFree)(appSids[i])
					capabilitySids.append(psid)
					sidString = makeAutoFree(LPWSTR, LocalFree)()
					if not ConvertSidToStringSid(psid, byref(sidString)):
						raise RuntimeError(f"Failed to convert capability SID to string, {ctypes.WinError()}")
					log.debug(f"  Derived capability app SID: {sidString.value}")
			capabilitiesBuf = (SID_AND_ATTRIBUTES * len(capabilitySids))()
			capabilitiesBuf._sidRefs = capabilitySids  # prevent GC
			for i, psid in enumerate(capabilitySids):
				capabilitiesBuf[i].Sid = psid
				capabilitiesBuf[i].Attributes = win32security.SE_GROUP_ENABLED
			sc.Capabilities = capabilitiesBuf
			sc._capabilitiesBufRef = capabilitiesBuf  # prevent GC
			sc.CapabilityCount = len(capabilitiesBuf)
		# self._addProcthreadAttribute(PROC_THREAD_ATTRIBUTE.SECURITY_CAPABILITIES, sc)
		self.appContainerName = appContainerName
		self.appContainerSidString = appContainerSidString.value
		self.appContainerCapabilities = appContainerCapabilities
		self.appContainerPath = appContainerPath.value
		self._appContainerSecurityCapabilities = sc
