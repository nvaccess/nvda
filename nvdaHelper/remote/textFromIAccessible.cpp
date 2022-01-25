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
#include <vector>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <atlcomcli.h>
#include <ia2.h>
#include <common/ia2utils.h>

using namespace std;
auto constexpr OBJ_REPLACEMENT_CHAR = L'\xfffc';


bool isEmpty(CComBSTR& val) {
	if (!val) {
		return true;
	}
	for (int i = 0; val[i] != L'\0'; ++i) {
		if (val[i] != OBJ_REPLACEMENT_CHAR && !iswspace(val[i])) {
			return false;
		}
	}
	return true;
}

bool appendNameDescription(CComPtr<IAccessible> pacc, wstring& textBuf) {
	bool gotText = false;
	CComVariant varChild;
	varChild.vt = VT_I4;
	varChild.lVal = 0;

	CComBSTR val;
	pacc->get_accName(varChild, &val);
	bool valEmpty = isEmpty(val);
	if (!valEmpty) {
		gotText = true;
		textBuf.append(val);
		textBuf.append(L" ");
	}

	val = nullptr;
	pacc->get_accDescription(varChild, &val);
	valEmpty = isEmpty(val);
	if (!valEmpty) {
		gotText = true;
		textBuf.append(val);
	}
	return gotText;
}


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
	CComQIPtr<IAccessibleText> paccText(pacc2);

	if (!paccText && recurse && !useNewText) {
		//no IAccessibleText interface, so try children instead
		long childCount = 0;
		if (!useNewText && pacc2->get_accChildCount(&childCount) == S_OK && childCount > 0) {
			auto[varChildren, accChildRes] = getAccessibleChildren(pacc2, 0, childCount);
			for(auto& child : varChildren){
				if (child.vt == VT_DISPATCH && child.pdispVal) {
					CComQIPtr<IAccessible2> pacc2Child(child.pdispVal);
					if (pacc2Child) {
						map<wstring, wstring> childAttribsMap;
						fetchIA2Attributes(pacc2Child, childAttribsMap);
						auto liveItr = childAttribsMap.find(L"live");
						if (liveItr == childAttribsMap.end() || liveItr->second.compare(L"off") != 0) {
							gotText |= getTextFromIAccessible(
								textBuf,
								pacc2Child,
								false, // useNewText
								true, // recurse
								true // includeTopLevelText
							);
						}
					}
				}
			}
		}
	}
	else if (paccText) {
		//We can use IAccessibleText because it exists
		CComBSTR bstrText;
		long startOffset = 0;
		//If requested, get the text from IAccessibleText::newText rather than just IAccessibleText::text.
		if (useNewText) {
			IA2TextSegment newSeg {};
			if (S_OK == paccText->get_newText(&newSeg) && newSeg.text) {
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
			CComQIPtr<IAccessibleHypertext> paccHypertext;
			if (recurse) {
				paccHypertext = pacc2;
			}
			for (long index = 0; index < textLength; ++index) {
				wchar_t realChar = bstrText[index];
				bool charAdded = false;
				if (realChar == OBJ_REPLACEMENT_CHAR) {
					const long charIndex = startOffset + index;
					long hyperlinkIndex = 0;
					if (paccHypertext && paccHypertext->get_hyperlinkIndex(charIndex, &hyperlinkIndex) == S_OK) {
						CComPtr<IAccessibleHyperlink> paccHyperlink;
						if (S_OK == paccHypertext->get_hyperlink(hyperlinkIndex, &paccHyperlink)) {
							CComQIPtr <IAccessible2> pacc2Child(paccHyperlink);
							if (pacc2Child) {
								map<wstring, wstring> childAttribsMap;
								fetchIA2Attributes(pacc2Child, childAttribsMap);
								auto liveItr = childAttribsMap.find(L"live");
								if (liveItr == childAttribsMap.end() || liveItr->second != L"off") {
									if (getTextFromIAccessible(textBuf, pacc2Child)) {
										gotText = true;
									}
								}
								charAdded = true;
							}
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
			textBuf.append(1, L' ');
		}
	}
	if (!gotText && !useNewText) {
		//We got no text from IAccessibleText interface or children, so try name and/or description
		gotText = appendNameDescription(pacc2, textBuf);
	}
	return gotText;
}
