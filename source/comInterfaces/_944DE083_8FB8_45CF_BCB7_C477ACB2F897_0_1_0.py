# -*- coding: mbcs -*-
typelib_path = 'UIAutomationCore.dll'
_lcid = 0 # change this if required
from ctypes import *
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from ctypes import HRESULT
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes.automation import _midlSAFEARRAY
from ctypes.wintypes import tagPOINT
from comtypes.automation import VARIANT
from ctypes.wintypes import tagRECT
from comtypes import BSTR
from comtypes import IUnknown
from comtypes.automation import IDispatch
WSTRING = c_wchar_p
from comtypes import CoClass


class IUIAutomationTableItemPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0B964EB3-EF2E-4464-9C79-61D61737A27E}')
    _idlflags_ = []
class IUIAutomationElementArray(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{14314595-B4BC-4055-95F2-58F2E42C9855}')
    _idlflags_ = []
IUIAutomationTableItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetCurrentRowHeaderItems',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentColumnHeaderItems',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedRowHeaderItems',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedColumnHeaderItems',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
]
################################################################
## code template for IUIAutomationTableItemPattern implementation
##class IUIAutomationTableItemPattern_Impl(object):
##    def GetCurrentRowHeaderItems(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentColumnHeaderItems(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedRowHeaderItems(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedColumnHeaderItems(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationTogglePattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{94CF8058-9B8D-4AB9-8BFD-4CD0A33C8C70}')
    _idlflags_ = []

# values for enumeration 'ToggleState'
ToggleState_Off = 0
ToggleState_On = 1
ToggleState_Indeterminate = 2
ToggleState = c_int # enum
IUIAutomationTogglePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Toggle'),
    COMMETHOD(['propget'], HRESULT, 'CurrentToggleState',
              ( ['out', 'retval'], POINTER(ToggleState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedToggleState',
              ( ['out', 'retval'], POINTER(ToggleState), 'retVal' )),
]
################################################################
## code template for IUIAutomationTogglePattern implementation
##class IUIAutomationTogglePattern_Impl(object):
##    def Toggle(self):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentToggleState(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedToggleState(self):
##        '-no docstring-'
##        #return retVal
##


# values for enumeration 'ZoomUnit'
ZoomUnit_NoAmount = 0
ZoomUnit_LargeDecrement = 1
ZoomUnit_SmallDecrement = 2
ZoomUnit_LargeIncrement = 3
ZoomUnit_SmallIncrement = 4
ZoomUnit = c_int # enum
class IUIAutomation(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{30CBE57D-D9D0-452A-AB13-7AC5AC4825EE}')
    _idlflags_ = []
class IUIAutomation2(IUIAutomation):
    _case_insensitive_ = True
    _iid_ = GUID('{34723AFF-0C9D-49D0-9896-7AB52DF8CD8A}')
    _idlflags_ = []
class IUIAutomationElement(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{D22108AA-8AC5-49A5-837B-37BBB3D7591E}')
    _idlflags_ = []
class IUIAutomationCacheRequest(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{B32A92B5-BC25-4078-9C08-D7EE95C48E03}')
    _idlflags_ = []
class IUIAutomationCondition(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{352FFBA8-0973-437C-A61F-F64CAFD81DF9}')
    _idlflags_ = []
class IUIAutomationTreeWalker(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{4042C624-389C-4AFC-A630-9DF854A541FC}')
    _idlflags_ = []

# values for enumeration 'PropertyConditionFlags'
PropertyConditionFlags_None = 0
PropertyConditionFlags_IgnoreCase = 1
PropertyConditionFlags_MatchSubstring = 2
PropertyConditionFlags = c_int # enum

# values for enumeration 'TreeScope'
TreeScope_None = 0
TreeScope_Element = 1
TreeScope_Children = 2
TreeScope_Descendants = 4
TreeScope_Parent = 8
TreeScope_Ancestors = 16
TreeScope_Subtree = 7
TreeScope = c_int # enum
class IUIAutomationEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{146C3C17-F12E-4E22-8C27-F894B9B79C69}')
    _idlflags_ = ['oleautomation']
class IUIAutomationPropertyChangedEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{40CD37D4-C756-4B0C-8C6F-BDDFEEB13B50}')
    _idlflags_ = ['oleautomation']
class IUIAutomationStructureChangedEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{E81D1B4E-11C5-42F8-9754-E7036C79F054}')
    _idlflags_ = ['oleautomation']
class IUIAutomationFocusChangedEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{C270F6B5-5C69-4290-9745-7A7F97169468}')
    _idlflags_ = ['oleautomation']
class IUIAutomationProxyFactory(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{85B94ECD-849D-42B6-B94D-D6DB23FDF5A4}')
    _idlflags_ = []
class IUIAutomationProxyFactoryEntry(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{D50E472E-B64B-490C-BCA1-D30696F9F289}')
    _idlflags_ = []
class IUIAutomationProxyFactoryMapping(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{09E31E18-872D-4873-93D1-1E541EC133FD}')
    _idlflags_ = []
class IAccessible(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{618736E0-3C3D-11CF-810C-00AA00389B71}')
    _idlflags_ = ['hidden', 'dual', 'oleautomation']
IUIAutomation._methods_ = [
    COMMETHOD([], HRESULT, 'CompareElements',
              ( ['in'], POINTER(IUIAutomationElement), 'el1' ),
              ( ['in'], POINTER(IUIAutomationElement), 'el2' ),
              ( ['out', 'retval'], POINTER(c_int), 'areSame' )),
    COMMETHOD([], HRESULT, 'CompareRuntimeIds',
              ( ['in'], _midlSAFEARRAY(c_int), 'runtimeId1' ),
              ( ['in'], _midlSAFEARRAY(c_int), 'runtimeId2' ),
              ( ['out', 'retval'], POINTER(c_int), 'areSame' )),
    COMMETHOD([], HRESULT, 'GetRootElement',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'root' )),
    COMMETHOD([], HRESULT, 'ElementFromHandle',
              ( ['in'], c_void_p, 'hwnd' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'ElementFromPoint',
              ( ['in'], tagPOINT, 'pt' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'GetFocusedElement',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'GetRootElementBuildCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'root' )),
    COMMETHOD([], HRESULT, 'ElementFromHandleBuildCache',
              ( ['in'], c_void_p, 'hwnd' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'ElementFromPointBuildCache',
              ( ['in'], tagPOINT, 'pt' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'GetFocusedElementBuildCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'CreateTreeWalker',
              ( ['in'], POINTER(IUIAutomationCondition), 'pCondition' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'ControlViewWalker',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'ContentViewWalker',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'RawViewWalker',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTreeWalker)), 'walker' )),
    COMMETHOD(['propget'], HRESULT, 'RawViewCondition',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
    COMMETHOD(['propget'], HRESULT, 'ControlViewCondition',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
    COMMETHOD(['propget'], HRESULT, 'ContentViewCondition',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
    COMMETHOD([], HRESULT, 'CreateCacheRequest',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCacheRequest)), 'cacheRequest' )),
    COMMETHOD([], HRESULT, 'CreateTrueCondition',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateFalseCondition',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreatePropertyCondition',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'value' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreatePropertyConditionEx',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'value' ),
              ( ['in'], PropertyConditionFlags, 'flags' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateAndCondition',
              ( ['in'], POINTER(IUIAutomationCondition), 'condition1' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition2' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateAndConditionFromArray',
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateAndConditionFromNativeArray',
              ( ['in'], POINTER(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['in'], c_int, 'conditionCount' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateOrCondition',
              ( ['in'], POINTER(IUIAutomationCondition), 'condition1' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition2' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateOrConditionFromArray',
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateOrConditionFromNativeArray',
              ( ['in'], POINTER(POINTER(IUIAutomationCondition)), 'conditions' ),
              ( ['in'], c_int, 'conditionCount' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'CreateNotCondition',
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'newCondition' )),
    COMMETHOD([], HRESULT, 'AddAutomationEventHandler',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveAutomationEventHandler',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddPropertyChangedEventHandlerNativeArray',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationPropertyChangedEventHandler), 'handler' ),
              ( ['in'], POINTER(c_int), 'propertyArray' ),
              ( ['in'], c_int, 'propertyCount' )),
    COMMETHOD([], HRESULT, 'AddPropertyChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationPropertyChangedEventHandler), 'handler' ),
              ( ['in'], _midlSAFEARRAY(c_int), 'propertyArray' )),
    COMMETHOD([], HRESULT, 'RemovePropertyChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationPropertyChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddStructureChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationStructureChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveStructureChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationStructureChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddFocusChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationFocusChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveFocusChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationFocusChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveAllEventHandlers'),
    COMMETHOD([], HRESULT, 'IntNativeArrayToSafeArray',
              ( ['in'], POINTER(c_int), 'array' ),
              ( ['in'], c_int, 'arrayCount' ),
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'safeArray' )),
    COMMETHOD([], HRESULT, 'IntSafeArrayToNativeArray',
              ( ['in'], _midlSAFEARRAY(c_int), 'intArray' ),
              ( ['out'], POINTER(POINTER(c_int)), 'array' ),
              ( ['out', 'retval'], POINTER(c_int), 'arrayCount' )),
    COMMETHOD([], HRESULT, 'RectToVariant',
              ( ['in'], tagRECT, 'rc' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'var' )),
    COMMETHOD([], HRESULT, 'VariantToRect',
              ( ['in'], VARIANT, 'var' ),
              ( ['out', 'retval'], POINTER(tagRECT), 'rc' )),
    COMMETHOD([], HRESULT, 'SafeArrayToRectNativeArray',
              ( ['in'], _midlSAFEARRAY(c_double), 'rects' ),
              ( ['out'], POINTER(POINTER(tagRECT)), 'rectArray' ),
              ( ['out', 'retval'], POINTER(c_int), 'rectArrayCount' )),
    COMMETHOD([], HRESULT, 'CreateProxyFactoryEntry',
              ( ['in'], POINTER(IUIAutomationProxyFactory), 'factory' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationProxyFactoryEntry)), 'factoryEntry' )),
    COMMETHOD(['propget'], HRESULT, 'ProxyFactoryMapping',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationProxyFactoryMapping)), 'factoryMapping' )),
    COMMETHOD([], HRESULT, 'GetPropertyProgrammaticName',
              ( ['in'], c_int, 'property' ),
              ( ['out', 'retval'], POINTER(BSTR), 'name' )),
    COMMETHOD([], HRESULT, 'GetPatternProgrammaticName',
              ( ['in'], c_int, 'pattern' ),
              ( ['out', 'retval'], POINTER(BSTR), 'name' )),
    COMMETHOD([], HRESULT, 'PollForPotentialSupportedPatterns',
              ( ['in'], POINTER(IUIAutomationElement), 'pElement' ),
              ( ['out'], POINTER(_midlSAFEARRAY(c_int)), 'patternIds' ),
              ( ['out'], POINTER(_midlSAFEARRAY(BSTR)), 'patternNames' )),
    COMMETHOD([], HRESULT, 'PollForPotentialSupportedProperties',
              ( ['in'], POINTER(IUIAutomationElement), 'pElement' ),
              ( ['out'], POINTER(_midlSAFEARRAY(c_int)), 'propertyIds' ),
              ( ['out'], POINTER(_midlSAFEARRAY(BSTR)), 'propertyNames' )),
    COMMETHOD([], HRESULT, 'CheckNotSupported',
              ( ['in'], VARIANT, 'value' ),
              ( ['out', 'retval'], POINTER(c_int), 'isNotSupported' )),
    COMMETHOD(['propget'], HRESULT, 'ReservedNotSupportedValue',
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'notSupportedValue' )),
    COMMETHOD(['propget'], HRESULT, 'ReservedMixedAttributeValue',
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'mixedAttributeValue' )),
    COMMETHOD([], HRESULT, 'ElementFromIAccessible',
              ( ['in'], POINTER(IAccessible), 'accessible' ),
              ( ['in'], c_int, 'childId' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD([], HRESULT, 'ElementFromIAccessibleBuildCache',
              ( ['in'], POINTER(IAccessible), 'accessible' ),
              ( ['in'], c_int, 'childId' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
]
################################################################
## code template for IUIAutomation implementation
##class IUIAutomation_Impl(object):
##    def CompareElements(self, el1, el2):
##        '-no docstring-'
##        #return areSame
##
##    def CompareRuntimeIds(self, runtimeId1, runtimeId2):
##        '-no docstring-'
##        #return areSame
##
##    def GetRootElement(self):
##        '-no docstring-'
##        #return root
##
##    def ElementFromHandle(self, hwnd):
##        '-no docstring-'
##        #return element
##
##    def ElementFromPoint(self, pt):
##        '-no docstring-'
##        #return element
##
##    def GetFocusedElement(self):
##        '-no docstring-'
##        #return element
##
##    def GetRootElementBuildCache(self, cacheRequest):
##        '-no docstring-'
##        #return root
##
##    def ElementFromHandleBuildCache(self, hwnd, cacheRequest):
##        '-no docstring-'
##        #return element
##
##    def ElementFromPointBuildCache(self, pt, cacheRequest):
##        '-no docstring-'
##        #return element
##
##    def GetFocusedElementBuildCache(self, cacheRequest):
##        '-no docstring-'
##        #return element
##
##    def CreateTreeWalker(self, pCondition):
##        '-no docstring-'
##        #return walker
##
##    @property
##    def ControlViewWalker(self):
##        '-no docstring-'
##        #return walker
##
##    @property
##    def ContentViewWalker(self):
##        '-no docstring-'
##        #return walker
##
##    @property
##    def RawViewWalker(self):
##        '-no docstring-'
##        #return walker
##
##    @property
##    def RawViewCondition(self):
##        '-no docstring-'
##        #return condition
##
##    @property
##    def ControlViewCondition(self):
##        '-no docstring-'
##        #return condition
##
##    @property
##    def ContentViewCondition(self):
##        '-no docstring-'
##        #return condition
##
##    def CreateCacheRequest(self):
##        '-no docstring-'
##        #return cacheRequest
##
##    def CreateTrueCondition(self):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateFalseCondition(self):
##        '-no docstring-'
##        #return newCondition
##
##    def CreatePropertyCondition(self, propertyId, value):
##        '-no docstring-'
##        #return newCondition
##
##    def CreatePropertyConditionEx(self, propertyId, value, flags):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateAndCondition(self, condition1, condition2):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateAndConditionFromArray(self, conditions):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateAndConditionFromNativeArray(self, conditions, conditionCount):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateOrCondition(self, condition1, condition2):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateOrConditionFromArray(self, conditions):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateOrConditionFromNativeArray(self, conditions, conditionCount):
##        '-no docstring-'
##        #return newCondition
##
##    def CreateNotCondition(self, condition):
##        '-no docstring-'
##        #return newCondition
##
##    def AddAutomationEventHandler(self, eventId, element, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveAutomationEventHandler(self, eventId, element, handler):
##        '-no docstring-'
##        #return 
##
##    def AddPropertyChangedEventHandlerNativeArray(self, element, scope, cacheRequest, handler, propertyArray, propertyCount):
##        '-no docstring-'
##        #return 
##
##    def AddPropertyChangedEventHandler(self, element, scope, cacheRequest, handler, propertyArray):
##        '-no docstring-'
##        #return 
##
##    def RemovePropertyChangedEventHandler(self, element, handler):
##        '-no docstring-'
##        #return 
##
##    def AddStructureChangedEventHandler(self, element, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveStructureChangedEventHandler(self, element, handler):
##        '-no docstring-'
##        #return 
##
##    def AddFocusChangedEventHandler(self, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveFocusChangedEventHandler(self, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveAllEventHandlers(self):
##        '-no docstring-'
##        #return 
##
##    def IntNativeArrayToSafeArray(self, array, arrayCount):
##        '-no docstring-'
##        #return safeArray
##
##    def IntSafeArrayToNativeArray(self, intArray):
##        '-no docstring-'
##        #return array, arrayCount
##
##    def RectToVariant(self, rc):
##        '-no docstring-'
##        #return var
##
##    def VariantToRect(self, var):
##        '-no docstring-'
##        #return rc
##
##    def SafeArrayToRectNativeArray(self, rects):
##        '-no docstring-'
##        #return rectArray, rectArrayCount
##
##    def CreateProxyFactoryEntry(self, factory):
##        '-no docstring-'
##        #return factoryEntry
##
##    @property
##    def ProxyFactoryMapping(self):
##        '-no docstring-'
##        #return factoryMapping
##
##    def GetPropertyProgrammaticName(self, property):
##        '-no docstring-'
##        #return name
##
##    def GetPatternProgrammaticName(self, pattern):
##        '-no docstring-'
##        #return name
##
##    def PollForPotentialSupportedPatterns(self, pElement):
##        '-no docstring-'
##        #return patternIds, patternNames
##
##    def PollForPotentialSupportedProperties(self, pElement):
##        '-no docstring-'
##        #return propertyIds, propertyNames
##
##    def CheckNotSupported(self, value):
##        '-no docstring-'
##        #return isNotSupported
##
##    @property
##    def ReservedNotSupportedValue(self):
##        '-no docstring-'
##        #return notSupportedValue
##
##    @property
##    def ReservedMixedAttributeValue(self):
##        '-no docstring-'
##        #return mixedAttributeValue
##
##    def ElementFromIAccessible(self, accessible, childId):
##        '-no docstring-'
##        #return element
##
##    def ElementFromIAccessibleBuildCache(self, accessible, childId, cacheRequest):
##        '-no docstring-'
##        #return element
##

IUIAutomation2._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'AutoSetFocus',
              ( ['out', 'retval'], POINTER(c_int), 'AutoSetFocus' )),
    COMMETHOD(['propput'], HRESULT, 'AutoSetFocus',
              ( ['in'], c_int, 'AutoSetFocus' )),
    COMMETHOD(['propget'], HRESULT, 'ConnectionTimeout',
              ( ['out', 'retval'], POINTER(c_ulong), 'timeout' )),
    COMMETHOD(['propput'], HRESULT, 'ConnectionTimeout',
              ( ['in'], c_ulong, 'timeout' )),
    COMMETHOD(['propget'], HRESULT, 'TransactionTimeout',
              ( ['out', 'retval'], POINTER(c_ulong), 'timeout' )),
    COMMETHOD(['propput'], HRESULT, 'TransactionTimeout',
              ( ['in'], c_ulong, 'timeout' )),
]
################################################################
## code template for IUIAutomation2 implementation
##class IUIAutomation2_Impl(object):
##    def _get(self):
##        '-no docstring-'
##        #return AutoSetFocus
##    def _set(self, AutoSetFocus):
##        '-no docstring-'
##    AutoSetFocus = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return timeout
##    def _set(self, timeout):
##        '-no docstring-'
##    ConnectionTimeout = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return timeout
##    def _set(self, timeout):
##        '-no docstring-'
##    TransactionTimeout = property(_get, _set, doc = _set.__doc__)
##

class IUIAutomationTextChildPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{6552B038-AE05-40C8-ABFD-AA08352AAB86}')
    _idlflags_ = []
class IUIAutomationTextRange(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A543CC6A-F4AE-494B-8239-C814481187A8}')
    _idlflags_ = []
IUIAutomationTextChildPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'TextContainer',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'container' )),
    COMMETHOD(['propget'], HRESULT, 'TextRange',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
]
################################################################
## code template for IUIAutomationTextChildPattern implementation
##class IUIAutomationTextChildPattern_Impl(object):
##    @property
##    def TextContainer(self):
##        '-no docstring-'
##        #return container
##
##    @property
##    def TextRange(self):
##        '-no docstring-'
##        #return range
##

IAccessible._methods_ = [
    COMMETHOD([dispid(-5000), 'hidden', 'propget'], HRESULT, 'accParent',
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppdispParent' )),
    COMMETHOD([dispid(-5001), 'hidden', 'propget'], HRESULT, 'accChildCount',
              ( ['out', 'retval'], POINTER(c_int), 'pcountChildren' )),
    COMMETHOD([dispid(-5002), 'hidden', 'propget'], HRESULT, 'accChild',
              ( ['in'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppdispChild' )),
    COMMETHOD([dispid(-5003), 'hidden', 'propget'], HRESULT, 'accName',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(BSTR), 'pszName' )),
    COMMETHOD([dispid(-5004), 'hidden', 'propget'], HRESULT, 'accValue',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(BSTR), 'pszValue' )),
    COMMETHOD([dispid(-5005), 'hidden', 'propget'], HRESULT, 'accDescription',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(BSTR), 'pszDescription' )),
    COMMETHOD([dispid(-5006), 'hidden', 'propget'], HRESULT, 'accRole',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'pvarRole' )),
    COMMETHOD([dispid(-5007), 'hidden', 'propget'], HRESULT, 'accState',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'pvarState' )),
    COMMETHOD([dispid(-5008), 'hidden', 'propget'], HRESULT, 'accHelp',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(BSTR), 'pszHelp' )),
    COMMETHOD([dispid(-5009), 'hidden', 'propget'], HRESULT, 'accHelpTopic',
              ( ['out'], POINTER(BSTR), 'pszHelpFile' ),
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(c_int), 'pidTopic' )),
    COMMETHOD([dispid(-5010), 'hidden', 'propget'], HRESULT, 'accKeyboardShortcut',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(BSTR), 'pszKeyboardShortcut' )),
    COMMETHOD([dispid(-5011), 'hidden', 'propget'], HRESULT, 'accFocus',
              ( ['out', 'retval'], POINTER(VARIANT), 'pvarChild' )),
    COMMETHOD([dispid(-5012), 'hidden', 'propget'], HRESULT, 'accSelection',
              ( ['out', 'retval'], POINTER(VARIANT), 'pvarChildren' )),
    COMMETHOD([dispid(-5013), 'hidden', 'propget'], HRESULT, 'accDefaultAction',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['out', 'retval'], POINTER(BSTR), 'pszDefaultAction' )),
    COMMETHOD([dispid(-5014), 'hidden'], HRESULT, 'accSelect',
              ( ['in'], c_int, 'flagsSelect' ),
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5015), 'hidden'], HRESULT, 'accLocation',
              ( ['out'], POINTER(c_int), 'pxLeft' ),
              ( ['out'], POINTER(c_int), 'pyTop' ),
              ( ['out'], POINTER(c_int), 'pcxWidth' ),
              ( ['out'], POINTER(c_int), 'pcyHeight' ),
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5016), 'hidden'], HRESULT, 'accNavigate',
              ( ['in'], c_int, 'navDir' ),
              ( ['in', 'optional'], VARIANT, 'varStart' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'pvarEndUpAt' )),
    COMMETHOD([dispid(-5017), 'hidden'], HRESULT, 'accHitTest',
              ( ['in'], c_int, 'xLeft' ),
              ( ['in'], c_int, 'yTop' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'pvarChild' )),
    COMMETHOD([dispid(-5018), 'hidden'], HRESULT, 'accDoDefaultAction',
              ( ['in', 'optional'], VARIANT, 'varChild' )),
    COMMETHOD([dispid(-5003), 'hidden', 'propput'], HRESULT, 'accName',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['in'], BSTR, 'pszName' )),
    COMMETHOD([dispid(-5004), 'hidden', 'propput'], HRESULT, 'accValue',
              ( ['in', 'optional'], VARIANT, 'varChild' ),
              ( ['in'], BSTR, 'pszValue' )),
]
################################################################
## code template for IAccessible implementation
##class IAccessible_Impl(object):
##    @property
##    def accParent(self):
##        '-no docstring-'
##        #return ppdispParent
##
##    @property
##    def accChildCount(self):
##        '-no docstring-'
##        #return pcountChildren
##
##    @property
##    def accChild(self, varChild):
##        '-no docstring-'
##        #return ppdispChild
##
##    def _get(self, varChild):
##        '-no docstring-'
##        #return pszName
##    def _set(self, varChild, pszName):
##        '-no docstring-'
##    accName = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self, varChild):
##        '-no docstring-'
##        #return pszValue
##    def _set(self, varChild, pszValue):
##        '-no docstring-'
##    accValue = property(_get, _set, doc = _set.__doc__)
##
##    @property
##    def accDescription(self, varChild):
##        '-no docstring-'
##        #return pszDescription
##
##    @property
##    def accRole(self, varChild):
##        '-no docstring-'
##        #return pvarRole
##
##    @property
##    def accState(self, varChild):
##        '-no docstring-'
##        #return pvarState
##
##    @property
##    def accHelp(self, varChild):
##        '-no docstring-'
##        #return pszHelp
##
##    @property
##    def accHelpTopic(self, varChild):
##        '-no docstring-'
##        #return pszHelpFile, pidTopic
##
##    @property
##    def accKeyboardShortcut(self, varChild):
##        '-no docstring-'
##        #return pszKeyboardShortcut
##
##    @property
##    def accFocus(self):
##        '-no docstring-'
##        #return pvarChild
##
##    @property
##    def accSelection(self):
##        '-no docstring-'
##        #return pvarChildren
##
##    @property
##    def accDefaultAction(self, varChild):
##        '-no docstring-'
##        #return pszDefaultAction
##
##    def accSelect(self, flagsSelect, varChild):
##        '-no docstring-'
##        #return 
##
##    def accLocation(self, varChild):
##        '-no docstring-'
##        #return pxLeft, pyTop, pcxWidth, pcyHeight
##
##    def accNavigate(self, navDir, varStart):
##        '-no docstring-'
##        #return pvarEndUpAt
##
##    def accHitTest(self, xLeft, yTop):
##        '-no docstring-'
##        #return pvarChild
##
##    def accDoDefaultAction(self, varChild):
##        '-no docstring-'
##        #return 
##

class IUIAutomationTransformPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A9B55844-A55D-4EF0-926D-569C16FF89BB}')
    _idlflags_ = []
IUIAutomationTransformPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Move',
              ( ['in'], c_double, 'x' ),
              ( ['in'], c_double, 'y' )),
    COMMETHOD([], HRESULT, 'Resize',
              ( ['in'], c_double, 'width' ),
              ( ['in'], c_double, 'height' )),
    COMMETHOD([], HRESULT, 'Rotate',
              ( ['in'], c_double, 'degrees' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanMove',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanResize',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanRotate',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanMove',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanResize',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanRotate',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationTransformPattern implementation
##class IUIAutomationTransformPattern_Impl(object):
##    def Move(self, x, y):
##        '-no docstring-'
##        #return 
##
##    def Resize(self, width, height):
##        '-no docstring-'
##        #return 
##
##    def Rotate(self, degrees):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentCanMove(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentCanResize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentCanRotate(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCanMove(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCanResize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCanRotate(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationDragPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{1DC7B570-1F54-4BAD-BCDA-D36A722FB7BD}')
    _idlflags_ = []
IUIAutomationDragPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentIsGrabbed',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsGrabbed',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDropEffect',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDropEffect',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDropEffects',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(BSTR)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDropEffects',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(BSTR)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentGrabbedItems',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedGrabbedItems',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
]
################################################################
## code template for IUIAutomationDragPattern implementation
##class IUIAutomationDragPattern_Impl(object):
##    @property
##    def CurrentIsGrabbed(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsGrabbed(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentDropEffect(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedDropEffect(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentDropEffects(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedDropEffects(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentGrabbedItems(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedGrabbedItems(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomation3(IUIAutomation2):
    _case_insensitive_ = True
    _iid_ = GUID('{73D768DA-9B51-4B89-936E-C209290973E7}')
    _idlflags_ = []
class IUIAutomation4(IUIAutomation3):
    _case_insensitive_ = True
    _iid_ = GUID('{1189C02A-05F8-4319-8E21-E817E3DB2860}')
    _idlflags_ = []

# values for enumeration 'TextEditChangeType'
TextEditChangeType_None = 0
TextEditChangeType_AutoCorrect = 1
TextEditChangeType_Composition = 2
TextEditChangeType_CompositionFinalized = 3
TextEditChangeType_AutoComplete = 4
TextEditChangeType = c_int # enum
class IUIAutomationTextEditTextChangedEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{92FAA680-E704-4156-931A-E32D5BB38F3F}')
    _idlflags_ = ['oleautomation']
IUIAutomation3._methods_ = [
    COMMETHOD([], HRESULT, 'AddTextEditTextChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], TextEditChangeType, 'TextEditChangeType' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationTextEditTextChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveTextEditTextChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationTextEditTextChangedEventHandler), 'handler' )),
]
################################################################
## code template for IUIAutomation3 implementation
##class IUIAutomation3_Impl(object):
##    def AddTextEditTextChangedEventHandler(self, element, scope, TextEditChangeType, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveTextEditTextChangedEventHandler(self, element, handler):
##        '-no docstring-'
##        #return 
##

class IUIAutomationChangesEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{58EDCA55-2C3E-4980-B1B9-56C17F27A2A0}')
    _idlflags_ = ['oleautomation']
IUIAutomation4._methods_ = [
    COMMETHOD([], HRESULT, 'AddChangesEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(c_int), 'changeTypes' ),
              ( ['in'], c_int, 'changesCount' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'pCacheRequest' ),
              ( ['in'], POINTER(IUIAutomationChangesEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveChangesEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationChangesEventHandler), 'handler' )),
]
################################################################
## code template for IUIAutomation4 implementation
##class IUIAutomation4_Impl(object):
##    def AddChangesEventHandler(self, element, scope, changeTypes, changesCount, pCacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveChangesEventHandler(self, element, handler):
##        '-no docstring-'
##        #return 
##

class IUIAutomationDropTargetPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{69A095F7-EEE4-430E-A46B-FB73B1AE39A5}')
    _idlflags_ = []
IUIAutomationDropTargetPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentDropTargetEffect',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDropTargetEffect',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDropTargetEffects',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(BSTR)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDropTargetEffects',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(BSTR)), 'retVal' )),
]
################################################################
## code template for IUIAutomationDropTargetPattern implementation
##class IUIAutomationDropTargetPattern_Impl(object):
##    @property
##    def CurrentDropTargetEffect(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedDropTargetEffect(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentDropTargetEffects(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedDropTargetEffects(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationValuePattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A94CD8B1-0844-4CD6-9D2D-640537AB39E9}')
    _idlflags_ = []
IUIAutomationValuePattern._methods_ = [
    COMMETHOD([], HRESULT, 'SetValue',
              ( ['in'], BSTR, 'val' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentValue',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsReadOnly',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedValue',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsReadOnly',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationValuePattern implementation
##class IUIAutomationValuePattern_Impl(object):
##    def SetValue(self, val):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentValue(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsReadOnly(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedValue(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsReadOnly(self):
##        '-no docstring-'
##        #return retVal
##


# values for enumeration 'NavigateDirection'
NavigateDirection_Parent = 0
NavigateDirection_NextSibling = 1
NavigateDirection_PreviousSibling = 2
NavigateDirection_FirstChild = 3
NavigateDirection_LastChild = 4
NavigateDirection = c_int # enum
class IUIAutomationElement2(IUIAutomationElement):
    _case_insensitive_ = True
    _iid_ = GUID('{6749C683-F70D-4487-A698-5F79D55290D6}')
    _idlflags_ = []

# values for enumeration 'OrientationType'
OrientationType_None = 0
OrientationType_Horizontal = 1
OrientationType_Vertical = 2
OrientationType = c_int # enum
IUIAutomationElement._methods_ = [
    COMMETHOD([], HRESULT, 'SetFocus'),
    COMMETHOD([], HRESULT, 'GetRuntimeId',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'runtimeId' )),
    COMMETHOD([], HRESULT, 'FindFirst',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'found' )),
    COMMETHOD([], HRESULT, 'FindAll',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'found' )),
    COMMETHOD([], HRESULT, 'FindFirstBuildCache',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'found' )),
    COMMETHOD([], HRESULT, 'FindAllBuildCache',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'found' )),
    COMMETHOD([], HRESULT, 'BuildUpdatedCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'updatedElement' )),
    COMMETHOD([], HRESULT, 'GetCurrentPropertyValue',
              ( ['in'], c_int, 'propertyId' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentPropertyValueEx',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], c_int, 'ignoreDefaultValue' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedPropertyValue',
              ( ['in'], c_int, 'propertyId' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedPropertyValueEx',
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], c_int, 'ignoreDefaultValue' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentPatternAs',
              ( ['in'], c_int, 'patternId' ),
              ( ['in'], POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'riid' ),
              ( ['out', 'retval'], POINTER(c_void_p), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCachedPatternAs',
              ( ['in'], c_int, 'patternId' ),
              ( ['in'], POINTER(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.GUID), 'riid' ),
              ( ['out', 'retval'], POINTER(c_void_p), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCurrentPattern',
              ( ['in'], c_int, 'patternId' ),
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCachedPattern',
              ( ['in'], c_int, 'patternId' ),
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'patternObject' )),
    COMMETHOD([], HRESULT, 'GetCachedParent',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'parent' )),
    COMMETHOD([], HRESULT, 'GetCachedChildren',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'children' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentProcessId',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentControlType',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLocalizedControlType',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAcceleratorKey',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAccessKey',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHasKeyboardFocus',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsKeyboardFocusable',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsEnabled',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAutomationId',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentClassName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHelpText',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCulture',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsControlElement',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsContentElement',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsPassword',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentNativeWindowHandle',
              ( ['out', 'retval'], POINTER(c_void_p), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentItemType',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsOffscreen',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentOrientation',
              ( ['out', 'retval'], POINTER(OrientationType), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFrameworkId',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsRequiredForForm',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentItemStatus',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentBoundingRectangle',
              ( ['out', 'retval'], POINTER(tagRECT), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLabeledBy',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAriaRole',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAriaProperties',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsDataValidForForm',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentControllerFor',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDescribedBy',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFlowsTo',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentProviderDescription',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedProcessId',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedControlType',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLocalizedControlType',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAcceleratorKey',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAccessKey',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHasKeyboardFocus',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsKeyboardFocusable',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsEnabled',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAutomationId',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedClassName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHelpText',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCulture',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsControlElement',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsContentElement',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsPassword',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedNativeWindowHandle',
              ( ['out', 'retval'], POINTER(c_void_p), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedItemType',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsOffscreen',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedOrientation',
              ( ['out', 'retval'], POINTER(OrientationType), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFrameworkId',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsRequiredForForm',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedItemStatus',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedBoundingRectangle',
              ( ['out', 'retval'], POINTER(tagRECT), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLabeledBy',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAriaRole',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAriaProperties',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsDataValidForForm',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedControllerFor',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDescribedBy',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFlowsTo',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedProviderDescription',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetClickablePoint',
              ( ['out'], POINTER(tagPOINT), 'clickable' ),
              ( ['out', 'retval'], POINTER(c_int), 'gotClickable' )),
]
################################################################
## code template for IUIAutomationElement implementation
##class IUIAutomationElement_Impl(object):
##    def SetFocus(self):
##        '-no docstring-'
##        #return 
##
##    def GetRuntimeId(self):
##        '-no docstring-'
##        #return runtimeId
##
##    def FindFirst(self, scope, condition):
##        '-no docstring-'
##        #return found
##
##    def FindAll(self, scope, condition):
##        '-no docstring-'
##        #return found
##
##    def FindFirstBuildCache(self, scope, condition, cacheRequest):
##        '-no docstring-'
##        #return found
##
##    def FindAllBuildCache(self, scope, condition, cacheRequest):
##        '-no docstring-'
##        #return found
##
##    def BuildUpdatedCache(self, cacheRequest):
##        '-no docstring-'
##        #return updatedElement
##
##    def GetCurrentPropertyValue(self, propertyId):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentPropertyValueEx(self, propertyId, ignoreDefaultValue):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedPropertyValue(self, propertyId):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedPropertyValueEx(self, propertyId, ignoreDefaultValue):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentPatternAs(self, patternId, riid):
##        '-no docstring-'
##        #return patternObject
##
##    def GetCachedPatternAs(self, patternId, riid):
##        '-no docstring-'
##        #return patternObject
##
##    def GetCurrentPattern(self, patternId):
##        '-no docstring-'
##        #return patternObject
##
##    def GetCachedPattern(self, patternId):
##        '-no docstring-'
##        #return patternObject
##
##    def GetCachedParent(self):
##        '-no docstring-'
##        #return parent
##
##    def GetCachedChildren(self):
##        '-no docstring-'
##        #return children
##
##    @property
##    def CurrentProcessId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentControlType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentLocalizedControlType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAcceleratorKey(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAccessKey(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentHasKeyboardFocus(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsKeyboardFocusable(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsEnabled(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAutomationId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentClassName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentHelpText(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentCulture(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsControlElement(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsContentElement(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsPassword(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentNativeWindowHandle(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentItemType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsOffscreen(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentOrientation(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentFrameworkId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsRequiredForForm(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentItemStatus(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentBoundingRectangle(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentLabeledBy(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAriaRole(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAriaProperties(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsDataValidForForm(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentControllerFor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentDescribedBy(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentFlowsTo(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentProviderDescription(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedProcessId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedControlType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLocalizedControlType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAcceleratorKey(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAccessKey(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedHasKeyboardFocus(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsKeyboardFocusable(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsEnabled(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAutomationId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedClassName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedHelpText(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCulture(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsControlElement(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsContentElement(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsPassword(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedNativeWindowHandle(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedItemType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsOffscreen(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedOrientation(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFrameworkId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsRequiredForForm(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedItemStatus(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedBoundingRectangle(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLabeledBy(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAriaRole(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAriaProperties(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsDataValidForForm(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedControllerFor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedDescribedBy(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFlowsTo(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedProviderDescription(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetClickablePoint(self):
##        '-no docstring-'
##        #return clickable, gotClickable
##


# values for enumeration 'LiveSetting'
Off = 0
Polite = 1
Assertive = 2
LiveSetting = c_int # enum
IUIAutomationElement2._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentOptimizeForVisualContent',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedOptimizeForVisualContent',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLiveSetting',
              ( ['out', 'retval'], POINTER(LiveSetting), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLiveSetting',
              ( ['out', 'retval'], POINTER(LiveSetting), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFlowsFrom',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFlowsFrom',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
]
################################################################
## code template for IUIAutomationElement2 implementation
##class IUIAutomationElement2_Impl(object):
##    @property
##    def CurrentOptimizeForVisualContent(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedOptimizeForVisualContent(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentLiveSetting(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLiveSetting(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentFlowsFrom(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFlowsFrom(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationWindowPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0FAEF453-9208-43EF-BBB2-3B485177864F}')
    _idlflags_ = []

# values for enumeration 'WindowVisualState'
WindowVisualState_Normal = 0
WindowVisualState_Maximized = 1
WindowVisualState_Minimized = 2
WindowVisualState = c_int # enum

# values for enumeration 'WindowInteractionState'
WindowInteractionState_Running = 0
WindowInteractionState_Closing = 1
WindowInteractionState_ReadyForUserInteraction = 2
WindowInteractionState_BlockedByModalWindow = 3
WindowInteractionState_NotResponding = 4
WindowInteractionState = c_int # enum
IUIAutomationWindowPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Close'),
    COMMETHOD([], HRESULT, 'WaitForInputIdle',
              ( ['in'], c_int, 'milliseconds' ),
              ( ['out', 'retval'], POINTER(c_int), 'success' )),
    COMMETHOD([], HRESULT, 'SetWindowVisualState',
              ( ['in'], WindowVisualState, 'state' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanMaximize',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanMinimize',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsModal',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsTopmost',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentWindowVisualState',
              ( ['out', 'retval'], POINTER(WindowVisualState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentWindowInteractionState',
              ( ['out', 'retval'], POINTER(WindowInteractionState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanMaximize',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanMinimize',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsModal',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsTopmost',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedWindowVisualState',
              ( ['out', 'retval'], POINTER(WindowVisualState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedWindowInteractionState',
              ( ['out', 'retval'], POINTER(WindowInteractionState), 'retVal' )),
]
################################################################
## code template for IUIAutomationWindowPattern implementation
##class IUIAutomationWindowPattern_Impl(object):
##    def Close(self):
##        '-no docstring-'
##        #return 
##
##    def WaitForInputIdle(self, milliseconds):
##        '-no docstring-'
##        #return success
##
##    def SetWindowVisualState(self, state):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentCanMaximize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentCanMinimize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsModal(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsTopmost(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentWindowVisualState(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentWindowInteractionState(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCanMaximize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCanMinimize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsModal(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsTopmost(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedWindowVisualState(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedWindowInteractionState(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationItemContainerPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{C690FDB2-27A8-423C-812D-429773C9084E}')
    _idlflags_ = []
IUIAutomationItemContainerPattern._methods_ = [
    COMMETHOD([], HRESULT, 'FindItemByProperty',
              ( ['in'], POINTER(IUIAutomationElement), 'pStartAfter' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'value' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'pFound' )),
]
################################################################
## code template for IUIAutomationItemContainerPattern implementation
##class IUIAutomationItemContainerPattern_Impl(object):
##    def FindItemByProperty(self, pStartAfter, propertyId, value):
##        '-no docstring-'
##        #return pFound
##

class IUIAutomation5(IUIAutomation4):
    _case_insensitive_ = True
    _iid_ = GUID('{25F700C8-D816-4057-A9DC-3CBDEE77E256}')
    _idlflags_ = []
class IUIAutomationNotificationEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{C7CB2637-E6C2-4D0C-85DE-4948C02175C7}')
    _idlflags_ = ['oleautomation']
IUIAutomation5._methods_ = [
    COMMETHOD([], HRESULT, 'AddNotificationEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationNotificationEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveNotificationEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationNotificationEventHandler), 'handler' )),
]
################################################################
## code template for IUIAutomation5 implementation
##class IUIAutomation5_Impl(object):
##    def AddNotificationEventHandler(self, element, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveNotificationEventHandler(self, element, handler):
##        '-no docstring-'
##        #return 
##

class IUIAutomationVirtualizedItemPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{6BA3D7A6-04CF-4F11-8793-A8D1CDE9969F}')
    _idlflags_ = []
IUIAutomationVirtualizedItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Realize'),
]
################################################################
## code template for IUIAutomationVirtualizedItemPattern implementation
##class IUIAutomationVirtualizedItemPattern_Impl(object):
##    def Realize(self):
##        '-no docstring-'
##        #return 
##

class IUIAutomation6(IUIAutomation5):
    _case_insensitive_ = True
    _iid_ = GUID('{AAE072DA-29E3-413D-87A7-192DBF81ED10}')
    _idlflags_ = []
class IUIAutomationEventHandlerGroup(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{C9EE12F2-C13B-4408-997C-639914377F4E}')
    _idlflags_ = []

# values for enumeration 'ConnectionRecoveryBehaviorOptions'
ConnectionRecoveryBehaviorOptions_Disabled = 0
ConnectionRecoveryBehaviorOptions_Enabled = 1
ConnectionRecoveryBehaviorOptions = c_int # enum

# values for enumeration 'CoalesceEventsOptions'
CoalesceEventsOptions_Disabled = 0
CoalesceEventsOptions_Enabled = 1
CoalesceEventsOptions = c_int # enum
class IUIAutomationActiveTextPositionChangedEventHandler(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{F97933B0-8DAE-4496-8997-5BA015FE0D82}')
    _idlflags_ = ['oleautomation']
IUIAutomation6._methods_ = [
    COMMETHOD([], HRESULT, 'CreateEventHandlerGroup',
              ( ['out'], POINTER(POINTER(IUIAutomationEventHandlerGroup)), 'handlerGroup' )),
    COMMETHOD([], HRESULT, 'AddEventHandlerGroup',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationEventHandlerGroup), 'handlerGroup' )),
    COMMETHOD([], HRESULT, 'RemoveEventHandlerGroup',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationEventHandlerGroup), 'handlerGroup' )),
    COMMETHOD(['propget'], HRESULT, 'ConnectionRecoveryBehavior',
              ( ['out', 'retval'], POINTER(ConnectionRecoveryBehaviorOptions), 'ConnectionRecoveryBehaviorOptions' )),
    COMMETHOD(['propput'], HRESULT, 'ConnectionRecoveryBehavior',
              ( ['in'], ConnectionRecoveryBehaviorOptions, 'ConnectionRecoveryBehaviorOptions' )),
    COMMETHOD(['propget'], HRESULT, 'CoalesceEvents',
              ( ['out', 'retval'], POINTER(CoalesceEventsOptions), 'CoalesceEventsOptions' )),
    COMMETHOD(['propput'], HRESULT, 'CoalesceEvents',
              ( ['in'], CoalesceEventsOptions, 'CoalesceEventsOptions' )),
    COMMETHOD([], HRESULT, 'AddActiveTextPositionChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationActiveTextPositionChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'RemoveActiveTextPositionChangedEventHandler',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationActiveTextPositionChangedEventHandler), 'handler' )),
]
################################################################
## code template for IUIAutomation6 implementation
##class IUIAutomation6_Impl(object):
##    def CreateEventHandlerGroup(self):
##        '-no docstring-'
##        #return handlerGroup
##
##    def AddEventHandlerGroup(self, element, handlerGroup):
##        '-no docstring-'
##        #return 
##
##    def RemoveEventHandlerGroup(self, element, handlerGroup):
##        '-no docstring-'
##        #return 
##
##    def _get(self):
##        '-no docstring-'
##        #return ConnectionRecoveryBehaviorOptions
##    def _set(self, ConnectionRecoveryBehaviorOptions):
##        '-no docstring-'
##    ConnectionRecoveryBehavior = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return CoalesceEventsOptions
##    def _set(self, CoalesceEventsOptions):
##        '-no docstring-'
##    CoalesceEvents = property(_get, _set, doc = _set.__doc__)
##
##    def AddActiveTextPositionChangedEventHandler(self, element, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def RemoveActiveTextPositionChangedEventHandler(self, element, handler):
##        '-no docstring-'
##        #return 
##

class IUIAutomationElement3(IUIAutomationElement2):
    _case_insensitive_ = True
    _iid_ = GUID('{8471DF34-AEE0-4A01-A7DE-7DB9AF12C296}')
    _idlflags_ = []
IUIAutomationElement3._methods_ = [
    COMMETHOD([], HRESULT, 'ShowContextMenu'),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsPeripheral',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsPeripheral',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationElement3 implementation
##class IUIAutomationElement3_Impl(object):
##    def ShowContextMenu(self):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentIsPeripheral(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsPeripheral(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationAnnotationPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{9A175B21-339E-41B1-8E8B-623F6B681098}')
    _idlflags_ = []
IUIAutomationAnnotationPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentAnnotationTypeId',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAnnotationTypeName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAuthor',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDateTime',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentTarget',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAnnotationTypeId',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAnnotationTypeName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAuthor',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDateTime',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedTarget',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
]
################################################################
## code template for IUIAutomationAnnotationPattern implementation
##class IUIAutomationAnnotationPattern_Impl(object):
##    @property
##    def CurrentAnnotationTypeId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAnnotationTypeName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAuthor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentDateTime(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentTarget(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAnnotationTypeId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAnnotationTypeName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAuthor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedDateTime(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedTarget(self):
##        '-no docstring-'
##        #return retVal
##

AnnotationType_FormatChange = 60014 # Constant c_int
AnnotationType_UnsyncedChange = 60015 # Constant c_int
AnnotationType_EditingLockedChange = 60016 # Constant c_int
AnnotationType_ExternalChange = 60017 # Constant c_int
AnnotationType_ConflictingChange = 60018 # Constant c_int
AnnotationType_Author = 60019 # Constant c_int
AnnotationType_AdvancedProofingIssue = 60020 # Constant c_int
AnnotationType_DataValidationError = 60021 # Constant c_int
AnnotationType_CircularReferenceError = 60022 # Constant c_int
AnnotationType_Mathematics = 60023 # Constant c_int

# values for enumeration 'AutomationElementMode'
AutomationElementMode_None = 0
AutomationElementMode_Full = 1
AutomationElementMode = c_int # enum
AnnotationType_Sensitive = 60024 # Constant c_int
StyleId_Custom = 70000 # Constant c_int
StyleId_Heading1 = 70001 # Constant c_int
StyleId_Heading2 = 70002 # Constant c_int
StyleId_Heading3 = 70003 # Constant c_int
StyleId_Heading4 = 70004 # Constant c_int
StyleId_Heading5 = 70005 # Constant c_int
StyleId_Heading6 = 70006 # Constant c_int
StyleId_Heading7 = 70007 # Constant c_int
StyleId_Heading8 = 70008 # Constant c_int
IUIAutomationEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleAutomationEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], c_int, 'eventId' )),
]
################################################################
## code template for IUIAutomationEventHandler implementation
##class IUIAutomationEventHandler_Impl(object):
##    def HandleAutomationEvent(self, sender, eventId):
##        '-no docstring-'
##        #return 
##

StyleId_Heading9 = 70009 # Constant c_int
StyleId_Title = 70010 # Constant c_int
StyleId_Subtitle = 70011 # Constant c_int
StyleId_Normal = 70012 # Constant c_int
StyleId_Emphasis = 70013 # Constant c_int
StyleId_Quote = 70014 # Constant c_int
StyleId_BulletedList = 70015 # Constant c_int
StyleId_NumberedList = 70016 # Constant c_int
UIA_CustomLandmarkTypeId = 80000 # Constant c_int
UIA_FormLandmarkTypeId = 80001 # Constant c_int
UIA_MainLandmarkTypeId = 80002 # Constant c_int
UIA_NavigationLandmarkTypeId = 80003 # Constant c_int
UIA_SearchLandmarkTypeId = 80004 # Constant c_int
HeadingLevel_None = 80050 # Constant c_int
HeadingLevel1 = 80051 # Constant c_int
HeadingLevel2 = 80052 # Constant c_int
HeadingLevel3 = 80053 # Constant c_int
HeadingLevel4 = 80054 # Constant c_int
HeadingLevel5 = 80055 # Constant c_int
HeadingLevel6 = 80056 # Constant c_int
HeadingLevel7 = 80057 # Constant c_int
HeadingLevel8 = 80058 # Constant c_int
IUIAutomationPropertyChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandlePropertyChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], VARIANT, 'newValue' )),
]
################################################################
## code template for IUIAutomationPropertyChangedEventHandler implementation
##class IUIAutomationPropertyChangedEventHandler_Impl(object):
##    def HandlePropertyChangedEvent(self, sender, propertyId, newValue):
##        '-no docstring-'
##        #return 
##

HeadingLevel9 = 80059 # Constant c_int
UIA_SummaryChangeId = 90000 # Constant c_int
UIA_SayAsInterpretAsMetadataId = 100000 # Constant c_int
IUIAutomationElementArray._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'Length',
              ( ['out', 'retval'], POINTER(c_int), 'Length' )),
    COMMETHOD([], HRESULT, 'GetElement',
              ( ['in'], c_int, 'index' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
]
################################################################
## code template for IUIAutomationElementArray implementation
##class IUIAutomationElementArray_Impl(object):
##    @property
##    def Length(self):
##        '-no docstring-'
##        #return Length
##
##    def GetElement(self, index):
##        '-no docstring-'
##        #return element
##

IUIAutomationCondition._methods_ = [
]
################################################################
## code template for IUIAutomationCondition implementation
##class IUIAutomationCondition_Impl(object):

IUIAutomationCacheRequest._methods_ = [
    COMMETHOD([], HRESULT, 'AddProperty',
              ( ['in'], c_int, 'propertyId' )),
    COMMETHOD([], HRESULT, 'AddPattern',
              ( ['in'], c_int, 'patternId' )),
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCacheRequest)), 'clonedRequest' )),
    COMMETHOD(['propget'], HRESULT, 'TreeScope',
              ( ['out', 'retval'], POINTER(TreeScope), 'scope' )),
    COMMETHOD(['propput'], HRESULT, 'TreeScope',
              ( ['in'], TreeScope, 'scope' )),
    COMMETHOD(['propget'], HRESULT, 'TreeFilter',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'filter' )),
    COMMETHOD(['propput'], HRESULT, 'TreeFilter',
              ( ['in'], POINTER(IUIAutomationCondition), 'filter' )),
    COMMETHOD(['propget'], HRESULT, 'AutomationElementMode',
              ( ['out', 'retval'], POINTER(AutomationElementMode), 'mode' )),
    COMMETHOD(['propput'], HRESULT, 'AutomationElementMode',
              ( ['in'], AutomationElementMode, 'mode' )),
]
################################################################
## code template for IUIAutomationCacheRequest implementation
##class IUIAutomationCacheRequest_Impl(object):
##    def AddProperty(self, propertyId):
##        '-no docstring-'
##        #return 
##
##    def AddPattern(self, patternId):
##        '-no docstring-'
##        #return 
##
##    def Clone(self):
##        '-no docstring-'
##        #return clonedRequest
##
##    def _get(self):
##        '-no docstring-'
##        #return scope
##    def _set(self, scope):
##        '-no docstring-'
##    TreeScope = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return filter
##    def _set(self, filter):
##        '-no docstring-'
##    TreeFilter = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return mode
##    def _set(self, mode):
##        '-no docstring-'
##    AutomationElementMode = property(_get, _set, doc = _set.__doc__)
##

IUIAutomationFocusChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleFocusChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' )),
]
################################################################
## code template for IUIAutomationFocusChangedEventHandler implementation
##class IUIAutomationFocusChangedEventHandler_Impl(object):
##    def HandleFocusChangedEvent(self, sender):
##        '-no docstring-'
##        #return 
##


# values for enumeration 'StructureChangeType'
StructureChangeType_ChildAdded = 0
StructureChangeType_ChildRemoved = 1
StructureChangeType_ChildrenInvalidated = 2
StructureChangeType_ChildrenBulkAdded = 3
StructureChangeType_ChildrenBulkRemoved = 4
StructureChangeType_ChildrenReordered = 5
StructureChangeType = c_int # enum
IUIAutomationTextEditTextChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleTextEditTextChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], TextEditChangeType, 'TextEditChangeType' ),
              ( ['in'], _midlSAFEARRAY(BSTR), 'eventStrings' )),
]
################################################################
## code template for IUIAutomationTextEditTextChangedEventHandler implementation
##class IUIAutomationTextEditTextChangedEventHandler_Impl(object):
##    def HandleTextEditTextChangedEvent(self, sender, TextEditChangeType, eventStrings):
##        '-no docstring-'
##        #return 
##

class IUIAutomationDockPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{FDE5EF97-1464-48F6-90BF-43D0948E86EC}')
    _idlflags_ = []

# values for enumeration 'DockPosition'
DockPosition_Top = 0
DockPosition_Left = 1
DockPosition_Bottom = 2
DockPosition_Right = 3
DockPosition_Fill = 4
DockPosition_None = 5
DockPosition = c_int # enum
IUIAutomationDockPattern._methods_ = [
    COMMETHOD([], HRESULT, 'SetDockPosition',
              ( ['in'], DockPosition, 'dockPos' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDockPosition',
              ( ['out', 'retval'], POINTER(DockPosition), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDockPosition',
              ( ['out', 'retval'], POINTER(DockPosition), 'retVal' )),
]
################################################################
## code template for IUIAutomationDockPattern implementation
##class IUIAutomationDockPattern_Impl(object):
##    def SetDockPosition(self, dockPos):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentDockPosition(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedDockPosition(self):
##        '-no docstring-'
##        #return retVal
##

class UiaChangeInfo(Structure):
    pass
IUIAutomationChangesEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleChangesEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], POINTER(UiaChangeInfo), 'uiaChanges' ),
              ( ['in'], c_int, 'changesCount' )),
]
################################################################
## code template for IUIAutomationChangesEventHandler implementation
##class IUIAutomationChangesEventHandler_Impl(object):
##    def HandleChangesEvent(self, sender, uiaChanges, changesCount):
##        '-no docstring-'
##        #return 
##


# values for enumeration 'NotificationKind'
NotificationKind_ItemAdded = 0
NotificationKind_ItemRemoved = 1
NotificationKind_ActionCompleted = 2
NotificationKind_ActionAborted = 3
NotificationKind_Other = 4
NotificationKind = c_int # enum

# values for enumeration 'NotificationProcessing'
NotificationProcessing_ImportantAll = 0
NotificationProcessing_ImportantMostRecent = 1
NotificationProcessing_All = 2
NotificationProcessing_MostRecent = 3
NotificationProcessing_CurrentThenMostRecent = 4
NotificationProcessing = c_int # enum
IUIAutomationNotificationEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleNotificationEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( [], NotificationKind, 'NotificationKind' ),
              ( [], NotificationProcessing, 'NotificationProcessing' ),
              ( ['in'], BSTR, 'displayString' ),
              ( ['in'], BSTR, 'activityId' )),
]
################################################################
## code template for IUIAutomationNotificationEventHandler implementation
##class IUIAutomationNotificationEventHandler_Impl(object):
##    def HandleNotificationEvent(self, sender, NotificationKind, NotificationProcessing, displayString, activityId):
##        '-no docstring-'
##        #return 
##

UiaChangeInfo._fields_ = [
    ('uiaId', c_int),
    ('payload', VARIANT),
    ('extraInfo', VARIANT),
]
assert sizeof(UiaChangeInfo) == 40, sizeof(UiaChangeInfo)
assert alignment(UiaChangeInfo) == 8, alignment(UiaChangeInfo)
class IUIAutomationScrollPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{88F4D42A-E881-459D-A77C-73BBBB7E02DC}')
    _idlflags_ = []

# values for enumeration 'ScrollAmount'
ScrollAmount_LargeDecrement = 0
ScrollAmount_SmallDecrement = 1
ScrollAmount_NoAmount = 2
ScrollAmount_LargeIncrement = 3
ScrollAmount_SmallIncrement = 4
ScrollAmount = c_int # enum
IUIAutomationScrollPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Scroll',
              ( ['in'], ScrollAmount, 'horizontalAmount' ),
              ( ['in'], ScrollAmount, 'verticalAmount' )),
    COMMETHOD([], HRESULT, 'SetScrollPercent',
              ( ['in'], c_double, 'horizontalPercent' ),
              ( ['in'], c_double, 'verticalPercent' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHorizontalScrollPercent',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentVerticalScrollPercent',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHorizontalViewSize',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentVerticalViewSize',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHorizontallyScrollable',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentVerticallyScrollable',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHorizontalScrollPercent',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedVerticalScrollPercent',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHorizontalViewSize',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedVerticalViewSize',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHorizontallyScrollable',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedVerticallyScrollable',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationScrollPattern implementation
##class IUIAutomationScrollPattern_Impl(object):
##    def Scroll(self, horizontalAmount, verticalAmount):
##        '-no docstring-'
##        #return 
##
##    def SetScrollPercent(self, horizontalPercent, verticalPercent):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentHorizontalScrollPercent(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentVerticalScrollPercent(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentHorizontalViewSize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentVerticalViewSize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentHorizontallyScrollable(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentVerticallyScrollable(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedHorizontalScrollPercent(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedVerticalScrollPercent(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedHorizontalViewSize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedVerticalViewSize(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedHorizontallyScrollable(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedVerticallyScrollable(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationInvokePattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{FB377FBE-8EA6-46D5-9C73-6499642D3059}')
    _idlflags_ = []
IUIAutomationInvokePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Invoke'),
]
################################################################
## code template for IUIAutomationInvokePattern implementation
##class IUIAutomationInvokePattern_Impl(object):
##    def Invoke(self):
##        '-no docstring-'
##        #return 
##

class IUIAutomationSelectionPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{5ED5202E-B2AC-47A6-B638-4B0BF140D78E}')
    _idlflags_ = []
IUIAutomationSelectionPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetCurrentSelection',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanSelectMultiple',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsSelectionRequired',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedSelection',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanSelectMultiple',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsSelectionRequired',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationSelectionPattern implementation
##class IUIAutomationSelectionPattern_Impl(object):
##    def GetCurrentSelection(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentCanSelectMultiple(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsSelectionRequired(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedSelection(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCanSelectMultiple(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsSelectionRequired(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationStylesPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{85B5F0A2-BD79-484A-AD2B-388C9838D5FB}')
    _idlflags_ = []
class ExtendedProperty(Structure):
    pass
IUIAutomationStylesPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentStyleId',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentStyleName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFillColor',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFillPatternStyle',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentShape',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentFillPatternColor',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentExtendedProperties',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentExtendedPropertiesAsArray',
              ( ['out'], POINTER(POINTER(ExtendedProperty)), 'propertyArray' ),
              ( ['out'], POINTER(c_int), 'propertyCount' )),
    COMMETHOD(['propget'], HRESULT, 'CachedStyleId',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedStyleName',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFillColor',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFillPatternStyle',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedShape',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFillPatternColor',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedExtendedProperties',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedExtendedPropertiesAsArray',
              ( ['out'], POINTER(POINTER(ExtendedProperty)), 'propertyArray' ),
              ( ['out'], POINTER(c_int), 'propertyCount' )),
]
################################################################
## code template for IUIAutomationStylesPattern implementation
##class IUIAutomationStylesPattern_Impl(object):
##    @property
##    def CurrentStyleId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentStyleName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentFillColor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentFillPatternStyle(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentShape(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentFillPatternColor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentExtendedProperties(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentExtendedPropertiesAsArray(self):
##        '-no docstring-'
##        #return propertyArray, propertyCount
##
##    @property
##    def CachedStyleId(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedStyleName(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFillColor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFillPatternStyle(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedShape(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFillPatternColor(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedExtendedProperties(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedExtendedPropertiesAsArray(self):
##        '-no docstring-'
##        #return propertyArray, propertyCount
##

UIA_SelectionPatternId = 10001 # Constant c_int
UIA_IsPasswordPropertyId = 30019 # Constant c_int
UIA_IsControlElementPropertyId = 30016 # Constant c_int
UIA_ClickablePointPropertyId = 30014 # Constant c_int
UIA_IsContentElementPropertyId = 30017 # Constant c_int
IUIAutomationStructureChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleStructureChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], StructureChangeType, 'changeType' ),
              ( ['in'], _midlSAFEARRAY(c_int), 'runtimeId' )),
]
################################################################
## code template for IUIAutomationStructureChangedEventHandler implementation
##class IUIAutomationStructureChangedEventHandler_Impl(object):
##    def HandleStructureChangedEvent(self, sender, changeType, runtimeId):
##        '-no docstring-'
##        #return 
##

UIA_LabeledByPropertyId = 30018 # Constant c_int
UIA_InvokePatternId = 10000 # Constant c_int
UIA_CulturePropertyId = 30015 # Constant c_int
UIA_ValuePatternId = 10002 # Constant c_int
UIA_RangeValuePatternId = 10003 # Constant c_int
UIA_ScrollPatternId = 10004 # Constant c_int
UIA_ExpandCollapsePatternId = 10005 # Constant c_int
class Library(object):
    name = 'UIAutomationClient'
    _reg_typelib_ = ('{944DE083-8FB8-45CF-BCB7-C477ACB2F897}', 1, 0)

