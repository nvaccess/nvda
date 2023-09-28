# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import sys
import os
import subprocess
import shutil
from typing import Set

"""
A script to ensure that the NVDA build system's Python virtual environment is created and up to date.
"""

top_dir: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
venv_path: str = os.path.join(top_dir, ".venv")
requirements_path: str = os.path.join(top_dir, "requirements.txt")
venv_orig_requirements_path: str = os.path.join(venv_path, "_requirements.txt")
venv_python_version_path: str = os.path.join(venv_path, "python_version")
#: Whether this script is run interactively,
#: i.e. whether user input is possible to answer questions.
#: Value is True if interactive (i.e. stdout is attached to a terminal), False otherwise.
isInteractive = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
if not isInteractive:
	print(
		"Warning: Running in non-interactive mode. Defaults are assumed for prompts, if applicable",
		flush=True
	)


def askYesNoQuestion(message: str, default: bool) -> bool:
	"""
	Displays the given message to the user and accepts y or n as input.
	Any other input causes the question to be asked again.
	If isInteractive is False, the default is always returned, the question and outcome
	will still be sent to stdout for inspection of the build.
	@param default: the return value when the user can not be prompted.
	@returns: True for y and False for n.
	"""
	question: str = f"{message} [y/n]: "
	while True:
		if isInteractive:
			answer = input(question)
		else:
			answer = "y" if default else "n"
			print(f"{question}{answer} (answered non-interactively)")
		if answer == 'n':
			return False
		elif answer == 'y':
			return True
		else:
			continue  # ask again


def fetchRequirementsSet(path: str) -> Set[str]:
	"""
	Fetches all the package lines from a pip requirements.txt file
	returning them as a set of strings.
	The returned set could be compared with a set from another file
	which would allow easy identification of which requirements were added or removed.
	"""
	with open(path, "r") as f:
		lines = [x.strip() for x in f.readlines()]
		lines = [x for x in lines if x and not x.isspace() and not x.startswith('#')]
	return set(lines)


def populate():
	"""
	Installs all required packages within the virtual environment.
	When called stand alone, this function only ensures that NVDA's package requirements are met,
	without recreating the full environment.
	This means that transitive dependencies can get out of sync with those used in automated builds.
	"""
	print("Installing packages in virtual environment...", flush=True)
	subprocess.run(
		[
			# Activate virtual environment
			os.path.join(venv_path, "scripts", "activate.bat"),
			"&&",
			# Ensure we have the latest version of pip
			"py", "-m", "pip",
			"install", "--upgrade", "pip",
			"&&",
			# Install required packages with pip
			"py", "-m", "pip",
			"install", "-r", requirements_path,
		],
		check=True,
		shell=True,
	)
	shutil.copy(requirements_path, venv_orig_requirements_path)


def createVenv():
	"""
	Creates the NVDA build system's Python virtual environment.
	This function will overwrite any existing virtual environment found at c{venv_path}.
	"""
	print("Creating virtual environment...", flush=True)
	subprocess.run(
		[
			sys.executable,
			"-m", "venv",
			"--clear",
			venv_path,
		],
		check=True
	)
	with open(venv_python_version_path, "w") as f:
		f.write(sys.version)


def createVenvAndPopulate():
	createVenv()
	populate()


def ensureVenvAndRequirements():
	"""
	Ensures that the NVDA build system's Python virtual environment is created and up to date.
	If a previous virtual environment exists but has a miss-matching Python version
	the virtual environment is recreated with the updated version of Python.
	When pip package requirements have changed, this function asks the user to recreate the environment.
	If a virtual environment is found but does not seem to be ours,
	This function asks the user if it should be overwritten or not.
	"""
	if not os.path.exists(venv_path):
		print("Virtual environment does not exist.")
		return createVenvAndPopulate()
	if (
		not os.path.exists(venv_python_version_path)
		or not os.path.exists(venv_orig_requirements_path)
	):
		if askYesNoQuestion(
			f"Virtual environment at {venv_path} probably not created by NVDA. "
			"This directory must be removed before continuing. Should it be removed?",
			default=True
		):
			return createVenvAndPopulate()
		else:
			print("Aborting")
		sys.exit(1)
	venv_python_version = open(venv_python_version_path, "r").read()
	if venv_python_version != sys.version:
		print(f"Python version changed. Was {venv_python_version}, now is {sys.version}")
		return createVenvAndPopulate()
	oldRequirements = fetchRequirementsSet(venv_orig_requirements_path)
	newRequirements = fetchRequirementsSet(requirements_path)
	addedRequirements = newRequirements - oldRequirements
	if addedRequirements:
		if askYesNoQuestion(
			f"Added or changed package requirements. {addedRequirements}\n"
			"You are encouraged to recreate the virtual environment. "
			"If you choose no, the new requirements will be installed without recreating. "
			"This means that transitive dependencies can get out of sync "
			"with those used in automated builds. "
			"Would you like to continue recreating the environment?",
			default=True
		):
			return createVenvAndPopulate()
		return populate()


if __name__ == '__main__':
	# Ensure we are not inside an already active Python virtual environment.
	virtualEnv = os.getenv("VIRTUAL_ENV")
	if virtualEnv:
		print(
			"Error: It looks like another Python virtual environment is already active in this shell.\n"
			"Please deactivate the current Python virtual environment and try again."
		)
		sys.exit(1)
	ensureVenvAndRequirements()
