#include <windows.h>
#include <UIAutomation.h>
#include <winrt/Windows.UI.Internal.Automation.h>
#include <common/log.h>

namespace uiaRemote {
	using namespace winrt::Windows::UI::Internal::Automation;
}

extern "C" __declspec(dllexport) int __stdcall uiaRemote_getTextRangeUnitCount(IUIAutomationTextRange* a_textRange,  TextUnit a_unit) {
	uiaRemote::AutomationTextRange l_textRange=nullptr;
	winrt::copy_from_abi(l_textRange,a_textRange);
	uiaRemote::AutomationRemoteOperation rp;
	auto r_textRange=rp.ImportTextRange(l_textRange);
	auto r_tempRange=r_textRange.Clone();
	r_tempRange.MoveEndpointByRange(rp.NewEnum(uiaRemote::AutomationTextPatternRangeEndpoint::End),r_tempRange,rp.NewEnum(uiaRemote::AutomationTextPatternRangeEndpoint::Start));
	auto r_unitCount=rp.NewInt(0);
	rp.WhileBlock(rp.NewBool(true),[&](){
		auto r_moved=r_tempRange.Move(rp.NewEnum(uiaRemote::AutomationTextUnit::Character),rp.NewInt(1));
		rp.IfBlock(r_moved.IsLessThanOrEqual(rp.NewInt(0)),[&]() {
			rp.BreakLoop();
		});
		auto r_passedEnd=r_tempRange.CompareEndpoints(rp.NewEnum(uiaRemote::AutomationTextPatternRangeEndpoint::Start),r_textRange,rp.NewEnum(uiaRemote::AutomationTextPatternRangeEndpoint::End));
		rp.IfBlock(r_passedEnd.IsGreaterThanOrEqual(rp.NewInt(0)),[&]() {
			rp.BreakLoop();
		});
		r_unitCount.Add(rp.NewInt(1));
	});
	auto t_unitCount=rp.RequestResponse(r_unitCount);
	auto results=rp.Execute();
	auto status=results.OperationStatus();
	if(FAILED(status)) {
		LOG_ERROR(L"UIA remote execution failed with code "<<status);
		return status;
	}
	int retVal=winrt::unbox_value<int>(results.GetResult(t_unitCount));
	return retVal;
}




