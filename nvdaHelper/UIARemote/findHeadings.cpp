#define _SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING
#include <locale>
#include <codecvt>
#include <string>
#include <functional>
#include <string>
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

class RemoteableLogger {
	public:
	RemoteableLogger(UiaOperationScope& scope): _log{} {
		scope.BindResult(_log);
	}
	void log(std::initializer_list<const UiaString> messageArgs) {
		for(const auto& message: messageArgs) {
			_log.Append(message);
		}
		_log.Append(L"\n");
	}
	void dumpLog() {
		assert(!UiaOperationAbstraction::ShouldUseRemoteApi());
		std::wstring messageBlock{L"Dump log start:\n"};
		try {
			auto v = *_log;
			for(const auto& message: v) {
				messageBlock+=message.get();
			}
		} catch (std::exception& e) {
			std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
			auto what = converter.from_bytes(e.what());
			messageBlock+=L"dumpLog exception: " + what + L"\n";
		}
		messageBlock+=L"Dump log end";
		LOG_INFO(messageBlock);
	}
	private:
	UiaArray<UiaString> _log;
};

const bool enableLogging{false};
template<typename... ArgTypes> void LOG(RemoteableLogger& logger, ArgTypes... messageArgs) {
	if constexpr(enableLogging) {
		logger.log({messageArgs...});
	}
}

void _remoteable_visitTextRangeByUnit(RemoteableLogger& logger, UiaOperationScope& scope, UiaTextRange& textRange, TextUnit unit, bool backwards, std::function<UiaBool(UiaTextRange& subrange)> visitorFunc, UiaInt& numUnitsVisited) {
	LOG(logger,L"_remoteable_visitTextRangeByUnit start");
	const UiaInt logical_minForwardDistance{backwards?-1:1};
	const UiaTextPatternRangeEndpoint logical_TextPatternRangeEndpoint_Start{backwards?TextPatternRangeEndpoint_End:TextPatternRangeEndpoint_Start};
	const UiaTextPatternRangeEndpoint logical_TextPatternRangeEndpoint_End{backwards?TextPatternRangeEndpoint_Start:TextPatternRangeEndpoint_End};
	auto logical_less = [backwards](auto x, auto y) { return backwards?(x>y):(x<y); };
	auto logical_greater = [backwards](auto x, auto y) { return backwards?(x<y):(x>y); };
	auto logical_greater_equal = [backwards](auto x, auto y) { return backwards?(x<=y):(x>=y); };
	// Start with a clone of textRange collapsed to the start
	LOG(logger,L"Cloning tempRange");
	auto tempRange=textRange.Clone();
	LOG(logger,L"Collapsing tempRange to start");
	tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,tempRange,logical_TextPatternRangeEndpoint_Start);
	UiaInt endDelta=0;
	UiaBool needsFinalVisit {true};
	LOG(logger,L"Entering while loop");
	scope.While([&](){
		LOG(logger,L"Loop condition: MoveEndPointByUnit != 0");
		return tempRange.MoveEndpointByUnit(logical_TextPatternRangeEndpoint_End, unit,logical_minForwardDistance) != 0;
	},[&]() {
		LOG(logger,L"Loop body");
		endDelta = tempRange.CompareEndpoints(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		scope.If(logical_greater(endDelta,0),[&](){
			LOG(logger,L"Moved past the end of the over all textRange, so clip the tempRange so it stays inside");
			tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		});
		LOG(logger,L"Visit this range");
		scope.If(!visitorFunc(tempRange.Clone()), [&]() {
			LOG(logger,L"Visitor returned false. Breaking");
			needsFinalVisit = false;
			scope.Break();
		},[&](){
			LOG(logger,L"Visitor returned true. not breaking");
		});
		// keep track of where we are now up to in case of timeout
		numUnitsVisited += 1;
		textRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_Start,tempRange,logical_TextPatternRangeEndpoint_End);
		// if we had to clip to the end of the over all textRange,
		// We should not go any further.
		LOG(logger,L"Checking if end was clipped");
		scope.If(logical_greater(endDelta,0),[&](){
			LOG(logger,L"Already clipped the end. Breaking");
			scope.Break();
		});
		LOG(logger,L"collapse the tempRange up to the end");
		tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_Start,tempRange,logical_TextPatternRangeEndpoint_End);
	}); // loop end
	LOG(logger,L"While loop complete");
	scope.If(needsFinalVisit&&logical_less(endDelta,0),[&](){ 
		// For some reason we never reached the end of the over all textRange.
		// Move the end forward so we do.
		LOG(logger,L"Move to cover remaining unit");
		tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		LOG(logger,L"Visit this final range");
		visitorFunc(tempRange.Clone());
		numUnitsVisited += 1;
	});
	LOG(logger,L"_remoteable_visitTextRangeByUnit end");
}

