# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2025 NV Access Limited, Peter Vagner, Davy Kager, Mozilla Corporation, Google LLC,
# Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import (
	c_ushort,
	c_void_p,
	c_size_t,
	cdll,
	CFUNCTYPE,
	Structure,
	c_voidp,
	c_bool,
	c_int,
	c_long,
	c_ulong,
	c_longlong,
	c_ulonglong,
	POINTER,
	c_char_p,
	c_wchar_p,
	c_float,
	c_uint,
)
from ctypes.wintypes import (
	DWORD,
	HANDLE,
	HWND,
	RECT,
)
from comtypes import (
	HRESULT,
	BSTR,
	IUnknown,
	GUID,
)
from comtypes.automation import VARIANT
import NVDAState
from winBindings.mmeapi import WAVEFORMATEX


DWORD_PTR = c_size_t


dll = cdll.LoadLibrary(NVDAState.ReadPaths.nvdaHelperLocalDll)

nvdaHelperLocal_initialize = dll.nvdaHelperLocal_initialize
nvdaHelperLocal_initialize.restype = c_voidp
nvdaHelperLocal_initialize.argtypes = (
	c_bool,  # secureMode
)

nvdaHelperLocal_terminate = dll.nvdaHelperLocal_terminate
nvdaHelperLocal_terminate.restype = None
nvdaHelperLocal_terminate.argtypes = ()

createRemoteBindingHandle = dll.createRemoteBindingHandle
createRemoteBindingHandle.restype = HANDLE
createRemoteBindingHandle.argtypes = (
	c_wchar_p,  # uuidString
)

cancellableSendMessageTimeout = dll.cancellableSendMessageTimeout
cancellableSendMessageTimeout.restype = c_int
# we use c_void_p for WPARAM and LPARAM as this gives us the greatest flexibility
# of passing in Python native ints, ctypes arrays, pointers etc.
cancellableSendMessageTimeout.argtypes = (
	HWND,  # hwnd
	c_uint,  # msg
	c_void_p,  # wParam
	c_void_p,  # lParam
	c_uint,  # fuFlags
	c_uint,  # uTimeout
	POINTER(DWORD_PTR),  # lpdwResult
)

generateBeep = dll.generateBeep
generateBeep.restype = c_int
generateBeep.argtypes = (
	c_char_p,  # buff
	c_float,  # hz
	c_int,  # length
	c_int,  # left
	c_int,  # right
)

nvdaInProcUtils_registerNVDAProcess = dll.nvdaInProcUtils_registerNVDAProcess
nvdaInProcUtils_registerNVDAProcess.restype = c_int  # error_status_t
nvdaInProcUtils_registerNVDAProcess.argtypes = (
	HANDLE,  # bindingHandle
	POINTER(c_void_p),  # registrationhandle
)

nvdaInProcUtils_unregisterNVDAProcess = dll.nvdaInProcUtils_unregisterNVDAProcess
nvdaInProcUtils_unregisterNVDAProcess.restype = c_int  # error_status_t
nvdaInProcUtils_unregisterNVDAProcess.argtypes = (
	POINTER(c_void_p),  # registrationhandle
)

nvdaInProcUtils_winword_expandToLine = dll.nvdaInProcUtils_winword_expandToLine
nvdaInProcUtils_winword_expandToLine.restype = c_int  # error_status_t
nvdaInProcUtils_winword_expandToLine.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # offset
	POINTER(c_int),  # lineStart
	POINTER(c_int),  # lineEnd
)

nvdaInProcUtils_winword_getTextInRange = dll.nvdaInProcUtils_winword_getTextInRange
nvdaInProcUtils_winword_getTextInRange.restype = c_int  # error_status_t
nvdaInProcUtils_winword_getTextInRange.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # startOffset
	c_int,  # endOffset
	c_long,  # formatConfig
	POINTER(BSTR),  # text
)

nvdaInProcUtils_winword_moveByLine = dll.nvdaInProcUtils_winword_moveByLine
nvdaInProcUtils_winword_moveByLine.restype = c_int  # error_status_t
nvdaInProcUtils_winword_moveByLine.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # offset
	c_int,  # moveBack
	POINTER(c_int),  # newOffset
)

