# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module is not a Robot Framework library itself, it provides a way to get an instance of a library
(importing it if necessary first). Using RobotFramework can manage the lifetimes of libraries so the libraries
can configure themselves to be created per test / per suite etc.
"""
from typing import Any


def _getLib(libraryName: str, *args) -> Any:
	"""Tries to get existing instance first, on failure imports the library
	The library instance from Robot is used in order to access the same state that may be present on
	stateful libraries.
	"""
	from . import _nvdaSpyAlias
	if libraryName == _nvdaSpyAlias:
		raise AssertionError(f"Don't use _getLib for {_nvdaSpyAlias}, instead use 'NvdaLib.getSpyLib()'")
	from robot.libraries.BuiltIn import BuiltIn
	builtIn: BuiltIn = BuiltIn()
	lib = None
	try:
		lib = builtIn.get_library_instance(libraryName)
	except RuntimeError:
		pass
	if lib is None:
		builtIn.import_library(libraryName, *args)
		lib = builtIn.get_library_instance(libraryName)
		if lib is None:
			raise AssertionError(f"Unable to get library: {libraryName}")
	return lib
