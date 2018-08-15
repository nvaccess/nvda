#validate.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2018 NV Access Limited, Babbage B.V., Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""
Module to provide backwards compatibility with add-ons that use the configobj validate module.
Add-ons should be changed to use configobj.validate instead.
"""

from configobj.validate import *
import warnings

warnings.warn("Importing validate directly is deprecated. Please use configobj.validate instead", DeprecationWarning, stacklevel=2)
