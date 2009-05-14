"""NVDA slave process
Performs miscellaneous tasks which need to be performed in a separate process.
"""

import sys

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
		else:
			raise ValueError("No such action")

	except Exception, e:
		sys.exit(e)

if __name__ == "__main__":
	main()