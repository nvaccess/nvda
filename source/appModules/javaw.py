#appModules/javaw.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 NV Access Limited

"""Support for app specific modules for Java apps hosted by javaw.exe.
"""

import re
import appModuleHandler
from appModuleHandler import AppModule

RE_CMDLINE_CLASS = re.compile(r'(?:"[^"]+"|[^ ]+)(?: +-[^ "]+(?:"[^"]+")?)* +([^ ]+)')
def getAppNameFromHost(processId):
	# Some apps have launcher executables which launch javaw.exe to run the app.
	# In this case, the parent process will usually be the launcher.
	proc = appModuleHandler.getWmiProcessInfo(processId)
	parent = proc.parentProcessId
	if parent:
		name = appModuleHandler.getAppNameFromProcessID(parent)
		if name and name not in ("explorer", "cmd"):
			# The parent isn't a shell, so it's probably a launcher.
			return name

	# Try getting the class from the command line.
	cmd = proc.CommandLine
	if not cmd:
		raise LookupError
	m = RE_CMDLINE_CLASS.match(cmd)
	if not m:
		raise LookupError
	return "javaw_" + m.group(1).replace(".", "_")
