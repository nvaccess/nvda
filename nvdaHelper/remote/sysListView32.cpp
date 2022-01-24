/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2022 NV Access Limited, Leonard de Ruijter.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#define WIN32_LEAN_AND_MEAN 

#include <windows.h>
#include <commctrl.h>
#include <algorithm>
#include <iterator>
#include <common/log.h>
#include <remote/nvdaInProcUtils.h>

// #7828: Windows headers define this as 260 characters.
// However this is not long enough for modern Twitter clients that need at least 280 characters.
// Therefore, round it up to the nearest power of 2.
#undef CBEMAXSTRLEN
#define CBEMAXSTRLEN 512

using namespace std;

error_status_t nvdaInProcUtils_sysListView32_getGroupInfo(handle_t bindingHandle, const unsigned long windowHandle, int groupIndex, BSTR* header, BSTR* footer, int* state) {
	LVGROUP group={0};
	group.cbSize=sizeof(group);
	group.mask=LVGF_HEADER|LVGF_FOOTER|LVGF_STATE;
	group.stateMask=0xffffffff;
	if(!SendMessage((HWND)UlongToHandle(windowHandle),LVM_GETGROUPINFOBYINDEX,(WPARAM)groupIndex,(LPARAM)&group)) {
		LOG_DEBUGWARNING(L"LVM_GETGROUPINFOBYINDEX failed");
		return 1;
	}
	if(group.pszHeader) *header=SysAllocString(group.pszHeader);
	if(group.pszFooter) *footer=SysAllocString(group.pszFooter);
	*state=group.state;
	return 0;
}

error_status_t nvdaInProcUtils_sysListView32_getColumnContent(handle_t bindingHandle, const unsigned long windowHandle, int item, int subItem, BSTR* text) {
	LVITEM lvItem = {0};
	lvItem.mask = LVIF_TEXT | LVIF_COLUMNS;
	lvItem.iItem = item;
	lvItem.iSubItem = subItem;
	lvItem.cchTextMax = CBEMAXSTRLEN;
	wchar_t textBuf[CBEMAXSTRLEN]{}; // Ensure that the array initialised with all zero values ('\0')
	lvItem.pszText= textBuf;
	if (!SendMessage((HWND)UlongToHandle(windowHandle), LVM_GETITEM, (WPARAM)0, (LPARAM)&lvItem)) {
		LOG_DEBUGWARNING(L"LVM_GETITEM failed");
		return 1;
	}
	if(!lvItem.pszText) {
		LOG_DEBUGWARNING(L"LVM_GETITEM didn't retrieve any text");
		return 1;
	}
	*text = SysAllocString(lvItem.pszText);
	return 0;
}

error_status_t nvdaInProcUtils_sysListView32_getColumnLocation(handle_t bindingHandle, const unsigned long windowHandle, int item, int subItem, RECT* location) {
	RECT localRect {
		// Returns the bounding rectangle of the entire item, including the icon and label.
		LVIR_LABEL,  // left
		// According to Microsoft, top should be the one-based index of the subitem.
		// However, indexes coming from LVM_GETCOLUMNORDERARRAY are zero based.
		subItem // top
	};
	if (!SendMessage((HWND)UlongToHandle(windowHandle), LVM_GETSUBITEMRECT, (WPARAM)item, (LPARAM)&localRect)) {
		LOG_DEBUGWARNING(L"LVM_GETSUBITEMRECT failed");
		return 1;
	}
	*location = localRect;
	return 0;
}

error_status_t nvdaInProcUtils_sysListView32_getColumnHeader(handle_t bindingHandle, const unsigned long windowHandle, int subItem, BSTR* text) {
	LVCOLUMN lvColumn = {0};
	lvColumn.mask = LVCF_TEXT;
	lvColumn.iSubItem = subItem;
	lvColumn.cchTextMax = CBEMAXSTRLEN;
	wchar_t textBuf[CBEMAXSTRLEN]{}; // Ensure that the array initialised with all zero values ('\0')
	lvColumn.pszText= textBuf;
	if (!SendMessage((HWND)UlongToHandle(windowHandle), LVM_GETCOLUMN, (WPARAM)subItem, (LPARAM)&lvColumn)) {
		LOG_DEBUGWARNING(L"LVM_GETCOLUMN failed");
		return 1;
	}
	if(!lvColumn.pszText) {
		LOG_DEBUGWARNING(L"LVM_GETCOLUMN didn't retrieve any text");
		return 1;
	}
	*text = SysAllocString(lvColumn.pszText);
	return 0;
}

error_status_t nvdaInProcUtils_sysListView32_getColumnOrderArray(handle_t bindingHandle, const unsigned long windowHandle, const int columnCount, int* coa) {
	if (!SendMessage((HWND)UlongToHandle(windowHandle), LVM_GETCOLUMNORDERARRAY, (WPARAM)columnCount, (LPARAM)coa)) {
		LOG_DEBUGWARNING(L"LVM_GETCOLUMNORDERARRAY failed");
		return 1;
	}
	return 0;
}
