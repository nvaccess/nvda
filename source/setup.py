from distutils.core import setup
import py2exe
from glob import glob

setup(
	name = "NVDA",
	windows = ["nvda.pyw"],
	options = {"py2exe": {"bundle_files": 3}},
	zipfile = None,
	data_files = [
		("dictionaries", glob("dictionaries/*.py")),
		("synthDrivers", glob("synthDrivers/*.py")),
		("appModules", glob("appModules/*.py*")),
	],
)
