Instructions for testing startup / shutdown.

### Start from shortcut
Prerequisites:
 - NVDA installed
 - Shortcut enabled during installation

Steps:
 1. Press (or emulate) Ctrl+Alt+N, observe NVDA starts up

Variation:
- At step 1. A version of NVDA is already running. Observe running version exits before installed version starts up.

### Windows Sign-in screen, automatic start
Prerequisites:
 - NVDA installed
 - Enable "Use NVDA during sign-in"

Steps:
 1. Sign out (not lock) Windows
 1. Observe NVDA announces the Windows sign-in screen

### UAC, automatic start
Prerequisites:
 - NVDA installed
 - An active Windows session (i.e. not signed out, locked)
 - The NVDA installed copy is running

Steps:
 1. Open the Start menu
 1. Type notepad
 1. Open context menu for notepad and choose `Run as Administrator`.
 1. When the UAC dialog appears, verify that NVDA launches on this secure desktop and reports the dialog.

### Windows Successful sign-in, automatic start
Prerequisites:
 - NVDA installed
 - Enable "Start NVDA after I sign in"

Steps:
 1. Start Windows
 1. Sign in
 1. Observe NVDA starts

### Running the *.exe

Steps:
 1. Press `win+r`
 1. Enter <path to nvda.exe>
 1. Press enter
 1. Observe NVDA starts

Variation:
- using an installer (launcher)
   -  eg: `C:\Users\username\Downloads\nvda_2021.1.exe`
- using an installed copy
   - just type `nvda` in place of the .exe
- using a portable copy
   - find and use the path to `nvda.exe`, located within the portable copy directory
   - the installer allows you to create an installed copy and a portable copy

### Running from source (runnvda.bat)
Prerequisites
- clone project and build NVDA (see [project readme](https://github.com/nvaccess/nvda/blob/master/readme.md#getting-the-source-code)).

Steps:
 1. Run `runnvda.bat` from cmd
 1. Observe NVDA starts

### An input gesture to restart

Prerequisite:
- Input gesture for "Restarts NVDA!" is assigned

Steps:
 1. Press (or emulate) the input gesture
 1. Observe that NVDA exits
 1. Observe that a new instance is started
