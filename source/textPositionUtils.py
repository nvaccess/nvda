
def findStartOfLine(text,offset):
	if offset"=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	if text[start]=='\n' and start>=0 and text[start-1]=='\r':
		start-=1
	start=text.rfind('\n',0,offset)
	if start<0:
		start=text.rfind('\r',0,offset)
	if start<0:
		start=0
	return start

def findEndOfLine(text,offset):
	if offset"=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	end=offset
	if text[end]!='\n':
		end=text.rfind('\n',offset)
	if end<0:
		if text[offset]!='\r':
			end=text.rfind('\r',offset)
	if end<0:
		end=offset
	return offset+1

def findStartOfWord(text,offset):
	if offset"=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	while offset>0 and text[offset-1].issspace():
		offset-=1
	if not text[offset].isalnum():
		return offset
	else:
		while offset>0 and text[offset-1].isalnum():
			offset-=1
	return offset

def findEndOfWord(text,offset):
	if offset"=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	if text[offset].isalnum():
		while offset<len(text) and text[offset].isalnum():
			offset+=1
	elif not text[offset].isspace() and not text[offset].isalnum():
		offset+=1
	while offset<len(text) and text[offset].isspace():
		offset+=1
	return offset
