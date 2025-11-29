import inspect
import sys
import threading
import os
import subprocess
import argparse
import secureProcess
from secureProcess.token import integrityLevels

import logging

old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
	record = old_factory(*args, **kwargs)
	frame = inspect.currentframe().f_back.f_back.f_back.f_back
	record.qualname = frame.f_code.co_qualname.removesuffix('.__init__')
	return record

logging.setLogRecordFactory(record_factory)

logging.basicConfig(
	level=logging.DEBUG,
	format="%(levelname)s %(name)s.%(qualname)s: %(message)s"
)


def readToStdout(stream):
	while True:
		data = stream.readline()
		if not data:
			break
		data = data.decode("utf-8", errors="replace")
		print(data, end="")

def main():
	parser = argparse.ArgumentParser(description="Launch a process with a restricted token")
	parser.add_argument(
		"-il", "--integrity-level",
		choices=integrityLevels.keys(),
		help="Integrity level for the restricted token",
		default=None
	)
	parser.add_argument("-r", "--restrict-sids", help="Restricted SIDs", action="store_true")
	parser.add_argument("-p", "--remove-privileges", help="Remove privileges from the token", action="store_true")
	parser.add_argument("-d", "--disable-dangerous-sids", help="Disable dangerous SIDs in the token", action="store_true")
	parser.add_argument("-s", "--service-logon", help="Use the LocalService account to create the token", action="store_true")
	parser.add_argument("-td", "--temp-desktop", help="Create a temporary desktop for the process", action="store_true")
	parser.add_argument("-tw", "--temp-window-station", help="Create a temporary window station for the process", action="store_true")
	parser.add_argument("-b", "--block", help="Wait for the launched process to exit", action="store_true")
	parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute with restricted token")
	parser.add_argument("-he", "--hide-critical-error-dialogs", help="Hide critical error dialogs in the launched process", action="store_true")
	args = parser.parse_args()
	p = secureProcess.SecurePopen(
		args.command,
		stdin=subprocess.PIPE if args.block else None,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		integrityLevel=args.integrity_level,
		removePrivileges=args.remove_privileges,
		allowUser=not args.restrict_sids,
		disableDangerousSids=args.disable_dangerous_sids,
		runAsLocalService=args.service_logon,
		isolateWindowStation=args.temp_window_station,
		isolateDesktop=args.temp_desktop,
		killOnDelete=True,
		startSuspended=True,
		hideCriticalErrorDialogs=args.hide_critical_error_dialogs,
	)
	print(f"Launched process PID: {p.pid}\n")
	input("Press Enter to resume the process...")
	p.resume()
	if args.block:
		p.interact()
	else:
		rt = threading.Thread(target=readToStdout, args=(p.stdout,))
		rt.start()
		input("Press Enter to continue...\n")
		if p.poll() is None:
			p.job.close()
		rt.join()
		p.wait()
	print(f"\nProcess exited with code: {p.returncode}")

if __name__ == "__main__":
	main()
