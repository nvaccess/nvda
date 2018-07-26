# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Babbage B.V., Davy Kager
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from cStringIO import StringIO
from configobj import ConfigObj

#: The version of the schema outlined in this file. Increment this when modifying the schema and 
#: provide an upgrade step (@see profileUpgradeSteps.py). An upgrade step does not need to be added when
#: just adding a new element to (or removing from) the schema, only when old versions of the config 
#: (conforming to old schema versions) will not work correctly with the new schema.
latestSchemaVersion = 2

#: The configuration specification string
#: @type: String
configSpecString = ("""# NVDA Configuration File
schemaVersion = integer(min=0, default={latestSchemaVersion})
[general]
	language = string(default="Windows")
	saveConfigurationOnExit = boolean(default=True)
	askToExit = boolean(default=True)
	playStartAndExitSounds = boolean(default=True)
	loggingLevel = option("DEBUG", "IO", "DEBUGWARNING", "INFO", "OFF", default="INFO")
	showWelcomeDialogAtStartup = boolean(default=True)

# Speech settings
[speech]
	# The synthesiser to use
	synth = string(default=auto)
	symbolLevel = integer(min=0, max=300, default=100)
	trustVoiceLanguage = boolean(default=True)
	includeCLDR = boolean(default=True)
	beepSpeechModePitch = integer(min=50, max=11025, default=10000)
	outputDevice = string(default=default)
	autoLanguageSwitching = boolean(default=True)
	autoDialectSwitching = boolean(default=False)

	[[__many__]]
		capPitchChange = integer(min=-100, max=100, default=30)
		sayCapForCapitals = boolean(default=False)
		beepForCapitals = boolean(default=False)
		useSpellingFunctionality = boolean(default=True)

# Audio settings
[audio]
	audioDuckingMode = integer(min=0, max=2, default=0)

# Braille settings
[braille]
	display = string(default=auto)
	translationTable = string(default=en-ueb-g1.ctb)
	inputTable = string(default=en-ueb-g1.ctb)
	expandAtCursor = boolean(default=True)
	showCursor = boolean(default=True)
	cursorBlink = boolean(default=True)
	cursorBlinkRate = integer(min=200, max=2000, default=500)
	cursorShapeFocus = integer(min=1, max=255, default=192)
	cursorShapeReview = integer(min=1, max=255, default=128)
	noMessageTimeout = boolean(default=False)
	messageTimeout = integer(min=0, max=20, default=4)
	tetherTo = option("focus", "review", default="focus")
	autoTether = boolean(default=True)
	readByParagraph = boolean(default=False)
	wordWrap = boolean(default=True)
	focusContextPresentation = option("changedContext", "fill", "scroll", default="changedContext")

	# Braille display driver settings
	[[__many__]]
		port = string(default="")

# Presentation settings
[presentation]
		reportKeyboardShortcuts = boolean(default=True)
		reportObjectPositionInformation = boolean(default=True)
		guessObjectPositionInformationWhenUnavailable = boolean(default=False)
		reportTooltips = boolean(default=False)
		reportHelpBalloons = boolean(default=True)
		reportObjectDescriptions = boolean(default=True)
		reportDynamicContentChanges = boolean(default=True)
		reportAutoSuggestionsWithSound = boolean(default=True)

	[[progressBarUpdates]]
		reportBackgroundProgressBars = boolean(default=False)
		progressBarOutputMode = option("beep", "speak", "both", "off", default="beep")
		speechPercentageInterval = integer(default=10)
		beepPercentageInterval = integer(default=1)
		beepMinHZ = integer(default=110)

[mouse]
	enableMouseTracking = boolean(default=True) #must be true for any of the other settings to work
	mouseTextUnit = option("character", "word", "line", "paragraph", default="paragraph")
	reportObjectRoleOnMouseEnter = boolean(default=False)
	audioCoordinatesOnMouseMove = boolean(default=False)
	audioCoordinates_detectBrightness = boolean(default=False)
	audioCoordinates_blurFactor = integer(default=3)
	audioCoordinates_minVolume = float(default=0.1)
	audioCoordinates_maxVolume = float(default=1.0)
	audioCoordinates_minPitch = integer(default=220)
	audioCoordinates_maxPitch = integer(default=880)
	reportMouseShapeChanges = boolean(default=False)
	ignoreInjectedMouseInput = boolean(default=False)

[speechViewer]
	showSpeechViewerAtStartup = boolean(default=False)
	autoPositionWindow = boolean(default=True)
	# values for positioning the window. Defaults are not used. They should not be read if autoPositionWindow is True
	x = integer()
	y = integer()
	width = integer()
	height = integer()
	displays = string_list()

#Keyboard settings
[keyboard]
	useCapsLockAsNVDAModifierKey = boolean(default=False)
	useNumpadInsertAsNVDAModifierKey = boolean(default=True)
	useExtendedInsertAsNVDAModifierKey = boolean(default=True)
	keyboardLayout = option("desktop", "laptop", default="desktop")
	speakTypedCharacters = boolean(default=True)
	speakTypedWords = boolean(default=False)
	beepForLowercaseWithCapslock = boolean(default=True)
	speakCommandKeys = boolean(default=False)
	speechInterruptForCharacters = boolean(default=True)
	speechInterruptForEnter = boolean(default=True)
	allowSkimReadingInSayAll = boolean(default=False)
	alertForSpellingErrors = boolean(default=True)
	handleInjectedKeys= boolean(default=True)

[virtualBuffers]
	maxLineLength = integer(min=10, max=250, default=100)
	linesPerPage = integer(min=5, max=150, default=25)
	useScreenLayout = boolean(default=True)
	autoPassThroughOnFocusChange = boolean(default=True)
	autoPassThroughOnCaretMove = boolean(default=False)
	passThroughAudioIndication = boolean(default=True)
	autoSayAllOnPageLoad = boolean(default=True)
	trapNonCommandGestures = boolean(default=True)
	focusFollowsBrowse = boolean(default=True)

[touch]
	touchTyping = boolean(default=False)

#Settings for document reading (such as MS Word and wordpad)
[documentFormatting]
	#These settings affect what information is reported when you navigate to text where the formatting  or placement has changed
	detectFormatAfterCursor = boolean(default=False)
	reportFontName = boolean(default=False)
	reportFontSize = boolean(default=False)
	reportFontAttributes = boolean(default=False)
	reportRevisions = boolean(default=True)
	reportEmphasis = boolean(default=False)
	reportColor = boolean(default=False)
	reportAlignment = boolean(default=False)
	reportLineSpacing = boolean(default=False)
	reportStyle = boolean(default=False)
	reportSpellingErrors = boolean(default=True)
	reportPage = boolean(default=True)
	reportLineNumber = boolean(default=False)
	reportLineIndentation = boolean(default=False)
	reportLineIndentationWithTones = boolean(default=False)
	reportParagraphIndentation = boolean(default=False)
	reportTables = boolean(default=True)
	includeLayoutTables = boolean(default=False)
	reportTableHeaders = boolean(default=True)
	reportTableCellCoords = boolean(default=True)
	reportBorderStyle = boolean(default=False)
	reportBorderColor = boolean(default=False)
	reportLinks = boolean(default=True)
	reportComments = boolean(default=True)
	reportLists = boolean(default=True)
	reportHeadings = boolean(default=True)
	reportBlockQuotes = boolean(default=True)
	reportLandmarks = boolean(default=True)
	reportFrames = boolean(default=True)
	reportClickable = boolean(default=True)

[reviewCursor]
	simpleReviewMode = boolean(default=True)
	followFocus = boolean(default=True)
	followCaret = boolean(default=True)
	followMouse = boolean(default=False)

[UIA]
	enabled = boolean(default=True)
	useInMSWordWhenAvailable = boolean(default=False)

[update]
	autoCheck = boolean(default=True)
	startupNotification = boolean(default=True)
	allowUsageStats = boolean(default=False)
	askedAllowUsageStats = boolean(default=False)

[inputComposition]
	autoReportAllCandidates = boolean(default=True)
	announceSelectedCandidate = boolean(default=True)
	alwaysIncludeShortCharacterDescriptionInCandidateName = boolean(default=True)
	reportReadingStringChanges = boolean(default=True)
	reportCompositionStringChanges = boolean(default=True)

[debugLog]
	hwIo = boolean(default=False)
	audioDucking = boolean(default=False)
	gui = boolean(default=False)
	louis = boolean(default=False)
	timeSinceInput = boolean(default=False)

[uwpOcr]
	language = string(default="")

[upgrade]
	newLaptopKeyboardLayout = boolean(default=False)

[editableText]
	caretMoveTimeoutMs = integer(min=0, max=2000, default=100)

[development]
	enableScratchpadDir = boolean(default=False)
""").format(latestSchemaVersion=latestSchemaVersion)

#: The configuration specification
#: @type: ConfigObj
confspec = ConfigObj(StringIO( configSpecString ), list_values=False, encoding="UTF-8")
confspec.newlines = "\r\n"
