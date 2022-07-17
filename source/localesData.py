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
	"an": pgettext("languageName", "Aragonese"),
	# Translators: The name of a language supported by NVDA.
	"ckb": pgettext("languageName", "Central Kurdish"),
	# Translators: The name of a language supported by NVDA.
	"kmr": pgettext("languageName", "Northern Kurdish"),
	# Translators: The name of a language supported by NVDA.
	"my": pgettext("languageName", "Burmese"),
	# Translators: The name of a language supported by NVDA.
	"so": pgettext("languageName", "Somali"),
}