nvdaInProcUtils_sysListView32_getGroupInfo = dll.nvdaInProcUtils_sysListView32_getGroupInfo
nvdaInProcUtils_sysListView32_getGroupInfo.restype = c_int  # error_status_t
nvdaInProcUtils_sysListView32_getGroupInfo.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # groupIndex
	POINTER(BSTR),  # header
	POINTER(BSTR),  # footer
	POINTER(c_int),  # state
)

nvdaInProcUtils_sysListView32_getColumnContent = dll.nvdaInProcUtils_sysListView32_getColumnContent
nvdaInProcUtils_sysListView32_getColumnContent.restype = c_int  # error_status_t
nvdaInProcUtils_sysListView32_getColumnContent.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # item
	c_int,  # subItem
	POINTER(BSTR),  # text
)

nvdaInProcUtils_sysListView32_getColumnLocation = dll.nvdaInProcUtils_sysListView32_getColumnLocation
nvdaInProcUtils_sysListView32_getColumnLocation.restype = c_int  # error_status_t
nvdaInProcUtils_sysListView32_getColumnLocation.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # item
	c_int,  # subItem
	POINTER(RECT),  # location
)

nvdaInProcUtils_sysListView32_getColumnHeader = dll.nvdaInProcUtils_sysListView32_getColumnHeader
nvdaInProcUtils_sysListView32_getColumnHeader.restype = c_int  # error_status_t
nvdaInProcUtils_sysListView32_getColumnHeader.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # subItem
	POINTER(BSTR),  # text
)

nvdaInProcUtils_sysListView32_getColumnOrderArray = dll.nvdaInProcUtils_sysListView32_getColumnOrderArray
nvdaInProcUtils_sysListView32_getColumnOrderArray.restype = c_int  # error_status_t
nvdaInProcUtils_sysListView32_getColumnOrderArray.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	c_int,  # columnCount
	POINTER(c_int),  # columnOrderArray
)

nvdaInProcUtils_getActiveObject = dll.nvdaInProcUtils_getActiveObject
nvdaInProcUtils_getActiveObject.restype = c_int  # error_status_t
nvdaInProcUtils_getActiveObject.argtypes = (
	HANDLE,  # bindingHandle
	c_wchar_p,  # progid
	POINTER(POINTER(IUnknown)),  # ppUnknown
)

nvdaInProcUtils_dumpOnCrash = dll.nvdaInProcUtils_dumpOnCrash
nvdaInProcUtils_dumpOnCrash.restype = c_int  # error_status_t
nvdaInProcUtils_dumpOnCrash.argtypes = (
	HANDLE,  # bindingHandle
	c_wchar_p,  # minidumpPath
)

nvdaInProcUtils_IA2Text_findContentDescendant = dll.nvdaInProcUtils_IA2Text_findContentDescendant
nvdaInProcUtils_IA2Text_findContentDescendant.restype = c_int  # error_status_t
nvdaInProcUtils_IA2Text_findContentDescendant.argtypes = (
	HANDLE,  # bindingHandle
	c_ulong,  # hwnd
	c_long,  # parentID
	c_long,  # what
	POINTER(c_long),  # descendantID
	POINTER(c_long),  # descendantOffset
)

nvdaInProcUtils_getTextFromIAccessible = dll.nvdaInProcUtils_getTextFromIAccessible
nvdaInProcUtils_getTextFromIAccessible.restype = c_int  # error_status_t
nvdaInProcUtils_getTextFromIAccessible.argtypes = (
	HANDLE,  # bindingHandle
	c_ulong,  # hwnd
	c_long,  # parentID
	POINTER(BSTR),  # textBuf
	c_bool,  # recurse
	c_bool,  # includeTopLevelText
)

nvdaInProcUtils_outlook_getMAPIProp = dll.nvdaInProcUtils_outlook_getMAPIProp
nvdaInProcUtils_outlook_getMAPIProp.restype = c_int  # error_status_t
nvdaInProcUtils_outlook_getMAPIProp.argtypes = (
	HANDLE,  # IDL_handle
	c_long,  # threadID
	POINTER(IUnknown),  # mapiObject
	c_ulong,  # mapiPropTag
	POINTER(VARIANT),  # val
)


