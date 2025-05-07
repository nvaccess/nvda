# NVDA NVDA_VERSION Developer Guide

[TOC]



## Introduction {#introduction}

This guide provides information concerning NVDA development, including translation and the development of components for NVDA.

### Add-on API stability {#API}

The NVDA Add-on API includes all NVDA internals, except symbols that are prefixed with an underscore.

The NVDA Add-on API changes over time, for example because of the addition of new features, removal or replacement of outdated libraries, deprecation of unused or replaced code and methodologies, and changes to Python.
Important changes to the API are announced on the [NVDA API mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-api/about).
Changes relevant to developers are also announced via the [NVDA changes file](https://download.nvaccess.org/documentation/changes.html).
Any changes to the API policy outlined in this section will be conveyed via these two channels.

API breaking releases happen at most once per year, these are `.1` releases, e.g. `2022.1`.
The API remains backwards compatible between breaking releases.
API breaking changes should be considered relatively stable in the first beta: e.g. `2022.1.beta1`.

API features may become deprecated over time.
Deprecated API features may have a scheduled removal date, a future breaking release (e.g. `2022.1`).
Deprecations may also have no scheduled removal date, and will remain supported until it is no longer reasonable.
Note, the roadmap for removals is 'best effort' and may be subject to change.
Please open a GitHub issue if the described add-on API changes result in the API no longer meeting the needs of an add-on you develop or maintain.

### A Note About Python {#aboutPython}

NVDA and its components are primarily written in the Python programming language.
It is not the goal of this guide to teach you Python, though examples are provided through out this guide which will help to familiarise you with the Python syntax.
Documentation and other resources related to the Python language can be found at [www.python.org/](http://www.python.org/)

### C++ {#cPlusPlus}

Some of NVDA is written in C++, e.g. nvdaHelper.
For an overview of nvdaHelper, including how to configure Visual Studio to enable intellisense see the
[nvdaHelper readme](https://github.com/nvaccess/nvda/blob/master/nvdaHelper/readme.md)

## Translation {#translation}

In order to support multiple languages/locales, NVDA must be translated, and data specific to the locale must be provided.
This section only includes information on custom NVDA file formats required for translation.
Other items need to be translated, such as the NVDA user interface and documentation, but these use standard file formats.
For complete documentation about translating NVDA, please see the [Translating page](https://github.com/nvaccess/nvda/blob/master/projectDocs/translating/readme.md)

### Character Descriptions {#characterDescriptions}

Sometimes it can be very difficult or even impossible to distinguish one character from another.
For example, two characters might be pronounced the same way, even though they are actually different characters.
To help users when this occurs, character descriptions can be provided which describe the character in a unique way.

Character descriptions can be provided for a locale in a file named `characterDescriptions.dic` in the directory for the locale.
This is a UTF-8 encoded text file.
Blank lines and lines beginning with a "`#`" character are ignored.
All other lines should contain a character, followed by a tab, then one or more descriptions separated by tabs.
Multiple descriptions for a character will be read with natural pauses between them when reading a single character, e.g. when using `leftArrow` or `rightArrow`.
When reading character descriptions of multiple subsequent characters using spelling commands, the first description is used for each character, e.g. spelling the current line with triple press on `NVDA+upArrow`.

For example:

```
# This is a comment.
a	alpha
b	bravo beta
```

In this example, "a" will read "alpha" as the character description, and "b" will read as "bravo, beta".

In most cases, the characters in this file should be a single lower case character.
It is assumed that characters will have the same description regardless of their case, so upper case characters are converted to lower case before looking up their character descriptions.

#### Translating this file {#TranslatingCharacterDescriptionsFile}

Translation of `characterDescriptions.dic` happens via [Pull Request to NVDA](https://github.com/nvaccess/nvda/blob/master/projectDocs/translating/github.md).

For a full example and reference, please look at [the English `characterDescriptions.dic` file](https://github.com/nvaccess/nvda/blob/master/source/locale/en/characterDescriptions.dic).

### Symbol Pronunciation {#symbolPronunciation}

It is often useful to hear punctuation and other symbols pronounced as words when reading text, particularly when moving by character.
Unfortunately, the pronunciation of symbols is inconsistent between speech synthesisers and many synthesisers do not speak many symbols and/or do not allow control over what symbols are spoken.
Therefore, NVDA allows information about symbol pronunciation to be provided.

This is done for a locale by providing a file named `symbols.dic` in the directory for the locale.
This is a UTF-8 encoded text file.
Blank lines and lines beginning with a "`#`" character are ignored.
All locales implicitly inherit the symbol information for English, though any of this information can be overridden.

The file contains two sections, [complex symbols](#complexSymbols) and [symbols](#symbolInformation).

#### Defining Complex Symbols {#complexSymbols}

The first section is optional and defines regular expression patterns for complex symbols.
Complex symbols are symbols which aren't simply a character or sequence of characters, but instead require a more complicated match.
An example is the full stop (.) sentence ending in English.
The "." is used for multiple purposes, so a more complicated check is required to determine whether this refers to the end of a sentence.

The complex symbols section begins with the line:

```
complexSymbols:
```

Subsequent lines contain a textual identifier used to identify the symbol, a tab and the regular expression pattern for that symbol.
For example:

```re
sentence ending	(?<=[^\s.])\.(?=[\"')\s]|$)
dates with .	\b(\d\d)\.(\d\d)\.(\d{2}|\d{4})\b
```

Again, the English symbols are inherited by all other locales, so you need not include any complex symbols already defined for English.

#### Defining Symbol Information {#symbolInformation}

The second section provides information about when and how to pronounce all symbols.
It begins with the line:

```
symbols:
```

Subsequent lines should contain several fields separated by tabs.
The only mandatory fields are the identifier and replacement.
The default will be used for omitted fields.
The fields are as follows:

* `identifier`: The identifier of the symbol.
  In most cases, this is just the character or characters of the symbol.
  However, it can also be the identifier of a complex symbol.
  Certain characters cannot be typed into the file, so the following special sequences can be used:
  * `\0`: null
  * `\t`: tab
  * `\n`: line feed
  * `\r`: carriage return
  * `\f`: form feed
  * `\#`: # character (needed because # at the start of a line denotes a comment)
* `replacement:` The text which should be spoken for the symbol.
  If the symbol is a complex symbol, `\1`, `\2`, etc. can be used to refer to the groups matches, which will be inlined in the replacement, allowing for simpler rules.
  This also means that to get a `\` character in the replacement, one has to type `\\`.
* `level`: The symbol level at which the symbol should be spoken.
  * The symbol level is configured by the user and specifies the amount of symbols that should be spoken.
  * This field should contain one of the levels "none", "some", "most", "all" or "char", or "-" to use the default.
  * "char" means that the symbol should only be pronounced when moving by character.
  * The default is to inherit the value or "all" if there is nothing to inherit.
* `preserve`: Whether the symbol itself should be preserved to facilitate correct pronunciation by the synthesiser.
  For example, symbols which cause pauses or inflection (such as the comma in English) should be preserved.
  This field should be one of the following:
  * `never`: Never preserve the symbol.
  * `always`: Always preserve the symbol.
  * `norep`: Only preserve the symbol if it is not being replaced; i.e. the user has set symbol level lower than the level of this symbol.
  * `-`: Use the default.
  The default is to inherit the value or "never" if there is nothing to inherit.

Finally, a display name for the symbol can be provided in a comment after a tab at the end of the line.
This will be shown to users when editing the symbol information and is especially useful for translators to define translated names for English complex symbols.

#### Examples {#TranslatingSymbolsExamples}

```
(	left paren	most
```

This means that the "(" character should be spoken as "left paren" only when the symbol level is set to most or higher; i.e. most or all.

```
,	comma	all	always
```

This means that the "," character should be spoken as "comma" when the symbol level is set to all and that the character itself should always be preserved so that the synthesiser will pause appropriately.

```
. sentence ending	point	# . fin de phrase
```

This line appears in the French symbols.dic file.
It means that the ". sentence ending" complex symbol should be spoken as "point".
Level and preserve are not specified, so they will be taken from English.
A display name is provided so that French users will know what the symbol represents.

```
dates with .	\1 point \2 point \3	all	norep	# date avec points
```

This line appears in the French symbols.dic file.
It means that the first, second, and third groups of the match will be included, separated by the word 'point'.
The effect is thus to replace the dots from the date with the word 'point'.

If your language uses a thousands separator such as a full stop (.) which is handled incorrectly due to other rules, you will need to define a complex symbol pattern for it.
For example, if your language uses a comma (,) as its thousands separator, you would include the following in the complex symbols section:

```re
thousands separator	(?<=\d)\,(?=\d)
```

You would also include something like the following in the main symbols section:

```
thousands separator	comma	all	norep
```

#### Translating this file {#TranslatingSymbolsFile}

Translation of `symbols.dic` happens via [Pull Request to NVDA](https://github.com/nvaccess/nvda/blob/master/projectDocs/translating/github.md).

See the file [locale\en\symbols.dic](https://github.com/nvaccess/nvda/blob/master/source/locale/en/symbols.dic) for the English definitions which are inherited for all locales.

### Gestures {#TranslatingGestures}

The gestures defined originally in NVDA are configured to expect English software and keyboard layout.
In most cases, these gestures can also be executed on other keyboard layouts without any problem.
However, sometimes a gesture originally defined by NVDA is not suitable for a specific locale (keyboard layout or software).
The need to modify an original gesture may be due to the following reasons:

* The original gesture is defined with a character that is not a key name on the locale keyboard layout.
Generally, the key names are the characters that can be input without the help of a modifier key (`shift`, `control`, etc.)
* The original gesture takes advantage of the key's physical location on the English keyboard layout, but this advantage does not exist with the locale keyboard layout.
* The original gesture is defined to match a native shortcut in Windows or in an application, but the shortcut in the local version of Windows or of this application is not the same as the English one.

In all of these cases, NVDA allows remapping of this gesture for this specific locale.

#### Examples {#TranslatingGesturesExamples}

Below are three detailed examples of `gestures.ini` files corresponding to the three listed situations where a gesture remapping could be required.

##### Example 1: The original gesture is defined with a character that is not a key name on the locale keyboard layout {#TranslatingGesturesEx1}

In the original English version, the scripts for left and right mouse click (laptop layout) are executed with `NVDA+[` and `NVDA+]`, respectively.

* On an English keyboard layout, the `[` and `]` keys are the two keys to the right of the `p` key.
* On an Italian keyboard layout, `[` and `]` characters can only be input with the help of the `altGr` modifier: `altGr+è` and `altGr+plus`, respectively.

Thus, the Italian translators decided to remap these scripts using the two keys at the right of the `p` key on the Italian keyboard layout, i.e. `è` and `+`.
To do this, they have added the following lines in the `gestures.ini` file:

```
[globalCommands.GlobalCommands]
	leftMouseClick = kb(laptop):NVDA+è
	rightMouseClick = kb(laptop):NVDA+plus
```

##### Example 2: The original gesture takes advantage of the keys physical location {#TranslatingGesturesEx2}

Looking again at the scripts for left and right mouse click (laptop layout) we can see that they are originally mapped (in English) to two neighboring keys.
This corresponds to the left and right buttons of the mouse.
As seen in example 1, many translators have had to modify these keys.
Most of them (if not all) have chosen two neighboring keys.
For example, in the French `gestures.ini`, the following lines have been added:

```
[globalCommands.GlobalCommands]
	None = kb(laptop):nvda+[, kb(laptop):nvda+control+[, kb(laptop):nvda+], kb(laptop):nvda+control+], kb(laptop):nvda+shift+., kb(laptop):nvda+., kb(laptop):nvda+control+.
	leftMouseClick = kb(laptop):nvda+ù
	rightMouseClick = kb(laptop):nvda+*
```

The `ù` and `*` on the French layout are not at the same location as `[` and `]` of the English layout, but these are still two neighboring keys.
Moreover we can see here that `NVDA+[` and `NVDA+]`, among others, have been mapped to `None`, in order to unbind these gestures.
For the French (France) layout, this was not mandatory since there is no possibility to input `NVDA+[` or `NVDA+]` without any other modifier key.

##### Example 3: The original gesture is defined to match a native shortcut {#TranslatingGesturesEx3}

NVDA provides a script for the Word document object named `toggleBold`.
This script is mapped to the same gesture as the Word native shortcut to set text bold, i.e. `control+b` in the English version of Word.
However in the French version of Word, the shortcut to turn text bold is `control+g`.
The G stands for "gras" meaning "bold" in French.
The following lines have been added in the French `gestures.ini` file to remap this script:

```
[NVDAObjects.window.winword.WordDocument]
	None = kb:control+b, kb:control+[, kb:control+], "kb:control+shift+,", kb:control+shift+., kb:control+l, kb:control+r
	toggleBold = kb:control+g, kb:control+shift+b
```

We can see that `control+b` has been unbound.
This was necessary because it is the shortcut of another command in the French version of Word.
No remapping has been done for the `toggleItalic` script, since the shortcut is the same for French and English versions of Word.

#### How to remap a shortcut key {#TranslatingGesturesSteps}

##### Identify the class, the script and the original gesture to be remapped {#TranslatingGesturesStepIdentify}

To edit the `gesture.ini` file, you will have to identify the class, the script and the original shortcut you want to remap.

##### Case of a global command script {#TranslatingGesturesStepCaseGlobal}

If the gesture to be remapped is a global command, you may execute the following steps to find out the class and the script name of the command:

* activate input help (`NVDA+1`)
* press the gesture you want to remap, e.g. `NVDA+]` (laptop layout)
* de-activate input help (`NVDA+1`)
* open the log (`NVDA+F1`)
* find the line corresponding to the moment you executed the gesture, e.g.:

  ```
  Input help: gesture kb(laptop):NVDA+], bound to script rightMouseClick on globalCommands.GlobalCommands
  ```

The information you are searching is on this line:

* script name: `rightMouseClick`
* class name: `globalCommands.GlobalCommands` (Note that this is always the class for global commands)
* original gesture: `kb(laptop):NVDA+]`

##### Case of an application specific script {#TranslatingGesturesStepCaseApplication}

In case you want to remap an application specific script, you will have to follow the same steps as those for a global command script.
You just need to ensure before proceeding that you are in the targeted application.

##### Case of an object specific script {#TranslatingGesturesStepCaseObject}

For object specific scripts such as the ones linked to `NVDAObjects.window.winword.WordDocument`, you may follow the same steps as those for application specific scripts, paying attention to the following two points:

* You need to ensure before proceeding that the object to which the script is bound is focused.
* Some of these scripts have no help message, so you may not hear anything when executing them in input help mode; but the script's name and the class of the object will still appear in the log.

Note that the class of the object appearing in the log may be a subclass of the one where the original gesture is actually bound.
In this case, you will have to explore NVDA's source code to find this parent class.

#### Translating this file {#TranslatingGesturesFile}

Translation of `gestures.ini` happens via [Pull Request to NVDA](https://github.com/nvaccess/nvda/blob/master/projectDocs/translating/github.md).

1. In this file the sections correspond to the class to which the script belongs.
If the class your looking for does not exist, create this section.
1. Under the targeted section, add a line corresponding to the new shortcut. e.g.:

   ```
   toggleBold = kb:control+g, kb:control+shift+b
   ```

   If a line already exists for the script name, but you want to modify the shortcut, add the new shortcut on the same line, separating each shortcut with a comma ("`,`").

1. If you want to unmap the original shortcut, just map it to `None`, e.g.:

   ```
   None = kb:control+b
   ```

   Unmapping the original shortcut is only required if this shortcut does not match any other remapped locale shortcut.

## Plugins {#plugins}
### Overview {#pluginsOverview}

Plugins allow you to customize the way NVDA behaves overall or within a particular application.
They are able to:

* Respond to particular events such as focus and object property changes; e.g. when a control changes its name.
* Implement commands which are bound to particular key presses or other input.
* Customise the behaviour of and implement additional functionality for particular controls.
* Customise or add new support for text content and complex documents.

This section provides an introduction to developing plugins.
Developers should consult the code documentation for a complete reference.

### Types of Plugins {#pluginsTypes}

There are two types of plugins. These are:

* App Modules: code specific to a particular application.
The App Module receives all events for a particular application, even if that application is not currently active.
When the application is active, any commands that the App Module has bound to key presses or other input can be executed by the user.
* Global Plugins: code global to NVDA; i.e. it is used in all applications.
Global Plugins Receive all events for all controls in the Operating System.
Any commands bound by a Global Plugin can be executed by the user wherever they are in the operating system, regardless of application.

If you wish to improve NVDA's access to a particular application, it is most likely you will want to write an App Module.
In contrast, if you wish to add some overall functionality to NVDA (e.g. a script that announces current Wireless network strength while in any application), then a Global Plugin is what you want.

Both App Modules and Global Plugins share a common look and feel.
They are both Python source files (with a .py extension), they both define a special class containing all events, scripts and bindings, and they both may define custom classes to access controls, text content and complex documents.
However, they do differ in some ways.

Custom appModules and globalPlugins can be packaged into NVDA add-ons.
This allows easy distribution, and provides a safe way for the user to install and uninstall the custom code.
Please refer to the [Add-ons section](#Addons) later on in this document.

In order to test the code while developing, you can place it in a special 'scratchpad' directory in your NVDA user configuration directory.
You will also need to configure NVDA to enable loading of custom code from the Developer Scratchpad Directory, by enabling this in the Advanced category of NVDA's Settings dialog.
The Advanced category also contains a button to easily open the Developer Scratchpad directory if enabled.

The following few sections will talk separately about App Modules and Global Plugins.
After this point, discussion is again more general.

### Basics of an App Module {#appModuleBasics}

App Module files have a .py extension, and in most cases should be named the same as either the main executable of the application for which you wish them to be used or the package inside a host executable.
For example, an App Module for notepad would be called notepad.py, as notepad's main executable is called notepad.exe.
To map a single App Module for multiple executables, or handle when an executable name violates the Python import rules, refer to [Associating App Modules with an executable](#AssociatingAppModule).
For apps hosted inside host executables, see the section on app modules for hosted apps.

App Module files must be placed in the appModules subdirectory of an add-on, or of the scratchpad directory of the NVDA user configuration directory.

App Modules must define a class called AppModule, which inherits from appModuleHandler.AppModule.
This class can then define event and script methods, gesture bindings and other code.
This will all be covered in depth later.

NVDA loads an App Module for an application as soon as it notices the application is running.
The App Module is unloaded once the application is closed or when NVDA is exiting.

### Associating App Modules with an executable {#AssociatingAppModule}

As explained above, sometimes the default way of associating an App Module with an application is not flexible enough. Examples include:

* You want to use a single App Module for various binaries (perhaps both stable and preview versions of the application should have the same accessibility enhancements)
* The executable file is named in a way which conflicts with the Python naming rules. i.e. for an application named "time", naming the App Module "time.py" would conflict with the built-in module from the standard library

In such cases you can distribute a small global plugin along with your App Module which maps it to the executable.
For example to map the App Module named "time_app_mod" to the "time" executable the plugin may be written as follows:

```py
import appModuleHandler
import globalPluginHandler


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		appModuleHandler.registerExecutableWithAppModule("time", "time_app_mod")

	def terminate(self, *args, **kwargs):
		super().terminate(*args, **kwargs)
		appModuleHandler.unregisterExecutable("time")
```

### Example 1: An App Module that Beeps on Focus Change Events {#Example1}

The following example App Module makes NVDA beep each time the focus changes within the notepad application.
This example shows you the basic layout of an App Module.

Copy and paste the code between (but not including) the start and end markers into a new text file called notepad.py, which should be saved in the AppModules subdirectory.
Be very careful to keep all tabs and spaces intact.

Once saved in the correct location, either restart NVDA or choose Reload Plugins found under Tools in the NVDA menu.

Finally, open Notepad and move the focus around the application; e.g. move along the menu bar, open some dialog boxes, etc.
You should hear beeps each time the focus changes.
Note though that if you move outside of Notepad - for instance, to Windows Explorer - you do not hear beeps.

```py
# Notepad App Module for NVDA
# Developer guide example 1

import appModuleHandler

class AppModule(appModuleHandler.AppModule):

	def event_gainFocus(self, obj, nextHandler):
		import tones
		tones.beep(550, 50)
		nextHandler()
```

This App Module file starts with two comment lines, which describe what the file is for.

It then imports the appModuleHandler module, so that the App Module then has access to the base AppModule class.

Next, it defines a class called AppModule, which is inherited from appModuleHandler.AppModule.

Inside this class, it defines 1 or more events, scripts or gesture bindings.
In this example, it defines one event method for gainFocus events (event_gainFocus), which plays a short beep each time it is executed.
The implementation of this event is not important for the purposes of this example.
The most important part is the class itself.
Events will be covered in greater detail later.

As with other examples in this guide, remember to delete the created app module when you are finished testing and then restart NVDA or reload plugins, so that original functionality is restored.

### App modules for hosted apps {#appModulesForHostedApps}

Some executables host various apps inside or are employed by an app to display their interfaces.
These include `javaw.exe` for running various Java programs, `wwahost.exe` for some apps in Windows 8 and later, and `msedgewebview2.exe` for displaying web-like interfaces on apps employing Edge WebView2 runtime.

If an app runs inside a host executable or employs a different app to display the interface, the name of the app module must be the name as defined by the host or the interface executable, which can be found through the `AppModule.appName` property.
For example, an app module for a Java app named "`test`" hosted inside `javaw.exe` must be named `test.py`.
For apps hosted inside `wwahost`, not only must the app module name be the name of the loaded app, but the app module must subclass the app module class found in `wwahost`.
By default, apps employing Edge WebView2 such as modern Outlook (olk.exe) are displayed as a webpage.

### Example 2: an app module for an app hosted by `wwahost.exe` {#example2}

The following example is the same as the Notepad app module above, except this is for an app hosted by `wwahost.exe`.

```py
# wwahost/test App Module for NVDA
# Developer guide example 2

from nvdaBuiltin.appModules.wwahost import *

class AppModule(AppModule):

	def event_gainFocus(self, obj, nextHandler):
		import tones
		tones.beep(550, 50)
		nextHandler()
```

The biggest difference from the Notepad app module is where the `wwahost` app module comes from.
As a built-in app module, `wwahost` can be imported from `nvdaBuiltin.appModules`.

Another difference is how the app module class is defined.
As wwahost app module provides necessary infrastructure for apps hosted inside, you just need to subclass the wwahost AppModule class.

### Example 3: an app module for an app employing Edge WebView2 (`msedgewebview2.exe`) {#example3}

The following example is an app module employing Edge WebView2 runtime with browse mode disabled by default, using modern Outlook (olk.exe) as an example.

```py
# msedgewebview2 example (modern Outlook/olk.py)

import appModuleHandler

class AppModule(appModuleHandler.AppModule):
	disableBrowseModeByDefault: bool = True
```

Browse mode is disabled for this example because apps employing WebView2 display their interfaces as webpages.
You can remove the "disableBrowseModeByDefault" line if you would like to let users navigate the app using browse mode commands.

### Basics of a Global Plugin {#globalPluginBasics}

Global Plugin files have a .py extension, and should have a short unique name which identifies what they do.

Global plugin files must be placed in the globalPlugins subdirectory of an add-on, or of the scratchpad directory of the NVDA user configuration directory.

Global Plugins must define a class called GlobalPlugin, which inherits from globalPluginHandler.GlobalPlugin.
This class can then define event and script methods, gesture bindings and other code.
This will all be covered in depth later.

NVDA loads all global plugins as soon as it starts, and unloads them on exit.

### Example 3: a Global Plugin Providing a Script to Announce the NVDA Version {#example3}

The following example Global Plugin Allows you to press NVDA+shift+v while anywhere in the Operating System to find out NVDA's version.
This example is only to show you the basic layout of a Global Plugin.

Copy and paste the code between (but not including) the start and end markers into a new text file with a name of example2.py, which should be saved in the globalPlugins subdirectory.
Be very careful to keep all tabs and spaces intact.

Once saved in the right place, either restart NVDA or choose Reload Plugins found under Tools in the NVDA menu.

From anywhere, you can now press `NVDA+shift+v` to have NVDA's version spoken and brailled.

```py
# Version announcement plugin for NVDA
# Developer guide example 3

import globalPluginHandler
from scriptHandler import script
import ui
import versionInfo


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(gesture="kb:NVDA+shift+v")
	def script_announceNVDAVersion(self, gesture):
		ui.message(versionInfo.version)
```

This Global Plugin file starts with two comment lines, which describe what the file is for.

It then imports the globalPluginHandler module, so that the Global Plugin has access to the base GlobalPlugin class.

It also imports a few other modules, namely ui, versionInfo and scriptHandler, which this specific plugin needs in order for it to perform the necessary actions to announce the version.

Next, it defines a class called GlobalPlugin, which is inherited from globalPluginHandler.GlobalPlugin.

Inside this class, it defines 1 or more events, scripts or gesture bindings.
In this example, it defines a script method that performs the version announcement.
The script decorator from the scriptHandler module is used to assign the NVDA+shift+v shortcut to this script.
However, the details of the script and its binding are not important for the purposes of this example.
The most important part is the class itself.
More information about scripts and the script decorator can be found in the [Defining script properties](#DefiningScriptProperties) section of this guide.

As with other examples in this guide, remember to delete the created Global Plugin when finished testing and then restart NVDA or reload plugins, so that original functionality is restored.

### NVDA Objects {#NVDAObjects}

NVDA represents controls and other GUI elements as NVDA Objects.
These NVDA Objects contain standardised properties, such as name, role, value, states and description, which allow other parts of NVDA to query or present information about a control in a generalised way.
For example, the OK button in a dialog would be represented as an NVDA Object with a name of "OK" and a role of button.
Similarly, a checkbox with a label of "I agree" would have a name of "I agree", a role of checkbox, and if currently checked, a state of checked.

As there are many different GUI Toolkits and platform and accessibility APIs, NVDA Objects abstract these differences into a standard form that NVDA can use, regardless of the toolkit or API a particular control is made with.
For example, the Ok button just discussed could be a widget in a Java application, an MSAA object, an IAccessible2 object or a UI Automation element.

NVDA Objects have many properties.
Some of the most useful are:

* name: the label of the control.
* role: one of the Role.* constants from NVDA's controlTypes module.
Button, dialog, editableText, window and checkbox are examples of roles.
* states: a set of 0 or more of the State.* constants from NVDA's controlTypes module.
Focusable, focused, selected, selectable, expanded, collapsed and checked are some examples of states.
* value: the value of the control; e.g. the percentage of a scroll bar or the current setting of a combo box.
* description: a sentence or two describing what the control does (usually the same as its tooltip).
* location: the object's left, top, width and height positions in screen coordinates.
* parent: this object's parent object.
For example, a list item object's parent would be the list containing it.
* next: the object directly after this one on the same level in logical order.
For example, a menu item NVDA Object's next object is most likely another menu item within the same menu.
* previous: like next but in reverse.
* firstChild: the first direct child object of this object.
For example, a list's first child would be the first list item.
* lastChild: the last direct child of this object.
* children: a list of all the direct children of this object; e.g. all the menu items in a menu.

There are also a few simplified navigation properties such as simpleParent, simpleNext, simpleFirstChild and simpleLastChild.
These are like their respective navigation properties described above, but NVDA filters out useless objects.
These properties are used when NVDA's simple review mode is turned on, which is the default.
These simple properties may be easier to use, but the real navigation properties more closely reflect the underlying Operating System structure.
Also, these may change in future versions of NVDA as improvements are made to simple review, so they should generally be avoided when programmatically locating specific objects.

When developing plugins, most of the time, it is not important what toolkit or API backs an NVDA Object, as the plugin will usually only access standard properties such as name, role and value.
However, as plugins become more advanced, it is certainly possible to delve deeper into NVDA Objects to find out toolkit or API specific information if required.

Plugins make use of NVDA Objects in three particular ways:

* Most events that plugins receive take an argument which is the NVDA Object on which the event occurred.
For example, event_gainFocus takes the NVDA Object that represents the control gaining focus.
* Scripts, events or other code may fetch objects of interest such as the NVDA Object with focus, NVDA's current navigator object, or perhaps the Desktop NVDA Object.
The code may then retrieve information from that object or perhaps even retrieve another object related to it (e.g. its parent, first child, etc.).
* the Plugin may define its own custom NVDA Object classes which will be used to wrap a specific control to give it extra functionality, mutate its properties, etc.

Just like App Modules and Global Plugins, NVDA Objects can also define events, scripts and gesture bindings.

### Scripts and Gesture Bindings {#scripts}

App Modules, Global Plugins and NVDA Objects can define special methods which can be bound to a particular piece of input such as a key press.
NVDA refers to these methods as scripts.

A script is a standard Python instance method with a name starting with "script_"; e.g. "script_sayDateTime".

A script method takes two arguments:

* self: a reference to the App Module, Global Plugin or NVDA Object instance the script was called on.
* gesture: an Input Gesture object, which represents the input that caused the script to run.

As well as the actual script method, some form of gesture binding must be defined, so that NVDA knows what input should execute the script.

A gesture identifier string is a simple string representation of a piece of input.
It consists of a two letter character code denoting the source of the input, an optional device in brackets, a colon (:) and one or more names separated by a plus (+) denoting the actual keys or input values.

Some examples of gesture string identifiers are:

* "kb:NVDA+shift+v"
* "br(freedomScientific):leftWizWheelUp"
* "br(alva.BC640):t3"
* "kb(laptop):NVDA+t"

Currently, the input sources in NVDA are:

* kb: system keyboard input
* br: braille display controls
* ts: touch screen
* bk: braille keyboard input

When NVDA receives input, it looks for a matching gesture binding in a particular order.
Once a gesture binding is found, the script is executed and no further bindings are used, nor is that particular gesture passed on automatically to the Operating System.

The order for gesture binding lookup is:

* The user specific gesture map
* The locale specific gesture map
* The braille display driver specific gesture map
* Loaded Global Plugins
* App Module of the active application
* Tree Interceptor of the NVDA Object with focus if any; e.g. a virtualBuffer
* NVDA Object with focus
* Global Commands (built in commands like quitting NVDA, object navigation commands, etc.)

#### Defining script properties {#DefiningScriptProperties}

For NVDA 2018.3 and above, the recommended way to set script properties is by means of the so called script decorator.
In short, a decorator is a function that modifies the behavior of a particular function or method.
The script decorator modifies the script in such a way that it will be properly bound to the desired gestures.
Furthermore, it ensures that the script is listed with the description you specify, and that it is categorised under the desired category in the input gestures dialog.

In order for you to use the `script` decorator, you will have to import it from the `scriptHandler` module.

```py
from scriptHandler import script
```

After that, just above your script definition, add the `script` decorator, providing the desired arguments.
For example:

```py
	@script(
		description=_("Speaks the date and time"),
		category=inputCore.SCRCAT_MISC,
		gestures=["kb:NVDA+shift+t", "kb:NVDA+alt+r"]
	)
	def script_sayDateTime(self, gesture):
```

In this example, your script will be listed in the input gestures dialog under the "Miscellaneous" category.
It will have the description "Speaks the date and time", and will be bound to the "NVDA+shift+t" and "NVDA+alt+r" key combinations on the keyboard.

The following keyword arguments can be used when applying the script decorator:

* description: A short, translatable string which describes the command for users.
  This is reported to users when in Input Help mode and shown in the input gestures dialog.
  The script will not appear in the Input Gestures dialog unless you specify a description.
* category: The category of the script in order for it to be grouped with other similar scripts.
  For example, a script in a global plugin which adds browse mode quick navigation keys may be categorized under the "Browse mode" category.
  The category can be set for individual scripts, but you can also set the "scriptCategory" attribute on the plugin class, which will be used for scripts which do not specify a category.
  There are constants for common categories prefixed with SCRCAT_ in the inputCore and globalCommands modules, which can also be specified.
  The script will be listed under the specified category in the Input Gestures dialog.
  If no category is specified, the script will be categorized under "Miscellaneous".
* gesture: A string containing a single gesture associated with this script, e.g. "kb:NVDA+shift+r".
* gestures: A string list of multiple gestures associated with this script, e.g. ["kb:NVDA+shift+r", "kb:NVDA+alt+t"].
  When both gesture and gestures are specified, they are combined.
  Either gesture, or any item in gestures can be used to trigger the script.
* canPropagate: A boolean indicating whether this script should also apply when it belongs to a focus ancestor object.
  For example, this can be used when you want to specify a script on a particular foreground object, or another object in the focus ancestry which is not the current focus object.
  This option defaults to False.
* bypassInputHelp: A boolean indicating whether this script should run when input help is active.
  This option defaults to False.
* allowInSleepMode: A boolean indicating whether this script should run when sleep mode is active.
  This option defaults to False.
* resumeSayAllMode: The say all mode that should be resumed when active before executing this script.
  The constants for say all mode can be found in the CURSOR enum in speech.sayAll.
  If resumeSayAllMode is not specified, say all does not resume after this script.
* speakOnDemand: A boolean indicating whether this script should produce speech when called while speech mode is "on-demand".
  This option defaults to False.

Though the script decorator makes the script definition process a lot easier, there are more ways of binding gestures and setting script properties.
For example, a special "__gestures" Python dictionary can be defined as a class variable on an App Module, Global Plugin or NVDA Object.
This dictionary should contain gesture identifier strings pointing to the name of the requested script, without the "script_" prefix.
You can also specify a description of the script in the method's "doc" attribute.
However, beware not to include an inline docstring at the start of the method if you do not set the "doc" attribute, as it would render the description not translatable.
The script decorator does not suffer from this limitation, so you are encouraged to provide inline docstrings as needed when using it.
Furthermore, an alternative way of specifying the script's category is by means of setting a "category" attribute on the script method to a string containing the name of the category.

### Example 4: A Global Plugin to Find out Window Class and Control ID {#example4}

The following Global Plugin allows you to press NVDA+leftArrow to have the window class of the current focus announced, and NVDA+rightArrow to have the window control ID of the current focus announced.
This example shows you how to define one or more scripts and gesture bindings on a class such as an App Module, Global Plugin or NVDA Object.

Copy and paste the code between (but not including) the start and end markers into a new text file with a name of example3.py, which should be saved in the globalPlugins subdirectory.
Be very careful to keep all tabs and spaces intact.

Once saved in the right place, either restart NVDA or choose Reload Plugins found under Tools in the NVDA menu.

```py
#Window utility scripts for NVDA
#Developer guide example 4

import globalPluginHandler
from scriptHandler import script
import ui
import api

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	@script(
		description=_("Announces the window class name of the current focus object"),
		gesture="kb:NVDA+leftArrow"
	)
	def script_announceWindowClassName(self, gesture):
		focusObj = api.getFocusObject()
		name = focusObj.name
		windowClassName = focusObj.windowClassName
		ui.message(f"class for {name} window: {windowClassName}")

	@script(
		description=_("Announces the window control ID of the current focus object"),
		gesture="kb:NVDA+rightArrow"
	)
	def script_announceWindowControlID(self, gesture):
		focusObj = api.getFocusObject()
		name = focusObj.name
		windowControlID = focusObj.windowControlID
		ui.message(f"Control ID for {name} window: {windowControlID}")
```

### Events {#events}

When NVDA detects particular toolkit, API or Operating System events, it abstracts these and fires its own internal events on plugins and NVDA Objects.

Although most events are related to a specific NVDA Object (e.g. name change, gain focus, state change, etc.), these events can be handled at various levels.
When an event is handled, it is stopped from going further down the chain.
However, code inside the event can choose to propagate it further if needed.

The order of levels through which the event passes until an event method is found is:

* Loaded Global Plugins
* The App Module associated with the NVDA Object on which the event was fired
* The Tree Interceptor (if any) associated with the NVDAObject on which the event was fired
* the NVDAObject itself.

Events are Python instance methods, with a name starting with "event_" followed by the actual name of the event (e.g. gainFocus).

These event methods take slightly different arguments depending at what level they are defined.

If an event for an NVDA Object is defined on an NVDA Object itself, the method only takes one mandatory argument which is the 'self' argument; i.e. the NVDA Object instance).
Some events may take extra arguments, though this is quite rare.

If an event for an NVDA Object is defined on a Global Plugin, App Module or Tree Interceptor, the event takes the following arguments:

* self: the instance of the Global Plugin, App Module or Tree Interceptor
* obj: the NVDA Object on which the event was fired
* nextHandler: a function that when called will propagate the event further down the chain.

Some common NVDA Object events are:

* foreground: this NVDA Object has become the new foreground object; i.e. active top-level object
* gainFocus
* focusEntered: Focus has moved inside this object; i.e. it is an ancestor of the focus object
* loseFocus
* nameChange
* valueChange
* stateChange
* caret: when the caret (insertion point) within this NVDA Object moves
* locationChange: physical screen location changes

There are many other events, though those listed above are usually the most useful.

For an example of an event handled by an App Module, please refer to [example 1](#Example1) (focus beeps in notepad).

### the App Module SleepMode variable {#appModuleSleepMode}

App Modules have one very useful property called "sleepMode", which if set to true almost completely disables NVDA within that application.
Sleep Mode is very useful for self voicing applications that have their own screen reading functionality, or perhaps even some games that need full use of the keyboard.

Although sleep mode can be toggled on and off by the user with the key command NVDA+shift+s, a developer can choose to have sleep mode enabled by default for an application.
This is done by providing an App Module for that application which simply sets sleepMode to True in the AppModule class.

### Example 5: A Sleep Mode App Module {#example5}

The following code can be copied and pasted in to a text file, then saved in the `appModules` directory with the name of the application you wish to enable sleep mode for.
As always, the file must have a `.py` extension.

```py
import appModuleHandler

class AppModule(appModuleHandler.AppModule):

	sleepMode = True
```

### Providing Custom NVDA Object Classes {#customNVDAObjectClasses}

Providing custom NVDA Object classes is probably the most powerful and useful way to improve the experience of an application in an NVDA plugin.
This method allows you to place all the needed logic for a particular control altogether in one NVDA Object class for that control, rather than scattering code for many controls across a plugin's events.

There are two steps to providing a custom NVDA Object class:

* Define the NVDA Object class and its events, scripts, gesture bindings and overridden properties.
* Tell NVDA to use this NVDA Object class in specific situations by handling it in the plugin's `chooseNVDAObjectOverlayClasses` method.

When defining a custom NVDAObject class, you have many NVDAObject base classes to choose from.
These base classes contain the base support for the particular accessibility or OS API underlying the control, such as win32, MSAA or Java access Bridge.
You should usually inherit your custom NVDAObject class from the highest base class you need in order to choose your class in the first place.
For example, if you choose to use your custom NVDAObject class when the window class name is "Edit" and the window control ID is 15, you should probably inherit from `NVDAObjects.window.Window`, as you are clearly aware that this is a Window object.
Similarly, if you match on MSAA's `accRole` property, you would probably need to inherit from `NVDAObjects.IAccessible.IAccessible`.
You should also consider what properties you are going to override on the custom NVDA Object.
For instance, if you are going to override an IAccessible specific property, such as `shouldAllowIAccessibleFocusEvent`, then you need to inherit from `NVDAObjects.IAccessible.IAccessible`.

The `chooseNVDAObjectOverlayClasses` method can be implemented on app modules or global plugin classes.
It takes 3 arguments:

1. `self`: the app module or global plugin instance.
1. `obj`: the `NVDAObject` for which classes are being chosen.
1. `clsList`: a Python list of `NVDAObject` classes that will be used for `obj`.

Inside this method, you should decide which custom NVDA Object class(es) (if any) this NVDA Object should use by checking its properties, etc.
If a custom class should be used, it must be inserted into the class list, usually at the beginning.
You can also remove classes chosen by NVDA from the class list, although this is rarely required.

### Example 6: Command to Retrieve the Length of Text in an Edit Field Using a Custom NVDA Object {#example6}

This app module for notepad provides a command to report the number of characters in edit fields.
You can activate it using `NVDA+l`.
Notice that the command is specific to edit fields; i.e. it only works while you are focused in an edit field, rather than anywhere in the application.

The following code can be copied and pasted in to a text file, then saved in the `appModules` directory with the name of `notepad.py`.

```py
import appModuleHandler
from scriptHandler import script
from NVDAObjects.IAccessible import IAccessible
import controlTypes
import ui

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "Edit" and obj.role == controlTypes.Role.EDITABLETEXT:
			clsList.insert(0, EnhancedEditField)

class EnhancedEditField(IAccessible):

	@script(gesture="kb:NVDA+l")
	def script_reportLength(self, gesture):
		ui.message(f"{len(self.value)}")
```

### Making Small Changes to an NVDA Object in App Modules {#smallChangesToNVDAObjectInAppModules}

Sometimes, you may wish to make only small changes to an NVDA Object in an application, such as overriding its name or role.
In these cases, you don't need the full power of a custom NVDA Object class.
To do this, you can use the `NVDAObject_init` event available only on App Modules.

The `event_NVDAObject_init` method takes two arguments:

1. `self`: the AppModule instance.
1. `obj`: the `NVDAObject` being initialized.

Inside this method, you can check whether this object is relevant and then override properties accordingly.

### Example 7: Labelling the Notepad Edit Field Using event_NVDAObject_init {#example7}

This app module for notepad makes NVDA report Notepad's main edit field as having a name of "content".
That is, when it receives focus, NVDA will say "Content edit".

The following code can be copied and pasted in to a text file, then saved in the `appModules` directory with the name of `notepad.py`.

```py
import appModuleHandler
from NVDAObjects.window import Window

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if isinstance(obj, Window) and obj.windowClassName == "Edit" and obj.windowControlID == 15:
			obj.name = "Content"
```

### Parsing additional command line arguments in your plugin {#PluginCLIArgs}

By default NVDA accepts a limited set of command line arguments and shows an error for unknown ones.
However, if you want to use any additional arguments, this is possible by adding a handler to the [extension point](#ExtensionPoints) `addonHandler.isCLIParamKnown`.
Note that since command line arguments are processed just after NVDA starts, your add-on needs to process them in a global plugin, since app modules or other drivers may not be loaded at this stage.
A sample handler can be written as follows:

```py
def processArgs(cliArgument: str) -> bool:
	if cliArgument == "--enable-addon-feature":
		# Code to process your argument...
		return True  # Argument is known to the add-on and should not be flagged by NVDA
	return False  # unknown argument - NVDA should warn user
```

Then the handler needs to be registered, preferably in the constructor of your global plugin:

```py
import addonHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self) -> None:
		super().__init__()
		addonHandler.isCLIParamKnown.register(processArgs)
```

## Packaging Code as NVDA Add-ons {#Addons}

Add-ons make it easy for users to share and install plugins, drivers, speech symbol dictionaries and braille translation tables.
They can be packaged in to a single NVDA add-on package, which the user can then install into a copy of NVDA via the Add-on Store found under Tools in the NVDA menu.
An add-on package is simply a standard zip archive with the file extension of "`nvda-addon`".
It can contain a manifest file, install/uninstall code and directories containing plugins, drivers, speech symbol dictionaries and braille translation tables.

### Non-ASCII File Names in Zip Archives {#nonASCIIFileNamesInZip}

If your add-on includes files which contain non-ASCII (non-English) characters, you should create the zip archive such that it uses UTF-8 file names.
This means that these files can be extracted properly on all systems, regardless of the system's configured language.
Unfortunately, many zip archivers do not support this, including Windows Explorer.
Generally, it has to be explicitly enabled even in archivers that do support it.
[7-Zip](http://www.7-zip.org/) supports this, though it must be enabled by specifying the "cu=on" method parameter.

### Manifest Files {#manifest}

Each add-on package must contain a manifest file named manifest.ini.
This must be a UTF-8 encoded text file.
This manifest file contains key = value pairs declaring info such as the add-on's name, version and description.

#### Available Fields {#manifestFields}

Although it is highly suggested that manifests contain all fields, the fields marked as mandatory must be included.
Otherwise, the add-on will not install.

* name (string, required): A short, unique, name for the add-on.
  * The recommended convention is lowerCamelCase.
  * This is used to differentiate add-ons internally, and is also used as the name of the add-on's directory in the user configuration directory.
  * Special characters should be avoided as the add-on name will be used as a folder name.
  Expected characters are alphanumeric, space, underscore and hyphen.
* summary (string, required): The name of the add-on as shown to the user.
* version (string, required): The version of this add-on; e.g. 2.0.1.
When uploading to the Add-on Store certain requirements apply:
  * Using `<major>.<minor>` or `<major>.<minor>.<patch>` format.
  * For a user to be able to update to this add-on, the version must be greater than the last version uploaded.
  * Add-on versions are expected to be unique for the addon name and channel, meaning that a beta, stable and dev version of the same add-on cannot share a version number.
  This is so there can be a unique ordering of newest to oldest.
  * The suggested convention is to increment the patch version number for dev versions, increment the minor version number for beta versions, and increment the major version number for stable versions.
* author (string, required): The author of this add-on, preferably in the form Full Name <email address>; e.g. Michael Curran <<mick@example.com>>.
* description (string): A sentence or two describing what the add-on does.
* url (string): A URL where this add-on, further info and upgrades can be found.
  * Starting the URL with `https://` is required for submitting to the Add-on Store.
* docFileName (string): The name of the main documentation file for this add-on; e.g. readme.html. See the [Add-on Documentation](#AddonDoc) section for more details.
* minimumNVDAVersion (string, required): The minimum required version of NVDA for this add-on to be installed or enabled.
  * e.g "2021.1"
  * Must be a three part version string i.e. Year.Major.Minor, or a two part version string of Year.Major.
  In the second case, Minor defaults to 0.
  * Defaults to "0.0.0"
  * Must be less than or equal to `lastTestedNVDAVersion`
  * This must match a valid API version to be submitted to the Add-on Store.
  Valid API versions are found [on GitHub](https://github.com/nvaccess/addon-datastore-transform/blob/main/nvdaAPIVersions.json).
* lastTestedNVDAVersion (string, required): The last version of NVDA this add-on has been tested with.
  * e.g "2022.3.3"
  * Must be a three part version string i.e. Year.Major.Minor, or a two part version string of Year.Major.
  In the second case, Minor defaults to 0.
  * Defaults to "0.0.0"
  * Must be greater than or equal to `minimumNVDAVersion`
  * This must match a valid API version to be submitted to the Add-on Store.
  Valid API versions are found [on GitHub](https://github.com/nvaccess/addon-datastore-transform/blob/main/nvdaAPIVersions.json).

All string values must be enclosed in quotes as shown in the example below.

The lastTestedNVDAVersion field in particular is used to ensure that users can be confident about installing an add-on.
It allows the add-on author to make an assurance that the add-on will not cause instability, or break the users system.
When this is not provided, or is less than the current version of NVDA (ignoring minor point updates e.g. 2018.3.1) then the user will be warned not to install the add-on.

The manifest can also specify information regarding any additional speech symbol dictionaries or braille translation tables provided by the add-on.
Please refer to the [speech symbol dictionaries](#AddonSymbolDictionaries) and [braille translation tables](#BrailleTables) sections.

#### An Example Manifest File {#manifestExample}

```ini
name = "myTestAddon"
summary = "Cool Test Add-on"
version = "1.0.0"
description = "An example add-on showing how to create add-ons!"
author = "Michael Curran <mick@example.com>"
url = "https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/addons.md"
docFileName = "readme.html"
minimumNVDAVersion = "2021.1"
lastTestedNVDAVersion = "2022.3.3"
```

### Plugins and Drivers {#pluginsAndDrivers}

The following plugins and drivers can be included in an add-on:

* App modules: Place them in an `appModules` directory in the archive.
* Braille display drivers: Place them in a `brailleDisplayDrivers` directory in the archive.
* Global plugins: Place them in a `globalPlugins` directory in the archive.
* Synthesizer drivers: Place them in a `synthDrivers` directory in the archive.
* [Speech symbol dictionaries](#AddonSymbolDictionaries): Place them in the directory for one or more [locales](#localizingAddons) with a file name of `symbols-<name>.dic`, e.g. `locale\en\symbols-greek.dic`.
* [Braille translation tables](#BrailleTables): Place them in a `brailleTables` directory in the archive.

### Optional install / Uninstall code {#installUninstallCode}

If you need to execute code as your add-on is being installed or uninstalled from NVDA (e.g. to validate license information or to copy files to a custom location), you can provide a Python file called `installTasks.py` in the archive which contains special functions that NVDA will call while installing or uninstalling your add-on.
This file should avoid loading any modules that are not absolutely necessary, especially Python C extensions or dlls from your own add-on, as this could cause later removal of the add-on to fail.
However, if this does happen, the add-on directory will be renamed and then deleted after the next restart of NVDA.
Finally, it should not depend on the existence or state of other add-ons, as they may not be installed, may have already been removed or may not yet be initialized.

#### the onInstall function {#onInstall}

NVDA will look for and execute an `onInstall` function in `installTasks.py` after it has finished extracting the add-on into NVDA.
Note that although the add-on will have been extracted at this point, its directory will have a `.pendingInstall` suffix until NVDA is restarted, the directory is renamed and the add-on is really loaded for the first time.
If this function raises an exception, the installation of the add-on will fail and its directory will be cleaned up.

#### The onUninstall Function {#onUninstall}

NVDA will look for and execute an `onUninstall` function in `installTasks.py` when NVDA is restarted after the user has chosen to remove the add-on.
After this function completes, the add-on's directory will automatically be removed.
As this happens on NVDA startup before other components are initialized, this function cannot request input from the user.

### Localizing Add-ons {#localizingAddons}

It is possible to provide locale-specific information and messages for your add-on.
Locale information can be stored in a locale directory in the archive.
This directory should contain directories for each language it supports, using the same language code format as the rest of NVDA; e.g. en for English, fr_CA for French Canadian.

#### Locale-specific Manifest Files {#localeManifest}

Each of these language directories can contain a locale-specific manifest file called manifest.ini, which can contain a small subset of the manifest fields for translation.
These fields are `summary` and `description`.
You can also override the `displayName` field for speech symbol dictionaries and braille translation tables.
All other fields will be ignored.

#### Locale-specific Messages {#localeMessages}

Each language directory can also contain gettext information, which is the system used to translate the rest of NVDA's user interface and reported messages.
As with the rest of NVDA, an `nvda.mo` compiled gettext database file should be placed in the `LC_MESSAGES` directory within this directory.
To allow plugins in your add-on to access gettext message information via calls to `_()`, `ngettext()`, `npgettext()` and `pgettext()` you must initialize translations at the top of each Python module by calling `addonHandler.initTranslation()`.
This function cannot be called in modules that do not belong to an add-on, e.g. in a scratchpad subdirectory.
For more information about gettext and NVDA translation in general, please read the [Translating NVDA page](https://github.com/nvaccess/nvda/blob/master/projectDocs/translating/readme.md)

#### Speech symbol dictionaries {#AddonSymbolDictionaries}

You can provide custom speech symbol dictionaries in add-ons to improve symbol pronunciation.
The process to create custom speech symbol dictionaries is very similar to that of the [translation process of existing symbols](#symbolPronunciation).
Note that [complex symbols](#complexSymbols) are not supported.

Custom dictionaries must be placed in a language directory and have a filename in the form `symbols-<name>.dic`, where `<name>` is the name that has to be provided in the add-ons manifest.
All locales implicitly inherit the symbol information for English, though any of this information can be overridden for specific locales.

When adding a dictionary not marked as mandatory, some information must be provided such as its display name, since it should be shown in the speech category of the settings dialog.
A dictionary can also be marked mandatory, in which case it is always enabled with the add-on.
When an add-on ships with dictionaries, this information is included in its manifest in the optional `symbolDictionaries` section.
For example:

```ini
[symbolDictionaries]
[[greek]]
displayName = Greek
mandatory = false

[[hebrew]]
displayName = Biblical Hebrew
mandatory = true
```

In the above example, `greek` is a dictionary that is optional and will be listed in the speech category of NVDA's settings dialog under the "Extra dictionaries for character and symbol processing" setting.
Its file will be stored as `locale\en\symbols-greek.dic`, whereas French translations of the symbols are stored in `locale\fr\symbols-greek.dic`.
When using NVDA in French, symbols that aren't defined in the French dictionary inherit the symbol information for English.

Also in the example, the `hebrew` dictionary is marked mandatory and will therefore always be enabled as long as the add-on is active.
Its file will be stored as `locale\en\symbols-hebrew.dic`, whereas French translations of the symbols are stored in `locale\fr\symbols-hebrew.dic`.

Note that for the display name of the dictionary to be translated, an entry should be added to a [locale manifest](#localeManifest).
For example, add the following to `locale\fr\manifest.ini`:

```ini
[symbolDictionaries]
[[hebrew]]
displayName = Hébreu Biblique
```

### Add-on Documentation {#AddonDoc}

Documentation for an add-on should be placed in the `doc` directory in the archive.
Similar to the `locale` directory, this directory should contain directories for each language in which documentation is available.

Users can access documentation for a particular add-on by opening the Add-on Store, selecting the add-on and pressing the Add-on help button.
This will open the file named in the docFileName parameter of the manifest.
NVDA will search for this file in the appropriate language directories.
For example, if docFileName is set to readme.html and the user is using English, NVDA will open doc\en\readme.html.

### Braille translation tables {#BrailleTables}

Although NVDA ships with more than a hundred braille translation tables provided by [the liblouis project](https://liblouis.io/) aimed at fitting most needs, it also supports the addition of custom tables.
Custom tables must be placed in the brailleTables directory of an add-on or subdirectory of the scratchpad directory.
These tables can either replace standard tables shipped with NVDA or be completely new ones.

When adding a table, some information must be provided such as its display name in the Preferences dialog, whether it supports input and/or output and whether it is for contracted braille.
When an add-on ships with tables, this information is included in its manifest in the optional brailleTables section.
For example:

```
[brailleTables]
[[fr-bfu-tabmod-comp8.utb]]
displayName = French (unified) 8 dot computer braille - Addition
contracted = False
output = True
input = True

[[no-no-8dot.utb]]
displayName = Norwegian 8 dot computer braille - Replacement
contracted = False
output = True
input = True
```

In the above example, `fr-bfu-tabmod-comp8.utb` is a new table, while `no-no-8dot.utb` replaces a table that is already included in NVDA.
Both tables need to be shipped in the brailleTables directory of the add-on.
It is also possible to include a table in the manifest that is shipped with NVDA but otherwise unavailable for selection in the Preferences dialog.
In that case, the table does not need to be shipped in the add-on's brailleTables directory.

Providing a custom table, whether it has the same file name as a standard table or a different name, thus requires you to define the table in the add-on's manifest.
The only exception to this rule applies to tables that are included within other tables.
While they don't have to be included in the manifest of the add-on, they can only be included from other tables that are part of the same add-on.

Note that for the display name of the table to be translated, an entry should be added to a [locale manifest](#localeManifest).
For example, add the following to `locale\fr\manifest.ini`:

```ini
[brailleTables]
[[no-no-8dot.utb]]
displayName = Norvégien Braille informatique 8 points - Remplacement
```

Custom tables can also be placed in the brailleTables subdirectory of the scratchpad directory.
In this case, the table metadata can be placed in a `manifest.ini` file in the root of the scratchpad in the exact same format as the example above.
Basically, this means that, whether using an add-on or the scratchpad, the requirements and implementation steps are equal.
Note that a `manifest.ini` file in the scratchpad is only parsed for braille table metadata.
Other add-on metadata in the file is ignored.

Please refer to the [liblouis documentation](https://liblouis.io/documentation/) for detailed information regarding the braille translation tables format.

## NVDA Python Console {#PythonConsole}

The NVDA Python console emulates the interactive Python interpreter from within NVDA.
It is a development tool which is useful for debugging, general inspection of NVDA internals or inspection of the accessibility hierarchy of an application.

### Usage {#pythonConsoleUsage}

The console can be activated in two ways:

* By pressing NVDA+control+z.
If activated in this fashion, a snapshot of the current state of NVDA at the time the key was pressed will be taken and saved in certain variables available in the console.
See [Snapshot Variables](#PythonConsoleSnapshotVariables) for more details.
* By selecting Tools -> Python console from the NVDA system tray menu.

The console is similar to the standard interactive Python interpreter.
Input is accepted one line at a time and processed when enter is pressed.
Multiple lines can be pasted at once from the clipboard and will be processed one by one.
You can navigate through the history of previously entered lines using the up and down arrow keys.

Output (responses from the interpreter) will be spoken when enter is pressed.
The f6 key toggles between the input and output controls.
When on the output control, alt+up/down jumps to the previous/next result (add shift for selecting).
Pressing control+l clears the output.

The result of the last executed command is stored in the "_" global variable.
This shadows the gettext function which is stored as a built-in with the same name.
It can be unshadowed by executing "del _" and avoided altogether by executing "_ = _".

Closing the console window (with escape or alt+F4) simply hides it.
This allows the user to return to the session as it was left when it was closed, including history and variables.

### Namespace {#PythonConsoleNamespace}
#### Automatic Imports {#pythonConsoleAutoImports}

For convenience, the following modules and variables are automatically imported in the console:
sys, os, wx, log (from logHandler), api, queueHandler, config, controlTypes, textInfos, braille, speech, vision, appModules, globalPlugins

See: pythonConsole.PythonConsole.initNamespace

#### Snapshot Variables {#PythonConsoleSnapshotVariables}

Whenever NVDA+control+z is pressed, certain variables available in the console will be assigned according to the current state of NVDA.
These variables are:

* `focus`: The current focus object
* `focusAnc`: The ancestors of the current focus object
* `fdl`: Focus difference level; i.e. the level at which the ancestors for the current and previous focus differ
* `fg`: The current foreground object
* `nav`: The current navigator object
* `caretObj`: The object which contains the caret (focus or tree interceptor if any)
* `caretPos`: A text info at the position of the caret
* `review`: The current `TextInfo` instance representing the user's review position
* `mouse`: The current mouse object
* `brlRegions`: The braille regions from the active braille buffer

### Tab completion {#pythonConsoleTab}

The input control supports tab-completion of variables and member attribute names.
Hit the tab key once to complete the current input if there is one single candidate.
If there is more than one, hit the tab key a second time to open a menu listing all matching possibilities.
By default, only "public" member attributes are listed.
That is, if the input is "nav.", attribute names with no leading underscore are proposed.
If the input is "nav._", attribute names with a single leading underscore are proposed.
Similarly, if the input is "nav.__", attribute names with two leading underscores are proposed.

## Remote Python Console {#remotePythonConsole}

A remote Python console is available in source builds of NVDA, for situations where remote debugging of NVDA is useful.
It is similar to the [local Python console](#PythonConsole) discussed above, but is accessed via TCP.

Please be aware that this is a huge security risk.
It is not available in binary builds distributed by NV Access, and You should only enable it if you are connected to trusted networks.

### Usage {#remotePythonConsoleUsage}

To enable the remote Python console, use the local Python console to import remotePythonConsole and call remotePythonConsole.initialize().
You can then connect to it via TCP port 6832.

History of previously entered lines is not supported.

The namespace is the same as [the namespace in the local Python console](#PythonConsoleNamespace).

There are some special functions:

* snap(): Takes a snapshot of the current state of NVDA and saves it in the [snapshot variables](#PythonConsoleSnapshotVariables).
* rmSnap(): Removes all snapshot variables.

## Extension Points {#ExtensionPoints}

NVDA's `extensionPoints` module allows code in different parts of NVDA, or in add-ons, to perform tasks such as:

* Be notified when an action occurs or a state is changed.
* Receive, as part of being notified, variables related to the action or changed state.
* Cancel or alter an action NVDA was going to take, based upon certain conditions.
* Modify data that NVDA is using (such as changing speech sequences or braille, before they are spoken or brailled).
* Delay something NVDA is doing, while intervening operations are performed.

There are five kinds of extension point:

| Type |Purpose|
|---|---|
|`Action` |Allows some code to find out what other code is doing. For example, an add-on can be notified before or after a config profile changes.|
|`Filter` |Edits data. A filter registered in the speech module, might allow changing speech strings before they are spoken.|
|`Decider` |Runs each registered handler until one of them returns `False`. If one does, it can be used to prevent the invoking code from running.|
|`AccumulatingDecider` |Like `Decider`, but always runs all of its registered handlers, and only decides if one of them failed at the end. The expected result of each is `True` by default, though expecting `False` is possible.|
|`Chain` |Allows registering handlers that return iterables (mainly generators). Calling `iter` on the `Chain` returns a generator that iterates over all the handlers.|

The sections below provide the list of currently defined extension points in NVDA, along with brief descriptions for them.
Please see code documentation in the associated files, or the code itself, for further explanation.
The section titles below represent the package or module in which the listed extension points are defined.

For examples of how to define and use new extension points, please see the code documentation of the `extensionPoints` package.

### braille {#brailleExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Filter` |`filter_displaySize` | [Deprecated] Allows components or add-ons to change the display size used for braille output.|
|`Filter` |`filter_displayDimensions` | Allows components or add-ons to change the number of rows and columns of the display used for braille output.|
|`Action` |`displaySizeChanged` |Notifies of display size changes.|
|`Action` |`pre_writeCells` |Notifies when cells are about to be written to a braille display|
|`Action` |`displayChanged` |Notifies of braille display changes.|
|`Decider` |`decide_enabled` |Allows deciding whether the braille handler should be forcefully disabled.|

### appModuleHandler {#appModuleHandlerExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`post_appSwitch` |Triggered when the foreground application changes|

### addonHandler {#addonHandlerExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`AccumulatingDecider` |`isCLIParamKnown` |Allows adding NVDA commandline parameters which apply to plugins. See [this section of the Dev Guide](#PluginCLIArgs) for more information.|

### brailleViewer {#brailleViewerExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`postBrailleViewerToolToggledAction` |Triggered every time the Braille Viewer is created / shown or hidden / destroyed.|

### config {#configExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`post_configProfileSwitch` |Notifies after the configuration profile has been switched.|
|`Action` |`pre_configSave` |Notifies before NVDA's configuration is saved to disk.|
|`Action` |`post_configSave` |Notifies after NVDA's configuration has been saved to disk.|
|`Action` |`pre_configReset` |Notifies before configuration is reloaded from disk or factory defaults are applied.|
|`Action` |`post_configReset` |Notifies after configuration has been reloaded from disk or factory defaults were applied.|

### core {#coreExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`postNvdaStartup` |Notifies after NVDA has finished starting up.|

### inputCore {#inputCoreExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Decider` |`decide_handleRawKey` |Notifies when a raw keyboard event is received, before any NVDA processing, allowing other code to decide if it should be handled.|
|`Decider` |`decide_executeGesture` |Notifies when a gesture is about to be executed, allowing other code to decide if it should be.|

### logHandler {#logHandlerExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`_onErrorSoundRequested` |Triggered every time an error sound needs to be played. This extension point should not be used directly but retrieved calling `getOnErrorSoundRequested()` instead.|

### nvwave {#nvwaveExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Decider` |`decide_playWaveFile` |Notifies when a wave file is about to be played, allowing other code to decide if it should be.|

### speech {#speechExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`speechCanceled` |Triggered when speech is canceled.|
|`Action` |`pre_speechCanceled` |Triggered before speech is canceled.|
|`Action` |`pre_speech` |Triggered before NVDA handles prepared speech.|
|`Action` |`post_speechPaused` |Triggered when speech is paused or resumed.|
|`Action` |`pre_speechQueued` |Triggered after speech is processed and normalized and directly before it is enqueued.|
|`Filter` |`filter_speechSequence` |Allows components or add-ons to filter speech sequence before it passes to the synth driver.|

### synthDriverHandler {#synthDriverHandlerExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`synthIndexReached` |Notifies when a synthesizer reaches an index during speech.|
|`Action` |`synthDoneSpeaking` |Notifies when a synthesizer finishes speaking.|
|`Action` |`synthChanged` |Notifies of synthesizer changes.|
|`Action` |`pre_synthSpeak` |Notifies when the current synthesizer is about to speak something.|

### tones {#tonesExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Decider` |`decide_beep` |Notifies when a beep is about to be generated and played, allowing a component to decide whether it should be.|

### treeInterceptorHandler {#treeInterceptorHandlerExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`post_browseModeStateChange` |Notifies when browse mode state changes.|

### utils.security {#utils_securityExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`post_sessionLockStateChanged` |Notifies when a session lock or unlock event occurs.|

### winAPI.messageWindow {#winAPI_messageWindowExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`pre_handleWindowMessage` |Notifies when NVDA receives a window message, allowing components to perform an action when certain system events occur.|

### winAPI.secureDesktop {#winAPI_secureDesktopExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Action` |`winAPI.secureDesktop.post_secureDesktopStateChange` |Notifies when the user has switched to/from the secure desktop|

### bdDetect {#bdDetectExtPts}

| Type |Extension Point |Description|
|---|---|---|
|`Chain` |`scanForDevices` |Can be iterated to scan for braille devices.|

### vision.visionHandlerExtensionPoints.EventExtensionPoints {#visionExtPts}

These extension points are expected to be used and registered to differently than other extension points.
Please see the `EventExtensionPoints` class documentation for more information, and detailed descriptions.

| Type |Extension Point |Notifies a vision enhancement provider when ...|
|---|---|---|
|`Action` |`post_objectUpdate` |an object property has changed.|
|`Action` |`post_focusChange` |the focused NVDAObject has changed.|
|`Action` |`post_foregroundChange` |the foreground NVDAObject has changed.|
|`Action` |`post_caretMove` |a physical caret has moved.|
|`Action` |`post_browseModeMove` |a virtual caret has moved.|
|`Action` |`post_reviewMove` |the position of the review cursor has changed.|
|`Action` |`post_mouseMove` |the mouse has moved.|
|`Action` |`post_coreCycle` |the end of each core cycle has been reached.|

## Communicating with the user

### The message dialog API

The message dialog API provides a flexible way of presenting interactive messages to the user.
The messages are highly customisable, with options to change icons and sounds, button labels, return values, and close behaviour, as well as to attach your own callbacks.

All classes that make up the message dialog API are importable from `gui.message`.
While you are unlikely to need all of them, they are enumerated below:

* `ReturnCode`: Possible return codes from modal `MessageDialog`s.
* `EscapeCode`: Escape behaviour of `MessageDialog`s.
* `DialogType`: Types of dialogs (sets the dialog's sound and icon).
* `Button`: Button configuration data structure.
* `DefaultButton`: Enumeration of pre-configured buttons.
* `DefaultButtonSet`: Enumeration of common combinations of buttons.
* `MessageDialog`: The actual dialog class.

In many simple cases, you will be able to achieve what you need by simply creating a message dialog and calling `Show` or `ShowModal`. For example:

```py
from gui.message import MessageDialog
from gui import mainFrame

MessageDialog(
	mainFrame,
	_("Hello world!"),
).Show()
```

This will show a non-modal (that is, non-blocking) dialog with the text "Hello world!" and an OK button.

If you want the dialog to be modal (that is, to block the user from performing other actions in NVDA until they have responded to it), you can call `ShowModal` instead.

With modal dialogs, the easiest way to respond to user input is via the return code.

```py
from gui.message import DefaultButtonSet, ReturnCode

saveDialog = MessageDialog(
	mainFrame,
	_("Would you like to save your changes before exiting?"),
	_("Save changes?"),
	buttons=DefaultButtonSet.SAVE_NO_CANCEL
)

match saveDialog.ShowModal():
	case ReturnCode.SAVE:
		...  # Save the changes and close
	case ReturnCode.NO:
		...  # Discard changes and close
	case ReturnCode.CANCEL:
		...  # Do not close
```

For non-modal dialogs, the easiest way to respond to the user pressing a button is via callback methods.

```py
from gui.message import Payload

def readChangelog(payload: Payload):
	...  # Do something

def downloadUpdate(payload: Payload):
	...  # Do something

def remindLater(payload: Payload):
	...  # Do something

updateDialog = MessageDialog(
	mainFrame,
	"An update is available. "
	"Would you like to download it now?",
	"Update",
	buttons=None,
).addYesButton(
	callback=downloadUpdate
).addNoButton(
	label=_("&Remind me later"),
	fallbackAction=True,
	callback=remindLater
).addHelpButton(
	label=_("What's &new"),
	callback=readChangelog
)

updateDialog.Show()
```

You can set many of the parameters to `addButton` later, too:

* The default focus can be set by calling `setDefaultFocus` on your message dialog instance, and passing it the ID of the button to make the default focus.
* The fallback action can be set later by calling `setFallbackAction` or `SetEscapeId` with the ID of the button which performs the fallback action.
* The button's label can be changed by calling `setButtonLabel` with the ID of the button and the new label.

#### Fallback actions

The fallback action is the action performed when the dialog is closed without the user pressing one of the buttons you added to the dialog.
This can happen for several reasons:

* The user pressed `esc` or `alt+f4` to close the dialog.
* The user used the title bar close button or system menu close item to close the dialog.
* The user closed the dialog from the Task View, Taskbar or App Switcher.
* The user is quitting NVDA.
* Some other part of NVDA or an add-on has asked the dialog to close.

By default, the fallback action is set to `EscapeCode.CANCEL_OR_AFFIRMATIVE`.
This means that the fallback action will be the cancel button if there is one, the button whose ID is `dialog.GetAffirmativeId()` (`ReturnCode.OK`, by default), or `None` if no button with either ID exists in the dialog.
You can use `dialog.SetAffirmativeId(id)` to change the ID of the button used secondarily to Cancel, if you like.
The fallback action can also be set to `EscapeCode.NO_FALLBACK` to disable closing the dialog like this entirely.
If it is set to any other value, the value must be the id of a button to use as the default action.

In some cases, the dialog may be forced to close.
If the dialog is shown modally, a calculated fallback action will be used if the fallback action is `EscapeCode.NO_FALLBACK` or not found.
The order of precedence for calculating the fallback when a dialog is forced to close is as follows:

1. The developer-set fallback action.
2. The developer-set default focus.
3. The first button added to the dialog that closes the dialog.
4. The first button added to the dialog, regardless of whether it closes the dialog.
5. A dummy action that does nothing but close the dialog.
   In this case, and only this case, the return code from showing the dialog modally will be `EscapeCode.NO_FALLBACK`.

#### A note on threading

**IMPORTANT:** Most `MessageDialog` methods are **not** thread safe.
Calling these methods from non-GUI threads can cause crashes or unpredictable behavior.

When calling non thread safe methods on `MessageDialog` or its instances, be sure to do so on the GUI thread.
To do this with wxPython, you can use `wx.CallAfter` or  `wx.CallLater`.
As these operations schedule the passed callable to occur on the GUI thread, they will return immediately, and will not return the return value of the passed callable.
If you want to wait until the callable has completed, or care about its return value, consider using `gui.guiHelper.wxCallOnMain`.

The `wxCallOnMain` function executes the callable you pass to it, along with any positional and keyword arguments, on the GUI thread.
It blocks the calling thread until the passed callable returns or raises an exception, at which point it returns the returned value, or re-raises the raised exception.

```py
# To call
someFunction(arg1, arg2, kw1=value1, kw2=value2)
# on the GUI thread:
wxCallOnMain(someFunction, arg1, arg2, kw=value1, kw2=value2)
```

In fact, you cannot create, initialise, or show (modally or non-modally) `MessageDialog`s from any thread other than the GUI thread.

#### Buttons

You can add buttons in a number of ways:

* By passing a `Collection` of `Button`s to the `buttons` keyword-only parameter to `MessageDialog` when initialising.
* By calling `addButton` on a `MessageDialog` instance, either with a `Button` instance, or with simple parameters.
  * When calling `addButton` with a `Button` instance, you can override all of its parameters except `id` by providing their values as keyword arguments.
  * When calling `addButton` with simple parameters, the parameters it accepts are the same as those of `Button`.
  * In both cases, `id` or `button` is the first argument, and is positional only.
* By calling `addButtons` with a `Collection` of `Button`s.
* By calling any of the add button helpers.

Regardless of how you add them, you cannot add multiple buttons with the same ID to the same `MessageDialog`.

A `Button` is an immutable data structure containing all of the information needed to add a button to a `MessageDialog`.
Its fields are as follows:

| Field | Type | Default | Explanation |
|---|---|---|---|
| `id` | `ReturnCode` | No default | The ID used to refer to the button. |
| `label` | `str` | No default | The text label to display on the button. Prefix accelerator keys with an ampersand (&). |
| `callback` | `Callable` or `None` | `None` | The function to call when the button is clicked. This is most useful for non-modal dialogs. |
| `defaultFocus` | `bool` | `False` | Whether to explicitly set the button as the default focus. (1) |
| `fallbackAction` | `bool` | `False` | Whether the button should be the fallback action, which is called when the user presses `esc`, uses the system menu or title bar close buttons, or the dialog is asked to close programmatically. (2) |
| `closesDialog` | `bool` | `True` | Whether the button should close the dialog when pressed. (3) |
| `returnCode` | `ReturnCode` or `None` | `None` | Value to return when a modal dialog is closed. If `None`, the button's ID will be used. |

1. Setting `defaultFocus` only overrides the default focus:

  * If no buttons have this property, the first button will be the default focus.
  * If multiple buttons have this property, the last one will be the default focus.

2. `fallbackAction` only sets whether to override the fallback action:

  * This button will still be the fallback action if the dialog's fallback action is set to `EscapeCode.CANCEL_OR_AFFIRMATIVE` (the default) and its ID is `ReturnCode.CANCEL` (or whatever the value of `GetAffirmativeId()` is (`ReturnCode.OK`, by default), if there is no button with `id=ReturnCode.CANCEL`), even if it is added with `fallbackAction=False`.
    To set a dialog to have no fallback action, use `setFallbackAction(EscapeCode.NO_FALLBACK)`.
  * If multiple buttons have this property, the last one will be the fallback action.

3. Buttons with `fallbackAction=True` and `closesDialog=False` are not supported:

  * When adding a button with `fallbackAction=True` and `closesDialog=False`, `closesDialog` will be set to `True`.
  * If you attempt to call `setFallbackAction` with the ID of a button that does not close the dialog, `ValueError` will be raised.

A number of pre-configured buttons are available for you to use from the `DefaultButton` enumeration, complete with pre-translated labels.
None of these buttons will explicitly set themselves as the fallback action.
You can also add any of these buttons to an existing `MessageDialog` instance with its add button helper, which also allows you to override all but the `id` parameter.
The following default buttons are available:

| Button | Label | ID/return code | Closes dialog | Add button helper |
|---|---|---|---|---|
| `APPLY` | &Apply | `ReturnCode.APPLY` | No | `addApplyButton` |
| `CANCEL` | Cancel | `ReturnCode.CANCEL` | Yes | `addCancelButton` |
| `CLOSE` | Close | `ReturnCode.CLOSE` | Yes | `addCloseButton` |
| `HELP` | Help | `ReturnCode.HELP` | No | `addHelpButton` |
| `NO` | &No | `ReturnCode.NO` | Yes | `addNoButton` |
| `OK` | OK | `ReturnCode.OK` | Yes | `addOkButton` |
| `SAVE` | &Save | `ReturnCode.SAVE` | Yes | `addSaveButton` |
| `YES` | &Yes | `ReturnCode.YES` | Yes | `addYesButton` |

As you usually want more than one button on a dialog, there are also a number of pre-defined sets of buttons available as members of the `DefaultButtonSet` enumeration.
All of them comprise members of `DefaultButton`.
You can also add any of these default button sets to an existing `MessageDialog` with one of its add buttons helpers.
The following default button sets are available:

| Button set | Contains | Add button set helper | Notes |
|---|---|---|---|
| `OK_CANCEL` | `DefaultButton.OK` and `DefaultButton.Cancel` | `addOkCancelButtons` | |
| `YES_NO` | `DefaultButton.YES` and `DefaultButton.NO` | `addYesNoButtons` | You must set a fallback action if you want the user to be able to press escape to close a dialog with only these buttons. |
| `YES_NO_CANCEL` | `DefaultButton.YES`, `DefaultButton.NO` and `DefaultButton.CANCEL` | `addYesNoCancelButtons` | |
| `SAVE_NO_CANCEL` | `DefaultButton.SAVE`, `DefaultButton.NO`, `DefaultButton.CANCEL` | `addSaveNoCancelButtons` | The label of the no button is overridden to be "Do&n't save". |

If none of the standard `ReturnCode` values are suitable for your button, you may also use `ReturnCode.CUSTOM_1` through `ReturnCode.CUSTOM_5`, which will not conflict with any built-in identifiers.

#### Callbacks

A convenient way of responding to button presses, especially for non-modal message dialogs, is to attach callbacks to the buttons.
This is achieved by passing a `callback` function to `addButton`, `addButtons`, or any of the add button helpers.

A callback should be a function which accepts exactly one positional argument.
When called, a `Payload` data structure will be passed in.
This data structure currently contains no information, though in future it may be augmented to contain information about the dialog's state and the context from which the callback was called.

#### Convenience methods

The `MessageDialog` class also provides a number of convenience methods for showing common types of modal dialogs.
Each of them requires a message string, and optionally a title string and parent window.
They all also support overriding the labels on their buttons via keyword arguments.
They are all thread safe.
The following convenience class methods are provided (keyword arguments for overriding button labels indicated in parentheses):

| Method | Buttons | Return values |
|---|---|---|
| `alert` | OK (`okLabel`) | `None` |
| `confirm` | OK (`okLabel`) and Cancel (`cancelLabel`) | `ReturnCode.OK` or `ReturnCode.CANCEL` |
| `ask` | Yes (`yesLabel`), No (`noLabel`) and Cancel (`cancelLabel`) | `ReturnCode.YES`, `ReturnCode.NO` or `ReturnCode.CANCEL` |
