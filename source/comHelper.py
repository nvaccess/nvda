#comHelper.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities to help with issues related to COM.
"""

import subprocess
import comtypes.client.dynamic
from comtypes import IUnknown
from comtypes.automation import IDispatch
import oleacc
import config

def _lresultFromGetActiveObject(progid, dynamic):
	o = comtypes.client.GetActiveObject(progid, dynamic=dynamic)
	if not isinstance(o, IUnknown):
		o = o._comobj
	return oleacc.LresultFromObject(0, o)

def getActiveObject(progid, dynamic=False):
	"""Get an active COM object, handling privilege issues.
	This is similar to comtypes.client.GetActiveObject
	except that it can retrieve objects from normal processes when NVDA is running with uiAccess.
	"""
	# TODO: Try in our own process first; no point spawning a process when we don't need to.
	p = subprocess.Popen((config.SLAVE_FILENAME, "comGetActiveObject", progid, "%d" % dynamic),
		stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	try:
		# FIXME: Throw better exception for COM error in slave.
		lres = int(p.stdout.readline())
		o = oleacc.ObjectFromLresult(lres, 0,
			IDispatch if dynamic else IUnknown)
		if dynamic:
			o = comtypes.client.dynamic.Dispatch(o)
		return o
	finally:
		# This will cause EOF for the waiting process, which will then exit.
		p.stdin.close()
		p.wait()
		p.stdout.close()
