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
latestSchemaVersion = 20

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
	reportLanguage = boolean(default=false)
	reportNotSupportedLanguage = option("speech", "beep", "off", default="speech")
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
		excludedDisplays = string_list(default=list("dotPad"))

	# Braille display driver settings
	[[__many__]]
		port = string(default="")

# Vision enhancement provider settings
[vision]

	# Vision enhancement provider settings
	[[__many__]]
		enabled = boolean(default=false)

# Magnifier settings
[magnifier]
	defaultZoomLevel = float(min=1.0, max=10.0, default=2.0)
	defaultFullscreenMode = string(default="center")
	defaultFilter = string(default="normal")
	keepMouseCentered = boolean(default=false)
	saveShortcutChanges = boolean(default=false)

# Presentation settings
[presentation]
		reportKeyboardShortcuts = boolean(default=true)
		reportObjectPositionInformation = boolean(default=true)
		guessObjectPositionInformationWhenUnavailable = boolean(default=false)
		reportMultiSelect = boolean(default=false)
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
	# Bitwise combination of none, some or all values of ReportSpellingErrors
	# 1: Speech, 2: Sound, 4: Braille
	reportSpellingErrors2 = integer(min=0, max=7, default=1)
	reportPage = boolean(default=true)
	reportLineNumber = boolean(default=False)
	# 0: Off, 1: Speech, 2: Tones, 3: Both Speech and Tones
	reportLineIndentation = integer(0, 3, default=0)
	ignoreBlankLinesForRLI = boolean(default=False)
	# Duration of indentation beeps, in milliseconds
	indentToneDuration = integer(min=10, max=2000, default=40)
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
	bdDetect = boolean(default=False)

[uwpOcr]
	language = string(default="")
	autoRefresh = boolean(default=false)
	autoRefreshInterval = integer(default=1500, min=100)
	autoSayAllOnResult = boolean(default=false)

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
		muteOnLocalControl = boolean(default=False)

