# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Localization startup test helpers."""

from glob import glob as _glob
from pathlib import Path as _Path

from robot.libraries.BuiltIn import BuiltIn as _BuiltIn

_builtIn: _BuiltIn = _BuiltIn()


def append_failed_locale(failed_locales: list[str], locale_code: str, start_message: str) -> list[str]:
	"""Return the failed-locale list with a new entry appended."""
	return [*failed_locales, f"{locale_code}: {start_message}"]


def get_source_locale_codes() -> list[str]:
	"""Return source locale codes from source/locale."""

	nvdaPoFiles = _glob(
		str(_Path(__file__).resolve().parents[3] / "source" / "locale" / "*" / "LC_MESSAGES" / "nvda.po"),
	)
	if not nvdaPoFiles:
		raise AssertionError("Unable to find locale directory under source/locale")

	localeCodes = sorted(_Path(path).parents[1].name for path in nvdaPoFiles if _Path(path).is_file())
	_builtIn.should_be_true(bool(localeCodes), msg="No locale directories found under source/locale")
	return localeCodes
