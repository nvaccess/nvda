/**
 * backends/mshtml/node.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <list>
 #include <cassert>
#include <windows.h>
#include <oleidl.h>
#include <mshtml.h>
#include <base/debug.h>
#include "mshtml.h"
#include "node.h"

using namespace std;

class CDispatchChangeSink : public IDispatch {
	private:
	ULONG refCount;

	public:
	MshtmlVBufStorage_controlFieldNode_t* storageNode;
	bool allowDelete;

	CDispatchChangeSink(MshtmlVBufStorage_controlFieldNode_t* storageNode) {
		this->refCount=1;
		this->allowDelete=true;
		assert(storageNode);
		this->storageNode=storageNode;
		incBackendLibRefCount();
	}

	~CDispatchChangeSink() {
		decBackendLibRefCount();
	}

	void CDispatchChangeSink::onChange() {
		DEBUG_MSG(L"Marking storage node as invalid");
		this->storageNode->backend->invalidateSubtree(this->storageNode);
		DEBUG_MSG(L"Done");
	}

	HRESULT STDMETHODCALLTYPE IUnknown::QueryInterface(REFIID riid, void** pvpObject) {
		if(!pvpObject) return E_INVALIDARG;
		*pvpObject=NULL;
		if(riid==__uuidof(IDispatch)) {
			*pvpObject=static_cast<IDispatch*>(this);
		} else if(riid==__uuidof(IUnknown)) {
			*pvpObject=static_cast<IUnknown*>(this);
		} else {
			return E_NOINTERFACE;
		}
		this->AddRef();
		return S_OK;
	}

	ULONG STDMETHODCALLTYPE IUnknown::AddRef() {
		this->refCount++;
		return this->refCount;
	}

	ULONG STDMETHODCALLTYPE IUnknown::Release() {
		if(this->refCount>0)
			this->refCount--;
		if(this->refCount==0) {
			if (this->allowDelete) {
				delete this;
			} else {
				#ifdef DEBUG
				Beep(660,50);
				#endif
				DEBUG_MSG(L"refCount hit 0 before it should, not deleting, node info: " << this->storageNode->getDebugInfo());
			}
			return 0;
		}
		return this->refCount;
	}

	HRESULT STDMETHODCALLTYPE IDispatch::Invoke(DISPID  dispIdMember, REFIID  riid, LCID  lcid, WORD  wFlags, DISPPARAMS FAR*  pDispParams, VARIANT FAR*  pVarResult, EXCEPINFO FAR*  pExcepInfo, unsigned int FAR*  puArgErr) {
		if(dispIdMember==0) {
			DEBUG_MSG(L"calling onChange");
			this->onChange();
			DEBUG_MSG(L"Done, returning S_OK");
			return S_OK;
		}
		DEBUG_MSG(L"invoke called with unknown member ID, returning E_INVALIDARG");
		return E_INVALIDARG;
	}

	HRESULT STDMETHODCALLTYPE  IDispatch::GetTypeInfoCount(UINT* count) {
		*count=0;
		return S_OK;
	}

	HRESULT STDMETHODCALLTYPE IDispatch::GetTypeInfo(UINT index,LCID lcid,ITypeInfo** ppTypeInfo) {
		return E_NOTIMPL;
	}

	HRESULT STDMETHODCALLTYPE IDispatch::GetIDsOfNames(const IID& riid, LPOLESTR* name,UINT x, LCID lcid, DISPID* dispID) {
		return E_NOTIMPL;
	}

};

class CHTMLChangeSink : public IHTMLChangeSink {
	private:
	ULONG refCount;
	MshtmlVBufStorage_controlFieldNode_t* storageNode;
	IMarkupPointer* pMarkupPointerBegin;
	IMarkupPointer* pMarkupPointerEnd;

	public:

	CHTMLChangeSink(MshtmlVBufStorage_controlFieldNode_t* storageNode) {
		int res;
		this->refCount=1;
		assert(storageNode);
		this->storageNode=storageNode;
		this->pMarkupPointerBegin=NULL;
		this->pMarkupPointerEnd=NULL;
		IMarkupServices2* pMarkupServices2=NULL;
		res=storageNode->pMarkupContainer2->QueryInterface(IID_IMarkupServices2,(void**)&pMarkupServices2);
		if(res==S_OK) {
			pMarkupServices2->CreateMarkupPointer(&(this->pMarkupPointerBegin));
			pMarkupServices2->CreateMarkupPointer(&(this->pMarkupPointerEnd));
			pMarkupServices2->Release();
		}
		incBackendLibRefCount();
	}

	~CHTMLChangeSink() {
		if(this->pMarkupPointerBegin) {
			this->pMarkupPointerBegin->Release();
		}
		if(this->pMarkupPointerEnd) {
			this->pMarkupPointerEnd->Release();
		}
		decBackendLibRefCount();
	}

	HRESULT STDMETHODCALLTYPE IUnknown::QueryInterface(REFIID riid, void** pvpObject) {
		if(!pvpObject) return E_INVALIDARG;
		*pvpObject=NULL;
		if(riid==__uuidof(IHTMLChangeSink)) {
			*pvpObject=static_cast<IHTMLChangeSink*>(this);
		} else if(riid==__uuidof(IUnknown)) {
			*pvpObject=static_cast<IUnknown*>(this);
		} else {
			return E_NOINTERFACE;
		}
		this->AddRef();
		return S_OK;
	}

	ULONG STDMETHODCALLTYPE IUnknown::AddRef() {
		this->refCount++;
		return this->refCount;
	}

	ULONG STDMETHODCALLTYPE IUnknown::Release() {
		assert(this->refCount>0);
		this->refCount--;
		if(this->refCount==0) {
			delete this;
			return 0;
		}
		return this->refCount;
	}

	HRESULT STDMETHODCALLTYPE IHTMLChangeSink::Notify() {
		DEBUG_MSG(L"notify called for dirty range");
		if(this->storageNode->HTMLChangeSinkCookey==0) {
			DEBUG_MSG(L"Cookey not set yet!");
			return E_FAIL;
		}
		if(this->storageNode->pMarkupContainer2->GetAndClearDirtyRange(this->storageNode->HTMLChangeSinkCookey,this->pMarkupPointerBegin,this->pMarkupPointerEnd)!=S_OK) {
			DEBUG_MSG(L"Could not get and clear dirty range on IMarkupContainer2");
			return E_FAIL;
		}
		IHTMLElement* pHTMLElement=NULL;
		this->pMarkupPointerBegin->CurrentScope(&pHTMLElement);
		VBufStorage_controlFieldNode_t* beginningNode=this->storageNode->backend->getDeepestControlFieldNodeForHTMLElement(pHTMLElement);
		if(pHTMLElement) {
			pHTMLElement->Release();
			pHTMLElement=NULL;
		}
		this->pMarkupPointerEnd->CurrentScope(&pHTMLElement);
		VBufStorage_controlFieldNode_t* endNode=this->storageNode->backend->getDeepestControlFieldNodeForHTMLElement(pHTMLElement);
		if(pHTMLElement) pHTMLElement->Release();
		VBufStorage_controlFieldNode_t* invalidNode=NULL;
		if((beginningNode==endNode)||(beginningNode&&!endNode)) {
			invalidNode=beginningNode;
		} else if(endNode&&!beginningNode) {
			invalidNode=endNode;
		} else if(beginningNode&&endNode) {
			list<VBufStorage_controlFieldNode_t*> beginningAncestors;
			while(beginningNode) {
				beginningAncestors.push_front(beginningNode);
				beginningNode=beginningNode->getParent();
			}
			list<VBufStorage_controlFieldNode_t*> endAncestors;
			while(endNode) {
				endAncestors.push_front(endNode);
				endNode=endNode->getParent();
			}
			list<VBufStorage_controlFieldNode_t*>::iterator i=beginningAncestors.begin();
			list<VBufStorage_controlFieldNode_t*>::iterator j=endAncestors.begin();
			for(;i!=beginningAncestors.end()&&j!=endAncestors.end();i++,j++) {
				if(*i==*j) {
					invalidNode=*i;
					break;
				}
			}
			assert(invalidNode);
		}
		if(invalidNode) {
			this->storageNode->backend->invalidateSubtree(invalidNode);
		}
		DEBUG_MSG(L"notify done, returning S_OK");
		return S_OK;
	}

};

MshtmlVBufStorage_controlFieldNode_t::MshtmlVBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlock, MshtmlVBufBackend_t* backend, IHTMLDOMNode* pHTMLDOMNode): VBufStorage_controlFieldNode_t(docHandle,ID,isBlock) {
	int res;
	VARIANT_BOOL varBool;
	assert(backend);
	assert(pHTMLDOMNode);
	this->backend=backend;
	this->pHTMLElement2=NULL;
	this->propChangeSink=NULL;
	this->loadSink=NULL;
	this->pHTMLChangeSink=NULL;
	this->HTMLChangeSinkCookey=0;
	pHTMLDOMNode->QueryInterface(IID_IHTMLElement2,(void**)&(this->pHTMLElement2));
	if(!this->pHTMLElement2) {
		DEBUG_MSG(L"Could not queryInterface from IHTMLDOMNode to IHTMLElement2");
	}
	if(this->pHTMLElement2) {
		CDispatchChangeSink* propChangeSink=new CDispatchChangeSink(this);
		if((pHTMLElement2->attachEvent(L"onpropertychange",propChangeSink,&varBool)==S_OK)&&varBool) {
			this->propChangeSink=propChangeSink;
			// It seems that IE 6 sometimes calls Release() once too many times.
			// We don't want propChangeSink to be deleted until we're finished with it.
			propChangeSink->allowDelete=false;
		} else {
			DEBUG_MSG(L"Error attaching onPropertyChange event sink to IHTMLElement2 at "<<pHTMLElement2);
			propChangeSink->Release();
		}
	}
	BSTR nodeName=NULL;
	pHTMLDOMNode->get_nodeName(&nodeName);
	if(nodeName!=NULL&&(wcsicmp(nodeName,L"frame")==0||wcsicmp(nodeName,L"iframe")==0||wcsicmp(nodeName,L"img")==0||wcsicmp(nodeName,L"input")==0)) {
		if(this->pHTMLElement2) {
			CDispatchChangeSink* loadSink=new CDispatchChangeSink(this);
			if((pHTMLElement2->attachEvent(L"onload",loadSink,&varBool)==S_OK)&&varBool) {
				this->loadSink=loadSink;
			} else {
				DEBUG_MSG(L"Error attaching onload event sink to IHTMLElement2 at "<<pHTMLElement2);
				loadSink->Release();
			}
		}
	}
	if(nodeName!=NULL&&(wcsicmp(nodeName,L"body")==0||wcsicmp(nodeName,L"frameset")==0)) {
		IHTMLDOMNode2* pHTMLDOMNode2=NULL;
		pHTMLDOMNode->QueryInterface(IID_IHTMLDOMNode2,(void**)&pHTMLDOMNode2);
		if(pHTMLDOMNode2) {
			IDispatch* pDispDoc=NULL;
			pHTMLDOMNode2->get_ownerDocument(&pDispDoc);
			pHTMLDOMNode2->Release();
			if(pDispDoc) {
				pDispDoc->QueryInterface(IID_IMarkupContainer2,(void**)&(this->pMarkupContainer2)); 
				pDispDoc->Release();
				if(this->pMarkupContainer2) {
					this->pHTMLChangeSink=new CHTMLChangeSink(this);
					if(pMarkupContainer2->RegisterForDirtyRange(this->pHTMLChangeSink,&(this->HTMLChangeSinkCookey))!=S_OK) {
						DEBUG_MSG(L"Could not register dirty range notifications on IMarkupContainer2");
						this->pMarkupContainer2->Release();
						this->pMarkupContainer2=NULL;
						this->pHTMLChangeSink->Release();
						this->pHTMLChangeSink=NULL;
					}
				} else {
					DEBUG_MSG(L"Could not queryInterface from IDispatch to IMarkupContainer2");
				}
			} else {
				DEBUG_MSG(L"Could not get document of IHTMLDOMNode2");
			}
		} else {
			DEBUG_MSG(L"Could not queryInterface from IHTMLDOMNode to IHTMLDOMNode2");
		}
	}
	if(nodeName!=NULL) {
		SysFreeString(nodeName);
	}
}
 
MshtmlVBufStorage_controlFieldNode_t::~MshtmlVBufStorage_controlFieldNode_t() {
	if(this->propChangeSink) {
		assert(this->pHTMLElement2);
		if(pHTMLElement2->detachEvent(L"onpropertychange",this->propChangeSink)!=S_OK) {
			DEBUG_MSG(L"Error detaching onpropertychange event sink from IHTMLElement2");
		}
		static_cast<CDispatchChangeSink*>(this->propChangeSink)->allowDelete=true;
		this->propChangeSink->Release();
	}
	if(this->loadSink) {
		assert(this->pHTMLElement2);
		if(pHTMLElement2->detachEvent(L"onload",this->loadSink)!=S_OK) {
			DEBUG_MSG(L"Error detaching onload event sink from IHTMLElement2");
		}
		this->loadSink->Release();
	}
	if(this->pHTMLElement2) {
		this->pHTMLElement2->Release();
	}
	if(this->pHTMLChangeSink) {
		assert(this->pMarkupContainer2);
		if(this->pMarkupContainer2->UnRegisterForDirtyRange(this->HTMLChangeSinkCookey)!=S_OK) {
			DEBUG_MSG(L"Error unregistering for dirty range notifications on IMarkupContainer2");
		}
		this->pMarkupContainer2->Release();
		this->pHTMLChangeSink->Release();
	}
}
