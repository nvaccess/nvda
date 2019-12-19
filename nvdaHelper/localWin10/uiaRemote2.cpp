#include <functional>
#include <windows.h>
#include <atlsafe.h>
#include <atlcomcli.h>
#include <UIAutomation.h>
#include <UiaOperationAbstraction/UiaOperationAbstraction.h>
#include <common/log.h>

using namespace UiaOperationAbstraction;

const auto textContentCommand_elementStart=1;
const auto textContentCommand_text=2;
const auto textContentCommand_elementEnd=3;

template<typename ItemType> UiaBool _remoteable_areUiaArraysEqual(UiaOperationScope& scope, UiaArray<ItemType>& array1, UiaArray<ItemType>& array2) {
	auto count1=array1.Size();
	auto count2=array2.Size();
	UiaBool areEqual{true};
	scope.If(count1!=count2,[&]() {
		areEqual=false;
	},[&]() {
		UiaUint index=0;
		scope.For([&](){},[&]() {
			return index<count1;
		},[&]() {
			index+=1;
		},[&]() {
			areEqual=array1.GetAt(index)==array2.GetAt(index);
			scope.If(!areEqual,[&]() {
				scope.Break();
			});
		});
	});
	return areEqual;
}


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
		// Move the end forward by the given unit
		auto moved=tempRange.MoveEndpointByUnit(TextPatternRangeEndpoint_End, unit, 1);
		scope.If(moved<=0,[&]() {
			// We couldn't move forward, so break
			scope.Break();
		});
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
		tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_Start,tempRange,TextPatternRangeEndpoint_End);
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

template<typename ItemType> void _remoteable_visitUiaArrayElements(UiaOperationScope& scope, UiaArray<ItemType>& array, std::function<void(UiaOperationScope& scope, typename UiaArray<ItemType>::_ItemWrapperType&)> visitorFunc) {
	UiaUint arrayCount=array.Size();
	UiaUint index=0;
	scope.For([&](){},[&]() {
		return index<arrayCount;
	},[&](){
		index+=1;
	},[&]() {
		auto element=array.GetAt(index);
		visitorFunc(scope,element);
	});
}

UiaBool _remoteable_appendAttributesAndTextForRange(UiaOperationScope& scope,UiaTextRange& textRange,const std::vector<int>& attribIDs,UiaArray<UiaVariant>& outArray, UiaBool ignoreMixedAttributes) {
	UiaBool foundMixed=false;
	UiaArray<UiaVariant> attribValues;
	for(auto attribID: attribIDs) {
		scope.If(!foundMixed,[&]() {
			auto attribValue=textRange.GetAttributeValue(UiaTextAttributeId(attribID));
			scope.If(attribValue.IsMixedAttribute(nullptr),[&]() {
				attribValues.Append(UiaVariant(0));
				foundMixed=!ignoreMixedAttributes;
			},[&]() {
				scope.If(attribValue.IsNotSupported(nullptr),[&]() {
					attribValues.Append(UiaVariant(0));
				},[&]() {
					attribValues.Append(attribValue);
				});
			});
		});
	}
	scope.If(!foundMixed,[&]() {
		outArray.Append(UiaVariant(textContentCommand_text));
		_remoteable_visitUiaArrayElements(scope,attribValues,[&](UiaOperationScope& scope, auto& attribValue) {
			outArray.Append(attribValue);
		});
		auto text=textRange.GetText(-1);
		outArray.Append(UiaVariant(text));
	});
	return foundMixed;
}

UiaBool _remoteable_compareUiaElements(UiaOperationScope& scope, UiaElement& element1, UiaElement& element2) {
		auto ID1=element1.GetRuntimeId(false);
		auto ID2=element2.GetRuntimeId(false);
		return _remoteable_areUiaArraysEqual(scope,ID1,ID2);
}

