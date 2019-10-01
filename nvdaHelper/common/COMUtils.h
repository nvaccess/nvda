#include <comdef.h>
#include <common/log.h>

namespace nvCOMUtils {

class InterfaceMarshaller {
	private:
	DWORD cookie {(DWORD)(-1)};
	IGlobalInterfaceTablePtr pGIT {nullptr};

	public:
	InterfaceMarshaller() {};

	template<typename t> HRESULT marshal(t* p) {
		if(cookie!=-1) {
			LOG_ERROR(L"An interface is already marshalled");
			return E_FAIL;
		}
		HRESULT res=pGIT.CreateInstance(CLSID_StdGlobalInterfaceTable);
		if(res!=S_OK) {
			LOG_ERROR(L"Could not create global interface table");
			return res;
		}
		res=pGIT->RegisterInterfaceInGlobal(p,__uuidof(t),&cookie);
		if(res!=S_OK) {
			LOG_ERROR(L"Could not register object in global interface table");
			return res;
		}
		return S_OK;
	}

	template<typename t> t* unmarshal() {
		if(cookie==-1) {
			LOG_ERROR(L"Nothing has been marshalled");
			return nullptr;
		}
		t* p=nullptr;
		HRESULT res=pGIT->GetInterfaceFromGlobal(cookie,__uuidof(t),reinterpret_cast<void**>(&p));
		if(res!=S_OK) {
			LOG_ERROR(L"Could not unmarshal object, code "<<res);
			return nullptr;
		}
		return p;
	}

	~InterfaceMarshaller() {
		if(cookie!=-1) {
			pGIT->RevokeInterfaceFromGlobal(cookie);
		}
	}

};

};