[math]
	[[speech]]
		# LearningDisability, Blindness, LowVision
		impairment = string(default="Blindness")
		# any known language code and sub-code -- could be en-uk, etc
		language = string(default="Auto")
		# Any known speech style (falls back to ClearSpeak)
		speechStyle = string(default="ClearSpeak")
		# Terse, Medium, Verbose
		verbosity = string(default="Medium")
		# Change from text speech rate (%)
		mathRate = integer(default=100)
		# Change from normal pause length (%)
		pauseFactor = integer(default=100)
		# make a sound when starting/ending math speech -- None, Beep
		speechSound = string(default="None")
		# NOTE: not currently working in MathCAT
		subjectArea = string(default="General")
		# SpellOut (H 2 0), AsCompound (Water) -- not implemented, Off (H sub 2 O)
		chemistry = string(default="SpellOut")
		# Verbose, Brief, SuperBrief
		mathSpeak = string(default="Verbose")

		[[speech.speechOverrides]]
			# word to say as a prefix/postfix for capital letters; empty string leaves it calling AT with Unicode fallback
			capitalLetters = string(default="")
			# word used as override (not implemented)
			leftParen = string(default="")
			# word used as override (not implemented)
			rightParen = string(default="")

		# see ClearSpeak speak for meanings
		[[speech.ClearSpeak]]
			# SayCaps or use pitch
			capitalLetters = string(default="Auto")
			# Valid values: AbsEnd, Cardinality, Determinant, Auto
			absoluteValue = string(default="Auto")
			# Valid values: Ordinal, Over, FracOver, General, EndFrac, GeneralEndFrac, OverEndFrac, Per, Auto
			fractions = string(default="Auto")
			# Valid values: Ordinal, OrdinalPower, AfterPower, Auto
			exponents = string(default="Auto")
			# Valid values: PosNegSqRoot, RootEnd, PosNegSqRootEnd, Auto
			roots = string(default="Auto")
			# Valid values: Auto, None
			functions = string(default="Auto")
			# Valid values: TrigInverse, ArcTrig, Auto
			trig = string(default="Auto")
			# Valid values: LnAsNaturalLog, Auto
			log = string(default="Auto")
			# Valid values: MoreImpliedTimes , None, Auto
			impliedTimes = string(default="Auto")
			# Valid values: Speak, SpeakNestingLevel, Silent, CoordPoint, Interval, Auto
			paren = string(default="Auto")
			# Valid values: SpeakColNum, SilentColNum, EndMatrix, Vector, EndVector, Combinatorics, Auto
			matrix = string(default="Auto")
			# Valid values: Case, Constraint, Equation, Line, None, Row, Step, Auto
			multiLineLabel = string(default="Auto")
			# Valid values: None, Auto
			multiLineOverview = string(default="Auto")
			# Valid values: Long, Short
			multiLinePausesBetweenColumns = string(default="Short")
			# Valid values: woAll, SilentBracket, Auto
			sets = string(default="Auto")
			# Valid values: By, Cross, Auto
			multSymbolX = string(default="Auto")
			# Valid values: Dot, Auto
			multSymbolDot = string(default="Auto")
			# Valid values: Delta, Auto
			triangleSymbol = string(default="Auto")
			# Valid values: AndSoOn, Auto
			ellipses = string(default="Auto")
			# Valid values: SuchThat, Divides, Given, Auto
			verticalLine = string(default="Auto")
			# Valid values: Belongs, Element, Member, Auto
			setMemberSymbol = string(default="Auto")
			# Valid values: Angle, Length, Auto
			prime = string(default="Auto")
			# Valid values: ChoosePermute, Auto
			combinationPermutation = string(default="Auto")
			# Valid values: Bar, Conjugate, Mean, Auto
			bar = string(default="Auto")

	[[navigation]]
		# Valid values: Enhanced, Simple, Character
		navMode = string(default="Enhanced")
		# remember previous value and use it
		resetNavMode = boolean(default=false)
		# speak the expression or give a description/overview
		overview = boolean(default=false)
		# remember previous value and use it
		resetOverview = boolean(default=true)
		# Terse, Medium, Full (words to say for nav command)
		navVerbosity = string(default="Medium")
		# Auto zoom out of 2D exprs (use shift-arrow to force zoom out if unchecked)
		autoZoomOut = boolean(default=true)
		# MathML, LaTeX, ASCIIMath
		copyAs = string(default="MathML")

	[[braille]]
		# Any supported Braille code (such as UEB) or "Auto"
		brailleCode = string(default="Auto")
		# Highlight with dots 7 & 8 the current nav node -- values are Off, FirstChar, EndPoints, All
		brailleNavHighlight = string(default="EndPoints")
		# true/false
		useSpacesAroundAllOperators = boolean(default=false)

		[[braille.nemeth]]
			# Nemeth defines the typeforms: Bold, Italic, SansSerif, and Script. That leaves out DoubleStruck (Blackboard Bold)
			# Here we provide an option to specify a transcriber-defined typeform changes, with the default mapping DoubleStruck to Italic
			# first transcriber-defined typeform prefix indicator
			sansSerif = string(default="⠠⠨")
			bold = string(default="⠸")
			doubleStruck = string(default="⠨")
			script = string(default="⠈")
			italic = string(default="⠨")

		[[braille.UEB]]
		   	# Grade1/Grade2 -- assumed starting mode UEB braille (Grade1 assumes we are in G1 passage mode)
			startMode = string(default="Grade2")
			# true/false
			useSpacesAroundAllOperators = string(default=false)

			# UEB Guide to Technical Material (https://iceb.org/Guidelines_for_Technical_Material_2008-10.pdf)
			#   says to normally treat Fraktur and DoubleStruck as Script
			# Here we provide an option to specify a transcriber-defined typeform prefix indicator instead
			# Note: here are prefixes for 1st - 5th: "⠈⠼", "⠘⠼", "⠸⠼", "⠐⠼", "⠨⠼"
			doubleStruck = string(default="⠈")
			fraktur  = string(default="⠈")
			sansSerif = string(default="⠈⠼")
			greekVariant = string(default="⠨")

		[[braille.vietnam]]
			# drop digits down a row in simple numeric fractions
			useDropNumbers = boolean(default=false)
			# The guideline is being revised -- current guidance is to follow UEB for alternative scripts
			# UEB Guide to Technical Material (https://iceb.org/Guidelines_for_Technical_Material_2008-10.pdf)
			#   says to normally treat Fraktur and DoubleStruck as Script
			# Here we provide an option to specify a transcriber-defined typeform prefix indicator instead
			# Note: here are prefixes for 1st - 5th: "⠈⠼", "⠘⠼", "⠸⠼", "⠐⠼", "⠨⠼"
			doubleStruck = string(default="⠈")
			fraktur = string(default="⠈")
			# first transcriber-defined typeform prefix indicator
			sansSerif = string(default="⠈⠼")
			# default to Greek
			greekVariant = string(default="⠸")

		[[braille.LaTeX]]
			# Use the short form for the latex (e.g., "~a" instead of "\alpha")
			useShortName = boolean(default=false)


	[[other]]
		# [default]
		decimalSeparators = string(default=".")
		# [default -- includes two forms of non-breaking spaces]
		blockSeparators = string(default=", \u00a0\u202f")
		# Auto, '.', ',', Custom
		decimalSeparator = string(default="Auto")

[screenCurtain]
	enabled = boolean(default=false)
	warnOnLoad = boolean(default=true)
	playToggleSounds = boolean(default=true)
"""

#: The configuration specification
#: @type: ConfigObj
confspec = ConfigObj(StringIO(configSpecString), list_values=False, encoding="UTF-8")
confspec.newlines = "\r\n"
