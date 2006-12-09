from distutils.core import setup
import py2exe
from glob import glob
from versionInfo import *

setup(
	name = name,
	version=version,
	description=description,
	maintainer=maintainer,
	maintainer_email=maintainer_email,
	url=url,
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
		("documentation", glob("../*.txt")),
		("comInterfaces", glob("comInterfaces/*.py*")),
		("synthDrivers", glob("synthDrivers/*.py*")),
		("appModules", glob("appModules/*.py*")),
	],
)
