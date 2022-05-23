/*
This file is a part of the NVDA project.
Copyright 2019-2022 NV Access Limited, Accessolutions, Julien Cochuyt
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2.0, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#pragma once

// from XLDvType enumeration 
const long xlValidateList=3;

// Excel IDispatch IDs
const long XLDISPID_WINDOW_APPLICATION=148;
const long XLDISPID_APPLICATION_RANGE=197;
const long XLDISPID_RANGE__NEWENUM=-4;
const long XLDISPID_RANGE_FORMULA=261;
const long XLDISPID_RANGE_FORMULA_LOCAL=263;
const long XLDISPID_RANGE_ITEM=170;
const long XLDISPID_RANGE_ROW=257;
const long XLDISPID_RANGE_COLUMN=240;
const long XLDISPID_RANGE_ADDRESS=236;
const long XLDISPID_RANGE_MERGEAREA=1385;
const long XLDISPID_RANGE_NEXT=502;
const long XLDISPID_RANGE_WIDTH=122;
const long XLDISPID_RANGE_SHRINKTOFIT=209;
const long XLDISPID_RANGE_WRAPTEXT=276;
const long XLDISPID_RANGE_HYPERLINKS=1393;
const long XLDISPID_HYPERLINKS_COUNT=118;
const long XLDISPID_RANGE_ENTIREROW=247;
const long XLDISPID_RANGE_ROWS=258;
const long XLDISPID_ROWS_COUNT=118;
const long XLDISPID_ROWS_ITEM=170;
const long XLDISPID_ROW_SUMMARY=273;
const long XLDISPID_ROW_SHOWDETAIL=585;
const long XLDISPID_ROW_OUTLINELEVEL=271;
const long XLDISPID_RANGE_ENTIRECOLUMN=246;
const long XLDISPID_RANGE_COLUMNS=241;
const long XLDISPID_COLUMNS_COUNT=118;
const long XLDISPID_COLUMNS_ITEM=170;
const long XLDISPID_COLUMN_SUMMARY=273;
const long XLDISPID_COLUMN_SHOWDETAIL=585;
const long XLDISPID_COLUMN_OUTLINELEVEL=271;
const long XLDISPID_RANGE_COMMENT=910;
const long XLDISPID_COMMENT_TEXT=138;
const long XLDISPID_RANGE_HASFORMULA=267;
const long XLDISPID_RANGE_VALIDATION=1387;
const long XLDISPID_VALIDATION_TYPE=108;
const long XLDISPID_VALIDATION_INPUTMESSAGE=1611;
const long XLDISPID_VALIDATION_INPUTTITLE=1612;
const long XLDISPID_RANGE_WORKSHEET=348;
const long XLDISPID_WORKSHEET_PROTECTCONTENTS=292;
const long XLDISPID_RANGE_LOCKED=269;
const long XLDISPID_RANGE_TEXT=138;
const long XLDISPID_RANGE_FONT=146;
const long XLDISPID_FONT_SIZE=104;
const long XLDISPID_FONT_BOLD=96;
const long XLDISPID_FONT_ITALIC=101;
const long XLDISPID_FONT_UNDERLINE=106;
const long XLDISPID_FONT_STRIKETHROUGH=105;
const long XLDISPID_FONT_NAME=110;
const long XLDISPID_RANGE_DISPLAYFORMAT=666;
const long XLDISPID_RANGE_OFFSET=254;

const long NVCELLINFOFLAG_ADDRESS=0x1;
const long NVCELLINFOFLAG_TEXT=0x2;
const long NVCELLINFOFLAG_INPUTMESSAGE=0x4;
const long NVCELLINFOFLAG_STATES=0x8;
const long NVCELLINFOFLAG_COORDS=0x10;
const long NVCELLINFOFLAG_OUTLINELEVEL=0x20;
const long NVCELLINFOFLAG_COMMENTS=0x40;
const long NVCELLINFOFLAG_FORMULA=0x80;
const long NVCELLINFOFLAG_ALL=0xffff;

constexpr std::uint64_t setBit(const unsigned int bitPos) {
	return std::uint64_t(1) << bitPos;
}

/*NVDA sell specific states.
These values must match NvCellState enum in source/nvdaObjects/excel.py
*/
enum NvCellState : std::uint64_t {
	EXPANDED = setBit(1),
	COLLAPSED = setBit(2),
	LINKED = setBit(3),
	HASPOPUP = setBit(4),
	PROTECTED = setBit(5),
	HASFORMULA = setBit(6),
	HASCOMMENT = setBit(7),
	CROPPED = setBit(8),
	OVERFLOWING = setBit(9),
	UNLOCKED = setBit(10)
};

// an HRESULT error code randomly given by Excel such as for validation.type when there is no validation on the cell
const HRESULT XLGeneralError=0x800a03ec;
