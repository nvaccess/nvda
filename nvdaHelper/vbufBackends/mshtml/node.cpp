/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2020 NV Access Limited, Google LLC, Leonard de Ruijter
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <list>
#include <windows.h>
#include <objbase.h>
#include <oleidl.h>
#include <mshtml.h>
#include <mshtmdid.h>
#include <common/log.h>
#include "mshtml.h"
#include <remote/nvdaControllerInternal.h>
#include <common/xml.h>
#include "node.h"

using namespace std;

class CDispatchChangeSink : public IDispatch {
	private:
	ULONG refCount;
	MshtmlVBufStorage_controlFieldNode_t* storageNode;
	IConnectionPoint* pConnectionPoint;
	DWORD dwCookie;

	public:

	CDispatchChangeSink(MshtmlVBufStorage_controlFieldNode_t* storageNode) :
	refCount(1), dwCookie(0), pConnectionPoint(NULL) {
		nhAssert(storageNode);
		this->storageNode=storageNode;
		incBackendLibRefCount();
	}

	BOOL connect(IHTMLDOMNode* pHTMLDOMNode, REFIID iid) {
		if(dwCookie) {
			LOG_DEBUGWARNING(L"Already connected");
			return false;
		}
		IHTMLElement* pHTMLElement=NULL;
		pHTMLDOMNode->QueryInterface(IID_IHTMLElement,(void**)&pHTMLElement);
		if(!pHTMLElement) {
			LOG_DEBUGWARNING(L"QueryInterface to IHTMLElement failed");
			return false;
		}
		IConnectionPointContainer* pConnectionPointContainer=NULL;
		pHTMLElement->QueryInterface(IID_IConnectionPointContainer,(void**)&pConnectionPointContainer);
		pHTMLElement->Release();
		if(!pConnectionPointContainer) {
			LOG_DEBUGWARNING(L"QueryInterface to IConnectionPointContainer failed");
			return false;
		}
		IConnectionPoint* pConnectionPoint=NULL;
		pConnectionPointContainer->FindConnectionPoint(iid,&pConnectionPoint);
		pConnectionPointContainer->Release();
		if(!pConnectionPoint) {
			return false;
		}
		DWORD dwCookie=0;
		pConnectionPoint->Advise(this,&dwCookie);
		if(!dwCookie) {
			pConnectionPoint->Release();
			return false;
		}
		this->pConnectionPoint=pConnectionPoint;
		this->dwCookie=dwCookie;
		return true;
	}

	BOOL disconnect() {
		if(this->dwCookie==0) return false;
		this->pConnectionPoint->Unadvise(this->dwCookie);
		this->dwCookie=0;
		this->pConnectionPoint->Release();
		this->pConnectionPoint=NULL;
		return true;
	}

	~CDispatchChangeSink() {
		this->disconnect();
		decBackendLibRefCount();
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
		++(this->refCount);
		return this->refCount;
	}

	ULONG STDMETHODCALLTYPE IUnknown::Release() {
		if(this->refCount>0)
			this->refCount--;
		if(this->refCount==0) {
			delete this;
			return 0;
		}
		return this->refCount;
	}

	HRESULT STDMETHODCALLTYPE IDispatch::Invoke(DISPID  dispIdMember, REFIID  riid, LCID  lcid, WORD  wFlags, DISPPARAMS FAR*  pDispParams, VARIANT FAR*  pVarResult, EXCEPINFO FAR*  pExcepInfo, unsigned int FAR*  puArgErr) {
		if(dispIdMember==DISPID_EVMETH_ONPROPERTYCHANGE||dispIdMember==DISPID_EVMETH_ONLOAD) {
			this->storageNode->backend->invalidateSubtree(this->storageNode);
			// Force the update to happen with no delay if we happen to be in a live region
			if (
				this->storageNode->ariaLiveNode
				&& this->storageNode->ariaLiveNode != this->storageNode
				&& !this->storageNode->ariaLiveIsBusy
				&& (
					this->storageNode->ariaLiveIsTextRelevant
					|| this->storageNode->ariaLiveIsAdditionsRelevant
				)
			) {
				this->storageNode->backend->forceUpdate();
			}
			return S_OK;
		} else if(dispIdMember==DISPID_EVMETH_ONFOCUS) {
			this->storageNode->backend->forceUpdate();
			return S_OK;
		}
		return E_FAIL;
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
		nhAssert(storageNode);
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
		++(this->refCount);
		return this->refCount;
	}

