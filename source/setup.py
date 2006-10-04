from distutils.core import setup
import py2exe
from glob import glob

setup(
	name = "NVDA",
	version="0.1.0",
	description="A free and open-source screen reader for MS Windows", 
	maintainer="Michael Curran",
	maintainer_email="mick@kulgan.net",
	url="http://www.kulgan.net/nvda/",
	classifiers=[
'Development Status :: 3 - Alpha',
'Environment :: Win32 (MS Windows)',
'Topic :: Adaptive Technologies'
'Intended Audience :: Developers',
'Intended Audience :: End Users/Desktop',
'License :: OSI Approved :: GNU General Public License (GPL)',
'Natural Language :: English',
'Programming Language :: Python',
'Operating System :: Microsoft :: Windows',
],
	windows = ["nvda.pyw"],
	options = {"py2exe": {"bundle_files": 3}},
	zipfile = None,
	data_files = [
		("dictionaries", glob("dictionaries/*.py")),
		("synthDrivers", glob("synthDrivers/*.py")),
		("appModules", glob("appModules/*.py*")),
	],
)
