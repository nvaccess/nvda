/*
This file is a part of the NVDA project.
Copyright 2006-2021 NV Access Limited
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License version 2.0, as published by
	the Free Software Foundation.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include "textFromIAccessible.h"
#include <string>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <atlcomcli.h>
#include <ia2.h>
#include <common/ia2utils.h>

using namespace std;
auto constexpr OBJ_REPLACEMENT_CHAR = L'\xfffc';


bool getTextFromIAccessible(
	wstring& textBuf,
	IAccessible2* pacc2,
	bool useNewText,
	bool recurse,
	bool includeTopLevelText
) {
	if (!pacc2) {
		return false;
	}

	bool gotText = false;
	CComQIPtr<IAccessibleText, &IID_IAccessibleText> paccText(pacc2);

	if (!paccText && recurse && !useNewText) {
		//no IAccessibleText interface, so try children instead
		long childCount = 0;
		if (!useNewText && pacc2->get_accChildCount(&childCount) == S_OK && childCount > 0) {
			VARIANT* varChildren = new VARIANT[childCount];
			AccessibleChildren(pacc2, 0, childCount, varChildren, &childCount);
			for (int i = 0; i < childCount; ++i) {
				if (varChildren[i].vt == VT_DISPATCH) {
					IAccessible2* pacc2Child = NULL;
					if (varChildren[i].pdispVal && varChildren[i].pdispVal->QueryInterface(IID_IAccessible2, (void**)&pacc2Child) == S_OK) {
						map<wstring, wstring> childAttribsMap;
						fetchIA2Attributes(pacc2Child, childAttribsMap);
						auto liveItr = childAttribsMap.find(L"live");
						if (liveItr == childAttribsMap.end() || liveItr->second.compare(L"off") != 0) {
							if (getTextFromIAccessible(textBuf, pacc2Child)) {
								gotText = true;
							}
						}
						pacc2Child->Release();
					}
				}
				VariantClear(varChildren + i);
			}
			delete[] varChildren;
		}
	}
	else if (paccText) {
		//We can use IAccessibleText because it exists
		BSTR bstrText = NULL;
		long startOffset = 0;
		//If requested, get the text from IAccessibleText::newText rather than just IAccessibleText::text.
		if (useNewText) {
			IA2TextSegment newSeg = { 0 };
			if (paccText->get_newText(&newSeg) == S_OK && newSeg.text) {
				bstrText = newSeg.text;
				startOffset = newSeg.start;
			}
		}
		else {
			paccText->get_text(0, IA2_TEXT_OFFSET_LENGTH, &bstrText);
		}
		//If we got text, add it to  the string provided, however if there are embedded objects in the text, recurse in to these
		if (bstrText) {
			long textLength = SysStringLen(bstrText);
			IAccessibleHypertext* paccHypertext = NULL;
			if (!recurse || pacc2->QueryInterface(IID_IAccessibleHypertext, (void**)&paccHypertext) != S_OK) paccHypertext = NULL;
			for (long index = 0; index < textLength; ++index) {
				wchar_t realChar = bstrText[index];
				bool charAdded = false;
				if (realChar == OBJ_REPLACEMENT_CHAR) {
					long hyperlinkIndex;
					if (paccHypertext && paccHypertext->get_hyperlinkIndex(startOffset + index, &hyperlinkIndex) == S_OK) {
						IAccessibleHyperlink* paccHyperlink = NULL;
						if (paccHypertext->get_hyperlink(hyperlinkIndex, &paccHyperlink) == S_OK) {
							IAccessible2* pacc2Child = NULL;
							if (paccHyperlink->QueryInterface(IID_IAccessible2, (void**)&pacc2Child) == S_OK) {
								map<wstring, wstring> childAttribsMap;
								fetchIA2Attributes(pacc2Child, childAttribsMap);
								auto liveItr = childAttribsMap.find(L"live");
								if (liveItr == childAttribsMap.end() || liveItr->second.compare(L"off") != 0) {
									if (getTextFromIAccessible(textBuf, pacc2Child)) {
										gotText = true;
									}
								}
								charAdded = true;
								pacc2Child->Release();
							}
							paccHyperlink->Release();
						}
					}
				}
				if (!charAdded && includeTopLevelText) {
					textBuf.append(1, realChar);
					charAdded = true;
					if (realChar != OBJ_REPLACEMENT_CHAR && !iswspace(realChar)) {
						gotText = true;
					}
				}
			}
			if (paccHypertext) paccHypertext->Release();
			SysFreeString(bstrText);
			textBuf.append(1, L' ');
		}
	}
	if (!gotText && !useNewText) {
		//We got no text from IAccessibleText interface or children, so try name and/or description
		BSTR val = NULL;
		bool valEmpty = true;
		VARIANT varChild;
		varChild.vt = VT_I4;
		varChild.lVal = 0;
		pacc2->get_accName(varChild, &val);
		if (val) {
			for (int i = 0; val[i] != L'\0'; ++i) {
				if (val[i] != OBJ_REPLACEMENT_CHAR && !iswspace(val[i])) {
					valEmpty = false;
					break;
				}
			}
			if (!valEmpty) {
				gotText = true;
				textBuf.append(val);
				textBuf.append(L" ");
			}
			SysFreeString(val);
			val = NULL;
		}
		valEmpty = true;
		pacc2->get_accDescription(varChild, &val);
		if (val) {
			for (int i = 0; val[i] != L'\0'; ++i) {
				if (val[i] != OBJ_REPLACEMENT_CHAR && !iswspace(val[i])) {
					valEmpty = false;
					break;
				}
			}
			if (!valEmpty) {
				gotText = true;
				textBuf.append(val);
			}
			SysFreeString(val);
		}
	}
	return gotText;
}
