/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2016 NVDA contributers.
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

// See https://github.com/nvaccess/nvda/wiki/Using-COM-with-NVDA-and-Microsoft-Word
constexpr int wdDISPID_APPLICATION_ISSANDBOX = 492;
constexpr int wdDISPID_APPLICATION_SCREENUPDATING = 26;
constexpr int wdDISPID_APPLICATION_PIXELSTOPOINTS = 388;
constexpr int wdDISPID_BORDERS_ENABLE = 2;
constexpr int wdDISPID_CELL_COLUMNINDEX = 5;
constexpr int wdDISPID_CELL_RANGE = 0;
constexpr int wdDISPID_CELL_ROWINDEX = 4;
constexpr int wdDISPID_CELLS_ITEM = 0;
constexpr int wdDISPID_COLUMNS_COUNT = 2;
constexpr int wdDISPID_COMMENT_SCOPE = 1005;
constexpr int wdDISPID_COMMENTS_COUNT = 2;
constexpr int wdDISPID_COMMENTS_ITEM = 0;
constexpr int wdDISPID_CONTENTCONTROL_CHECKED = 28;
constexpr int wdDISPID_CONTENTCONTROL_RANGE = 1;
constexpr int wdDISPID_CONTENTCONTROL_TITLE = 12;
constexpr int wdDISPID_CONTENTCONTROL_TYPE = 5;
constexpr int wdDISPID_CONTENTCONTROLS_ITEM = 0;
constexpr int wdDISPID_DOCUMENT_RANGE = 2000;
constexpr int wdDISPID_DOCUMENT_STYLES = 22;
constexpr int wdDISPID_ENDNOTE_INDEX = 6;
constexpr int wdDISPID_ENDNOTES_COUNT = 2;
constexpr int wdDISPID_ENDNOTES_ITEM = 0;
constexpr int wdDISPID_FIELDS_COUNT = 1;
constexpr int wdDISPID_FIELDS_ITEM = 0;
constexpr int wdDISPID_FIELDS_ITEM_RESULT = 4;
constexpr int wdDISPID_FIELDS_ITEM_TYPE = 1;
constexpr int wdDISPID_FONT_BOLD = 130;
constexpr int wdDISPID_FONT_COLOR = 159;
constexpr int wdDISPID_FONT_DOUBLESTRIKETHROUGH = 136;
constexpr int wdDISPID_FONT_HIDDEN = 132;
constexpr int wdDISPID_FONT_ITALIC = 131;
constexpr int wdDISPID_FONT_NAME = 142;
constexpr int wdDISPID_FONT_SIZE = 141;
constexpr int wdDISPID_FONT_STRIKETHROUGH = 135;
constexpr int wdDISPID_FONT_SUBSCRIPT = 138;
constexpr int wdDISPID_FONT_SUPERSCRIPT = 139;
constexpr int wdDISPID_FONT_UNDERLINE = 140;
constexpr int wdDISPID_FOOTNOTE_INDEX = 6;
constexpr int wdDISPID_FOOTNOTES_COUNT = 2;
constexpr int wdDISPID_FOOTNOTES_ITEM = 0;
constexpr int wdDISPID_FORMFIELD_RANGE = 17;
constexpr int wdDISPID_FORMFIELD_RESULT = 10;
constexpr int wdDISPID_FORMFIELD_STATUSTEXT = 8;
constexpr int wdDISPID_FORMFIELD_TYPE = 0;
constexpr int wdDISPID_FORMFIELDS_ITEM = 0;
constexpr int wdDISPID_HYPERLINKS_COUNT = 1;
constexpr int wdDISPID_INLINESHAPE_ALTERNATIVETEXT = 131;
constexpr int wdDISPID_INLINESHAPE_OLEFORMAT = 5;
constexpr int wdDISPID_INLINESHAPE_TITLE = 158;
constexpr int wdDISPID_INLINESHAPE_TYPE = 6;
constexpr int wdDISPID_INLINESHAPES_COUNT = 1;
constexpr int wdDISPID_INLINESHAPES_ITEM = 0;
constexpr int wdDISPID_LISTFORMAT_LISTSTRING = 75;
constexpr int wdDISPID_OLEFORMAT_PROGID = 22;
constexpr int wdDISPID_PAGESETUP_GUTTER = 104;
constexpr int wdDISPID_PAGESETUP_GUTTERPOS = 1222;
constexpr int wdDISPID_PAGESETUP_GUTTERSTYLE = 129;
constexpr int wdDISPID_PAGESETUP_LEFTMARGIN = 102;
constexpr int wdDISPID_PAGESETUP_RIGHTMARGIN = 103;
constexpr int wdDISPID_PAGESETUP_MIRRORMARGINS = 111;
constexpr int wdDISPID_PAGESETUP_PAGEWIDTH = 105;
constexpr int wdDISPID_PAGESETUP_SECTIONSTART = 114;
constexpr int wdDISPID_PAGESETUP_TEXTCOLUMNS = 119;
constexpr int wdDISPID_PARAGRAPH_OUTLINELEVEL = 202;
constexpr int wdDISPID_PARAGRAPH_RANGE = 0;
constexpr int wdDISPID_PARAGRAPH_STYLE = 100;
constexpr int wdDISPID_PARAGRAPHFORMAT_ALIGNMENT = 101;
constexpr int wdDISPID_PARAGRAPHFORMAT_FIRSTLINEINDENT = 108;
constexpr int wdDISPID_PARAGRAPHFORMAT_LEFTINDENT = 107;
constexpr int wdDISPID_PARAGRAPHFORMAT_LINESPACING = 109;
constexpr int wdDISPID_PARAGRAPHFORMAT_LINESPACINGRULE = 110;
constexpr int wdDISPID_PARAGRAPHFORMAT_RIGHTINDENT = 106;
constexpr int wdDISPID_PARAGRAPHS_ITEM = 0;
constexpr int wdDISPID_RANGE_APPLICATION = 1000;
constexpr int wdDISPID_RANGE_CELLS = 57;
constexpr int wdDISPID_RANGE_COLLAPSE = 101;
constexpr int wdDISPID_RANGE_COMMENTS = 56;
constexpr int wdDISPID_RANGE_CONTENTCONTROLS = 424;
constexpr int wdDISPID_RANGE_DUPLICATE = 6;
constexpr int wdDISPID_RANGE_END = 4;
constexpr int wdDISPID_RANGE_ENDNOTES = 55;
constexpr int wdDISPID_RANGE_EXPAND = 129;
constexpr int wdDISPID_RANGE_FIELDS = 64;
constexpr int wdDISPID_RANGE_FONT = 5;
constexpr int wdDISPID_RANGE_FOOTNOTES = 54;
constexpr int wdDISPID_RANGE_FORMFIELDS = 65;
constexpr int wdDISPID_RANGE_HYPERLINKS = 156;
constexpr int wdDISPID_RANGE_INFORMATION = 313;
constexpr int wdDISPID_RANGE_INLINESHAPES = 319;
constexpr int wdDISPID_RANGE_INRANGE = 126;
constexpr int wdDISPID_RANGE_LANGUAGEID = 153;
constexpr int wdDISPID_RANGE_LISTFORMAT = 68;
constexpr int wdDISPID_RANGE_MOVE = 109;
constexpr int wdDISPID_RANGE_MOVEEND = 111;
constexpr int wdDISPID_RANGE_PAGESETUP = 1101;
constexpr int wdDISPID_RANGE_PARAGRAPHFORMAT = 1102;
constexpr int wdDISPID_RANGE_PARAGRAPHS = 59;
constexpr int wdDISPID_RANGE_REVISIONS = 150;
constexpr int wdDISPID_RANGE_SECTIONS = 58;
constexpr int wdDISPID_RANGE_SELECT = 65535;
constexpr int wdDISPID_RANGE_SETRANGE = 100;
constexpr int wdDISPID_RANGE_SPELLINGERRORS = 316;
constexpr int wdDISPID_RANGE_START = 3;
constexpr int wdDISPID_RANGE_STORYTYPE = 7;
constexpr int wdDISPID_RANGE_STYLE = 151;
constexpr int wdDISPID_RANGE_TABLES = 50;
constexpr int wdDISPID_RANGE_TEXT = 0;
constexpr int wdDISPID_REVISION_RANGE = 3;
constexpr int wdDISPID_REVISION_TYPE = 4;
constexpr int wdDISPID_REVISIONS_ITEM = 0;
constexpr int wdDISPID_REVISIONS_COUNT = 5;
constexpr int wdDISPID_ROWS_COUNT = 2;
constexpr int wdDISPID_SECTIONS_COUNT = 2;
constexpr int wdDISPID_SECTIONS_ITEM = 0;
constexpr int wdDISPID_SECTION_PAGESETUP = 1101;
constexpr int wdDISPID_SELECTION_ENDOF = 108;
constexpr int wdDISPID_SELECTION_RANGE = 400;
constexpr int wdDISPID_SELECTION_SETRANGE = 100;
constexpr int wdDISPID_SELECTION_STARTISACTIVE = 404;
constexpr int wdDISPID_SELECTION_STARTOF = 107;
constexpr int wdDISPID_SPELLINGERRORS_COUNT = 1;
constexpr int wdDISPID_SPELLINGERRORS_ITEM = 0;
constexpr int wdDISPID_STYLE_NAMELOCAL = 0;
constexpr int wdDISPID_STYLE_PARENT = 1002;
constexpr int wdDISPID_STYLES_ITEM = 0;
constexpr int wdDISPID_TABLE_BORDERS = 1100;
constexpr int wdDISPID_TABLE_COLUMNS = 100;
constexpr int wdDISPID_TABLE_DESCR = 210;
constexpr int wdDISPID_TABLE_NESTINGLEVEL = 108;
constexpr int wdDISPID_TABLE_RANGE = 0;
constexpr int wdDISPID_TABLE_ROWS = 101;
constexpr int wdDISPID_TABLE_TITLE = 209;
constexpr int wdDISPID_TABLES_ITEM = 0;
constexpr int wdDISPID_TEXTCOLUMN_WIDTH = 100;
constexpr int wdDISPID_TEXTCOLUMNS_COUNT = 2;
constexpr int wdDISPID_TEXTCOLUMNS_ITEM = 0;
constexpr int wdDISPID_TEXTCOLUMN_SPACEAFTER = 101;
constexpr int wdDISPID_WINDOW_APPLICATION = 1000;
constexpr int wdDISPID_WINDOW_DOCUMENT = 2;
constexpr int wdDISPID_WINDOW_SELECTION = 4;

