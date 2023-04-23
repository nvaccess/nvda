#include <vector>
#include <uiautomation.h>
#include <comutil.h>

std::vector<int> SafeArrayToVector(SAFEARRAY* pSafeArray);

std::vector<int> getRuntimeIDFromElement(IUIAutomationElement* pElement);
