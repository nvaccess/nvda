/*
This file is a part of the NVDA project.
Copyright 2018 NV Access Limited.
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

#include <comdef.h>
#include <windows.h>
#include <common/log.h>
#include "inProcess.h"
#include "nvdaInProcUtils.h"

error_status_t nvdaInProcUtils_excel_getCellTextWidth(handle_t bindingHandle, const long threadID, IDispatch* pDispatchCell, long* width) {
	*width=5;
	return RPC_S_OK;
}