class EXCEL_CELLINFO(Structure):
	_fields_ = [
		("text", BSTR),
		("address", BSTR),
		("inputTitle", BSTR),
		("inputMessage", BSTR),
		("nvCellStates", c_longlong),  # bitwise OR of the NvCellState enum values.
		("rowNumber", c_long),
		("rowSpan", c_long),
		("columnNumber", c_long),
		("columnSpan", c_long),
		("outlineLevel", c_long),
		("comments", BSTR),
		("formula", BSTR),
	]


nvdaInProcUtils_excel_getCellInfos = dll.nvdaInProcUtils_excel_getCellInfos
nvdaInProcUtils_excel_getCellInfos.restype = c_int  # error_status_t
nvdaInProcUtils_excel_getCellInfos.argtypes = (
	HANDLE,  # IDL_handle
	c_ulong,  # windowHandle
	BSTR,  # rangeAddress
	c_long,  # cellInfoFlags
	c_long,  # cellCount
	POINTER(EXCEL_CELLINFO),  # cellInfos
	POINTER(c_long),  # numCellsFetched
)

VBufRemote_bufferHandle_t = c_void_p
VBufRemote_nodeHandle_t = c_ulonglong  # MIDL_uhyper

VBuf_createBuffer = dll.VBuf_createBuffer
VBuf_createBuffer.restype = VBufRemote_bufferHandle_t
VBuf_createBuffer.argtypes = (
	HANDLE,  # bindingHandle
	c_int,  # docHandle
	c_int,  # ID
	c_wchar_p,  # backendName
)

VBuf_destroyBuffer = dll.VBuf_destroyBuffer
VBuf_destroyBuffer.restype = None
VBuf_destroyBuffer.argtypes = (
	POINTER(VBufRemote_bufferHandle_t),  # buffer
)

VBuf_findNodeByAttributes = dll.VBuf_findNodeByAttributes
VBuf_findNodeByAttributes.restype = c_int
VBuf_findNodeByAttributes.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	c_int,  # offset
	c_int,  # direction
	c_wchar_p,  # attribs
	c_wchar_p,  # regexp
	POINTER(c_int),  # startOffset
	POINTER(c_int),  # endOffset
	POINTER(VBufRemote_nodeHandle_t),  # foundNode
)

VBuf_getControlFieldNodeWithIdentifier = dll.VBuf_getControlFieldNodeWithIdentifier
VBuf_getControlFieldNodeWithIdentifier.restype = c_int
VBuf_getControlFieldNodeWithIdentifier.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	c_int,  # docHandle
	c_int,  # ID
	POINTER(VBufRemote_nodeHandle_t),  # foundNode
)

VBuf_getFieldNodeOffsets = dll.VBuf_getFieldNodeOffsets
VBuf_getFieldNodeOffsets.restype = c_int
VBuf_getFieldNodeOffsets.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	VBufRemote_nodeHandle_t,  # node
	POINTER(c_int),  # startOffset
	POINTER(c_int),  # endOffset
)

VBuf_getIdentifierFromControlFieldNode = dll.VBuf_getIdentifierFromControlFieldNode
VBuf_getIdentifierFromControlFieldNode.restype = c_int
VBuf_getIdentifierFromControlFieldNode.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	VBufRemote_nodeHandle_t,  # node
	POINTER(c_int),  # docHandle
	POINTER(c_int),  # ID
)

VBuf_getLineOffsets = dll.VBuf_getLineOffsets
VBuf_getLineOffsets.restype = c_int
VBuf_getLineOffsets.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	c_int,  # offset
	c_int,  # maxLineLength
	c_bool,  # useScreenLayout
	POINTER(c_int),  # startOffset
	POINTER(c_int),  # endOffset
)

VBuf_getSelectionOffsets = dll.VBuf_getSelectionOffsets
VBuf_getSelectionOffsets.restype = c_int
VBuf_getSelectionOffsets.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	POINTER(c_int),  # startOffset
	POINTER(c_int),  # endOffset
)

