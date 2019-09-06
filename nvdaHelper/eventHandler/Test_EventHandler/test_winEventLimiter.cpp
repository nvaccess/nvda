#include "stdafx.h"
#include "CppUnitTest.h"
#include "winEventLimiter.h"
#include <WinUser.h>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

std::vector<DWORD> specialCaseEvents({
	EVENT_SYSTEM_FOREGROUND,
	EVENT_OBJECT_FOCUS,
	EVENT_OBJECT_SHOW,
	EVENT_OBJECT_HIDE,
	EVENT_SYSTEM_MENUSTART,
	EVENT_SYSTEM_MENUEND,
	EVENT_SYSTEM_MENUPOPUPSTART,
	EVENT_SYSTEM_MENUPOPUPEND,
});

namespace Microsoft {
	namespace VisualStudio {
		namespace CppUnitTestFramework
		{
			template<> inline std::wstring ToString<std::vector<int>>(const std::vector<int>& t) {
				std::wstringstream ss;
				ss << "[ ";
				for (auto i : t) {
					ss << i << L", ";
				}
				ss << " ]";
				return ss.str();
			}
		}
	}
}


namespace Test_EventHandler
{		
	TEST_CLASS(test_WinEventLimiter)
	{
	public:

		TEST_METHOD(test_limitEventsPerThread)
		{
			WinEventLimiter limiter;
			for (int n = 2000 - 1; n >= 0; --n) {
				EventData e = {
					specialCaseEvents[n % specialCaseEvents.size()],
					reinterpret_cast<HWND>(n), // window
					n, // objectID - in this test, used as an ID.
					n, // childID
					0, // threadID - all events for same thread
				};
				limiter.AddEvent(e);
			}

			auto actualEvents = limiter.Flush();
			std::vector<int> actualIds;
			for (auto& e : actualEvents) {
				actualIds.push_back(e.idObject);
			}
			std::vector<int> expectedIds({
				// 26, 24, 19, 18, 16, 11, 10, 9, 8, 8, 4, 3, 2, 1, 0, 0 // python orderedWinEventLimiter result
				4, 0, // actual result.
				});
			Assert::AreEqual(expectedIds, actualIds);
		}

	};
}