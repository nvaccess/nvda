# typelib C:\WINDOWS\system32\RICHED20.DLL
_lcid = 0 # change this if required
from ctypes import *
import comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from ctypes import HRESULT
from comtypes import BSTR
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from comtypes import IUnknown
from comtypes import wireHWND
from comtypes.automation import VARIANT
from comtypes.automation import VARIANT


class ITextFont(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{8CC497C3-A1DF-11CE-8098-00AA0047BE5D}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']
ITextFont._methods_ = [
    COMMETHOD([dispid(0), 'propget'], HRESULT, 'Duplicate',
              ( ['retval', 'out'], POINTER(POINTER(ITextFont)), 'ppFont' )),
    COMMETHOD([dispid(0), 'propput'], HRESULT, 'Duplicate',
              ( ['in'], POINTER(ITextFont), 'ppFont' )),
    COMMETHOD([dispid(769)], HRESULT, 'CanChange',
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(770)], HRESULT, 'IsEqual',
              ( ['in'], POINTER(ITextFont), 'pFont' ),
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(771)], HRESULT, 'Reset',
              ( ['in'], c_int, 'Value' )),
    COMMETHOD([dispid(772), 'propget'], HRESULT, 'Style',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(772), 'propput'], HRESULT, 'Style',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(773), 'propget'], HRESULT, 'AllCaps',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(773), 'propput'], HRESULT, 'AllCaps',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(774), 'propget'], HRESULT, 'Animation',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(774), 'propput'], HRESULT, 'Animation',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(775), 'propget'], HRESULT, 'BackColor',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(775), 'propput'], HRESULT, 'BackColor',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(776), 'propget'], HRESULT, 'Bold',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(776), 'propput'], HRESULT, 'Bold',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(777), 'propget'], HRESULT, 'Emboss',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(777), 'propput'], HRESULT, 'Emboss',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(784), 'propget'], HRESULT, 'ForeColor',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(784), 'propput'], HRESULT, 'ForeColor',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(785), 'propget'], HRESULT, 'Hidden',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(785), 'propput'], HRESULT, 'Hidden',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(786), 'propget'], HRESULT, 'Engrave',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(786), 'propput'], HRESULT, 'Engrave',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(787), 'propget'], HRESULT, 'Italic',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(787), 'propput'], HRESULT, 'Italic',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(788), 'propget'], HRESULT, 'Kerning',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(788), 'propput'], HRESULT, 'Kerning',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(789), 'propget'], HRESULT, 'LanguageID',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(789), 'propput'], HRESULT, 'LanguageID',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(790), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstr' )),
    COMMETHOD([dispid(790), 'propput'], HRESULT, 'Name',
              ( ['in'], BSTR, 'pbstr' )),
    COMMETHOD([dispid(791), 'propget'], HRESULT, 'Outline',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(791), 'propput'], HRESULT, 'Outline',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(792), 'propget'], HRESULT, 'Position',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(792), 'propput'], HRESULT, 'Position',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(793), 'propget'], HRESULT, 'Protected',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(793), 'propput'], HRESULT, 'Protected',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(800), 'propget'], HRESULT, 'Shadow',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(800), 'propput'], HRESULT, 'Shadow',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(801), 'propget'], HRESULT, 'Size',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(801), 'propput'], HRESULT, 'Size',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(802), 'propget'], HRESULT, 'SmallCaps',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(802), 'propput'], HRESULT, 'SmallCaps',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(803), 'propget'], HRESULT, 'Spacing',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(803), 'propput'], HRESULT, 'Spacing',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(804), 'propget'], HRESULT, 'StrikeThrough',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(804), 'propput'], HRESULT, 'StrikeThrough',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(805), 'propget'], HRESULT, 'Subscript',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(805), 'propput'], HRESULT, 'Subscript',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(806), 'propget'], HRESULT, 'Superscript',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(806), 'propput'], HRESULT, 'Superscript',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(807), 'propget'], HRESULT, 'Underline',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(807), 'propput'], HRESULT, 'Underline',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(808), 'propget'], HRESULT, 'Weight',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(808), 'propput'], HRESULT, 'Weight',
              ( ['in'], c_int, 'pValue' )),
]
class ITextStoryRanges(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{8CC497C5-A1DF-11CE-8098-00AA0047BE5D}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']
class ITextRange(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{8CC497C2-A1DF-11CE-8098-00AA0047BE5D}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']
ITextStoryRanges._methods_ = [
    COMMETHOD([dispid(-4), 'restricted'], HRESULT, '_NewEnum',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'ppunkEnum' )),
    COMMETHOD([dispid(0)], HRESULT, 'Item',
              ( ['in'], c_int, 'Index' ),
              ( ['retval', 'out'], POINTER(POINTER(ITextRange)), 'ppRange' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'Count',
              ( ['retval', 'out'], POINTER(c_int), 'pCount' )),
]

# values for enumeration '__MIDL___MIDL_itf_tom_0000_0001'
tomFalse = 0
tomTrue = -1
tomUndefined = -9999999
tomToggle = -9999998
tomAutoColor = -9999997
tomDefault = -9999996
tomSuspend = -9999995
tomResume = -9999994
tomApplyNow = 0
tomApplyLater = 1
tomTrackParms = 2
tomCacheParms = 3
tomApplyTmp = 4
tomBackward = -1073741823
tomForward = 1073741823
tomMove = 0
tomExtend = 1
tomNoSelection = 0
tomSelectionIP = 1
tomSelectionNormal = 2
tomSelectionFrame = 3
tomSelectionColumn = 4
tomSelectionRow = 5
tomSelectionBlock = 6
tomSelectionInlineShape = 7
tomSelectionShape = 8
tomSelStartActive = 1
tomSelAtEOL = 2
tomSelOvertype = 4
tomSelActive = 8
tomSelReplace = 16
tomEnd = 0
tomStart = 32
tomCollapseEnd = 0
tomCollapseStart = 1
tomClientCoord = 256
tomAllowOffClient = 512
tomNone = 0
tomSingle = 1
tomWords = 2
tomDouble = 3
tomDotted = 4
tomDash = 5
tomDashDot = 6
tomDashDotDot = 7
tomWave = 8
tomThick = 9
tomHair = 10
tomDoubleWave = 11
tomHeavyWave = 12
tomLongDash = 13
tomThickDash = 14
tomThickDashDot = 15
tomThickDashDotDot = 16
tomThickDotted = 17
tomThickLongDash = 18
tomLineSpaceSingle = 0
tomLineSpace1pt5 = 1
tomLineSpaceDouble = 2
tomLineSpaceAtLeast = 3
tomLineSpaceExactly = 4
tomLineSpaceMultiple = 5
tomAlignLeft = 0
tomAlignCenter = 1
tomAlignRight = 2
tomAlignJustify = 3
tomAlignDecimal = 3
tomAlignBar = 4
tomAlignInterWord = 3
tomAlignInterLetter = 4
tomAlignScaled = 5
tomAlignGlyphs = 6
tomAlignSnapGrid = 7
tomSpaces = 0
tomDots = 1
tomDashes = 2
tomLines = 3
tomThickLines = 4
tomEquals = 5
tomTabBack = -3
tomTabNext = -2
tomTabHere = -1
tomListNone = 0
tomListBullet = 1
tomListNumberAsArabic = 2
tomListNumberAsLCLetter = 3
tomListNumberAsUCLetter = 4
tomListNumberAsLCRoman = 5
tomListNumberAsUCRoman = 6
tomListNumberAsSequence = 7
tomListParentheses = 65536
tomListPeriod = 131072
tomListPlain = 196608
tomCharacter = 1
tomWord = 2
tomSentence = 3
tomParagraph = 4
tomLine = 5
tomStory = 6
tomScreen = 7
tomSection = 8
tomColumn = 9
tomRow = 10
tomWindow = 11
tomCell = 12
tomCharFormat = 13
tomParaFormat = 14
tomTable = 15
tomObject = 16
tomPage = 17
tomMatchWord = 2
tomMatchCase = 4
tomMatchPattern = 8
tomUnknownStory = 0
tomMainTextStory = 1
tomFootnotesStory = 2
tomEndnotesStory = 3
tomCommentsStory = 4
tomTextFrameStory = 5
tomEvenPagesHeaderStory = 6
tomPrimaryHeaderStory = 7
tomEvenPagesFooterStory = 8
tomPrimaryFooterStory = 9
tomFirstPageHeaderStory = 10
tomFirstPageFooterStory = 11
tomNoAnimation = 0
tomLasVegasLights = 1
tomBlinkingBackground = 2
tomSparkleText = 3
tomMarchingBlackAnts = 4
tomMarchingRedAnts = 5
tomShimmer = 6
tomWipeDown = 7
tomWipeRight = 8
tomAnimationMax = 8
tomLowerCase = 0
tomUpperCase = 1
tomTitleCase = 2
tomSentenceCase = 4
tomToggleCase = 5
tomReadOnly = 256
tomShareDenyRead = 512
tomShareDenyWrite = 1024
tomPasteFile = 4096
tomCreateNew = 16
tomCreateAlways = 32
tomOpenExisting = 48
tomOpenAlways = 64
tomTruncateExisting = 80
tomRTF = 1
tomText = 2
tomHTML = 3
tomWordDocument = 4
tomBold = -2147483647
tomItalic = -2147483646
tomUnderline = -2147483644
tomStrikeout = -2147483640
tomProtected = -2147483632
tomLink = -2147483616
tomSmallCaps = -2147483584
tomAllCaps = -2147483520
tomHidden = -2147483392
tomOutline = -2147483136
tomShadow = -2147482624
tomEmboss = -2147481600
tomImprint = -2147479552
tomDisabled = -2147475456
tomRevised = -2147467264
tomNormalCaret = 0
tomKoreanBlockCaret = 1
tomIncludeInset = 1
tomIgnoreCurrentFont = 0
tomMatchFontCharset = 1
tomMatchFontSignature = 2
tomCharset = -2147483648
tomRE10Mode = 1
tomUseAtFont = 2
tomTextFlowMask = 12
tomTextFlowES = 0
tomTextFlowSW = 4
tomTextFlowWN = 8
tomTextFlowNE = 12
tomUsePassword = 16
tomNoIME = 524288
tomSelfIME = 262144
__MIDL___MIDL_itf_tom_0000_0001 = c_int # enum
tomConstants = __MIDL___MIDL_itf_tom_0000_0001
class ITextMsgFilter(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{A3787420-4267-11D1-883A-3C8B00C10000}')
    _idlflags_ = ['nonextensible']
class ITextDocument(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{8CC497C0-A1DF-11CE-8098-00AA0047BE5D}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']
class ITextDocument2(ITextDocument):
    _case_insensitive_ = True
    _iid_ = GUID('{01C25500-4268-11D1-883A-3C8B00C10000}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']
ITextMsgFilter._methods_ = [
    COMMETHOD([helpstring(u'method AttachDocument')], HRESULT, 'AttachDocument',
              ( ['in'], wireHWND, 'hwnd' ),
              ( ['in'], POINTER(ITextDocument2), 'pTextDoc' ),
              ( ['in'], POINTER(IUnknown), 'punk' )),
    COMMETHOD([helpstring(u'method HandleMessage')], HRESULT, 'HandleMessage',
              ( ['in', 'out'], POINTER(c_uint), 'pmsg' ),
              ( ['in', 'out'], POINTER(c_uint), 'pwparam' ),
              ( ['in', 'out'], POINTER(c_int), 'plparam' ),
              ( ['out'], POINTER(c_int), 'plres' )),
    COMMETHOD([helpstring(u'method AttachMsgFilter')], HRESULT, 'AttachMsgFilter',
              ( ['in'], POINTER(ITextMsgFilter), 'pMsgFilter' )),
]
class ITextPara(comInterfaces._00020430_0000_0000_C000_000000000046_0_2_0.IDispatch):
    _case_insensitive_ = True
    _iid_ = GUID('{8CC497C4-A1DF-11CE-8098-00AA0047BE5D}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']
ITextRange._methods_ = [
    COMMETHOD([dispid(0), 'propget'], HRESULT, 'Text',
              ( ['retval', 'out'], POINTER(BSTR), 'pbstr' )),
    COMMETHOD([dispid(0), 'propput'], HRESULT, 'Text',
              ( ['in'], BSTR, 'pbstr' )),
    COMMETHOD([dispid(513), 'propget'], HRESULT, 'Char',
              ( ['retval', 'out'], POINTER(c_int), 'pch' )),
    COMMETHOD([dispid(513), 'propput'], HRESULT, 'Char',
              ( ['in'], c_int, 'pch' )),
    COMMETHOD([dispid(514), 'propget'], HRESULT, 'Duplicate',
              ( ['retval', 'out'], POINTER(POINTER(ITextRange)), 'ppRange' )),
    COMMETHOD([dispid(515), 'propget'], HRESULT, 'FormattedText',
              ( ['retval', 'out'], POINTER(POINTER(ITextRange)), 'ppRange' )),
    COMMETHOD([dispid(515), 'propput'], HRESULT, 'FormattedText',
              ( ['in'], POINTER(ITextRange), 'ppRange' )),
    COMMETHOD([dispid(516), 'propget'], HRESULT, 'Start',
              ( ['retval', 'out'], POINTER(c_int), 'pcpFirst' )),
    COMMETHOD([dispid(516), 'propput'], HRESULT, 'Start',
              ( ['in'], c_int, 'pcpFirst' )),
    COMMETHOD([dispid(517), 'propget'], HRESULT, 'End',
              ( ['retval', 'out'], POINTER(c_int), 'pcpLim' )),
    COMMETHOD([dispid(517), 'propput'], HRESULT, 'End',
              ( ['in'], c_int, 'pcpLim' )),
    COMMETHOD([dispid(518), 'propget'], HRESULT, 'Font',
              ( ['retval', 'out'], POINTER(POINTER(ITextFont)), 'pFont' )),
    COMMETHOD([dispid(518), 'propput'], HRESULT, 'Font',
              ( ['in'], POINTER(ITextFont), 'pFont' )),
    COMMETHOD([dispid(519), 'propget'], HRESULT, 'Para',
              ( ['retval', 'out'], POINTER(POINTER(ITextPara)), 'pPara' )),
    COMMETHOD([dispid(519), 'propput'], HRESULT, 'Para',
              ( ['in'], POINTER(ITextPara), 'pPara' )),
    COMMETHOD([dispid(520), 'propget'], HRESULT, 'StoryLength',
              ( ['retval', 'out'], POINTER(c_int), 'pcch' )),
    COMMETHOD([dispid(521), 'propget'], HRESULT, 'StoryType',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(528)], HRESULT, 'Collapse',
              ( ['in'], c_int, 'bStart' )),
    COMMETHOD([dispid(529)], HRESULT, 'Expand',
              ( ['in'], c_int, 'Unit' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(530)], HRESULT, 'GetIndex',
              ( ['in'], c_int, 'Unit' ),
              ( ['retval', 'out'], POINTER(c_int), 'pIndex' )),
    COMMETHOD([dispid(531)], HRESULT, 'SetIndex',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Index' ),
              ( ['in'], c_int, 'Extend' )),
    COMMETHOD([dispid(532)], HRESULT, 'SetRange',
              ( ['in'], c_int, 'cpActive' ),
              ( ['in'], c_int, 'cpOther' )),
    COMMETHOD([dispid(533)], HRESULT, 'InRange',
              ( ['in'], POINTER(ITextRange), 'pRange' ),
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(534)], HRESULT, 'InStory',
              ( ['in'], POINTER(ITextRange), 'pRange' ),
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(535)], HRESULT, 'IsEqual',
              ( ['in'], POINTER(ITextRange), 'pRange' ),
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(536)], HRESULT, 'Select'),
    COMMETHOD([dispid(537)], HRESULT, 'StartOf',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(544)], HRESULT, 'EndOf',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(545)], HRESULT, 'Move',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(546)], HRESULT, 'MoveStart',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(547)], HRESULT, 'MoveEnd',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(548)], HRESULT, 'MoveWhile',
              ( ['in'], POINTER(VARIANT), 'Cset' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(549)], HRESULT, 'MoveStartWhile',
              ( ['in'], POINTER(VARIANT), 'Cset' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(550)], HRESULT, 'MoveEndWhile',
              ( ['in'], POINTER(VARIANT), 'Cset' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(551)], HRESULT, 'MoveUntil',
              ( ['in'], POINTER(VARIANT), 'Cset' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(552)], HRESULT, 'MoveStartUntil',
              ( ['in'], POINTER(VARIANT), 'Cset' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(553)], HRESULT, 'MoveEndUntil',
              ( ['in'], POINTER(VARIANT), 'Cset' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(560)], HRESULT, 'FindText',
              ( ['in'], BSTR, 'bstr' ),
              ( ['in'], c_int, 'cch' ),
              ( ['in'], c_int, 'Flags' ),
              ( ['retval', 'out'], POINTER(c_int), 'pLength' )),
    COMMETHOD([dispid(561)], HRESULT, 'FindTextStart',
              ( ['in'], BSTR, 'bstr' ),
              ( ['in'], c_int, 'cch' ),
              ( ['in'], c_int, 'Flags' ),
              ( ['retval', 'out'], POINTER(c_int), 'pLength' )),
    COMMETHOD([dispid(562)], HRESULT, 'FindTextEnd',
              ( ['in'], BSTR, 'bstr' ),
              ( ['in'], c_int, 'cch' ),
              ( ['in'], c_int, 'Flags' ),
              ( ['retval', 'out'], POINTER(c_int), 'pLength' )),
    COMMETHOD([dispid(563)], HRESULT, 'Delete',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(564)], HRESULT, 'Cut',
              ( ['out'], POINTER(VARIANT), 'pVar' )),
    COMMETHOD([dispid(565)], HRESULT, 'Copy',
              ( ['out'], POINTER(VARIANT), 'pVar' )),
    COMMETHOD([dispid(566)], HRESULT, 'Paste',
              ( ['in'], POINTER(VARIANT), 'pVar' ),
              ( ['in'], c_int, 'Format' )),
    COMMETHOD([dispid(567)], HRESULT, 'CanPaste',
              ( ['in'], POINTER(VARIANT), 'pVar' ),
              ( ['in'], c_int, 'Format' ),
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(568)], HRESULT, 'CanEdit',
              ( ['retval', 'out'], POINTER(c_int), 'pbCanEdit' )),
    COMMETHOD([dispid(569)], HRESULT, 'ChangeCase',
              ( ['in'], c_int, 'Type' )),
    COMMETHOD([dispid(576)], HRESULT, 'GetPoint',
              ( ['in'], c_int, 'Type' ),
              ( ['out'], POINTER(c_int), 'px' ),
              ( ['out'], POINTER(c_int), 'py' )),
    COMMETHOD([dispid(577)], HRESULT, 'SetPoint',
              ( ['in'], c_int, 'x' ),
              ( ['in'], c_int, 'y' ),
              ( ['in'], c_int, 'Type' ),
              ( ['in'], c_int, 'Extend' )),
    COMMETHOD([dispid(578)], HRESULT, 'ScrollIntoView',
              ( ['in'], c_int, 'Value' )),
    COMMETHOD([dispid(579)], HRESULT, 'GetEmbeddedObject',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'ppv' )),
]
class ITextSelection(ITextRange):
    _case_insensitive_ = True
    _iid_ = GUID('{8CC497C1-A1DF-11CE-8098-00AA0047BE5D}')
    _idlflags_ = ['nonextensible', 'dual', 'oleautomation']
