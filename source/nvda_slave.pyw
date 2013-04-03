"""NVDA slave process
Performs miscellaneous tasks which need to be performed in a separate process.
"""

import pythonMonkeyPatches

import sys
import os
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
		if action == "service_NVDALauncher":
			import nvda_service
			nvda_service.nvdaLauncher()
		elif action=="install":
			installer.install(bool(int(args[0])),bool(int(args[1])))
		elif action=="unregisterInstall":
			import installer
			installer.unregisterInstallation()
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
		elif action == "installer_installService":
			import nvda_service
			nvdaDir = os.path.dirname(sys.argv[0])
			nvda_service.installService(nvdaDir)
			nvda_service.startService()
		elif action == "installer_uninstallService":
			import nvda_service
			try:
				nvda_service.stopService()
			except:
				pass
			nvda_service.removeService()
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
			h=ctypes.windll.kernel32.LoadLibraryExW(os.path.abspath(ur"lib\nvdaHelperRemote.dll"),0,0x8)
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
