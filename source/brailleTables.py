# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2022 NV Access Limited, Joseph Lee, Babbage B.V.

"""Manages information about available braille translation tables.
"""

import os
import collections
from locale import strxfrm
import globalVars


#: The directory in which liblouis braille tables are located.
TABLES_DIR = os.path.join(globalVars.appDir, "louis", "tables")

#: Information about a braille table.
#: This has the following attributes:
#: * fileName: The file name of the table.
#: * displayname: The name of the table as displayed to the user. This should be translatable.
#: * contracted: C{True} if the table is contracted, C{False} if uncontracted.
#: * output: C{True} if this table can be used for output, C{False} if not.
#: * input: C{True} if this table can be used for input, C{False} if not.
BrailleTable = collections.namedtuple("BrailleTable", ("fileName", "displayName", "contracted", "output", "input"))

#: Maps file names to L{BrailleTable} objects.
_tables = {}

def addTable(fileName, displayName, contracted=False, output=True, input=True):
	"""Register a braille translation table.
	At least one of C{input} or C{output} must be C{True}.
	@param fileName: The file name of the table.
	@type fileName: basestring
	@param displayname: The name of the table as displayed to the user. This should be translatable.
	@type displayName: unicode
	@param contracted: C{True} if the table is contracted, C{False} if uncontracted.
	@type cContracted: bool
	@param output: C{True} if this table can be used for output, C{False} if not.
	@type output: bool
	@param input: C{True} if this table can be used for input, C{False} if not.
	@type input: bool
	"""
	if not output and not input:
		raise ValueError("input and output cannot both be False")
	table = BrailleTable(fileName, displayName, contracted, output, input)
	_tables[fileName] = table

def getTable(fileName):
	"""Get information about a table given its file name.
	@return: The table information.
	@rtype: L{BrailleTable}
	@raise LookupError: If there is no table registered with this file name.
	"""
	return _tables[fileName]

def listTables():
	"""List all registered braille tables.
	@return: A list of braille tables.
	@rtype: list of L{BrailleTable}
	"""
	return sorted(_tables.values(), key=lambda table: strxfrm(table.displayName))

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
	"mn-MN.utb": "mn-MN-g1.utb",
	"nl-BE-g0.utb": "nl-NL-g0.utb",
	"nl-NL-g1.ctb": "nl-NL-g0.utb",
	"no-no.ctb": "no-no-8dot.utb",
	"no-no-comp8.ctb": "no-no-8dot.utb",
	"ru-compbrl.ctb": "ru.ctb",
	"ru-ru-g1.utb": "ru-litbrl-detailed.utb",
	"sk-sk-g1.utb": "sk-g1.ctb",
	"UEBC-g1.ctb": "en-ueb-g1.ctb",
	"UEBC-g2.ctb": "en-ueb-g2.ctb",
	"vi-g1.ctb": "vi-vn-g1.ctb",
}

