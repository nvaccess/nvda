#nvda_slave.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2009-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA slave process
Performs miscellaneous tasks which need to be performed in a separate process.
"""

import sys
import os
import globalVars
import monkeyPatches.comtypesMonkeyPatches

# Ensure that slave uses generated comInterfaces by adding our comInterfaces to `comtypes.gen` search path.
monkeyPatches.comtypesMonkeyPatches.appendComInterfacesToGenSearchPath()


if hasattr(sys, "frozen"):
	# Error messages (which are only for debugging) should not cause the py2exe log message box to appear.
	sys.stderr = sys.stdout
	globalVars.appDir = sys.prefix
else:
	globalVars.appDir = os.path.abspath(os.path.dirname(__file__))

# #2391: some functions may still require the current directory to be set to NVDA's app dir
os.chdir(globalVars.appDir)


import gettext
import locale
#Localization settings
try:
	gettext.translation(
		'nvda',
		localedir=os.path.join(globalVars.appDir, 'locale'),
		languages=[locale.getdefaultlocale()[0]]
	).install()
except:
	gettext.install('nvda')


import logHandler


def getNvdaHelperRemote():
	import buildVersion
	import ctypes
	import winKernel
	# Load nvdaHelperRemote.dll but with an altered search path so it can pick up other dlls in lib
	h = winKernel.kernel32.LoadLibraryExW(
		os.path.join(globalVars.appDir, "lib", buildVersion.version, "nvdaHelperRemote.dll"),
		0,
		# Using an altered search path is necessary here
		# As NVDAHelperRemote needs to locate dependent dlls in the same directory
		# such as IAccessible2proxy.dll.
		winKernel.LOAD_WITH_ALTERED_SEARCH_PATH
	)
	remoteLib = ctypes.WinDLL("nvdaHelperRemote", handle=h)
	return remoteLib


def main():
	import installer
	try:
		action = sys.argv[1]
	except IndexError:
		sys.exit("No action")
	args = sys.argv[2:]

	try:
		if action=="install":
			installer.install(bool(int(args[0])),bool(int(args[1])))
		elif action=="unregisterInstall":
			import installer
			installer.unregisterInstallation()
		elif action=="fixCOMRegistrations":
			import COMRegistrationFixes
			COMRegistrationFixes.fixCOMRegistrations()
		elif action=="launchNVDA":
			import subprocess
			import shellapi
			import winUser
			shellapi.ShellExecute(0,None,
				r"%s\nvda.exe"%sys.prefix,
				subprocess.list2cmdline(args),
				None,winUser.SW_SHOWNORMAL)
		elif action=="setNvdaSystemConfig":
			import config
			config._setSystemConfig(args[0])
		elif action == "config_setStartOnLogonScreen":
			enable = bool(int(args[0]))
			import config
			config._setStartOnLogonScreen(enable)
		elif action == "explore_userConfigPath":
			ret = getNvdaHelperRemote().nvdaControllerInternal_openConfigDirectory()
			if ret != 0:  # NVDA is not running
				import systemUtils
				systemUtils.openDefaultConfigurationDirectory()
		elif action == "addons_installAddonPackage":
			try:
				addonPath=args[0]
			except IndexError:
				raise ValueError("Addon path was not provided.")
			ret = getNvdaHelperRemote().nvdaControllerInternal_installAddonPackageFromPath(addonPath)
			if ret != 0:
				import winUser
				winUser.MessageBox(0,
				# Translators: the message that is shown when the user tries to install an add-on from windows explorer and NVDA is not running.
				_("Cannot install NVDA add-on from {path}.\n"
				"You must be running NVDA to be able to install add-ons.").format(path=addonPath),
				0, winUser.MB_ICONERROR)
		elif action == "comGetActiveObject":
			import comHelper
			# py2exe scraps sys.stdout.
			sys.__stdout__.write("%s\n" %
				comHelper._lresultFromGetActiveObject(args[0], bool(int(args[1]))))
			sys.__stdout__.flush()
			try:
				input()
			except EOFError:
				pass
		else:
			raise ValueError("No such action")

	except installer.RetriableFailure:
		logHandler.log.error("Task failed, try again",exc_info=True)
		sys.exit(2)
	except Exception as e:
		logHandler.log.error("slave error",exc_info=True)
		sys.exit(1)

if __name__ == "__main__":
	# Initialize remote logging back to NVDA
	logHandler.initialize(True)
	# Log at the most detailed level, and NVDA will filter it using its own level setting.
	logHandler.log.setLevel(logHandler.log.DEBUG)
	import languageHandler
	languageHandler.setLanguage("Windows")
	main()
