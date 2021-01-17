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
#include <common/log.h>

enum UNIT {
	UNIT_CHARACTER,
	UNIT_WORD
};

bool _calculateUniscribeOffsets(enum UNIT unit, wchar_t* text, int textLength, int offset, int* startOffset, int* endOffset) {
	if(unit!=UNIT_CHARACTER&&unit!=UNIT_WORD) {
		LOG_ERROR(L"Unsupported unit");
		return false;
	}
	if(textLength<=0) return false;
	if(offset<0) return false;
	if(offset>=textLength) {
		*startOffset=offset;
		*endOffset=offset+1;
		return true;
	}
	SCRIPT_ITEM* pItems=new SCRIPT_ITEM[textLength+1];
	int numItems=0;
	if(ScriptItemize(text,textLength,textLength,NULL,NULL,pItems,&numItems)!=S_OK||numItems==0) {
		delete[] pItems;
		return false;
	}
	SCRIPT_LOGATTR* logAttrArray=new SCRIPT_LOGATTR[textLength];
	int nextICharPos=textLength;
	for(int itemIndex=numItems-1;itemIndex>=0;--itemIndex) {
		int iCharPos=pItems[itemIndex].iCharPos;
		int iCharLength=nextICharPos-iCharPos;
		if(ScriptBreak(text+iCharPos,iCharLength,&(pItems[itemIndex].a),logAttrArray+iCharPos)!=S_OK) {
			delete[] pItems;
			delete[] logAttrArray;
			return false;
		}
	}
	delete[] pItems;
	if(unit==UNIT_CHARACTER) {
		for(int i=offset;i>=0;--i) {
			if(logAttrArray[i].fCharStop) {
				*startOffset=i;
				break;
			}
		}
		for(int i=offset+1;i<textLength;++i) {
			if(logAttrArray[i].fCharStop) {
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
	delete[] logAttrArray;
	return true;
}

bool calculateWordOffsets(wchar_t* text, int textLength, int offset, int* startOffset, int* endOffset) {
	return _calculateUniscribeOffsets(UNIT_WORD, text, textLength, offset, startOffset, endOffset);
}

bool calculateCharacterOffsets(wchar_t* text, int textLength, int offset, int* startOffset, int* endOffset) {
	return _calculateUniscribeOffsets(UNIT_CHARACTER, text, textLength, offset, startOffset, endOffset);
}
