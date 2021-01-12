# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2013-2021 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Set up the Python environment when running from source.
"""

import sys
import os

# Get the path to the top of the repo; i.e. where include and miscDeps are.
TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def pythonPackagesDir() -> str:
	"""Returns path to the directory in which packages installed using pip should  be placed.
	The directory would be created if it does not exist.
	"""
	PACKAGES_DIR = os.path.abspath(os.path.join(TOP_DIR, "installed_packages"))
	os.makedirs(PACKAGES_DIR, exist_ok=True)
	return PACKAGES_DIR


# Directories containing Python modules included in git submodules.
PYTHON_DIRS = (
	os.path.join(TOP_DIR, "include", "pyserial"),
	os.path.join(TOP_DIR, "include", "comtypes"),
	os.path.join(TOP_DIR, "include", "configobj", "src"),
	os.path.join(TOP_DIR, "include", "wxPython"),
	os.path.join(TOP_DIR, "miscDeps", "python"),
	pythonPackagesDir(),
)


def expandPythonPath() -> None:
	"""Adds `PYTHON_DIRS` to the `PythonPath` of the current interpreter
	raising appropriate exceptions if any  of the dirs does not exist."""
	# Check for existance of each Python dir
	for path in PYTHON_DIRS:
		if not os.path.exists(path):
			raise OSError("Path %s does not exist. Perhaps try running git submodule update --init" % path)
	# sys.path[0] will always be the current dir, which should take precedence.
	# Insert our include paths after that.
	sys.path[1:1] = PYTHON_DIRS
