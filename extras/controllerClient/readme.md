# NVDA Controller Client API 1.0 Documentation

## Introduction

This client API allows an application to communicate with NVDA, in order to do such things as speak text or braille a message.

The client API is implemented as a dll (dynamic link library). The functions in this dll can be called from any programming language that supports looking up and calling of any symbol in a dll (such as ctypes in Python), or by linking to it for languages like C and C++.

## What is Included?

Note: The header and library files are built along with nvdaHelper. If you want to build them yourself, please see readme.txt in the NVDA source distribution for instructions. Alternatively, you can find here a [pre-built package](http://www.nvda-project.org/nvdaControllerClient/nvdaControllerClient_20100219.7z).

Versions of the libraries and headers are supplied for both x86 and x64 applications. They have been split in to x86 and x64 directories, respectivly.

Each directory contains the following files, where * denotes 32 for x86 and 64 for x64:

*   nvdaControllerClient*.dll: the dll that contains all the functions. You can distribute this dll with your application.
*   nvdaControllerClient*.lib and nvdaControllerClient*.exp: The import and export libraries for nvdaControllerClient*.dll (used when linking with C/C++ code).
*   nvdaController.h: a C header file containing declarations for all the provided functions.

The x86 directory also contains three example files:

*   example_python.py: an example Python program that uses the NVDA controller client API.
*   example_c.c: The source code for an example C program that uses the NVDA controller client API.
*   example_csharp.cs: The source code for an example C# program that uses the NVDA controller client API.

## Available Functions

All functions in this dll return 0 on success and a non-0 code on failure. Failure could be due to not being able to communicate with NVDA or incorrect usage of the function. The error codes that these functions return are always standard Windows error codes.

For definitions of all the functions available, please see nvdaController.h. The functions are documented with comments.

## License

The NVDA Controller Client API is licensed under the GNU Lesser General Public License (LGPL), version 2.1\. In simple terms, this means you can use this library in any application, but if you modify the library in any way, you must contribute the changes back to the community under the same license.

Please see license.txt in this directory for more details.