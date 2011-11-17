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

#include <sstream>
#include <comdef.h>
#include <windows.h>
#include <oleacc.h>
#include "log.h"
#include "nvdaHelperRemote.h"
#include "nvdaInProcUtils.h"
#include "nvdaInProcUtils.h"
#include "winword.h"

using namespace std;

#define wdDISPID_DOCUMENT_RANGE 2000
#define wdDISPID_WINDOW_DOCUMENT 2
#define wdDISPID_WINDOW_APPLICATION 1000
#define wdDISPID_APPLICATION_SELECTION 5
#define wdDISPID_APPLICATION_SCREENUPDATING 26
#define wdDISPID_SELECTION_RANGE 400
#define wdDISPID_SELECTION_SETRANGE 100
#define wdDISPID_RANGE_MOVEEND 111
#define wdDISPID_RANGE_COLLAPSE 101
#define wdDISPID_RANGE_TEXT 0
#define wdDISPID_RANGE_EXPAND 129
#define wdDISPID_RANGE_SELECT 65535
#define wdDISPID_RANGE_START 3
#define wdDISPID_RANGE_END 4
#define wdDISPID_RANGE_INFORMATION 313
#define wdDISPID_RANGE_STYLE 151
#define wdDISPID_STYLE_NAMELOCAL 0
#define wdDISPID_RANGE_SPELLINGERRORS 316
#define wdDISPID_SPELLINGERRORS_COUNT 1
#define wdDISPID_RANGE_FONT 5
#define wdDISPID_FONT_BOLD 130
#define wdDISPID_FONT_ITALIC 131
#define wdDISPID_FONT_UNDERLINE 140
#define wdDISPID_FONT_NAME 142
#define wdDISPID_FONT_SIZE 141
#define wdDISPID_FONT_SUBSCRIPT 138
#define wdDISPID_FONT_SUPERSCRIPT 139
#define wdDISPID_RANGE_PARAGRAPHFORMAT 1102
#define wdDISPID_PARAGRAPHFORMAT_ALIGNMENT 101
#define wdDISPID_RANGE_LISTFORMAT 68
#define wdDISPID_LISTFORMAT_LISTSTRING 75
#define wdDISPID_RANGE_PARAGRAPHS 59
#define wdDISPID_PARAGRAPHS_ITEM 0
#define wdDISPID_PARAGRAPH_RANGE 0

#define wdWord 2
#define wdLine 5
#define wdCharacterFormatting 13

#define wdCollapseEnd 0
#define wdCollapseStart 1

#define wdActiveEndAdjustedPageNumber 1
#define wdFirstCharacterLineNumber 10
#define wdWithInTable 12
#define wdStartOfRangeRowNumber 13
#define wdMaximumNumberOfRows 15
#define wdStartOfRangeColumnNumber 16
#define wdMaximumNumberOfColumns 18

#define wdAlignParagraphLeft 0
#define wdAlignParagraphCenter 1
#define wdAlignParagraphRight 2
#define wdAlignParagraphJustify 3

#define formatConfig_reportFontName 1
#define formatConfig_reportFontSize 2
#define formatConfig_reportFontAttributes 4
#define formatConfig_reportColor 8
#define formatConfig_reportAlignment 16
#define formatConfig_reportStyle 32
#define formatConfig_reportSpellingErrors 64
#define formatConfig_reportPage 128
#define formatConfig_reportLineNumber 256
#define formatConfig_reportTables 512
#define formatConfig_reportLists 1024

#define formatConfig_fontFlags (formatConfig_reportFontName|formatConfig_reportFontSize|formatConfig_reportFontAttributes)
#define formatConfig_initialFormatFlags (formatConfig_reportPage|formatConfig_reportLineNumber|formatConfig_reportTables|formatConfig_reportLists)
 
