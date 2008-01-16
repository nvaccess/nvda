from ctypes import *

VBUF_FINDDIRECTION_NEXT=1
VBUF_FINDDIRECTION_PREVIOUS=2

VBUF_ERROR_NOTFOUND=-7

class attribute_t(Structure):
	_fields_=[('name',c_wchar_p),('value',c_wchar_p)]

class multyValueAttribute_t(Structure):
	_fields_=[('name',c_wchar_p),('value',POINTER(c_wchar_p)),('numValues',c_int)]

dll=cdll.virtualBuffer_new

def dllErrorCheck(res,func,args):
	if res<0:
		raise RuntimeError("error in %s with args of %s, code %s"%(func.__name__,args,res))
	return res

VBufStorage_createBuffer=dll.VBufStorage_createBuffer
VBufStorage_createBuffer.errcheck=dllErrorCheck

VBufStorage_getBufferNodeWithIdentifier=dll.VBufStorage_getBufferNodeWithIdentifier
VBufStorage_getBufferNodeWithIdentifier.errcheck=dllErrorCheck

VBufStorage_mergeBuffer=dll.VBufStorage_mergeBuffer
VBufStorage_mergeBuffer.errcheck=dllErrorCheck

VBufStorage_destroyBuffer=dll.VBufStorage_destroyBuffer
VBufStorage_destroyBuffer.errcheck=dllErrorCheck

VBufStorage_clearBuffer=dll.VBufStorage_clearBuffer
VBufStorage_clearBuffer.errcheck=dllErrorCheck

VBufStorage_splitTextNodeAtOffset=dll.VBufStorage_splitTextNodeAtOffset
VBufStorage_splitTextNodeAtOffset.errcheck=dllErrorCheck

def VBufStorage_addTagNodeToBuffer(parent, previous, docHandle,ID,attribs,isBlock=True):
	if not isinstance(attribs,dict) or len(attribs)==0:
		raiseValueError("attribs must be of type dict containing 1 or more entries")
	cAttribs=(attribute_t*len(attribs))()
	for index,name in enumerate(attribs.keys()):
		cAttribs[index].name=name
		val=attribs[name]
		cAttribs[index].value=unicode(val) if val is not None else ""
	isBlock=1 if isBlock else 0
	return dll.VBufStorage_addTagNodeToBuffer(parent,previous,docHandle,ID,cAttribs,len(cAttribs),isBlock)

dll.VBufStorage_addTagNodeToBuffer.errcheck=dllErrorCheck

def VBufStorage_addTextNodeToBuffer(parent, previous, docHandle, ID,text):
	return dll.VBufStorage_addTextNodeToBuffer(parent,previous,docHandle,ID,text)

dll.VBufStorage_addTextNodeToBuffer.errcheck=dllErrorCheck

VBufStorage_addTextNodeToBuffer.errcheck=dllErrorCheck

VBufStorage_removeNodeFromBuffer=dll.VBufStorage_removeNodeFromBuffer
VBufStorage_removeNodeFromBuffer.errcheck=dllErrorCheck

VBufStorage_removeDescendantsFromBufferNode=dll.VBufStorage_removeDescendantsFromBufferNode
VBufStorage_removeDescendantsFromBufferNode.errcheck=dllErrorCheck

def VBufStorage_getFieldIdentifierFromBufferOffset(buf,offset):
	docHandle=c_int()
	ID=c_int()
	dll.VBufStorage_getFieldIdentifierFromBufferOffset(buf,offset,byref(docHandle),byref(ID))
	return docHandle.value,ID.value

dll.VBufStorage_getFieldIdentifierFromBufferOffset.errcheck=dllErrorCheck

def VBufStorage_getBufferOffsetsFromFieldIdentifier(buf, docHandle, ID):
	start=c_int()
	end=c_int()
	dll.VBufStorage_getBufferOffsetsFromFieldIdentifier(buf,docHandle,ID,byref(start),byref(end))
	return (start.value,end.value)

dll.VBufStorage_getBufferOffsetsFromFieldIdentifier.errcheck=dllErrorCheck

