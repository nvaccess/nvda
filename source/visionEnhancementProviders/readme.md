## Vision Enhancement Providers

These modules use the "vision framework" to augment visual information presented to the user.
For more information about the implementation of a provider see vision.providerBase.VisionEnhancementProvider
(in source/vision/providerBase.py)

Two of the built-in examples are:
- NVDA Highlighter which will react to changes in focus and draw a rectangle outline around the focused object.
- Screen Curtain which when enabled makes the screen black for privacy reasons.

A vision enhancement provider module should have a class called `VisionEnhancementProvider`.
To make identifying a provider that is causing errors easier, name your provider class something descriptive and set
`VisionEnhancementProvider = MyProviderClass` at the bottom of your module.
See the NVDAHighlighter module as an example.
EG:

```
class MyProviderClass:
	...

VisionEnhancementProvider = MyProviderClass
print(VisionEnhancementProvider.__qualname__) # prints: MyProviderClass
```

### Provider settings

Providers must provide an VisionEnhancementProviderSettings object (via VisionEnhancementProvider.getSettings).
This VisionEnhancementProviderSettings instance then provides the DriverSettings objects via the supportedSettings
property.
These are used to save / load settings for the provider.

### Providing a GUI

A GUI can be built automatically from the DriverSettings objects accessed via the VisionEnhancementProviderSettings.
Alternatively the provider can supply a custom settings panel implementation via the getSettingsPanelClass class method.
A custom settings panel must return a class type derived from gui.SettingsPanel which will take responsibility for
building the GUI.
For an example see NVDAHighlighter or ScreenCurtain.

#### Automatic GUI building

The provider settings (described above) are also used to automatically construct a GUI for the provider when
getSettingsPanelClass returns None.

See exampleProvider_autoGui.py