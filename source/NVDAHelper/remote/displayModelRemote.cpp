#include <string>
#include <map>
#include "displayModelRemote.h"
#include "gdiHooks.h"

using namespace std;

error_status_t displayModelRemote_getWindowTextInRect(handle_t bindingHandle, const long windowHandle, const int left, const int top, const int right, const int bottom, BSTR* textBuf) {
	displayModelsByWindow_t::iterator i=displayModelsByWindow.find((HWND)windowHandle);
	if(i!=displayModelsByWindow.end()) {
		wstring text;
		RECT rect={left,top,right,bottom};
		i->second->renderText(&rect,text);
		*textBuf=SysAllocString(text.c_str());
	}
	return 0;
}
