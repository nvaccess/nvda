# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Noelia Ruiz Martínez
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


import yaml  # noqa: I001
from configobj.validate import Validator, VdtParamError, VdtUnknownCheckError, ValidateError
from typing import Any

import globalVars
from .configSpec import confspec
from logHandler import log
from NVDAState import shouldWriteToDisk, WritePaths


_customSections: dict[str, dict[str, Any]] = {}


def _loadCustomSections() -> None:
	"""Add registered customSections to the configuration."""
	if globalVars.appArgs.disableAddons:
		return

	path = WritePaths.nvdaCustomSectionsFile
	try:
		with open(path, encoding="utf-8") as _f:
			sections = yaml.safe_load(_f)
	except FileNotFoundError:
		return
	except OSError:
		log.exception(f"Error reading custom sections at {path}.")
		return
	except yaml.YAMLError:
		log.exception(f"Error parsing {path}.")
		return
	if sections is None:
		return
	if not isinstance(sections, dict):
		log.error(f"{path} has unexpected format (expected a mapping).")
		return
	for name, entry in sections.items():
		if not isinstance(name, str):
			log.debugWarning(f"Custom section name {name} is not a string; skipping.")
			continue
		if name in confspec:
			log.debugWarning(f"Registering custom section {name!r} that is already registered.")
		if not isinstance(entry, dict) or "spec" not in entry:
			log.debugWarning(f"Custom section {name} has an invalid entry; skipping.")
			continue
		if not isinstance(entry["spec"], dict):
			log.debugWarning(f"Custom section {name} has a non-mapping spec; skipping.")
			continue
		if not _isValidSpec(entry["spec"]):
			log.debugWarning(f"Custom section {name} has an invalid spec; skipping.")
			continue
		isBaseOnly = bool(entry.get("isBaseOnly", False))
		_addSection(name, entry["spec"], isBaseOnly)


def _isValidSpec(spec: dict) -> bool:
	"""Check if the given spec is valid.

	:param spec: The spec dictionary to validate.
	:return: True if the spec is valid, False otherwise.
	"""
	validator = Validator()
	for value in spec.values():
		if isinstance(value, dict):
			if not _isValidSpec(value):
				return False
		elif not isinstance(value, str):
			return False
		else:
			try:
				validator.check(value, "")
			except (VdtUnknownCheckError, VdtParamError):
				return False
			except ValidateError:
				pass  # Syntax is valid; the empty value just failed the check.
	return True


def _addSection(sectionName: str, sectionSpec: dict[str, Any], isBaseOnly: bool = False):
	"""Add a section to the configuration.
	:param sectionName: The name of the section to add.
	:param sectionSpec: The configspec for the section to add.
	:param isBaseOnly: Whether this section should only be in the base configuration, defaults to False.
	"""
	confspec[sectionName] = sectionSpec
	_customSections[sectionName] = {"spec": sectionSpec, "isBaseOnly": isBaseOnly}
	if isBaseOnly:
		from . import ConfigManager

		ConfigManager.BASE_ONLY_SECTIONS.add(sectionName)


def registerSection(
	sectionName: str,
	sectionSpec: dict[str, Any],
	isBaseOnly: bool = False,
) -> None:
	"""Register a configuration section.
	This is intended for add-ons to register custom sections.
	:param sectionName: The name of the section to add.
	:param sectionSpec: The configspec for the section to add.
	:param isBaseOnly: Whether this section should only be in the base configuration.
	"""
	if sectionName in confspec:
		log.debugWarning(f"Registering custom section {sectionName!r} that is already registered.")
	if not isinstance(sectionSpec, dict):
		raise TypeError(f"sectionSpec for {sectionName!r} must be a dict.")
	_customSections[sectionName] = {"spec": sectionSpec, "isBaseOnly": isBaseOnly}
	_saveCustomSections()


def unregisterSection(sectionName: str) -> None:
	"""Unregister a section that was added to the configuration.
	This is intended for add-ons to unregister custom sections they added, for example when the add-on is uninstalled.
	:param sectionName: The name of the section to remove.
	"""
	try:
		del _customSections[sectionName]
		_saveCustomSections()
	except KeyError:
		log.debugWarning(
			f"Attempted to unregister custom section {sectionName!r} that was not registered.",
		)


def _saveCustomSections() -> None:
	"""Write all registered custom sections to disk."""
	if not shouldWriteToDisk():
		return
	path = WritePaths.nvdaCustomSectionsFile
	try:
		with open(path, "w", encoding="utf-8") as f:
			yaml.safe_dump(_customSections, f, allow_unicode=True, default_flow_style=False)
	except (OSError, yaml.YAMLError):
		log.exception(f"Error saving sections to {path}.")