	ULONG STDMETHODCALLTYPE IUnknown::Release() {
		nhAssert(this->refCount>0);
		this->refCount--;
		if(this->refCount==0) {
			delete this;
			return 0;
		}
		return this->refCount;
	}

	HRESULT STDMETHODCALLTYPE IHTMLChangeSink::Notify() {
		LOG_DEBUG(L"notify called for dirty range");
		if(this->storageNode->HTMLChangeSinkCookey==0) {
			LOG_DEBUG(L"Cookey not set yet!");
			return E_FAIL;
		}
		if(this->storageNode->pMarkupContainer2->GetAndClearDirtyRange(this->storageNode->HTMLChangeSinkCookey,this->pMarkupPointerBegin,this->pMarkupPointerEnd)!=S_OK) {
			LOG_DEBUG(L"Could not get and clear dirty range on IMarkupContainer2");
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
			for(;i!=beginningAncestors.end()&&j!=endAncestors.end();++i,++j) {
				if(*i==*j) {
					invalidNode=*i;
				} else {
					break;
				}
			}
			nhAssert(invalidNode);
		}
		if(invalidNode) {
			this->storageNode->backend->invalidateSubtree(invalidNode);
			MshtmlVBufStorage_controlFieldNode_t* invalidMshtmlNode=(MshtmlVBufStorage_controlFieldNode_t*)invalidNode;
			// Force the update to happen with no delay if we happen to be in a live region
			if (
				invalidMshtmlNode->ariaLiveNode
				&& invalidMshtmlNode->ariaLiveNode != invalidMshtmlNode
				&& !invalidMshtmlNode->ariaLiveIsBusy
				&& (
					invalidMshtmlNode->ariaLiveIsTextRelevant
					|| invalidMshtmlNode->ariaLiveIsAdditionsRelevant
				)
			) {
				this->storageNode->backend->forceUpdate();
			}
		}
		LOG_DEBUG(L"notify done, returning S_OK");
		return S_OK;
	}

};

MshtmlVBufStorage_controlFieldNode_t::MshtmlVBufStorage_controlFieldNode_t(
	int docHandle,
	int ID,
	bool isBlock,
	MshtmlVBufBackend_t* backend,
	bool isRootNode,
	IHTMLDOMNode*
	pHTMLDOMNode,
	const wstring& lang
)
	: VBufStorage_controlFieldNode_t(docHandle, ID, isBlock)
	, backend(backend)
	, language(lang)
	, isRootNode(isRootNode)
{
	nhAssert(backend);
	nhAssert(pHTMLDOMNode);

	pHTMLDOMNode->AddRef();
	this->pHTMLDOMNode=pHTMLDOMNode;

	BSTR nodeName=NULL;
	pHTMLDOMNode->get_nodeName(&nodeName);
	CDispatchChangeSink* propChangeSink=new CDispatchChangeSink(this);
	if(propChangeSink->connect(pHTMLDOMNode,IID_IDispatch)) {
		this->propChangeSink=propChangeSink;
	} else {
		propChangeSink->Release();
	}
	if(this->isRootNode||(nodeName!=NULL&&(_wcsicmp(nodeName,L"body")==0||_wcsicmp(nodeName,L"frameset")==0))) {
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
						LOG_DEBUG(L"Could not register dirty range notifications on IMarkupContainer2");
						this->pMarkupContainer2->Release();
						this->pMarkupContainer2=NULL;
						this->pHTMLChangeSink->Release();
						this->pHTMLChangeSink=NULL;
					}
				} else {
					LOG_DEBUG(L"Could not queryInterface from IDispatch to IMarkupContainer2");
				}
			} else {
				LOG_DEBUG(L"Could not get document of IHTMLDOMNode2");
			}
		} else {
			LOG_DEBUG(L"Could not queryInterface from IHTMLDOMNode to IHTMLDOMNode2");
		}
	}
	if(nodeName!=NULL) {
		SysFreeString(nodeName);
	}
}
 
