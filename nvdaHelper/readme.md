## NVDA Helper

Parts of NVDA Helper are used to capture and cache information, in-process, within web browsers and other applications.
This cache is called a virtual buffer.
While virtual buffers apply to several different application types, it may first be easiest to think about how they
work with browsers, the rest of this document will take a web browser centric view unless specified otherwise.

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


### Overview

- NVDA's python code calls into the (`NVDAHelperLocal.dll` / `NVDAHelperLocalWin10.dll`).
- Generated RPC Wrappers are called.
- The RPC Wrappers call through to the "remote in-process DLL" (`nvdaHelperRemote.dll`)

#### Build notes
IDL/ACF files are input to MSRPCStubs to generate headers in `build/<arch>`
- See `MSRPCStubs` in `*scons*` files.
- Note these set a prefix, making whole word searches for methods difficult.