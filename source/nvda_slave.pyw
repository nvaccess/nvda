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

	except Exception, e:
		sys.exit(e)

if __name__ == "__main__":
	main()