#ifndef NVDAHELPERREMOTE_MODULEENSURER
#define NVDAHELPERREMOTE_MODULEENSURER

#include <windows.h>

/**
 * Instanciate an object of this class on the stack with a module handle of a dll, and it will ensure that the dll is not unloaded at least until this object goes out of scope.
 * Very useful for API hook callbacks.
 */
class ModuleEnsurer {
	private:
	HINSTANCE _moduleHandle;

	public:

	inline ModuleEnsurer(HINSTANCE moduleHandle): _moduleHandle(0) {
		GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,(LPCTSTR)moduleHandle,&_moduleHandle);
		assert(moduleHandle==_moduleHandle);
	}

	inline ~ModuleEnsurer() {
		FreeLibrary(_moduleHandle);
	}

};

#endif
