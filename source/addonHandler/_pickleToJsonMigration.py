# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Utilities for migrating add-on state from the legacy pickle format to JSON.

Prior to NVDA 2026.1, add-on state (which add-ons are disabled, pending install/removal, etc.) was persisted as a pickle file (``addonsState.pickle``).
This module provides helpers that read such a pickle file, validate its contents, and return a JSON-serialisable dictionary so the state can be persisted as JSON instead (``addonsState.json``).

.. warning:
	This module is scheduled for removal in NVDA 2027.1 once all users have had sufficient opportunity to migrate.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import NVDAState
from addonAPIVersion import BACK_COMPAT_TO
from addonStore.models.status import AddonStateCategory
from logHandler import log

if TYPE_CHECKING:
	import os


# This module and its callers should be removed in 2027.1.
# To ensure this isn't missed, log an error about using the module on 2027.1 if deprecated APIs are allowed, and fail if they're not.
if BACK_COMPAT_TO >= (2027, 1, 0):
	DEPRECATION_STRING = "addonHandler._pickleToJsonMigration is deprecated. All internal use of pickle should be removed in NVDA 2027.1."
	if NVDAState._allowDeprecatedAPI():
		log.error(DEPRECATION_STRING, stack_info=True)
	else:
		raise RuntimeError(DEPRECATION_STRING)


def _pickledStateDictToJsonStateDict(pickledState: Any) -> dict[str, list[str] | tuple[int, int, int]]:
	"""Convert an unpickled add-on state dictionary to a JSON-compatible form.

	Keys and values are validated, and unrecognised or malformed entries are logged and silently discarded.
	This allows partially corrupt pickles to be migrated.

	:param pickledState: The raw object obtained from ``pickle.load``.
		Expected to be a ``dict`` mapping :class:`AddonStateCategory` string keys to ``set[str]`` values.
		May also include a ``"backCompatToAPIVersion"`` key with a 2- or 3-element integer tuple.
	:return: A new dictionary suitable for JSON serialisation.
		May be empty depending on the validity of ``pickledDict``.
	"""
	if not isinstance(pickledState, dict):
		log.debug(f"Invalid pickled state: {pickledState!r}")
		return {}
	jsonState: dict[str, list[str] | tuple[int, int, int]] = {}
	for key, value in pickledState.items():
		if key == "backCompatToAPIVersion":
			# backCompatToAPIVersion is an API version tuple, e.g. (2024, 1, 0).
			# The patch version is optional and defaults to 0.
			if (
				isinstance(value, tuple)
				and 2 <= len(value) <= 3
				and all(isinstance(part, int) for part in value)
			):
				jsonState[key] = value
			else:
				log.debug(f"Invalid backCompatToAPIVersion: {value!r}. Discarding.")
		elif key in AddonStateCategory:
			# Add-on category values were stored as sets of add-on name strings.
			# Since JSON doesn't have a set type, convert each to a list, filtering out any non-string values.
			if not isinstance(value, set):
				log.debug(f"Invalid category {key}: {value!r}. Discarding.")
				continue
			addons = jsonState[key] = []
			for addon in value:
				if isinstance(addon, str):
					addons.append(addon)
				else:
					log.debug(f"Invalid add-on in category {key}: {addon!r}. Discarding")
		else:
			log.debug(f"Unrecognised key-value pair: {key!r}: {value!r}. Discarding")
	return jsonState


def _getAddonsStateDictFromPickle(picklePath: os.PathLike) -> dict[str, list[str] | tuple[int, int, int]]:
	"""Load a legacy pickled add-on state file and return a JSON-compatible dict.

	This is the main entry point used by :mod:`addonHandler` and :mod:`installer` when an ``addonsState.pickle`` file exists and hasn't yet been migrated to ``addonsState.json``.

	:param picklePath: Path to the ``addonsState.pickle`` file.
	:return: A validated, JSON-serialisable dictionary of add-on state.
	:raises Exception: Any exception raised by :func:`open` or :func:`pickle.load`.
		E.g. ``FileNotFoundError``, ``pickle.UnpicklingError``.
	"""
	# pickle is imported locally to avoid loading it at module level, since this migration path will eventually be removed entirely.
	import pickle

	with open(picklePath, "rb") as pickleFile:
		return _pickledStateDictToJsonStateDict(pickle.load(pickleFile))
