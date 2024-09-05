# Feature Flags

NVDA makes judicious use of feature flags to enable and disable features that are in early development.
The following are provided to streamline the creation of new feature flags:
- A config spec type
- A GUI control type

## Background
When providing a feature flag it is important to understand the importance of providing a "default" state.
A boolean feature, must have 3 states selectable by the user:
- `True`
- `False`
- `Default` (NVDA developer recommendation)

This allows a choice between the following use-cases to be made at any point in time:
- **Explicitly opt-in** to the feature, regardless of the default behavior.
An early adopter may choose to do this to test the feature and provide feedback.
- **Explicitly opt-out** of the feature, regardless of the default behavior.
A user may find the pre-existing behavior acceptable, and wants the maximum delay to adopt the new feature.
They may be prioritising stability, or anticipating this feature flag receives a permanent home in NVDA settings.
- **Explicitly choose the default** (NVDA developer recommended) behavior.
Noting, that in this case it is important that the user must be able to select one of the other options first,
and return to the default behavior at any point in time.

This should be possible while still allowing developers to change the behaviour
of the default option.
The development process might require that initially NVDA is released with
the feature disabled by default.
In this case only testers, or the most curious users are expected to opt-in temporarily.
As the feature improves, bugs are fixed, edge cases are handled, and the UX is improved,
developers may wish to change the behavior of the default option to enable the feature.
This change shouldn't affect those who have already explicitly opted out of the feature.
Only those who maybe haven't tried the feature, because they were using the prior default behaviour, or
those who have tried and found the feature to be unstable and decided they would wait for it to become
stable.

## Feature Flag Enum
To aid static typing in NVDA, `enum` classes are used.
`BoolFlag` is provided, the majority of feature flags are expected to use this.
However, if more values are required (E.G. `AllowUiaInMSWord` has options `WHEN_NECESSARY`, `WHERE_SUITABLE`, `ALWAYS`, in addition to `DEFAULT`), then a new `enum` class can be defined.
Adding the enum class to the `featureFlagEnums.py` file will automatically expose it for use in the config spec (see the next section).
Example new `enum` class:

```python

class AllowUiaInMSWordFlag(DisplayStringEnum):
	"""Feature flag for UIA in MS Word.
	The explicit DEFAULT option allows developers to differentiate between a value set that happens to be
	the current default, and a value that has been returned to the "default" explicitly.
	"""

	@property
	def _displayStringLabels(self):
		""" These labels will be used in the GUI when displaying the options.
		"""
		# To prevent duplication, self.DEFAULT is not included here.
		return {
			# Translators: Label for an option in NVDA settings.
			self.WHEN_NECESSARY: _("Only when necessary"),
			# Translators: Label for an option in NVDA settings.
			self.WHERE_SUITABLE: _("Where suitable"),
			# Translators: Label for an option in NVDA settings.
			self.ALWAYS: _("ALWAYS"),
		}

	DEFAULT = enum.auto()
	WHEN_NECESSARY = enum.auto()
	WHERE_SUITABLE = enum.auto()
	ALWAYS = enum.auto()
```

## Config Spec
In `configSpec.py` specify the new config key, ideally in the category that is most relevant to the feature.
Placing it in a category rather than a catch-all feature flags category, allows for the option to become
permanent without having to write config upgrade code to move it from section to another.

```ini
[virtualBuffers]
    newOptionForUsers = featureFlag(optionsEnum="BoolFlag", behaviourOfDefault="disabled")
    anotherOptionForUsers = featureFlag(optionsEnum="AllowUiaInMSWordFlag", behaviourOfDefault="WHERE_SUITABLE")
```

The `featureFlag` type is a custom spec type.
It will produce a `config.FeatureFlag` class instance when the key is accessed.
```python
newFlagValue: config.FeatureFlag = config.conf["virtualBuffers"]["newOptionForUsers"]

# BoolFlag converts to bool automatically, taking into account 'behaviorOfDefault'
if newFlagValue:
    print("The new option is enabled")

anotherFlagValue: config.FeatureFlag = config.conf["virtualBuffers"]["anotherOptionForUsers"]

# Other "optionsEnum" types can compare with the value, the 'behaviorOfDefault' is taken into account.
if flagValue == AllowUiaInMSWordFlag.ALWAYS:
    print("Another option is enabled")
```

## GUI
A control (`gui.nvdaControls.FeatureFlagCombo`) is provided to simplify exposing the feature flag to the user.

### Usage:
Note the comments in the example:
- `creation`
- `is default`
- `reset to default value`
- `save GUI value to config`


```python
import collections
from gui import nvdaControls, guiHelper
import config
import wx

sHelper = guiHelper.BoxSizerHelper(self, sizer=wx.BoxSizer(wx.HORIZONTAL))

# Translators: Explanation for the group name
label = _("Virtual Buffers")
vbufSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=label)
vbufGroup = guiHelper.BoxSizerHelper(vbufSizer, sizer=vbufSizer)
sHelper.addItem(vbufGroup)

# creation
self.newOptionForUsersCombo: nvdaControls.FeatureFlagCombo = vbufGroup.addLabeledControl(
    labelText=_(
        # Translators: Explanation of what the control does and where it is used.
        "New option for users"
    ),
    wxCtrlClass=nvdaControls.FeatureFlagCombo,
    keyPath=["virtualBuffers", "newOptionForUsers"], # The path of keys, see config spec.
    conf=config.conf, # The configObj instance, allows getting / setting the value
)
...
# is default
# Checking if the user has a saved (non-default) value
self.loadChromeVbufWhenBusyCombo.isValueConfigSpecDefault()
...
# reset to default value:
self.loadChromeVbufWhenBusyCombo.resetToConfigSpecDefault()
...
# save GUI value to config:
self.loadChromeVbufWhenBusyCombo.saveCurrentValueToConf()
```

## User Guide Documentation
Refer to [User Guide Standards](./userGuideStandards.md#feature-settings)