# Add builtin tables.
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("afr-za-g1.ctb", _("Afrikaans grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("afr-za-g2.ctb", _("Afrikaans grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ar-ar-comp8.utb", _("Arabic 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ar-ar-g1.utb", _("Arabic grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ar-ar-g2.ctb", _("Arabic grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("as-in-g1.utb", _("Assamese grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ba.utb", _("Bashkir grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("be-in-g1.utb", _("Bengali grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("bel-comp.utb", _("Belarusian computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("bel.utb", _("Belarusian literary braille"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("bg.ctb", _("Bulgarian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("bg.utb", _("Bulgarian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ca-g1.ctb", _("Catalan grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ckb-g1.ctb", _("Central Kurdish grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cop-eg-comp8.utb", _("Coptic 8 dot computer braille"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cy-cy-g1.utb", _("Welsh grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cy-cy-g2.ctb", _("Welsh grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cs-comp8.utb", _("Czech 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cs-g1.ctb", _("Czech grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g08.ctb", _("Danish 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g16.ctb", _("Danish 6 dot grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g18.ctb", _("Danish 8 dot grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g26.ctb", _("Danish 6 dot grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g28.ctb", _("Danish 8 dot grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-comp6.utb", _("German 6 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-de-comp8.ctb", _("German 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g0.utb", _("German grade 0"), input=False)

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g0-detailed.utb", _("German grade 0 (detailed)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g1.ctb", _("German grade 1"), input=False)

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g1-detailed.ctb", _("German grade 1 (detailed)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g2.ctb", _("German grade 2"), contracted=True, input=False)

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("el.ctb", _("Greek (Greece)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-gb-comp8.ctb", _("English (U.K.) 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-gb-g1.utb", _("English (U.K.) grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-GB-g2.ctb", _("English (U.K.) grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-nabcc.utb", _("English North American Braille Computer Code"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-ueb-g1.ctb", _("Unified English Braille Code grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-ueb-g2.ctb", _("Unified English Braille Code grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-us-comp6.ctb", _("English (U.S.) 6 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-us-comp8-ext.utb", _("English (U.S.) 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-us-g1.ctb", _("English (U.S.) grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("en-us-g2.ctb", _("English (U.S.) grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("eo-g1.ctb", _("Esperanto grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Es-Es-G0.utb", _("Spanish 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("es-g1.ctb", _("Spanish grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("es-g2.ctb", _("Spanish grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("et-g0.utb", _("Estonian grade 0"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ethio-g1.ctb", _("Ethiopic grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fa-ir-comp8.ctb", _("Persian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fa-ir-g1.utb", _("Persian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fi.utb", _("Finnish 6 dot"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fi-fi-8dot.ctb", _("Finnish 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fr-bfu-comp6.utb", _("French (unified) 6 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fr-bfu-comp8.utb", _("French (unified) 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fr-bfu-g2.ctb", _("French (unified) grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ga-g1.utb", _("Irish grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ga-g2.ctb", _("Irish grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("gu-in-g1.utb", _("Gujarati grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("grc-international-en.utb", _("Greek international braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("he-IL.utb", _("Israeli grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("he-IL-comp8.utb", _("Hebrew computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hi-in-g1.utb", _("Hindi grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hr-comp8.utb", _("Croatian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hr-g1.ctb", _("Croatian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hu-hu-comp8.ctb", _("Hungarian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hu-hu-g1.ctb", _("Hungarian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hu-hu-g2.ctb", _("Hungarian grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("is.ctb", _("Icelandic 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("it-it-comp6.utb", _("Italian 6 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("it-it-comp8.utb", _("Italian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ja-kantenji.utb", _("Japanese (Kantenji) literary braille"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ka-in-g1.utb", _("Kannada grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("kk.utb", _("Kazakh grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("km-g1.utb", _("Khmer grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("kmr.tbl", _("Northern Kurdish grade 0"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ko-2006-g1.ctb", _("Korean grade 1 (2006)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ko-2006-g2.ctb", _("Korean grade 2 (2006)"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ko-g1.ctb", _("Korean grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ko-g2.ctb", _("Korean grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ks-in-g1.utb", _("Kashmiri grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("lt.ctb", _("Lithuanian 8 dot"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("lt-6dot.utb", _("Lithuanian 6 dot"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Lv-Lv-g1.utb", _("Latvian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ml-in-g1.utb", _("Malayalam grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("mn-in-g1.utb", _("Manipuri grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ms-my-g2.ctb", _("Malay grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("mn-MN-g1.utb", _("Mongolian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("mn-MN-g2.ctb", _("Mongolian grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("mr-in-g1.utb", _("Marathi grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("my-g1.utb", _("Burmese grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("my-g2.ctb", _("Burmese grade 2"), contracted=True, input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nl-NL-g0.utb", _("Dutch 6 dot"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nl-comp8.utb", _("Dutch 8 dot"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("no-no-8dot.utb", _("Norwegian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g0.utb", _("Norwegian grade 0"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g1.ctb", _("Norwegian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g2.ctb", _("Norwegian grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g3.ctb", _("Norwegian grade 3"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("np-in-g1.utb", _("Nepali grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nso-za-g1.utb", _("Sepedi grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nso-za-g2.ctb", _("Sepedi grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("or-in-g1.utb", _("Oriya grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("pl-pl-comp8.ctb", _("Polish 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Pl-Pl-g1.utb", _("Polish literary braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("pt-pt-comp8.ctb", _("Portuguese 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Pt-Pt-g1.utb", _("Portuguese grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Pt-Pt-g2.ctb", _("Portuguese grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("pu-in-g1.utb", _("Punjabi grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ro.ctb", _("Romanian"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru.ctb", _("Russian computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-litbrl.ctb", _("Russian literary braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-litbrl-detailed.utb", _("Russian literary braille (detailed)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-ru-g1.ctb", _("Russian contracted braille"), contracted=True, input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sa-in-g1.utb", _("Sanskrit grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sah.utb", _("Yakut grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Se-Se.ctb", _("Swedish 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Se-Se-g1.utb", _("Swedish grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sk-g1.ctb", _("Slovak grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sl-si-comp8.ctb", _("Slovenian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sl-si-g1.utb", _("Slovenian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sot-za-g1.ctb", _("Sesotho grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sot-za-g2.ctb", _("Sesotho grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sr-g1.ctb", _("Serbian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ta-ta-g1.ctb", _("Tamil grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tt.utb", _("Tatar grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("te-in-g1.utb", _("Telugu grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tr.ctb", _("Turkish grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tsn-za-g1.ctb", _("Setswana grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tsn-za-g2.ctb", _("Setswana grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("uk.utb", _("Ukrainian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("uk-comp.utb", _("Ukrainian computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ur-pk-g1.utb", _("Urdu grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ur-pk-g2.ctb", _("Urdu grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("uz-g1.utb", _("Uzbek grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("unicode-braille.utb", _("Unicode braille"), output=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("vi-vn-g0.utb", _("Vietnamese grade 0"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ve-za-g1.utb", _("Tshivenda grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ve-za-g2.ctb", _("Tshivenda grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("vi-vn-g1.ctb", _("Vietnamese grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("vi-vn-g2.ctb", _("Vietnamese grade 2"), contracted=True, input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("vi-saigon-g1.ctb", _("Southern Vietnamese grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("xh-za-g1.utb", _("Xhosa grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("xh-za-g2.ctb", _("Xhosa grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
# This should be translated to '中文中国汉语现行盲文' in Mandarin.
addTable("zhcn-g1.ctb", _("Chinese (China, Mandarin) Current Braille System"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
# This should be translated to '中文中国汉语双拼盲文' in Mandarin.
addTable("zhcn-g2.ctb", _("Chinese (China, Mandarin) Double-phonic Braille System"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zh-hk.ctb", _("Chinese (Hong Kong, Cantonese)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zh-tw.ctb", _("Chinese (Taiwan, Mandarin)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zu-za-g1.utb", _("Zulu grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zu-za-g2.ctb", _("Zulu grade 2"), contracted=True)