VBuf_setSelectionOffsets = dll.VBuf_setSelectionOffsets
VBuf_setSelectionOffsets.restype = c_int
VBuf_setSelectionOffsets.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	c_int,  # startOffset
	c_int,  # endOffset
)

VBuf_getTextInRange = dll.VBuf_getTextInRange
VBuf_getTextInRange.restype = c_int
VBuf_getTextInRange.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	c_int,  # startOffset
	c_int,  # endOffset
	POINTER(c_wchar_p),  # text
	c_bool,  # useMarkup
)

# special handling to ensure that the bstr is freed correctly.
VBuf_getTextInRange = CFUNCTYPE(c_int, VBufRemote_bufferHandle_t, c_int, c_int, POINTER(BSTR), c_int)(  # noqa: F405
	("VBuf_getTextInRange", dll),
	((1,), (1,), (1,), (2,), (1,)),
)

VBuf_getTextLength = dll.VBuf_getTextLength
VBuf_getTextLength.restype = c_int
VBuf_getTextLength.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
)

VBuf_isFieldNodeAtOffset = dll.VBuf_isFieldNodeAtOffset
VBuf_isFieldNodeAtOffset.restype = c_int
VBuf_isFieldNodeAtOffset.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	VBufRemote_nodeHandle_t,  # node
	c_int,  # offset
)

VBuf_locateTextFieldNodeAtOffset = dll.VBuf_locateTextFieldNodeAtOffset
VBuf_locateTextFieldNodeAtOffset.restype = c_int
VBuf_locateTextFieldNodeAtOffset.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	c_int,  # offset
	POINTER(c_int),  # nodeStartOffset,
	POINTER(c_int),  # nodeEndOffset,
	POINTER(VBufRemote_nodeHandle_t),  # foundNode
)

VBuf_locateControlFieldNodeAtOffset = dll.VBuf_locateControlFieldNodeAtOffset
VBuf_locateControlFieldNodeAtOffset.restype = c_int
VBuf_locateControlFieldNodeAtOffset.argtypes = (
	VBufRemote_bufferHandle_t,  # buffer
	c_int,  # offset
	POINTER(c_int),  # nodeStartOffset,
	POINTER(c_int),  # nodeEndOffset,
	POINTER(c_int),  # docHandle,
	POINTER(c_int),  # ID,
	POINTER(VBufRemote_nodeHandle_t),  # foundNode
)

getOleClipboardText = dll.getOleClipboardText
getOleClipboardText.restype = HRESULT
getOleClipboardText.argtypes = (
	POINTER(IUnknown),  # object that supports IDataObject
	POINTER(BSTR),  # BSTR* text
)

getOleUserType = dll.getOleUserType
getOleUserType.restype = HRESULT
getOleUserType.argtypes = (
	POINTER(IUnknown),  # object supporting IOLEObject
	DWORD,  # dwFlags
	POINTER(BSTR),  # BSTR* userType
)

audioDucking_shouldDelay = dll.audioDucking_shouldDelay
audioDucking_shouldDelay.restype = c_bool
audioDucking_shouldDelay.argtypes = ()

findWindowWithClassInThread = dll.findWindowWithClassInThread
findWindowWithClassInThread.restype = HWND
findWindowWithClassInThread.argtypes = (
	c_long,  # threadID
	c_wchar_p,  # windowClassName
	c_bool,  # checkVisible
)

dllImportTableHooks_hookSingle = dll.dllImportTableHooks_hookSingle
dllImportTableHooks_hookSingle.restype = c_void_p
dllImportTableHooks_hookSingle.argtypes = (
	c_char_p,  # targetDll
	c_char_p,  # importDll
	c_char_p,  # functionName
	c_void_p,  # newFunction
)

dllImportTableHooks_unhookSingle = dll.dllImportTableHooks_unhookSingle
dllImportTableHooks_unhookSingle.restype = None

dllImportTableHooks_unhookSingle.argtypes = (
	c_void_p,  # hook
)


