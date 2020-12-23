# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Functions useful when building NVDA"""


def installCallback(package):
	import sys
	import subprocess
	subprocess.check_call(
		[sys.executable, "-m", "pip", "install", str(package)]
	)
	import importlib
	import pkg_resources
	# Evenn though this is quite ugly there is no other way to refresh list of available packages.
	importlib.reload(pkg_resources)
	return pkg_resources.working_set.find(
		# `resolve` considers installation to be succesfull only when installed package is
		# returned from the callback.
		list(pkg_resources.parse_requirements(str(package)))[0]
	)


def requestPackage(requirementsString):
	import pkg_resources
	pkg_resources.working_set.resolve(
		pkg_resources.parse_requirements(requirementsString),
		installer=installCallback
	)
