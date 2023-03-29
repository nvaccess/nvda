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
#include <common/log.h>
#include <remote/nvdaInProcUtils.h>

// #7828: Windows headers define this as 260 characters.
// However this is not long enough for modern Twitter clients that need at least 280 characters.
// Therefore, round it up to the nearest power of 2.
#undef CBEMAXSTRLEN
#define CBEMAXSTRLEN 512

error_status_t nvdaInProcUtils_sysListView32_getGroupInfo(handle_t bindingHandle, const unsigned long windowHandle, int groupIndex, BSTR* header, BSTR* footer, int* state) {
	LVGROUP group={0};
	group.cbSize=sizeof(group);
	group.mask=LVGF_HEADER|LVGF_FOOTER|LVGF_STATE;
	group.stateMask=0xffffffff;
	// ListView_GetGroupInfoByIndex macro has no return value, using SendMessage directly so errors are caught.
	// The meaning of the return value depends on the message sent, for LVM_GETGROUPINFOBYINDEX,
	// it returns TRUE if successful, or FALSE otherwise.
	const auto sendMsgRes = SendMessage(
		static_cast<HWND>(UlongToHandle(windowHandle)),
		LVM_GETGROUPINFOBYINDEX,
		static_cast<WPARAM>(groupIndex),
		reinterpret_cast<LPARAM>(&group)
	);
	if(TRUE != sendMsgRes) {
		LOG_DEBUGWARNING(L"LVM_GETGROUPINFOBYINDEX failed");
		return 1;
	}
	if(group.pszHeader) *header=SysAllocString(group.pszHeader);
	if(group.pszFooter) *footer=SysAllocString(group.pszFooter);
	*state=group.state;
	return 0;
}

error_status_t nvdaInProcUtils_sysListView32_getColumnContent(handle_t bindingHandle, const unsigned long windowHandle, int item, int subItem, BSTR* text) {
	if (text == nullptr) {
		LOG_ERROR(L"text was not provided");
		return ERROR_INVALID_PARAMETER;
	}
	LVITEM lvItem {};
	lvItem.mask = LVIF_TEXT | LVIF_COLUMNS;
	lvItem.iItem = item;
	lvItem.iSubItem = subItem;
	lvItem.cchTextMax = CBEMAXSTRLEN;
	wchar_t textBuf[CBEMAXSTRLEN]{}; // Ensure that the array initialised with all zero values ('\0')
	lvItem.pszText= textBuf;
	// ListView_GetItem macro has no return value, using SendMessage directly so errors are caught.
	// The meaning of the return value depends on the message sent, for LVM_GETITEM,
	// it returns TRUE if successful, or FALSE otherwise.
	const auto sendMsgRes = SendMessage(
		static_cast<HWND>(UlongToHandle(windowHandle)),
		LVM_GETITEM,
		static_cast<WPARAM>(0),
		reinterpret_cast<LPARAM>(&lvItem)
	);
	if (TRUE != sendMsgRes) {
		LOG_DEBUGWARNING(L"LVM_GETITEM failed");
		return 1;
	}
	if(!lvItem.pszText) {
		LOG_DEBUGWARNING(L"LVM_GETITEM didn't retrieve any text");
		return 1;
	}
	// cchTextMax won't be changed to the actual number of characters in the buffer, so we can't use SysAllocStringLen here.
	// It would result in many null characters in the resulting BSTR.
	*text = SysAllocString(lvItem.pszText);
	return 0;
}

