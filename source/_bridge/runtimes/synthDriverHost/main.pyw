import sys
import os
import logging
import gettext
import tempfile

exeName = os.path.splitext(os.path.basename(sys.executable))[0]
logPath = os.path.join(tempfile.gettempdir(), f"{exeName}.log")
logging.basicConfig(
	filename=logPath,
	filemode="w",
	level=logging.DEBUG,
	format="%(levelname)s - %(name)s (%(asctime)s):\n%(message)s"
)
log = logging.getLogger(exeName)
# No comtypes debug logging
logging.getLogger("comtypes").setLevel(logging.INFO)

try:
	gettext.install("nvda", names=["pgettext", "npgettext", "ngettext"])
	import synthDriverHost
	synthDriverHost.main()
except Exception:
	log.exception("Unhandled exception")
