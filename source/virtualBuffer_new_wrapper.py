from ctypes import *

class attribute_t(Structure):
	_fields_=[('name',c_wchar_p),('value',c_wchar_p)]

class multyValueAttribute_t(Structure):
	_fields_=[('name',c_wchar_p),('value',POINTER(c_wchar_p))]

dll=cdll.virtualBuffer_new

VBufStorage_createBuffer=dll.VBufStorage_createBuffer
VBufStorage_getBufferNodeWithID=dll.VBufStorage_getBufferNodeWithID
VBufStorage_mergeBuffer=dll.VBufStorage_mergeBuffer
VBufStorage_destroyBuffer=dll.VBufStorage_destroyBuffer
VBufStorage_clearBuffer=dll.VBufStorage_clearBuffer
VBufStorage_splitTextNodeAtOffset=dll.VBufStorage_splitTextNodeAtOffset

def VBufStorage_addTagNodeToBuffer(parent, previous, ID,attribs):
	if not isinstance(attribs,dict) or len(attribs)==0:
		raiseValueError("attribs must be of type dict containing 1 or more entries")
	cAttribs=attribute_t*len(attribs)
	for index,name in enumerate(attribs.keys()):
		cAttribs[index].name=name
		cAttribs[index].value=attribs[name]
	return dll.VBufStorage_addTagNodeToBuffer(parent,previous,ID,cAttribs,len(cAttribs))
 
VBufStorage_addTextNodeToBuffer=dll.VBufStorage_addTextNodeToBuffer
VBufStorage_removeNodeFromBuffer=dll.VBufStorage_removeNodeFromBuffer
VBufStorage_removeDescendantsFromBufferNode=dll.VBufStorage_removeDescendantsFromBufferNode
VBufStorage_getFieldIDFromBufferOffset=dll.VBufStorage_getFieldIDFromBufferOffset

def VBufStorage_getBufferOffsetsFromFieldID(buf, ID):
	start=c_int()
	end=c_int()
	dll.VBufStorage_getBufferOffsetsFromFieldID(buf,ID,byref(start),byref(end))
	return (start.value,end.value)

def VBufStorage_findBufferFieldIDByProperties(buf,direction,startID,attribs):
	if not isinstance(attribs,dict) or len(attribs)==0:
		raiseValueError("attribs must be of type dict containing 1 or more entries")
	cAttribs=multyValueAttribute_t*len(attribs)
	for index,name in enumerate(attribs.keys()):
		cAttribs[index].name=name
		vals=(c_wchar_p*len(attribs[name]))()
		for valIndex,val in enumerate(attribs[name]):
			vals[valIndex]=val
		cAttribs[index].value=vals
	return dll.VBufStorage_findBufferFieldIDByProperties(buf,direction,startID,cAttribs,len(cAttribs))

VBufStorage_getBufferTextLength=dll.VBufStorage_getBufferTextLength
VBufStorage_getBufferFieldCount=dll.VBufStorage_getBufferFieldCount
VBufStorage_findBufferText=dll.VBufStorage_findBufferText

def VBufStorage_getBufferTextByOffsets(buf,startOffset,endOffset):
	text=create_unicode_buffer((endOffset-startOffset)+1)
	dll.VBufStorage_getBufferTextByOffsets(buf,startOffset,endOffset,text)
	return text

def VBufStorage_getXMLContextAtBufferOffset(buf,offset):
	textLength=dll.VBufStorage_getXMLContextAtBufferOffset(buf,offset,None)
	textBuf=create_unicode_buffer(textLength)
	dll.VBufStorage_getXMLContextAtBufferOffset(buf,offset,textBuf)
	return textBuf.value

def VBufStorage_getXMLBufferTextByOffsets(buf,startOffset,endOffset):
	textLength=dll.VBufStorage_getXMLBufferTextByOffsets(buf,startOffset,endOffset,None)
	textBuf=create_unicode_buffer(textLength)
	dll.VBufStorage_getXMLBufferTextByOffsets(buf,startOffset,endOffset,textBuf)
	return textBuf.value

def VBufStorage_getBufferLineOffsets(buf,offset):
	startOffset=c_int()
	endOffset=c_int()
	dll.VBufStorage_getBufferLineOffsets(buf,offset,byref(startOffset),byref(endOffset))
	return (startOffset,endOffset)

def VBufStorage_getBufferSelection(buf):
	startOffset=c_int()
	endOffset=c_int()
	dll.VBufStorage_getBufferSelectionOffsets(buf,byref(startOffset),byref(endOffset))
	return (startOffset,endOffset)

VBufStorage_setBufferSelectionOffsets=dll.VBufStorage_setBufferSelectionOffsets
