#include <windows.h>
#include <interfaces/nvdaController/nvdaController.h>

__declspec(dllexport) error_status_t(*_nvdaController_getNVDAVersionString)(wchar_t**);
error_status_t nvdaController_getNVDAVersionString(wchar_t** version) {
	return _nvdaController_getNVDAVersionString(version);
}

__declspec(dllexport) error_status_t(*_nvdaController_speakText)(const wchar_t*);
error_status_t nvdaController_speakText(const wchar_t* text) {
	return _nvdaController_speakText(text);
}

__declspec(dllexport) error_status_t(*_nvdaController_cancelSpeech)();
error_status_t nvdaController_cancelSpeech() {
	return _nvdaController_cancelSpeech();
}

__declspec(dllexport) error_status_t(*_nvdaController_brailleMessage)(const wchar_t*);
error_status_t nvdaController_brailleMessage(const wchar_t* text) {
	return _nvdaController_brailleMessage(text);
}

error_status_t nvdaController_testIfRunning() {
	return 0;
}
