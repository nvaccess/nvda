# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

# Punctuation that should NOT have a separator BEFORE it (no space before these marks)
NO_SEP_BEFORE = {
	# Common Chinese fullwidth punctuation
	"。",
	"，",
	"、",
	"；",
	"：",
	"？",
	"！",
	"…",
	"...",
	"—",
	"–",
	"——",
	"）",
	"】",
	"》",
	"〉",
	"」",
	"』",
	"”",
	"’",
	"％",
	"‰",
	"￥",
	# Common ASCII / halfwidth punctuation
	".",
	",",
	";",
	":",
	"?",
	"!",
	"%",
	".",
	")",
	"]",
	"}",
	">",
	'"',
	"'",
}

# Punctuation that should NOT have a separator AFTER it (no space after these marks)
NO_SEP_AFTER = {
	# Common Chinese fullwidth opening/leading punctuation
	"（",
	"【",
	"《",
	"〈",
	"「",
	"『",
	"“",
	"‘",
	# Common ASCII / halfwidth opening/leading punctuation
	"(",
	"[",
	"{",
	"<",
	'"',
	"'",
	# Currency and prefix-like symbols that typically bind to the following token
	"$",
	"€",
	"£",
	"¥",
	"₹",
	# Social/identifier prefixes
	"@",
	"#",
	"&",
}
