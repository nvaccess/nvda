from types import SimpleNamespace
import sys
import inspect
import threading
import os
import subprocess
import argparse
import secureProcess
from secureProcess.token import integrityLevels, logonTypes

import logging

old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
	record = old_factory(*args, **kwargs)
	frame = inspect.currentframe()
	count = 5
	while count > 0:
		if not frame.f_back:
			break
		frame = frame.f_back
		count -= 1
	record.qualname = frame.f_code.co_qualname.removesuffix('.__init__')
	mod = os.path.splitext(os.path.basename(frame.f_code.co_filename))[0]
	record.module = mod
	return record

logging.setLogRecordFactory(record_factory)

logging.basicConfig(
	level=logging.DEBUG,
	format="%(levelname)s %(module)s.%(qualname)s: %(message)s"
)
log = logging.getLogger()
sys.modules['logHandler'] = SimpleNamespace(log=log)


def readToStdout(stream):
	while True:
		data = stream.readline()
		if not data:
			break
		data = data.decode("utf-8", errors="replace")
		print(data, end="")

def main():
	parser = argparse.ArgumentParser(description="Launch a process with a restricted token")
	parser.add_argument("-il", "--integrity-level", choices=integrityLevels.keys(), help="Integrity level for the restricted token", default=None)
	parser.add_argument("-r", "--restrict-sids", help="Restricted SIDs", action="store_true")
	parser.add_argument("-ru", "--retain-user-in-restricted-token", help="Retain user SID in restricted token", action="store_true")
	parser.add_argument("-p", "--remove-privileges", help="Remove privileges from the token", action="store_true")
	parser.add_argument("-re", "--remove-elevation", help="If the current token is elevated, obtain an unelevated interactive user token from the shell instead", action="store_true")
	parser.add_argument("-u", "--username", help="Run the process as the specified user", default=None)
	parser.add_argument("-d", "--domain", help="Domain for the specified user", default=".")
	parser.add_argument("-pw", "--password", help="Password for the specified user", default="")
	parser.add_argument("-lt", "--logon-type", choices=logonTypes.keys(), help="Logon type to use when running as a different user", default="interactive")
	parser.add_argument("-td", "--temp-desktop", help="Create a temporary desktop for the process", action="store_true")
	parser.add_argument("-tw", "--temp-window-station", help="Create a temporary window station for the process", action="store_true")
	parser.add_argument("-he", "--hide-critical-error-dialogs", help="Hide critical error dialogs in the launched process", action="store_true")
	parser.add_argument("-ui", "--ui-restrictions", help="Apply UI restrictions to the launched process", action="store_true")
	parser.add_argument("-acn", "--app-container-name", help="Run the process in the specified AppContainer", default=None)
	parser.add_argument("-acc", "--app-container-capabilities", help="An appContainer Capability to add to the AppContainer. Can be specified multiple times", action="append", default=[])
	parser.add_argument("-nw", "--no-window", help="Create the process without a window", action="store_true")
	parser.add_argument("-rh", "--redirect-handles", help="Redirect stdin/stdout/stderr handles", action="store_true")
	parser.add_argument("-py", "--python", help="Use the current Python interpreter to launch the process", action="store_true")
	parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute with restricted token")
	args = parser.parse_args()
	command = args.command.copy()
	if args.python:
		log.debug("Using current Python interpreter to launch the process")
		command.insert(0, sys.executable)
	p = secureProcess.SecurePopen(
		command,
		stdin=subprocess.PIPE if args.redirect_handles else None,
		stdout=subprocess.PIPE if args.redirect_handles else None,
		stderr=subprocess.STDOUT	 if args.redirect_handles else None,
		integrityLevel=args.integrity_level,
		removePrivileges=args.remove_privileges,
		removeElevation=args.remove_elevation,
		restrictToken=args.restrict_sids,
		retainUserInRestrictedToken=args.retain_user_in_restricted_token,
		username=args.username,
		domain=args.domain,
		password=args.password,
		logonType=args.logon_type,
		isolateWindowStation=args.temp_window_station,
		isolateDesktop=args.temp_desktop,
		killOnDelete=True,
		startSuspended=True,
		hideCriticalErrorDialogs=args.hide_critical_error_dialogs,
		createNoWindow=args.no_window,
		applyUIRestrictions=args.ui_restrictions,
		appContainerName=args.app_container_name,
		appContainerCapabilities=args.app_container_capabilities,
	)
	print(f"Launched process PID: {p.pid}\n")
	input("Press Enter to resume the process...")
	p.resume()
	if args.redirect_handles:
		p.interact()
	else:
		p.wait()
	print(f"\nProcess exited with code: {p.returncode}")

if __name__ == "__main__":
	main()
