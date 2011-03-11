#appModules/devenv.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 Soronel Haetir <soronel.haetir@gmail.com>
#
# Suggestions from James Teh <jamie@nvaccess.org> have been used.
#
# Visual Studio 2005/2008 support for NVDA.
#	I believe this code should work for VS2002/2003 as well but have no way of testing that.
# I have confirmed this script requires at least Visual Studio Standard, as the Express editions
#	don't register themselves with the running object table.
# I have tried several means of getting around this, so far without success.
#
# I started with revision 3493 of the main NVDA branch for this work.
#
# !!! IMPORTANT !!!
#
# I had to modify many of the members of IVsTextManager and IVsTextView to cut down on dependencies.
# Specifically any interface pointers other than IVsTextView have been changed to IUnknown
# Also, many structure and enumerations have been replaced with c_int.
# 
# If NVDA becomes more dependant on the Visual Studio SDK interfaces the embedded wrappers
# should be dropped in favor of the type library.
#
# !!! END OF IMPORTANT INFORMATION !!!
#
# The Visual Studio 2008 SDK is required if you wish
#		to generate python type wrappers.  It can be downloaded at:
#		http://www.microsoft.com/downloads/details.aspx?familyid=59EC6EC3-4273-48A3-BA25-DC925A45584D&displaylang=en
# Use the MIDL compiler to build textmgr.tlb.
# From \Program Files\Microsoft Visual Studio 2008 SDK\VisualStudioIntegration\Common\IDL:
# midl /I ..\inc textmgr.idl
# and then copy the resulting typelib to your sources\typelibs directory.
#

import ctypes
import objbase
from comtypes import IUnknown, IServiceProvider , GUID, COMMETHOD, HRESULT, BSTR
from ctypes import POINTER, c_int, c_short, c_ushort, c_ulong
import comtypes.client.dynamic
from comtypes.automation import IDispatch

from logHandler import log
import textInfos.offsets

from NVDAObjects.behaviors import EditableTextWithoutAutoSelectDetection
from NVDAObjects.window import Window

from NVDAObjects.window import DisplayModelEditableText

import appModuleHandler


#
# A few helpful constants
#

VsRootWindowClassName="wndclass_desked_gsk"
VsTextEditPaneClassName="VsTextEditPane"

SVsTextManager = GUID('{F5E7E71D-1401-11D1-883B-0000F87579D2}')
VsVersion_None = 0
VsVersion_2002 = 1
VsVersion_2003 = 2
VsVersion_2005 = 3
VsVersion_2008 = 4

# Possible values of the VS .Type property of VS windows.
# According to the docs this property should not be used but I have not been able to determine all of the needed values
# of the .Kind property which is the suggested alternative.
#
# I don't have a type library or header defining the VsWindowType enumeration so only .Type values
#		I've actually encountered are defined.
# Known missing values are:
#	CodeWindow, Designer, Browser, Watch, Locals,
#	SolutionExplorer, Properties, Find, FindReplace, Toolbox, LinkedWindowFrame, MainWindow, Preview,
#	ColorPalettte, ToolWindowTaskList, Autos, CallStack, Threads, DocumentOutline, RunningDocuments
# Most of these host controls which should hopefully be the "real" window by the time any text needs to be rendered.
VsWindowTypeCommand = 15
VsWindowTypeDocument = 16
VsWindowTypeOutput = 17

