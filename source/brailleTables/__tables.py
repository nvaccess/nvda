# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2024 NV Access Limited, Joseph Lee, Babbage B.V., Julien Cochuyt, Leonard de Ruijter

"""Contains the braille table definitions as used in NVDA.
Note that importing this module for the first time will add all tables to the internal table store.
"""

from . import addTable

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("afr-za-g1.ctb", _("Afrikaans grade 1"), inputForLangs={"af_ZA"}, outputForLangs={"af_ZA"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("afr-za-g2.ctb", _("Afrikaans grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("akk.utb", _("Akkadian (US) grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("akk-borger.utb", _("Akkadian (Borger) grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ar-ar-comp8.utb", _("Arabic 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ar-ar-g1.utb", _("Arabic grade 1"), inputForLangs={"ar"}, outputForLangs={"ar"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ar-ar-g2.ctb", _("Arabic grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("as-in-g1.utb", _("Assamese grade 1"), inputForLangs={"as"}, outputForLangs={"as"})
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
addTable("bel.utb", _("Belarusian literary braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("bel-detailed.utb", _("Belarusian literary braille (detailed)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("bg.ctb", _("Bulgarian 8 dot computer braille"), inputForLangs={"bg"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("bg.utb", _("Bulgarian grade 1"), outputForLangs={"bg"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ca-g1.ctb", _("Catalan grade 1"), inputForLangs={"ca"}, outputForLangs={"ca"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ckb-g1.ctb", _("Central Kurdish grade 1"), inputForLangs={"ckb"}, outputForLangs={"ckb"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cop-eg-comp8.utb", _("Coptic 8 dot computer braille"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cop.utb", _("Coptic grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cuneiform-transliterated.utb", _("Cuneiform (transliterated) grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("cuneiform-transliterated-compact.utb", _("Cuneiform (transliterated, compact diacritics) grade 1"))
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
addTable("cs-g1.ctb", _("Czech grade 1"), inputForLangs={"cs"}, outputForLangs={"cs"})

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g08.ctb", _("Danish 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g08_1993.ctb", _("Danish 8 dot computer braille (1993)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g16.ctb", _("Danish 6 dot grade 1"), inputForLangs={"da"}, outputForLangs={"da"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g16_1993.ctb", _("Danish 6 dot grade 1 (1993)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g18.ctb", _("Danish 8 dot grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g18_1993.ctb", _("Danish 8 dot grade 1 (1993)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g26.ctb", _("Danish 6 dot grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g26_1993.ctb", _("Danish 6 dot grade 2 (1993)"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g28.ctb", _("Danish 8 dot grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("da-dk-g28_1993.ctb", _("Danish 8 dot grade 2 (1993)"), contracted=True)

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
addTable("de-g1.ctb", _("German grade 1"), input=False, outputForLangs={"de"})

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g1-detailed.ctb", _("German grade 1 (detailed)"), inputForLangs={"de"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g2.ctb", _("German grade 2"), contracted=True, input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("de-g2-detailed.ctb", _("German grade 2 (detailed)"), contracted=True, input=False)

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("el.ctb", _("Greek (Greece)"), inputForLangs={"el"}, outputForLangs={"el"})
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
addTable(
	"Es-Es-G0.utb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Spanish 8 dot computer braille"),
	inputForLangs={"es", "gl"},
	outputForLangs={"es", "gl"},
)
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
addTable("ethio-g1.ctb", _("Ethiopic grade 1"), inputForLangs={"am"}, outputForLangs={"am"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fa-ir-comp8.ctb", _("Persian 8 dot computer braille"), inputForLangs={"fa"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fa-ir-g1.utb", _("Persian grade 1"), outputForLangs={"fa"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fi.utb", _("Finnish 6 dot"))
addTable(
	"fi-fi-8dot.ctb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Finnish 8 dot computer braille"),
	inputForLangs={"fi"},
	outputForLangs={"fi"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fil-g2.ctb", _("Filipino grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fr-bfu-comp6.utb", _("French (unified) 6 dot computer braille"))
addTable(
	"fr-bfu-comp8.utb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("French (unified) 8 dot computer braille"),
	inputForLangs={"fr"},
	outputForLangs={"fr"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("fr-bfu-g2.ctb", _("French (unified) grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ga-g1.utb", _("Irish grade 1"), inputForLangs={"ga"}, outputForLangs={"ga"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ga-g2.ctb", _("Irish grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("gu-in-g1.utb", _("Gujarati grade 1"), inputForLangs={"gu"}, outputForLangs={"gu"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("grc-international-en.utb", _("Greek international braille (2-cell accented letters)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("grc-international-en-composed.utb", _("Greek international braille (single-cell accented letters)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("grc-international-es.utb", _("Spanish for Greek text"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hbo.utb", _("Hebrew (Biblical) IHBC"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hbo-cantillated.utb", _("Hebrew (Biblical) full cantillation"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hbo-slim.utb", _("Hebrew (Biblical) Slim"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("he-IL.utb", _("Israeli grade 1"))
addTable(
	"he-IL-comp8.utb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Hebrew computer braille"),
	inputForLangs={"he"},
	outputForLangs={"he"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hi-in-g1.utb", _("Hindi grade 1"), inputForLangs={"hi"}, outputForLangs={"hi"})
addTable(
	"hr-comp8.utb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Croatian 8 dot computer braille"),
	inputForLangs={"hr"},
	outputForLangs={"hr"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hr-g1.ctb", _("Croatian grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hu-hu-comp8.ctb", _("Hungarian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hu-hu-g1.ctb", _("Hungarian grade 1"), inputForLangs={"hu"}, outputForLangs={"hu"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("hu-hu-g2.ctb", _("Hungarian grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("is.ctb", _("Icelandic 8 dot computer braille"), inputForLangs={"is"}, outputForLangs={"is"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("IPA.utb", _("International Phonetic Alphabet"), input=False)
addTable(
	"it-it-comp6.utb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Italian 6 dot computer braille"),
	inputForLangs={"it"},
	outputForLangs={"it"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("it-it-comp8.utb", _("Italian 8 dot computer braille"))

addTable(
	"ja-kantenji.utb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Japanese (Kantenji) literary braille"),
	input=False,
	outputForLangs={"ja"},
)
addTable(
	"ja-rokutenkanji.utb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Japanese (Rokuten Kanji) Braille"),
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ka-in-g1.utb", _("Kannada grade 1"), inputForLangs={"kn"}, outputForLangs={"kn"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ka.utb", _("Georgian literary braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("kk.utb", _("Kazakh grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("km-g1.utb", _("Khmer grade 1"), inputForLangs={"km"}, outputForLangs={"km"})
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
addTable("ko-g1.ctb", _("Korean grade 1"), inputForLangs={"ko"}, outputForLangs={"ko"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ko-g2.ctb", _("Korean grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ks-in-g1.utb", _("Kashmiri grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("lo-g1.utb", _("Lao Grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("lg-ug-g1.utb", _("Luganda literary braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("lt-8dot.utb", _("Lithuanian 8 dot"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("lt-6dot.utb", _("Lithuanian 6 dot"), inputForLangs={"lt"}, outputForLangs={"lt"})
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
addTable("mn-MN-g1.utb", _("Mongolian grade 1"), inputForLangs={"mn"}, outputForLangs={"mn"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("mn-MN-g2.ctb", _("Mongolian grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("mr-in-g1.utb", _("Marathi grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("my-g1.utb", _("Burmese grade 1"), inputForLangs={"my"}, outputForLangs={"my"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("my-g2.ctb", _("Burmese grade 2"), contracted=True, input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nl-NL-g0.utb", _("Dutch 6 dot"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nl-comp8.utb", _("Dutch 8 dot"), inputForLangs={"nl"}, outputForLangs={"nl"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("no-no-8dot.utb", _("Norwegian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g0.utb", _("Norwegian grade 0"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g1.ctb", _("Norwegian grade 1"), inputForLangs={"nb_NO"}, outputForLangs={"nb_NO"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g2.ctb", _("Norwegian grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("No-No-g3.ctb", _("Norwegian grade 3"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("np-in-g1.utb", _("Nepali grade 1"), inputForLangs={"ne"}, outputForLangs={"ne"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nso-za-g1.utb", _("Sepedi grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("nso-za-g2.ctb", _("Sepedi grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ny-mw.utb", _("Chichewa (Malawi) literary braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("or-in-g1.utb", _("Oriya grade 1"))
addTable(
	"pl-pl-comp8.ctb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	_("Polish 8 dot computer braille"),
	inputForLangs={"pl"},
	outputForLangs={"pl"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Pl-Pl-g1.utb", _("Polish literary braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("pt-comp6.utb", _("Portuguese 6 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("pt-pt-comp8.ctb", _("Portuguese 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Pt-Pt-g1.utb", _("Portuguese grade 1"), inputForLangs={"pt"}, outputForLangs={"pt"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("Pt-Pt-g2.ctb", _("Portuguese grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("pu-in-g1.utb", _("Punjabi grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ro-g0.utb", _("Romanian 6 dot"), inputForLangs={"ro"}, outputForLangs={"ro"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ro.ctb", _("Romanian"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-comp6.utb", _("Russian 6 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-comp8.utb", _("Russian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-litbrl.ctb", _("Russian literary braille"), inputForLangs={"ru"}, outputForLangs={"ru"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-litbrl-detailed.utb", _("Russian literary braille (detailed)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ru-ru-g1.ctb", _("Russian contracted braille"), contracted=True, input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("rw-rw-g1.utb", _("Kinyarwanda literary braille"))
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
addTable("sk-g1.ctb", _("Slovak grade 1"), inputForLangs={"sk"}, outputForLangs={"sk"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sl-si-comp8.ctb", _("Slovenian 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sl-si-g1.utb", _("Slovenian grade 1"), inputForLangs={"sl"}, outputForLangs={"sl"})
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
addTable("sr-Cyrl.ctb", _("Serbian Cyrillic grade 1"))

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sv-g0.utb", _("Swedish uncontracted braille"), input=False, outputForLangs={"sv"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sv-g1.ctb", _("Swedish partially contracted braille"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sv-g2.ctb", _("Swedish contracted braille"), contracted=True, input=False)

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sw-ke-g1.utb", _("Swahili (Kenya) grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sw-ke-g1-2.ctb", _("Swahili (Kenya) grade 1.2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sw-ke-g1-3.ctb", _("Swahili (Kenya) grade 1.3"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sw-ke-g1-4.ctb", _("Swahili (Kenya) grade 1.4"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sw-ke-g1-5.ctb", _("Swahili (Kenya) grade 1.5"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("sw-ke-g2.ctb", _("Swahili (Kenya) Grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("syc.utb", _("Syriac grade 1"))

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ta-ta-g1.ctb", _("Tamil grade 1"), inputForLangs={"ta"}, outputForLangs={"ta"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tt.utb", _("Tatar grade 1"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("te-in-g1.utb", _("Telugu grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("th-comp8-backward.utb", _("Thai 8 dot computer braille"), output=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("th-g0.utb", _("Thai grade 0"), input=False)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("th-g1.utb", _("Thai grade 1"), input=False, contracted=True, outputForLangs={"th"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("th-g2.ctb", _("Thai grade 2"), input=False, contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tr.ctb", _("Turkish 8 dot computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tr-g1.ctb", _("Turkish grade 1"), inputForLangs={"tr"}, outputForLangs={"tr"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tr-g2.ctb", _("Turkish grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tsn-za-g1.ctb", _("Setswana grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("tsn-za-g2.ctb", _("Setswana grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("uga.utb", _("Ugaritic grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("uk.utb", _("Ukrainian grade 1"), inputForLangs={"uk"}, outputForLangs={"uk"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("uk-detailed.utb", _("Ukrainian literary braille (detailed)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("uk-comp.utb", _("Ukrainian computer braille"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ur-pk-g1.utb", _("Urdu grade 1"), inputForLangs={"ur"}, outputForLangs={"ur"})
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
addTable("vi-vn-g0.utb", _("Vietnamese grade 0"), inputForLangs={"vi"})
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ve-za-g1.utb", _("Tshivenda grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("ve-za-g2.ctb", _("Tshivenda grade 2"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("vi-vn-g1.ctb", _("Vietnamese grade 1"), input=False, outputForLangs={"vi"})
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
addTable("yi.utb", _("Yiddish grade 1"))
addTable(
	"zhcn-cbs.ctb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	# This should be translated to '中文中国汉语通用盲文' in Mandarin.
	_("Chinese common braille (simplified Chinese characters)"),
	input=False,
	outputForLangs={"zh_CN"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
# This should be translated to '中文中国汉语现行盲文（无声调）' in Mandarin.
addTable("zh-chn.ctb", _("Chinese (China, Mandarin) Current Braille System (no tones)"))

addTable(
	"zhcn-g1.ctb",
	# Translators: The name of a braille table displayed in the
	# braille settings dialog.
	# This should be translated to '中文中国汉语现行盲文' in Mandarin.
	_("Chinese (China, Mandarin) Current Braille System"),
	inputForLangs={"zh_HK"},
	outputForLangs={"zh_HK"},
)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
# This should be translated to '中文中国汉语双拼盲文' in Mandarin.
addTable("zhcn-g2.ctb", _("Chinese (China, Mandarin) Double-phonic Braille System"), contracted=True)
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zh-hk.ctb", _("Chinese (Hong Kong, Cantonese)"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zh-tw.ctb", _("Chinese (Taiwan, Mandarin)"), inputForLangs={"zh_TW"}, outputForLangs={"zh_TW"})

# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zu-za-g1.utb", _("Zulu grade 1"))
# Translators: The name of a braille table displayed in the
# braille settings dialog.
addTable("zu-za-g2.ctb", _("Zulu grade 2"), contracted=True)