MshtmlVBufStorage_controlFieldNode_t::~MshtmlVBufStorage_controlFieldNode_t() {
	if(this->propChangeSink) {
		if(!(static_cast<CDispatchChangeSink*>(this->propChangeSink)->disconnect())) {
			LOG_DEBUGWARNING(L"Failed to stop listening with HTMLElementEvents2 for node "<<this->getDebugInfo());
		}
		this->propChangeSink->Release();
		this->propChangeSink=NULL;
	}
	if(this->pHTMLDOMNode) {
		this->pHTMLDOMNode->Release();
		this->pHTMLDOMNode=NULL;
	}
	if(this->pHTMLChangeSink) {
		nhAssert(this->pMarkupContainer2);
		if(this->pMarkupContainer2->UnRegisterForDirtyRange(this->HTMLChangeSinkCookey)!=S_OK) {
			LOG_DEBUG(L"Error unregistering for dirty range notifications on IMarkupContainer2");
		}
		this->pMarkupContainer2->Release();
		this->pHTMLChangeSink->Release();
	}
}

void MshtmlVBufStorage_controlFieldNode_t::preProcessLiveRegion(const MshtmlVBufStorage_controlFieldNode_t* parent, const std::map<std::wstring,std::wstring>& attribsMap) {
	auto i=attribsMap.find(L"HTMLAttrib::aria-live");
	if(i!=attribsMap.end()&&!i->second.empty()) {
		bool isAriaLiveEnabled = i->second == L"polite" || i->second == L"assertive";
		this->ariaLiveNode = isAriaLiveEnabled ? this : nullptr;
		this->ariaLivePoliteness = i->second;
	} else {
		this->ariaLiveNode = parent? parent->ariaLiveNode : nullptr;
		if (this->ariaLiveNode) {
			this->ariaLivePoliteness = this->ariaLiveNode->ariaLivePoliteness;
		} else {
			this->ariaLivePoliteness = L"";
		}
	}
	i=attribsMap.find(L"HTMLAttrib::aria-relevant");
	if(i!=attribsMap.end()&&!i->second.empty()) {
		if(i->second.compare(L"all")==0) {
			this->ariaLiveIsTextRelevant=true;
			this->ariaLiveIsAdditionsRelevant=true;
		} else {
			this->ariaLiveIsTextRelevant=i->second.find(L"text")!=wstring::npos;
			this->ariaLiveIsAdditionsRelevant=i->second.find(L"additions")!=wstring::npos;
		}
	} else {
		this->ariaLiveIsTextRelevant=parent?parent->ariaLiveIsTextRelevant:true;
		this->ariaLiveIsAdditionsRelevant=parent?parent->ariaLiveIsAdditionsRelevant:true;
	}
	i=attribsMap.find(L"HTMLAttrib::aria-busy");
	if(i!=attribsMap.end()&&!i->second.empty()) {
		this->ariaLiveIsBusy=i->second.compare(L"true")==0;
	} else {
		this->ariaLiveIsBusy=parent?parent->ariaLiveIsBusy:false;
	}
	i=attribsMap.find(L"HTMLAttrib::aria-atomic");
	if(i!=attribsMap.end()&&!i->second.empty()) {
		this->ariaLiveAtomicNode=(i->second.compare(L"true")==0)?this:NULL;
	} else {
		this->ariaLiveAtomicNode=parent?parent->ariaLiveAtomicNode:NULL;
	}
	LOG_DEBUG(L"preProcessLiveRegion: ariaLiveNode "<<ariaLiveNode<<L", ariaLiveIsTextRelevant "<<ariaLiveIsTextRelevant<<L", ariaLiveIsAdditionsRelevant "<<ariaLiveIsAdditionsRelevant<<L", ariaLiveIsBusy "<<ariaLiveIsBusy<<L", ariaLiveAtomicNode "<<ariaLiveAtomicNode);
}

void MshtmlVBufStorage_controlFieldNode_t::reportLiveText(wstring& text, wstring& politeness) {
	if(!all_of(text.cbegin(), text.cend(), iswspace)) {
		nvdaControllerInternal_reportLiveRegion(text.c_str(), politeness.c_str());
	}
}

bool isNodeInLiveRegion(VBufStorage_fieldNode_t* node) {
	if(!node) return false;
	if(node->getFirstChild()) {
		return ((MshtmlVBufStorage_controlFieldNode_t*)node)->ariaLiveNode != nullptr;
	}
	return true;
}