# Scroll bar selector
SB_HORZ = 0
SB_VERT = 1


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# Only use this overlay class if the top level automation object for the IDE can be retrieved,
		# as it will not work otherwise.
		if obj.windowClassName == VsTextEditPaneClassName and self._getDTE():
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList.insert(0, VsTextEditPane)
			
	def _getDTE(self):
	# Return the already fetched instance if there is one.
		try:
			if self._DTE:
				return self._DTE
		except AttributeError:
			pass
		
		# Retrieve and cache the top level automation object for the IDE
		DTEVersion = VsVersion_None
		bctx = objbase.CreateBindCtx()
		ROT = objbase.GetRunningObjectTable()
		for mon in ROT:
		# Test for the strings Visual Studio may have registered with.
			displayName = mon.GetDisplayName(bctx, None)
			if "!VisualStudio.DTE.9.0:%d"%self.processID==displayName:
				DTEVersion=VsVersion_2008
			elif "!VisualStudio.DTE.8.0:%d"%self.processID==displayName:
				DTEVersion = VsVersion_2005
			elif "!VisualStudio.DTE.7.1:%d"%self.processID==displayName:
				DTEVersion = VsVersion_2003
			elif "!VisualStudio.DTE:%d"%self.processID==displayName:
				DTEVersion = VsVersion_2002
				
			if DTEVersion != VsVersion_None:
				self._DTEVersion = DTEVersion
				self._DTE = comtypes.client.dynamic.Dispatch(ROT.GetObject(mon).QueryInterface(IDispatch))
				break

		else:
			# None found.
			log.debugWarning("No top level automation object found")
			self._DTE = None
			self._DTEVersion = VsVersion_None

		# Loop has completed
		return self._DTE
		
	def _getTextManager(self):
		try:
			if self._textManager:
				return self._textManager
		except AttributeError:
			pass
		serviceProvider = self._getDTE().QueryInterface(comtypes.IServiceProvider)
		self._textManager = serviceProvider.QueryService(SVsTextManager, IVsTextManager)
		return self._textManager


class VsTextEditPaneTextInfo(textInfos.offsets.OffsetsTextInfo):
	def _InformUnsupportedWindowType(self,type):
		log.error("An unsupported window type `%d' was encountered, please inform the NVDA development team." %type)
		raise NotImplementedError
		
	def _getSelectionObject(self):
		Selection = None
		if self._window.Type == VsWindowTypeDocument:
			Selection = self._window.Selection
		elif self._window.Type == VsWindowTypeOutput:
			Selection = self._window.Object.ActivePane.TextDocument.Selection
		elif self._window.Type==VsWindowTypeCommand:
			Selection = self._window.Object.TextDocument.Selection
		else:
			self._InformUnsupportedWindowType(self._window.Type)
		return Selection
	
	def _createEditPoint(self):
		return self._getSelectionObject().ActivePoint.CreateEditPoint()
		
	def _getOffsetFromPoint(self,x,y):
		yMinUnit, yMaxUnit, yVisible, yFirstVisible = self._textView.GetScrollInfo(SB_VERT)
		hMinUnit, hMaxUnit, hVisible, hFirstVisible = self._textView.GetScrollInfo(SB_HORZ)
		
		# These should probably be cached as they are fairly unlikely to change, but ...
		lineHeight = self._textView.GetLineHeight()
		charWidth = self._window.Width / hVisible

		offsetLine = (y - self._window.Top) / lineHeight + yFirstVisible
		offsetChar = (x - self._window.Left) / charWidth + hFirstVisible
		return self._textView.GetNearestPosition(offsetLine, offsetChar)[0]

	def __init__(self, obj, position):
		self._window = obj._window
		self._textView = obj._textView
		super(VsTextEditPaneTextInfo, self).__init__(obj, position)
	
	def _getCaretOffset(self):
		return self._createEditPoint().AbsoluteCharOffset
		
	def _setCaretOffset(self,offset):
		self._getSelectionObject().MoveToAbsoluteOffset(offset)
		
	def _setSelectionOffsets(self,start,end):
		Selection = self._getSelectionObject()
		Selection.MoveToAbsoluteOffset(start)
		Selection.MoveToAbsoluteOffset(end,True)
		
	def _getSelectionOffsets(self):
		selection = self._getSelectionObject()
		startPos = selection.ActivePoint.CreateEditPoint().AbsoluteCharOffset - 1
		endPos = selection.AnchorPoint.CreateEditPoint().AbsoluteCharOffset - 1
		return (startPos,endPos)
			
	def _getTextRange(self,start,end):
		editPointStart = self._createEditPoint()
		editPointStart.StartOfDocument()
		if start:
			editPointStart.MoveToAbsoluteOffset(start)
		else:
			start = 1
		return editPointStart.GetText(end-start)
		
	def _getWordOffsets(self,startOffset):
		editPointStart = self._createEditPoint()
		editPointEnd = editPointStart.CreateEditPoint()
		editPointEnd.WordRight()
		return editPointStart.AbsoluteCharOffset,editPointEnd.AbsoluteCharOffset
		
	def _getLineOffsets(self,offset):
		editPointStart = self._createEditPoint()
		editPointStart.MoveToAbsoluteOffset(offset)
		editPointStart.StartOfLine()
		editPointEnd = editPointStart.CreateEditPoint()
		editPointEnd.EndOfLine()
		return (editPointStart.AbsoluteCharOffset,editPointEnd.AbsoluteCharOffset)
	
	def _getLineNumFromOffset(self,offset):
		editPoint = self._createEditPoint()
		editPoint.MoveToAbsoluteOffset(offset)
		return editPoint.Line
	
	def _getStoryLength(self):
		editPoint = self._createEditPoint()
		editPoint.EndOfDocument()
		return editPoint.AbsoluteCharOffset


