
def findStartOfLine(text,offset,lineLength=None):
	if offset>=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	start=offset
	if isinstance(lineLength,int):
		return offset-(offset%lineLength)
	if text[start]=='\n' and start>=0 and text[start-1]=='\r':
		start-=1
	start=text.rfind('\n',0,offset)
	if start<0:
		start=text.rfind('\r',0,offset)
	if start<0:
		start=-1
	return start+1

def findEndOfLine(text,offset,lineLength=None):
	if offset>=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	if isinstance(lineLength,int):
		return (offset-(offset%lineLength)+lineLength)
	end=offset
	if text[end]!='\n':
		end=text.find('\n',offset)
	if end<0:
		if text[offset]!='\r':
			end=text.find('\r',offset)
	if end<0:
		end=len(text)-1
	return end+1

def findStartOfWord(text,offset,lineLength=None):
	if offset>=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	lineStart=findStartOfLine(text,offset,lineLength=lineLength)
	while offset>lineStart and text[offset].isspace():
		offset-=1
	if not text[offset].isalnum():
		return offset
	else:
		while offset>lineStart and text[offset-1].isalnum():
			offset-=1
	return offset

def findEndOfWord(text,offset,lineLength=None):
	if offset>=len(text):
		raise ValueError("Offset %d is too high for text of length %d"%(offset,len(text)))
	lineEnd=findEndOfLine(text,offset,lineLength=lineLength)
	if text[offset].isalnum():
		while offset<lineEnd and text[offset].isalnum():
			offset+=1
	elif not text[offset].isspace() and not text[offset].isalnum():
		offset+=1
	while offset<lineEnd and text[offset].isspace():
		offset+=1
	return offset
