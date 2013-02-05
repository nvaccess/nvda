/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
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
#include "nvdaInProcUtils.h"

error_status_t nvdaInProcUtils_sysListView32_getGroupInfo(handle_t bindingHandle, long windowHandle, int groupIndex, BSTR* header, BSTR* footer, int* state) {
	LVGROUP group={0};
	group.cbSize=sizeof(group);
	group.mask=LVGF_HEADER|LVGF_FOOTER|LVGF_STATE;
	group.stateMask=0xffffffff;
	if(!SendMessage((HWND)windowHandle,LVM_GETGROUPINFOBYINDEX,(WPARAM)groupIndex,(LPARAM)&group)) {
		LOG_DEBUGWARNING(L"LVM_GETGROUPINFOBYINDEX failed");
		return 1;
	}
	if(group.pszHeader) *header=SysAllocString(group.pszHeader);
	if(group.pszFooter) *footer=SysAllocString(group.pszFooter);
	*state=group.state;
	return 0;
}