void _remoteable_findHeadingsInTextRange(RemoteableLogger& logger, UiaOperationScope& scope, UiaTextRange& textRange, UiaInt level, const int maxItems, const bool backwards, UiaInt& numUnitsVisited, UiaInt& numItemsFound, UiaArray<UiaInt>& foundLevels, UiaArray<UiaString> foundLabels, UiaArray<UiaTextRange>& foundRanges) {
	LOG(logger,L"_remoteable_findHeadingsInTextRange start");
	_remoteable_visitTextRangeByUnit(logger,scope,textRange,TextUnit_Paragraph,backwards,[&](UiaTextRange& subRange){
		LOG(logger,L"Checking styleId attribute on subRange");
		auto val = subRange.GetAttributeValue(UIA_StyleIdAttributeId);
		scope.If(val.IsInt(),[&]() {
			auto styleID = val.AsInt();
			LOG(logger,L"got styleID: ",styleID.Stringify());
			scope.If(styleID>=UiaInt(StyleId_Heading1)&&styleID<=UiaInt(StyleId_Heading9),[&]() {
				LOG(logger,L"Found heading");
				auto foundLevel = UiaInt(styleID);
				foundLevel-=UiaInt(StyleId_Heading1-1);
			LOG(logger,L"Level: ",foundLevel.Stringify());
				scope.If(level==UiaInt(0)||level==foundLevel,[&]() {
					LOG(logger,L"Level matches");
					foundLevels.Append(foundLevel);
					auto foundLabel = subRange.GetText(-1);
					LOG(logger,L"And label: ",foundLabel.Stringify());
					foundLabels.Append(foundLabel);
					foundRanges.Append(subRange);
					numItemsFound += 1;
				},[&]() {
					LOG(logger,L"Level did not match");
				});
			},[&](){
				LOG(logger,L"Not a heading");
			});
		},[&]() {
			LOG(logger,L"StyleID not an int");
		});
		LOG(logger,L"Returning from visitor");
		return (maxItems==0)?UiaBool(true):(numItemsFound<maxItems);
	}, numUnitsVisited);
	LOG(logger,L"numItemsFound: ",numItemsFound.Stringify());
}

extern "C" __declspec(dllexport) HRESULT __stdcall findHeadingsInTextRange(IUIAutomationTextRange* textRangeArg, int maxItemsArg, bool backwardsArg, int levelArg, int* pNumItemsFound, SAFEARRAY** pFoundLevelsArg, SAFEARRAY** pFoundLabelsArg, SAFEARRAY** pFoundRangesArg, IUIAutomationTextRange** pRemainingTextRange) {
	// Start a new remote ops scope.
	LOG_INFO(L"Starting remote scope");
	auto scope=UiaOperationScope::StartNew();
	// Everything from here on is remoted
	LOG_INFO(L"Creating remote variables");
	RemoteableLogger logger{scope};
	LOG_INFO(L"started logging");
	UiaTextRange textRange{textRangeArg};
	LOG_INFO(L"Created textRange");
	UiaInt level{levelArg};
	LOG_INFO(L"Created level");
	UiaInt numUnitsVisited{0};
	UiaArray<UiaInt> foundLevels;
	UiaArray<UiaString> foundLabels;
	LOG_INFO(L"Created foundLabels");
	UiaArray<UiaTextRange> foundRanges;
	LOG_INFO(L"Created foundRanges");
	LOG_INFO(L"Calling func");
	UiaInt numItemsFound{0};
	try {
		scope.TryCatch([&]() {
			_remoteable_findHeadingsInTextRange(logger,scope,textRange,level,maxItemsArg,backwardsArg,numUnitsVisited,numItemsFound,foundLevels,foundLabels,foundRanges);
		},[&](UiaFailure& failure) {
			auto code = failure.GetCurrentFailureCode();
			LOG(logger,L"_remoteable_findHeadingsInTextRange failed with code ",code.Stringify());
		});
	} catch (std::exception& e) {
		std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
		auto what = converter.from_bytes(e.what());
		LOG_INFO(L"Error calling _remoteable_findHeadingsInTextRange: "<<what);
	}
	LOG_INFO(L"Done calling func");
	scope.BindResult(textRange,numItemsFound, numUnitsVisited, foundLevels, foundLabels, foundRanges);
	LOG_INFO(L"call resolve");
	auto res = scope.ResolveHr();
	if(res != S_OK) {
		LOG_INFO(L"Error in remote operation. code "<<res);
	}
	// We aare back to local again 
	logger.dumpLog();
	LOG_INFO(L"NumUnitsVisited: "<<(int)numUnitsVisited);
	size_t numItems=numItemsFound;
	*pNumItemsFound = numItemsFound;
	LOG_INFO(L"NumItems: "<<numItems);
	SafeArrayUtil::ArrayToSafeArray((*foundLevels).data(), numItems, VT_I4, pFoundLevelsArg);
	LOG(logger,L"wrote SAFEARRAY for foundLevels");
	CComSafeArray<BSTR> sa_foundLabels{numItems};
	for(size_t i=0;i<numItems;++i) {
		sa_foundLabels.SetAt(i, (*foundLabels)[i].get());
	}
	*pFoundLabelsArg=sa_foundLabels.Detach();
	LOG(logger,L"wrote SAFEARRAY for foundLabels");
	SafeArrayUtil::ArrayToSafeArray((*foundRanges).data(), numItems, VT_UNKNOWN, pFoundRangesArg);
	LOG(logger,L"wrote SAFEARRAY for foundRanges");
	if(res==E_FAIL) {
		LOG_INFO(L"Max instructions reached. Returning remaining textRange");
		*pRemainingTextRange = (*textRange).detach();
		return S_FALSE;
	}
	return S_OK;
}
