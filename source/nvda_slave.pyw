"""NVDA slave process
Performs miscellaneous tasks which need to be performed in a separate process.
"""

import sys
import os
if hasattr(sys, "frozen"):
	# Error messages (which are only for debugging) should not cause the py2exe log message box to appear.
	sys.stderr = sys.stdout

def main():
	try:
		action = sys.argv[1]
	except IndexError:
		sys.exit("No action")
	args = sys.argv[2:]

	try:
		if action == "service_NVDALauncher":
			import nvda_service
			nvda_service.nvdaLauncher()
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
			if not os.path.isdir(path):
				os.makedirs(path)
			import shellapi
			import winUser
			shellapi.ShellExecute(0,None,path,None,None,winUser.SW_SHOWNORMAL)
		else:
			raise ValueError("No such action")

	except Exception, e:
		sys.exit(e)

if __name__ == "__main__":
	main()
