#include <string>
#include <map>
#include "displayModelRemote.h"
#include "gdiHooks.h"

using namespace std;

error_status_t displayModelRemote_getTextInWindow(handle_t bindingHandle, const long windowHandle, wchar_t** textBuf) {
	map<HWND,displayModel_t*>::iterator i=displayModelsByWindow.find((HWND)windowHandle);
	if(i!=displayModelsByWindow.end()) {
		wstring text;
		i->second->renderText(text);
		*textBuf=_wcsdup(text.c_str());
	}
	return 0;
}
