#include <windows.h>
#include <atlcomcli.h>
#include <UIAutomation.h>
#include <UiaOperationAbstraction/UiaOperationAbstraction.h>
#include <common/log.h>

using namespace UiaOperationAbstraction;

UiaArray<UiaTextRange> UiaRemote_splitTextRangeByUnit(UiaTextRange textRange, TextUnit unit) {
	auto scope=UiaOperationScope::StartOrContinue();
	scope.BindInput(textRange);
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
	scope.BindResult(ranges);
	scope.Resolve();
	return ranges;
}

extern "C" __declspec(dllexport) BSTR __stdcall uiaRemote_getTextContent(IUIAutomationTextRange* textRangeArg) {
	UiaTextRange textRange{textRangeArg};
	auto scope=UiaOperationScope::StartNew();
	//scope.BindInput(textRange);
	auto ranges=UiaRemote_splitTextRangeByUnit(textRange,TextUnit_Format);
	auto s=ranges.Size();
	UiaUint index=0;
	UiaArray<UiaString> textContent;
	scope.For([&]() {
		index=0;
	},[&]() {
		return index<s;
	},[&]() {
		index+=1;
	},[&]() {
		textContent.Append(L"format ");
		auto subrange=ranges.GetAt(index);
				textContent.Append(subrange.GetText(-1));
	});
	scope.BindResult(textContent);
	scope.Resolve();
	std::wstring finalText;
	for(auto t: *textContent) {
		finalText.append(t.get());
	}
	return SysAllocString(finalText.c_str());
}

extern "C" __declspec(dllexport) void __stdcall uiaRemote_initialize(bool doRemote, IUIAutomation* client) {
	UiaOperationAbstraction::Initialize(doRemote,client);
}