class VsTextEditPane(EditableTextWithoutAutoSelectDetection,Window):
	TextInfo = VsTextEditPaneTextInfo

	def initOverlayClass(self):
		self._window = self.appModule._getDTE().ActiveWindow
		self.location = (self._window.Top,self._window.Left,self._window.Width,self._window.Height)
		self._textView = self.appModule._getTextManager().GetActiveView(True, None)

	def event_valueChange(self):
		pass


class IVsTextView(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{BB23A14B-7C61-469A-9890-A95648CED5E6}')
	_idlflags_ = []


class IVsTextManager(comtypes.IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{909F83E3-B3FC-4BBF-8820-64378744B39B}')
	_idlflags_ = []

IVsTextManager._methods_ = [
	COMMETHOD([], HRESULT, 'RegisterView',
		( ['in'], POINTER(IVsTextView), 'pView' ),
		( ['in'], POINTER(IUnknown), 'pBuffer' )),
	COMMETHOD([], HRESULT, 'UnregisterView',
		( ['in'], POINTER(IVsTextView), 'pView' )),
	COMMETHOD([], HRESULT, 'EnumViews',
		( ['in'], POINTER(IUnknown), 'pBuffer' ),
		( ['out'], POINTER(POINTER(IUnknown)), 'ppEnum' )),
    COMMETHOD([], HRESULT, 'CreateSelectionAction',
              ( ['in'], POINTER(IUnknown), 'pBuffer' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppAction' )),
    COMMETHOD([], HRESULT, 'MapFilenameToLanguageSID',
              ( ['in'], POINTER(c_ushort), 'pszFileName' ),
              ( ['out'], POINTER(GUID), 'pguidLangSID' )),
    COMMETHOD([], HRESULT, 'GetRegisteredMarkerTypeID',
              ( ['in'], POINTER(GUID), 'pguidMarker' ),
              ( ['out'], POINTER(c_int), 'piMarkerTypeID' )),
    COMMETHOD([], HRESULT, 'GetMarkerTypeInterface',
              ( ['in'], c_int, 'iMarkerTypeID' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppMarkerType' )),
    COMMETHOD([], HRESULT, 'GetMarkerTypeCount',
              ( ['out'], POINTER(c_int), 'piMarkerTypeCount' )),
    COMMETHOD([], HRESULT, 'GetActiveView',
              ( ['in'], c_int, 'fMustHaveFocus' ),
              ( ['in'], POINTER(IUnknown), 'pBuffer' ),
              ( ['out'], POINTER(POINTER(IVsTextView)), 'ppView' )),
    COMMETHOD([], HRESULT, 'GetUserPreferences',
              ( ['out'], POINTER(c_int), 'pViewPrefs' ),
              ( ['out'], POINTER(c_int), 'pFramePrefs' ),
              ( ['in', 'out'], POINTER(c_int), 'pLangPrefs' ),
              ( ['in', 'out'], POINTER(c_int), 'pColorPrefs' )),
    COMMETHOD([], HRESULT, 'SetUserPreferences',
              ( ['in'], POINTER(c_int), 'pViewPrefs' ),
              ( ['in'], POINTER(c_int), 'pFramePrefs' ),
              ( ['in'], POINTER(c_int), 'pLangPrefs' ),
              ( ['in'], POINTER(c_int), 'pColorPrefs' )),
    COMMETHOD([], HRESULT, 'SetFileChangeAdvise',
              ( ['in'], POINTER(c_ushort), 'pszFileName' ),
              ( ['in'], c_int, 'fStart' )),
    COMMETHOD([], HRESULT, 'SuspendFileChangeAdvise',
              ( ['in'], POINTER(c_ushort), 'pszFileName' ),
              ( ['in'], c_int, 'fSuspend' )),
    COMMETHOD([], HRESULT, 'NavigateToPosition',
              ( ['in'], POINTER(IUnknown), 'pBuffer' ),
              ( ['in'], POINTER(GUID), 'guidDocViewType' ),
              ( ['in'], c_int, 'iPos' ),
              ( ['in'], c_int, 'iLen' )),
    COMMETHOD([], HRESULT, 'NavigateToLineAndColumn',
              ( ['in'], POINTER(IUnknown), 'pBuffer' ),
              ( ['in'], POINTER(GUID), 'guidDocViewType' ),
              ( ['in'], c_int, 'iStartRow' ),
              ( ['in'], c_int, 'iStartIndex' ),
              ( ['in'], c_int, 'iEndRow' ),
              ( ['in'], c_int, 'iEndIndex' )),
    COMMETHOD([], HRESULT, 'GetBufferSccStatus',
              ( ['in'], POINTER(IUnknown), 'pBufData' ),
              ( ['out'], POINTER(c_int), 'pbNonEditable' )),
    COMMETHOD([], HRESULT, 'RegisterBuffer',
              ( ['in'], POINTER(IUnknown), 'pBuffer' )),
    COMMETHOD([], HRESULT, 'UnregisterBuffer',
              ( ['in'], POINTER(IUnknown), 'pBuffer' )),
    COMMETHOD([], HRESULT, 'EnumBuffers',
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppEnum' )),
    COMMETHOD([], HRESULT, 'GetPerLanguagePreferences',
              ( ['out'], POINTER(c_int), 'pLangPrefs' )),
    COMMETHOD([], HRESULT, 'SetPerLanguagePreferences',
              ( ['in'], POINTER(c_int), 'pLangPrefs' )),
    COMMETHOD([], HRESULT, 'AttemptToCheckOutBufferFromScc',
              ( ['in'], POINTER(IUnknown), 'pBufData' ),
              ( ['out'], POINTER(c_int), 'pfCheckoutSucceeded' )),
    COMMETHOD([], HRESULT, 'GetShortcutManager',
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppShortcutMgr' )),
    COMMETHOD([], HRESULT, 'RegisterIndependentView',
              ( ['in'], POINTER(IUnknown), 'punk' ),
              ( ['in'], POINTER(IUnknown), 'pBuffer' )),
    COMMETHOD([], HRESULT, 'UnregisterIndependentView',
              ( ['in'], POINTER(IUnknown), 'punk' ),
              ( ['in'], POINTER(IUnknown), 'pBuffer' )),
    COMMETHOD([], HRESULT, 'IgnoreNextFileChange',
              ( ['in'], POINTER(IUnknown), 'pBuffer' )),
    COMMETHOD([], HRESULT, 'AdjustFileChangeIgnoreCount',
              ( ['in'], POINTER(IUnknown), 'pBuffer' ),
              ( ['in'], c_int, 'fIgnore' )),
    COMMETHOD([], HRESULT, 'GetBufferSccStatus2',
              ( ['in'], POINTER(c_ushort), 'pszFileName' ),
              ( ['out'], POINTER(c_int), 'pbNonEditable' ),
              ( ['out'], POINTER(c_int), 'piStatusFlags' )),
    COMMETHOD([], HRESULT, 'AttemptToCheckOutBufferFromScc2',
              ( ['in'], POINTER(c_ushort), 'pszFileName' ),
              ( ['out'], POINTER(c_int), 'pfCheckoutSucceeded' ),
              ( ['out'], POINTER(c_int), 'piStatusFlags' )),
    COMMETHOD([], HRESULT, 'EnumLanguageServices',
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppEnum' )),
    COMMETHOD([], HRESULT, 'EnumIndependentViews',
              ( ['in'], POINTER(IUnknown), 'pBuffer' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppEnum' )),
]


IVsTextView._methods_ = [
    COMMETHOD([], HRESULT, 'Initialize',
              ( ['in'], POINTER(IUnknown), 'pBuffer' ),
              ( ['in'], comtypes.wireHWND, 'hwndParent' ),
              ( ['in'], c_ulong, 'InitFlags' ),
              ( ['in'], POINTER(c_int), 'pInitView' )),
    COMMETHOD([], HRESULT, 'CloseView'),
    COMMETHOD([], HRESULT, 'GetCaretPos',
              ( ['out'], POINTER(c_int), 'piLine' ),
              ( ['out'], POINTER(c_int), 'piColumn' )),
    COMMETHOD([], HRESULT, 'SetCaretPos',
              ( ['in'], c_int, 'iLine' ),
              ( ['in'], c_int, 'iColumn' )),
    COMMETHOD([], HRESULT, 'GetSelectionSpan',
              ( ['out'], POINTER(c_int), 'pSpan' )),
    COMMETHOD([], HRESULT, 'GetSelection',
              ( ['out'], POINTER(c_int), 'piAnchorLine' ),
              ( ['out'], POINTER(c_int), 'piAnchorCol' ),
              ( ['out'], POINTER(c_int), 'piEndLine' ),
              ( ['out'], POINTER(c_int), 'piEndCol' )),
    COMMETHOD([], HRESULT, 'SetSelection',
              ( ['in'], c_int, 'iAnchorLine' ),
              ( ['in'], c_int, 'iAnchorCol' ),
              ( ['in'], c_int, 'iEndLine' ),
              ( ['in'], c_int, 'iEndCol' )),
    COMMETHOD([], c_int, 'GetSelectionMode'),
    COMMETHOD([], HRESULT, 'SetSelectionMode',
              ( ['in'], c_int, 'iSelMode' )),
    COMMETHOD([], HRESULT, 'ClearSelection',
              ( ['in'], c_int, 'fMoveToAnchor' )),
    COMMETHOD([], HRESULT, 'CenterLines',
              ( ['in'], c_int, 'iTopLine' ),
              ( ['in'], c_int, 'iCount' )),
    COMMETHOD([], HRESULT, 'GetSelectedText',
              ( ['out'], POINTER(BSTR), 'pbstrText' )),
    COMMETHOD([], HRESULT, 'GetSelectionDataObject',
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppIDataObject' )),
    COMMETHOD([], HRESULT, 'GetTextStream',
              ( ['in'], c_int, 'iTopLine' ),
              ( ['in'], c_int, 'iTopCol' ),
              ( ['in'], c_int, 'iBottomLine' ),
              ( ['in'], c_int, 'iBottomCol' ),
              ( ['out'], POINTER(BSTR), 'pbstrText' )),
    COMMETHOD([], HRESULT, 'GetBuffer',
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppBuffer' )),
    COMMETHOD([], HRESULT, 'SetBuffer',
              ( ['in'], POINTER(IUnknown), 'pBuffer' )),
    COMMETHOD([], comtypes.wireHWND, 'GetWindowHandle'),
    COMMETHOD([], HRESULT, 'GetScrollInfo',
              ( ['in'], c_int, 'iBar' ),
              ( ['out'], POINTER(c_int), 'piMinUnit' ),
              ( ['out'], POINTER(c_int), 'piMaxUnit' ),
              ( ['out'], POINTER(c_int), 'piVisibleUnits' ),
              ( ['out'], POINTER(c_int), 'piFirstVisibleUnit' )),
    COMMETHOD([], HRESULT, 'SetScrollPosition',
              ( ['in'], c_int, 'iBar' ),
              ( ['in'], c_int, 'iFirstVisibleUnit' )),
    COMMETHOD([], HRESULT, 'AddCommandFilter',
              ( ['in'], POINTER(IUnknown), 'pNewCmdTarg' ),
              ( ['out'], POINTER(POINTER(IUnknown)), 'ppNextCmdTarg' )),
    COMMETHOD([], HRESULT, 'RemoveCommandFilter',
              ( ['in'], POINTER(IUnknown), 'pCmdTarg' )),
    COMMETHOD([], HRESULT, 'UpdateCompletionStatus',
              ( ['in'], POINTER(IUnknown), 'pCompSet' ),
              ( ['in'], c_ulong, 'dwFlags' )),
    COMMETHOD([], HRESULT, 'UpdateTipWindow',
              ( ['in'], POINTER(IUnknown), 'pTipWindow' ),
              ( ['in'], c_ulong, 'dwFlags' )),
    COMMETHOD([], HRESULT, 'GetWordExtent',
              ( ['in'], c_int, 'iLine' ),
              ( ['in'], c_int, 'iCol' ),
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['out'], POINTER(c_int), 'pSpan' )),
    COMMETHOD([], HRESULT, 'RestrictViewRange',
              ( ['in'], c_int, 'iMinLine' ),
              ( ['in'], c_int, 'iMaxLine' ),
              ( ['in'], POINTER(IUnknown), 'pClient' )),
    COMMETHOD([], HRESULT, 'ReplaceTextOnLine',
              ( ['in'], c_int, 'iLine' ),
              ( ['in'], c_int, 'iStartCol' ),
              ( ['in'], c_int, 'iCharsToReplace' ),
              ( ['in'], POINTER(c_ushort), 'pszNewText' ),
              ( ['in'], c_int, 'iNewLen' )),
    COMMETHOD([], HRESULT, 'GetLineAndColumn',
              ( ['in'], c_int, 'iPos' ),
              ( ['out'], POINTER(c_int), 'piLine' ),
              ( ['out'], POINTER(c_int), 'piIndex' )),
    COMMETHOD([], HRESULT, 'GetNearestPosition',
              ( ['in'], c_int, 'iLine' ),
              ( ['in'], c_int, 'iCol' ),
              ( ['out'], POINTER(c_int), 'piPos' ),
              ( ['out'], POINTER(c_int), 'piVirtualSpaces' )),
    COMMETHOD([], HRESULT, 'UpdateViewFrameCaption'),
    COMMETHOD([], HRESULT, 'CenterColumns',
              ( ['in'], c_int, 'iLine' ),
              ( ['in'], c_int, 'iLeftCol' ),
              ( ['in'], c_int, 'iColCount' )),
    COMMETHOD([], HRESULT, 'EnsureSpanVisible',
              ( ['in'], c_int, 'span' )),
    COMMETHOD([], HRESULT, 'PositionCaretForEditing',
              ( ['in'], c_int, 'iLine' ),
              ( ['in'], c_int, 'cIndentLevels' )),
    COMMETHOD([], HRESULT, 'GetPointOfLineColumn',
              ( ['in'], c_int, 'iLine' ),
              ( ['in'], c_int, 'iCol' ),
              ( ['retval', 'out'], POINTER(ctypes.wintypes.tagPOINT), 'ppt' )),
    COMMETHOD([], HRESULT, 'GetLineHeight',
              ( ['retval', 'out'], POINTER(c_int), 'piLineHeight' )),
    COMMETHOD([], HRESULT, 'HighlightMatchingBrace',
              ( ['in'], c_ulong, 'dwFlags' ),
              ( ['in'], c_ulong, 'cSpans' ),
              ( ['in'], POINTER(c_int), 'rgBaseSpans' )),
    COMMETHOD([], HRESULT, 'SendExplicitFocus'),
    COMMETHOD([], HRESULT, 'SetTopLine',
              ( ['in'], c_int, 'iBaseLine' )),
]
