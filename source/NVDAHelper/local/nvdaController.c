#include <windows.h>
#include <interfaces/nvdaController/nvdaController.h>

__declspec(dllexport) RPC_STATUS(*_nvdaController_getNVDAVersionString)(handle_t,wchar_t**);
boolean nvdaController_getNVDAVersionString(handle_t bindingHandle, wchar_t** version) {
	return _nvdaController_getNVDAVersionString(bindingHandle,version);
}

__declspec(dllexport) RPC_STATUS(*_nvdaController_speakText)(handle_t,const wchar_t*);
boolean nvdaController_speakText(handle_t bindingHandle, const wchar_t* text) {
	return _nvdaController_speakText(bindingHandle,text);
}
