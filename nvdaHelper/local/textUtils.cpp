#include <windows.h>
#include <usp10.h>

bool calculateWordOffsets(wchar_t* text, int textLength, int offset, int* startOffset, int* endOffset) {
	if(textLength<=0) return false;
	if(offset<0) return false;
	if(offset>=textLength) {
		*startOffset=offset;
		*endOffset=offset+1;
		return true;
	}
	SCRIPT_ITEM* pItems=new SCRIPT_ITEM[textLength+1];
	int numItems=0;
	if(ScriptItemize(text,textLength,textLength,NULL,NULL,pItems,&numItems)!=S_OK||numItems==0) {
		delete[] pItems;
		return false;
	}
	SCRIPT_LOGATTR* logAttrArray=new SCRIPT_LOGATTR[textLength];
	int nextICharPos=textLength;
	for(int itemIndex=numItems-1;itemIndex>=0;--itemIndex) {
		int iCharPos=pItems[itemIndex].iCharPos;
		int iCharLength=nextICharPos-iCharPos;
		if(ScriptBreak(text+iCharPos,iCharLength,&(pItems[itemIndex].a),logAttrArray+iCharPos)!=S_OK) {
			delete[] pItems;
			delete[] logAttrArray;
			return false;
		}
	}
	delete[] pItems;
	for(int i=offset;i>=0;--i) {
		if(logAttrArray[i].fWordStop) {
			*startOffset=i;
			break;
		}
	}
	*endOffset=textLength;
	for(int i=offset+1;i<textLength;++i) {
		if(logAttrArray[i].fWordStop) {
			*endOffset=i;
			break;
		}
	}
	delete[] logAttrArray;
	return true;
}

