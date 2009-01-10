#NVDAObjects/IAccessible/edit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from . import IAccessible
from NVDAObjects.edit import *

#Create IAccessible versions of some edit window NVDAObjects using mixins
for cls in (Edit,RichEdit,RichEdit20,RichEdit30,RichEdit50):
	globals()[cls.__name__]=type(cls.__name__,(cls,IAccessible),{})
