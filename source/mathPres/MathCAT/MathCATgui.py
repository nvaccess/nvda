import wx

# import wx.xrc
import gettext
import addonHandler

_ = gettext.gettext
addonHandler.initTranslation()

###########################################################################
# Class MathCATPreferencesDialog
###########################################################################


class MathCATPreferencesDialog(wx.Dialog):
	"""Main dialog window for configuring MathCAT preferences.

	This base class sets up the layout and controls.
	"""

	def __init__(self, parent: wx.Window | None):
		"""Initialize the preferences dialog.

		:param parent: The parent window for this dialog.
		"""
		wx.Dialog.__init__(
			self,
			parent,
			id=wx.ID_ANY,
			# Translators: title for MathCAT preferences dialog
			title=_("MathCAT Preferences"),
			pos=wx.DefaultPosition,
			size=wx.Size(-1, -1),
			style=wx.DEFAULT_DIALOG_STYLE,
		)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		gbSizerMathCATPreferences: wx.GridBagSizer = wx.GridBagSizer(0, 0)
		gbSizerMathCATPreferences.SetFlexibleDirection(wx.BOTH)
		gbSizerMathCATPreferences.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

		self._panelCategories: wx.Panel = wx.Panel(
			self,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			wx.TAB_TRAVERSAL,
		)
		bSizerCategories: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

		self._staticTextCategories: wx.StaticText = wx.StaticText(
			self._panelCategories,
			wx.ID_ANY,
			# Translators: A heading that labels three navigation pane tab names in the MathCAT dialog
			_("Categories:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextCategories.Wrap(-1)

		bSizerCategories.Add(self._staticTextCategories, 0, wx.ALL, 5)

		listBoxPreferencesTopicChoices: list[str] = [
			# Translators: these are navigation pane headings for the MathCAT preferences dialog under the title "Categories"
			_("Speech"),
			# Translators: these are navigation pane headings for the MathCAT preferences dialog under the title "Categories"
			_("Navigation"),
			# Translators: these are navigation pane headings for the MathCAT preferences dialog under the title "Categories"
			_("Braille"),
		]
		self._listBoxPreferencesTopic: wx.ListBox = wx.ListBox(
			self._panelCategories,
			wx.ID_ANY,
			wx.Point(-1, -1),
			wx.Size(-1, -1),
			listBoxPreferencesTopicChoices,
			wx.LB_NO_SB | wx.LB_SINGLE,
		)
		bSizerCategories.Add(self._listBoxPreferencesTopic, 0, wx.ALL, 5)

		bSizerCategories.Add((0, 0), 1, wx.EXPAND, 5)

		self._bitmapLogo: wx.StaticBitmap = wx.StaticBitmap(
			self._panelCategories,
			wx.ID_ANY,
			wx.NullBitmap,
			wx.DefaultPosition,
			wx.Size(126, 85),
			0,
		)
		bSizerCategories.Add(self._bitmapLogo, 0, wx.ALL, 5)

		self._panelCategories.SetSizer(bSizerCategories)
		self._panelCategories.Layout()
		bSizerCategories.Fit(self._panelCategories)
		gbSizerMathCATPreferences.Add(
			self._panelCategories,
			wx.GBPosition(0, 0),
			wx.GBSpan(1, 1),
			wx.EXPAND | wx.ALL,
			5,
		)

		self._simplebookPanelsCategories: wx.Simplebook = wx.Simplebook(
			self,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._panelSpeech: wx.Panel = wx.Panel(
			self._simplebookPanelsCategories,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL,
		)
		bSizerSpeech: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

		bSizerImpairment: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextImpairment: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: this is the text label for whom to target the speech for (options are below)
			_("Generate speech for:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextImpairment.Wrap(-1)

		bSizerImpairment.Add(self._staticTextImpairment, 0, wx.ALL, 5)

		impairmentChoices: list[str] = [
			# Translators: these are the categories of impairments that MathCAT supports
			# Translators: Learning disabilities includes dyslexia and ADHD
			_("Learning disabilities"),
			# Translators: target people who are blind
			_("Blindness"),
			# Translators: target people who have low vision
			_("Low vision"),
		]
		self._choiceImpairment: wx.Choice = wx.Choice(
			self._panelSpeech,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			impairmentChoices,
			0,
		)
		self._choiceImpairment.SetSelection(1)
		bSizerImpairment.Add(self._choiceImpairment, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerImpairment, 1, wx.EXPAND, 5)

		bSizerLanguage: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextLanguage: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for pull down allowing users to choose the speech language for math
			_("Language:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextLanguage.Wrap(-1)

		bSizerLanguage.Add(self._staticTextLanguage, 0, wx.ALL, 5)

		languageChoices: list[str] = ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
		self._choiceLanguage: wx.Choice = wx.Choice(
			self._panelSpeech,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			languageChoices,
			0,
		)
		self._choiceLanguage.SetSelection(0)
		bSizerLanguage.Add(self._choiceLanguage, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerLanguage, 1, wx.EXPAND, 5)

		bSizerDecimalSeparator: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextDecimalSeparator: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for pull down to specify what character to use in numbers as the decimal separator
			_("Decimal separator for numbers:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextDecimalSeparator.Wrap(-1)

		bSizerDecimalSeparator.Add(self._staticTextDecimalSeparator, 0, wx.ALL, 5)

		# Translators: options for decimal separator.
		decimalSeparatorChoices: list[str] = [
			# Translators: options for decimal separator -- "Auto" = automatically pick the choice based on the language
			_("Auto"),
			# options for decimal separator -- use "."  (and use ", " for block separators)
			("."),
			# options for decimal separator -- use ","  (and use ". " for block separators)
			(","),
			# Translators: options for decimal separator -- "Custom" = user sets it
			#   Currently there is no UI for how it is done yet, but eventually there will be a dialog that pops up to set it
			_("Custom"),
		]
		self._choiceDecimalSeparator: wx.Choice = wx.Choice(
			self._panelSpeech,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			decimalSeparatorChoices,
			0,
		)
		self._choiceDecimalSeparator.SetSelection(0)
		bSizerDecimalSeparator.Add(self._choiceDecimalSeparator, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerDecimalSeparator, 1, wx.EXPAND, 5)

		bSizerSpeechStyle: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextSpeechStyle: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for pull down allowing users to choose the "style" (version, rules) of speech for math
			_("Speech style:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextSpeechStyle.Wrap(-1)

		bSizerSpeechStyle.Add(self._staticTextSpeechStyle, 0, wx.ALL, 5)

		speechStyleChoices: list[str] = ["xxxxxxxxxxxxxxxx"]
		self._choiceSpeechStyle: wx.Choice = wx.Choice(
			self._panelSpeech,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			speechStyleChoices,
			0,
		)
		self._choiceSpeechStyle.SetSelection(0)
		bSizerSpeechStyle.Add(self._choiceSpeechStyle, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerSpeechStyle, 1, wx.EXPAND, 5)

		bSizerSpeechAmount: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextSpeechAmount: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for pull down to specify how verbose/terse the speech should be
			_("Speech verbosity:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextSpeechAmount.Wrap(-1)

		bSizerSpeechAmount.Add(self._staticTextSpeechAmount, 0, wx.ALL, 5)

		# Translators: options for speech verbosity.
		speechAmountChoices: list[str] = [
			# Translators: options for speech verbosity -- "terse" = use less words
			_("Terse"),
			# Translators: options for speech verbosity -- "medium" = try to be nether too terse nor too verbose words
			_("Medium"),
			# Translators: options for speech verbosity -- "verbose" = use more words
			_("Verbose"),
		]
		self._choiceSpeechAmount: wx.Choice = wx.Choice(
			self._panelSpeech,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			speechAmountChoices,
			0,
		)
		self._choiceSpeechAmount.SetSelection(0)
		bSizerSpeechAmount.Add(self._choiceSpeechAmount, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerSpeechAmount, 1, wx.EXPAND, 5)

		bSizerRelativeSpeed: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextRelativeSpeed: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for slider that specifies a percentage of the normal speech rate that should be used for math
			_("Relative speech rate:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextRelativeSpeed.Wrap(-1)

		bSizerRelativeSpeed.Add(self._staticTextRelativeSpeed, 0, wx.ALL, 5)

		self._sliderRelativeSpeed: wx.Slider = wx.Slider(
			self._panelSpeech,
			wx.ID_ANY,
			100,
			10,
			100,
			wx.DefaultPosition,
			wx.DefaultSize,
			wx.SL_HORIZONTAL,
		)
		self._sliderRelativeSpeed.SetLineSize(9)
		bSizerRelativeSpeed.Add(self._sliderRelativeSpeed, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerRelativeSpeed, 1, wx.EXPAND, 5)

		bSizerPauseFactor: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticPauseFactor: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for slider that specifies relative factor to increase or decrease pauses in the math speech
			_("Pause factor:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticPauseFactor.Wrap(-1)

		bSizerPauseFactor.Add(self._staticPauseFactor, 0, wx.ALL, 5)

		self._sliderPauseFactor: wx.Slider = wx.Slider(
			self._panelSpeech,
			wx.ID_ANY,
			7,
			0,
			14,
			wx.DefaultPosition,
			wx.DefaultSize,
			wx.SL_HORIZONTAL,
		)
		bSizerPauseFactor.Add(self._sliderPauseFactor, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerPauseFactor, 1, wx.EXPAND, 5)

		bSizerSpeechSound: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._checkBoxSpeechSound: wx.CheckBox = wx.CheckBox(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for check box controling a beep sound
			_("Make a sound when starting/ending math speech"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		bSizerSpeechSound.Add(self._checkBoxSpeechSound, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerSpeechSound, 1, wx.EXPAND, 5)

		bSizerSubjectArea: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextSubjectArea: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for pull down to specify a subject area (Geometry, Calculus, ...)
			_("Subject area to be used when it cannot be determined automatically:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextSubjectArea.Wrap(-1)

		bSizerSubjectArea.Add(self._staticTextSubjectArea, 0, wx.ALL, 5)

		# Translators: a generic (non-specific) math subject area
		subjectAreaChoices: list[str] = [_("General")]
		self._choiceSubjectArea: wx.Choice = wx.Choice(
			self._panelSpeech,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			subjectAreaChoices,
			0,
		)
		self._choiceSubjectArea.SetSelection(0)
		bSizerSubjectArea.Add(self._choiceSubjectArea, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerSubjectArea, 1, wx.EXPAND, 5)

		bSizerSpeechForChemical: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextSpeechForChemical: wx.StaticText = wx.StaticText(
			self._panelSpeech,
			wx.ID_ANY,
			# Translators: label for pull down to specify how verbose/terse the speech should be
			_("Speech for chemical formulas:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextSpeechForChemical.Wrap(-1)

		bSizerSpeechForChemical.Add(self._staticTextSpeechForChemical, 0, wx.ALL, 5)

		speechForChemicalChoices: list[str] = [
			# Translators: values for chemistry options with example speech in parenthesis
			_("Spell it out (H 2 O)"),
			# Translators: values for chemistry options with example speech in parenthesis (never interpret as chemistry)
			_("Off (H sub 2 O)"),
		]
		self._choiceSpeechForChemical = wx.Choice(
			self._panelSpeech,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			speechForChemicalChoices,
			0,
		)
		self._choiceSpeechForChemical.SetSelection(0)
		bSizerSpeechForChemical.Add(self._choiceSpeechForChemical, 0, wx.ALL, 5)

		bSizerSpeech.Add(bSizerSpeechForChemical, 1, wx.EXPAND, 5)

		self._panelSpeech.SetSizer(bSizerSpeech)
		self._panelSpeech.Layout()
		bSizerSpeech.Fit(self._panelSpeech)
		self._simplebookPanelsCategories.AddPage(self._panelSpeech, "a page", False)
		self._panelNavigation: wx.Panel = wx.Panel(
			self._simplebookPanelsCategories,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL,
		)
		bSizerNavigation: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

		sbSizerNavigationMode: wx.StaticBoxSizer = wx.StaticBoxSizer(
			wx.StaticBox(
				self._panelNavigation,
				wx.ID_ANY,
				# Translators: label for pull down to specify one of three modes use to navigate math expressions
				_("Navigation mode to use when beginning to navigate an equation:"),
			),
			wx.VERTICAL,
		)

		navigationModeChoices: list[str] = [
			# Translators: names of different modes of navigation. "Enhanced" mode understands math structure
			_("Enhanced"),
			# Translators: "Simple" walks by character expect for things like fractions, roots, and scripts
			_("Simple"),
			# Translators: "Character" moves around by character, automatically moving into fractions, etc
			_("Character"),
		]
		self._choiceNavigationMode: wx.Choice = wx.Choice(
			sbSizerNavigationMode.GetStaticBox(),
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			navigationModeChoices,
			0,
		)
		self._choiceNavigationMode.SetSelection(1)
		sbSizerNavigationMode.Add(self._choiceNavigationMode, 0, wx.ALL, 5)

		self._checkBoxResetNavigationMode: wx.CheckBox = wx.CheckBox(
			sbSizerNavigationMode.GetStaticBox(),
			wx.ID_ANY,
			# Translators: label for checkbox that controls whether any changes to the navigation mode should be preserved
			_("Reset navigation mode on entry to an expression"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		sbSizerNavigationMode.Add(self._checkBoxResetNavigationMode, 0, wx.ALL, 5)

		bSizerNavigation.Add(sbSizerNavigationMode, 1, wx.EXPAND, 5)

		sbSizerNavigationSpeech: wx.StaticBoxSizer = wx.StaticBoxSizer(
			wx.StaticBox(
				self._panelNavigation,
				wx.ID_ANY,
				# Translators: label for pull down to specify whether the expression is spoken or described (an overview)
				_("Navigation speech to use when beginning to navigate an equation:"),
			),
			wx.VERTICAL,
		)

		# Translators: either "Speak" the expression or give a description (overview) of the expression
		navigationSpeechChoices: list[str] = [
			# Translators: "Speak" the expression after moving to it
			_("Speak"),
			# Translators: "Describe" the expression after moving to it ("overview is a synonym")
			_("Describe/overview"),
		]
		self._choiceNavigationSpeech: wx.Choice = wx.Choice(
			sbSizerNavigationSpeech.GetStaticBox(),
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			navigationSpeechChoices,
			0,
		)
		self._choiceNavigationSpeech.SetSelection(1)
		sbSizerNavigationSpeech.Add(self._choiceNavigationSpeech, 0, wx.ALL, 5)

		self._checkBoxResetNavigationSpeech: wx.CheckBox = wx.CheckBox(
			sbSizerNavigationSpeech.GetStaticBox(),
			wx.ID_ANY,
			# Translators: label for checkbox that controls whether any changes to the speak vs overview reading should be ignored
			_("Reset navigation speech on entry to an expression"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._checkBoxResetNavigationSpeech.SetValue(True)
		sbSizerNavigationSpeech.Add(self._checkBoxResetNavigationSpeech, 0, wx.ALL, 5)

		bSizerNavigation.Add(sbSizerNavigationSpeech, 1, wx.EXPAND, 5)

		bSizerNavigationZoom: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

		self._checkBoxAutomaticZoom: wx.CheckBox = wx.CheckBox(
			self._panelNavigation,
			wx.ID_ANY,
			# Translators: label for checkbox that controls whether arrow keys move out of fractions, etc.,
			# or whether you have to manually back out of the fraction, etc.
			_("Automatic zoom out of 2D notations"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		bSizerNavigationZoom.Add(self._checkBoxAutomaticZoom, 0, wx.ALL, 5)

		bSizerSpeechAmountNavigation: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextSpeechAmountNavigation: wx.StaticText = wx.StaticText(
			self._panelNavigation,
			wx.ID_ANY,
			# Translators: label for pull down to specify whether you want a terse or verbose reading of navigation commands
			_("Speech amount for navigation:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextSpeechAmountNavigation.Wrap(-1)

		bSizerSpeechAmountNavigation.Add(self._staticTextSpeechAmountNavigation, 0, wx.ALL, 5)

		# Translators: options for navigation verbosity.
		speechAmountNavigationChoices: list[str] = [
			# Translators: options for navigation verbosity -- "terse" = use less words
			_("Terse"),
			# Translators: options for navigation verbosity -- "medium" = try to be nether too terse nor too verbose words
			_("Medium"),
			# Translators: options for navigation verbosity -- "verbose" = use more words
			_("Verbose"),
		]
		self._choiceSpeechAmountNavigation: wx.Choice = wx.Choice(
			self._panelNavigation,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			speechAmountNavigationChoices,
			0,
		)
		self._choiceSpeechAmountNavigation.SetSelection(0)
		bSizerSpeechAmountNavigation.Add(self._choiceSpeechAmountNavigation, 0, wx.ALL, 5)

		bSizerNavigationZoom.Add(bSizerSpeechAmountNavigation, 1, wx.EXPAND, 5)

		bSizerNavigation.Add(bSizerNavigationZoom, 1, wx.EXPAND, 5)

		bSizerCopyAs: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextCopyMathAs: wx.StaticText = wx.StaticText(
			self._panelNavigation,
			wx.ID_ANY,
			# Translators: label for pull down to specify how math will be copied to the clipboard
			_("Copy math as:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextCopyMathAs.Wrap(-1)

		bSizerCopyAs.Add(self._staticTextCopyMathAs, 0, wx.ALL, 5)

		# Translators: options for copy math as.
		copyAsChoices: list[str] = [
			# Translators: options for Copy expression to clipboard as -- "MathML"
			_("MathML"),
			# Translators: options for Copy expression to clipboard as -- "LaTeX"
			_("LaTeX"),
			# Translators: options for Copy expression to clipboard as -- "ASCIIMath"
			_("ASCIIMath"),
			# Translators: options for Copy expression to clipboard as -- speech text
			_("Speech"),
		]
		self._choiceCopyAs: wx.Choice = wx.Choice(
			self._panelNavigation,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			copyAsChoices,
			0,
		)
		self._choiceCopyAs.SetSelection(0)
		bSizerCopyAs.Add(self._choiceCopyAs, 0, wx.ALL, 5)

		bSizerNavigation.Add(bSizerCopyAs, 1, wx.EXPAND, 5)

		self._panelNavigation.SetSizer(bSizerNavigation)
		self._panelNavigation.Layout()
		bSizerNavigation.Fit(self._panelNavigation)
		self._simplebookPanelsCategories.AddPage(
			self._panelNavigation,
			"a page",
			False,
		)
		self._panelBraille: wx.Panel = wx.Panel(
			self._simplebookPanelsCategories,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL,
		)
		bSizerBraille = wx.BoxSizer(wx.VERTICAL)

		bSizerBrailleMathCode: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextBrailleMathCode: wx.StaticText = wx.StaticText(
			self._panelBraille,
			wx.ID_ANY,
			# Translators: label for pull down to specify which braille code to use
			_("Braille math code for refreshable displays:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextBrailleMathCode.Wrap(-1)

		bSizerBrailleMathCode.Add(self._staticTextBrailleMathCode, 0, wx.ALL, 5)
		brailleMathCodeChoices: list[str] = ["xxxxxxxxxxx"]
		self._choiceBrailleMathCode: wx.Choice = wx.Choice(
			self._panelBraille,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			brailleMathCodeChoices,
			0,
		)
		self._choiceBrailleMathCode.SetSelection(1)
		bSizerBrailleMathCode.Add(self._choiceBrailleMathCode, 0, wx.ALL, 5)

		bSizerBraille.Add(bSizerBrailleMathCode, 1, wx.EXPAND, 5)

		bSizerBrailleHighlights = wx.BoxSizer(wx.HORIZONTAL)

		self._staticTextBrailleHighlights: wx.StaticText = wx.StaticText(
			self._panelBraille,
			wx.ID_ANY,
			# Translators: label for pull down to specify how braille dots should be modified when navigating/selecting subexprs
			_("Highlight with dots 7 && 8 the current nav node:"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		self._staticTextBrailleHighlights.Wrap(-1)

		bSizerBrailleHighlights.Add(self._staticTextBrailleHighlights, 0, wx.ALL, 5)

		brailleHighlightsChoices: list[str] = [
			# Translators: options for using dots 7 and 8:
			# Translators: "off" -- don't highlight
			_("Off"),
			# Translators: "First character" -- only the first character of the current navigation node uses dots 7 & 8
			_("First character"),
			# Translators: "Endpoints" -- only the first and last character of the current navigation node uses dots 7 & 8
			_("Endpoints"),
			# Translators: "All" -- all the characters for the current navigation node use dots 7 & 8
			_("All"),
		]
		self._choiceBrailleHighlights: wx.Choice = wx.Choice(
			self._panelBraille,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			brailleHighlightsChoices,
			0,
		)
		self._choiceBrailleHighlights.SetSelection(1)
		bSizerBrailleHighlights.Add(self._choiceBrailleHighlights, 0, wx.ALL, 5)

		bSizerBraille.Add(bSizerBrailleHighlights, 1, wx.EXPAND, 5)

		bSizerBraille.Add((0, 0), 1, wx.EXPAND, 5)

		bSizerBraille.Add((0, 0), 1, wx.EXPAND, 5)

		bSizerBraille.Add((0, 0), 1, wx.EXPAND, 5)

		bSizerBraille.Add((0, 0), 1, wx.EXPAND, 5)

		bSizerBraille.Add((0, 0), 1, wx.EXPAND, 5)

		self._panelBraille.SetSizer(bSizerBraille)
		self._panelBraille.Layout()
		bSizerBraille.Fit(self._panelBraille)
		self._simplebookPanelsCategories.AddPage(self._panelBraille, "a page", False)

		gbSizerMathCATPreferences.Add(
			self._simplebookPanelsCategories,
			wx.GBPosition(0, 1),
			wx.GBSpan(1, 1),
			wx.EXPAND | wx.ALL,
			10,
		)

		self._staticlineAboveButtons: wx.StaticLine = wx.StaticLine(
			self,
			wx.ID_ANY,
			wx.DefaultPosition,
			wx.DefaultSize,
			wx.LI_HORIZONTAL,
		)
		gbSizerMathCATPreferences.Add(
			self._staticlineAboveButtons,
			wx.GBPosition(1, 0),
			wx.GBSpan(1, 2),
			wx.EXPAND | wx.ALL,
			5,
		)

		self._panelButtons: wx.Panel = wx.Panel(self, wx.ID_ANY, wx.Point(-1, -1), wx.DefaultSize, 0)
		bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

		bSizerButtons.Add((0, 0), 1, wx.EXPAND, 5)

		self._buttonOK: wx.Button = wx.Button(
			self._panelButtons,
			wx.ID_ANY,
			# Translators: dialog "ok" button
			_("OK"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		bSizerButtons.Add(self._buttonOK, 0, wx.ALL, 5)

		self._buttonCancel: wx.Button = wx.Button(
			self._panelButtons,
			wx.ID_ANY,
			# Translators: dialog "cancel" button
			_("Cancel"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		bSizerButtons.Add(self._buttonCancel, 0, wx.ALL, 5)

		self._buttonApply: wx.Button = wx.Button(
			self._panelButtons,
			wx.ID_ANY,
			# Translators: dialog "apply" button
			_("Apply"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		bSizerButtons.Add(self._buttonApply, 0, wx.ALL, 5)

		self._buttonReset: wx.Button = wx.Button(
			self._panelButtons,
			wx.ID_ANY,
			# Translators: button to reset all the preferences to their default values
			_("Reset to defaults"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		bSizerButtons.Add(self._buttonReset, 0, wx.ALL, 5)

		self._buttonHelp: wx.Button = wx.Button(
			self._panelButtons,
			wx.ID_ANY,
			# Translators: button to bring up a help page
			_("Help"),
			wx.DefaultPosition,
			wx.DefaultSize,
			0,
		)
		bSizerButtons.Add(self._buttonHelp, 0, wx.ALL, 5)

		self._panelButtons.SetSizer(bSizerButtons)
		self._panelButtons.Layout()
		bSizerButtons.Fit(self._panelButtons)
		gbSizerMathCATPreferences.Add(
			self._panelButtons,
			wx.GBPosition(2, 1),
			wx.GBSpan(1, 2),
			wx.EXPAND | wx.ALL,
			5,
		)

		self.SetSizer(gbSizerMathCATPreferences)
		self.Layout()
		gbSizerMathCATPreferences.Fit(self)

		self.Centre(wx.BOTH)

		# Connect Events
		self.Bind(wx.EVT_CHAR_HOOK, self.mathCATPreferencesDialogOnCharHook)
		self.Bind(wx.EVT_KEY_UP, self.mathCATPreferencesDialogOnKeyUp)
		self._listBoxPreferencesTopic.Bind(wx.EVT_LISTBOX, self.onListBoxCategories)
		self._choiceLanguage.Bind(wx.EVT_CHOICE, self.onLanguage)
		self._sliderRelativeSpeed.Bind(
			wx.EVT_SCROLL_CHANGED,
			self.onRelativeSpeedChanged,
		)
		self._sliderPauseFactor.Bind(wx.EVT_SCROLL_CHANGED, self.onPauseFactorChanged)
		self._buttonOK.Bind(wx.EVT_BUTTON, self.onClickOK)
		self._buttonCancel.Bind(wx.EVT_BUTTON, self.onClickCancel)
		self._buttonApply.Bind(wx.EVT_BUTTON, self.onClickApply)
		self._buttonReset.Bind(wx.EVT_BUTTON, self.onClickReset)
		self._buttonHelp.Bind(wx.EVT_BUTTON, self.onClickHelp)

	def __del__(self):
		"""Destructor placeholder; override if cleanup is needed."""
		pass

	# Virtual event handlers, override them in your derived class
	def mathCATPreferencesDialogOnCharHook(self, event: wx.KeyEvent) -> None:
		"""Handle character input events; override in subclass as needed."""
		event.Skip()

	def mathCATPreferencesDialogOnKeyUp(self, event: wx.KeyEvent) -> None:
		"""Handle key release events; override in subclass as needed."""
		event.Skip()

	def onListBoxCategories(self, event: wx.CommandEvent) -> None:
		"""Handle selection events in the categories list box; override in subclass as needed."""
		event.Skip()

	def onLanguage(self, event: wx.CommandEvent) -> None:
		"""Handle language selection; override in subclass as needed."""
		event.Skip()

	def onRelativeSpeedChanged(self, event: wx.ScrollEvent) -> None:
		"""Handle change in relative speed; override in subclass as needed."""
		event.Skip()

	def onPauseFactorChanged(self, event: wx.ScrollEvent) -> None:
		"""Handle change in pause factor; override in subclass as needed."""
		event.Skip()

	def onClickOK(self, event: wx.CommandEvent) -> None:
		"""Handle OK button click; override in subclass as needed."""
		event.Skip()

	def onClickCancel(self, event: wx.CommandEvent) -> None:
		"""Handle Cancel button click; override in subclass as needed."""
		event.Skip()

	def onClickApply(self, event: wx.CommandEvent) -> None:
		"""Handle Apply button click; override in subclass as needed."""
		event.Skip()

	def onClickReset(self, event: wx.CommandEvent) -> None:
		"""Handle Reset button click; override in subclass as needed."""
		event.Skip()

	def onClickHelp(self, event: wx.CommandEvent) -> None:
		"""Handle Help button click; override in subclass as needed."""
		event.Skip()
