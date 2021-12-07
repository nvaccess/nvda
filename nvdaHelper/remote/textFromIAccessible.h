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
#include <string>

#ifndef IA2TEXTFROMIACCESSIBLE_H
#define IA2TEXTFROMIACCESSIBLE_H
struct IAccessible2;

/* getTextFromIAccessible
* Summarizes the text for an IAccessible
* @param textBuf: An out-param, the string to fill with the text from the IAccessible
* @param pacc2: The IAccessible2 object to get the text from.
* @param useNewText: Only valid during an in-process winEvent callback (ie text changed). Specifies
*    to use the new text (ie post change) should be used instead of the old text.
* @param recurse: Should text from child objects also be gathered.
* @param includeTopLevelText: If true, text from the top level pacc2 should be included.
* @return: true if text was collected.
*/
bool getTextFromIAccessible(
    std::wstring& textBuf,
    IAccessible2* pacc2,
    bool useNewText = false,
    bool recurse = true,
    bool includeTopLevelText = true
);

#endif  // IA2TEXTFROMIACCESSIBLE_H