UINT wm_winword_expandToLine=0;
typedef struct {
	int offset;
	int lineStart;
	int lineEnd;
} winword_expandToLine_args;
void winword_expandToLine_helper(HWND hwnd, winword_expandToLine_args* args) {
	//Fetch all needed objects
	IDispatchPtr pDispatchWindow=NULL;
	if(AccessibleObjectFromWindow(hwnd,OBJID_NATIVEOM,IID_IDispatch,(void**)&pDispatchWindow)!=S_OK) {
		LOG_DEBUGWARNING(L"AccessibleObjectFromWindow failed");
		return;
	}
	IDispatchPtr pDispatchApplication=NULL;
	if(_com_dispatch_propget(pDispatchWindow,wdDISPID_WINDOW_APPLICATION,VT_DISPATCH,&pDispatchApplication)!=S_OK) {
		LOG_DEBUGWARNING(L"window.application failed");
		return;
	}
	IDispatchPtr pDispatchSelection=NULL;
	if(_com_dispatch_propget(pDispatchApplication,wdDISPID_APPLICATION_SELECTION,VT_DISPATCH,&pDispatchSelection)!=S_OK||!pDispatchSelection) {
		LOG_DEBUGWARNING(L"application.selection failed");
		return;
	}
	IDispatch* pDispatchOldSelRange=NULL;
	if(_com_dispatch_propget(pDispatchSelection,wdDISPID_SELECTION_RANGE,VT_DISPATCH,&pDispatchOldSelRange)!=S_OK) {
		LOG_DEBUGWARNING(L"selection.range failed");
		return;
	}
	//Disable screen updating as we will be moving the selection temporarily
	_com_dispatch_propput(pDispatchApplication,wdDISPID_APPLICATION_SCREENUPDATING,VT_BOOL,false);
	//Move the selection to the given range
	_com_dispatch_method(pDispatchSelection,wdDISPID_SELECTION_SETRANGE,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003\x0003",args->offset,args->offset);
	//Expand the selection to the line
	_com_dispatch_method(pDispatchSelection,wdDISPID_RANGE_EXPAND,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003",wdLine);
	//Collect the start and end offsets of the selection
	_com_dispatch_propget(pDispatchSelection,wdDISPID_RANGE_START,VT_I4,&(args->lineStart));
	_com_dispatch_propget(pDispatchSelection,wdDISPID_RANGE_END,VT_I4,&(args->lineEnd));
	//Move the selection back to its original location
	_com_dispatch_method(pDispatchOldSelRange,wdDISPID_RANGE_SELECT,DISPATCH_METHOD,VT_EMPTY,NULL,NULL);
	//Reenable screen updating
	_com_dispatch_propput(pDispatchApplication,wdDISPID_APPLICATION_SCREENUPDATING,VT_BOOL,true);
}

void generateXMLAttribsForFormatting(IDispatch* pDispatchRange, int startOffset, int endOffset, int formatConfig, wostringstream& formatAttribsStream) {
	int iVal=0;
	if((formatConfig&formatConfig_reportPage)&&(_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdActiveEndAdjustedPageNumber)==S_OK)) {
		formatAttribsStream<<L"page-number=\""<<iVal<<L"\" ";
	}
	if((formatConfig&formatConfig_reportLineNumber)&&(_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdFirstCharacterLineNumber)==S_OK)) {
		formatAttribsStream<<L"line-number=\""<<iVal<<L"\" ";
	}
	if((formatConfig&formatConfig_reportTables)&&_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdWithInTable)==S_OK&&iVal) {
		formatAttribsStream<<L"inTable=\""<<iVal<<L"\" ";
		if(_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdMaximumNumberOfRows)==S_OK) {
			formatAttribsStream<<L"table-row-count=\""<<iVal<<L"\" ";
		}
		if(_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdMaximumNumberOfColumns)==S_OK) {
			formatAttribsStream<<L"table-column-count=\""<<iVal<<L"\" ";
		}
		if(_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdStartOfRangeRowNumber)==S_OK) {
			formatAttribsStream<<L"table-row-number=\""<<iVal<<L"\" ";
		}
		if(_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdStartOfRangeColumnNumber)==S_OK) {
			formatAttribsStream<<L"table-column-number=\""<<iVal<<L"\" ";
		}
	}
	if(formatConfig&formatConfig_reportAlignment) {
		IDispatchPtr pDispatchParagraphFormat=NULL;
		if(_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_PARAGRAPHFORMAT,VT_DISPATCH,&pDispatchParagraphFormat)==S_OK&&pDispatchParagraphFormat) {
			if(_com_dispatch_propget(pDispatchParagraphFormat,wdDISPID_PARAGRAPHFORMAT_ALIGNMENT,VT_I4,&iVal)==S_OK) {
				switch(iVal) {
					case wdAlignParagraphLeft:
					formatAttribsStream<<L"text-align=\"left\" ";
					break;
					case wdAlignParagraphCenter:
					formatAttribsStream<<L"text-align=\"center\" ";
					break;
					case wdAlignParagraphRight:
					formatAttribsStream<<L"text-align=\"right\" ";
					break;
					case wdAlignParagraphJustify:
					formatAttribsStream<<L"text-align=\"justified\" ";
					break;
				}
			}
		}
	}
	if(formatConfig&formatConfig_reportLists) {
		IDispatchPtr pDispatchListFormat=NULL;
		if(_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_LISTFORMAT,VT_DISPATCH,&pDispatchListFormat)==S_OK&&pDispatchListFormat) {
			BSTR listString=NULL;
			if(_com_dispatch_propget(pDispatchListFormat,wdDISPID_LISTFORMAT_LISTSTRING,VT_BSTR,&listString)==S_OK&&listString) {
				if(SysStringLen(listString)>0) {
					IDispatchPtr pDispatchParagraphs=NULL;
					IDispatchPtr pDispatchParagraph=NULL;
					IDispatchPtr pDispatchParagraphRange=NULL;
					if(
						_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_PARAGRAPHS,VT_DISPATCH,&pDispatchParagraphs)==S_OK&&pDispatchParagraphs\
						&&_com_dispatch_method(pDispatchParagraphs,wdDISPID_PARAGRAPHS_ITEM,DISPATCH_METHOD,VT_DISPATCH,&pDispatchParagraph,L"\x0003",1)==S_OK&&pDispatchParagraph\
						&&_com_dispatch_propget(pDispatchParagraph,wdDISPID_PARAGRAPH_RANGE,VT_DISPATCH,&pDispatchParagraphRange)==S_OK&&pDispatchParagraphRange\
						&&_com_dispatch_propget(pDispatchParagraphRange,wdDISPID_RANGE_START,VT_I4,&iVal)==S_OK&&iVal==startOffset\
					) {
						formatAttribsStream<<L"line-prefix=\""<<listString<<L"\" ";
					}
				}
				SysFreeString(listString);
			}
		}
	}
	if(formatConfig&formatConfig_reportStyle) {
		IDispatchPtr pDispatchStyle=NULL;
		if(_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_STYLE,VT_DISPATCH,&pDispatchStyle)==S_OK&&pDispatchStyle) {
			BSTR nameLocal=NULL;
			_com_dispatch_propget(pDispatchStyle,wdDISPID_STYLE_NAMELOCAL,VT_BSTR,&nameLocal);
			if(nameLocal) {
				formatAttribsStream<<L"style=\""<<nameLocal<<L"\" ";
				SysFreeString(nameLocal);
			}
		}
	}
	if(formatConfig&formatConfig_fontFlags) {
		IDispatchPtr pDispatchFont=NULL;
		if(_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_FONT,VT_DISPATCH,&pDispatchFont)==S_OK&&pDispatchFont) {
			BSTR fontName=NULL;
			if((formatConfig&formatConfig_reportFontName)&&(_com_dispatch_propget(pDispatchFont,wdDISPID_FONT_NAME,VT_BSTR,&fontName)==S_OK)&&fontName) {
				formatAttribsStream<<L"font-name=\""<<fontName<<L"\" ";
				SysFreeString(fontName);
			}
			if((formatConfig&formatConfig_reportFontSize)&&(_com_dispatch_propget(pDispatchFont,wdDISPID_FONT_SIZE,VT_I4,&iVal)==S_OK)) {
				formatAttribsStream<<L"font-size=\""<<iVal<<L"pt\" ";
			}
			if(formatConfig&formatConfig_reportFontAttributes) {
				if(_com_dispatch_propget(pDispatchFont,wdDISPID_FONT_BOLD,VT_I4,&iVal)==S_OK&&iVal) {
					formatAttribsStream<<L"bold=\"1\" ";
				}
				if(_com_dispatch_propget(pDispatchFont,wdDISPID_FONT_ITALIC,VT_I4,&iVal)==S_OK&&iVal) {
					formatAttribsStream<<L"italic=\"1\" ";
				}
				if(_com_dispatch_propget(pDispatchFont,wdDISPID_FONT_UNDERLINE,VT_I4,&iVal)==S_OK&&iVal) {
					formatAttribsStream<<L"underline=\"1\" ";
				}
				if(_com_dispatch_propget(pDispatchFont,wdDISPID_FONT_SUPERSCRIPT,VT_I4,&iVal)==S_OK&&iVal) {
					formatAttribsStream<<L"text-position=\"super\" ";
				} else if(_com_dispatch_propget(pDispatchFont,wdDISPID_FONT_SUBSCRIPT,VT_I4,&iVal)==S_OK&&iVal) {
					formatAttribsStream<<L"text-position=\"sub\" ";
				}
			}
		}
	} 
	if(formatConfig&formatConfig_reportSpellingErrors) {
		IDispatchPtr pDispatchSpellingErrors=NULL;
		if(_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_SPELLINGERRORS,VT_DISPATCH,&pDispatchSpellingErrors)==S_OK&&pDispatchSpellingErrors) {
			_com_dispatch_propget(pDispatchSpellingErrors,wdDISPID_SPELLINGERRORS_COUNT,VT_I4,&iVal);
			if(iVal>0) {
				formatAttribsStream<<L"invalid-spelling=\""<<iVal<<L"\" ";
			}
		}
	} 
}

