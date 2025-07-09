# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Davy Kager, Bill Dengler, Julien Cochuyt,
# Joseph Lee, Dawid Pieper, mltony, Bram Duvigneau, Cyrille Bougot, Rob Meredith,
# Burman's Computer and Education Ltd., Leonard de Ruijter, Łukasz Golonka, Cary-rowen
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from io import StringIO
from configobj import ConfigObj
from . import configDefaults

#: The version of the schema outlined in this file. Increment this when modifying the schema and
#: provide an upgrade step (@see profileUpgradeSteps.py). An upgrade step does not need to be added when
#: just adding a new element to (or removing from) the schema, only when old versions of the config
#: (conforming to old schema versions) will not work correctly with the new schema.
latestSchemaVersion = 17

#: The configuration specification string
#: @type: String
configSpecString = f"""# NVDA Configuration File
schemaVersion = integer(min=0, default={latestSchemaVersion})
[general]
	language = string(default="Windows")
	saveConfigurationOnExit = boolean(default=True)
	askToExit = boolean(default=true)
	playStartAndExitSounds = boolean(default=true)
	#possible log levels are DEBUG, IO, DEBUGWARNING, INFO
	loggingLevel = string(default="INFO")
	showWelcomeDialogAtStartup = boolean(default=true)
	preventDisplayTurningOff = boolean(default=true)

# Speech settings
[speech]
	# The synthesizer to use
	synth = string(default=auto)
	# symbolLevel: One of the characterProcessing.SymbolLevel values.
	symbolLevel = integer(default=100)
	trustVoiceLanguage = boolean(default=true)
	unicodeNormalization = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
	reportNormalizedForCharacterNavigation = boolean(default=true)
	symbolDictionaries = string_list(default=list("cldr"))
	beepSpeechModePitch = integer(default=10000,min=50,max=11025)
	autoLanguageSwitching = boolean(default=true)
	autoDialectSwitching = boolean(default=false)
	delayedCharacterDescriptions = boolean(default=false)
	excludedSpeechModes = int_list(default=list())
	trimLeadingSilence = boolean(default=true)
	useWASAPIForSAPI4 = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")

	[[__many__]]
		capPitchChange = integer(default=30,min=-100,max=100)
		sayCapForCapitals = boolean(default=false)
		beepForCapitals = boolean(default=false)
		useSpellingFunctionality = boolean(default=true)

# Audio settings
[audio]
	outputDevice = string(default=default)
	audioDuckingMode = integer(default=0)
	soundVolumeFollowsVoice = boolean(default=false)
	soundVolume = integer(default=100, min=0, max=100)
	audioAwakeTime = integer(default=30, min=0, max=3600)
	whiteNoiseVolume = integer(default=0, min=0, max=100)
	soundSplitState = integer(default=0)
	includedSoundSplitModes = int_list(default=list(0, 2, 3))

# Braille settings
[braille]
	display = string(default=auto)
	mode = option("followCursors", "speechOutput", default="followCursors")
	translationTable = string(default=auto)
	inputTable = string(default=auto)
	expandAtCursor = boolean(default=true)
	showCursor = boolean(default=true)
	cursorBlink = boolean(default=true)
	cursorBlinkRate = integer(default=500,min=200,max=2000)
	cursorShapeFocus = integer(default=192,min=1,max=255)
	cursorShapeReview = integer(default=128,min=1,max=255)
	# How braille display will show messages
	# 0: Disabled, 1: Use timeout, 2: Show indefinitely
	showMessages = integer(0, 2, default=1)
	# Timeout after the message will disappear from braille display
	messageTimeout = integer(default=4, min=1, max=20)
	tetherTo = option("auto", "focus", "review", default="auto")
	reviewRoutingMovesSystemCaret = featureFlag(\
		optionsEnum="ReviewRoutingMovesSystemCaretFlag", behaviorOfDefault="NEVER")
	readByParagraph = boolean(default=false)
	paragraphStartMarker = option("", " ", "¶", default="")
	wordWrap = boolean(default=true)
	unicodeNormalization = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="disabled")
	focusContextPresentation = option("changedContext", "fill", "scroll", default="changedContext")
	interruptSpeechWhileScrolling = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
	speakOnRouting = boolean(default=false)
	speakOnNavigatingByUnit = boolean(default=false)
	showSelection = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
	reportLiveRegions = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
	fontFormattingDisplay = featureFlag(optionsEnum="FontFormattingBrailleModeFlag", behaviorOfDefault="LIBLOUIS")
	[[auto]]
    	excludedDisplays = string_list(default=list())

	# Braille display driver settings
	[[__many__]]
		port = string(default="")

# Vision enhancement provider settings
[vision]

	# Vision enhancement provider settings
	[[__many__]]
		enabled = boolean(default=false)

# Presentation settings
[presentation]
		reportKeyboardShortcuts = boolean(default=true)
		reportObjectPositionInformation = boolean(default=true)
		guessObjectPositionInformationWhenUnavailable = boolean(default=false)
		reportTooltips = boolean(default=false)
		reportHelpBalloons = boolean(default=true)
		reportObjectDescriptions = boolean(default=True)
		reportDynamicContentChanges = boolean(default=True)
		reportAutoSuggestionsWithSound = boolean(default=True)
	[[progressBarUpdates]]
		reportBackgroundProgressBars = boolean(default=false)
		#output modes are beep, speak, both, or off
		progressBarOutputMode = string(default="beep")
		speechPercentageInterval = integer(default=10)
		beepPercentageInterval = integer(default=1)
		beepMinHZ = integer(default=110)

[mouse]
	enableMouseTracking = boolean(default=True) #must be true for any of the other settings to work
	mouseTextUnit = string(default="paragraph")
	reportObjectRoleOnMouseEnter = boolean(default=False)
	audioCoordinatesOnMouseMove = boolean(default=False)
	audioCoordinates_detectBrightness = boolean(default=False)
	audioCoordinates_blurFactor = integer(default=3)
	audioCoordinates_minVolume = float(default=0.1)
	audioCoordinates_maxVolume = float(default=1.0)
	audioCoordinates_minPitch = integer(default=220)
	audioCoordinates_maxPitch = integer(default=880)
	reportMouseShapeChanges = boolean(default=false)
	ignoreInjectedMouseInput = boolean(default=false)

[speechViewer]
	showSpeechViewerAtStartup = boolean(default=false)
	autoPositionWindow = boolean(default=True)
	# Values for positioning the window.
	# Defaults are not used.
	# They should not be read if autoPositionWindow is True
	x = integer()
	y = integer()
	width = integer()
	height = integer()
	displays = string_list()

[brailleViewer]
	showBrailleViewerAtStartup = boolean(default=false)
	shouldHoverRouteToCell = boolean(default=false)
	secondsOfHoverToActivate = float(min=0.0, default=1.0)
	# Devices with 40 cells are quite common.
	defaultCellCount = integer(min=20, max=160, default=40)
	autoPositionWindow = boolean(default=True)
	# Values for positioning the window.
	# Defaults are not used.
	# They should not be read if autoPositionWindow is True
	x = integer()
	y = integer()
	displays = string_list()

#Keyboard settings
[keyboard]
	# NVDAModifierKeys: Integer value combining single-bit value:
	# 1: CapsLock
	# 2: NumpadInsert
	# 4: ExtendedInsert
	# Default = 6: NumpadInsert + ExtendedInsert
	NVDAModifierKeys = integer(1, 7, default=6)
	keyboardLayout = string(default="desktop")
	# 0: Off, 1: Only in edit controls, 2: Always
	speakTypedCharacters = integer(default=1,min=0,max=2)
	# 0: Off, 1: Only in edit controls, 2: Always
	speakTypedWords = integer(default=0,min=0,max=2)
	beepForLowercaseWithCapslock = boolean(default=true)
	speakCommandKeys = boolean(default=false)
	speechInterruptForCharacters = boolean(default=true)
	speechInterruptForEnter = boolean(default=true)
	allowSkimReadingInSayAll = boolean(default=False)
	alertForSpellingErrors = boolean(default=True)
	handleInjectedKeys= boolean(default=true)
	multiPressTimeout = integer(default=500, min=100, max=20000)

[virtualBuffers]
	maxLineLength = integer(default=100)
	linesPerPage = integer(default=25)
	useScreenLayout = boolean(default=True)
	autoPassThroughOnFocusChange = boolean(default=true)
	autoPassThroughOnCaretMove = boolean(default=false)
	passThroughAudioIndication = boolean(default=true)
	autoSayAllOnPageLoad = boolean(default=true)
	trapNonCommandGestures = boolean(default=true)
	enableOnPageLoad = boolean(default=true)
	loadChromiumVBufOnBusyState = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
	textParagraphRegex = string(default="{configDefaults.DEFAULT_TEXT_PARAGRAPH_REGEX}")

[touch]
	enabled = boolean(default=true)
	touchTyping = boolean(default=False)

#Settings for document reading (such as MS Word and wordpad)
[documentFormatting]
	# These settings affect what information is reported when you navigate
	# to text where the formatting  or placement has changed
	detectFormatAfterCursor = boolean(default=false)
	reportFontName = boolean(default=false)
	reportFontSize = boolean(default=false)
	# 0: Off, 1: Speech, 2: Braille, 3: Speech and Braille
	fontAttributeReporting = integer(0, 3, default=0)
	reportRevisions = boolean(default=true)
	reportEmphasis = boolean(default=false)
	reportHighlight = boolean(default=true)
	reportSuperscriptsAndSubscripts = boolean(default=false)
	reportColor = boolean(default=False)
	reportTransparentColor = boolean(default=False)
	reportAlignment = boolean(default=false)
	reportLineSpacing = boolean(default=false)
	reportStyle = boolean(default=false)
	reportSpellingErrors = boolean(default=true)
	reportPage = boolean(default=true)
	reportLineNumber = boolean(default=False)
	# 0: Off, 1: Speech, 2: Tones, 3: Both Speech and Tones
	reportLineIndentation = integer(0, 3, default=0)
	ignoreBlankLinesForRLI = boolean(default=False)
	reportParagraphIndentation = boolean(default=False)
	reportTables = boolean(default=true)
	includeLayoutTables = boolean(default=False)
	# 0: Off, 1: Rows and columns, 2: Rows, 3: Columns
	reportTableHeaders = integer(0, 3, default=1)
	reportTableCellCoords = boolean(default=True)
	# 0: Off, 1: style, 2: color and style
	reportCellBorders = integer(0, 2, default=0)
	reportLinks = boolean(default=true)
	reportLinkType = boolean(default=true)
	reportGraphics = boolean(default=True)
	reportComments = boolean(default=true)
	reportBookmarks = boolean(default=true)
	reportLists = boolean(default=true)
	reportHeadings = boolean(default=true)
	reportBlockQuotes = boolean(default=true)
	reportGroupings = boolean(default=true)
	reportLandmarks = boolean(default=true)
	reportArticles = boolean(default=false)
	reportFrames = boolean(default=true)
	reportFigures = boolean(default=true)
	reportClickable = boolean(default=true)

[documentNavigation]
	paragraphStyle = featureFlag(optionsEnum="ParagraphNavigationFlag", behaviorOfDefault="application")

[reviewCursor]
	simpleReviewMode = boolean(default=True)
	followFocus = boolean(default=True)
	followCaret = boolean(default=True)
	followMouse = boolean(default=False)

[UIA]
	enabled = boolean(default=true)
	useInMSExcelWhenAvailable = boolean(default=false)
	winConsoleImplementation= option("auto", "legacy", "UIA", default="auto")
	eventRegistration = option("auto", "selective", "global", default="auto")
	# 0:default, 1:Only when necessary, 2:yes, 3:no
	allowInChromium = integer(0, 3, default=0)
	# 0:default (where suitable), 1:Only when necessary, 2: where suitable, 3: always
	allowInMSWord = integer(0, 3, default=0)
	enhancedEventProcessing = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")

[annotations]
	reportDetails = boolean(default=true)
	reportAriaDescription = boolean(default=true)

[terminals]
	speakPasswords = boolean(default=false)
	keyboardSupportInLegacy = boolean(default=True)
	diffAlgo = option("auto", "dmp", "difflib", default="auto")
	wtStrategy = featureFlag(optionsEnum="WindowsTerminalStrategyFlag", behaviorOfDefault="diffing")

[update]
	autoCheck = boolean(default=true)
	startupNotification = boolean(default=true)
	allowUsageStats = boolean(default=false)
	askedAllowUsageStats = boolean(default=false)
	serverURL = string(default="")

[inputComposition]
	autoReportAllCandidates = boolean(default=True)
	announceSelectedCandidate = boolean(default=True)
	alwaysIncludeShortCharacterDescriptionInCandidateName = boolean(default=True)
	reportReadingStringChanges = boolean(default=True)
	reportCompositionStringChanges = boolean(default=True)

[debugLog]
	hwIo = boolean(default=false)
	MSAA = boolean(default=false)
	UIA = boolean(default=false)
	audioDucking = boolean(default=false)
	gui = boolean(default=false)
	louis = boolean(default=false)
	timeSinceInput = boolean(default=false)
	vision = boolean(default=false)
	speech = boolean(default=false)
	speechManager = boolean(default=false)
	synthDriver = boolean(default=false)
	nvwave = boolean(default=false)
	annotations = boolean(default=false)
	events = boolean(default=false)
	garbageHandler = boolean(default=false)
	remoteClient = boolean(default=False)
	externalPythonDependencies = boolean(default=False)

[uwpOcr]
	language = string(default="")
	autoRefresh = boolean(default=false)
	autoRefreshInterval = integer(default=1500, min=100)

[editableText]
	caretMoveTimeoutMs = integer(min=0, max=2000, default=100)

[development]
	enableScratchpadDir = boolean(default=false)

[featureFlag]
	# 0:default, 1:yes, 2:no
	cancelExpiredFocusSpeech = integer(0, 2, default=0)
	# 0:Only in test versions, 1:yes
	playErrorSound = integer(0, 1, default=0)

[addonStore]
	automaticUpdates = option("notify", "update", "disabled", default="notify")
	allowIncompatibleUpdates = boolean(default=false)
	baseServerURL = string(default="")
	# UpdateChannel values:
	# same channel (default), any channel, do not update, stable, beta & dev, beta, dev
	defaultUpdateChannel = integer(0, 6, default=0)

# Remote Settings
[remote]
	enabled = boolean(default=False)
	[[connections]]
		lastConnected = string_list(default=list())
	[[controlServer]]
		autoconnect = boolean(default=False)
		selfHosted = boolean(default=False)
		# 0: follower, 1: leader
		connectionMode = integer(default=0, min=0, max=1)
		host = string(default="")
		port = integer(default=6837)
		key = string(default="")
	[[seenMOTDs]]
		__many__ = string(default="")
	[[trustedCertificates]]
		__many__ = string(default="")
	[[ui]]
		confirmDisconnectAsFollower = boolean(default=True)
[math]
	[[Speech]]
    	Impairment = string(default="Blindness")       # LearningDisability, LowVision, Blindness
    	Language = string(default="Auto")                # any known language code and sub-code -- could be en-uk, etc
    	SpeechStyle = string(default="ClearSpeak")     # Any known speech style (falls back to ClearSpeak)
    	Verbosity = string(default="Medium")           # Terse, Medium, Verbose
    	MathRate = integer(default=100)               # Change from text speech rate (%)
    	PauseFactor = integer(default=100)            # Change from normal pause length (%)
    	SpeechSound = string(default="None")           # make a sound when starting/ending math speech -- None, Beep
    	SubjectArea = string(default="General")        # FIX: still working on this
    	Chemistry = string(default="SpellOut")         # SpellOut (H 2 0), AsCompound (Water) -- not implemented, Off (H sub 2 O)
		MathSpeak = string(default="Verbose")          # Brief, SuperBrief

		[[Speech.SpeechOverrides]]
			CapitalLetters = string(default="")        # word to say as a prefix/postfix for capital letters; empty string leaves it calling AT with Unicode fallback
			LeftParen = string(default="")             # word used as override (not implemented)
			RightParen = string(default="")            # word used as override (not implemented)

		[[Speech.ClearSpeak]]                 # see ClearSpeak speak for meanings
			CapitalLetters = string(default="Auto")      # SayCaps or use pitch
			AbsoluteValue = string(default="Auto")       # AbsEnd, Cardinality, Determinant
			Fractions = string(default="Auto")           # Ordinal, Over, FracOver, General, EndFrac, GeneralEndFrac, OverEndFrac, Per
			Exponents = string(default="Auto")           # Ordinal, OrdinalPower, AfterPower
			Roots = string(default="Auto")               # PosNegSqRoot, RootEnd, PosNegSqRootEnd
			Functions = string(default="Auto")           # None
			Trig = string(default="Auto")                # TrigInverse, ArcTrig
			Log = string(default="Auto")                 # LnAsNaturalLog
			ImpliedTimes = string(default="Auto")        # MoreImpliedTimes , None
			Paren = string(default="Auto")               # Speak, SpeakNestingLevel, Silent, CoordPoint, Interval
			Matrix = string(default="Auto")              # SpeakColNum, SilentColNum, EndMatrix, Vector, EndVector, Combinatorics
			MultiLineLabel = string(default="Auto")      # Case, Constraint, Equation, Line, None, Row, Step
			MultiLineOverview = string(default="Auto")   # None,
			MultiLinePausesBetweenColumns = string(default="Short")  # Long
			Sets = string(default="Auto")                # woAll, SilentBracket
			MultSymbolX = string(default="Auto")         # By, Cross
			MultSymbolDot = string(default="Auto")       # Dot
			TriangleSymbol = string(default="Auto")      # Delta
			Ellipses = string(default="Auto")            # AndSoOn,
			VerticalLine = string(default="Auto")        # SuchThat, Divides, Given
			SetMemberSymbol = string(default="Auto")     # Belongs, Element, Member
			Prime = string(default="Auto")               # Angle, Length
			CombinationPermutation = string(default="Auto")  # ChoosePermute
			Bar = string(default="Auto")                 # Bar, Conjugate, Mean

	[[Navigation]]
		NavMode = string(default="Enhanced")         # Enhanced, Simple, Character
		ResetNavMode = boolean(default=false)       # remember previous value and use it
		Overview = boolean(default=false)             # speak the expression or give a description/overview
		ResetOverview = boolean(default=true)        # remember previous value and use it
		NavVerbosity = string(default="Medium")        # Terse, Medium, Full (words to say for nav command)
		AutoZoomOut = boolean(default=true)           # Auto zoom out of 2D exprs (use shift-arrow to force zoom out if unchecked)
		CopyAs = string(default="MathML")       # MathML, LaTeX, ASCIIMath

	[[Braille]]
		BrailleCode = string(default="Nemeth")                # Any supported braille code (currently Nemeth, UEB)
		BrailleNavHighlight = string(default="EndPoints")   # Highlight with dots 7 & 8 the current nav node -- values are Off, FirstChar, EndPoints, All
		UseSpacesAroundAllOperators = boolean(default=false)  # true/false

		[[Braille.Nemeth]]
			# Nemeth defines the typeforms: Bold, Italic, SansSerif, and Script. That leaves out DoubleStruck (Blackboard Bold)
			# Here we provide an option to specify a transcriber-defined typeform changes, with the default mapping DoubleStruck to Italic
			SansSerif = string(default="⠠⠨")     # first transcriber-defined typeform prefix indicator
			Bold = string(default="⠸")     # t
			DoubleStruck = string(default="⠨")     # script
			Script = string(default="⠈")     # script
			Italic = string(default="⠨")     # script

		[[Braille.UEB]]
			StartMode = string(default="Grade2")   # Grade1/Grade2 -- assumed starting mode UEB braille (Grade1 assumes we are in G1 passage mode)
			UseSpacesAroundAllOperators = string(default=false)  # true/false

			# UEB Guide to Technical Material (https://iceb.org/Guidelines_for_Technical_Material_2008-10.pdf)
			#   says to normally treat Fraktur and DoubleStruck as Script
			# Here we provide an option to specify a transcriber-defined typeform prefix indicator instead
			# Note: here are prefixes for 1st - 5th: "⠈⠼", "⠘⠼", "⠸⠼", "⠐⠼", "⠨⠼"
			DoubleStruck = string(default="⠈")     # script
			Fraktur  = string(default="⠈")     # script
			SansSerif = string(default="⠈⠼")     # first transcriber-defined typeform prefix indicator
			GreekVariant = string(default="⠨")     # default to Greek

		[[Braille.Vietnam]]
			UseDropNumbers = boolean(default=false)    # drop digits down a row in simple numeric fractions
			# The guideline is being revised -- current guidance is to follow UEB for alternative scripts
			# UEB Guide to Technical Material (https://iceb.org/Guidelines_for_Technical_Material_2008-10.pdf)
			#   says to normally treat Fraktur and DoubleStruck as Script
			# Here we provide an option to specify a transcriber-defined typeform prefix indicator instead
			# Note: here are prefixes for 1st - 5th: "⠈⠼", "⠘⠼", "⠸⠼", "⠐⠼", "⠨⠼"
			DoubleStruck = string(default="⠈")     # script
			Fraktur = string(default="⠈")     # script
			SansSerif = string(default="⠈⠼")    # first transcriber-defined typeform prefix indicator
			GreekVariant = string(default="⠸")     # default to Greek

		[[Braille.LaTeX]]
			UseShortName = boolean(default=false)   # Use the short form for the latex (e.g., "~a" instead of "\alpha")


	[[Other]]
		DecimalSeparators = string(default=".") # [default]
		BlockSeparators = string(default=", \u00a0\u202f") # [default -- includes two forms of non-breaking spaces]
		DecimalSeparator = string(default="Auto") # Auto, '.', ',', Custom
"""

#: The configuration specification
#: @type: ConfigObj
confspec = ConfigObj(StringIO(configSpecString), list_values=False, encoding="UTF-8")
confspec.newlines = "\r\n"
