# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2024 NV Access Limited, Joseph Lee, Babbage B.V., Julien Cochuyt, Leonard de Ruijter

"""Manages information about available braille translation tables."""

import collections
from enum import Enum, StrEnum, auto
import os
from locale import strxfrm
from typing import NamedTuple

from configobj import ConfigObj, flatten_errors
from configobj.validate import Validator

import config
import globalVars
from logHandler import log
import languageHandler

TABLES_DIR = os.path.join(globalVars.appDir, "louis", "tables")
"""The directory in which liblouis braille tables are located."""

DEFAULT_TABLE = "en-ueb-g1.ctb"
"""The default braille table."""


class TableSource(StrEnum):
	BUILTIN = "builtin"
	"""The name of the builtin table source"""
	SCRATCHPAD = "scratchpad"
	"""The name of the scratchpad table source"""


class TableType(Enum):
	INPUT = auto()
	"""Input type for braille tables for back-translation"""
	OUTPUT = auto()
	"""Output type for braille tables for translation"""


_tablesDirs = collections.ChainMap(
	{
		TableSource.BUILTIN: TABLES_DIR,
	},
)
"""Chainmap of directories for braille tables lookup, including custom tables."""


class BrailleTable(NamedTuple):
	"""Information about a braille table."""

	fileName: str
	"""The file name of the table."""

	displayName: str
	"""The name of the table as displayed to the user. This should be translatable."""

	contracted: bool = False
	"""True if the table is contracted, False if uncontracted."""

	output: bool = True
	"""True if this table can be used for output, False if not."""

	input: bool = True
	"""True if this table can be used for input, False if not."""

	source: str = TableSource.BUILTIN
	"""An identifier describing the source of the table.
	This defaults to C{TableSource.BUILTIN}, but is set to the name of the add-on or "scratchpad",
	depending on its source.
	"""


_tables = collections.ChainMap()
"""Maps file names to L{BrailleTable} objects.
The parent map will be loaded at import time with the builtin tables.
The first map will be loaded when calling L{initialize} with the custom tables,
and cleared when calling L{terminate}.
"""

_inputTableForLangs: dict[str, str] = dict()
"""Maps languages to input L{BrailleTable.fileName}."""

_outputTableForLangs: dict[str, str] = dict()
"""Maps languages to output L{BrailleTable.fileName}."""


def getDefaultTableForCurLang(tableType: TableType) -> str:
	"""Gets the file name of the braille table for the current NVDA language.
	:param tableType: INPUT (back-translation) or OUTPUT (translation).
	:return: A L{BrailleTable} fileName.
	"""
	match tableType:
		case tableType.INPUT:
			langDict = _inputTableForLangs
		case tableType.OUTPUT:
			langDict = _outputTableForLangs
		case _:
			raise ValueError(f"Unknown tableType: {tableType}")
	lang = languageHandler.getLanguage()
	table = langDict.get(lang)
	if table is not None:
		return table
	if "_" in lang:
		lang = lang.split("_")[0]
	return langDict.get(lang, DEFAULT_TABLE)


def addTable(
	fileName: str,
	displayName: str,
	contracted: bool = False,
	output: bool = True,
	input: bool = True,
	source: str = TableSource.BUILTIN,
	inputForLangs: set[str] | None = None,
	outputForLangs: set[str] | None = None,
):
	"""Register a braille translation table.
	At least one of C{input} or C{output} must be C{True}.
	:param fileName: The file name of the table.
	:param displayname: The name of the table as displayed to the user. This should be translatable.
	:param contracted: True if the table is contracted, False if uncontracted.
	:param output: True if this table can be used for output, False if not.
	:param input: True if this table can be used for input, False if not.
	:param source: An identifier describing the source of the table.
	:param inputForLangs: A set of languages available in NVDA or C{None}.
	:param outputForLangs: A set of languages available in NVDA or C{None}.
	"""
	if not output and not input:
		raise ValueError("input and output cannot both be False")
	table = BrailleTable(fileName, displayName, contracted, output, input, source)
	_tables[fileName] = table
	if inputForLangs is not None:
		for lang in inputForLangs:
			if lang in _inputTableForLangs:
				log.warning(
					f"input table lang {lang} already set to {_inputTableForLangs[lang]} overwriting to {table.fileName}",
				)
			_inputTableForLangs[lang] = table.fileName
	if outputForLangs is not None:
		for lang in outputForLangs:
			if lang in _outputTableForLangs:
				log.warning(
					f"output table lang {lang} already set to {_outputTableForLangs[lang]} overwriting to {table.fileName}",
				)
			_outputTableForLangs[lang] = table.fileName


def getTable(fileName: str) -> BrailleTable:
	"""Get information about a table given its file name.
	@return: The table information.
	@raise LookupError: If there is no table registered with this file name.
	"""
	if fileName == "auto":
		fileName = DEFAULT_TABLE
	return _tables[fileName]


