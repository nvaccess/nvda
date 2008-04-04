from ctypes import *

VBUF_FINDDIRECTION_NEXT=1
VBUF_FINDDIRECTION_PREVIOUS=2

VBUF_ERROR_NOTFOUND=-7

class attributeValue_t(Structure):
	_fields_=[('value',c_wchar_p),('valueLength',c_int)]

class multyValueAttribute_t(Structure):
	_fields_=[('name',c_wchar_p),('nameLength',c_int),('values',POINTER(attributeValue_t)),('numValues',c_int)]

dll=cdll.virtualBuffer

def dllErrorCheck(res,func,args):
	if res<0 or (func==VBufClient_createBuffer and res==0):
		raise RuntimeError("error in %s with args of %s, code %s"%(func.__name__,args,res))

	return res

VBufClient_createBuffer=dll.VBufClient_createBuffer
VBufClient_createBuffer.errcheck=dllErrorCheck


VBufClient_destroyBuffer=dll.VBufClient_destroyBuffer
VBufClient_destroyBuffer.errcheck=dllErrorCheck

def VBufClient_getFieldIdentifierFromBufferOffset(buf,offset):
	docHandle=c_int()
	ID=c_int()
	dll.VBufClient_getFieldIdentifierFromBufferOffset(buf,offset,byref(docHandle),byref(ID))
	return docHandle.value,ID.value

dll.VBufClient_getFieldIdentifierFromBufferOffset.errcheck=dllErrorCheck

def VBufClient_getBufferOffsetsFromFieldIdentifier(buf, docHandle, ID):
	start=c_int()
	end=c_int()
	dll.VBufClient_getBufferOffsetsFromFieldIdentifier(buf,docHandle,ID,byref(start),byref(end))
	return (start.value,end.value)

dll.VBufClient_getBufferOffsetsFromFieldIdentifier.errcheck=dllErrorCheck

def VBufClient_findBufferFieldIdentifierByProperties(buf,direction,startOffset,attribs):
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
		cAttribs[index].nameLength=len(name)+1
		vals=(attributeValue_t*len(attribs[name]))()
		for valIndex,val in enumerate(attribs[name]):
			val=unicode(val) if val is not None else None
			vals[valIndex].value=val
			vals[valIndex].valueLength=len(val)+1 if isinstance(val,basestring) else 0
		cAttribs[index].values=vals
		cAttribs[index].numValues=len(attribs[name])
	foundDocHandle=c_int()
	foundID=c_int()
	res=dll.VBufClient_findBufferFieldIdentifierByProperties(buf,direction,startOffset,cAttribs,len(cAttribs),byref(foundDocHandle),byref(foundID))
	if res==VBUF_ERROR_NOTFOUND:
		return None
	elif res<0:
		raise RuntimeError("VBufClient_findBufferFieldIdentifierByProperties returned code %d"%res)
	return foundDocHandle.value,foundID.value

VBufClient_getBufferTextLength=dll.VBufClient_getBufferTextLength

VBufClient_getBufferFieldCount=dll.VBufClient_getBufferFieldCount

VBufClient_findBufferText=dll.VBufClient_findBufferText
VBufClient_findBufferText.errcheck=dllErrorCheck

def VBufClient_getBufferTextByOffsets(buf,startOffset,endOffset):
	text=create_unicode_buffer((endOffset-startOffset)+1)
	dll.VBufClient_getBufferTextByOffsets(buf,startOffset,endOffset,text)
	return text.value

dll.VBufClient_getBufferTextByOffsets.errcheck=dllErrorCheck

def VBufClient_getXMLContextAtBufferOffset(buf,offset):
	textLength=dll.VBufClient_getXMLContextAtBufferOffset(buf,offset,None,0)
	textBuf=create_unicode_buffer(textLength)
	dll.VBufClient_getXMLContextAtBufferOffset(buf,offset,textBuf,textLength)
	return textBuf.value

dll.VBufClient_getXMLContextAtBufferOffset.errcheck=dllErrorCheck

def VBufClient_getXMLBufferTextByOffsets(buf,startOffset,endOffset):
	if endOffset<=startOffset:
		return ""
	textLength=dll.VBufClient_getXMLBufferTextByOffsets(buf,startOffset,endOffset,None,0)
	textBuf=create_unicode_buffer(textLength)
	dll.VBufClient_getXMLBufferTextByOffsets(buf,startOffset,endOffset,textBuf,textLength)
	return textBuf.value

dll.VBufClient_getXMLBufferTextByOffsets.errcheck=dllErrorCheck

def VBufClient_getBufferLineOffsets(buf,offset,maxLineLength=0,useScreenLayout=True):
	startOffset=c_int()
	endOffset=c_int()
	cUseScreenLayout=1 if useScreenLayout else 0
	dll.VBufClient_getBufferLineOffsets(buf,offset,maxLineLength,cUseScreenLayout,byref(startOffset),byref(endOffset))
	return (startOffset.value,endOffset.value)

dll.VBufClient_getBufferLineOffsets.errcheck=dllErrorCheck


def VBufClient_getBufferSelectionOffsets(buf):
	startOffset=c_int()
	endOffset=c_int()
	dll.VBufClient_getBufferSelectionOffsets(buf,byref(startOffset),byref(endOffset))
	return (startOffset.value,endOffset.value)

dll.VBufClient_getBufferSelectionOffsets.errcheck=dllErrorCheck

VBufClient_setBufferSelectionOffsets=dll.VBufClient_setBufferSelectionOffsets
VBufClient_setBufferSelectionOffsets.errcheck=dllErrorCheck