UIA_GridPatternId = 10006 # Constant c_int
UIA_GridItemPatternId = 10007 # Constant c_int
UIA_MultipleViewPatternId = 10008 # Constant c_int
UIA_WindowPatternId = 10009 # Constant c_int
UIA_SelectionItemPatternId = 10010 # Constant c_int
UIA_DockPatternId = 10011 # Constant c_int
UIA_TablePatternId = 10012 # Constant c_int
UIA_TableItemPatternId = 10013 # Constant c_int
ExtendedProperty._fields_ = [
    ('PropertyName', BSTR),
    ('PropertyValue', BSTR),
]
assert sizeof(ExtendedProperty) == 8, sizeof(ExtendedProperty)
assert alignment(ExtendedProperty) == 4, alignment(ExtendedProperty)
UIA_TextPatternId = 10014 # Constant c_int
UIA_TogglePatternId = 10015 # Constant c_int
UIA_TransformPatternId = 10016 # Constant c_int
UIA_ScrollItemPatternId = 10017 # Constant c_int
UIA_LegacyIAccessiblePatternId = 10018 # Constant c_int
UIA_ItemContainerPatternId = 10019 # Constant c_int
UIA_VirtualizedItemPatternId = 10020 # Constant c_int
UIA_SynchronizedInputPatternId = 10021 # Constant c_int
UIA_ObjectModelPatternId = 10022 # Constant c_int
UIA_AnnotationPatternId = 10023 # Constant c_int
UIA_TextPattern2Id = 10024 # Constant c_int
UIA_StylesPatternId = 10025 # Constant c_int
UIA_SpreadsheetPatternId = 10026 # Constant c_int
UIA_SpreadsheetItemPatternId = 10027 # Constant c_int
UIA_TransformPattern2Id = 10028 # Constant c_int
UIA_TextChildPatternId = 10029 # Constant c_int
UIA_DragPatternId = 10030 # Constant c_int
UIA_DropTargetPatternId = 10031 # Constant c_int
UIA_TextEditPatternId = 10032 # Constant c_int
UIA_CustomNavigationPatternId = 10033 # Constant c_int
UIA_SelectionPattern2Id = 10034 # Constant c_int
UIA_ToolTipOpenedEventId = 20000 # Constant c_int
UIA_ToolTipClosedEventId = 20001 # Constant c_int
UIA_StructureChangedEventId = 20002 # Constant c_int
class IUIAutomationSpreadsheetPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{7517A7C8-FAAE-4DE9-9F08-29B91E8595C1}')
    _idlflags_ = []
IUIAutomationSpreadsheetPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetItemByName',
              ( ['in'], BSTR, 'name' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
]
################################################################
## code template for IUIAutomationSpreadsheetPattern implementation
##class IUIAutomationSpreadsheetPattern_Impl(object):
##    def GetItemByName(self, name):
##        '-no docstring-'
##        #return element
##

UIA_MenuOpenedEventId = 20003 # Constant c_int
UIA_AutomationPropertyChangedEventId = 20004 # Constant c_int
UIA_AutomationFocusChangedEventId = 20005 # Constant c_int
UIA_AsyncContentLoadedEventId = 20006 # Constant c_int
UIA_MenuClosedEventId = 20007 # Constant c_int
UIA_LayoutInvalidatedEventId = 20008 # Constant c_int
UIA_Invoke_InvokedEventId = 20009 # Constant c_int
class IUIAutomationSpreadsheetItemPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{7D4FB86C-8D34-40E1-8E83-62C15204E335}')
    _idlflags_ = []
IUIAutomationSpreadsheetItemPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentFormula',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentAnnotationObjects',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentAnnotationTypes',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFormula',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedAnnotationObjects',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedAnnotationTypes',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
]
################################################################
## code template for IUIAutomationSpreadsheetItemPattern implementation
##class IUIAutomationSpreadsheetItemPattern_Impl(object):
##    @property
##    def CurrentFormula(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentAnnotationObjects(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentAnnotationTypes(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFormula(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedAnnotationObjects(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedAnnotationTypes(self):
##        '-no docstring-'
##        #return retVal
##

UIA_SelectionItem_ElementAddedToSelectionEventId = 20010 # Constant c_int
UIA_SelectionItem_ElementRemovedFromSelectionEventId = 20011 # Constant c_int
UIA_SelectionItem_ElementSelectedEventId = 20012 # Constant c_int
UIA_Selection_InvalidatedEventId = 20013 # Constant c_int
UIA_Text_TextSelectionChangedEventId = 20014 # Constant c_int
UIA_Text_TextChangedEventId = 20015 # Constant c_int
UIA_Window_WindowOpenedEventId = 20016 # Constant c_int
UIA_Window_WindowClosedEventId = 20017 # Constant c_int
UIA_MenuModeStartEventId = 20018 # Constant c_int
UIA_MenuModeEndEventId = 20019 # Constant c_int
UIA_InputReachedTargetEventId = 20020 # Constant c_int
UIA_InputReachedOtherElementEventId = 20021 # Constant c_int
UIA_InputDiscardedEventId = 20022 # Constant c_int
UIA_SystemAlertEventId = 20023 # Constant c_int
UIA_LiveRegionChangedEventId = 20024 # Constant c_int
UIA_HostedFragmentRootsInvalidatedEventId = 20025 # Constant c_int
UIA_Drag_DragStartEventId = 20026 # Constant c_int
UIA_Drag_DragCancelEventId = 20027 # Constant c_int
UIA_Drag_DragCompleteEventId = 20028 # Constant c_int
UIA_DropTarget_DragEnterEventId = 20029 # Constant c_int
UIA_DropTarget_DragLeaveEventId = 20030 # Constant c_int
UIA_DropTarget_DroppedEventId = 20031 # Constant c_int
UIA_TextEdit_TextChangedEventId = 20032 # Constant c_int
UIA_TextEdit_ConversionTargetChangedEventId = 20033 # Constant c_int
UIA_ChangesEventId = 20034 # Constant c_int
UIA_NotificationEventId = 20035 # Constant c_int
UIA_ActiveTextPositionChangedEventId = 20036 # Constant c_int
class IUIAutomationTransformPattern2(IUIAutomationTransformPattern):
    _case_insensitive_ = True
    _iid_ = GUID('{6D74D017-6ECB-4381-B38B-3C17A48FF1C2}')
    _idlflags_ = []
IUIAutomationTransformPattern2._methods_ = [
    COMMETHOD([], HRESULT, 'Zoom',
              ( ['in'], c_double, 'zoomValue' )),
    COMMETHOD([], HRESULT, 'ZoomByUnit',
              ( ['in'], ZoomUnit, 'ZoomUnit' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCanZoom',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCanZoom',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentZoomLevel',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedZoomLevel',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentZoomMinimum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedZoomMinimum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentZoomMaximum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedZoomMaximum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
]
################################################################
## code template for IUIAutomationTransformPattern2 implementation
##class IUIAutomationTransformPattern2_Impl(object):
##    def Zoom(self, zoomValue):
##        '-no docstring-'
##        #return 
##
##    def ZoomByUnit(self, ZoomUnit):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentCanZoom(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCanZoom(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentZoomLevel(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedZoomLevel(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentZoomMinimum(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedZoomMinimum(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentZoomMaximum(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedZoomMaximum(self):
##        '-no docstring-'
##        #return retVal
##

UIA_RuntimeIdPropertyId = 30000 # Constant c_int
UIA_BoundingRectanglePropertyId = 30001 # Constant c_int
UIA_ProcessIdPropertyId = 30002 # Constant c_int
UIA_ControlTypePropertyId = 30003 # Constant c_int
UIA_LocalizedControlTypePropertyId = 30004 # Constant c_int
UIA_NamePropertyId = 30005 # Constant c_int
UIA_AcceleratorKeyPropertyId = 30006 # Constant c_int
UIA_AccessKeyPropertyId = 30007 # Constant c_int
UIA_HasKeyboardFocusPropertyId = 30008 # Constant c_int
UIA_IsKeyboardFocusablePropertyId = 30009 # Constant c_int
UIA_IsEnabledPropertyId = 30010 # Constant c_int
UIA_AutomationIdPropertyId = 30011 # Constant c_int
UIA_ClassNamePropertyId = 30012 # Constant c_int
UIA_HelpTextPropertyId = 30013 # Constant c_int
class IRawElementProviderSimple(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{D6DD68D1-86FD-4332-8666-9ABEDEA2D24C}')
    _idlflags_ = ['oleautomation']
IUIAutomationProxyFactory._methods_ = [
    COMMETHOD([], HRESULT, 'CreateProvider',
              ( ['in'], c_void_p, 'hwnd' ),
              ( ['in'], c_int, 'idObject' ),
              ( ['in'], c_int, 'idChild' ),
              ( ['out', 'retval'], POINTER(POINTER(IRawElementProviderSimple)), 'provider' )),
    COMMETHOD(['propget'], HRESULT, 'ProxyFactoryId',
              ( ['out', 'retval'], POINTER(BSTR), 'factoryId' )),
]
################################################################
## code template for IUIAutomationProxyFactory implementation
##class IUIAutomationProxyFactory_Impl(object):
##    def CreateProvider(self, hwnd, idObject, idChild):
##        '-no docstring-'
##        #return provider
##
##    @property
##    def ProxyFactoryId(self):
##        '-no docstring-'
##        #return factoryId
##


# values for enumeration 'ProviderOptions'
ProviderOptions_ClientSideProvider = 1
ProviderOptions_ServerSideProvider = 2
ProviderOptions_NonClientAreaProvider = 4
ProviderOptions_OverrideProvider = 8
ProviderOptions_ProviderOwnsSetFocus = 16
ProviderOptions_UseComThreading = 32
ProviderOptions_RefuseNonClientSupport = 64
ProviderOptions_HasNativeIAccessible = 128
ProviderOptions_UseClientCoordinates = 256
ProviderOptions = c_int # enum
IRawElementProviderSimple._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ProviderOptions',
              ( ['out', 'retval'], POINTER(ProviderOptions), 'pRetVal' )),
    COMMETHOD([], HRESULT, 'GetPatternProvider',
              ( ['in'], c_int, 'patternId' ),
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'pRetVal' )),
    COMMETHOD([], HRESULT, 'GetPropertyValue',
              ( ['in'], c_int, 'propertyId' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'pRetVal' )),
    COMMETHOD(['propget'], HRESULT, 'HostRawElementProvider',
              ( ['out', 'retval'], POINTER(POINTER(IRawElementProviderSimple)), 'pRetVal' )),
]
################################################################
## code template for IRawElementProviderSimple implementation
##class IRawElementProviderSimple_Impl(object):
##    @property
##    def ProviderOptions(self):
##        '-no docstring-'
##        #return pRetVal
##
##    def GetPatternProvider(self, patternId):
##        '-no docstring-'
##        #return pRetVal
##
##    def GetPropertyValue(self, propertyId):
##        '-no docstring-'
##        #return pRetVal
##
##    @property
##    def HostRawElementProvider(self):
##        '-no docstring-'
##        #return pRetVal
##

class IUIAutomationSelectionPattern2(IUIAutomationSelectionPattern):
    _case_insensitive_ = True
    _iid_ = GUID('{0532BFAE-C011-4E32-A343-6D642D798555}')
    _idlflags_ = []
IUIAutomationSelectionPattern2._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentFirstSelectedItem',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLastSelectedItem',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCurrentSelectedItem',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentItemCount',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFirstSelectedItem',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLastSelectedItem',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCurrentSelectedItem',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedItemCount',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationSelectionPattern2 implementation
##class IUIAutomationSelectionPattern2_Impl(object):
##    @property
##    def CurrentFirstSelectedItem(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentLastSelectedItem(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentCurrentSelectedItem(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentItemCount(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFirstSelectedItem(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLastSelectedItem(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCurrentSelectedItem(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedItemCount(self):
##        '-no docstring-'
##        #return retVal
##

IUIAutomationProxyFactoryEntry._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ProxyFactory',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationProxyFactory)), 'factory' )),
    COMMETHOD(['propget'], HRESULT, 'ClassName',
              ( ['out', 'retval'], POINTER(BSTR), 'ClassName' )),
    COMMETHOD(['propget'], HRESULT, 'ImageName',
              ( ['out', 'retval'], POINTER(BSTR), 'ImageName' )),
    COMMETHOD(['propget'], HRESULT, 'AllowSubstringMatch',
              ( ['out', 'retval'], POINTER(c_int), 'AllowSubstringMatch' )),
    COMMETHOD(['propget'], HRESULT, 'CanCheckBaseClass',
              ( ['out', 'retval'], POINTER(c_int), 'CanCheckBaseClass' )),
    COMMETHOD(['propget'], HRESULT, 'NeedsAdviseEvents',
              ( ['out', 'retval'], POINTER(c_int), 'adviseEvents' )),
    COMMETHOD(['propput'], HRESULT, 'ClassName',
              ( ['in'], WSTRING, 'ClassName' )),
    COMMETHOD(['propput'], HRESULT, 'ImageName',
              ( ['in'], WSTRING, 'ImageName' )),
    COMMETHOD(['propput'], HRESULT, 'AllowSubstringMatch',
              ( ['in'], c_int, 'AllowSubstringMatch' )),
    COMMETHOD(['propput'], HRESULT, 'CanCheckBaseClass',
              ( ['in'], c_int, 'CanCheckBaseClass' )),
    COMMETHOD(['propput'], HRESULT, 'NeedsAdviseEvents',
              ( ['in'], c_int, 'adviseEvents' )),
    COMMETHOD([], HRESULT, 'SetWinEventsForAutomationEvent',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['in'], _midlSAFEARRAY(c_uint), 'winEvents' )),
    COMMETHOD([], HRESULT, 'GetWinEventsForAutomationEvent',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], c_int, 'propertyId' ),
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_uint)), 'winEvents' )),
]
################################################################
## code template for IUIAutomationProxyFactoryEntry implementation
##class IUIAutomationProxyFactoryEntry_Impl(object):
##    @property
##    def ProxyFactory(self):
##        '-no docstring-'
##        #return factory
##
##    def _get(self):
##        '-no docstring-'
##        #return ClassName
##    def _set(self, ClassName):
##        '-no docstring-'
##    ClassName = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return ImageName
##    def _set(self, ImageName):
##        '-no docstring-'
##    ImageName = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return AllowSubstringMatch
##    def _set(self, AllowSubstringMatch):
##        '-no docstring-'
##    AllowSubstringMatch = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return CanCheckBaseClass
##    def _set(self, CanCheckBaseClass):
##        '-no docstring-'
##    CanCheckBaseClass = property(_get, _set, doc = _set.__doc__)
##
##    def _get(self):
##        '-no docstring-'
##        #return adviseEvents
##    def _set(self, adviseEvents):
##        '-no docstring-'
##    NeedsAdviseEvents = property(_get, _set, doc = _set.__doc__)
##
##    def SetWinEventsForAutomationEvent(self, eventId, propertyId, winEvents):
##        '-no docstring-'
##        #return 
##
##    def GetWinEventsForAutomationEvent(self, eventId, propertyId):
##        '-no docstring-'
##        #return winEvents
##

class IUIAutomationSelectionItemPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A8EFA66A-0FDA-421A-9194-38021F3578EA}')
    _idlflags_ = []
IUIAutomationSelectionItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Select'),
    COMMETHOD([], HRESULT, 'AddToSelection'),
    COMMETHOD([], HRESULT, 'RemoveFromSelection'),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsSelected',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentSelectionContainer',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsSelected',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedSelectionContainer',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
]
################################################################
## code template for IUIAutomationSelectionItemPattern implementation
##class IUIAutomationSelectionItemPattern_Impl(object):
##    def Select(self):
##        '-no docstring-'
##        #return 
##
##    def AddToSelection(self):
##        '-no docstring-'
##        #return 
##
##    def RemoveFromSelection(self):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentIsSelected(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentSelectionContainer(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsSelected(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedSelectionContainer(self):
##        '-no docstring-'
##        #return retVal
##

IUIAutomationProxyFactoryMapping._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'count',
              ( ['out', 'retval'], POINTER(c_uint), 'count' )),
    COMMETHOD([], HRESULT, 'GetTable',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(POINTER(IUIAutomationProxyFactoryEntry))), 'table' )),
    COMMETHOD([], HRESULT, 'GetEntry',
              ( ['in'], c_uint, 'index' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationProxyFactoryEntry)), 'entry' )),
    COMMETHOD([], HRESULT, 'SetTable',
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationProxyFactoryEntry)), 'factoryList' )),
    COMMETHOD([], HRESULT, 'InsertEntries',
              ( ['in'], c_uint, 'before' ),
              ( ['in'], _midlSAFEARRAY(POINTER(IUIAutomationProxyFactoryEntry)), 'factoryList' )),
    COMMETHOD([], HRESULT, 'InsertEntry',
              ( ['in'], c_uint, 'before' ),
              ( ['in'], POINTER(IUIAutomationProxyFactoryEntry), 'factory' )),
    COMMETHOD([], HRESULT, 'RemoveEntry',
              ( ['in'], c_uint, 'index' )),
    COMMETHOD([], HRESULT, 'ClearTable'),
    COMMETHOD([], HRESULT, 'RestoreDefaultTable'),
]
################################################################
## code template for IUIAutomationProxyFactoryMapping implementation
##class IUIAutomationProxyFactoryMapping_Impl(object):
##    @property
##    def count(self):
##        '-no docstring-'
##        #return count
##
##    def GetTable(self):
##        '-no docstring-'
##        #return table
##
##    def GetEntry(self, index):
##        '-no docstring-'
##        #return entry
##
##    def SetTable(self, factoryList):
##        '-no docstring-'
##        #return 
##
##    def InsertEntries(self, before, factoryList):
##        '-no docstring-'
##        #return 
##
##    def InsertEntry(self, before, factory):
##        '-no docstring-'
##        #return 
##
##    def RemoveEntry(self, index):
##        '-no docstring-'
##        #return 
##
##    def ClearTable(self):
##        '-no docstring-'
##        #return 
##
##    def RestoreDefaultTable(self):
##        '-no docstring-'
##        #return 
##

class IUIAutomationSynchronizedInputPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{2233BE0B-AFB7-448B-9FDA-3B378AA5EAE1}')
    _idlflags_ = []

# values for enumeration 'SynchronizedInputType'
SynchronizedInputType_KeyUp = 1
SynchronizedInputType_KeyDown = 2
SynchronizedInputType_LeftMouseUp = 4
SynchronizedInputType_LeftMouseDown = 8
SynchronizedInputType_RightMouseUp = 16
SynchronizedInputType_RightMouseDown = 32
SynchronizedInputType = c_int # enum
IUIAutomationSynchronizedInputPattern._methods_ = [
    COMMETHOD([], HRESULT, 'StartListening',
              ( ['in'], SynchronizedInputType, 'inputType' )),
    COMMETHOD([], HRESULT, 'Cancel'),
]
################################################################
## code template for IUIAutomationSynchronizedInputPattern implementation
##class IUIAutomationSynchronizedInputPattern_Impl(object):
##    def StartListening(self, inputType):
##        '-no docstring-'
##        #return 
##
##    def Cancel(self):
##        '-no docstring-'
##        #return 
##

class IUIAutomationTablePattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{620E691C-EA96-4710-A850-754B24CE2417}')
    _idlflags_ = []

# values for enumeration 'RowOrColumnMajor'
RowOrColumnMajor_RowMajor = 0
RowOrColumnMajor_ColumnMajor = 1
RowOrColumnMajor_Indeterminate = 2
RowOrColumnMajor = c_int # enum
IUIAutomationTablePattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetCurrentRowHeaders',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentColumnHeaders',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRowOrColumnMajor',
              ( ['out', 'retval'], POINTER(RowOrColumnMajor), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedRowHeaders',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedColumnHeaders',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRowOrColumnMajor',
              ( ['out', 'retval'], POINTER(RowOrColumnMajor), 'retVal' )),
]
################################################################
## code template for IUIAutomationTablePattern implementation
##class IUIAutomationTablePattern_Impl(object):
##    def GetCurrentRowHeaders(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentColumnHeaders(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentRowOrColumnMajor(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedRowHeaders(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedColumnHeaders(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedRowOrColumnMajor(self):
##        '-no docstring-'
##        #return retVal
##

IUIAutomationEventHandlerGroup._methods_ = [
    COMMETHOD([], HRESULT, 'AddActiveTextPositionChangedEventHandler',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationActiveTextPositionChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddAutomationEventHandler',
              ( ['in'], c_int, 'eventId' ),
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddChangesEventHandler',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(c_int), 'changeTypes' ),
              ( ['in'], c_int, 'changesCount' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationChangesEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddNotificationEventHandler',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationNotificationEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddPropertyChangedEventHandler',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationPropertyChangedEventHandler), 'handler' ),
              ( ['in'], POINTER(c_int), 'propertyArray' ),
              ( ['in'], c_int, 'propertyCount' )),
    COMMETHOD([], HRESULT, 'AddStructureChangedEventHandler',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationStructureChangedEventHandler), 'handler' )),
    COMMETHOD([], HRESULT, 'AddTextEditTextChangedEventHandler',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], TextEditChangeType, 'TextEditChangeType' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], POINTER(IUIAutomationTextEditTextChangedEventHandler), 'handler' )),
]
################################################################
## code template for IUIAutomationEventHandlerGroup implementation
##class IUIAutomationEventHandlerGroup_Impl(object):
##    def AddActiveTextPositionChangedEventHandler(self, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def AddAutomationEventHandler(self, eventId, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def AddChangesEventHandler(self, scope, changeTypes, changesCount, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def AddNotificationEventHandler(self, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def AddPropertyChangedEventHandler(self, scope, cacheRequest, handler, propertyArray, propertyCount):
##        '-no docstring-'
##        #return 
##
##    def AddStructureChangedEventHandler(self, scope, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##
##    def AddTextEditTextChangedEventHandler(self, scope, TextEditChangeType, cacheRequest, handler):
##        '-no docstring-'
##        #return 
##

class IUIAutomationObjectModelPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{71C284B3-C14D-4D14-981E-19751B0D756D}')
    _idlflags_ = []
IUIAutomationObjectModelPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetUnderlyingObjectModel',
              ( ['out', 'retval'], POINTER(POINTER(IUnknown)), 'retVal' )),
]
################################################################
## code template for IUIAutomationObjectModelPattern implementation
##class IUIAutomationObjectModelPattern_Impl(object):
##    def GetUnderlyingObjectModel(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationRangeValuePattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{59213F4F-7346-49E5-B120-80555987A148}')
    _idlflags_ = []
IUIAutomationRangeValuePattern._methods_ = [
    COMMETHOD([], HRESULT, 'SetValue',
              ( ['in'], c_double, 'val' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentValue',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentIsReadOnly',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentMaximum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentMinimum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLargeChange',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentSmallChange',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedValue',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsReadOnly',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedMaximum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedMinimum',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLargeChange',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedSmallChange',
              ( ['out', 'retval'], POINTER(c_double), 'retVal' )),
]
################################################################
## code template for IUIAutomationRangeValuePattern implementation
##class IUIAutomationRangeValuePattern_Impl(object):
##    def SetValue(self, val):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentValue(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentIsReadOnly(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentMaximum(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentMinimum(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentLargeChange(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentSmallChange(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedValue(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsReadOnly(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedMaximum(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedMinimum(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLargeChange(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedSmallChange(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationBoolCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{1B4E1F2E-75EB-4D0B-8952-5A69988E2307}')
    _idlflags_ = []
IUIAutomationBoolCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'BooleanValue',
              ( ['out', 'retval'], POINTER(c_int), 'boolVal' )),
]
################################################################
## code template for IUIAutomationBoolCondition implementation
##class IUIAutomationBoolCondition_Impl(object):
##    @property
##    def BooleanValue(self):
##        '-no docstring-'
##        #return boolVal
##

class IUIAutomationPropertyCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{99EBF2CB-5578-4267-9AD4-AFD6EA77E94B}')
    _idlflags_ = []
IUIAutomationPropertyCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'propertyId',
              ( ['out', 'retval'], POINTER(c_int), 'propertyId' )),
    COMMETHOD(['propget'], HRESULT, 'PropertyValue',
              ( ['out', 'retval'], POINTER(VARIANT), 'PropertyValue' )),
    COMMETHOD(['propget'], HRESULT, 'PropertyConditionFlags',
              ( ['out', 'retval'], POINTER(PropertyConditionFlags), 'flags' )),
]
################################################################
## code template for IUIAutomationPropertyCondition implementation
##class IUIAutomationPropertyCondition_Impl(object):
##    @property
##    def propertyId(self):
##        '-no docstring-'
##        #return propertyId
##
##    @property
##    def PropertyValue(self):
##        '-no docstring-'
##        #return PropertyValue
##
##    @property
##    def PropertyConditionFlags(self):
##        '-no docstring-'
##        #return flags
##

class IUIAutomationAndCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{A7D0AF36-B912-45FE-9855-091DDC174AEC}')
    _idlflags_ = []
IUIAutomationAndCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ChildCount',
              ( ['out', 'retval'], POINTER(c_int), 'ChildCount' )),
    COMMETHOD([], HRESULT, 'GetChildrenAsNativeArray',
              ( ['out'], POINTER(POINTER(POINTER(IUIAutomationCondition))), 'childArray' ),
              ( ['out'], POINTER(c_int), 'childArrayCount' )),
    COMMETHOD([], HRESULT, 'GetChildren',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(POINTER(IUIAutomationCondition))), 'childArray' )),
]
################################################################
## code template for IUIAutomationAndCondition implementation
##class IUIAutomationAndCondition_Impl(object):
##    @property
##    def ChildCount(self):
##        '-no docstring-'
##        #return ChildCount
##
##    def GetChildrenAsNativeArray(self):
##        '-no docstring-'
##        #return childArray, childArrayCount
##
##    def GetChildren(self):
##        '-no docstring-'
##        #return childArray
##

class IUIAutomationOrCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{8753F032-3DB1-47B5-A1FC-6E34A266C712}')
    _idlflags_ = []
IUIAutomationOrCondition._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'ChildCount',
              ( ['out', 'retval'], POINTER(c_int), 'ChildCount' )),
    COMMETHOD([], HRESULT, 'GetChildrenAsNativeArray',
              ( ['out'], POINTER(POINTER(POINTER(IUIAutomationCondition))), 'childArray' ),
              ( ['out'], POINTER(c_int), 'childArrayCount' )),
    COMMETHOD([], HRESULT, 'GetChildren',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(POINTER(IUIAutomationCondition))), 'childArray' )),
]
################################################################
## code template for IUIAutomationOrCondition implementation
##class IUIAutomationOrCondition_Impl(object):
##    @property
##    def ChildCount(self):
##        '-no docstring-'
##        #return ChildCount
##
##    def GetChildrenAsNativeArray(self):
##        '-no docstring-'
##        #return childArray, childArrayCount
##
##    def GetChildren(self):
##        '-no docstring-'
##        #return childArray
##

class IUIAutomationNotCondition(IUIAutomationCondition):
    _case_insensitive_ = True
    _iid_ = GUID('{F528B657-847B-498C-8896-D52B565407A1}')
    _idlflags_ = []
IUIAutomationNotCondition._methods_ = [
    COMMETHOD([], HRESULT, 'GetChild',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
]
################################################################
## code template for IUIAutomationNotCondition implementation
##class IUIAutomationNotCondition_Impl(object):
##    def GetChild(self):
##        '-no docstring-'
##        #return condition
##

IUIAutomationTreeWalker._methods_ = [
    COMMETHOD([], HRESULT, 'GetParentElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'parent' )),
    COMMETHOD([], HRESULT, 'GetFirstChildElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'first' )),
    COMMETHOD([], HRESULT, 'GetLastChildElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'last' )),
    COMMETHOD([], HRESULT, 'GetNextSiblingElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'next' )),
    COMMETHOD([], HRESULT, 'GetPreviousSiblingElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'previous' )),
    COMMETHOD([], HRESULT, 'NormalizeElement',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'normalized' )),
    COMMETHOD([], HRESULT, 'GetParentElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'parent' )),
    COMMETHOD([], HRESULT, 'GetFirstChildElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'first' )),
    COMMETHOD([], HRESULT, 'GetLastChildElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'last' )),
    COMMETHOD([], HRESULT, 'GetNextSiblingElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'next' )),
    COMMETHOD([], HRESULT, 'GetPreviousSiblingElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'previous' )),
    COMMETHOD([], HRESULT, 'NormalizeElementBuildCache',
              ( ['in'], POINTER(IUIAutomationElement), 'element' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'normalized' )),
    COMMETHOD(['propget'], HRESULT, 'condition',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationCondition)), 'condition' )),
]
################################################################
## code template for IUIAutomationTreeWalker implementation
##class IUIAutomationTreeWalker_Impl(object):
##    def GetParentElement(self, element):
##        '-no docstring-'
##        #return parent
##
##    def GetFirstChildElement(self, element):
##        '-no docstring-'
##        #return first
##
##    def GetLastChildElement(self, element):
##        '-no docstring-'
##        #return last
##
##    def GetNextSiblingElement(self, element):
##        '-no docstring-'
##        #return next
##
##    def GetPreviousSiblingElement(self, element):
##        '-no docstring-'
##        #return previous
##
##    def NormalizeElement(self, element):
##        '-no docstring-'
##        #return normalized
##
##    def GetParentElementBuildCache(self, element, cacheRequest):
##        '-no docstring-'
##        #return parent
##
##    def GetFirstChildElementBuildCache(self, element, cacheRequest):
##        '-no docstring-'
##        #return first
##
##    def GetLastChildElementBuildCache(self, element, cacheRequest):
##        '-no docstring-'
##        #return last
##
##    def GetNextSiblingElementBuildCache(self, element, cacheRequest):
##        '-no docstring-'
##        #return next
##
##    def GetPreviousSiblingElementBuildCache(self, element, cacheRequest):
##        '-no docstring-'
##        #return previous
##
##    def NormalizeElementBuildCache(self, element, cacheRequest):
##        '-no docstring-'
##        #return normalized
##
##    @property
##    def condition(self):
##        '-no docstring-'
##        #return condition
##

class IUIAutomationScrollItemPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{B488300F-D015-4F19-9C29-BB595E3645EF}')
    _idlflags_ = []
IUIAutomationScrollItemPattern._methods_ = [
    COMMETHOD([], HRESULT, 'ScrollIntoView'),
]
################################################################
## code template for IUIAutomationScrollItemPattern implementation
##class IUIAutomationScrollItemPattern_Impl(object):
##    def ScrollIntoView(self):
##        '-no docstring-'
##        #return 
##

class IUIAutomationTextRangeArray(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{CE4AE76A-E717-4C98-81EA-47371D028EB6}')
    _idlflags_ = []
IUIAutomationTextRangeArray._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'Length',
              ( ['out', 'retval'], POINTER(c_int), 'Length' )),
    COMMETHOD([], HRESULT, 'GetElement',
              ( ['in'], c_int, 'index' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'element' )),
]
################################################################
## code template for IUIAutomationTextRangeArray implementation
##class IUIAutomationTextRangeArray_Impl(object):
##    @property
##    def Length(self):
##        '-no docstring-'
##        #return Length
##
##    def GetElement(self, index):
##        '-no docstring-'
##        #return element
##

class CUIAutomation(CoClass):
    'The Central Class for UIAutomation'
    _reg_clsid_ = GUID('{FF48DBA4-60EF-4201-AA87-54103EEF594E}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{944DE083-8FB8-45CF-BCB7-C477ACB2F897}', 1, 0)
CUIAutomation._com_interfaces_ = [IUIAutomation]

class IUIAutomationElement4(IUIAutomationElement3):
    _case_insensitive_ = True
    _iid_ = GUID('{3B6E233C-52FB-4063-A4C9-77C075C2A06B}')
    _idlflags_ = []
IUIAutomationElement4._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentPositionInSet',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentSizeOfSet',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLevel',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAnnotationTypes',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentAnnotationObjects',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedPositionInSet',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedSizeOfSet',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLevel',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAnnotationTypes',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedAnnotationObjects',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'retVal' )),
]
################################################################
## code template for IUIAutomationElement4 implementation
##class IUIAutomationElement4_Impl(object):
##    @property
##    def CurrentPositionInSet(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentSizeOfSet(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentLevel(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAnnotationTypes(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentAnnotationObjects(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedPositionInSet(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedSizeOfSet(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLevel(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAnnotationTypes(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedAnnotationObjects(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationTextPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{32EBA289-3583-42C9-9C59-3B6D9A1E9B6A}')
    _idlflags_ = []

# values for enumeration 'SupportedTextSelection'
SupportedTextSelection_None = 0
SupportedTextSelection_Single = 1
SupportedTextSelection_Multiple = 2
SupportedTextSelection = c_int # enum
IUIAutomationTextPattern._methods_ = [
    COMMETHOD([], HRESULT, 'RangeFromPoint',
              ( ['in'], tagPOINT, 'pt' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD([], HRESULT, 'RangeFromChild',
              ( ['in'], POINTER(IUIAutomationElement), 'child' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD([], HRESULT, 'GetSelection',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRangeArray)), 'ranges' )),
    COMMETHOD([], HRESULT, 'GetVisibleRanges',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRangeArray)), 'ranges' )),
    COMMETHOD(['propget'], HRESULT, 'DocumentRange',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD(['propget'], HRESULT, 'SupportedTextSelection',
              ( ['out', 'retval'], POINTER(SupportedTextSelection), 'SupportedTextSelection' )),
]
################################################################
## code template for IUIAutomationTextPattern implementation
##class IUIAutomationTextPattern_Impl(object):
##    def RangeFromPoint(self, pt):
##        '-no docstring-'
##        #return range
##
##    def RangeFromChild(self, child):
##        '-no docstring-'
##        #return range
##
##    def GetSelection(self):
##        '-no docstring-'
##        #return ranges
##
##    def GetVisibleRanges(self):
##        '-no docstring-'
##        #return ranges
##
##    @property
##    def DocumentRange(self):
##        '-no docstring-'
##        #return range
##
##    @property
##    def SupportedTextSelection(self):
##        '-no docstring-'
##        #return SupportedTextSelection
##

class CUIAutomation8(CoClass):
    'The Central Class for UIAutomation8'
    _reg_clsid_ = GUID('{E22AD333-B25F-460C-83D0-0581107395C9}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{944DE083-8FB8-45CF-BCB7-C477ACB2F897}', 1, 0)
CUIAutomation8._com_interfaces_ = [IUIAutomation2, IUIAutomation3, IUIAutomation4, IUIAutomation5, IUIAutomation6]

class IUIAutomationTextPattern2(IUIAutomationTextPattern):
    _case_insensitive_ = True
    _iid_ = GUID('{506A921A-FCC9-409F-B23B-37EB74106872}')
    _idlflags_ = []
IUIAutomationTextPattern2._methods_ = [
    COMMETHOD([], HRESULT, 'RangeFromAnnotation',
              ( ['in'], POINTER(IUIAutomationElement), 'annotation' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD([], HRESULT, 'GetCaretRange',
              ( ['out'], POINTER(c_int), 'isActive' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
]
################################################################
## code template for IUIAutomationTextPattern2 implementation
##class IUIAutomationTextPattern2_Impl(object):
##    def RangeFromAnnotation(self, annotation):
##        '-no docstring-'
##        #return range
##
##    def GetCaretRange(self):
##        '-no docstring-'
##        #return isActive, range
##

class IUIAutomationElement5(IUIAutomationElement4):
    _case_insensitive_ = True
    _iid_ = GUID('{98141C1D-0D0E-4175-BBE2-6BFF455842A7}')
    _idlflags_ = []
IUIAutomationElement5._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentLandmarkType',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentLocalizedLandmarkType',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLandmarkType',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedLocalizedLandmarkType',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
]
################################################################
## code template for IUIAutomationElement5 implementation
##class IUIAutomationElement5_Impl(object):
##    @property
##    def CurrentLandmarkType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentLocalizedLandmarkType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLandmarkType(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedLocalizedLandmarkType(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationTextEditPattern(IUIAutomationTextPattern):
    _case_insensitive_ = True
    _iid_ = GUID('{17E21576-996C-4870-99D9-BFF323380C06}')
    _idlflags_ = []
IUIAutomationTextEditPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetActiveComposition',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
    COMMETHOD([], HRESULT, 'GetConversionTarget',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'range' )),
]
################################################################
## code template for IUIAutomationTextEditPattern implementation
##class IUIAutomationTextEditPattern_Impl(object):
##    def GetActiveComposition(self):
##        '-no docstring-'
##        #return range
##
##    def GetConversionTarget(self):
##        '-no docstring-'
##        #return range
##

class IUIAutomationElement6(IUIAutomationElement5):
    _case_insensitive_ = True
    _iid_ = GUID('{4780D450-8BCA-4977-AFA5-A4A517F555E3}')
    _idlflags_ = []
class IUIAutomationElement7(IUIAutomationElement6):
    _case_insensitive_ = True
    _iid_ = GUID('{204E8572-CFC3-4C11-B0C8-7DA7420750B7}')
    _idlflags_ = []
IUIAutomationElement6._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentFullDescription',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedFullDescription',
              ( ['out', 'retval'], POINTER(BSTR), 'retVal' )),
]
################################################################
## code template for IUIAutomationElement6 implementation
##class IUIAutomationElement6_Impl(object):
##    @property
##    def CurrentFullDescription(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedFullDescription(self):
##        '-no docstring-'
##        #return retVal
##


# values for enumeration 'TreeTraversalOptions'
TreeTraversalOptions_Default = 0
TreeTraversalOptions_PostOrder = 1
TreeTraversalOptions_LastToFirstOrder = 2
TreeTraversalOptions = c_int # enum
IUIAutomationElement7._methods_ = [
    COMMETHOD([], HRESULT, 'FindFirstWithOptions',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], TreeTraversalOptions, 'traversalOptions' ),
              ( ['in'], POINTER(IUIAutomationElement), 'root' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'found' )),
    COMMETHOD([], HRESULT, 'FindAllWithOptions',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], TreeTraversalOptions, 'traversalOptions' ),
              ( ['in'], POINTER(IUIAutomationElement), 'root' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'found' )),
    COMMETHOD([], HRESULT, 'FindFirstWithOptionsBuildCache',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], TreeTraversalOptions, 'traversalOptions' ),
              ( ['in'], POINTER(IUIAutomationElement), 'root' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'found' )),
    COMMETHOD([], HRESULT, 'FindAllWithOptionsBuildCache',
              ( ['in'], TreeScope, 'scope' ),
              ( ['in'], POINTER(IUIAutomationCondition), 'condition' ),
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['in'], TreeTraversalOptions, 'traversalOptions' ),
              ( ['in'], POINTER(IUIAutomationElement), 'root' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'found' )),
    COMMETHOD([], HRESULT, 'GetCurrentMetadataValue',
              ( ['in'], c_int, 'targetId' ),
              ( ['in'], c_int, 'metadataId' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'returnVal' )),
]
################################################################
## code template for IUIAutomationElement7 implementation
##class IUIAutomationElement7_Impl(object):
##    def FindFirstWithOptions(self, scope, condition, traversalOptions, root):
##        '-no docstring-'
##        #return found
##
##    def FindAllWithOptions(self, scope, condition, traversalOptions, root):
##        '-no docstring-'
##        #return found
##
##    def FindFirstWithOptionsBuildCache(self, scope, condition, cacheRequest, traversalOptions, root):
##        '-no docstring-'
##        #return found
##
##    def FindAllWithOptionsBuildCache(self, scope, condition, cacheRequest, traversalOptions, root):
##        '-no docstring-'
##        #return found
##
##    def GetCurrentMetadataValue(self, targetId, metadataId):
##        '-no docstring-'
##        #return returnVal
##

class IUIAutomationCustomNavigationPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{01EA217A-1766-47ED-A6CC-ACF492854B1F}')
    _idlflags_ = []
IUIAutomationCustomNavigationPattern._methods_ = [
    COMMETHOD([], HRESULT, 'Navigate',
              ( ['in'], NavigateDirection, 'direction' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'pRetVal' )),
]
################################################################
## code template for IUIAutomationCustomNavigationPattern implementation
##class IUIAutomationCustomNavigationPattern_Impl(object):
##    def Navigate(self, direction):
##        '-no docstring-'
##        #return pRetVal
##

IUIAutomationActiveTextPositionChangedEventHandler._methods_ = [
    COMMETHOD([], HRESULT, 'HandleActiveTextPositionChangedEvent',
              ( ['in'], POINTER(IUIAutomationElement), 'sender' ),
              ( ['in'], POINTER(IUIAutomationTextRange), 'range' )),
]
################################################################
## code template for IUIAutomationActiveTextPositionChangedEventHandler implementation
##class IUIAutomationActiveTextPositionChangedEventHandler_Impl(object):
##    def HandleActiveTextPositionChangedEvent(self, sender, range):
##        '-no docstring-'
##        #return 
##

class IUIAutomationLegacyIAccessiblePattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{828055AD-355B-4435-86D5-3B51C14A9B1B}')
    _idlflags_ = []
IUIAutomationLegacyIAccessiblePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Select',
              ( [], c_int, 'flagsSelect' )),
    COMMETHOD([], HRESULT, 'DoDefaultAction'),
    COMMETHOD([], HRESULT, 'SetValue',
              ( [], WSTRING, 'szValue' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentChildId',
              ( ['out', 'retval'], POINTER(c_int), 'pRetVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentName',
              ( ['out', 'retval'], POINTER(BSTR), 'pszName' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentValue',
              ( ['out', 'retval'], POINTER(BSTR), 'pszValue' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDescription',
              ( ['out', 'retval'], POINTER(BSTR), 'pszDescription' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRole',
              ( ['out', 'retval'], POINTER(c_ulong), 'pdwRole' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentState',
              ( ['out', 'retval'], POINTER(c_ulong), 'pdwState' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentHelp',
              ( ['out', 'retval'], POINTER(BSTR), 'pszHelp' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentKeyboardShortcut',
              ( ['out', 'retval'], POINTER(BSTR), 'pszKeyboardShortcut' )),
    COMMETHOD([], HRESULT, 'GetCurrentSelection',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'pvarSelectedChildren' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentDefaultAction',
              ( ['out', 'retval'], POINTER(BSTR), 'pszDefaultAction' )),
    COMMETHOD(['propget'], HRESULT, 'CachedChildId',
              ( ['out', 'retval'], POINTER(c_int), 'pRetVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedName',
              ( ['out', 'retval'], POINTER(BSTR), 'pszName' )),
    COMMETHOD(['propget'], HRESULT, 'CachedValue',
              ( ['out', 'retval'], POINTER(BSTR), 'pszValue' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDescription',
              ( ['out', 'retval'], POINTER(BSTR), 'pszDescription' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRole',
              ( ['out', 'retval'], POINTER(c_ulong), 'pdwRole' )),
    COMMETHOD(['propget'], HRESULT, 'CachedState',
              ( ['out', 'retval'], POINTER(c_ulong), 'pdwState' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHelp',
              ( ['out', 'retval'], POINTER(BSTR), 'pszHelp' )),
    COMMETHOD(['propget'], HRESULT, 'CachedKeyboardShortcut',
              ( ['out', 'retval'], POINTER(BSTR), 'pszKeyboardShortcut' )),
    COMMETHOD([], HRESULT, 'GetCachedSelection',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'pvarSelectedChildren' )),
    COMMETHOD(['propget'], HRESULT, 'CachedDefaultAction',
              ( ['out', 'retval'], POINTER(BSTR), 'pszDefaultAction' )),
    COMMETHOD([], HRESULT, 'GetIAccessible',
              ( ['out', 'retval'], POINTER(POINTER(IAccessible)), 'ppAccessible' )),
]
################################################################
## code template for IUIAutomationLegacyIAccessiblePattern implementation
##class IUIAutomationLegacyIAccessiblePattern_Impl(object):
##    def Select(self, flagsSelect):
##        '-no docstring-'
##        #return 
##
##    def DoDefaultAction(self):
##        '-no docstring-'
##        #return 
##
##    def SetValue(self, szValue):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentChildId(self):
##        '-no docstring-'
##        #return pRetVal
##
##    @property
##    def CurrentName(self):
##        '-no docstring-'
##        #return pszName
##
##    @property
##    def CurrentValue(self):
##        '-no docstring-'
##        #return pszValue
##
##    @property
##    def CurrentDescription(self):
##        '-no docstring-'
##        #return pszDescription
##
##    @property
##    def CurrentRole(self):
##        '-no docstring-'
##        #return pdwRole
##
##    @property
##    def CurrentState(self):
##        '-no docstring-'
##        #return pdwState
##
##    @property
##    def CurrentHelp(self):
##        '-no docstring-'
##        #return pszHelp
##
##    @property
##    def CurrentKeyboardShortcut(self):
##        '-no docstring-'
##        #return pszKeyboardShortcut
##
##    def GetCurrentSelection(self):
##        '-no docstring-'
##        #return pvarSelectedChildren
##
##    @property
##    def CurrentDefaultAction(self):
##        '-no docstring-'
##        #return pszDefaultAction
##
##    @property
##    def CachedChildId(self):
##        '-no docstring-'
##        #return pRetVal
##
##    @property
##    def CachedName(self):
##        '-no docstring-'
##        #return pszName
##
##    @property
##    def CachedValue(self):
##        '-no docstring-'
##        #return pszValue
##
##    @property
##    def CachedDescription(self):
##        '-no docstring-'
##        #return pszDescription
##
##    @property
##    def CachedRole(self):
##        '-no docstring-'
##        #return pdwRole
##
##    @property
##    def CachedState(self):
##        '-no docstring-'
##        #return pdwState
##
##    @property
##    def CachedHelp(self):
##        '-no docstring-'
##        #return pszHelp
##
##    @property
##    def CachedKeyboardShortcut(self):
##        '-no docstring-'
##        #return pszKeyboardShortcut
##
##    def GetCachedSelection(self):
##        '-no docstring-'
##        #return pvarSelectedChildren
##
##    @property
##    def CachedDefaultAction(self):
##        '-no docstring-'
##        #return pszDefaultAction
##
##    def GetIAccessible(self):
##        '-no docstring-'
##        #return ppAccessible
##

class IUIAutomationElement8(IUIAutomationElement7):
    _case_insensitive_ = True
    _iid_ = GUID('{8C60217D-5411-4CDE-BCC0-1CEDA223830C}')
    _idlflags_ = []
IUIAutomationElement8._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentHeadingLevel',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedHeadingLevel',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationElement8 implementation
##class IUIAutomationElement8_Impl(object):
##    @property
##    def CurrentHeadingLevel(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedHeadingLevel(self):
##        '-no docstring-'
##        #return retVal
##

class IUIAutomationElement9(IUIAutomationElement8):
    _case_insensitive_ = True
    _iid_ = GUID('{39325FAC-039D-440E-A3A3-5EB81A5CECC3}')
    _idlflags_ = []
IUIAutomationElement9._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentIsDialog',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedIsDialog',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationElement9 implementation
##class IUIAutomationElement9_Impl(object):
##    @property
##    def CurrentIsDialog(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedIsDialog(self):
##        '-no docstring-'
##        #return retVal
##

UIA_IsDropTargetPatternAvailablePropertyId = 30141 # Constant c_int
UIA_Transform2ZoomMinimumPropertyId = 30146 # Constant c_int
UIA_DropTargetDropTargetEffectPropertyId = 30142 # Constant c_int
UIA_DragGrabbedItemsPropertyId = 30144 # Constant c_int
UIA_DropTargetDropTargetEffectsPropertyId = 30143 # Constant c_int
UIA_Transform2ZoomLevelPropertyId = 30145 # Constant c_int
UIA_NativeWindowHandlePropertyId = 30020 # Constant c_int
UIA_ItemTypePropertyId = 30021 # Constant c_int
UIA_IsOffscreenPropertyId = 30022 # Constant c_int
UIA_OrientationPropertyId = 30023 # Constant c_int
UIA_FrameworkIdPropertyId = 30024 # Constant c_int
UIA_IsRequiredForFormPropertyId = 30025 # Constant c_int
UIA_ItemStatusPropertyId = 30026 # Constant c_int
UIA_IsDockPatternAvailablePropertyId = 30027 # Constant c_int
UIA_IsExpandCollapsePatternAvailablePropertyId = 30028 # Constant c_int
UIA_IsGridItemPatternAvailablePropertyId = 30029 # Constant c_int
UIA_IsGridPatternAvailablePropertyId = 30030 # Constant c_int
UIA_IsInvokePatternAvailablePropertyId = 30031 # Constant c_int
UIA_IsMultipleViewPatternAvailablePropertyId = 30032 # Constant c_int
UIA_IsRangeValuePatternAvailablePropertyId = 30033 # Constant c_int
UIA_IsScrollPatternAvailablePropertyId = 30034 # Constant c_int
UIA_IsScrollItemPatternAvailablePropertyId = 30035 # Constant c_int
UIA_IsSelectionItemPatternAvailablePropertyId = 30036 # Constant c_int
UIA_IsSelectionPatternAvailablePropertyId = 30037 # Constant c_int
UIA_IsTablePatternAvailablePropertyId = 30038 # Constant c_int
UIA_IsTableItemPatternAvailablePropertyId = 30039 # Constant c_int
UIA_IsTextPatternAvailablePropertyId = 30040 # Constant c_int

# values for enumeration 'TextPatternRangeEndpoint'
TextPatternRangeEndpoint_Start = 0
TextPatternRangeEndpoint_End = 1
TextPatternRangeEndpoint = c_int # enum

# values for enumeration 'TextUnit'
TextUnit_Character = 0
TextUnit_Format = 1
TextUnit_Word = 2
TextUnit_Line = 3
TextUnit_Paragraph = 4
TextUnit_Page = 5
TextUnit_Document = 6
TextUnit = c_int # enum
IUIAutomationTextRange._methods_ = [
    COMMETHOD([], HRESULT, 'Clone',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'clonedRange' )),
    COMMETHOD([], HRESULT, 'Compare',
              ( ['in'], POINTER(IUIAutomationTextRange), 'range' ),
              ( ['out', 'retval'], POINTER(c_int), 'areSame' )),
    COMMETHOD([], HRESULT, 'CompareEndpoints',
              ( ['in'], TextPatternRangeEndpoint, 'srcEndPoint' ),
              ( ['in'], POINTER(IUIAutomationTextRange), 'range' ),
              ( ['in'], TextPatternRangeEndpoint, 'targetEndPoint' ),
              ( ['out', 'retval'], POINTER(c_int), 'compValue' )),
    COMMETHOD([], HRESULT, 'ExpandToEnclosingUnit',
              ( ['in'], TextUnit, 'TextUnit' )),
    COMMETHOD([], HRESULT, 'FindAttribute',
              ( ['in'], c_int, 'attr' ),
              ( ['in'], VARIANT, 'val' ),
              ( ['in'], c_int, 'backward' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'found' )),
    COMMETHOD([], HRESULT, 'FindText',
              ( ['in'], BSTR, 'text' ),
              ( ['in'], c_int, 'backward' ),
              ( ['in'], c_int, 'ignoreCase' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationTextRange)), 'found' )),
    COMMETHOD([], HRESULT, 'GetAttributeValue',
              ( ['in'], c_int, 'attr' ),
              ( ['out', 'retval'], POINTER(VARIANT), 'value' )),
    COMMETHOD([], HRESULT, 'GetBoundingRectangles',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_double)), 'boundingRects' )),
    COMMETHOD([], HRESULT, 'GetEnclosingElement',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'enclosingElement' )),
    COMMETHOD([], HRESULT, 'GetText',
              ( ['in'], c_int, 'maxLength' ),
              ( ['out', 'retval'], POINTER(BSTR), 'text' )),
    COMMETHOD([], HRESULT, 'Move',
              ( ['in'], TextUnit, 'unit' ),
              ( ['in'], c_int, 'count' ),
              ( ['out', 'retval'], POINTER(c_int), 'moved' )),
    COMMETHOD([], HRESULT, 'MoveEndpointByUnit',
              ( ['in'], TextPatternRangeEndpoint, 'endpoint' ),
              ( ['in'], TextUnit, 'unit' ),
              ( ['in'], c_int, 'count' ),
              ( ['out', 'retval'], POINTER(c_int), 'moved' )),
    COMMETHOD([], HRESULT, 'MoveEndpointByRange',
              ( ['in'], TextPatternRangeEndpoint, 'srcEndPoint' ),
              ( ['in'], POINTER(IUIAutomationTextRange), 'range' ),
              ( ['in'], TextPatternRangeEndpoint, 'targetEndPoint' )),
    COMMETHOD([], HRESULT, 'Select'),
    COMMETHOD([], HRESULT, 'AddToSelection'),
    COMMETHOD([], HRESULT, 'RemoveFromSelection'),
    COMMETHOD([], HRESULT, 'ScrollIntoView',
              ( ['in'], c_int, 'alignToTop' )),
    COMMETHOD([], HRESULT, 'GetChildren',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'children' )),
]
################################################################
## code template for IUIAutomationTextRange implementation
##class IUIAutomationTextRange_Impl(object):
##    def Clone(self):
##        '-no docstring-'
##        #return clonedRange
##
##    def Compare(self, range):
##        '-no docstring-'
##        #return areSame
##
##    def CompareEndpoints(self, srcEndPoint, range, targetEndPoint):
##        '-no docstring-'
##        #return compValue
##
##    def ExpandToEnclosingUnit(self, TextUnit):
##        '-no docstring-'
##        #return 
##
##    def FindAttribute(self, attr, val, backward):
##        '-no docstring-'
##        #return found
##
##    def FindText(self, text, backward, ignoreCase):
##        '-no docstring-'
##        #return found
##
##    def GetAttributeValue(self, attr):
##        '-no docstring-'
##        #return value
##
##    def GetBoundingRectangles(self):
##        '-no docstring-'
##        #return boundingRects
##
##    def GetEnclosingElement(self):
##        '-no docstring-'
##        #return enclosingElement
##
##    def GetText(self, maxLength):
##        '-no docstring-'
##        #return text
##
##    def Move(self, unit, count):
##        '-no docstring-'
##        #return moved
##
##    def MoveEndpointByUnit(self, endpoint, unit, count):
##        '-no docstring-'
##        #return moved
##
##    def MoveEndpointByRange(self, srcEndPoint, range, targetEndPoint):
##        '-no docstring-'
##        #return 
##
##    def Select(self):
##        '-no docstring-'
##        #return 
##
##    def AddToSelection(self):
##        '-no docstring-'
##        #return 
##
##    def RemoveFromSelection(self):
##        '-no docstring-'
##        #return 
##
##    def ScrollIntoView(self, alignToTop):
##        '-no docstring-'
##        #return 
##
##    def GetChildren(self):
##        '-no docstring-'
##        #return children
##

UIA_IsTogglePatternAvailablePropertyId = 30041 # Constant c_int
UIA_IsTransformPatternAvailablePropertyId = 30042 # Constant c_int
UIA_IsValuePatternAvailablePropertyId = 30043 # Constant c_int
UIA_IsWindowPatternAvailablePropertyId = 30044 # Constant c_int
UIA_ValueValuePropertyId = 30045 # Constant c_int
UIA_ValueIsReadOnlyPropertyId = 30046 # Constant c_int
UIA_RangeValueValuePropertyId = 30047 # Constant c_int
UIA_RangeValueIsReadOnlyPropertyId = 30048 # Constant c_int
UIA_RangeValueMinimumPropertyId = 30049 # Constant c_int
UIA_RangeValueMaximumPropertyId = 30050 # Constant c_int
UIA_RangeValueLargeChangePropertyId = 30051 # Constant c_int
UIA_RangeValueSmallChangePropertyId = 30052 # Constant c_int
UIA_ScrollHorizontalScrollPercentPropertyId = 30053 # Constant c_int
UIA_ScrollHorizontalViewSizePropertyId = 30054 # Constant c_int
UIA_ScrollVerticalScrollPercentPropertyId = 30055 # Constant c_int
UIA_ScrollVerticalViewSizePropertyId = 30056 # Constant c_int
UIA_ScrollHorizontallyScrollablePropertyId = 30057 # Constant c_int
UIA_ScrollVerticallyScrollablePropertyId = 30058 # Constant c_int
UIA_SelectionSelectionPropertyId = 30059 # Constant c_int
UIA_SelectionCanSelectMultiplePropertyId = 30060 # Constant c_int
UIA_SelectionIsSelectionRequiredPropertyId = 30061 # Constant c_int
UIA_GridRowCountPropertyId = 30062 # Constant c_int
UIA_GridColumnCountPropertyId = 30063 # Constant c_int
UIA_GridItemRowPropertyId = 30064 # Constant c_int
UIA_GridItemColumnPropertyId = 30065 # Constant c_int
UIA_GridItemRowSpanPropertyId = 30066 # Constant c_int
UIA_GridItemColumnSpanPropertyId = 30067 # Constant c_int
UIA_GridItemContainingGridPropertyId = 30068 # Constant c_int
UIA_DockDockPositionPropertyId = 30069 # Constant c_int
UIA_ExpandCollapseExpandCollapseStatePropertyId = 30070 # Constant c_int
UIA_MultipleViewCurrentViewPropertyId = 30071 # Constant c_int
UIA_MultipleViewSupportedViewsPropertyId = 30072 # Constant c_int
UIA_WindowCanMaximizePropertyId = 30073 # Constant c_int
UIA_WindowCanMinimizePropertyId = 30074 # Constant c_int
UIA_WindowWindowVisualStatePropertyId = 30075 # Constant c_int
UIA_WindowWindowInteractionStatePropertyId = 30076 # Constant c_int
UIA_WindowIsModalPropertyId = 30077 # Constant c_int
UIA_WindowIsTopmostPropertyId = 30078 # Constant c_int
UIA_SelectionItemIsSelectedPropertyId = 30079 # Constant c_int
UIA_SelectionItemSelectionContainerPropertyId = 30080 # Constant c_int
UIA_TableRowHeadersPropertyId = 30081 # Constant c_int
UIA_TableColumnHeadersPropertyId = 30082 # Constant c_int
UIA_TableRowOrColumnMajorPropertyId = 30083 # Constant c_int
UIA_TableItemRowHeaderItemsPropertyId = 30084 # Constant c_int
UIA_TableItemColumnHeaderItemsPropertyId = 30085 # Constant c_int
UIA_ToggleToggleStatePropertyId = 30086 # Constant c_int
UIA_TransformCanMovePropertyId = 30087 # Constant c_int
UIA_TransformCanResizePropertyId = 30088 # Constant c_int
UIA_TransformCanRotatePropertyId = 30089 # Constant c_int
UIA_IsLegacyIAccessiblePatternAvailablePropertyId = 30090 # Constant c_int
UIA_LegacyIAccessibleChildIdPropertyId = 30091 # Constant c_int
UIA_LegacyIAccessibleNamePropertyId = 30092 # Constant c_int
UIA_LegacyIAccessibleValuePropertyId = 30093 # Constant c_int
UIA_LegacyIAccessibleDescriptionPropertyId = 30094 # Constant c_int
UIA_LegacyIAccessibleRolePropertyId = 30095 # Constant c_int
UIA_LegacyIAccessibleStatePropertyId = 30096 # Constant c_int
UIA_LegacyIAccessibleHelpPropertyId = 30097 # Constant c_int
UIA_LegacyIAccessibleKeyboardShortcutPropertyId = 30098 # Constant c_int
UIA_LegacyIAccessibleSelectionPropertyId = 30099 # Constant c_int
UIA_LegacyIAccessibleDefaultActionPropertyId = 30100 # Constant c_int
UIA_AriaRolePropertyId = 30101 # Constant c_int
UIA_AriaPropertiesPropertyId = 30102 # Constant c_int
UIA_IsDataValidForFormPropertyId = 30103 # Constant c_int
UIA_ControllerForPropertyId = 30104 # Constant c_int
UIA_DescribedByPropertyId = 30105 # Constant c_int
UIA_FlowsToPropertyId = 30106 # Constant c_int
UIA_ProviderDescriptionPropertyId = 30107 # Constant c_int
UIA_IsItemContainerPatternAvailablePropertyId = 30108 # Constant c_int
UIA_IsVirtualizedItemPatternAvailablePropertyId = 30109 # Constant c_int
UIA_IsSynchronizedInputPatternAvailablePropertyId = 30110 # Constant c_int
UIA_OptimizeForVisualContentPropertyId = 30111 # Constant c_int
UIA_IsObjectModelPatternAvailablePropertyId = 30112 # Constant c_int
UIA_AnnotationAnnotationTypeIdPropertyId = 30113 # Constant c_int
UIA_AnnotationAnnotationTypeNamePropertyId = 30114 # Constant c_int
UIA_AnnotationAuthorPropertyId = 30115 # Constant c_int
UIA_AnnotationDateTimePropertyId = 30116 # Constant c_int
UIA_AnnotationTargetPropertyId = 30117 # Constant c_int
UIA_IsAnnotationPatternAvailablePropertyId = 30118 # Constant c_int
UIA_IsTextPattern2AvailablePropertyId = 30119 # Constant c_int
UIA_StylesStyleIdPropertyId = 30120 # Constant c_int
UIA_StylesStyleNamePropertyId = 30121 # Constant c_int
UIA_StylesFillColorPropertyId = 30122 # Constant c_int
class IUIAutomationTextRange2(IUIAutomationTextRange):
    _case_insensitive_ = True
    _iid_ = GUID('{BB9B40E0-5E04-46BD-9BE0-4B601B9AFAD4}')
    _idlflags_ = []
IUIAutomationTextRange2._methods_ = [
    COMMETHOD([], HRESULT, 'ShowContextMenu'),
]
################################################################
## code template for IUIAutomationTextRange2 implementation
##class IUIAutomationTextRange2_Impl(object):
##    def ShowContextMenu(self):
##        '-no docstring-'
##        #return 
##

UIA_StylesFillPatternStylePropertyId = 30123 # Constant c_int
UIA_StylesShapePropertyId = 30124 # Constant c_int
UIA_StylesFillPatternColorPropertyId = 30125 # Constant c_int
UIA_StylesExtendedPropertiesPropertyId = 30126 # Constant c_int
class IUIAutomationTextRange3(IUIAutomationTextRange2):
    _case_insensitive_ = True
    _iid_ = GUID('{6A315D69-5512-4C2E-85F0-53FCE6DD4BC2}')
    _idlflags_ = []
IUIAutomationTextRange3._methods_ = [
    COMMETHOD([], HRESULT, 'GetEnclosingElementBuildCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'enclosingElement' )),
    COMMETHOD([], HRESULT, 'GetChildrenBuildCache',
              ( ['in'], POINTER(IUIAutomationCacheRequest), 'cacheRequest' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElementArray)), 'children' )),
    COMMETHOD([], HRESULT, 'GetAttributeValues',
              ( ['in'], POINTER(c_int), 'attributeIds' ),
              ( ['in'], c_int, 'attributeIdCount' ),
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(VARIANT)), 'attributeValues' )),
]
################################################################
## code template for IUIAutomationTextRange3 implementation
##class IUIAutomationTextRange3_Impl(object):
##    def GetEnclosingElementBuildCache(self, cacheRequest):
##        '-no docstring-'
##        #return enclosingElement
##
##    def GetChildrenBuildCache(self, cacheRequest):
##        '-no docstring-'
##        #return children
##
##    def GetAttributeValues(self, attributeIds, attributeIdCount):
##        '-no docstring-'
##        #return attributeValues
##