void MshtmlVBufStorage_controlFieldNode_t::reportLiveAddition() {
	wstring text; //=(this->ariaLiveAtomicNode==this)?L"atomic: ":L"additions: ";
	this->getTextInRange(0,this->getLength(),text,false,isNodeInLiveRegion);
	this->reportLiveText(text, this->ariaLivePoliteness);
}

void MshtmlVBufStorage_controlFieldNode_t::postProcessLiveRegion(VBufStorage_controlFieldNode_t* oldNode, set<VBufStorage_controlFieldNode_t*>& atomicNodes) {
	LOG_DEBUG(L"postProcessLiveRegion: ariaLiveNode "<<ariaLiveNode<<L", ariaLiveIsTextRelevant "<<ariaLiveIsTextRelevant<<L", ariaLiveIsAdditionsRelevant "<<ariaLiveIsAdditionsRelevant<<L", ariaLiveIsBusy "<<ariaLiveIsBusy<<L", ariaLiveAtomicNode "<<ariaLiveAtomicNode);
	if (!this->ariaLiveNode || this->ariaLiveIsBusy) {
		return;
	}
	bool reportNode=!oldNode && this->ariaLiveIsAdditionsRelevant && this->ariaLiveNode != this;
	wstring newChildrenText;
	if(!reportNode&&oldNode&&ariaLiveIsTextRelevant) {
		// Find the first new text child
		VBufStorage_fieldNode_t* newStart=this->getFirstChild();
		VBufStorage_fieldNode_t* oldStart=oldNode->getFirstChild();
		while(newStart&&oldStart) {
			if(newStart->getLength()==0||newStart->getFirstChild()) {
				newStart=newStart->getNext();
				continue;
			}
			if(oldStart->getLength()==0||oldStart->getFirstChild()) {
				oldStart=oldStart->getNext();
				continue;
			}
			if(((VBufStorage_textFieldNode_t*)oldStart)->text.compare(((VBufStorage_textFieldNode_t*)newStart)->text)!=0) {
				break;
			}
			oldStart=oldStart->getNext();
			newStart=newStart->getNext();
		}
		// Find the last new text child
		VBufStorage_fieldNode_t* newEnd=this->getLastChild();
		VBufStorage_fieldNode_t* oldEnd=oldNode->getLastChild();
		while(newEnd&&oldEnd) {
			if(newEnd->getLength()==0||newEnd->getLastChild()) {
				newEnd=newEnd->getPrevious();
				continue;
			}
			if(oldEnd->getLength()==0||oldEnd->getLastChild()) {
				oldEnd=oldEnd->getPrevious();
				continue;
			}
			if(((VBufStorage_textFieldNode_t*)oldEnd)->text.compare(((VBufStorage_textFieldNode_t*)newEnd)->text)!=0) {
				break;
			}
			oldEnd=oldEnd->getPrevious();
			newEnd=newEnd->getPrevious();
		}
		// Collect all the text between the first and last new text children.
		while(newStart) {
			if(newStart->getLength()>0&&!newStart->getFirstChild()) {
				newStart->getTextInRange(0,newStart->getLength(),newChildrenText,false);
			}
			if(newStart==newEnd) break;
			newStart=newStart->getNext();
		}
	}
	if(!reportNode&&newChildrenText.empty()) return;
	if(this->ariaLiveAtomicNode) {
		atomicNodes.insert(this->ariaLiveAtomicNode);
		newChildrenText=L"";
		reportNode=false;
	} else if(reportNode) {
		this->reportLiveAddition();
	} else if(!newChildrenText.empty()) {
		this->reportLiveText(newChildrenText, this->ariaLivePoliteness);
	}
}

void MshtmlVBufStorage_controlFieldNode_t::generateAttributesForMarkupOpeningTag(wstring& text, int startOffset, int endOffset) {
	VBufStorage_controlFieldNode_t::generateAttributesForMarkupOpeningTag(text, startOffset, endOffset);
	text += L"language=\"";
	for (wstring::const_iterator it = language.begin(); it != language.end(); ++it)
		appendCharToXML(*it, text, true);
	text += L"\" ";
}
