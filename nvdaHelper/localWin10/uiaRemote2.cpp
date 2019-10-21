#include <windows.h>
#include <UIAutomation.h>
#include <UiaOperationAbstraction/UiaOperationAbstraction.h>
#include <common/log.h>

using namespace UiaOperationAbstraction;

extern "C" __declspec(dllexport) int __stdcall uiaRemote_getTextRangeUnitCount2(BOOL doRemote, IUIAutomationTextRange* textRangeArg,  TextUnit unitArg) {
	UiaOperationAbstraction::Initialize(doRemote,nullptr);
	UiaTextRange textRange{textRangeArg};
	auto scope=UiaOperationScope::StartNew();
	scope.BindInput(textRange);
	auto tempRange=textRange.Clone();
	tempRange.MoveEndpointByRange(TextPatternRangeEndpoint_End,tempRange,TextPatternRangeEndpoint_Start);
	UiaInt unitCount=0;
	scope.While([&](){ return true; },[&](){
		auto moved=tempRange.Move(unitArg,1);
		scope.If(moved<=0,[&]() {
			scope.Break();
		});
		auto passedEnd=tempRange.CompareEndpoints(TextPatternRangeEndpoint_Start,textRange,TextPatternRangeEndpoint_End);
		scope.If(passedEnd>=0,[&]() {
			scope.Break();
		});
		unitCount+=1;
	});
	scope.BindResult(unitCount);
	scope.Resolve();
	return unitCount;
}
