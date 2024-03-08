# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import os
import tempfile


def _createEmptyTempFileForDeletingFile(
		dir: str | None = None,
		prefix: str | None = None,
		suffix: str | None = None,
	) -> str:
	"""
	Create an empty temporary file and return its path.

	tempfile.mktemp is deprecated as creating a temporary file in the system's temporary directory is a security risk,
	without holding it open, as the file could be created by an attacker with the same name.
	tempfile.mkstemp / tempfile.NamedTemporaryFile was created for the purpose of creating temporary files securely.
	However, we do not need this secure behaviour, as we are just creating a temp file to move files for future deletion.
	As such, we close the file handle and return the path.
	"""
	fh, tempPath = tempfile.mkstemp(dir=dir, suffix=suffix, prefix=prefix)
	os.close(fh)
	return tempPath
