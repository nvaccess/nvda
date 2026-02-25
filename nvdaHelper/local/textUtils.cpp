/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2008-2019 NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <windows.h>
#include <usp10.h>
#include <vector>
#include <common/log.h>

using namespace std;

enum UNIT {
	UNIT_CHARACTER,
	UNIT_WORD
};

vector<SCRIPT_LOGATTR> _getLogAttrArray(const wchar_t* text, int textLength) {
	if (textLength <= 0 || !text) {
		return {};
	}
	// It is invalid to call ScriptItemize with a buffer to hold less than two SCRIPT_ITEM structures.
	auto cMaxItems = textLength + 1;
	// The buffer should be (cMaxItems + 1)
	vector<SCRIPT_ITEM> items(cMaxItems + 1);
	int numItems = 0;
	HRESULT hr;
	if ((hr = ScriptItemize(text, textLength, cMaxItems, nullptr, nullptr, items.data(), &numItems)) != S_OK || numItems == 0) {
		LOG_ERROR(L"ScriptItemize failed for text '" << text << L"'; hr=" << hr);
		return {};
	}

	vector<SCRIPT_LOGATTR> logAttrArray(textLength);
	// The function always adds a terminal item to the item analysis array.
	// numItems contains the number of actually processed items excluding the terminating item.
	int nextICharPos = textLength;  // should be equal to items[numItems].iCharPos
	for (int itemIndex = numItems - 1; itemIndex >= 0; --itemIndex) {
		int iCharPos = items[itemIndex].iCharPos;
		int iCharLength = nextICharPos - iCharPos;
		if ((hr = ScriptBreak(text + iCharPos, iCharLength, &(items[itemIndex].a), logAttrArray.data() + iCharPos)) != S_OK) {
			LOG_ERROR(L"ScriptBreak failed for text '" << text << L"' at run " << itemIndex << L"; hr=" << hr);
			return {};
		}
		// Note, ideally we'd set nextICharPos to iCharPos, so that the
		// next iteration of the loop will only call ScriptBreak for the text that belongs to the current item.
		// Now that we don't do this, every call of ScriptBreak refills logAttrArray
		// for the characters after this item based on the SCRIPT_ANALYSIS for the current item,
		// effectively treating all the characters as belonging to the script at itemIndex = 0.
		// However, resetting nextICharPos causes word segmentation to differ from the one used in notepad.
	}
	return logAttrArray;
}

bool calculateCharacterBoundaries(const wchar_t* text, int textLength, int* offsets, int* offsetsCount) {
	if (!offsets) {
		return false;
	}
	vector<SCRIPT_LOGATTR> logAttrArray = _getLogAttrArray(text, textLength);
	if (logAttrArray.empty()) {
		return false;
	}
	int count = 0;
	for (int i = 0; i <= textLength; ++i) {
		if (i == 0 || i == textLength || logAttrArray[i].fCharStop) {
			offsets[count++] = i;
		}
	}
	*offsetsCount = count;
	return true;
}

bool _calculateUniscribeOffsets(enum UNIT unit, wchar_t* text, int textLength, int offset, int* startOffset, int* endOffset) {
	if(unit!=UNIT_CHARACTER&&unit!=UNIT_WORD) {
		LOG_ERROR(L"Unsupported unit");
		return false;
	}
	if (offset < 0 || !text) {
		return false;
	}
	if (offset >= textLength) {
		*startOffset = offset;
		*endOffset = offset + 1;
		return true;
	}
	vector<SCRIPT_LOGATTR> logAttrArray = _getLogAttrArray(text, textLength);
	if (logAttrArray.empty()) {
		return false;
	}
	if(unit==UNIT_CHARACTER) {
		for(int i=offset;i>=0;--i) {
			if (logAttrArray[i].fCharStop) {
				*startOffset=i;
				break;
			}
		}
		*endOffset = textLength;
		for(int i=offset+1;i<textLength;++i) {
			if (logAttrArray[i].fCharStop) {
				*endOffset=i;
				break;
			}
		}
	} else if(unit==UNIT_WORD) {
		for(int i=offset;i>=0;--i) {
			if(logAttrArray[i].fWordStop) {
				*startOffset=i;
				break;
			}
		}
		// #1656: fWordStop doesn't seem to stop on whitespace where punctuation follows the whitespace.
		bool skipWhitespace=true;
		for(int i=offset;i>=*startOffset;--i) {
			if(iswspace(text[i])) {
				if(skipWhitespace) {
					// If we start in a block of whitespace, the word must start before this,
					// as whitespace is included at the end of a word.
					// Therefore, skip the whitespace and keep searching.
					continue;
				}
				// This is whitespace. The word starts after it.
				*startOffset=i+1;
				break;
			} else
				skipWhitespace=false;
		}
		*endOffset=textLength;
		for(int i=offset+1;i<textLength;++i) {
			if(logAttrArray[i].fWordStop) {
				*endOffset=i;
				break;
			}
		}
		// #1656: fWordStop doesn't seem to stop on whitespace where punctuation follows the whitespace.
		for(int i=offset;i<*endOffset;++i) {
			if(iswspace(text[i])) {
				// This begins a block of whitespace. The word ends after it.
				// Find the end of the whitespace.
				for(;i<*endOffset;++i) {
					if(!iswspace(text[i]))
						break;
				}
				// We're now positioned on the first non-whitespace character,
				// so the word ends here.
				*endOffset=i;
				break;
			}
		}
	}
	return true;
}

bool calculateWordOffsets(wchar_t* text, int textLength, int offset, int* startOffset, int* endOffset) {
	return _calculateUniscribeOffsets(UNIT_WORD, text, textLength, offset, startOffset, endOffset);
}

bool calculateCharacterOffsets(wchar_t* text, int textLength, int offset, int* startOffset, int* endOffset) {
	return _calculateUniscribeOffsets(UNIT_CHARACTER, text, textLength, offset, startOffset, endOffset);
}
