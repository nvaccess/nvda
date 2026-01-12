import sys
import inspect
import os
import logging
import gettext
import tempfile
from winBindings.kernel32 import GetCurrentProcessId

old_factory = logging.getLogRecordFactory()
def record_factory(*args, **kwargs):
	record = old_factory(*args, **kwargs)
	frame = inspect.currentframe()
	count = 4
	while count > 0:
		if not frame.f_back:
			break
		frame = frame.f_back
		count -= 1
	try:
		record.name = frame.f_code.co_qualname
	except AttributeError:
		# co_qualname may be unavailable for some frames; in that case, keep the default record.name
		pass
	return record
logging.setLogRecordFactory(record_factory)

exeName = os.path.splitext(os.path.basename(sys.executable))[0]
pid = GetCurrentProcessId()
logPath = os.path.join(tempfile.gettempdir(), f"{exeName}.{pid}.log")
logging.basicConfig(
	filename=logPath,
	filemode="w",
	level=logging.DEBUG,
	format="%(levelname)s - %(module)s.%(name)s (%(asctime)s):\n%(message)s"
)
log = logging.getLogger(exeName)
# No comtypes debug logging
logging.getLogger("comtypes").setLevel(logging.INFO)
log.info(f"Logging initialized, log file: {logPath}")

try:
	gettext.install("nvda", names=["pgettext", "npgettext", "ngettext"])
	import core
	core.main()
except Exception:
	log.exception("Unhandled exception")
