#nvda_eoaProxy.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA proxy process for Ease of Access in Windows Vista/7.
This version of Ease of Access terminates ATs on every desktop switch,
but this is bad for NVDA, as state is lost and cleanup isn't performed.
This process runs while NVDA is running so EoA knows NVDA is running.
However, when EoA kills this process, it doesn't affect NVDA.
"""

import sys
import os
import ctypes
import winUser
import winKernel

def getNvdaProcess():
	try:
		window = winUser.FindWindow(u"wxWindowClassNR", u"NVDA")
	except WindowsError:
		return None
	pid = winUser.getWindowThreadProcessID(window)[0]
	return winKernel.openProcess(winKernel.SYNCHRONIZE, False, pid)

UOI_NAME = 2
def isSecureDesktop():
	desktop = ctypes.windll.user32.OpenInputDesktop(0, False, 0)
	name = ctypes.create_unicode_buffer(256)
	ctypes.windll.user32.GetUserObjectInformationW(desktop, UOI_NAME, ctypes.byref(name), ctypes.sizeof(name), None)
	ctypes.windll.user32.CloseDesktop(desktop)
	return name.value == "Winlogon"

def waitForNvdaStart():
	# Wait up to 10 seconds for NVDA to start.
	for attempt in range(11):
		process = getNvdaProcess()
		if process:
			return process
		import time
		time.sleep(1)
	return None

def main():
	process = getNvdaProcess()
	if not process:
		if isSecureDesktop():
			import subprocess
			subprocess.Popen((os.path.join(sys.prefix, "nvda.exe"), "--ease-of-access"))
		process = waitForNvdaStart()
	if not process:
		return
	# Wait for NVDA to exit.
	winKernel.waitForSingleObject(process, winKernel.INFINITE)
	winKernel.closeHandle(process)

if __name__ == "__main__":
	main()