UINT wm_winword_getTextInRange=0;
typedef struct {
	int startOffset;
	int endOffset;
	long formatConfig;
	BSTR text;
} winword_getTextInRange_args;
void winword_getTextInRange_helper(HWND hwnd, winword_getTextInRange_args* args) {
	//Fetch all needed objects
	//Get the window object
	IDispatchPtr pDispatchWindow=NULL;
	if(AccessibleObjectFromWindow(hwnd,OBJID_NATIVEOM,IID_IDispatch,(void**)&pDispatchWindow)!=S_OK) {
		LOG_DEBUGWARNING(L"AccessibleObjectFromWindow failed");
		return;
	}
	//Get the active document for the window
	IDispatchPtr pDispatchDocument=NULL;
	if(_com_dispatch_propget(pDispatchWindow,wdDISPID_WINDOW_DOCUMENT,VT_DISPATCH,&pDispatchDocument)!=S_OK) {
		LOG_DEBUGWARNING(L"window.document failed");
		return;
	}
	//Create a range of the document using the given start and end offsets
	IDispatchPtr pDispatchRange=NULL;
	if(_com_dispatch_method(pDispatchDocument,wdDISPID_DOCUMENT_RANGE,DISPATCH_METHOD,VT_DISPATCH,&pDispatchRange,L"\x0003\x0003",args->startOffset,args->endOffset)!=S_OK) {
		LOG_DEBUGWARNING(L"document.range("<<(args->startOffset)<<L","<<(args->endOffset)<<L") failed");
		return;
	}
	//A temporary stringstream for initial formatting
	wostringstream initialFormatAttribsStream;
	//Start writing the output xml to a stringstream
	wostringstream XMLStream;
	XMLStream<<L"<control>";
	//Collapse the range
	int initialformatConfig=(args->formatConfig)&formatConfig_initialFormatFlags;
	int formatConfig=(args->formatConfig)&(~formatConfig_initialFormatFlags);
	_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_COLLAPSE,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003",wdCollapseStart);
	int chunkStartOffset=args->startOffset;
	int chunkEndOffset=chunkStartOffset;
	int unitsMoved=0;
	BSTR text=NULL;
	//Walk the range from the given start to end by characterFormatting or word units
	//And grab any text and formatting and generate appropriate xml
	bool firstLoop=true;
	do {
		//Try moving
		//But if characterFormatting doesn't work, and word doesn't work, or no units were moved then break out of the loop
		if((
			((formatConfig&formatConfig_reportSpellingErrors)||(_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_MOVEEND,DISPATCH_METHOD,VT_I4,&unitsMoved,L"\x0003\x0003",wdCharacterFormatting,1)!=S_OK))&&
			_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_MOVEEND,DISPATCH_METHOD,VT_I4,&unitsMoved,L"\x0003\x0003",wdWord,1)!=S_OK
		)||unitsMoved<=0) {
			break;
		}
		_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_END,VT_I4,&chunkEndOffset);
		//Make sure  that the end is not past the requested end after the move
		if(chunkEndOffset>(args->endOffset)) {
			_com_dispatch_propput(pDispatchRange,wdDISPID_RANGE_END,VT_I4,args->endOffset);
			chunkEndOffset=args->endOffset;
		}
		XMLStream<<L"<text ";
		if(firstLoop) {
			generateXMLAttribsForFormatting(pDispatchRange,chunkStartOffset,chunkEndOffset,initialformatConfig,initialFormatAttribsStream);
		}
		XMLStream<<initialFormatAttribsStream.str();
		generateXMLAttribsForFormatting(pDispatchRange,chunkStartOffset,chunkEndOffset,formatConfig,XMLStream);
		XMLStream<<L">";
		if(firstLoop) {
			//If there is no general formatting to look for  then expand all the way to the end
			if(!formatConfig) {
				_com_dispatch_propput(pDispatchRange,wdDISPID_RANGE_END,VT_I4,args->endOffset);
				chunkEndOffset=args->endOffset;
			}
			firstLoop=false;
		}
		_com_dispatch_propget(pDispatchRange,wdDISPID_RANGE_TEXT,VT_BSTR,&text);
		if(text) {
			XMLStream<<text;
			SysFreeString(text);
			text=NULL;
		}
		XMLStream<<L"</text>";
		_com_dispatch_method(pDispatchRange,wdDISPID_RANGE_COLLAPSE,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003",wdCollapseEnd);
		chunkStartOffset=chunkEndOffset;
	} while(chunkEndOffset<(args->endOffset));
	XMLStream<<L"</control>";
	args->text=SysAllocString(XMLStream.str().c_str());
}