UIA_IsStylesPatternAvailablePropertyId = 30127 # Constant c_int
UIA_IsSpreadsheetPatternAvailablePropertyId = 30128 # Constant c_int
UIA_SpreadsheetItemFormulaPropertyId = 30129 # Constant c_int
UIA_SpreadsheetItemAnnotationObjectsPropertyId = 30130 # Constant c_int
UIA_SpreadsheetItemAnnotationTypesPropertyId = 30131 # Constant c_int
UIA_IsSpreadsheetItemPatternAvailablePropertyId = 30132 # Constant c_int
UIA_Transform2CanZoomPropertyId = 30133 # Constant c_int
UIA_IsTransformPattern2AvailablePropertyId = 30134 # Constant c_int
UIA_LiveSettingPropertyId = 30135 # Constant c_int
UIA_IsTextChildPatternAvailablePropertyId = 30136 # Constant c_int
UIA_IsDragPatternAvailablePropertyId = 30137 # Constant c_int
UIA_DragIsGrabbedPropertyId = 30138 # Constant c_int
UIA_DragDropEffectPropertyId = 30139 # Constant c_int
UIA_DragDropEffectsPropertyId = 30140 # Constant c_int
AnnotationType_MoveChange = 60013 # Constant c_int
AnnotationType_Highlighted = 60008 # Constant c_int
AnnotationType_InsertionChange = 60011 # Constant c_int
AnnotationType_Footnote = 60010 # Constant c_int
AnnotationType_Endnote = 60009 # Constant c_int
AnnotationType_DeletionChange = 60012 # Constant c_int
UIA_Transform2ZoomMaximumPropertyId = 30147 # Constant c_int
UIA_FlowsFromPropertyId = 30148 # Constant c_int
UIA_IsTextEditPatternAvailablePropertyId = 30149 # Constant c_int
UIA_IsPeripheralPropertyId = 30150 # Constant c_int
UIA_IsCustomNavigationPatternAvailablePropertyId = 30151 # Constant c_int
UIA_PositionInSetPropertyId = 30152 # Constant c_int
UIA_SizeOfSetPropertyId = 30153 # Constant c_int
UIA_LevelPropertyId = 30154 # Constant c_int
UIA_AnnotationTypesPropertyId = 30155 # Constant c_int
UIA_AnnotationObjectsPropertyId = 30156 # Constant c_int
UIA_LandmarkTypePropertyId = 30157 # Constant c_int
UIA_LocalizedLandmarkTypePropertyId = 30158 # Constant c_int
UIA_FullDescriptionPropertyId = 30159 # Constant c_int
UIA_FillColorPropertyId = 30160 # Constant c_int
UIA_OutlineColorPropertyId = 30161 # Constant c_int
UIA_FillTypePropertyId = 30162 # Constant c_int
UIA_VisualEffectsPropertyId = 30163 # Constant c_int
UIA_OutlineThicknessPropertyId = 30164 # Constant c_int
UIA_CenterPointPropertyId = 30165 # Constant c_int
UIA_RotationPropertyId = 30166 # Constant c_int
UIA_SizePropertyId = 30167 # Constant c_int
UIA_IsSelectionPattern2AvailablePropertyId = 30168 # Constant c_int
UIA_Selection2FirstSelectedItemPropertyId = 30169 # Constant c_int
UIA_Selection2LastSelectedItemPropertyId = 30170 # Constant c_int
UIA_Selection2CurrentSelectedItemPropertyId = 30171 # Constant c_int
UIA_Selection2ItemCountPropertyId = 30172 # Constant c_int
class IUIAutomationExpandCollapsePattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{619BE086-1F4E-4EE4-BAFA-210128738730}')
    _idlflags_ = []

