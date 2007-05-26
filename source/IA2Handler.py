#IAccessibleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypesClient
import ctypes

IServiceProvider=comtypesClient.GetModule('lib/ServProv.tlb').IServiceProvider
IA2Lib=comtypesClient.GetModule('lib/ia2.tlb')

def IA2FromMSAA(pacc):
	try:
		s=pacc.QueryInterface(IServiceProvider)
		i=s.QueryService(ctypes.byref(IA2Lib.IAccessible2._iid_),ctypes.byref(IA2Lib.IAccessible2._iid_))
		newPacc=ctypes.POINTER(IA2Lib.IAccessible2)(i)
		return newPacc
	except:
		return None