LRESULT CALLBACK winword_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if(pcwp->message==wm_winword_expandToLine) {
		winword_expandToLine_helper(pcwp->hwnd,reinterpret_cast<winword_expandToLine_args*>(pcwp->wParam));
	} else if(pcwp->message==wm_winword_getTextInRange) {
		winword_getTextInRange_helper(pcwp->hwnd,reinterpret_cast<winword_getTextInRange_args*>(pcwp->wParam));
		winword_expandToLine_helper(pcwp->hwnd,reinterpret_cast<winword_expandToLine_args*>(pcwp->wParam));
	}
	return 0;
}

error_status_t nvdaInProcUtils_winword_expandToLine(handle_t bindingHandle, const long windowHandle, const int offset, int* lineStart, int* lineEnd) {
	winword_expandToLine_args args={offset,3,4};
	DWORD_PTR wmRes=0;
	SendMessageTimeout((HWND)windowHandle,wm_winword_expandToLine,(WPARAM)&args,0,SMTO_ABORTIFHUNG,2000,&wmRes);
	*lineStart=args.lineStart;
	*lineEnd=args.lineEnd;
	return RPC_S_OK;
}

error_status_t nvdaInProcUtils_winword_getTextInRange(handle_t bindingHandle, const long windowHandle, const int startOffset, const int endOffset, const long formatConfig, BSTR* text) { 
	winword_getTextInRange_args args={startOffset,endOffset,formatConfig,NULL};
	DWORD_PTR wmRes=0;
	SendMessageTimeout((HWND)windowHandle,wm_winword_getTextInRange,(WPARAM)&args,0,SMTO_ABORTIFHUNG,2000,&wmRes);
	*text=args.text;
	return RPC_S_OK;
}

void winword_inProcess_initialize() {
	wm_winword_expandToLine=RegisterWindowMessage(L"wm_winword_expandToLine");
	wm_winword_getTextInRange=RegisterWindowMessage(L"wm_winword_getTextInRange");
	registerWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}

void winword_inProcess_terminate() {
	unregisterWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}