def VBufStorage_findBufferFieldIdentifierByProperties(buf,direction,startOffset,attribs):
	if direction=="next":
		direction=VBUF_FINDDIRECTION_NEXT
	elif direction=="previous":
		direction=VBUF_FINDDIRECTION_PREVIOUS
	else:
		raise ValueError("bad direction: %s"%unicode(direction))
	if not isinstance(attribs,dict) or len(attribs)==0:
		raiseValueError("attribs must be of type dict containing 1 or more entries")
	cAttribs=(multyValueAttribute_t*len(attribs))()
	for index,name in enumerate(attribs.keys()):
		cAttribs[index].name=name
		vals=(c_wchar_p*len(attribs[name]))()
		for valIndex,val in enumerate(attribs[name]):
			vals[valIndex]=unicode(val) if val is not None else None
		cAttribs[index].value=vals
		cAttribs[index].numValues=len(attribs[name])
	foundDocHandle=c_int()
	foundID=c_int()
	res=dll.VBufStorage_findBufferFieldIdentifierByProperties(buf,direction,startOffset,cAttribs,len(cAttribs),byref(foundDocHandle),byref(foundID))
	if res==VBUF_ERROR_NOTFOUND:
		return None
	elif res<0:
		raise RuntimeError("VBufStorage_findBufferFieldIdentifierByProperties returned code %d"%res)
	return foundDocHandle.value,foundID.value

VBufStorage_getBufferTextLength=dll.VBufStorage_getBufferTextLength

VBufStorage_getBufferFieldCount=dll.VBufStorage_getBufferFieldCount

VBufStorage_findBufferText=dll.VBufStorage_findBufferText
VBufStorage_findBufferText.errcheck=dllErrorCheck

def VBufStorage_getBufferTextByOffsets(buf,startOffset,endOffset):
	text=create_unicode_buffer((endOffset-startOffset)+1)
	dll.VBufStorage_getBufferTextByOffsets(buf,startOffset,endOffset,text)
	return text.value

dll.VBufStorage_getBufferTextByOffsets.errcheck=dllErrorCheck

def VBufStorage_getXMLContextAtBufferOffset(buf,offset):
	textLength=dll.VBufStorage_getXMLContextAtBufferOffset(buf,offset,None)
	textBuf=create_unicode_buffer(textLength)
	dll.VBufStorage_getXMLContextAtBufferOffset(buf,offset,textBuf)
	return textBuf.value

dll.VBufStorage_getXMLContextAtBufferOffset.errcheck=dllErrorCheck

def VBufStorage_getXMLBufferTextByOffsets(buf,startOffset,endOffset):
	if endOffset<=startOffset:
		return ""
	textLength=dll.VBufStorage_getXMLBufferTextByOffsets(buf,startOffset,endOffset,None)
	textBuf=create_unicode_buffer(textLength)
	dll.VBufStorage_getXMLBufferTextByOffsets(buf,startOffset,endOffset,textBuf)
	return textBuf.value

dll.VBufStorage_getXMLBufferTextByOffsets.errcheck=dllErrorCheck

def VBufStorage_getBufferLineOffsets(buf,offset,maxLineLength=0,useScreenLayout=True):
	startOffset=c_int()
	endOffset=c_int()
	cUseScreenLayout=1 if useScreenLayout else 0
	dll.VBufStorage_getBufferLineOffsets(buf,offset,maxLineLength,cUseScreenLayout,byref(startOffset),byref(endOffset))
	return (startOffset.value,endOffset.value)

dll.VBufStorage_getBufferLineOffsets.errcheck=dllErrorCheck


def VBufStorage_getBufferSelectionOffsets(buf):
	startOffset=c_int()
	endOffset=c_int()
	dll.VBufStorage_getBufferSelectionOffsets(buf,byref(startOffset),byref(endOffset))
	return (startOffset.value,endOffset.value)

dll.VBufStorage_getBufferSelectionOffsets.errcheck=dllErrorCheck

VBufStorage_setBufferSelectionOffsets=dll.VBufStorage_setBufferSelectionOffsets
VBufStorage_setBufferSelectionOffsets.errcheck=dllErrorCheck

