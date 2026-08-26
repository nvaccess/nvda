# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Localization startup test helpers."""

from glob import glob
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn


_builtIn: BuiltIn = BuiltIn()


def get_source_locale_codes() -> list[str]:
	"""Return source locale codes from source/locale."""
	nvdaPoFiles = glob(
		str(Path(__file__).resolve().parents[3] / "source" / "locale" / "*" / "LC_MESSAGES" / "nvda.po"),
	)
	if not nvdaPoFiles:
		raise AssertionError("Unable to find locale directory under source/locale")

	localeCodes = sorted(Path(path).parents[1].name for path in nvdaPoFiles if Path(path).is_file())
	_builtIn.should_be_true(bool(localeCodes), msg="No locale directories found under source/locale")
	return localeCodes