displayModel_getWindowTextInRect = CFUNCTYPE(
	c_int,  # (return) error_status_t
	HANDLE,  # bindingHandle
	c_long,  # windowHandle
	c_bool,  # includeDescendantWindows
	c_int,  # left
	c_int,  # top
	c_int,  # right
	c_int,  # bottom
	c_int,  # minHorizontalWhitespace
	c_int,  # minVerticalWhitespace
	c_bool,  # stripOuterWhitespace
	POINTER(BSTR),  # text
	POINTER(BSTR),  # characterPoints
)(
	("displayModel_getWindowTextInRect", dll),
	(
		(1,),  # [in] bindingHandle
		(1,),  # [in] windowHandle
		(1,),  # [in] includeDescendantWindows
		(1,),  # [in] left
		(1,),  # [in] top
		(1,),  # [in] right
		(1,),  # [in] bottom
		(1,),  # [in] minHorizontalWhitespace
		(1,),  # [in] minVerticalWhitespace
		(1,),  # [in] stripOuterWhitespace
		(2,),  # [out] text
		(2,),  # [out] characterPoints
	),
)


displayModel_getCaretRect = dll.displayModel_getCaretRect
displayModel_getCaretRect.restype = c_int  # error_status_t
displayModel_getCaretRect.argtypes = (
	HANDLE,  # bindingHandle
	c_long,  # threadID
	POINTER(c_long),  # left
	POINTER(c_long),  # top
	POINTER(c_long),  # right
	POINTER(c_long),  # bottom
)

displayModel_getFocusRect = dll.displayModel_getFocusRect
displayModel_getFocusRect.restype = c_int  # error_status_t
displayModel_getFocusRect.argtypes = (
	HANDLE,  # bindingHandle
	c_ulong,  # hwnd
	POINTER(c_long),  # left
	POINTER(c_long),  # top
	POINTER(c_long),  # right
	POINTER(c_long),  # bottom
)

displayModel_requestTextChangeNotificationsForWindow = (
	dll.displayModel_requestTextChangeNotificationsForWindow
)
displayModel_requestTextChangeNotificationsForWindow.restype = c_int  # error_status_t
displayModel_requestTextChangeNotificationsForWindow.argtypes = (
	HANDLE,  # bindingHandle
	c_ulong,  # windowHandle
	c_bool,  # enable
)

PROPERTYID = c_long

registerUIAProperty = dll.registerUIAProperty
registerUIAProperty.restype = PROPERTYID
registerUIAProperty.argtypes = (
	POINTER(GUID),  # guid
	c_wchar_p,  # programmaticName
	c_int,  # propertyType (UIAutomationType)
)

registerUIAAnnotationType = dll.registerUIAAnnotationType
registerUIAAnnotationType.restype = c_int
registerUIAAnnotationType.argtypes = (
	POINTER(GUID),  # guid
)

HUiaRateLimitedEventHandler = HANDLE

rateLimitedUIAEventHandler_create = dll.rateLimitedUIAEventHandler_create
rateLimitedUIAEventHandler_create.restype = HRESULT
rateLimitedUIAEventHandler_create.argtypes = (
	POINTER(IUnknown),  # pExistingHandler
	POINTER(HUiaRateLimitedEventHandler),  # ppRateLimitedEventHandler
)

rateLimitedUIAEventHandler_terminate = dll.rateLimitedUIAEventHandler_terminate
rateLimitedUIAEventHandler_terminate.restype = HRESULT
rateLimitedUIAEventHandler_terminate.argtypes = (
	HUiaRateLimitedEventHandler,  # pRateLimitedEventHandler
)

HWasapiPlayer = HANDLE

wasPlay_callback = CFUNCTYPE(None, c_void_p, c_uint)

wasPlay_create = dll.wasPlay_create
wasPlay_create.restype = HWasapiPlayer
wasPlay_create.argtypes = (
	c_wchar_p,  # endpointId
	WAVEFORMATEX,  # format
	wasPlay_callback,  # callback
)

wasPlay_destroy = dll.wasPlay_destroy
wasPlay_destroy.restype = None
wasPlay_destroy.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_open = dll.wasPlay_open
wasPlay_open.restype = HRESULT
wasPlay_open.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_feed = dll.wasPlay_feed
wasPlay_feed.restype = HRESULT
wasPlay_feed.argtypes = (
	HWasapiPlayer,  # player
	c_char_p,  # data
	c_uint,  # size
	POINTER(c_uint),  # id
)