# values for enumeration 'ExpandCollapseState'
ExpandCollapseState_Collapsed = 0
ExpandCollapseState_Expanded = 1
ExpandCollapseState_PartiallyExpanded = 2
ExpandCollapseState_LeafNode = 3
ExpandCollapseState = c_int # enum
IUIAutomationExpandCollapsePattern._methods_ = [
    COMMETHOD([], HRESULT, 'Expand'),
    COMMETHOD([], HRESULT, 'Collapse'),
    COMMETHOD(['propget'], HRESULT, 'CurrentExpandCollapseState',
              ( ['out', 'retval'], POINTER(ExpandCollapseState), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedExpandCollapseState',
              ( ['out', 'retval'], POINTER(ExpandCollapseState), 'retVal' )),
]
################################################################
## code template for IUIAutomationExpandCollapsePattern implementation
##class IUIAutomationExpandCollapsePattern_Impl(object):
##    def Expand(self):
##        '-no docstring-'
##        #return 
##
##    def Collapse(self):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentExpandCollapseState(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedExpandCollapseState(self):
##        '-no docstring-'
##        #return retVal
##

UIA_HeadingLevelPropertyId = 30173 # Constant c_int
UIA_IsDialogPropertyId = 30174 # Constant c_int
UIA_AnimationStyleAttributeId = 40000 # Constant c_int
UIA_BackgroundColorAttributeId = 40001 # Constant c_int
UIA_BulletStyleAttributeId = 40002 # Constant c_int
UIA_CapStyleAttributeId = 40003 # Constant c_int
UIA_CultureAttributeId = 40004 # Constant c_int
UIA_FontNameAttributeId = 40005 # Constant c_int
UIA_FontSizeAttributeId = 40006 # Constant c_int
UIA_FontWeightAttributeId = 40007 # Constant c_int
UIA_ForegroundColorAttributeId = 40008 # Constant c_int
UIA_HorizontalTextAlignmentAttributeId = 40009 # Constant c_int
UIA_IndentationFirstLineAttributeId = 40010 # Constant c_int
UIA_IndentationLeadingAttributeId = 40011 # Constant c_int
UIA_IndentationTrailingAttributeId = 40012 # Constant c_int
UIA_IsHiddenAttributeId = 40013 # Constant c_int
UIA_IsItalicAttributeId = 40014 # Constant c_int
UIA_IsReadOnlyAttributeId = 40015 # Constant c_int
UIA_IsSubscriptAttributeId = 40016 # Constant c_int
UIA_IsSuperscriptAttributeId = 40017 # Constant c_int
UIA_MarginBottomAttributeId = 40018 # Constant c_int
UIA_MarginLeadingAttributeId = 40019 # Constant c_int
UIA_MarginTopAttributeId = 40020 # Constant c_int
UIA_MarginTrailingAttributeId = 40021 # Constant c_int
UIA_OutlineStylesAttributeId = 40022 # Constant c_int
UIA_OverlineColorAttributeId = 40023 # Constant c_int
UIA_OverlineStyleAttributeId = 40024 # Constant c_int
UIA_StrikethroughColorAttributeId = 40025 # Constant c_int
UIA_StrikethroughStyleAttributeId = 40026 # Constant c_int
UIA_TabsAttributeId = 40027 # Constant c_int
class IUIAutomationGridPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{414C3CDC-856B-4F5B-8538-3131C6302550}')
    _idlflags_ = []
IUIAutomationGridPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetItem',
              ( ['in'], c_int, 'row' ),
              ( ['in'], c_int, 'column' ),
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'element' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRowCount',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentColumnCount',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRowCount',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedColumnCount',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationGridPattern implementation
##class IUIAutomationGridPattern_Impl(object):
##    def GetItem(self, row, column):
##        '-no docstring-'
##        #return element
##
##    @property
##    def CurrentRowCount(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentColumnCount(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedRowCount(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedColumnCount(self):
##        '-no docstring-'
##        #return retVal
##

UIA_TextFlowDirectionsAttributeId = 40028 # Constant c_int
UIA_UnderlineColorAttributeId = 40029 # Constant c_int
UIA_UnderlineStyleAttributeId = 40030 # Constant c_int
UIA_AnnotationTypesAttributeId = 40031 # Constant c_int
UIA_AnnotationObjectsAttributeId = 40032 # Constant c_int
UIA_StyleNameAttributeId = 40033 # Constant c_int
UIA_StyleIdAttributeId = 40034 # Constant c_int
UIA_LinkAttributeId = 40035 # Constant c_int
UIA_IsActiveAttributeId = 40036 # Constant c_int
UIA_SelectionActiveEndAttributeId = 40037 # Constant c_int
UIA_CaretPositionAttributeId = 40038 # Constant c_int
UIA_CaretBidiModeAttributeId = 40039 # Constant c_int
UIA_LineSpacingAttributeId = 40040 # Constant c_int
UIA_BeforeParagraphSpacingAttributeId = 40041 # Constant c_int
UIA_AfterParagraphSpacingAttributeId = 40042 # Constant c_int
UIA_SayAsInterpretAsAttributeId = 40043 # Constant c_int
UIA_ButtonControlTypeId = 50000 # Constant c_int
UIA_CalendarControlTypeId = 50001 # Constant c_int
UIA_CheckBoxControlTypeId = 50002 # Constant c_int
UIA_ComboBoxControlTypeId = 50003 # Constant c_int
UIA_EditControlTypeId = 50004 # Constant c_int
UIA_HyperlinkControlTypeId = 50005 # Constant c_int
class IUIAutomationGridItemPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{78F8EF57-66C3-4E09-BD7C-E79B2004894D}')
    _idlflags_ = []
IUIAutomationGridItemPattern._methods_ = [
    COMMETHOD(['propget'], HRESULT, 'CurrentContainingGrid',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRow',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentColumn',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentRowSpan',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentColumnSpan',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedContainingGrid',
              ( ['out', 'retval'], POINTER(POINTER(IUIAutomationElement)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRow',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedColumn',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedRowSpan',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedColumnSpan',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
]
################################################################
## code template for IUIAutomationGridItemPattern implementation
##class IUIAutomationGridItemPattern_Impl(object):
##    @property
##    def CurrentContainingGrid(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentRow(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentColumn(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentRowSpan(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CurrentColumnSpan(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedContainingGrid(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedRow(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedColumn(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedRowSpan(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedColumnSpan(self):
##        '-no docstring-'
##        #return retVal
##

UIA_ImageControlTypeId = 50006 # Constant c_int
UIA_ListItemControlTypeId = 50007 # Constant c_int
UIA_ListControlTypeId = 50008 # Constant c_int
UIA_MenuControlTypeId = 50009 # Constant c_int
UIA_MenuBarControlTypeId = 50010 # Constant c_int
UIA_MenuItemControlTypeId = 50011 # Constant c_int
UIA_ProgressBarControlTypeId = 50012 # Constant c_int
UIA_RadioButtonControlTypeId = 50013 # Constant c_int
UIA_ScrollBarControlTypeId = 50014 # Constant c_int
UIA_SliderControlTypeId = 50015 # Constant c_int
UIA_SpinnerControlTypeId = 50016 # Constant c_int
UIA_StatusBarControlTypeId = 50017 # Constant c_int
UIA_TabControlTypeId = 50018 # Constant c_int
UIA_TabItemControlTypeId = 50019 # Constant c_int
UIA_TextControlTypeId = 50020 # Constant c_int
UIA_ToolBarControlTypeId = 50021 # Constant c_int
UIA_ToolTipControlTypeId = 50022 # Constant c_int
UIA_TreeControlTypeId = 50023 # Constant c_int
UIA_TreeItemControlTypeId = 50024 # Constant c_int
UIA_CustomControlTypeId = 50025 # Constant c_int
UIA_GroupControlTypeId = 50026 # Constant c_int
UIA_ThumbControlTypeId = 50027 # Constant c_int
UIA_DataGridControlTypeId = 50028 # Constant c_int
UIA_DataItemControlTypeId = 50029 # Constant c_int
UIA_DocumentControlTypeId = 50030 # Constant c_int
UIA_SplitButtonControlTypeId = 50031 # Constant c_int
UIA_WindowControlTypeId = 50032 # Constant c_int
UIA_PaneControlTypeId = 50033 # Constant c_int
UIA_HeaderControlTypeId = 50034 # Constant c_int
UIA_HeaderItemControlTypeId = 50035 # Constant c_int
UIA_TableControlTypeId = 50036 # Constant c_int
UIA_TitleBarControlTypeId = 50037 # Constant c_int
UIA_SeparatorControlTypeId = 50038 # Constant c_int
class IUIAutomationMultipleViewPattern(comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{8D253C91-1DC5-4BB5-B18F-ADE16FA495E8}')
    _idlflags_ = []
IUIAutomationMultipleViewPattern._methods_ = [
    COMMETHOD([], HRESULT, 'GetViewName',
              ( ['in'], c_int, 'view' ),
              ( ['out', 'retval'], POINTER(BSTR), 'name' )),
    COMMETHOD([], HRESULT, 'SetCurrentView',
              ( ['in'], c_int, 'view' )),
    COMMETHOD(['propget'], HRESULT, 'CurrentCurrentView',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCurrentSupportedViews',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
    COMMETHOD(['propget'], HRESULT, 'CachedCurrentView',
              ( ['out', 'retval'], POINTER(c_int), 'retVal' )),
    COMMETHOD([], HRESULT, 'GetCachedSupportedViews',
              ( ['out', 'retval'], POINTER(_midlSAFEARRAY(c_int)), 'retVal' )),
]
################################################################
## code template for IUIAutomationMultipleViewPattern implementation
##class IUIAutomationMultipleViewPattern_Impl(object):
##    def GetViewName(self, view):
##        '-no docstring-'
##        #return name
##
##    def SetCurrentView(self, view):
##        '-no docstring-'
##        #return 
##
##    @property
##    def CurrentCurrentView(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCurrentSupportedViews(self):
##        '-no docstring-'
##        #return retVal
##
##    @property
##    def CachedCurrentView(self):
##        '-no docstring-'
##        #return retVal
##
##    def GetCachedSupportedViews(self):
##        '-no docstring-'
##        #return retVal
##

UIA_SemanticZoomControlTypeId = 50039 # Constant c_int
UIA_AppBarControlTypeId = 50040 # Constant c_int
AnnotationType_Unknown = 60000 # Constant c_int
AnnotationType_SpellingError = 60001 # Constant c_int
AnnotationType_GrammarError = 60002 # Constant c_int
AnnotationType_Comment = 60003 # Constant c_int
AnnotationType_FormulaError = 60004 # Constant c_int
AnnotationType_TrackChanges = 60005 # Constant c_int
AnnotationType_Header = 60006 # Constant c_int
AnnotationType_Footer = 60007 # Constant c_int
__all__ = [ 'UIA_LegacyIAccessibleSelectionPropertyId',
           'UIA_StyleNameAttributeId', 'UIA_ProcessIdPropertyId',
           'UIA_InputDiscardedEventId', 'AutomationElementMode_Full',
           'UIA_AcceleratorKeyPropertyId', 'DockPosition_Top',
           'UIA_DataItemControlTypeId', 'ToggleState_On',
           'HeadingLevel6', 'UIA_AutomationPropertyChangedEventId',
           'UIA_ExpandCollapseExpandCollapseStatePropertyId',
           'IUIAutomationSelectionPattern',
           'IUIAutomationNotificationEventHandler',
           'UIA_BoundingRectanglePropertyId',
           'AnnotationType_UnsyncedChange',
           'UIA_LayoutInvalidatedEventId',
           'UIA_DragGrabbedItemsPropertyId',
           'UIA_UnderlineStyleAttributeId',
           'ConnectionRecoveryBehaviorOptions_Enabled',
           'UIA_DropTarget_DragLeaveEventId',
           'IUIAutomationOrCondition',
           'AnnotationType_InsertionChange',
           'UIA_RangeValueIsReadOnlyPropertyId',
           'UIA_HeaderItemControlTypeId',
           'UIA_IsSubscriptAttributeId',
           'UIA_InputReachedOtherElementEventId',
           'IUIAutomationElementArray',
           'UIA_Selection_InvalidatedEventId',
           'UIA_IsPasswordPropertyId', 'UIA_HyperlinkControlTypeId',
           'UIA_ClickablePointPropertyId',
           'UIA_RangeValueSmallChangePropertyId',
           'UIA_IsEnabledPropertyId', 'StyleId_Custom',
           'RowOrColumnMajor_Indeterminate', 'UIA_FillTypePropertyId',
           'UIA_MenuOpenedEventId', 'IUIAutomationWindowPattern',
           'StyleId_Heading6',
           'UIA_IsDropTargetPatternAvailablePropertyId',
           'AutomationElementMode_None', 'UIA_ThumbControlTypeId',
           'UIA_TableRowHeadersPropertyId', 'StyleId_Quote',
           'UIA_AnnotationPatternId',
           'UIA_TableItemRowHeaderItemsPropertyId',
           'SynchronizedInputType_RightMouseDown',
           'UIA_TabControlTypeId', 'UIA_ObjectModelPatternId',
           'UIA_DockDockPositionPropertyId',
           'UIA_SpreadsheetItemAnnotationObjectsPropertyId',
           'UIA_VirtualizedItemPatternId',
           'UIA_InputReachedTargetEventId',
           'UIA_IsTransformPatternAvailablePropertyId',
           'AnnotationType_ConflictingChange',
           'IUIAutomationChangesEventHandler',
           'UIA_ButtonControlTypeId', 'UIA_ValueIsReadOnlyPropertyId',
           'UIA_DockPatternId', 'UIA_GridItemColumnPropertyId',
           'UIA_HasKeyboardFocusPropertyId', 'UIA_LevelPropertyId',
           'TextEditChangeType_AutoCorrect',
           'UIA_PositionInSetPropertyId', 'UIA_CheckBoxControlTypeId',
           'UIA_StylesStyleIdPropertyId', 'StyleId_Subtitle',
           'UIA_TextControlTypeId',
           'UIA_TransformCanRotatePropertyId', 'DockPosition_Right',
           'AnnotationType_Author', 'UIA_MarginBottomAttributeId',
           'UIA_TitleBarControlTypeId',
           'ProviderOptions_HasNativeIAccessible',
           'IUIAutomationProxyFactoryEntry',
           'TextPatternRangeEndpoint_Start', 'ZoomUnit_NoAmount',
           'UIA_TextEdit_ConversionTargetChangedEventId',
           'IUIAutomationTextRangeArray',
           'UIA_IsTablePatternAvailablePropertyId',
           'UIA_ScrollHorizontalScrollPercentPropertyId',
           'UIA_MultipleViewCurrentViewPropertyId',
           'UIA_MenuBarControlTypeId',
           'IUIAutomationEventHandlerGroup',
           'UIA_SpinnerControlTypeId', 'IUIAutomation',
           'DockPosition_Left', 'UIA_AnimationStyleAttributeId',
           'UIA_TableItemPatternId',
           'UIA_IsTextPattern2AvailablePropertyId',
           'TextUnit_Document', 'UIA_DropTarget_DragEnterEventId',
           'StyleId_Heading9', 'IUIAutomation4', 'TreeScope_Element',
           'IUIAutomationPropertyCondition',
           'UIA_GridItemRowPropertyId', 'UIA_ListControlTypeId',
           'UIA_NativeWindowHandlePropertyId', 'UIA_ValuePatternId',
           'ProviderOptions_OverrideProvider',
           'WindowVisualState_Normal',
           'UIA_DropTargetDropTargetEffectPropertyId',
           'UIA_GridPatternId',
           'UIA_IsDockPatternAvailablePropertyId',
           'ScrollAmount_NoAmount', 'UIA_LiveSettingPropertyId',
           'UIA_IsExpandCollapsePatternAvailablePropertyId',
           'UIA_MultipleViewSupportedViewsPropertyId',
           'UIA_IsRangeValuePatternAvailablePropertyId',
           'UIA_CulturePropertyId', 'IUIAutomationTextPattern2',
           'UIA_IsGridItemPatternAvailablePropertyId',
           'UIA_SelectionItemPatternId',
           'IUIAutomationSpreadsheetItemPattern',
           'UIA_DropTargetPatternId',
           'UIA_AnnotationAnnotationTypeIdPropertyId',
           'UIA_SelectionSelectionPropertyId',
           'UIA_SelectionPatternId', 'UIA_AnnotationTargetPropertyId',
           'UIA_MenuClosedEventId', 'SynchronizedInputType',
           'ProviderOptions_ProviderOwnsSetFocus',
           'UIA_Window_WindowClosedEventId', 'IUIAutomation2',
           'UIA_ChangesEventId', 'UIA_SearchLandmarkTypeId',
           'UIA_CapStyleAttributeId',
           'UIA_StylesFillPatternStylePropertyId',
           'TextPatternRangeEndpoint_End',
           'IUIAutomationFocusChangedEventHandler',
           'SynchronizedInputType_LeftMouseDown',
           'UIA_FontSizeAttributeId',
           'UIA_IsSpreadsheetItemPatternAvailablePropertyId',
           'UIA_ScrollVerticalScrollPercentPropertyId',
           'StructureChangeType_ChildrenReordered',
           'UIA_RotationPropertyId', 'UIA_SizeOfSetPropertyId',
           'AnnotationType_ExternalChange', 'TextUnit_Line',
           'SupportedTextSelection_Multiple',
           'UIA_MarginTopAttributeId', 'UIA_VisualEffectsPropertyId',
           'UIA_ToolTipOpenedEventId',
           'IUIAutomationObjectModelPattern',
           'UIA_TableItemColumnHeaderItemsPropertyId',
           'UIA_Transform2ZoomMinimumPropertyId',
           'UIA_Transform2ZoomMaximumPropertyId',
           'UIA_CalendarControlTypeId', 'IUIAutomationDragPattern',
           'UIA_WindowPatternId', 'UIA_TransformCanResizePropertyId',
           'UIA_IsScrollItemPatternAvailablePropertyId',
           'NotificationProcessing_MostRecent',
           'PropertyConditionFlags_None', 'UIA_MenuModeEndEventId',
           'UIA_ActiveTextPositionChangedEventId',
           'UIA_LocalizedControlTypePropertyId', 'Off',
           'UIA_WindowWindowInteractionStatePropertyId',
           'IUIAutomationActiveTextPositionChangedEventHandler',
           'IUIAutomationTreeWalker',
           'UIA_IsAnnotationPatternAvailablePropertyId',
           'UIA_FormLandmarkTypeId', 'StyleId_Heading5',
           'UIA_CustomNavigationPatternId', 'OrientationType',
           'UIA_TextPattern2Id', 'CoalesceEventsOptions_Enabled',
           'UIA_ProviderDescriptionPropertyId',
           'UIA_AnnotationAnnotationTypeNamePropertyId',
           'StructureChangeType_ChildrenBulkAdded',
           'AnnotationType_DataValidationError',
           'IUIAutomationDropTargetPattern',
           'UIA_ExpandCollapsePatternId', 'UIA_SystemAlertEventId',
           'IUIAutomationGridPattern', 'RowOrColumnMajor_RowMajor',
           'IUIAutomation5', 'IUIAutomationVirtualizedItemPattern',
           'UIA_MarginTrailingAttributeId',
           'AnnotationType_MoveChange',
           'UIA_WindowCanMaximizePropertyId',
           'AnnotationType_Sensitive', 'AnnotationType_SpellingError',
           'UIA_OptimizeForVisualContentPropertyId',
           'NavigateDirection_FirstChild',
           'AnnotationType_GrammarError', 'StyleId_Heading2',
           'UIA_RangeValueMinimumPropertyId',
           'IUIAutomationSelectionItemPattern',
           'IUIAutomationTextEditPattern',
           'UIA_LegacyIAccessibleHelpPropertyId',
           'IUIAutomationAnnotationPattern',
           'UIA_SelectionPattern2Id',
           'IUIAutomationTransformPattern2',
           'UIA_IsDataValidForFormPropertyId',
           'UIA_SpreadsheetPatternId', 'UIA_StylesShapePropertyId',
           'TreeScope', 'IUIAutomationTablePattern',
           'UIA_WindowCanMinimizePropertyId',
           'UIA_FullDescriptionPropertyId', 'UIA_PaneControlTypeId',
           'UIA_IsSelectionItemPatternAvailablePropertyId',
           'SynchronizedInputType_LeftMouseUp',
           'UIA_TableRowOrColumnMajorPropertyId',
           'UIA_MenuModeStartEventId',
           'UIA_IsSynchronizedInputPatternAvailablePropertyId',
           'UIA_RadioButtonControlTypeId',
           'UIA_SplitButtonControlTypeId',
           'ProviderOptions_NonClientAreaProvider',
           'UIA_WindowControlTypeId',
           'UIA_GridItemContainingGridPropertyId',
           'UIA_LineSpacingAttributeId', 'AnnotationType_Footer',
           'UIA_AnnotationObjectsAttributeId',
           'UIA_Invoke_InvokedEventId', 'TextUnit_Character',
           'UIA_HostedFragmentRootsInvalidatedEventId',
           'UIA_LegacyIAccessibleValuePropertyId',
           'UIA_LiveRegionChangedEventId', 'UIA_TogglePatternId',
           'WindowInteractionState_NotResponding',
           'IUIAutomationSynchronizedInputPattern', 'HeadingLevel3',
           'IUIAutomationBoolCondition', 'CoalesceEventsOptions',
           'UIA_TabsAttributeId', 'UIA_IndentationLeadingAttributeId',
           'OrientationType_Horizontal',
           'UIA_IsObjectModelPatternAvailablePropertyId',
           'UIA_SelectionCanSelectMultiplePropertyId',
           'UIA_DescribedByPropertyId',
           'UIA_RangeValueLargeChangePropertyId',
           'UIA_FontNameAttributeId', 'UIA_AnnotationTypesPropertyId',
           'IUIAutomationElement',
           'UIA_LegacyIAccessibleKeyboardShortcutPropertyId',
           'UIA_TableColumnHeadersPropertyId',
           'UIA_HorizontalTextAlignmentAttributeId',
           'UIA_AppBarControlTypeId', 'RowOrColumnMajor',
           'UIA_CustomLandmarkTypeId',
           'UIA_IsGridPatternAvailablePropertyId',
           'WindowInteractionState_ReadyForUserInteraction',
           'TextUnit_Word', 'UIA_MainLandmarkTypeId',
           'UIA_SliderControlTypeId', 'UIA_IsOffscreenPropertyId',
           'UIA_ClassNamePropertyId', 'UIA_AriaPropertiesPropertyId',
           'UIA_IsActiveAttributeId', 'UIA_LandmarkTypePropertyId',
           'UIA_Window_WindowOpenedEventId', 'TextUnit',
           'UIA_OverlineColorAttributeId',
           'UIA_Transform2CanZoomPropertyId',
           'UIA_OutlineThicknessPropertyId',
           'UIA_IsSpreadsheetPatternAvailablePropertyId',
           'PropertyConditionFlags', 'Polite',
           'UIA_StylesFillPatternColorPropertyId',
           'IUIAutomationCustomNavigationPattern',
           'UIA_AutomationFocusChangedEventId',
           'UIA_SemanticZoomControlTypeId',
           'NavigateDirection_LastChild',
           'UIA_SelectionItemIsSelectedPropertyId',
           'StyleId_Heading1', 'IUIAutomationInvokePattern',
           'ToggleState_Off', 'UIA_IsRequiredForFormPropertyId',
           'UIA_TableControlTypeId', 'IUIAutomationCondition',
           'UIA_LegacyIAccessibleDefaultActionPropertyId',
           'PropertyConditionFlags_IgnoreCase',
           'RowOrColumnMajor_ColumnMajor',
           'TreeTraversalOptions_LastToFirstOrder',
           'StyleId_Heading7', 'UIA_TreeItemControlTypeId',
           'UIA_DragDropEffectsPropertyId',
           'UIA_SeparatorControlTypeId',
           'UIA_IndentationTrailingAttributeId', 'TextEditChangeType',
           'NotificationKind_ActionAborted',
           'UIA_ProgressBarControlTypeId',
           'NavigateDirection_NextSibling', 'UIA_IsItalicAttributeId',
           'StyleId_Heading8', 'UIA_IsDialogPropertyId',
           'WindowVisualState', 'UIA_ToolTipClosedEventId',
           'UIA_NamePropertyId', 'AnnotationType_Footnote',
           'UIA_DragPatternId', 'UIA_SayAsInterpretAsMetadataId',
           'UIA_ScrollItemPatternId',
           'UIA_IsInvokePatternAvailablePropertyId', 'LiveSetting',
           'CUIAutomation8', 'UIA_ItemContainerPatternId',
           'UIA_LocalizedLandmarkTypePropertyId',
           'UIA_AfterParagraphSpacingAttributeId', 'IUIAutomation3',
           'UIA_LegacyIAccessibleStatePropertyId',
           'NavigateDirection_Parent',
           'ExpandCollapseState_Collapsed',
           'UIA_IsTransformPattern2AvailablePropertyId',
           'UIA_StrikethroughColorAttributeId',
           'UIA_LegacyIAccessibleChildIdPropertyId',
           'UIA_ImageControlTypeId', 'ToggleState_Indeterminate',
           'TreeScope_Children', 'AnnotationType_Unknown',
           'UIA_IsSelectionPattern2AvailablePropertyId',
           'UIA_FlowsToPropertyId', 'ExtendedProperty',
           'DockPosition_Bottom',
           'NotificationProcessing_CurrentThenMostRecent',
           'UIA_ControllerForPropertyId', 'UIA_ValueValuePropertyId',
           'UIA_Selection2FirstSelectedItemPropertyId',
           'UIA_StylesExtendedPropertiesPropertyId', 'TextUnit_Page',
           'IUIAutomationTextRange2', 'UIA_SpreadsheetItemPatternId',
           'StyleId_NumberedList', 'HeadingLevel4',
           'PropertyConditionFlags_MatchSubstring', 'DockPosition',
           'UIA_AccessKeyPropertyId', 'StyleId_Heading4',
           'CUIAutomation', 'AnnotationType_Mathematics',
           'UIA_StylesPatternId',
           'WindowInteractionState_BlockedByModalWindow',
           'NavigateDirection_PreviousSibling',
           'StructureChangeType_ChildAdded',
           'SynchronizedInputType_KeyDown', 'UIA_SizePropertyId',
           'IUIAutomationElement2', 'UIA_RangeValueMaximumPropertyId',
           'UIA_SelectionIsSelectionRequiredPropertyId',
           'IUIAutomationMultipleViewPattern', 'StyleId_Heading3',
           'TreeTraversalOptions_PostOrder',
           'UIA_TransformPattern2Id',
           'UIA_IndentationFirstLineAttributeId',
           'UIA_ScrollPatternId', 'UIA_SynchronizedInputPatternId',
           'UIA_SpreadsheetItemFormulaPropertyId',
           'UIA_IsValuePatternAvailablePropertyId',
           'AutomationElementMode', 'UIA_ToolTipControlTypeId',
           'UIA_IsControlElementPropertyId',
           'UIA_GridItemColumnSpanPropertyId',
           'UIA_BulletStyleAttributeId', 'IUIAutomationAndCondition',
           'AnnotationType_Header', 'TextUnit_Format',
           'ProviderOptions_ClientSideProvider',
           'UIA_ScrollHorizontallyScrollablePropertyId',
           'IUIAutomationElement7', 'TextEditChangeType_AutoComplete',
           'UIA_Drag_DragCancelEventId',
           'UIA_GridItemRowSpanPropertyId',
           'OrientationType_Vertical',
           'UIA_AnnotationObjectsPropertyId',
           'UIA_AnnotationDateTimePropertyId',
           'StructureChangeType_ChildrenBulkRemoved',
           'UIA_IsScrollPatternAvailablePropertyId',
           'UIA_GroupControlTypeId', 'UIA_TextChildPatternId',
           'UIA_IsTogglePatternAvailablePropertyId',
           'UIA_BeforeParagraphSpacingAttributeId',
           'IUIAutomationSelectionPattern2',
           'UIA_TransformCanMovePropertyId',
           'IUIAutomationTableItemPattern', 'UIA_CultureAttributeId',
           'ProviderOptions_RefuseNonClientSupport',
           'UIA_SelectionActiveEndAttributeId',
           'TextEditChangeType_CompositionFinalized',
           'ZoomUnit_SmallDecrement', 'UIA_RangeValuePatternId',
           'UIA_IsSuperscriptAttributeId', 'UIA_HelpTextPropertyId',
           'UIA_EditControlTypeId', 'UIA_CaretPositionAttributeId',
           'UIA_StyleIdAttributeId',
           'UIA_IsDragPatternAvailablePropertyId',
           'ZoomUnit_SmallIncrement',
           'NotificationProcessing_ImportantMostRecent', 'ZoomUnit',
           'TreeScope_None', 'UIA_IsKeyboardFocusablePropertyId',
           'ExpandCollapseState', 'IUIAutomationElement6',
           'UIA_BackgroundColorAttributeId', 'IUIAutomationElement5',
           'UIA_MenuControlTypeId', 'TreeTraversalOptions_Default',
           'TreeScope_Ancestors', 'IUIAutomationElement9',
           'StyleId_Emphasis', 'UIA_IsContentElementPropertyId',
           'UIA_TablePatternId', 'UIA_TabItemControlTypeId',
           'HeadingLevel9', 'AnnotationType_AdvancedProofingIssue',
           'AnnotationType_Comment', 'IUIAutomationCacheRequest',
           'SupportedTextSelection_None',
           'IUIAutomationGridItemPattern',
           'IUIAutomationEventHandler',
           'ProviderOptions_ServerSideProvider',
           'UIA_WindowIsModalPropertyId',
           'NotificationKind_ActionCompleted',
           'IUIAutomationLegacyIAccessiblePattern',
           'UIA_IsTextEditPatternAvailablePropertyId',
           'UIA_IsTableItemPatternAvailablePropertyId',
           'AnnotationType_CircularReferenceError',
           'UIA_AsyncContentLoadedEventId', 'UIA_TreeControlTypeId',
           'UIA_LinkAttributeId', 'IUIAutomationElement8',
           'UIA_StylesStyleNamePropertyId', 'IUIAutomationElement3',
           'UIA_LegacyIAccessibleRolePropertyId',
           'NotificationKind_ItemRemoved', 'TreeScope_Subtree',
           'ZoomUnit_LargeIncrement', 'NotificationKind',
           'UIA_NavigationLandmarkTypeId',
           'UIA_TextEdit_TextChangedEventId',
           'UIA_CaretBidiModeAttributeId',
           'IUIAutomationProxyFactory', 'UIA_GridItemPatternId',
           'NotificationProcessing_All',
           'IUIAutomationPropertyChangedEventHandler',
           'UIA_ToolBarControlTypeId',
           'UIA_WindowWindowVisualStatePropertyId', 'StyleId_Normal',
           'IUIAutomationTextPattern', 'UIA_RuntimeIdPropertyId',
           'TextPatternRangeEndpoint', 'UIA_FontWeightAttributeId',
           'UIA_LabeledByPropertyId',
           'UIA_AnnotationAuthorPropertyId',
           'UIA_DragDropEffectPropertyId',
           'ProviderOptions_UseClientCoordinates',
           'IUIAutomationScrollPattern',
           'UIA_StrikethroughStyleAttributeId',
           'UIA_IsMultipleViewPatternAvailablePropertyId',
           'UIA_StructureChangedEventId', 'TextEditChangeType_None',
           'HeadingLevel2', 'TextUnit_Paragraph',
           'UIA_ScrollVerticalViewSizePropertyId',
           'AnnotationType_Endnote', 'HeadingLevel7',
           'UIA_LegacyIAccessiblePatternId',
           'UIA_FillColorPropertyId', 'AnnotationType_FormulaError',
           'UIA_SayAsInterpretAsAttributeId',
           'ExpandCollapseState_PartiallyExpanded', 'StyleId_Title',
           'IUIAutomationElement4', 'IUIAutomationNotCondition',
           'IUIAutomationTransformPattern', 'NotificationKind_Other',
           'UIA_FrameworkIdPropertyId',
           'UIA_DropTarget_DroppedEventId',
           'SynchronizedInputType_KeyUp',
           'UIA_StylesFillColorPropertyId',
           'IUIAutomationTextEditTextChangedEventHandler',
           'UIA_ComboBoxControlTypeId', 'AnnotationType_Highlighted',
           'IRawElementProviderSimple',
           'UIA_MarginLeadingAttributeId', 'HeadingLevel1',
           'UIA_ToggleToggleStatePropertyId',
           'UIA_AutomationIdPropertyId',
           'UIA_IsCustomNavigationPatternAvailablePropertyId',
           'NotificationProcessing_ImportantAll', 'UIA_TextPatternId',
           'TreeScope_Parent', 'UIA_NotificationEventId', 'Assertive',
           'WindowInteractionState_Closing',
           'ScrollAmount_SmallDecrement', 'UIA_ControlTypePropertyId',
           'UIA_SelectionItem_ElementAddedToSelectionEventId',
           'UIA_WindowIsTopmostPropertyId',
           'UIA_IsPeripheralPropertyId',
           'UIA_Text_TextChangedEventId',
           'ScrollAmount_LargeIncrement',
           'UIA_AnnotationTypesAttributeId',
           'TextEditChangeType_Composition',
           'IUIAutomationRangeValuePattern', 'IUIAutomation6',
           'UIA_ForegroundColorAttributeId',
           'UIA_ScrollHorizontalViewSizePropertyId',
           'UIA_DragIsGrabbedPropertyId',
           'IUIAutomationStylesPattern',
           'ProviderOptions_UseComThreading', 'TreeTraversalOptions',
           'UIA_IsVirtualizedItemPatternAvailablePropertyId',
           'AnnotationType_FormatChange', 'WindowInteractionState',
           'UIA_IsSelectionPatternAvailablePropertyId',
           'UIA_MenuItemControlTypeId', 'UIA_StatusBarControlTypeId',
           'DockPosition_Fill', 'TreeScope_Descendants',
           'ConnectionRecoveryBehaviorOptions', 'HeadingLevel5',
           'IUIAutomationTextRange', 'ToggleState',
           'StructureChangeType',
           'UIA_Selection2CurrentSelectedItemPropertyId',
           'UIA_OutlineStylesAttributeId',
           'UIA_DropTargetDropTargetEffectsPropertyId',
           'UIA_LegacyIAccessibleNamePropertyId', 'NavigateDirection',
           'SupportedTextSelection', 'UIA_DocumentControlTypeId',
           'IUIAutomationProxyFactoryMapping',
           'AnnotationType_DeletionChange',
           'SupportedTextSelection_Single',
           'ConnectionRecoveryBehaviorOptions_Disabled',
           'ScrollAmount', 'UIA_TextEditPatternId',
           'IUIAutomationScrollItemPattern',
           'UIA_GridRowCountPropertyId', 'UIA_CenterPointPropertyId',
           'UIA_TextFlowDirectionsAttributeId',
           'NotificationProcessing',
           'AnnotationType_EditingLockedChange',
           'UIA_IsStylesPatternAvailablePropertyId',
           'ScrollAmount_LargeDecrement',
           'WindowVisualState_Maximized', 'UIA_Drag_DragStartEventId',
           'UIA_FlowsFromPropertyId', 'UIA_HeadingLevelPropertyId',
           'UIA_IsTextChildPatternAvailablePropertyId',
           'IUIAutomationExpandCollapsePattern',
           'UIA_Transform2ZoomLevelPropertyId',
           'UIA_SelectionItemSelectionContainerPropertyId',
           'UIA_MultipleViewPatternId', 'UIA_AriaRolePropertyId',
           'SynchronizedInputType_RightMouseUp',
           'UIA_RangeValueValuePropertyId',
           'UIA_Text_TextSelectionChangedEventId',
           'UIA_DataGridControlTypeId',
           'UIA_IsTextPatternAvailablePropertyId',
           'UIA_IsReadOnlyAttributeId', 'IAccessible',
           'UIA_Selection2ItemCountPropertyId',
           'UIA_SelectionItem_ElementSelectedEventId',
           'HeadingLevel8',
           'UIA_SpreadsheetItemAnnotationTypesPropertyId',
           'UIA_TransformPatternId',
           'UIA_Selection2LastSelectedItemPropertyId',
           'UIA_InvokePatternId', 'UIA_OverlineStyleAttributeId',
           'UIA_Drag_DragCompleteEventId',
           'IUIAutomationItemContainerPattern',
           'UIA_IsWindowPatternAvailablePropertyId',
           'IUIAutomationTextRange3', 'ExpandCollapseState_LeafNode',
           'StructureChangeType_ChildrenInvalidated',
           'UIA_IsLegacyIAccessiblePatternAvailablePropertyId',
           'WindowInteractionState_Running', 'HeadingLevel_None',
           'UIA_ScrollVerticallyScrollablePropertyId',
           'UIA_ItemStatusPropertyId', 'WindowVisualState_Minimized',
           'UIA_GridColumnCountPropertyId',
           'StructureChangeType_ChildRemoved',
           'UIA_OrientationPropertyId',
           'ExpandCollapseState_Expanded', 'UIA_IsHiddenAttributeId',
           'UIA_ListItemControlTypeId',
           'IUIAutomationTextChildPattern', 'OrientationType_None',
           'IUIAutomationSpreadsheetPattern',
           'UIA_CustomControlTypeId', 'ProviderOptions',
           'UIA_SummaryChangeId', 'UIA_HeaderControlTypeId',
           'CoalesceEventsOptions_Disabled',
           'UIA_IsItemContainerPatternAvailablePropertyId',
           'AnnotationType_TrackChanges', 'UiaChangeInfo',
           'UIA_ItemTypePropertyId', 'ZoomUnit_LargeDecrement',
           'NotificationKind_ItemAdded', 'IUIAutomationTogglePattern',
           'IUIAutomationValuePattern', 'IUIAutomationDockPattern',
           'IUIAutomationStructureChangedEventHandler',
           'UIA_OutlineColorPropertyId',
           'UIA_LegacyIAccessibleDescriptionPropertyId',
           'UIA_UnderlineColorAttributeId',
           'UIA_SelectionItem_ElementRemovedFromSelectionEventId',
           'ScrollAmount_SmallIncrement', 'DockPosition_None',
           'UIA_ScrollBarControlTypeId', 'StyleId_BulletedList']
from comtypes import _check_version; _check_version('')
