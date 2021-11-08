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

void _remoteable_visitTextRangeByUnit(UiaOperationScope& scope, UiaTextRange& textRange, TextUnit unit, bool backwards, std::function<UiaBool(UiaTextRange& subrange)> visitorFunc) {
	auto logical_minForwardDistance = backwards?-1:1;
	auto logical_TextPatternRangeEndpoint_Start = backwards?TextPatternRangeEndpoint_End:TextPatternRangeEndpoint_Start;
	auto logical_TextPatternRangeEndpoint_End = backwards?TextPatternRangeEndpoint_Start:TextPatternRangeEndpoint_End;
	auto logical_less = [backwards](auto x, auto y) { return backwards?(x>y):(x<y); };
	auto logical_greater = [backwards](auto x, auto y) { return backwards?(x<y):(x>y); };
	auto logical_greater_equal = [backwards](auto x, auto y) { return backwards?(x<=y):(x>=y); };
	// Start with a clone of textRange collapsed to the start
	auto tempRange=textRange.Clone();
	tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,tempRange,logical_TextPatternRangeEndpoint_Start);
	UiaInt endDelta=0;
	UiaBool needsFinalVisit {true};
	scope.While([&](){ return true; },[&](){
		// tempRange may already be at the end of textRange
		// If so, then break out of the loop.
		UiaInt startDelta = tempRange.CompareEndpoints(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		scope.BreakIf(logical_greater_equal(startDelta,0));
		// Expand to the enclosing unit
		auto oldTempRange=tempRange.Clone();
		tempRange.ExpandToEnclosingUnit(unit);
		// Ensure we have not expanded back before where we started.
		startDelta = tempRange.CompareEndpoints(logical_TextPatternRangeEndpoint_Start,oldTempRange,logical_TextPatternRangeEndpoint_Start);
		scope.If(logical_less(startDelta,0),[&](){
			// Clip the range to keep it bounded to where we started.
			tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_Start,oldTempRange,logical_TextPatternRangeEndpoint_Start);
		});
		// Find out if we are past the end of the over all textRange yet
		endDelta = tempRange.CompareEndpoints(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		scope.If(logical_greater(endDelta,0),[&](){
			// We moved past the end of the over all textRange,
			// Clip the tempRange so it stays inside
			tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		});
		auto tempRangeWidth = tempRange.CompareEndpoints(logical_TextPatternRangeEndpoint_End,tempRange,logical_TextPatternRangeEndpoint_Start);
		scope.If(logical_greater(tempRangeWidth,0),[&]() {
			// visit this range
			scope.If(!visitorFunc(tempRange.Clone()), [&]() {
				needsFinalVisit = false;
				scope.Break();
			});
		});
		// if we had to clip to the end of the over all textRange,
			// We should not go any further.
		scope.BreakIf(logical_greater(endDelta,0));
		// collapse the tempRange up to the end, ready to go through the loop again
		tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,tempRange,logical_TextPatternRangeEndpoint_Start);
		auto moved=tempRange.Move(unit,logical_minForwardDistance);
		scope.BreakIf(moved==0);
	}); // loop end
	scope.If(needsFinalVisit&&logical_less(endDelta,0),[&](){ 
		// For some reason we never reached the end of the over all textRange.
		// Move the end forward so we do.
		tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		// Visit this final range
		visitorFunc(tempRange.Clone());
	});
}

UiaInt _remoteable_findHeadingsInTextRange(UiaOperationScope& scope, UiaTextRange& textRange, UiaInt level, UiaInt maxItems, bool backwards, UiaArray<UiaInt>& foundLevels, UiaArray<UiaString> foundLabels, UiaArray<UiaTextRange>& foundRanges) {
	UiaInt numItemsFound {0};
	_remoteable_visitTextRangeByUnit(scope,textRange,TextUnit_Paragraph,backwards,[&](UiaTextRange& subRange){
		auto val = subRange.GetAttributeValue(UIA_StyleIdAttributeId);
		scope.If(val.IsInt(),[&]() {
			auto styleID = val.AsInt();
			scope.If(styleID>=(int)StyleId_Heading1&&styleID<=(int)StyleId_Heading9&&(level==0||(level+(StyleId_Heading1-1))==styleID),[&]() {
				foundLevels.Append(styleID-(StyleId_Heading1-1));
				foundLabels.Append(subRange.GetText(-1));
				foundRanges.Append(subRange);
				numItemsFound += 1;
			});
		});
		return numItemsFound<maxItems;
	});
	return numItemsFound;
}

extern "C" __declspec(dllexport) int __stdcall uiaRemote_findHeadingsInTextRange(IUIAutomationTextRange* textRangeArg, int levelArg, int maxItemsArg, bool backwardsArg, SAFEARRAY** pFoundLevelsArg, SAFEARRAY** pFoundLabelsArg, SAFEARRAY** pFoundRangesArg) {
	// Start a new remote ops scope.
	auto scope=UiaOperationScope::StartNew();
	// Everything from here on is remoted
	UiaTextRange textRange{textRangeArg};
	UiaInt level{levelArg};
	UiaInt maxItems{maxItemsArg};
	UiaArray<UiaInt> foundLevels;
	UiaArray<UiaString> foundLabels;
	UiaArray<UiaTextRange> foundRanges;
	auto numItemsFound=_remoteable_findHeadingsInTextRange(scope,textRange,level,maxItems,backwardsArg,foundLevels,foundLabels,foundRanges);
	scope.BindResult(numItemsFound);
	scope.BindResult(foundLevels);
	scope.BindResult(foundLabels);
	scope.BindResult(foundRanges);
	// Actually execute the remote call
	scope.Resolve();
	// We aare back to local again 
	size_t numItems=numItemsFound;
	SafeArrayUtil::ArrayToSafeArray((*foundLevels).data(), numItems, VT_I4, pFoundLevelsArg);
	SafeArrayUtil::ArrayToSafeArray((*foundLabels).data(), numItems, VT_BSTR, pFoundLabelsArg);
	SafeArrayUtil::ArrayToSafeArray((*foundRanges).data(), numItems, VT_UNKNOWN, pFoundRangesArg);
	return numItemsFound;
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

