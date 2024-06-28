#nvdaBuiltin.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited

"""Provides access to built-in NVDA modules where they have been overridden by third party modules.
This should only be used by overriding modules to extend the built-in module.
For example, if an add-on overrides the skype app module but wants to access the built-in module,
it can do this by importing nvdaBuiltin.appModules.skype.
"""

import os

__path__ = [os.path.dirname(__file__)]
