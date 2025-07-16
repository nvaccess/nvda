# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2021 NV Access Limited, Joseph Lee, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


"""Contains information about various languages supported by NVDA.
As there are localizable strings at module level,
this can only be imported once localization is set up via `languageHandler.initialize`.
"""

from typing import Dict


# Maps names of languages supported by NVDA to their translated names
# for langs for which Windows does not contain a translated description.
LANG_NAMES_TO_LOCALIZED_DESCS: Dict[str, str] = {
	# Translators: The name of a language supported by NVDA.
	"aa": pgettext("languageName", "Afar"),
	# Translators: The name of a language supported by NVDA.
	"ab": pgettext("languageName", "Abkhazian"),
	# Translators: The name of a language supported by NVDA.
	"ak": pgettext("languageName", "Akan"),
	# Translators: The name of a language supported by NVDA.
	"an": pgettext("languageName", "Aragonese"),
	# Translators: The name of a language supported by NVDA.
	"av": pgettext("languageName", "Avaric"),
	# Translators: The name of a language supported by NVDA.
	"ay": pgettext("languageName", "Aymara"),
	# Translators: The name of a language supported by NVDA.
	"bh": pgettext("languageName", "Unknown"),
	# Translators: The name of a language supported by NVDA.
	"bi": pgettext("languageName", "Bislama"),
	# Translators: The name of a language supported by NVDA.
	"bm": pgettext("languageName", "Bambara"),
	# Translators: The name of a language supported by NVDA.
	"ce": pgettext("languageName", "Chechen"),
	# Translators: The name of a language supported by NVDA.
	"ch": pgettext("languageName", "Chamorro"),
	# Translators: The name of a language supported by NVDA.
	"ckb": pgettext("languageName", "Central Kurdish"),
	# Translators: The name of a language supported by NVDA.
	"cr": pgettext("languageName", "Cree"),
	# Translators: The name of a language supported by NVDA.
	"cu": pgettext("languageName", "Church Slavic"),
	# Translators: The name of a language supported by NVDA.
	"cv": pgettext("languageName", "Chuvash"),
	# Translators: The name of a language supported by NVDA.
	"ee": pgettext("languageName", "Ewe"),
	# Translators: The name of a language supported by NVDA.
	"eo": pgettext("languageName", "Esperanto"),
	# Translators: The name of a language supported by NVDA.
	"fj": pgettext("languageName", "Fijian"),
	# Translators: The name of a language supported by NVDA.
	"gv": pgettext("languageName", "Manx"),
	# Translators: The name of a language supported by NVDA.
	"ho": pgettext("languageName", "Hiri Motu"),
	# Translators: The name of a language supported by NVDA.
	"ht": pgettext("languageName", "Haitian"),
	# Translators: The name of a language supported by NVDA.
	"hz": pgettext("languageName", "Herero"),
	# Translators: The name of a language supported by NVDA.
	"ia": pgettext("languageName", "Interlingua (International Auxiliary Language Association)"),
	# Translators: The name of a language supported by NVDA.
	"ik": pgettext("languageName", "Inupiaq"),
	# Translators: The name of a language supported by NVDA.
	"io": pgettext("languageName", "Ido"),
	# Translators: The name of a language supported by NVDA.
	"jv": pgettext("languageName", "Javanese"),
	# Translators: The name of a language supported by NVDA.
	"kg": pgettext("languageName", "Kongo"),
	# Translators: The name of a language supported by NVDA.
	"ki": pgettext("languageName", "Kikuyu"),
	# Translators: The name of a language supported by NVDA.
	"kj": pgettext("languageName", "Kuanyama"),
	# Translators: The name of a language supported by NVDA.
	"kmr": pgettext("languageName", "Northern Kurdish"),
	# Translators: The name of a language supported by NVDA.
	"ks": pgettext("languageName", "Kashmiri"),
	# Translators: The name of a language supported by NVDA.
	"kv": pgettext("languageName", "Komi"),
	# Translators: The name of a language supported by NVDA.
	"kw": pgettext("languageName", "Cornish"),
	# Translators: The name of a language supported by NVDA.
	"lg": pgettext("languageName", "Ganda"),
	# Translators: The name of a language supported by NVDA.
	"li": pgettext("languageName", "Limburgan"),
	# Translators: The name of a language supported by NVDA.
	"ln": pgettext("languageName", "Lingala"),
	# Translators: The name of a language supported by NVDA.
	"mg": pgettext("languageName", "Malagasy"),
	# Translators: The name of a language supported by NVDA.
	"mh": pgettext("languageName", "Marshallese"),
	# Translators: The name of a language supported by NVDA.
	"mo": pgettext("languageName", "Unknown"),
	# Translators: The name of a language supported by NVDA.
	"my": pgettext("languageName", "Burmese"),
	# Translators: The name of a language supported by NVDA.
	"na": pgettext("languageName", "Nauru"),
	# Translators: The name of a language supported by NVDA.
	"ng": pgettext("languageName", "Ndonga"),
	# Translators: The name of a language supported by NVDA.
	"nr": pgettext("languageName", "South Ndebele"),
	# Translators: The name of a language supported by NVDA.
	"nv": pgettext("languageName", "Navajo"),
	# Translators: The name of a language supported by NVDA.
	"ny": pgettext("languageName", "Nyanja"),
	# Translators: The name of a language supported by NVDA.
	"oj": pgettext("languageName", "Ojibwa"),
	# Translators: The name of a language supported by NVDA.
	"os": pgettext("languageName", "Ossetian"),
	# Translators: The name of a language supported by NVDA.
	"pi": pgettext("languageName", "Pali"),
	# Translators: The name of a language supported by NVDA.
	"sc": pgettext("languageName", "Sardinian"),
	# Translators: The name of a language supported by NVDA.
	"sg": pgettext("languageName", "Sango"),
	# Translators: The name of a language supported by NVDA.
	"sh": pgettext("languageName", "Serbo-Croatian"),
	# Translators: The name of a language supported by NVDA.
	"sm": pgettext("languageName", "Samoan"),
	# Translators: The name of a language supported by NVDA.
	"sn": pgettext("languageName", "Shona"),
	# Translators: The name of a language supported by NVDA.
	"so": pgettext("languageName", "Somali"),
	# Translators: The name of a language supported by NVDA.
	"ss": pgettext("languageName", "Swati"),
	# Translators: The name of a language supported by NVDA.
	"su": pgettext("languageName", "Sundanese"),
	# Translators: The name of a language supported by NVDA.
	"tl": pgettext("languageName", "Tagalog"),
	# Translators: The name of a language supported by NVDA.
	"to": pgettext("languageName", "Tonga (Tonga Islands)"),
	# Translators: The name of a language supported by NVDA.
	"tw": pgettext("languageName", "Twi"),
	# Translators: The name of a language supported by NVDA.
	"ty": pgettext("languageName", "Tahitian"),
	# Translators: The name of a language supported by NVDA.
	"vo": pgettext("languageName", "Volap�k"),
	# Translators: The name of a language supported by NVDA.
	"wa": pgettext("languageName", "Walloon"),
	# Translators: The name of a language supported by NVDA.
	"za": pgettext("languageName", "Zhuang"),
}
