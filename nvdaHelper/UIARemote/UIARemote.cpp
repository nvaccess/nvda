#include <functional>
#include <windows.h>
#include <atlsafe.h>
#include <atlcomcli.h>
#include <roapi.h>
#include <winstring.h>
#include <UIAutomation.h>
#include <UiaOperationAbstraction/UiaOperationAbstraction.h>
#include <UiaOperationAbstraction/SafeArrayUtil.h>
#include <common/log.h>
#include <winrt/microsoft.ui.uiautomation.h>

using namespace UiaOperationAbstraction;

wchar_t dllDirectory[MAX_PATH];

#define  localLog(logLevel,content) if(!UiaOperationAbstraction::ShouldUseRemoteApi()) {\
			LOG_##logLevel(content);\
		} 

const auto textContentCommand_elementStart=1;
const auto textContentCommand_text=2;
const auto textContentCommand_elementEnd=3;

template<typename ItemType> void _remoteable_clearUiaArray(UiaOperationScope& scope, UiaArray<ItemType>& array) {
	auto arrayCount=array.Size();
	UiaUint index=0;
	scope.For([&](){},[&]() {
		return index<arrayCount;
	},[&](){
		index+=1;
	},[&]() {
		array.RemoveAt(0);
	});
}

UiaArray<UiaTextRange> _remoteable_splitTextRangeByUnit(UiaOperationScope& scope, UiaTextRange& textRange, TextUnit unit) {
	UiaArray<UiaTextRange> ranges;
	// Start with a clone of textRange collapsed to the start
	auto tempRange=textRange.Clone();
	tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
	UiaInt endDelta=0;
	scope.While([&](){ return true; },[&](){
		// tempRange may already be at the end of textRange
		// If so, then break out of the loop.
		UiaInt startDelta = tempRange.CompareEndpoints(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
		scope.If(startDelta>=0,[&](){
			scope.Break();
		});
		// Expand to the enclosing unit
		auto oldTempRange=tempRange.Clone();
		tempRange.ExpandToEnclosingUnit(unit);
		// Ensure we have not expanded back before where we started.
		startDelta = tempRange.CompareEndpoints(TextPatternRangeEndpoint_Start,oldTempRange,TextPatternRangeEndpoint_Start);
		scope.If(startDelta<0,[&](){
			// Clip the range to keep it bounded to where we started.
			tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_Start,oldTempRange,TextPatternRangeEndpoint_Start);
		});
		//tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_Start,oldTempRange,TextPatternRangeEndpoint_Start);
		// Find out if we are past the end of the over all textRange yet
		endDelta = tempRange.CompareEndpoints(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
		scope.If(endDelta>0,[&](){
			// We moved past the end of the over all textRange,
			// Clip the tempRange so it stays inside
			tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
		});
		auto tempRangeWidth = tempRange.CompareEndpoints(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
		scope.If(tempRangeWidth>0,[&]() {
			// Save off this range
			ranges.Append(tempRange.Clone());
		});
		scope.If(endDelta>0,[&](){
			// Since we had to clip to the end of the over all textRange,
			// We should not go any further.
			scope.Break();
		});
		// collapse the tempRange up to the end, ready to go through the loop again
		tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
		auto moved=tempRange.Move(unit,1);
		scope.If(moved==0,[&](){
			// We could not move further. Break.
			scope.Break();
		});
	}); // loop end
	scope.If(endDelta<0,[&](){ 
		// For some reason we never reached the end of the over all textRange.
		// Move the end forward so we do.
		tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
		// Save off this final range.
		ranges.Append(tempRange.Clone());
	});
	return ranges;
}

UiaBool _remoteable_appendAttributesAndTextForRange(UiaOperationScope& scope,UiaTextRange& textRange,const std::vector<int>& attribIDs,UiaArray<UiaVariant>& outArray, UiaBool ignoreMixedAttributes) {
	UiaBool foundMixed=false;
	UiaArray<UiaVariant> attribValues;
	for(auto attribID: attribIDs) {
		scope.If(!foundMixed,[&]() {
			auto attribValue=textRange.GetAttributeValue(UiaTextAttributeId(attribID));
			scope.If(attribValue.IsMixedAttribute(),[&]() {
				attribValues.Append(UiaVariant(0));
				foundMixed=!ignoreMixedAttributes;
			},[&]() {
				scope.If(attribValue.IsNotSupported(),[&]() {
					attribValues.Append(UiaVariant(0));
				},[&]() {
					attribValues.Append(attribValue);
				});
			});
		});
	}
	scope.If(!foundMixed,[&]() {
		outArray.Append(UiaVariant(textContentCommand_text));
		scope.ForEach(attribValues,[&](auto attribValue) {
			outArray.Append(attribValue);
		});
		auto text=textRange.GetText(-1);
		outArray.Append(UiaVariant(text));
	});
	return foundMixed;
}

UiaBool _remoteable_compareUiaElements(UiaOperationScope& scope, UiaElement& element1, UiaElement& element2) {
		// compare the two elements using their runtime IDs.
		auto ID1=element1.GetRuntimeId();
		auto ID2=element2.GetRuntimeId();
		return ID1 == ID2;
}

UiaArray<UiaElement> _remoteable_getAncestorsForTextRange(UiaOperationScope& scope, UiaTextRange& textRange, UiaElement& rootElement) {
	UiaArray<UiaElement> ancestors;
	// Get the enclosing element for this textRange.
	auto parent=textRange.GetEnclosingElement();
	// Walk up the parent chain recording saving off each ancestor.
	// However stop once we reach the given root element.
	scope.While([&]() {
		return !parent.IsNull();
	},[&]() {
		localLog(INFO,L"ancestor: "<<(parent.GetName(false).get())<<L" "<<(parent.GetLocalizedControlType(false).get()));
		ancestors.Append(parent);
		scope.If(_remoteable_compareUiaElements(scope,parent,rootElement),[&]() {
			scope.Break();
		});
		parent=parent.GetParentElement();
	});
	return ancestors;
}

void _remoteable_calculateAncestorsExitedAndEntered(UiaOperationScope& scope, UiaArray<UiaElement>& oldAncestors, UiaArray<UiaElement>& newAncestors, UiaArray<UiaElement>& elementsExited, UiaArray<UiaElement>& elementsEntered) {
	auto oldCount=oldAncestors.Size();
	auto newCount=newAncestors.Size();
	UiaUint exitCount=0;
	exitCount+=oldCount;
	UiaUint index=0;
	// Walking backward through newAncestors (from parent to child),
	// save off all new ancestors that do not also appear in oldAncestors.
	// I.e. elements now entered.
	// also take note at which index in oldAncestors, new and old ancestors are the same.
	scope.For([&](){},[&]() {
		return index<newCount;
	},[&]() {
		index+=1;
	},[&]() {
		UiaUint newElementIndex=0;
		newElementIndex = newCount;
		newElementIndex -= index;
		newElementIndex -= 1;
		auto newElement=newAncestors.GetAt(newElementIndex);
		scope.If(index<oldCount,[&]() {
			UiaUint oldElementIndex=0;
			oldElementIndex = oldCount;
			oldElementIndex -= index;
			oldElementIndex -= 1;
			auto oldElement=oldAncestors.GetAt(oldElementIndex);
			scope.If(_remoteable_compareUiaElements(scope,newElement,oldElement),[&]() {
				exitCount=oldElementIndex;
			},[&]() {
				elementsEntered.Append(newElement);
			});
		},[&]() {
			elementsEntered.Append(newElement);
		});
	});
	UiaUint oldIndex=0;
	// For all old ancestors that don't appear in newAncestors,
	// Save them off as elements exited.
	scope.For([&](){},[&]() {
		return oldIndex<exitCount;
	},[&]() {
		oldIndex+=1;
	},[&]() {
		auto oldElement=oldAncestors.GetAt(oldIndex);
		elementsExited.Append(oldElement);
	});
}

void _remoteable_appendElementStartInfo(UiaOperationScope& scope, UiaElement& element, UiaOperationAbstraction::UiaCacheRequest& cacheRequest, UiaArray<UiaVariant>& outArray) {
	// Record an elementStart command
	outArray.Append(UiaVariant(textContentCommand_elementStart));
	outArray.Append(UiaVariant(element.GetUpdatedCacheElement(cacheRequest)));
}

void _remoteable_appendElementEndInfo(UiaOperationScope& scope, UiaElement& element, UiaArray<UiaVariant>& outArray) {
	// record an elementEnd command
	outArray.Append(UiaVariant(textContentCommand_elementEnd));
}

void _remoteable_visitChildRangesAndGaps(UiaOperationScope& scope, UiaTextPattern& textPattern, UiaTextRange& textRange, std::function<void(UiaOperationScope& scope, UiaTextRange& subrange, UiaElement& childElement)> visitorFunc) {
	// collect the children
	auto children=textRange.GetChildren();
	localLog(INFO,L"Number of children: "<<(children.Size()));
	// clone a new range, collapsing it to the beginning of the over all textRange
	auto tempRange=textRange.Clone();
	tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
	// for all children:
	scope.ForEach(children,[&](auto child) {
		scope.If(child.IsNull(),[&]() {
			localLog(INFO,L"Child is null. Skipping");
			scope.Continue();
		});
		// fetch the subrange for the current child
		auto childRange=textPattern.RangeFromChild(child);
		scope.If(childRange.IsNull(),[&]() {
			localLog(INFO,L"Child range is null. Skipping");
			scope.Continue();
		});
		auto childStartDeltaFromEnd= childRange.CompareEndpoints(TextPatternRangeEndpoint_Start,textRange,TextPatternRangeEndpoint_End);
		scope.If(childStartDeltaFromEnd>=0,[&]() {
			// This child starts at or past the end of the over all textRange.
			// Therefore,  stop processing children.
			scope.Break();
		});
		auto childStartDeltaFromStart = childRange.CompareEndpoints(TextPatternRangeEndpoint_Start,tempRange,TextPatternRangeEndpoint_Start);
		scope.If(childStartDeltaFromStart>0,[&]() {
			// The child starts after tempRange,
			// So stretch tempRange up to start of child and visit that subrange.
			tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,childRange,TextPatternRangeEndpoint_Start);
			visitorFunc(scope,tempRange,UiaElement(nullptr));
			// Collapse tempRange to its end.
			tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_Start,tempRange,TextPatternRangeEndpoint_End);
		});
		auto childEndDeltaFromStart = childRange.CompareEndpoints(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
		scope.If(childEndDeltaFromStart<0,[&]() {
			// This child is completely before tempRange.
			// So skip it.
			scope.Continue();
		});
		// tempRange is now lined up with the start of child,
		// Or the start of textRange if the child happened to start before the over all textRange.
		// Now stretch tempRange's end so it covers all of the child.
		tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,childRange,TextPatternRangeEndpoint_End);
		auto childEndDeltaFromEnd = tempRange.CompareEndpoints(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
		scope.If(childEndDeltaFromEnd>0,[&]() {
			// child's range ends outside of the over all textRange,
			// Therefore clip tempRange so that it does not go beyond the over all textRange.
			tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
		});
		auto tempRangeWidth = tempRange.CompareEndpoints(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
		scope.If(tempRangeWidth>0,[&]() {
			auto text=tempRange.GetText(1);
			scope.If(!text.IsNull()&&text.Length()>0,[&]() {
				// Visit this subrange with the child
				visitorFunc(scope,tempRange,child);
			});
			// collapse tempRange to its end.
			tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_Start,tempRange,TextPatternRangeEndpoint_End);
		});
	});
	auto childEndDeltaFromEnd = tempRange.CompareEndpoints(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
	scope.If(childEndDeltaFromEnd<0,[&]() {
		// After all children,
		// tempRange never reached the end of textRange,
		// I.e. the last child finished before the end.
		// Therefore stretch tempRange's end to the end of the over all textRange.
		tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,textRange,TextPatternRangeEndpoint_End);
		// Visit the final subrange.
		visitorFunc(scope,tempRange,UiaElement(nullptr));
	});
}

UiaArray<UiaVariant> _remoteable_getTextContent(UiaOperationScope& scope, UiaElement& rootElement, UiaTextRange& textRange, UiaOperationAbstraction::UiaCacheRequest& cacheRequest, const std::vector<int>& attribIDs) {
	UiaArray<UiaVariant> content;
	localLog(INFO,L"getTextcontent start");
	localLog(INFO,L"Full text: "<<(textRange.GetText(256).get()));
	auto textPattern=rootElement.GetTextPattern(false);
	scope.If(textPattern.IsNull(),[&]() {
		localLog(INFO,L"text pattern is NULL.");
		return content;
	});
	// Split textRange into subranges by format unit. 
	auto formatRanges=_remoteable_splitTextRangeByUnit(scope,textRange,TextUnit_Format);
	UiaArray<UiaElement> oldAncestors;
	// For each of the subranges:
	scope.ForEach(formatRanges,[&](auto formatRange) {
		localLog(INFO,L"Handling format range");
		// Collect the ancestor UIAElements enclosing this range, up to the root element.
		auto newAncestors=_remoteable_getAncestorsForTextRange(scope,formatRange,rootElement);
		UiaArray<UiaElement> elementsExited;
		UiaArray<UiaElement> elementsEntered;
		// Calculate which ancestors have been exited
		// I.e. the last ancestors which this range is not a part of.
		// and the ancestors now entered
		// I.e. the new ancestors this range is a part of.
		_remoteable_calculateAncestorsExitedAndEntered(scope,oldAncestors,newAncestors,elementsExited,elementsEntered);
		// For each of the old ancestors exited,
		// Record this in the generated textContent.
		scope.ForEach(elementsExited,[&](auto element) {
			localLog(INFO,L"Exited element: "<<(element.GetName(false).get())<<L" "<<(element.GetLocalizedControlType(false).get()));
			_remoteable_appendElementEndInfo(scope,element,content);
		});
		// for each of the ancestors now entered,
		// Record all of their properties in the generated textContent.
		scope.ForEach(elementsEntered,[&](auto element) {
			localLog(INFO,L"Entered element: "<<(element.GetName(false).get())<<L" "<<(element.GetLocalizedControlType(false).get()));
			_remoteable_appendElementStartInfo(scope,element,cacheRequest,content);
		});
		// Splitting the format range into ranges for each embedded child,
		// and the gaps between the children,
		// Walk through the ranges:
		_remoteable_visitChildRangesAndGaps(scope,textPattern,formatRange,[&](UiaOperationScope& scope, UiaTextRange& subrange, UiaElement& child) {
			localLog(INFO,L"Handling childAndGaps subrange");
			// If this range is for a embedded child, record its element start, including properties.
			scope.If(!child.IsNull(),[&]() {
				localLog(INFO,L"child start: "<<(child.GetName(false).get())<<L" "<<(child.GetLocalizedControlType(false).get()));
				_remoteable_appendElementStartInfo(scope,child,cacheRequest,content);
			});
			// Record the text attributes and text for this subrange.
			// If one of the attribute values is Mixed (I.e. resolution is not fine enough),
			// then none of the attributes or text will be recorded at all.
			// In that case, attributes and text should be fetched at an even smaller range later.
			localLog(INFO,L"text: "<<(subrange.GetText(256).get()));
			UiaBool foundMixed=_remoteable_appendAttributesAndTextForRange(scope,subrange,attribIDs,content,false);
			scope.If(foundMixed,[&]() {
				// A mixed attribute value was detected.
				// Therefore, split this subrange into characters.
				auto charRanges=_remoteable_splitTextRangeByUnit(scope,subrange,TextUnit_Character);
				// for each of the character ranges:
				scope.ForEach(charRanges,[&](auto charRange) {
					// Record the text attributes and text for this subrange.
					// this time, Mixed attribute values will simply be ignored,
					// Though we don't expect that there would be any at the smallest resolution.
					_remoteable_appendAttributesAndTextForRange(scope,charRange,attribIDs,content,true);
				});
			});
			// If this range was for an embeded child,
			// Record its element end.
			scope.If(!child.IsNull(),[&]() {
				localLog(INFO,L"child end");
				_remoteable_appendElementEndInfo(scope,child,content);
			});
		});
		// Clear the oldAncestors and copy the newAncestors to the old ready for the next loop iteration.
		_remoteable_clearUiaArray(scope,oldAncestors);
		scope.ForEach(newAncestors,[&](auto element) {
			oldAncestors.Append(element);
		});
	});
	// Now having processed all the format ranges,
	// Finally record element exits for all remaining oldAncestors.
	scope.ForEach(oldAncestors,[&](auto element) {
		localLog(INFO,L"Exit element: "<<(element.GetName(false).get())<<L" "<<(element.GetLocalizedControlType(false).get()));
		_remoteable_appendElementEndInfo(scope,element,content);
	});
	// return the generated text content.
	localLog(INFO,L"getTextcontent end");
	return content;
}

extern "C" __declspec(dllexport) SAFEARRAY* __stdcall uiaRemote_getTextContent(IUIAutomationElement* rootElementArg, IUIAutomationTextRange* textRangeArg, SAFEARRAY* pPropIDsArg, SAFEARRAY* pAttribIDsArg) {
	// Unpack the requested  property and attribute ID safeArrays into vectors.
	auto propIDs=SafeArrayUtil::SafeArrayToVector<VT_I4>(pPropIDsArg);
	auto attribIDs=SafeArrayUtil::SafeArrayToVector<VT_I4>(pAttribIDsArg);
	// Start a new remote ops scope.
	LOG_INFO(L"about to call scope.start_new");
	auto scope=UiaOperationScope::StartNew();
	LOG_INFO(L"Called scope.start_new");
	// Everything from here on is remoted
	UiaTextRange textRange{textRangeArg};
	UiaElement rootElement{rootElementArg};
	// Create a new cache request, and add all the requested properties to it.
	UiaOperationAbstraction::UiaCacheRequest cacheRequest;
	for(auto propID: propIDs) {
		cacheRequest.AddProperty(UiaPropertyId(propID));
	}
	LOG_INFO(L"Calling _remotable_getTextContent");
	auto textContent=_remoteable_getTextContent(scope,rootElement,textRange,cacheRequest,attribIDs);
	LOG_INFO(L"Calling scope.bindResult");
	scope.BindResult(textContent);
	// Actually execute the remote call
	LOG_INFO(L"Calling scope.Resolve");
	scope.Resolve();
	LOG_INFO(L"Called resolve");
	// We aare back to local again 
	// Pack the textContent array we got from the remote call into a new safeArray for returning
	size_t numItems=textContent.Size();
	CComSafeArray<VARIANT> safeArray(numItems);
	for(size_t i=0;i<numItems;++i) {
		VARIANT v=*((*textContent)[i]);
		safeArray.SetAt(i,v);
	}
	return safeArray.Detach();
}

extern "C" __declspec(dllexport) bool __stdcall uiaRemote_initialize(bool doRemote, IUIAutomation* client) {
	std::wstring manifestPath = dllDirectory;
	manifestPath += L"\\Microsoft.UI.UIAutomation.dll.manifest";
	ACTCTX actCtx={0};
	actCtx.cbSize=sizeof(actCtx);
	actCtx.lpSource = L"Microsoft.UI.UIAutomation.dll.manifest";
	actCtx.lpAssemblyDirectory = dllDirectory;
	actCtx.dwFlags = ACTCTX_FLAG_ASSEMBLY_DIRECTORY_VALID;
	HANDLE hActCtx=CreateActCtx(&actCtx);
	if(hActCtx==NULL) {
		LOG_ERROR(L"Could not create activation context for "<<manifestPath);
		return false;
	}
	ULONG_PTR actCtxCookie;
	if(!ActivateActCtx(hActCtx,&actCtxCookie)) {
		LOG_ERROR(L"Error activating activation context for "<<manifestPath);
		ReleaseActCtx(hActCtx);
		return false;
	}
	LOG_INFO(L"Registered "<<manifestPath);
	auto MSUIA_activationFactory = winrt::get_activation_factory<winrt::Microsoft::UI::UIAutomation::AutomationRemoteOperation>();
	if(!MSUIA_activationFactory) {
		LOG_ERROR(L"Unable to get Microsoft.UI.UIAutomation activation factory");
		return false;
	}
	UiaOperationAbstraction::Initialize(doRemote,client);
	LOG_INFO(L"UIAOperationAbstraction::initialize");
	return true;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		GetModuleFileName(hModule,dllDirectory,MAX_PATH);
		PathRemoveFileSpec(dllDirectory);
	}
	return true;
}
