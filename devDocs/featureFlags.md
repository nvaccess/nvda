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

## Config Spec
In `configSpec.py` specify the new config key, ideally in the category that is most relevant to the feature.
Placing it in a category rather than a catch-all feature flags category, allows for the option to become
permanent without having to write config upgrade code to move it from section to another.

```ini
[virtualBuffers]
    newOptionForUsers= featureFlag(behaviourOfDefault=disabled)
```

The `featureFlag` type is a custom spec type.
It will produce a `config.FeatureFlag` class instance when the key is accessed.
```python
flagValue: config.FeatureFlag = config.conf["virtualBuffers"]["newOptionForUsers"]
if flagValue:  # converts to bool automatically, taking into account 'behaviorOfDefault'
    print("The new option is enabled")
```

## GUI
A control (`gui.nvdaControls.FeatureFlagCombo`) is provided to simplify exposing the feature flag to the user.

### Usage:
Note comments:
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
    translatedOptions=collections.OrderedDict({ # OrderedDict to communicate that order of items will be preseverd.
        # Translators: Explanation of yes option
        config.FeatureFlagValues.ENABLED: _("Yes"),
        # Translators: Explanation of no option
        config.FeatureFlagValues.DISABLED: _("No"),
    })
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
