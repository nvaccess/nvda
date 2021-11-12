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

const std::wstring endl{L"\n"};
const bool enableLogging{true};

class RemoteableLogger;

class RemoteableLogger {
	public:
	RemoteableLogger(UiaOperationScope& scope): _log{} {
		scope.BindResult(_log);
	}
	template<typename T> RemoteableLogger& operator <<(T& message) {
		if constexpr(enableLogging) {
			if constexpr(std::is_base_of<UiaInt,T>::value) {
				_log.Append(message.Stringify());
			} else {
				_log.Append(message);
			}
		}
		return *this;
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

void _remoteable_visitTextRangeByUnit(RemoteableLogger& logger, UiaOperationScope& scope, UiaTextRange& textRange, TextUnit unit, bool backwards, std::function<UiaBool(UiaTextRange& subrange)> visitorFunc, UiaInt& numUnitsVisited) {
	logger<<L"_remoteable_visitTextRangeByUnit start"<<endl;
	const UiaInt logical_minForwardDistance{backwards?-1:1};
	const UiaTextPatternRangeEndpoint logical_TextPatternRangeEndpoint_Start{backwards?TextPatternRangeEndpoint_End:TextPatternRangeEndpoint_Start};
	const UiaTextPatternRangeEndpoint logical_TextPatternRangeEndpoint_End{backwards?TextPatternRangeEndpoint_Start:TextPatternRangeEndpoint_End};
	auto logical_less = [backwards](auto x, auto y) { return backwards?(x>y):(x<y); };
	auto logical_greater = [backwards](auto x, auto y) { return backwards?(x<y):(x>y); };
	auto logical_greater_equal = [backwards](auto x, auto y) { return backwards?(x<=y):(x>=y); };
	// Start with a clone of textRange collapsed to the start
	logger<<L"Cloning tempRange"<<endl;
	auto tempRange=textRange.Clone();
	logger<<L"Collapsing tempRange to start"<<endl;
	tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,tempRange,logical_TextPatternRangeEndpoint_Start);
	UiaInt endDelta=0;
	UiaBool needsFinalVisit {true};
	logger<<L"Entering while loop"<<endl;
	scope.While([&](){
		logger<<L"Loop condition: MoveEndPointByUnit != 0"<<endl;
		return tempRange.MoveEndpointByUnit(logical_TextPatternRangeEndpoint_End, unit,logical_minForwardDistance) != 0;
	},[&]() {
		logger<<L"Loop body"<<endl;
		endDelta = tempRange.CompareEndpoints(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		scope.If(logical_greater(endDelta,0),[&](){
			logger<<L"Moved past the end of the over all textRange, so clip the tempRange so it stays inside"<<endl;
			tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		});
		logger<<L"Visit this range"<<endl;
		scope.If(!visitorFunc(tempRange.Clone()), [&]() {
			logger<<L"Visitor returned false. Breaking"<<endl;
			needsFinalVisit = false;
			scope.Break();
		},[&](){
			logger<<L"Visitor returned true. not breaking"<<endl;
		});
		// keep track of where we are now up to in case of timeout
		numUnitsVisited += 1;
		textRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_Start,tempRange,logical_TextPatternRangeEndpoint_End);
		// if we had to clip to the end of the over all textRange,
		// We should not go any further.
		logger<<L"Checking if end was clipped"<<endl;
		scope.If(logical_greater(endDelta,0),[&](){
			logger<<L"Already clipped the end. Breaking"<<endl;
			scope.Break();
		});
		logger<<L"collapse the tempRange up to the end"<<endl;
		tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_Start,tempRange,logical_TextPatternRangeEndpoint_End);
	}); // loop end
	logger<<L"While loop complete"<<endl;
	scope.If(needsFinalVisit&&logical_less(endDelta,0),[&](){ 
		// For some reason we never reached the end of the over all textRange.
		// Move the end forward so we do.
		logger<<L"Move to cover remaining unit"<<endl;
		tempRange.MoveEndpointByRange(logical_TextPatternRangeEndpoint_End,textRange,logical_TextPatternRangeEndpoint_End);
		logger<<L"Visit this final range"<<endl;
		visitorFunc(tempRange.Clone());
		numUnitsVisited += 1;
	});
	logger<<L"_remoteable_visitTextRangeByUnit end"<<endl;
}

