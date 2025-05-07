# Design Overview

This article attempts to provide an overview of NVDA's technical design and architecture.
It is necessarily technical in nature.
You should have a reasonable knowledge of programming and object oriented programming concepts in particular, as well as at least a basic knowledge of Python, before attempting to understand NVDA's design.
Please see the code documentation for the relevant classes for more information.

## Terminology

### Abbreviations
 * API: Application programming interface
 * GUI: Graphical user interface

### Definitions
 * Caret: The system cursor; i.e.
the cursor generally moved when you use the normal cursor keys.
 * Script: A function which is executed in response to input from the user such  as key presses from the keyboard, manipulating braille display controls and taps on touchscreens.
Also known as a command.
 * Widget: An individual component in a GUI with which a user can interact;
 e.g. a button, an editable text field, a list box, etc.
Also known as a control or object.

## General

### Programming Languages
NVDA is primarily written in the [Python programming language](http://www.python.org/), which allows for rapid development among other benefits.
Code that needs to be [injected into other processes](#in-process-code) is written in C++ for high performance.

### Accessibility APIs
In order to make graphical widgets accessible to assistive technologies, operating systems and applications can use special purpose accessibility APIs.
These APIs provide information about the widget such as its name, type/role (button, check box, editable text field, etc.), description, value, states (checked, unavailable, invisible, etc.) and keyboard shortcut.
Accessibility APIs also provide events to allow assistive technologies to monitor changes, such as when the focus changes, properties of an object (such as name, description, value, and state) change, etc.
Rich accessibility APIs provide additional information, including the ability to access detailed information about and track the cursor in editable text controls, and table information such as row and column coordinates.
NVDA relies heavily on accessibility APIs to gather information.
Several accessibility APIs are used, including Microsoft Active Accessibility (MSAA) (also known as IAccessible), [IAccessible2](http://www.linuxfoundation.org/en/Accessibility/IAccessible2), Java Access Bridge and UI Automation.

**Note:** IAccessible2 was not created by Microsoft, see [Wikipedia for more background](https://en.wikipedia.org/wiki/IAccessible2).

See also:
- [Stack Overflow: "What is the difference between IAccessible, IAccessible2, UIAutomation and MSAA?"](https://stackoverflow.com/a/55130227)
- [The Linux Foundation IA2 reference](https://accessibility.linuxfoundation.org/a11yspecs/ia2/docs/html/)
- [IA2 event constants](https://accessibility.linuxfoundation.org/a11yspecs/ia2/docs/html/_accessible_event_i_d_8idl.html)
  - From the perspective of Windows, the IA2 event constants are considered custom "application specific" event IDs.
- [IA2 Project (IDL files)](https://github.com/LinuxA11y/IAccessible2)
- [Windows event constants](https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants)


#### Tools for investigating Accessibility APIs

- Using [NVDA Object Navigation](https://download.nvaccess.org/documentation/userGuide.html#ObjectNavigation) and [logging developer information](https://download.nvaccess.org/documentation/userGuide.html#LogViewer).
- [Accessibility Viewer (aViewer)](https://github.com/ThePacielloGroup/aviewer/)
	- handles MSAA, IA2, UIA but can be a bit buggy
	- tends to provide user friendly display strings that make it harder to map back to raw values
- [Accessibility Insights for Windows - Accessibility Insights](https://accessibilityinsights.io/docs/en/windows/overview/#:~:text=Accessibility%20Insights%20for%20Windows%20helps%20developers%20find%20and,the%20element%20or%20setting%20keyboard%20focus%20on%20it.)
	- Good for UIA, doesn't support MSAA / IA2
- [Inspect.exe (Windows SDK)](https://docs.microsoft.com/en-us/windows/win32/winauto/inspect-objects)
	- Handles MSAA and UIA, but not IA2

### Native APIs
Some widgets do not expose sufficient information via accessibility APIs to make them fully accessible.
For example, MSAA, which is the accessibility API used by most standard Windows controls, does not provide the ability to obtain the location of the cursor or retrieve individual units of text in editable text fields.
However, some widgets provide their own native APIs (not specific to accessibility) which can be used to obtain this information.
NVDA makes use of these APIs where possible; e.g. in standard edit controls.

### Operating System Functions
Aside from accessibility and native APIs, Windows provides many functions which can be used to obtain information and perform tasks.
Information that can be obtained includes the class name of a window, the current foreground window and system battery status.
Tasks that can be performed include moving/clicking the mouse and sending key presses.

### Logging

#### Logging in secure mode
`logHandler.initialize` prevents logging in [secure mode](https://download.nvaccess.org/documentation/userGuide.html#SecureMode).
This is because it is a security concern to log during secure mode (e.g. passwords are logged on [secure screens](https://download.nvaccess.org/documentation/userGuide.html#SecureScreens).
To change this for testing, use the [serviceDebug](https://download.nvaccess.org/documentation/userGuide.html#SystemWideParameters) system wide parameter to prevent secure mode on secure screens.
When logging from a secure screen, `nvda.log` files are generated in the System profile's `%TEMP%` directory.

## NVDA Components
NVDA is built with an extensible, modular, object oriented, abstract design.
It is divided into several distinct components.

### Launcher
The launcher is the module which the user executes to start NVDA.
It is contained in the file `nvda.pyw`.
Refer to [startupShutdown documentation](./startupShutdown.md).

### Core
The core (in the function `core.main`) loads the configuration, initialises all other components and then enters the main loop.
In each iteration of the main loop, the core pumps the [API](#api-handlers) and [input](#input-handlers) handlers, [registered generators](#registered-generators) and the main queue.
All events, scripts, etc. are indirectly queued to this main queue by API and input handlers, so pumping the main queue causes these to be executed.
At the end of the iteration, the core then goes to sleep until more work is added to the main queue, at which point the core will again wake and perform another iteration.
The main loop continues to iterate / sleep until NVDA is instructed to exit either by the user or a newly started copy of NVDA.
Once NVDA is instructed to exit, the core terminates all other components, saves the configuration if appropriate and then exits.

#### Event and Script Handling
Rather than queuing scripts and events directly to the main queue, this is abstracted using the `eventHandler` and `scriptHandler` modules.
Input and API handlers use these modules to queue or directly execute scripts and events.

#### Registered Generators
Some tasks need to run in the background without causing NVDA to block (freeze) while waiting for them to complete.
They need to execute code regularly, but at no specific time interval.
NVDA allows Python generator functions to be registered for this purpose.
Once registered, the generator will be pumped once for each iteration/tick of the main loop.
Examples of this include the say all and speak spelling functionality.
They are registered using `queueHandler.registerGeneratorObject`.

### Input Handlers
The input handlers handle input from various sources.
Currently, there are three main input handler modules: `keyboardHandler`, `mouseHandler` and `touchHandler`. [Braille display drivers](#output-drivers) can also handle input.
These handlers listen for input and generate appropriate [input gestures](#input-gestures) and events.

### Input Gestures
An input gesture is an abstract representation of a single piece of input from the user; e.g. a key press.
All input gestures derive from the base `inputCore.InputGesture` class.
This allows all input to be handled in a consistent, unified way.
For example, any input gesture can be bound to any script, both in code and by the user.

### API Handlers
These handle initialisation, listening for events and termination for specific accessibility and native APIs.
They also contain utility functions useful for working with their API.
When an event is received for a widget, an appropriate [NVDA object](#nvda-objects) is fetched or constructed and an event is then queued for that NVDA object.
Together with [NVDA objects](#nvda-objects), they abstract the handling of queries and events for specific APIs so that the bulk of NVDA need not be concerned with specific APIs.
To introduce support for a new API, a developer just creates another API handler and appropriate NVDA objects without needing to change the majority of the code.
API handler modules include `IAccessibleHandler` for MSAA/IAccessible and IAccessible2, `JABHandler` for Java Access Bridge and `UIAHandler` for UI Automation.

### Output Modules
Separate modules encapsulate the handling of output functionality.
Currently, there are two main output modules: `speech` and `braille`.
There is also the `tones` module, which is used to output tones/beeps, and `nvWave` module used to play wave files indicating specific events.

### Output Drivers
Synth drivers are drivers to allow NVDA to utilise particular speech synthesisers.
They are derived from the `synthDriverHandler.SynthDriver` base class.
Braille display drivers are drivers to allow NVDA to utilise particular braille displays.
They are derived from the `braille.BrailleDisplayDriver` base class.

### NVDA Objects
An NVDA object (`NVDAObject`) is an abstract representation of a single widget in NVDA.
All NVDA objects derive from the base `NVDAObjects.NVDAObject` class.
Methods and properties are used to query information about, handle events from and execute actions on the widget represented by the NVDA object in an abstract way.
This means that the bulk of NVDA need not be concerned with specific accessibility or native APIs, but can instead work with a single, abstract representation.
This allows for the seamless support and integration of many vastly different APIs.
It is here that the full power of object oriented programming is used.
Many methods are implemented on the base `NVDAObject` class and only need to be overridden if specific functionality is required.
Similarly, if a particular widget is non-standard, problematic, provides additional information using other mechanisms, etc., it can simply subclass another NVDA object and override methods as appropriate.
NVDA objects that might be used in any application are contained in the NVDAObjects package. [App modules](#app-modules) may also define NVDA objects specific to an application.

A part from properties such as a widget's name, role, states etc, NVDA objects also include relational properties such as parent, next, previous and first child.
These allow both the user and code to navigate the entire Operating System and its applications in a tree-like structure.
The root of the tree being the Desktop, whose children is all the top-level windows for all open applications, each containing further subtrees of more widgets representing an application's user interface.

### Text Ranges
When working with editable text controls, NVDA needs to be able to obtain information about the text in the widget.
Aside from just retrieving the entire text, proper navigation requires retrieval of specific units of text (e.g. paragraphs, lines, words and characters), as well as the ability to find and set the location of the caret and selection.
Also, if the widget supports formatting, NVDA should be able to retrieve text attributes such as font name, size, bold, italic, underline and whether there is a spelling error.
Each API provides a different way of querying and manipulating text.
Just as NVDA objects provide an abstract representation of a widget, TextInfo objects provide an abstract representation of a range of text.
These objects are derived from the `textInfos.TextInfo` base class.

TextInfo objects contain properties and methods to:
* Move or expand the range by units such as character, word, line and paragraph
* compare the start and end of a range with itself or another range
* Fetch the text and formatting of the range

You can fetch a TextInfo object from an NVDA object via its `makeTextInfo` method, passing in the particular `textInfos.POSITION_*` constant depending on whether you want to fetch a range representing the position of the caret, selection, start or end of the text, or the entire text.

### Global Commands
The global commands object (`globalCommands.GlobalCommands`) contains built-in global scripts; i.e.
they can be executed everywhere.
For example, the review, report current focus and date/time scripts are all located in global commands.

### Plugins
NVDA allows third-parties to extend NVDA's functionality through plugins and add-ons.
These may define custom NVDA objects for specific applications, add global features and add support for new braille displays and speech synthesizers.
There are three plugin types: appModules, globalPlugins and drivers, with drivers further divided between speech synthesizer and braille display support.

#### App Modules
Generally, most widgets may appear in any application and an [NVDA object](#nvda-objects) should therefore be included in the main `NVDAObjects` package.
However, there are sometimes cases where a widget is implemented specifically for one application, as well as cases where a single event must be overridden or a script must be provided only in one application.
An app module provides support specific to an application for these cases.
An app module is derived from the `appModuleHandler.AppModule` base class.
App modules receive events for all [NVDA objects](#nvda-objects) in the application and can bind scripts which can be executed anywhere in that application.
They can also implement their own NVDA objects for use within the application.
Usually the App Module should be named the same as the executable for which it should be loaded.
In cases where this is problematic (one App Module should support multiple applications, the binary is named in a way which conflicts with the Python import system) you can add an entry to the `appModules.EXECUTABLE_NAMES_TO_APP_MODS` where the binary name is the key and the name of the App Module is the value.

#### Global Plugins
Aside from application specific customisation using [app modules](#app-modules), it is also possible to extend NVDA on a global level.
For example, new global commands can be added, behaviour can be changed and new GUI toolkits can be supported.
This can be done using global plugins.
A global plugin is derived from the `globalPluginHandler.GlobalPlugin` base class.
Similar to [global commands](#global-commands), they can bind scripts which can be executed everywhere.
More specifically, global plugins receive events for all [NVDA objects](#nvda-objects) in the Operating System and can bind scripts which can be executed anywhere.
They can also implement their own global [NVDA Objects](#nvda-objects).

### Tree Interceptors
Sometimes, it is necessary to intercept events and scripts for an entire hierarchy (or tree) of [NVDA objects](#nvda-objects).
For example, this is necessary to seamlessly handle complex documents which consist of many objects.
This can be done using a tree interceptor.
A tree interceptor (TreeInterceptor) is derived from the `treeInterceptorHandler.TreeInterceptor` base class.
It receives events and scripts for all [NVDA objects](#nvda-objects) beneath and including the root NVDA object of the tree interceptor.
Tree interceptors are created when a TreeInterceptor class is returned from the `treeInterceptorClass` property of an NVDA object.
Tree interceptors are used mostly for web documents, where all events and scripts for NVDA objects within a document need to be handled by the document (root NVDA object) itself.

#### Browse mode documents
Complex documents such as web pages are very often not flat; i.e. information does not simply run from top to bottom.
Because of this, complex document browsers often do not provide a way to navigate documents using the caret, and even when they do, it is often problematic.
Therefore, screen readers need to create their own flat representation of a document from the object hierarchy provided by the browser and allow the user to navigate this flat representation.
Browse mode documents are a subclass of `TreeInterceptor` that provide scripts that allow navigating the document in a linear fashion.

##### Virtual buffers
Due to the extreme slowness of performing large numbers of [out-of-process](#out-of-process-code) queries, some complex documents are accessed by NVDA by using [in-process code](#in-process-code), which collects all the content of a document in one go, and allows NVDA to search and fetch parts of this cached content on demand.
These are known as virtual buffers.
A virtual buffer (VirtualBuffer) in NVDA is derived from the `virtualBuffers.VirtualBuffer` base class and is a type of [browse mode document](##browse-mode-documents).

### GUI
NVDA has its own graphical user interface to allow for easy configuration and other user interaction.
This code is primarily contained in the `gui` package.
[wxPython](http://www.wxpython.org/) is used as the GUI toolkit.

#### Common GUI bugs

##### Controls are invisible or clipping

Adding controls to the wrong parent will cause them to visually clip or become invisible.
Adding controls to a ``wx.StaticBoxSizer`` by adding them to its parent causes undefined behaviour.
This has caused problems with users with right-to-left language locales.
wxWidgets requires that these items be added directly to the `StaticBox` associated with the `wx.StaticBoxSizer` via `GetStaticBox()`.

**Before (buggy behaviour):**

```python
sizer = new wx.StaticBoxSizer(wx.VERTICAL, parent, "Test")
sizer.Add(wx.StaticText(parent, wx.ID_ANY, "Where am I?"))
sizer.Add(wx.Button(parent, wx.ID_ADD))
```

**After:**

```python
sizer = new wx.StaticBoxSizer(wx.VERTICAL, parent, "Test")
sizer.Add(wx.StaticText(sizer.GetStaticBox(), wx.ID_ANY, "Where am I?"))
sizer.Add(wx.Button(sizer.GetStaticBox(), wx.ID_ADD))
```

PR [#12181](https://github.com/nvaccess/nvda/pull/12181) is an example of fixing this.

##### Event handlers are firing unexpectedly or failing to fire

When event handlers are firing unexpectedly or failing to fire, refer to the [wxWidgets documentation for event propagation](https://wiki.wxpython.org/EventPropagation).

Notably:
* Event handlers stop propagation.
   - If `event.Skip()` is called in an event handler, propagation will continue.
* `wx.CommandEvents`, a subset of wxEvents, will propagate up to the parent dialog by default.
   - If a child control performs an event, a parent event handler may fire.
   PR [#13117](https://github.com/nvaccess/nvda/pull/13117) is an example of a bug caused by this being fixed.

### Configuration management
NVDA includes an extensive configuration management facility including various preferences dialogs, ability to apply a given configuration in apps and so forth.
The base configuration options, as well as routines that manage configuration profiles and other management routines are housed in the `config` package, and NVDA uses [ConfigObj](http://www.voidspace.org.uk/python/configobj.html) to store configuration options.

## Special Object Functions

### Events
NVDA object, global plugin, app module and tree interceptor instances can all contain special methods which handle events for NVDA Objects.
These methods are all named beginning with "`event_`"; e.g. `event_gainFocus` and `event_nameChange`.
These events are generally executed by a call to `eventHandler.executeEvent`, which is in turn generally called resultant to events queued by [API Handlers](#api-handlers).
Most events do not take any additional arguments.
Global plugins, app modules and tree interceptors are passed a handler function which should be called if the event should be handled by the next handler;
e.g. the object itself.

Although an event is always for a particular NVDA object, it first has a chance of being handled by global plugins, app modules or tree interceptors.
If an event is handled by one of these, meaning that an `event_*` method was found and executed, the event stops there and does not go further, unless the method that handled it specifically calls the `nextHandler` function object passed to it.

The chain of handlers is as follows:
* The first found global plugin
* The next found global plugin (until no more are found)
* The app module containing the NVDA object the event is for, I.e. fetched from the NVDA object's `appModule` property.
* The tree interceptor containing the NVDA object the event is for. I.e. fetched from the NVDA object's `treeInterceptor` property if the property is not `None`
* The NVDA object itself.

### Scripts
NVDA object, global plugin, app module and tree interceptor instances can all contain special methods called scripts which are executed in response to [input gestures](#input-gestures) from the user.
These methods are all named beginning with "script_"; e.g. `script_reportCurrentFocus` and `script_dateTime`.
Script methods are passed the input gesture that triggered them.
Input gestures are bound to scripts in the class using a `scriptHandler.script` function decorator.
They can also be bound at runtime using `bindGesture`.
These are inherited from `baseObject.ScriptableObject`.

Similar to events, input gestures have a chance to be handled by a script at one of many levels.
But unlike events, once an input gesture finds and executes a script, there is no clean way to have the input gesture handled by a subsequent level.

The chain of handlers is as follows:
* The first found global plugin
* The next found global plugin (until no more are found)
* The app module containing the currently focused NVDA object, I.e. fetched from the NVDA object's `appModule` property
* The tree interceptor containing the currently focused NVDA object, I.e. fetched from the NVDA object's `treeInterceptor` property if the property is not `None`
* The currently focused NVDA object
* the first ancestor (parent) of the currently focused NVDAObject, if the found script's `canPropagate` property is `True`
* the next ancestor of the currently focused NVDAObject, if the found script's `canPropagate` property is `True`...
 * Global commands

## Inter-process Communication
In general terms, every running application or service on a computer, including NVDA, is a separate process.
No process can access data in another process except via special operating system mechanisms.
This is called inter-process communication (IPC).

### Out-of-process Code
NVDA functions primarily out-of-process.
That is, events and queries for information from other processes must be marshalled (communicated) between NVDA and the process in question using IPC.
This is many times slower than queries and events managed in the same process.
However, for the majority of screen reader functionality, this performance hit is insignificant.

### In-process Code
When large numbers of queries need to be made in one hit, working [out-of-process](#out-of-process-code) is far too slow.
A noteworthy example is rendering a web page into a flat representation, as is done by [virtual buffers](#virtual-buffers).
In these cases, code can be "injected" into the remote process.
Because this code is running in the same process, queries and events are much faster, as they do not have to be marshalled between processes, which means that large numbers of queries are quite fast.
NVDA can then perform single out-of-process queries for relevant information.
In-process code must be small and light-weight, as it is being injected into other processes.
It must also be as fast as possible to allow for maximum performance.
Python is unsuitable for this task.
All of NVDA's in-process code is written in C++, which allows for maximum performance and minimal overhead.
