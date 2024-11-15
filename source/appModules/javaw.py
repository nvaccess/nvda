# appModules/javaw.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2014 NV Access Limited

"""Support for app specific modules for Java apps hosted by javaw.exe."""

import os
import shlex
import appModuleHandler


def _getEntryPoint(cmd):
	cmd = iter(shlex.split(cmd))
	# First argument is the executable.
	next(cmd)
	for arg in cmd:
		if arg in ("-cp", "-classpath"):
			# This option consuems the next argument.
			next(cmd)
			continue
		if arg.startswith("-jar"):
			# Next argument is the jar. Remove the extension.
			return os.path.splitext(next(cmd))[0]
		if arg.startswith("-"):
			continue
		if not arg:
			continue
		# Class.
		return arg
	raise LookupError


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

	# Try getting the class/jar from the command line.
	cmd = proc.CommandLine
	if not cmd:
		raise LookupError
	try:
		return "javaw_" + _getEntryPoint(cmd).replace(".", "_")
	except:  # noqa: E722
		raise LookupError
