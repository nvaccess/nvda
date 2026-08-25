# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import sys  # noqa: I001


# This file wraps buildVersion.py from NVDA's own source directory,
# Exposing the symbols required by pyproject.toml and setup-runtime.py in this particular sub-project.

sys.path.insert(0, "../../source")
try:
	from buildVersion import (  # noqa: I001
		version_detailed,
		formatBuildVersionString,
		name,
		publisher,
		version,
	)
finally:
	del sys.path[0]

__all__ = [
	"formatBuildVersionString",
	"name",
	"publisher",
	"version",
	"version_detailed",
]