// WdConstants Enumeration
constexpr int wdUndefined = 9999999;

// WdStoryType Enumeration
constexpr int wdCommentsStory = 4;

// WdUnits Enumeration
constexpr int wdCharacter = 1;
constexpr int wdWord = 2;
constexpr int wdParagraph = 4;
constexpr int wdLine = 5;
constexpr int wdStory = 6;
constexpr int wdCharacterFormatting = 13;

// WdCollapseDirection Enumeration
constexpr int wdCollapseEnd = 0;
constexpr int wdCollapseStart = 1;

// WdInformation Enumeration values
constexpr int wdActiveEndAdjustedPageNumber = 1;
constexpr int wdActiveEndSectionNumber = 2;
constexpr int wdFirstCharacterLineNumber = 10;
constexpr int wdWithInTable = 12;
constexpr int wdStartOfRangeRowNumber = 13;
constexpr int wdMaximumNumberOfRows = 15;
constexpr int wdStartOfRangeColumnNumber = 16;
constexpr int wdMaximumNumberOfColumns = 18;
constexpr int wdHorizontalPositionRelativeToPage = 5;

// WdParagraphAlignment Enumeration
constexpr int wdAlignParagraphLeft = 0;
constexpr int wdAlignParagraphCenter = 1;
constexpr int wdAlignParagraphRight = 2;
constexpr int wdAlignParagraphJustify = 3;

// WdLanguageID Enumeration
constexpr int wdLanguageNone = 0;  //&H0
constexpr int wdNoProofing = 1024;  //&H400
constexpr int wdLanguageUnknown = 9999999;

// WdInlineShapeType Enumeration
constexpr int wdInlineShapeEmbeddedOLEObject = 1;
constexpr int wdInlineShapePicture = 3;
constexpr int wdInlineShapeLinkedPicture = 4;
constexpr int wdInlineShapeChart = 12;

// WdGutterStyle Enumeration
constexpr int wdGutterPosLeft = 0;
constexpr int wdGutterPosRight = 2;
constexpr int wdGutterPosTop = 1;

// chart constants
constexpr int wdDISPID_INLINESHAPE_HASCHART = 148;
constexpr int wdDISPID_INLINESHAPE_CHART = 149;
constexpr int wdDISPID_CHART_CHARTTITLE = 1610743811;
constexpr int wdDISPID_CHART_HASTITLE = 1610743809;
constexpr int wdDISPID_CHARTTITLE_TEXT = 1610743820;
