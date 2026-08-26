# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Localization startup test helpers."""

from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn
import NvdaLib as _NvdaLib


_builtIn: BuiltIn = BuiltIn()
_nvdaRobot = _builtIn.get_library_instance("NvdaLib")


def _getSourceLocaleCodes() -> list[str]:
	localesDir = Path("source") / "locale"
	if not localesDir.is_dir():
		raise AssertionError(f"Unable to find locale directory: {localesDir}")

	# Match the user request directly: run startup checks for each language folder in source/locale.
	return sorted(path.name for path in localesDir.iterdir() if path.is_dir())


def NVDA_starts_for_all_locales():
	"""Start NVDA with each source locale and ensure startup succeeds."""
	localeCodes = _getSourceLocaleCodes()
	_builtIn.should_be_true(bool(localeCodes), msg="No locale directories found under source/locale")
	spy = _NvdaLib.getSpyLib()

	for localeCode in localeCodes:
		_builtIn.log(f"Testing NVDA startup with language: {localeCode}")
		started = False
		try:
			spy.start_NVDA(
				"standard-dontShowWelcomeDialog.ini",
				language=localeCode,
			)
			started = True
		finally:
			if started:
				spy.quit_NVDA()
