#include <windows.h>
#include <interfaces/nvdaController/nvdaController.h>

__declspec(dllexport) error_status_t(__stdcall *_nvdaController_getNVDAVersionString)(wchar_t**);
error_status_t __stdcall nvdaController_getNVDAVersionString(wchar_t** version) {
	return _nvdaController_getNVDAVersionString(version);
}

__declspec(dllexport) error_status_t(__stdcall *_nvdaController_speakText)(const wchar_t*);
error_status_t __stdcall nvdaController_speakText(const wchar_t* text) {
	return _nvdaController_speakText(text);
}

__declspec(dllexport) error_status_t(__stdcall *_nvdaController_cancelSpeech)();
error_status_t __stdcall nvdaController_cancelSpeech() {
	return _nvdaController_cancelSpeech();
}

__declspec(dllexport) error_status_t(__stdcall *_nvdaController_brailleMessage)(const wchar_t*);
error_status_t __stdcall nvdaController_brailleMessage(const wchar_t* text) {
	return _nvdaController_brailleMessage(text);
}

error_status_t __stdcall nvdaController_testIfRunning() {
	return 0;
}

__declspec(dllexport) error_status_t(__stdcall *_nvdaController_inputLangChangeNotify)(const long, const wchar_t*);
error_status_t __stdcall nvdaController_inputLangChangeNotify(const long hkl, const wchar_t* layoutString) {
	return _nvdaController_inputLangChangeNotify(hkl,layoutString);
}
