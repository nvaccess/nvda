#nvda_slave.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2009-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA slave process
Performs miscellaneous tasks which need to be performed in a separate process.
"""

import gettext
import locale
#Localization settings
try:
	gettext.translation('nvda',localedir='locale',languages=[locale.getdefaultlocale()[0]]).install(True)
except:
	gettext.install('nvda',unicode=True)

import pythonMonkeyPatches

import sys
import os
import versionInfo
import logHandler
if hasattr(sys, "frozen"):
	# Error messages (which are only for debugging) should not cause the py2exe log message box to appear.
	sys.stderr = sys.stdout
	#Many functions expect  the current directory to be where slave is located (#2391) 
	os.chdir(sys.prefix)

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
				ur"%s\nvda.exe"%sys.exec_prefix.decode("mbcs"),
				subprocess.list2cmdline(args).decode("mbcs"),
				None,winUser.SW_SHOWNORMAL)
		elif action=="setNvdaSystemConfig":
			import config
			config._setSystemConfig(args[0].decode('mbcs'))
		elif action == "config_setStartOnLogonScreen":
			enable = bool(int(args[0]))
			import config
			config._setStartOnLogonScreen(enable)
		elif action == "explore_userConfigPath":
			import config
			path=config.getUserDefaultConfigPath()
			if not path:
				raise ValueError("no user default config path")
			config.initConfigPath(path)
			import shellapi
			import winUser
			shellapi.ShellExecute(0,None,path,None,None,winUser.SW_SHOWNORMAL)
		elif action == "addons_installAddonPackage":
			try:
				addonPath=unicode(args[0], "mbcs")
			except IndexError:
				raise ValueError("Addon path was not provided.")
			#Load nvdaHelperRemote.dll but with an altered search path so it can pick up other dlls in lib
			import ctypes
			h=ctypes.windll.kernel32.LoadLibraryExW(os.path.abspath(os.path.join(u"lib",versionInfo.version,u"nvdaHelperRemote.dll")),0,0x8)
			remoteLib=ctypes.WinDLL("nvdaHelperRemote",handle=h)
			ret = remoteLib.nvdaControllerInternal_installAddonPackageFromPath(addonPath)
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
				raw_input()
			except EOFError:
				pass
		else:
			raise ValueError("No such action")

	except installer.RetriableFailure:
		logHandler.log.error("Task failed, try again",exc_info=True)
		sys.exit(2)
	except Exception, e:
		logHandler.log.error("slave error",exc_info=True)
		sys.exit(1)

if __name__ == "__main__":
	logHandler.initialize(True)
	logHandler.log.setLevel(0)
	import languageHandler
	languageHandler.setLanguage("Windows")
	main()