wasPlay_stop = dll.wasPlay_stop
wasPlay_stop.restype = HRESULT
wasPlay_stop.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_sync = dll.wasPlay_sync
wasPlay_sync.restype = HRESULT
wasPlay_sync.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_idle = dll.wasPlay_idle
wasPlay_idle.restype = HRESULT
wasPlay_idle.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_pause = dll.wasPlay_pause
wasPlay_pause.restype = HRESULT
wasPlay_pause.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_resume = dll.wasPlay_resume
wasPlay_resume.restype = HRESULT
wasPlay_resume.argtypes = (
	HWasapiPlayer,  # player
)

wasPlay_setChannelVolume = dll.wasPlay_setChannelVolume
wasPlay_setChannelVolume.restype = HRESULT
wasPlay_setChannelVolume.argtypes = (
	HWasapiPlayer,  # player
	c_uint,  # channel
	c_float,  # level
)

wasPlay_startup = dll.wasPlay_startup
wasPlay_startup.restype = HRESULT
wasPlay_startup.argtypes = ()

wasPlay_startTrimmingLeadingSilence = dll.wasPlay_startTrimmingLeadingSilence
wasPlay_startTrimmingLeadingSilence.argtypes = (
	HWasapiPlayer,  # player
	c_bool,  # start
)
wasPlay_startTrimmingLeadingSilence.restype = None

wasSilence_init = dll.wasSilence_init
wasSilence_init.restype = HRESULT
wasSilence_init.argtypes = (
	c_wchar_p,  # endpointId
)

wasSilence_playFor = dll.wasSilence_playFor
wasSilence_playFor.restype = None
wasSilence_playFor.argtypes = (
	DWORD,  # ms
	c_float,  # volume
)

wasSilence_terminate = dll.wasSilence_terminate
wasSilence_terminate.restype = None
wasSilence_terminate.argtypes = ()

nvdaController_onSsmlMarkReached = dll.nvdaController_onSsmlMarkReached
nvdaController_onSsmlMarkReached.restype = c_ulong
nvdaController_onSsmlMarkReached.argtypes = (c_wchar_p,)

calculateCharacterBoundaries = dll.calculateCharacterBoundaries
calculateCharacterBoundaries.restype = c_bool
calculateCharacterBoundaries.argtypes = (
	c_wchar_p,  # text
	c_int,  # textLength
	POINTER(c_int),  #  offsets
	POINTER(c_int),  #  offsetsCount
)

calculateCharacterOffsets = dll.calculateCharacterOffsets
calculateCharacterOffsets.restype = c_bool
calculateCharacterOffsets.argtypes = (
	c_wchar_p,  # text
	c_int,  # textLength
	c_int,  # offset
	POINTER(c_int),  # startOffset
	POINTER(c_int),  # endOffset
)

calculateWordOffsets = dll.calculateWordOffsets
calculateWordOffsets.restype = c_bool
calculateWordOffsets.argtypes = (
	c_wchar_p,  # text
	c_int,  # textLength
	c_int,  # offset
	POINTER(c_int),  # startOffset
	POINTER(c_int),  # endOffset
)

isScreenFullyBlack = dll.isScreenFullyBlack
isScreenFullyBlack.argtypes = tuple()
isScreenFullyBlack.restype = c_bool

localListeningSocketExists = dll.localListeningSocketExists
localListeningSocketExists.argtypes = (c_ushort, c_wchar_p)
localListeningSocketExists.restype = c_bool

writeCrashDump = dll.writeCrashDump
"""
Writes a crash dump to the specified path.
:param dumpPath: Path to write the dump to.
:param exceptionPointers: Pointer to an EXCEPTION_POINTERS structure from an UnhandledExceptionFilter callback.
:return: True on success, False on failure.
"""
writeCrashDump.argtypes = (
	c_wchar_p,  # dumpPath
	c_void_p,  # exceptionPointers
)
writeCrashDump.restype = bool
