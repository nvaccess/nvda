# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2013-2020 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Set up the Python environment when running from source.
"""

import sys
import os

# Get the path to the top of the repo; i.e. where include and miscDeps are.
TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Directories containing Python modules included in git submodules.
PYTHON_DIRS = (
	os.path.join(TOP_DIR, "miscDeps", "python"),
)

#Check for existance of each Python dir
for path in PYTHON_DIRS:
	if not os.path.exists(path):
		raise OSError("Path %s does not exist. Perhaps try running git submodule update --init"%path)

# sys.path[0] will always be the current dir, which should take precedence.
# Insert our include paths after that.
sys.path[1:1] = PYTHON_DIRS
