#sourceEnv.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Set up the Python environment when running from source.
"""

import sys
import os

# Get the path to the top of the repo; i.e. where include and miscDeps are.
top = os.path.dirname(os.path.dirname(__file__))
# sys.path[0] will always be the current dir, which should take precedence.
# Insert our include paths after that.
sys.path[1:1] = (
	os.path.join(top, "include", "pyserial"),
	os.path.join(top, "miscDeps", "python"),
)
