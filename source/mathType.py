# -*- coding: UTF-8 -*-
# mathType.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


"""Utilities for working with MathType.
"""

import winreg
import ctypes
import mathPres

def _getDllPath():
	with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Design Science\DSMT6\Directories", 0, winreg.KEY_WOW64_32KEY | winreg.KEY_QUERY_VALUE) as key:
		return winreg.QueryValueEx(key, "AppSystemDir32")[0] + "\\MT6.dll"

lib = ctypes.windll[_getDllPath()]

def getMathMl(oleFormat, runForConversion=True):
	"""Get MathML from a MathType OLEFormat object.
	"""
	if runForConversion:
		oleFormat.DoVerb(2) # "RunForConversion"
	mt = oleFormat.object._comobj
	length = ctypes.c_long()
	# 2 is get MathML
	try:
		if lib.MTGetLangStrFromEqn(mt, 2, None, ctypes.byref(length)) != 0:
			raise RuntimeError
		mathMl = (ctypes.c_char * length.value)()
		if lib.MTGetLangStrFromEqn(mt, 2, ctypes.byref(mathMl), ctypes.byref(length)) != 0:
			raise RuntimeError
	finally:
		# 1 is OLECLOSE_NOSAVE
		lib.MTCloseOleObject(1, mt)
	return mathPres.stripExtraneousXml(
		mathMl.value.decode('utf8')
	)
