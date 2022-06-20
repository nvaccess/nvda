## NVDA Helper

Parts of NVDA Helper are used to capture and cache information, in-process, within web browsers and other applications.
This cache is called a virtual buffer.
While virtual buffers apply to several different application types, it may first be easiest to think about how they
work with browsers, the rest of this document will take a web browser centric view unless specified otherwise.

### Output
Internal code is built into several DLLs:
- `nvdaHelperLocal.dll`
- `nvdaHelperLocalWin10.dll`
- `nvdaHelperRemote.dll`
- Several COM proxy dlls
- `UIARemote.dll`

The `*local*.dll`'s are built for x86 (ie to match NVDA's arch), others are built for x86, x64, and arm64.

#### COM proxy dlls
Several COM Proxy DLLs are built from IDL files. A COM Proxy tells windows how to marshal data over COM when calling
 the target API interface.
For instance:
- IAccessible2 IDL files are built into `IAccessible2Proxy.dll`
- ISimpleDOM IDL files are built into `ISimpleDOM.dll`

#### nvdaHelperLocalWin10.dll
Contains code specific to Windows 10 and above, that aides in accessing newer technologies such as Windows OneCore speech synthesis, the Windows in-built OCR service.
This code is mostly C++/WinRT. 

#### nvdaHelperLocal.dll
This dll is loaded directly in to NVDA. It provides the following features:
*  client stub methods for several RPC interfaces allowing NVDA to execute code in-process. These interfaces include nvdaInprocUtils, vbufBackends, and displayModel, which are implemented in nvdaHelperRemote.dll.
* Server stub methods for several RPC interfaces allowing in-process code to execute code in NVDA. These interfaces include nvdaController and nvdaControllerInternal. 
* Functions to aide NVDA in hooking platform dlls to make their calls easier to cancel 
* Several small utility functions that assist in processing text (which are faster in c++).

#### NVDAHelperRemote.dll
This dll injects itself into other processes on the system, allowing for in-process code execution by NVDA.
It provides the following features:
* Server stub methods for several RPC interfaces, including NVDAInprocUtils, VBufBackends and displayModel.
* Client stub methods for several RPC interfaces, allowing in-process code to execute code back in NVDA. These interfaces include NVDAController and NVDAControllerInternal

#### UIARemote.dll
This dll is loaded by NVDA, providing utility functions that perform certain tasks or batch procedures on Microsoft UI Automation elements.
It makes use of the UI Automation Remote Operations capabilities in Windows 11, allowing to declaratively define code  to  access and manipulate UI Automation elements, that will be Just-In-Time compiled by Windows and executed in the process providing the UI Automation elements.

##### microsoft-ui-uiAutomation remote ops library
As a dependency of UIARemote.dll, the open source [Microsoft-UI-UIAutomation Remote Operations library](https://github.com/microsoft/microsoft-ui-uiautomation)  is also built.
This library contains both a low-level winrt API, and a higher-level pure C++ API which depends on the lower-level winrt API. UIARemote.dll tends to use the higher-level Operations abstraction API for its work.
In order for the winrt API to be available, UIARemote must register it with the Windows winrt platform. this involves loading a manifest file (See `microsoft-ui-uiautomation/Microsoft.UI.UIAutomation.dll.manifest`) and activating an activation context.

### Configuring Visual Studio
The following steps won't prepare a buildable solution, but it will enable intellisense.
You should still build on the command line to verify errors.

- Ensure you have built NVDA on the command line first.
- Create a new project from existing code
- Type: Visual C++, press next.
- Set the `<repo root>/nvdaHelper/` directory as the project file location.
- Project name: "nvdaHelper"
- Add files to the project from these folders: checked.
  - This should have a single 'checked' item, the path to nvdaHelper
- Other defaults are fine, press next
- Select "use external build system" for "How do you want to build the project?", press next
- Build command line: `scons source`
- Include search paths: `../include;../miscDeps/include;./;../build\x86_64;../include/minhook/include`
- Preprocessor definitions: `WIN32;_WINDOWS;_USRDLL;NVDAHELPER_EXPORTS;UNICODE;_CRT_SECURE_NO_DEPRECATE;LOGLEVEL=15;_WIN32_WINNT=_WIN32_WINNT_WIN7;`
- Forced Included files: `winuser.h`
- Press next
- Ensure "same as Debug configuration" is checked and press finish
- Open the project settings and change the following:
  - NMake -> Additional Options -> `/std:c++17`

#### To confirm these settings
- Build NVDA normally
- Look for lines in the build output that start with `cl`
  - EG
  ```
  cl /Fobuild\x86\vbufBackends\gecko_ia2\gecko_ia2.obj /c build\x86\vbufBackends\gecko_ia2\gecko_ia2.cpp
  /TP /EHsc /nologo /std:c++17 /Od /MT /W3 /WX
  /DUNICODE /D_CRT_SECURE_NO_DEPRECATE /DLOGLEVEL=15 /D_WIN32_WINNT=_WIN32_WINNT_WIN7 /DNDEBUG
  /Iinclude /Imiscdeps\include /Ibuild\x86
  /Z7
  ```
- This shows the:
  - defines beginning with `/D`
  - includes directories beginning with `/I`
  - Additional options like `/std:c++17`

### Virtual Buffer Backends

This code runs within the target applications process, it is responsible for building the virtual buffer.
The base classes are in the `storage.h` and `storage.cpp`.
The `storage` classes are implementation agnostic, they don't use the accessibility APIs directly and thus don't have
the same performance concerns as the code that directly interacts with the accessibility APIs,
such as the code in `gecko_ia2.cpp`.
A buffer (`VBufStorage_buffer_t`) has many `Nodes` that make up the document.
The `VBufStorage_buffer_t` class owns the *Node instances, such as `controlFieldNode` and `textFieldNode`.
The buffer (`VBufStorage_buffer_t`) is responsible for creating (in `fillVBuf`) and caching the nodes that make up the
document.
An element in a HTML document becomes a `controlFieldNode`.
The inner text of a HTML element would become a `textFieldNode`.
Extra information that we want to be able to present to the user is collected as these nodes are created.
For instance the name, description, role, and many other pieces of information.
A Node has a pointer to its parent node, child nodes, and sibling nodes, we have a graph of the virtual buffer.
Each `controlFieldNode` (like an element, remember?) has an identifier (`VBufStorage_controlFieldNodeIdentifier_t`).
Given an identifier, a `controlFieldNode` can be looked up using `controlFieldNodesByIdentifier`.
Though, take care, looking up nodes is only possible after that part of the tree has been rendered.
The `controlFieldNode`s are added to the buffer via `addControlFieldNode`, which also adds these nodes to the map.

### Gecko IA2

This is a virtual buffer backend implementation used for Firefox and Chrome.
When `fillVBuf` is called, it recursively descends through the child elements that we care about, creating either
`controlFieldNode`s or `textFieldNode`s for them.
This code is responsible for interacting with the IA2 accessibility API, these calls should be minimised for
 performance reasons.


### Overview of calling to remote code.

- NVDA's python code calls into the local DLL (`NVDAHelperLocal.dll`).
- Generated RPC Wrappers are called
- The RPC Wrappers call through to the "remote in-process DLL" (ie `nvdaHelperRemote.dll`)

#### Build notes
IDL/ACF files are input to MSRPCStubs to generate headers in `build/<arch>`
- See `MSRPCStubs` in `*scons*` files.
- Note these set a prefix, making whole word searches for methods difficult.