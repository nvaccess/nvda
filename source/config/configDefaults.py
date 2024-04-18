# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import json


DEFAULT_TEXT_PARAGRAPH_REGEX = (
	r"^|({plb}{nlb}{optQuote}{dot}{optQuote}|{punc2}{optQuote}|{cjk}){optWiki}{spaces}|{n2}|\Z".format(
		# Look behind clause ensures that we have a text character before text punctuation mark.
		# We have a positive lookBehind \w that resolves to a text character in any language,
		# coupled with negative lookBehind \d that excludes digits.
		plb=r"(?<=\w)(?<!\d)",
		# Language-specific exceptions: characters suggesting that the following dot is not indicative
		# of a sentence stop.
		# This is a negative look-behind and will be inserted later when language is specified.
		nlb="{nonBreakingRegex}",
		# In some cases quote or closing parenthesis might appear right before or right after text punctuation.
		# For example:
		# > He replied, "That's wonderful."
		optQuote=r'["”»)]?',
		# Actual punctuation marks that suggest end of sentence.
		# We don't include symbols like comma and colon, because of too many false positives.
		# We include question mark and exclamation mark below in punc2.
		dot=r"[.]{{1,3}}",
		# On Wikipedia references appear right after period in sentences, the following clause takes this
		# into account. For example:
		# > On his father's side, he was a direct descendant of John Churchill.[3]
		optWiki=r"(\[\d+\])*",
		# spaces clause checks that punctuation mark must be followed by either space,
		# or newLine symbol or end of string.
		spaces=r"([  ]+|([  \t]*\n)+|$)",
		# Include question mark and exclamation mark with no extra conditions,
		# since they don't trigger as many false positives.
		punc2=r"[?!…]",
		# We also check for CJK full-width punctuation marks without any extra rules.
		cjk=r"[。．！？]",
		# Double newline means end of sentence too.
		n2=r"([  \t]*\n){{2,}}",
	)
)


nonBreakingPrefix = json.dumps({
	"en": r"\b[A-Z]|\bMr|\bMs|\bMrs|\bDr|\bProf|\bSt|\be.g|\bi.e",
	"ru": r"\b[A-ZА-Я]|\b[Тт]ов|\b[Уу]л|\bт.[ке]|\bт. [ке]",
})
