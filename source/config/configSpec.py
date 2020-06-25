# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2020 NV Access Limited, Babbage B.V., Davy Kager, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from io import StringIO
from configobj import ConfigObj

#: The version of the schema outlined in this file. Increment this when modifying the schema and 
#: provide an upgrade step (@see profileUpgradeSteps.py). An upgrade step does not need to be added when
#: just adding a new element to (or removing from) the schema, only when old versions of the config 
#: (conforming to old schema versions) will not work correctly with the new schema.
latestSchemaVersion = 4

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

# Speech settings
[speech]
	# The synthesizer to use
	synth = string(default=auto)
	symbolLevel = integer(default=100)
	trustVoiceLanguage = boolean(default=true)
	includeCLDR = boolean(default=True)
	beepSpeechModePitch = integer(default=10000,min=50,max=11025)
	outputDevice = string(default=default)
	autoLanguageSwitching = boolean(default=true)
	autoDialectSwitching = boolean(default=false)

	[[__many__]]
		capPitchChange = integer(default=30,min=-100,max=100)
		sayCapForCapitals = boolean(default=false)
		beepForCapitals = boolean(default=false)
		useSpellingFunctionality = boolean(default=true)

# Audio settings
[audio]
	audioDuckingMode = integer(default=0)

# Braille settings
[braille]
	display = string(default=auto)
	translationTable = string(default=en-ueb-g1.ctb)
	inputTable = string(default=en-ueb-g1.ctb)
	expandAtCursor = boolean(default=true)
	showCursor = boolean(default=true)
	cursorBlink = boolean(default=true)
	cursorBlinkRate = integer(default=500,min=200,max=2000)
	cursorShapeFocus = integer(default=192,min=1,max=255)
	cursorShapeReview = integer(default=128,min=1,max=255)
	noMessageTimeout = boolean(default=false)
	messageTimeout = integer(default=4,min=0,max=20)
	tetherTo = string(default="focus")
	autoTether = boolean(default=true)
	readByParagraph = boolean(default=false)
	wordWrap = boolean(default=true)
	focusContextPresentation = option("changedContext", "fill", "scroll", default="changedContext")

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
	autoPositionWindow = boolean(default=True)
	# Values for positioning the window.
	# Defaults are not used.
	# They should not be read if autoPositionWindow is True
	x = integer()
	y = integer()
	displays = string_list()

#Keyboard settings
[keyboard]
	useCapsLockAsNVDAModifierKey = boolean(default=false)
	useNumpadInsertAsNVDAModifierKey = boolean(default=true)
	useExtendedInsertAsNVDAModifierKey = boolean(default=true)
	keyboardLayout = string(default="desktop")
	speakTypedCharacters = boolean(default=true)
	speakTypedWords = boolean(default=false)
	beepForLowercaseWithCapslock = boolean(default=true)
	speakCommandKeys = boolean(default=false)
	speechInterruptForCharacters = boolean(default=true)
	speechInterruptForEnter = boolean(default=true)
	allowSkimReadingInSayAll = boolean(default=False)
	alertForSpellingErrors = boolean(default=True)
	handleInjectedKeys= boolean(default=true)

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
	autoFocusFocusableElements = boolean(default=False)

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
	reportFontAttributes = boolean(default=false)
	reportRevisions = boolean(default=true)
	reportEmphasis = boolean(default=false)
	reportSuperscriptsAndSubscripts = boolean(default=false)
	reportColor = boolean(default=False)
	reportAlignment = boolean(default=false)
	reportLineSpacing = boolean(default=false)
	reportStyle = boolean(default=false)
	reportSpellingErrors = boolean(default=true)
	reportPage = boolean(default=true)
	reportLineNumber = boolean(default=False)
	reportLineIndentation = boolean(default=False)
	reportLineIndentationWithTones = boolean(default=False)
	reportParagraphIndentation = boolean(default=False)
	reportTables = boolean(default=true)
	includeLayoutTables = boolean(default=False)
	reportTableHeaders = boolean(default=True)
	reportTableCellCoords = boolean(default=True)
	reportBorderStyle = boolean(default=False)
	reportBorderColor = boolean(default=False)
	reportLinks = boolean(default=true)
	reportGraphics = boolean(default=True)
	reportComments = boolean(default=true)
	reportLists = boolean(default=true)
	reportHeadings = boolean(default=true)
	reportBlockQuotes = boolean(default=true)
	reportGroupings = boolean(default=true)
	reportLandmarks = boolean(default=true)
	reportArticles = boolean(default=false)
	reportFrames = boolean(default=true)
	reportClickable = boolean(default=true)

[reviewCursor]
	simpleReviewMode = boolean(default=True)
	followFocus = boolean(default=True)
	followCaret = boolean(default=True)
	followMouse = boolean(default=False)

[UIA]
	enabled = boolean(default=true)
	useInMSWordWhenAvailable = boolean(default=false)
	winConsoleImplementation= option("auto", "legacy", "UIA", default="auto")

[terminals]
	speakPasswords = boolean(default=false)
	keyboardSupportInLegacy = boolean(default=True)

[update]
	autoCheck = boolean(default=true)
	startupNotification = boolean(default=true)
	allowUsageStats = boolean(default=false)
	askedAllowUsageStats = boolean(default=false)

[inputComposition]
	autoReportAllCandidates = boolean(default=True)
	announceSelectedCandidate = boolean(default=True)
	alwaysIncludeShortCharacterDescriptionInCandidateName = boolean(default=True)
	reportReadingStringChanges = boolean(default=True)
	reportCompositionStringChanges = boolean(default=True)

[debugLog]
	hwIo = boolean(default=false)
	UIA = boolean(default=false)
	audioDucking = boolean(default=false)
	gui = boolean(default=false)
	louis = boolean(default=false)
	timeSinceInput = boolean(default=false)
	vision = boolean(default=false)
	speech = boolean(default=false)
	speechManager = boolean(default=false)

[uwpOcr]
	language = string(default="")

[upgrade]
	newLaptopKeyboardLayout = boolean(default=false)

[editableText]
	caretMoveTimeoutMs = integer(min=0, max=2000, default=100)

[development]
	enableScratchpadDir = boolean(default=false)

[featureFlag]
	# 0:default, 1:yes, 2:no
	cancelExpiredFocusSpeech = integer(0, 2, default=0)
"""

#: The configuration specification
#: @type: ConfigObj
confspec = ConfigObj(StringIO( configSpecString ), list_values=False, encoding="UTF-8")
confspec.newlines = "\r\n"
