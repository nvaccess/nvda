import time
import os
from ctypes import windll, byref, POINTER, c_int, c_void_p
from comtypes import BSTR
from comtypes.safearray import _midlSAFEARRAY as SAFEARRAY
import NVDAHelper
from logHandler import log
import UIAHandler


_dll=windll[os.path.join(NVDAHelper.versionedLibPath, "UIARemote.dll")]
initialize=_dll.initialize

def findHeadingsInTextRange(textRange, maxItems=None, backwards=False, level=0):
	headings = []
	numCalls = 0
	startTime = time.time()
	while textRange:
		numItemsFound = c_int()
		foundLevels = SAFEARRAY(c_int)()
		foundLabels = SAFEARRAY(BSTR)()
		foundRanges = SAFEARRAY(POINTER(UIAHandler.IUIAutomationTextRange))()
		remainingTextRange = POINTER(UIAHandler.IUIAutomationTextRange)()
		_dll.findHeadingsInTextRange(textRange, maxItems, backwards, level, byref(numItemsFound), byref(foundLevels), byref(foundLabels), byref(foundRanges), byref(remainingTextRange));
		numCalls += 1
		headings.extend((foundLevels[0][i],foundLabels[0][i],foundRanges[0][i].QueryInterface(UIAHandler.IUIAutomationTextRange)) for i in range(numItemsFound.value))
		textRange = remainingTextRange
		if textRange:
			log.info("Fetching more headings...")
	endTime = time.time()
	log.info(f"Fetched {len(headings)} headings requiring {numCalls} calls in {endTime-startTime} seconds")
	return headings
