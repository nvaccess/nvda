# comHelper.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2013 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities to help with issues related to COM."""

import subprocess
import ctypes
import comtypes.client.dynamic
from comtypes import IUnknown
from comtypes.automation import IDispatch
import oleacc
import config

MK_E_UNAVAILABLE = -2147221021
CO_E_CLASSSTRING = -2147221005


def _lresultFromGetActiveObject(progid, dynamic):
	o = comtypes.client.GetActiveObject(progid, dynamic=dynamic)
	if not isinstance(o, IUnknown):
		o = o._comobj
	return oleacc.LresultFromObject(0, o)


def getActiveObject(progid, dynamic=False, appModule=None):
	"""Get an active COM object, handling privilege issues.
	This is similar to comtypes.client.GetActiveObject
	except that it can retrieve objects from normal processes when NVDA is running with uiAccess.
	"""
	if appModule:
		if not appModule.helperLocalBindingHandle:
			raise ValueError("appModule does not have a binding handle")
		import NVDAHelper

		p = ctypes.POINTER(comtypes.IUnknown)()
		res = NVDAHelper.localLib.nvdaInProcUtils_getActiveObject(
			appModule.helperLocalBindingHandle,
			progid,
			ctypes.byref(p),
		)
		if res != 0:
			raise ctypes.WinError(res)
		if not p:
			raise RuntimeError("NULL IUnknown pointer")
		if dynamic:
			return comtypes.client.dynamic.Dispatch(p.QueryInterface(IDispatch))
		else:
			return comtypes.client.GetBestInterface(p)
	try:
		return comtypes.client.GetActiveObject(progid, dynamic=dynamic)
	except WindowsError as e:
		if e.winerror not in (MK_E_UNAVAILABLE, CO_E_CLASSSTRING):
			# This isn't related to privileges.
			raise
	p = subprocess.Popen(
		(config.SLAVE_FILENAME, "comGetActiveObject", progid, "%d" % dynamic),
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
	)
	try:
		try:
			lres = int(p.stdout.readline())
		except ValueError:
			raise RuntimeError("Helper process unable to get object; see log for details")
		o = oleacc.ObjectFromLresult(
			lres,
			0,
			IDispatch if dynamic else IUnknown,
		)
		if dynamic:
			o = comtypes.client.dynamic.Dispatch(o)
		return o
	finally:
		# This will cause EOF for the waiting process, which will then exit.
		p.stdin.close()
		p.wait()
		p.stdout.close()
