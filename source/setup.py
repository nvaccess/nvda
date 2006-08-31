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
		("", glob("synth_*.py*")),
		("appModules", glob("appModules/*.py*")),
		("waves", glob("waves/*.wav")),
	],
)
