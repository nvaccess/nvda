# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

DEFAULT_TEXT_PARAGRAPH_REGEX = (
	r"({lookBehind}{optQuote}{punc}{optQuote}{optWiki}{lookAhead}|{punc2}|{cjk})".format(
		# Look behind clause ensures that we have a text character before text punctuation mark.
		# We have a positive lookBehind \w that resolves to a text character in any language,
		# coupled with negative lookBehind \d that excludes digits.
		lookBehind=r'(?<=\w)(?<!\d)',
		# In some cases quote or closing parenthesis might appear right before or right after text punctuation.
		# For example:
		# > He replied, "That's wonderful."
		optQuote=r'["”»)]?',
		# Actual punctuation marks that suggest end of sentence.
		# We don't include symbols like comma and colon, because of too many false positives.
		# We include question mark and exclamation mark below in punc2.
		punc=r'[.…]{1,3}',
		# On Wikipedia references appear right after period in sentences, the following clause takes this
		# into account. For example:
		# > On his father's side, he was a direct descendant of John Churchill.[3]
		optWiki=r'(\[\d+\])*',
		# LookAhead clause checks that punctuation mark must be followed by either space,
		# or newLine symbol or end of string.
		lookAhead=r'(?=[\r\n  ]|$)',
		# Include question mark and exclamation mark with no extra conditions,
		# since they don't trigger as many false positives.
		punc2=r'[?!]',
		# We also check for CJK full-width punctuation marks without any extra rules.
		cjk=r'[．！？：；]',
	)
)
