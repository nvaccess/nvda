# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited, Neil Soiffer, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import glob
import os
from collections.abc import Callable
from zipfile import ZipFile

from logHandler import log


def getRulesFiles(
	pathToDir: str,
	processSubDirs: Callable[[str, str], list[str]] | None,
) -> list[str]:
	"""Get the rule files from a directory, optionally processing subdirectories.
	Searches for files ending with '_Rules.yaml' in the specified directory.
	If no rule files are found, attempts to find them inside a corresponding ZIP archive,
	including checking any subdirectories inside the ZIP.
	:param pathToDir: Path to the directory to search for rule files.
	:param processSubDirs: Optional callable to process subdirectories. It should take the subdirectory name
	and the language code as arguments, returning a list of rule filenames found in that subdirectory.
	:return: A list of rule file names found either directly in the directory or inside the ZIP archive.
	"""
	language: str = os.path.basename(pathToDir)
	ruleFiles: list[str] = [
		os.path.basename(file) for file in glob.glob(os.path.join(pathToDir, "*_Rules.yaml"))
	]
	for dir in os.listdir(pathToDir):
		if os.path.isdir(os.path.join(pathToDir, dir)):
			if processSubDirs:
				ruleFiles.extend(processSubDirs(dir, language))
		if len(ruleFiles) == 0:
			# look in the .zip file for the style files, including regional subdirs -- it might not have been unzipped
			try:
				zip_file: ZipFile = ZipFile(f"{pathToDir}\\{language}.zip", "r")
				for file in zip_file.namelist():
					if file.endswith("_Rules.yaml"):
						ruleFiles.append(file)
					elif zip_file.getinfo(file).is_dir() and processSubDirs:
						ruleFiles.extend(processSubDirs(dir, language))
			except Exception as e:
				log.debugWarning(f"MathCAT Dialog: didn't find zip file {zip_file}. Error: {e}")
	return ruleFiles