ITextSelection._methods_ = [
    COMMETHOD([dispid(257), 'propget'], HRESULT, 'Flags',
              ( ['retval', 'out'], POINTER(c_int), 'pFlags' )),
    COMMETHOD([dispid(257), 'propput'], HRESULT, 'Flags',
              ( ['in'], c_int, 'pFlags' )),
    COMMETHOD([dispid(258), 'propget'], HRESULT, 'Type',
              ( ['retval', 'out'], POINTER(c_int), 'pType' )),
    COMMETHOD([dispid(259)], HRESULT, 'MoveLeft',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(260)], HRESULT, 'MoveRight',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(261)], HRESULT, 'MoveUp',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(262)], HRESULT, 'MoveDown',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Count' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(263)], HRESULT, 'HomeKey',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(264)], HRESULT, 'EndKey',
              ( ['in'], c_int, 'Unit' ),
              ( ['in'], c_int, 'Extend' ),
              ( ['retval', 'out'], POINTER(c_int), 'pDelta' )),
    COMMETHOD([dispid(265)], HRESULT, 'TypeText',
              ( ['in'], BSTR, 'bstr' )),
]
class __MIDL_IWinTypes_0009(Union):
    pass
__MIDL_IWinTypes_0009._fields_ = [
    ('hInproc', c_int),
    ('hRemote', c_int),
]
assert sizeof(__MIDL_IWinTypes_0009) == 4, sizeof(__MIDL_IWinTypes_0009)
assert alignment(__MIDL_IWinTypes_0009) == 4, alignment(__MIDL_IWinTypes_0009)
ITextPara._methods_ = [
    COMMETHOD([dispid(0), 'propget'], HRESULT, 'Duplicate',
              ( ['retval', 'out'], POINTER(POINTER(ITextPara)), 'ppPara' )),
    COMMETHOD([dispid(0), 'propput'], HRESULT, 'Duplicate',
              ( ['in'], POINTER(ITextPara), 'ppPara' )),
    COMMETHOD([dispid(1025)], HRESULT, 'CanChange',
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(1026)], HRESULT, 'IsEqual',
              ( ['in'], POINTER(ITextPara), 'pPara' ),
              ( ['retval', 'out'], POINTER(c_int), 'pB' )),
    COMMETHOD([dispid(1027)], HRESULT, 'Reset',
              ( ['in'], c_int, 'Value' )),
    COMMETHOD([dispid(1028), 'propget'], HRESULT, 'Style',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1028), 'propput'], HRESULT, 'Style',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1029), 'propget'], HRESULT, 'Alignment',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1029), 'propput'], HRESULT, 'Alignment',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1030), 'propget'], HRESULT, 'Hyphenation',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1030), 'propput'], HRESULT, 'Hyphenation',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1031), 'propget'], HRESULT, 'FirstLineIndent',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(1032), 'propget'], HRESULT, 'KeepTogether',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1032), 'propput'], HRESULT, 'KeepTogether',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1033), 'propget'], HRESULT, 'KeepWithNext',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1033), 'propput'], HRESULT, 'KeepWithNext',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1040), 'propget'], HRESULT, 'LeftIndent',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(1041), 'propget'], HRESULT, 'LineSpacing',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(1042), 'propget'], HRESULT, 'LineSpacingRule',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1043), 'propget'], HRESULT, 'ListAlignment',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1043), 'propput'], HRESULT, 'ListAlignment',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1044), 'propget'], HRESULT, 'ListLevelIndex',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1044), 'propput'], HRESULT, 'ListLevelIndex',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1045), 'propget'], HRESULT, 'ListStart',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1045), 'propput'], HRESULT, 'ListStart',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1046), 'propget'], HRESULT, 'ListTab',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(1046), 'propput'], HRESULT, 'ListTab',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(1047), 'propget'], HRESULT, 'ListType',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1047), 'propput'], HRESULT, 'ListType',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1048), 'propget'], HRESULT, 'NoLineNumber',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1048), 'propput'], HRESULT, 'NoLineNumber',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1049), 'propget'], HRESULT, 'PageBreakBefore',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1049), 'propput'], HRESULT, 'PageBreakBefore',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1056), 'propget'], HRESULT, 'RightIndent',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(1056), 'propput'], HRESULT, 'RightIndent',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(1057)], HRESULT, 'SetIndents',
              ( ['in'], c_float, 'StartIndent' ),
              ( ['in'], c_float, 'LeftIndent' ),
              ( ['in'], c_float, 'RightIndent' )),
    COMMETHOD([dispid(1058)], HRESULT, 'SetLineSpacing',
              ( ['in'], c_int, 'LineSpacingRule' ),
              ( ['in'], c_float, 'LineSpacing' )),
    COMMETHOD([dispid(1059), 'propget'], HRESULT, 'SpaceAfter',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(1059), 'propput'], HRESULT, 'SpaceAfter',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(1060), 'propget'], HRESULT, 'SpaceBefore',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(1060), 'propput'], HRESULT, 'SpaceBefore',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(1061), 'propget'], HRESULT, 'WidowControl',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(1061), 'propput'], HRESULT, 'WidowControl',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(1062), 'propget'], HRESULT, 'TabCount',
              ( ['retval', 'out'], POINTER(c_int), 'pCount' )),
    COMMETHOD([dispid(1063)], HRESULT, 'AddTab',
              ( ['in'], c_float, 'tbPos' ),
              ( ['in'], c_int, 'tbAlign' ),
              ( ['in'], c_int, 'tbLeader' )),
    COMMETHOD([dispid(1064)], HRESULT, 'ClearAllTabs'),
    COMMETHOD([dispid(1065)], HRESULT, 'DeleteTab',
              ( ['in'], c_float, 'tbPos' )),
    COMMETHOD([dispid(1072)], HRESULT, 'GetTab',
              ( ['in'], c_int, 'iTab' ),
              ( ['out'], POINTER(c_float), 'ptbPos' ),
              ( ['out'], POINTER(c_int), 'ptbAlign' ),
              ( ['out'], POINTER(c_int), 'ptbLeader' )),
]
ITextDocument._methods_ = [
    COMMETHOD([dispid(0), 'propget'], HRESULT, 'Name',
              ( ['retval', 'out'], POINTER(BSTR), 'pName' )),
    COMMETHOD([dispid(1), 'propget'], HRESULT, 'Selection',
              ( ['retval', 'out'], POINTER(POINTER(ITextSelection)), 'ppSel' )),
    COMMETHOD([dispid(2), 'propget'], HRESULT, 'StoryCount',
              ( ['retval', 'out'], POINTER(c_int), 'pCount' )),
    COMMETHOD([dispid(3), 'propget'], HRESULT, 'StoryRanges',
              ( ['retval', 'out'], POINTER(POINTER(ITextStoryRanges)), 'ppStories' )),
    COMMETHOD([dispid(4), 'propget'], HRESULT, 'Saved',
              ( ['retval', 'out'], POINTER(c_int), 'pValue' )),
    COMMETHOD([dispid(4), 'propput'], HRESULT, 'Saved',
              ( ['in'], c_int, 'pValue' )),
    COMMETHOD([dispid(5), 'propget'], HRESULT, 'DefaultTabStop',
              ( ['retval', 'out'], POINTER(c_float), 'pValue' )),
    COMMETHOD([dispid(5), 'propput'], HRESULT, 'DefaultTabStop',
              ( ['in'], c_float, 'pValue' )),
    COMMETHOD([dispid(6)], HRESULT, 'New'),
    COMMETHOD([dispid(7)], HRESULT, 'Open',
              ( ['in'], POINTER(VARIANT), 'pVar' ),
              ( ['in'], c_int, 'Flags' ),
              ( ['in'], c_int, 'CodePage' )),
    COMMETHOD([dispid(8)], HRESULT, 'Save',
              ( ['in'], POINTER(VARIANT), 'pVar' ),
              ( ['in'], c_int, 'Flags' ),
              ( ['in'], c_int, 'CodePage' )),
    COMMETHOD([dispid(9)], HRESULT, 'Freeze',
              ( ['retval', 'out'], POINTER(c_int), 'pCount' )),
    COMMETHOD([dispid(10)], HRESULT, 'Unfreeze',
              ( ['retval', 'out'], POINTER(c_int), 'pCount' )),
    COMMETHOD([dispid(11)], HRESULT, 'BeginEditCollection'),
    COMMETHOD([dispid(12)], HRESULT, 'EndEditCollection'),
    COMMETHOD([dispid(13)], HRESULT, 'Undo',
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'prop' )),
    COMMETHOD([dispid(14)], HRESULT, 'Redo',
              ( ['in'], c_int, 'Count' ),
              ( ['retval', 'out'], POINTER(c_int), 'prop' )),
    COMMETHOD([dispid(15)], HRESULT, 'Range',
              ( ['in'], c_int, 'cp1' ),
              ( ['in'], c_int, 'cp2' ),
              ( ['retval', 'out'], POINTER(POINTER(ITextRange)), 'ppRange' )),
    COMMETHOD([dispid(16)], HRESULT, 'RangeFromPoint',
              ( ['in'], c_int, 'x' ),
              ( ['in'], c_int, 'y' ),
              ( ['retval', 'out'], POINTER(POINTER(ITextRange)), 'ppRange' )),
]
ITextDocument2._methods_ = [
    COMMETHOD([dispid(21), helpstring(u'method AttachMsgFilter')], HRESULT, 'AttachMsgFilter',
              ( ['in'], POINTER(IUnknown), 'pFilter' )),
    COMMETHOD([dispid(22), helpstring(u'method SetEffectColor')], HRESULT, 'SetEffectColor',
              ( ['in'], c_int, 'Index' ),
              ( ['in'], c_ulong, 'cr' )),
    COMMETHOD([dispid(23), helpstring(u'method GetEffectColor')], HRESULT, 'GetEffectColor',
              ( ['in'], c_int, 'Index' ),
              ( ['out'], POINTER(c_ulong), 'pcr' )),
    COMMETHOD([dispid(24), helpstring(u'method GetCaretType'), 'propget'], HRESULT, 'CaretType',
              ( ['retval', 'out'], POINTER(c_int), 'pCaretType' )),
    COMMETHOD([dispid(24), helpstring(u'method GetCaretType'), 'propput'], HRESULT, 'CaretType',
              ( ['in'], c_int, 'pCaretType' )),
    COMMETHOD([dispid(25), helpstring(u'method GetImmContext')], HRESULT, 'GetImmContext',
              ( ['retval', 'out'], POINTER(c_int), 'pContext' )),
    COMMETHOD([dispid(26), helpstring(u'method ReleaseImmContext')], HRESULT, 'ReleaseImmContext',
              ( ['in'], c_int, 'Context' )),
    COMMETHOD([dispid(27), helpstring(u'method GetPreferredFont')], HRESULT, 'GetPreferredFont',
              ( ['in'], c_int, 'cp' ),
              ( ['in'], c_int, 'CodePage' ),
              ( ['in'], c_int, 'Option' ),
              ( ['in'], c_int, 'curCodepage' ),
              ( ['in'], c_int, 'curFontSize' ),
              ( ['out'], POINTER(BSTR), 'pbstr' ),
              ( ['out'], POINTER(c_int), 'pPitchAndFamily' ),
              ( ['out'], POINTER(c_int), 'pNewFontSize' )),
    COMMETHOD([dispid(28), helpstring(u'method GetNotificationMode'), 'propget'], HRESULT, 'NotificationMode',
              ( ['retval', 'out'], POINTER(c_int), 'pMode' )),
    COMMETHOD([dispid(28), helpstring(u'method GetNotificationMode'), 'propput'], HRESULT, 'NotificationMode',
              ( ['in'], c_int, 'pMode' )),
    COMMETHOD([dispid(29), helpstring(u'method GetClientRect')], HRESULT, 'GetClientRect',
              ( ['in'], c_int, 'Type' ),
              ( ['out'], POINTER(c_int), 'pLeft' ),
              ( ['out'], POINTER(c_int), 'pTop' ),
              ( ['out'], POINTER(c_int), 'pRight' ),
              ( ['out'], POINTER(c_int), 'pBottom' )),
    COMMETHOD([dispid(30), helpstring(u'method GetSelectionEx'), 'propget'], HRESULT, 'SelectionEx',
              ( ['retval', 'out'], POINTER(POINTER(ITextSelection)), 'ppSel' )),
    COMMETHOD([dispid(31), helpstring(u'method GetWindow')], HRESULT, 'GetWindow',
              ( ['out'], POINTER(c_int), 'phWnd' )),
    COMMETHOD([dispid(32), helpstring(u'method GetFEFlags')], HRESULT, 'GetFEFlags',
              ( ['out'], POINTER(c_int), 'pFlags' )),
    COMMETHOD([dispid(33), helpstring(u'method UpdateWindow')], HRESULT, 'UpdateWindow'),
    COMMETHOD([dispid(34), helpstring(u'method CheckTextLimit')], HRESULT, 'CheckTextLimit',
              ( [], c_int, 'cch' ),
              ( [], POINTER(c_int), 'pcch' )),
    COMMETHOD([dispid(35), helpstring(u'method IMEInProgress')], HRESULT, 'IMEInProgress',
              ( [], c_int, 'Mode' )),
    COMMETHOD([dispid(36), helpstring(u'method SysBeep')], HRESULT, 'SysBeep'),
    COMMETHOD([dispid(37), helpstring(u'method Update')], HRESULT, 'Update',
              ( ['in'], c_int, 'Mode' )),
    COMMETHOD([dispid(38), helpstring(u'method Notify')], HRESULT, 'Notify',
              ( ['in'], c_int, 'Notify' )),
    COMMETHOD([dispid(39), helpstring(u'method GetDocumentFont')], HRESULT, 'GetDocumentFont',
              ( ['retval', 'out'], POINTER(POINTER(ITextFont)), 'ppITextFont' )),
    COMMETHOD([dispid(40), helpstring(u'method GetDocumentPara')], HRESULT, 'GetDocumentPara',
              ( ['retval', 'out'], POINTER(POINTER(ITextPara)), 'ppITextPara' )),
    COMMETHOD([dispid(41), helpstring(u'method GetCallManager')], HRESULT, 'GetCallManager',
              ( ['retval', 'out'], POINTER(POINTER(IUnknown)), 'ppVoid' )),
    COMMETHOD([dispid(42), helpstring(u'method ReleaseCallManager')], HRESULT, 'ReleaseCallManager',
              ( [], POINTER(IUnknown), 'pVoid' )),
]
class _RemotableHandle(Structure):
    pass
_RemotableHandle._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0009),
]
assert sizeof(_RemotableHandle) == 8, sizeof(_RemotableHandle)
assert alignment(_RemotableHandle) == 4, alignment(_RemotableHandle)
