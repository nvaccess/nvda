# NVDA Hardware Support Smoke Testing Plan

## Objective

To ensure NVDA installs and functions correctly on supported hardware configurations.
NVDA is currently migrating to only 64bit hardware support, and currently recommends not using 32bit hardware nor 32bit Windows.

## Notes

* Ensure all test results are documented, including screenshots or logs for failures.
* Focus on identifying edge cases and compatibility issues during the migration process.
* Prioritize testing on hardware configurations most commonly used by NVDA users.

## Generic Steps

1. Run the NVDA installer on the target hardware.
2. Verify successful installation and basic functionality.
Test using Edge, Notepad and the NVDA GUI.

## Hardware to consider

### 1. ARM Hardware

ARM Variations to consider:

* ARMv8 Architecture
* ARMv9 Architecture
* ARM A-Profile (Application Profile): ARMv9-A and ARMv8-A
* ARM R-Profile (Real-Time Profile): ARMv8-R
* ARM M-Profile (Microcontroller Profile): ARMv8-M
* Custom ARM Implementations (e.g., vendor-specific modifications of ARM cores)

### 2. x64 Hardware

x64 variations to consider:

* AMD64
* Intel 64

### 3. Virtual Machines

Virtual Machines to consider:

* Hyper-V
* VirtualBox
* VMWare
* Parallels

### 4. CoPilot PCs

CoPilot PCs use a new form of architecture known as an NPU.

## Other Testing: 32-bit Hardware

1. Run the NVDA installer on 32-bit hardware.
2. Observe and document the results.
    * Expected Result using 64bit NVDA: Installation fails gracefully with a clear message indicating that 32-bit systems are no longer supported.
    * Expected Result using 32bit NVDA: Installation occurs successfully