def listTables() -> list[BrailleTable]:
	"""List all registered braille tables.
	@return: A list of braille tables.
	"""
	return sorted(
		_tables.values(),
		key=lambda table: (table.source != TableSource.BUILTIN, strxfrm(table.displayName)),
	)


#: Maps old table names to new table names for tables renamed in newer versions of liblouis.
RENAMED_TABLES = {
	"ar-fa.utb": "fa-ir-g1.utb",
	"da-dk-g16.utb": "da-dk-g16.ctb",
	"da-dk-g18.utb": "da-dk-g18.ctb",
	"de-de-g0.utb": "de-g0.utb",
	"de-de-g1.ctb": "de-g1.ctb",
	"de-de-g2.ctb": "de-g2.ctb",
	"de-g0-bidi.utb": "de-g0-detailed.utb",
	"de-g1-bidi.ctb": "de-g1-detailed.ctb",
	"en-us-comp8.ctb": "en-us-comp8-ext.utb",
	"fr-ca-g1.utb": "fr-bfu-comp6.utb",
	"Fr-Ca-g2.ctb": "fr-bfu-g2.ctb",
	"gr-bb.ctb": "grc-international-en.utb",
	"gr-gr-g1.utb": "el.ctb",
	"he.ctb": "he-IL-comp8.utb",
	"hr.ctb": "hr-comp8.utb",
	"lt.ctb": "lt-8dot.utb",
	"mn-MN.utb": "mn-MN-g1.utb",
	"nl-BE-g0.utb": "nl-NL-g0.utb",
	"nl-NL-g1.ctb": "nl-NL-g0.utb",
	"no-no.ctb": "no-no-8dot.utb",
	"no-no-comp8.ctb": "no-no-8dot.utb",
	"ru-compbrl.ctb": "ru-comp6.utb",
	"ru.ctb": "ru-comp8.utb",
	"ru-ru-g1.utb": "ru-litbrl-detailed.utb",
	"Se-Se-g1.utb": "sv-g0.utb",
	"sk-sk-g1.utb": "sk-g1.ctb",
	"UEBC-g1.ctb": "en-ueb-g1.ctb",
	"UEBC-g2.ctb": "en-ueb-g2.ctb",
	"vi-g1.ctb": "vi-vn-g1.ctb",
}


# Add the builtin tables at import time.

from . import __tables as __tables  # noqa: E402

# Add new first maps for the custom tables - provided in the scratchpad directory
# and/or by addons.
_tables = _tables.new_child()
_tablesDirs = _tablesDirs.new_child()


def _loadTablesFromManifestSection(source: str, directory: str, tablesDict: dict):
	for fileName, tableConfig in tablesDict.items():
		addTable(
			fileName=fileName,
			displayName=tableConfig["displayName"],
			contracted=tableConfig["contracted"],
			input=tableConfig["input"],
			output=tableConfig["output"],
			source=source,
		)


def initialize():
	if config.isAppX or globalVars.appArgs.disableAddons:
		return
	# The builtin tables were added at import time to the parent map.
	# Now, add the custom tables to the first map.
	import addonHandler

	for addon in addonHandler.getRunningAddons():
		try:
			tablesDict = addon.manifest.get("brailleTables")
			if not tablesDict:
				continue
			log.debug(f"Found {len(tablesDict)} braille table entries in manifest for add-on {addon.name!r}")
			directory = os.path.join(addon.path, "brailleTables")
			if os.path.isdir(directory):
				_tablesDirs[addon.name] = directory
			_loadTablesFromManifestSection(addon.name, directory, tablesDict)
		except Exception:
			log.exception(f"Error while applying custom braille tables config from addon {addon.name!r}")

	# Load the custom tables from the scratchpad last so it takes precedence over add-ons
	if not globalVars.appArgs.secure and config.conf["development"]["enableScratchpadDir"]:
		scratchpad = config.getScratchpadDir()
		directory = os.path.join(scratchpad, "brailleTables")
		if os.path.isdir(directory):
			manifestPath = os.path.join(scratchpad, addonHandler.MANIFEST_FILENAME)
			if not os.path.isfile(manifestPath):
				return
			_tablesDirs[TableSource.SCRATCHPAD] = directory
			configspec = {"brailleTables": addonHandler.AddonManifest.configspec["brailleTables"]}
			try:
				with open(manifestPath, "rb") as file:
					manifest = ConfigObj(file, configspec=configspec)
					section = manifest.get("brailleTables")
					if not section:
						return
					if (res := manifest.validate(Validator(), preserve_errors=True)) is not True:
						raise ValueError(f"Errors in scratchpad manifest: {flatten_errors(manifest, res)}")
					log.debug(f"Found {len(section)} braille table entries in manifest for scratchpad")
					_loadTablesFromManifestSection(TableSource.SCRATCHPAD, directory, section)
			except Exception:
				log.exception(
					"Error while applying custom braille tables config from scratchpad manifest: "
					f"{manifestPath}",
				)


def terminate():
	# Clear all the custom tables, preserving only the builtin ones.
	_tablesDirs.clear()
	_tables.clear()
