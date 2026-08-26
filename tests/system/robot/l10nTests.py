# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Localization startup test helpers."""

from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn


_builtIn: BuiltIn = BuiltIn()


def get_source_locale_codes() -> list[str]:
	"""Return source locale codes from source/locale."""
	localesDir = Path("source") / "locale"
	if not localesDir.is_dir():
		raise AssertionError(f"Unable to find locale directory: {localesDir}")

	localeCodes = sorted(path.name for path in localesDir.iterdir() if path.is_dir())
	_builtIn.should_be_true(bool(localeCodes), msg="No locale directories found under source/locale")
	return localeCodes
