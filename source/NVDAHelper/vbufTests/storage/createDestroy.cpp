#include <iostream>
#include <base/debug.h>
#include <base/storage.h>

using namespace std;

#define TESTSIZE 8
#define TESTSTRING L"test"

bool fillBuffer(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, int depth) {
	VBufStorage_controlFieldNode_t* controlNode=NULL;
	VBufStorage_textFieldNode_t* textNode=NULL;
	depth++;
	for(int i=0;i<depth;i++) {
		if(depth<TESTSIZE) {
			if((controlNode=buffer->addControlFieldNode(parentNode,controlNode,(int)parentNode,(int)controlNode,true))==NULL) {
				DEBUG_MSG(L"Error adding control node to buffer");
				return false;
			}
			controlNode->addAttribute(L"control name",L"test");
			if(!fillBuffer(buffer,controlNode,depth)) {
				DEBUG_MSG(L"Error in recursion");
				return false;
			}
		} else {
			if((textNode=buffer->addTextFieldNode(parentNode,textNode,TESTSTRING))==NULL) {
				DEBUG_MSG(L"Error adding text node to buffer");
				return false;
			}
			textNode->addAttribute(L"text name",L"test");
		}
	}
	return true;
}
 
int main(int argc, char* argv[]) {
	VBufStorage_buffer_t* buffer=new VBufStorage_buffer_t();
	if(buffer==NULL) {
		return 1;
	}
	if(fillBuffer(buffer,NULL,0)==0) {
		return 1;
	}
	delete buffer;
	return 0;
}