UiaArray<UiaElement> _remoteable_getAncestorsForTextRange(UiaOperationScope& scope, UiaTextRange& textRange, UiaElement& rootElement) {
	UiaArray<UiaElement> ancestors;
	auto parent=textRange.GetEnclosingElement();
	scope.While([&]() {
		return !parent.IsNull();
	},[&]() {
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
	auto exitCount=oldCount;
	auto newCount=newAncestors.Size();
	UiaUint index=0;
	scope.For([&](){},[&]() {
		return index<newCount;
	},[&]() {
		index+=1;
	},[&]() {
		auto newElementIndex=(newCount-index)-UiaUint(1);
		auto newElement=newAncestors.GetAt(newElementIndex);
		scope.If(index<oldCount,[&]() {
			auto oldElementIndex=(oldCount-index)-UiaUint(1);
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
	scope.For([&](){},[&]() {
		return oldIndex<exitCount;
	},[&]() {
		oldIndex+=1;
	},[&]() {
		auto oldElement=oldAncestors.GetAt(oldIndex);
		elementsExited.Append(oldElement);
	});
}

void _remoteable_appendElementStartInfo(UiaOperationScope& scope, UiaElement& element, std::vector<int>& propIDs, UiaArray<UiaVariant>& outArray) {
	outArray.Append(UiaVariant(textContentCommand_elementStart));
	for(auto propID: propIDs) {
		auto propValue=element.GetPropertyValue(UiaPropertyId(propID),false,false);
		outArray.Append(propValue);
	}
}

void _remoteable_appendElementEndInfo(UiaOperationScope& scope, UiaElement& element, UiaArray<UiaVariant>& outArray) {
	outArray.Append(UiaVariant(textContentCommand_elementEnd));
}

void _remoteable_visitChildRangesAndGaps(UiaOperationScope& scope, UiaTextRange& textRange, std::function<void(UiaOperationScope& scope, UiaTextRange& subrange, UiaElement& childElement)> visitorFunc) {
	// collect the children
	auto children=textRange.GetChildren();
	// clone a new range, collapsing it to the beginning of the over all textRange
	auto tempRange=textRange.Clone();
	tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
	// for all children:
	_remoteable_visitUiaArrayElements(scope,children,[&](UiaOperationScope& scope, auto& child) {
		scope.If(child.IsNull(),[&]() {
			// child is NULL. Skipping.
			scope.Continue();
		});
		// fetch the subrange for the current child
		auto textChildPattern=child.GetTextChildPattern(false);
		scope.If(textChildPattern.IsNull(),[&]() {
			// child does not support textchildPattern. Skipping.
			scope.Continue();
		});
		auto childRange=textChildPattern.GetTextRange();
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

UiaArray<UiaVariant> _remoteable_getTextContent(UiaOperationScope& scope, UiaElement& rootElement, UiaTextRange& textRange, std::vector<int>& propIDs, const std::vector<int>& attribIDs) {
	UiaArray<UiaVariant> content;
	auto formatRanges=_remoteable_splitTextRangeByUnit(scope,textRange,TextUnit_Format);
	UiaArray<UiaElement> oldAncestors;
	_remoteable_visitUiaArrayElements(scope,formatRanges,[&](UiaOperationScope& scope, auto& formatRange) {
		auto newAncestors=_remoteable_getAncestorsForTextRange(scope,formatRange,rootElement);
		UiaArray<UiaElement> elementsExited;
		UiaArray<UiaElement> elementsEntered;
		_remoteable_calculateAncestorsExitedAndEntered(scope,oldAncestors,newAncestors,elementsExited,elementsEntered);
		_remoteable_visitUiaArrayElements(scope,elementsExited,[&](UiaOperationScope& scope,auto& element) {
			_remoteable_appendElementEndInfo(scope,element,content);
		});
		_remoteable_visitUiaArrayElements(scope,elementsEntered,[&](UiaOperationScope& scope, auto& element) {
			_remoteable_appendElementStartInfo(scope,element,propIDs,content);
		});
		_remoteable_visitChildRangesAndGaps(scope,formatRange,[&](UiaOperationScope& scope, UiaTextRange& subrange, UiaElement& child) {
			scope.If(!child.IsNull(),[&]() {
				_remoteable_appendElementStartInfo(scope,child,propIDs,content);
			});
			UiaBool foundMixed=_remoteable_appendAttributesAndTextForRange(scope,subrange,attribIDs,content,false);
			scope.If(foundMixed,[&]() {
				auto charRanges=_remoteable_splitTextRangeByUnit(scope,subrange,TextUnit_Character);
				_remoteable_visitUiaArrayElements(scope,charRanges,[&](UiaOperationScope& scope, auto& charRange) {
					_remoteable_appendAttributesAndTextForRange(scope,charRange,attribIDs,content,true);
				});
			});
			scope.If(!child.IsNull(),[&]() {
				_remoteable_appendElementEndInfo(scope,child,content);
			});
		});
		_remoteable_clearUiaArray(scope,oldAncestors);
		_remoteable_visitUiaArrayElements(scope,newAncestors,[&](UiaOperationScope& scope, auto& element) {
			oldAncestors.Append(element);
		});
	});
	_remoteable_visitUiaArrayElements(scope,oldAncestors,[&](UiaOperationScope& scope, auto& element) {
		_remoteable_appendElementEndInfo(scope,element,content);
	});
	return content;
}

extern "C" __declspec(dllexport) SAFEARRAY* __stdcall uiaRemote_getTextContent(IUIAutomationElement* rootElementArg, IUIAutomationTextRange* textRangeArg, SAFEARRAY* pPropIDsArg, SAFEARRAY* pAttribIDsArg) {
	auto scope=UiaOperationScope::StartNew();
	UiaTextRange textRange{textRangeArg};
	UiaElement rootElement{rootElementArg};
	CComSafeArray<int> propIDsArray{pPropIDsArg};
	auto propCount=propIDsArray.GetCount();
	std::vector<int> propIDs;
	for(size_t i=0;i<propCount;++i) {
		auto propID=propIDsArray.GetAt(i);
		propIDs.push_back(propID);
	}
	CComSafeArray<int> attribIDsArray{pAttribIDsArg};
	auto attribCount=attribIDsArray.GetCount();
	std::vector<int> attribIDs;
	for(size_t i=0;i<attribCount;++i) {
		auto attribID=attribIDsArray.GetAt(i);
		attribIDs.push_back(attribID);
	}
	auto textContent=_remoteable_getTextContent(scope,rootElement,textRange,propIDs,attribIDs);
	scope.BindResult(textContent);
	scope.Resolve();
	size_t numItems=textContent.Size();
	CComSafeArray<VARIANT> safeArray(numItems);
	for(size_t i=0;i<numItems;++i) {
		VARIANT v=*((*textContent)[i]);
		safeArray.SetAt(i,v);
	}
	return safeArray.Detach();
}

extern "C" __declspec(dllexport) void __stdcall uiaRemote_initialize(bool doRemote, IUIAutomation* client) {
	UiaOperationAbstraction::Initialize(doRemote,client);
}