void _remoteable_findHeadingsInTextRange(RemoteableLogger& logger, UiaOperationScope& scope, UiaTextRange& textRange, UiaInt level, const int maxItems, const bool backwards, UiaInt& numUnitsVisited, UiaInt& numItemsFound, UiaArray<UiaInt>& foundLevels, UiaArray<UiaString> foundLabels, UiaArray<UiaTextRange>& foundRanges) {
	logger<<L"_remoteable_findHeadingsInTextRange start"<<endl;
	_remoteable_visitTextRangeByUnit(logger,scope,textRange,TextUnit_Paragraph,backwards,[&](UiaTextRange& subRange){
		logger<<L"Checking styleId attribute on subRange"<<endl;
		auto val = subRange.GetAttributeValue(UIA_StyleIdAttributeId);
		scope.If(val.IsInt(),[&]() {
			auto styleID = val.AsInt();
			logger<<L"got styleID: "<<styleID<<endl;
			scope.If(styleID>=UiaInt(StyleId_Heading1)&&styleID<=UiaInt(StyleId_Heading9),[&]() {
				logger<<L"Found heading"<<endl;
				auto foundLevel = UiaInt(styleID);
				foundLevel-=UiaInt(StyleId_Heading1-1);
			logger<<L"Level: "<<foundLevel<<endl;
				scope.If(level==UiaInt(0)||level==foundLevel,[&]() {
					logger<<L"Level matches"<<endl;
					foundLevels.Append(foundLevel);
					auto foundLabel = subRange.GetText(-1);
					logger<<L"And label: "<<foundLabel<<endl;
					foundLabels.Append(foundLabel);
					foundRanges.Append(subRange);
					numItemsFound += 1;
				},[&]() {
					logger<<L"Level did not match"<<endl;
				});
			},[&](){
				logger<<L"Not a heading"<<endl;
			});
		},[&]() {
			logger<<L"StyleID not an int"<<endl;
		});
		logger<<L"Returning from visitor"<<endl;
		return (maxItems==0)?UiaBool(true):(numItemsFound<maxItems);
	}, numUnitsVisited);
	logger<<L"numItemsFound: "<<numItemsFound<<endl;
}

extern "C" __declspec(dllexport) HRESULT __stdcall findHeadingsInTextRange(IUIAutomationTextRange* textRangeArg, int maxItemsArg, bool backwardsArg, int levelArg, int* pNumItemsFound, SAFEARRAY** pFoundLevelsArg, SAFEARRAY** pFoundLabelsArg, SAFEARRAY** pFoundRangesArg, IUIAutomationTextRange** pRemainingTextRange) {
	// Start a new remote ops scope.
	auto scope=UiaOperationScope::StartNew();
	// Everything from here on is remoted
	RemoteableLogger logger{scope};
	UiaTextRange textRange{textRangeArg};
	UiaInt level{levelArg};
	UiaInt numUnitsVisited{0};
	UiaArray<UiaInt> foundLevels;
	UiaArray<UiaString> foundLabels;
	UiaArray<UiaTextRange> foundRanges;
	UiaInt numItemsFound{0};
	try {
		scope.TryCatch([&]() {
			_remoteable_findHeadingsInTextRange(logger,scope,textRange,level,maxItemsArg,backwardsArg,numUnitsVisited,numItemsFound,foundLevels,foundLabels,foundRanges);
		},[&](UiaFailure& failure) {
			auto code = failure.GetCurrentFailureCode();
			logger<<L"_remoteable_findHeadingsInTextRange failed with code "<<code<<endl;
		});
	} catch (std::exception& e) {
		std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
		auto what = converter.from_bytes(e.what());
		LOG_ERROR(L"Error calling _remoteable_findHeadingsInTextRange: "<<what);
	}
	scope.BindResult(textRange,numItemsFound, numUnitsVisited, foundLevels, foundLabels, foundRanges);
	auto res = scope.ResolveHr();
	if(res != S_OK) {
		LOG_DEBUGWARNING(L"Error in remote operation. code "<<res);
	}
	// We aare back to local again 
	logger.dumpLog();
	size_t numItems=numItemsFound;
	*pNumItemsFound = numItemsFound;
	SafeArrayUtil::ArrayToSafeArray((*foundLevels).data(), numItems, VT_I4, pFoundLevelsArg);
	CComSafeArray<BSTR> sa_foundLabels{numItems};
	for(size_t i=0;i<numItems;++i) {
		sa_foundLabels.SetAt(i, (*foundLabels)[i].get());
	}
	*pFoundLabelsArg=sa_foundLabels.Detach();
	SafeArrayUtil::ArrayToSafeArray((*foundRanges).data(), numItems, VT_UNKNOWN, pFoundRangesArg);
	if(res==E_FAIL) {
		LOG_DEBUGWARNING(L"Max instructions reached. Returning remaining textRange");
		*pRemainingTextRange = (*textRange).detach();
		return S_FALSE;
	}
	return S_OK;
}