error_status_t nvdaInProcUtils_sysListView32_getColumnLocation(handle_t bindingHandle, const unsigned long windowHandle, int item, int subItem, RECT* location) {
	if (location == nullptr) {
		LOG_ERROR(L"location was not provided");
		return ERROR_INVALID_PARAMETER;
	}
	// LVM_GETSUBITEMRECT receives a pointer to a RECT structure
	// that will receive the subitem bounding rectangle information. Its left and top members must be initialized with infomration about the rectangle to retrieve.
	// See https://docs.microsoft.com/en-us/windows/win32/controls/lvm-getsubitemrect
	RECT localRect {
		// Returns the bounding rectangle of the entire item, including the icon and label.
		LVIR_LABEL,  // left
		// According to Microsoft, top should be the one-based index of the subitem.
		// However, indexes coming from LVM_GETCOLUMNORDERARRAY are zero based.
		subItem // top
		// Note: the remaining members (right, bottom) are zero initialized.
	};
	// ListView_GetSubItemRect macro has no return value, using SendMessage directly so errors are caught.
	// The meaning of the return value depends on the message sent, for LVM_GETSUBITEMRECT,
	// it returns nonzero if successful, or 0 otherwise.
	const auto sendMsgRes = SendMessage(
		static_cast<HWND>(UlongToHandle(windowHandle)),
		LVM_GETSUBITEMRECT,
		static_cast<WPARAM>(item),
		reinterpret_cast<LPARAM>(&localRect)
	);
	if (TRUE != sendMsgRes) {
		LOG_DEBUGWARNING(L"LVM_GETSUBITEMRECT failed");
		return ERROR_INVALID_FUNCTION;
	}
	// Location will only be changed on success, as it is undesirable to modify the struct passed by the caller
	// if the function fails.
	// It is also easier to initialize a fresh struct and pass that to SendMessage
	// than zero out and initialize an existing one.
	*location = localRect;
	return ERROR_SUCCESS;
}

error_status_t nvdaInProcUtils_sysListView32_getColumnHeader(handle_t bindingHandle, const unsigned long windowHandle, int subItem, BSTR* text) {
	if (text == nullptr) {
		LOG_ERROR(L"text was not provided");
		return ERROR_INVALID_PARAMETER;
	}
	LVCOLUMN lvColumn {};
	lvColumn.mask = LVCF_TEXT;
	lvColumn.iSubItem = subItem;
	lvColumn.cchTextMax = CBEMAXSTRLEN;
	wchar_t textBuf[CBEMAXSTRLEN]{}; // Ensure that the array initialised with all zero values ('\0')
	lvColumn.pszText= textBuf;
	// ListView_GetColumn macro has no return value, using SendMessage directly so errors are caught.
	// The meaning of the return value depends on the message sent, for LVM_GETCOLUMN,
	// it returns TRUE if successful, or FALSE otherwise.
	const auto sendMsgRes = SendMessage(
		static_cast<HWND>(UlongToHandle(windowHandle)),
		LVM_GETCOLUMN,
		static_cast<WPARAM>(subItem),
		reinterpret_cast<LPARAM>(&lvColumn)
	);
	if (TRUE != sendMsgRes) {
		LOG_DEBUGWARNING(L"LVM_GETCOLUMN failed");
		return ERROR_INVALID_FUNCTION;
	}
	if(!lvColumn.pszText) {
		LOG_DEBUGWARNING(L"LVM_GETCOLUMN didn't retrieve any text");
		return ERROR_INVALID_FUNCTION;
	}
	// cchTextMax won't be changed to the actual number of characters in the buffer, so we can't use SysAllocStringLen here.
	// It would result in many null characters in the resulting BSTR.
	*text = SysAllocString(lvColumn.pszText);
	return ERROR_SUCCESS;
}
error_status_t nvdaInProcUtils_sysListView32_getColumnOrderArray(handle_t bindingHandle, const unsigned long windowHandle, const int columnCount, int* columnOrderArray) {
	if (columnOrderArray == nullptr) {
		LOG_ERROR(L"columnOrderArray was not provided");
		return ERROR_INVALID_PARAMETER;
	}
	// ListView_GetColumnOrderArray macro has no return value, using SendMessage directly so errors are caught.
	// The meaning of the return value depends on the message sent, for LVM_GETCOLUMNORDERARRAY,
	// it returns nonzero if successful, or 0 otherwise.
	// https://docs.microsoft.com/en-us/windows/win32/controls/lvm-getcolumnorderarray#return-value
	const auto sendMsgRes = SendMessage(
		static_cast<HWND>(UlongToHandle(windowHandle)),
		LVM_GETCOLUMNORDERARRAY,
		static_cast<WPARAM>(columnCount),
		reinterpret_cast<LPARAM>(columnOrderArray)
	);
	if (FALSE == sendMsgRes) {
		LOG_DEBUGWARNING(
			L"LVM_GETCOLUMNORDERARRAY failed. " <<
			L"Windows Error: " << GetLastError() <<
			L", Window Handle: " << windowHandle
		);
		return ERROR_INVALID_FUNCTION;
	}
	return ERROR_SUCCESS;
}
