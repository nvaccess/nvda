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

UiaArray<UiaTextRange> _remoteable_splitTextRangeByUnit(UiaOperationScope& scope, UiaTextRange& textRange, TextUnit unit) {
	UiaArray<UiaTextRange> ranges;
	// Start with a clone of textRange collapsed to the start
	auto tempRange=textRange.Clone();
	tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
	UiaInt endDelta=0;
	scope.While([&](){ return true; },[&](){
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
		// Save off this range
		ranges.Append(tempRange.Clone());
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

template<typename arrayType> void _remoteable_visitUiaArrayElements(UiaOperationScope& scope, arrayType& array, std::function<UiaBool(typename arrayType::_ItemWrapperType&)> visitorFunc) {
	auto arrayCount=array.Size();
	UiaUint index=0;
	scope.For([&](){},[&]() {
		return index<arrayCount;
	},[&](){
		index+=1;
	},[&]() {
		auto element=array.GetAt(index);
		scope.If(!visitorFunc(element),[&]() {
			scope.Break();
		});
	});
}

UiaBool _remoteable_getAttributesAndTextForRange(UiaOperationScope& scope,UiaTextRange textRange,UiaArray<UiaInt>& attribIDs,UiaArray<UiaVariant>& outArray,const bool ignoreMixedAttributes) {
	UiaBool foundMixed{false};
	UiaArray<UiaVariant> attribValues;
	_remoteable_visitUiaArrayElements(scope,attribIDs,[&](UiaInt attribID) {
		auto attribValue=textRange.GetAttributeValue(UiaTextAttributeId(attribID));
		scope.If(attribValue.IsMixedAttribute(nullptr),[&]() {
			if(ignoreMixedAttributes) {
				attribValues.Append(UiaVariant(0));
			} else {
				foundMixed=true;
				scope.Break();
			}
		});
		scope.If(attribValue.IsNotSupported(nullptr),[&]() {
			attribValues.Append(UiaVariant(0));
		},[&]() {
			attribValues.Append(attribValue);
		});
		return !foundMixed;
	});
	scope.If(!foundMixed,[&]() {
		outArray.Append(UiaVariant(textContentCommand_text));
		_remoteable_visitUiaArrayElements(scope,attribValues,[&](auto& element) {
			outArray.Append(element);
			return true;
		});
		auto text=textRange.GetText(-1);
		outArray.Append(UiaVariant(text));
	});
	return foundMixed;
}

UiaArray<UiaVariant> _remoteable_getTextContent(UiaOperationScope& scope, UiaTextRange& textRange, UiaArray<UiaInt>& attribIDs) {
	UiaArray<UiaVariant> content;
	auto formatRanges=_remoteable_splitTextRangeByUnit(scope,textRange,TextUnit_Format);
	_remoteable_visitUiaArrayElements(scope,formatRanges,[&](auto& formatRange) {
		UiaBool foundMixed=_remoteable_getAttributesAndTextForRange(scope,formatRange,attribIDs,content,false);
		scope.If(foundMixed,[&]() {
			auto charRanges=_remoteable_splitTextRangeByUnit(scope,formatRange,TextUnit_Character);
			_remoteable_visitUiaArrayElements(scope,charRanges,[&](auto& charRange) {
				_remoteable_getAttributesAndTextForRange(scope,charRange,attribIDs,content,true);
				return true;
			});
		});
		return true;
	});
	return content;
}

extern "C" __declspec(dllexport) SAFEARRAY* __stdcall uiaRemote_getTextContent(IUIAutomationTextRange* textRangeArg, SAFEARRAY* pAttribIDsArg) {
	auto scope=UiaOperationScope::StartNew();
	UiaTextRange textRange{textRangeArg};
	CComSafeArray<int> attribIDsArray{pAttribIDsArg};
	auto attribCount=attribIDsArray.GetCount();
	UiaArray<UiaInt> attribIDs;
	for(size_t i=0;i<attribCount;++i) {
		attribIDs.Append(attribIDsArray.GetAt(i));
	}
	auto textContent=_remoteable_getTextContent(scope,textRange,attribIDs);
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
