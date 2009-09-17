#NVDAObjects/placeholder.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import controlTypes
from . import NVDAObject

class Placeholder(NVDAObject):
	"""An NVDAObject which serves as a placeholder when it does not make sense to present a real object.
	"""
	processID = 0
	role = controlTypes.ROLE_PLACEHOLDER

	@classmethod
	def findBestClass(cls, clsList, kwargs):
		clsList.append(cls)
		return clsList, kwargs

	def __init__(self, **kwargs):
		self.__dict__.update(**kwargs)

def NoFocus():
	return Placeholder(name=_("no focus"))

def SecureDesktop():
	return Placeholder(name=_("secure desktop"))
