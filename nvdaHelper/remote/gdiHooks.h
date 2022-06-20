/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
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

#ifndef NVDAHELPER_REMOTE_GDIHOOKS_H
#define NVDAHELPER_REMOTE_GDIHOOKS_H

#include <map>
#include <windef.h>
#include "displayModel.h"
#include <common/lock.h>

template <typename t> class displayModelsMap_t: public std::map<t,displayModel_t*>, public LockableObject {
	public:
	displayModelsMap_t(): map<t,displayModel_t*>(), LockableObject() {
	}
};

extern std::map<HWND,int> windowsForTextChangeNotifications; 
extern displayModelsMap_t<HWND> displayModelsByWindow;

void gdiHooks_inProcess_initialize();
void gdiHooks_inProcess_terminate();

//These structures were taken from http://www.microsoft.com/typography/OTSPEC/cmap.htm
//All TTF structures must be byte-aligned.
#pragma pack(push,1)

//Macros to convert from big endian. [MS]
#define SWAPWORD(x) MAKEWORD( \
	HIBYTE(x), \
	LOBYTE(x) \
	)
#define SWAPLONG(x) MAKELONG( \
	HIWORD(x), \
	LOWORD(x) \
	)

//CmapHeader structure
typedef struct {
	USHORT version; //Table version number (0).
	USHORT numTables; //Number of encoding tables that follow.
} CmapHeader;

//EncodingRecord structure
typedef struct {
	USHORT platformID; //Platform ID.
	USHORT encodingID; //Platform-specific encoding ID.
	ULONG offset; //Byte offset from beginning of table to the subtable for this encoding.
} EncodingRecord;

//CmapFmt4Header structure
typedef struct {
	USHORT format; //Format number is set to 4.
	USHORT length; //This is the length in bytes of the subtable.
	USHORT language; //Irrelevant for our purposes.
	USHORT segCountX2; //2 x segCount.
	USHORT searchRange; //2 x (2**floor(log2(segCount)))
	USHORT entrySelector; //log2(searchRange/2)
	USHORT rangeShift; //2 x segCount - searchRange
} CmapFmt4Header;

//FontHeader structure.
//http://www.microsoft.com/typography/OTSPEC/head.htm
typedef struct {
	LONG tableVersion;
	LONG fontRevision;
	ULONG checksumAdjustment;
	ULONG magicNumber;
	USHORT flags;
	USHORT unitsPerEm;
	__int64 created;
	__int64 modified;
	SHORT xMin;
	SHORT yMin;
	SHORT xMax;
	SHORT yMax;
	USHORT macStyle;
	USHORT lowestRecPPEM;
	SHORT fontDirectionHint;
	SHORT indexToLocFormat;
	SHORT glyphDataFormat;
} FontHeader;

#pragma pack(pop)

#endif