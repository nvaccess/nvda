---
applyTo: **/*.cpp, **/*.h
description: This file describes the C++ code style for the project.
---

# C++ code guidelines for NVDA

## Security-specific review checks

NVDA operates with `UIAccess` privileges, injects code into other processes and handles untrusted data.
Scrutinize code for privilege escalation and data leaks.

* Untrusted input & web parsing:
  * Validate that parsing of external structures (HTML, ARIA attributes, UIA/IA2 properties) handles malformed, excessively long or deeply nested inputs safely without causing infinite loops or memory crashes.
* IPC and injected C++ code (`NVDAHelper`):
  * Ensure data sent via RPC or IPC from injected processes to the main NVDA process is strictly validated for length and type.
  * Flag unsafe string handling, missing bounds checks or improper buffer allocations.

## Architecture / performance checks

* Flag expensive operations (such as heavy computations, blocking I/O, complex loops) inside performance-critical hot paths like focus changes, key presses, or text iteration.
Watch for excessive COM calls (e.g. fetching properties individually inside a large loop instead of caching) and deep UIA tree walks on the main thread.
* Prioritise RAII, smart pointers for COM objects and lightweight execution inside injected hooks to prevent crashing target apps.
